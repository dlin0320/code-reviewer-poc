from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.document_loaders import DirectoryLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from config import config
from template import Template
import git
import os

class Agent:
    get_loader = lambda: DirectoryLoader(path=config.repo_path, glob=config.glob_patterns)

    get_splitter = lambda: RecursiveCharacterTextSplitter.from_language(language=config.language)

    get_embedding_model = lambda: OpenAIEmbeddings(model=config.embedding_model)

    get_review_model = lambda: ChatOpenAI(model=config.review_model, api_key=os.getenv("OPENAI_API_KEY"))

    @staticmethod
    def _create_embedding() -> None:
        loader = Agent.get_loader()
        splitter = Agent.get_splitter()
        model = Agent.get_embedding_model()

        loaded_documents = loader.load()

        split_documents = splitter.split_documents(documents=loaded_documents)

        store = FAISS.from_documents(documents=split_documents, embedding=model)

        store.save_local(folder_path=config.vector_store_path)

    @staticmethod
    def _review_code() -> None:
        review_model = Agent.get_review_model()
        embedding_model = Agent.get_embedding_model()
        store = FAISS.load_local(folder_path=config.vector_store_path, embeddings=embedding_model, allow_dangerous_deserialization=True)

        repo = git.Repo(config.repo_path)
        main_commit = repo.commit("main")
        new_commit = repo.commit(repo.active_branch.name)
        diff = main_commit.diff(new_commit, create_patch=True)
        diff_str = ""
        for d in diff:
            diff_content = d.diff.decode("utf-8") if isinstance(d.diff, bytes) else d.diff
            diff_str += diff_content + "\n"

        code = store.as_retriever().invoke(diff_str)
        code_str = "\n\n".join([c.page_content for c in code])
        template = Template.use(config.template_name)
        prompt = PromptTemplate.from_template(template=template)
        formatted_prompt = prompt.format(description=config.description, diff=diff_str, code=code_str, language=config.feedback_language)
        with open("out/prompt.txt", "w") as f:
            f.write(formatted_prompt)
        qa_chain = (
            {
                "description": RunnablePassthrough(),
                "diff": RunnablePassthrough(),
                "code": RunnablePassthrough(),
                "language": RunnablePassthrough(),
            }
            | prompt 
            | review_model 
            | StrOutputParser()
        )
        output = qa_chain.invoke({"description": config.description, "diff": diff_str, "code": code_str, "language": config.feedback_language})
        with open("out/feedback.md", "w") as f:
            f.write(output)

    @staticmethod
    def run() -> None:
        if config.action == 'embed':
            Agent._create_embedding()
        elif config.action == 'review':
            Agent._review_code()