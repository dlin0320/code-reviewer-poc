from dotenv import load_dotenv
import json
import os

DEFAULT_ACTION = "review"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_VECTOR_STORE_PATH = "store"
DEFAULT_REVIEW_MODEL = "o1-mini"
DEFAULT_TEMPLATE_NAME = "new_feature"
DEFAULT_FEEDBACK_LANGUAGE = "en"

class Config:
    action: str
    repo_path: str 
    glob_patterns: list[str]
    language: str
    embedding_model: str
    vector_store_path: str
    review_model: str
    template_name: str
    description: str
    feedback_language: str

    def __init__(self) -> None:
        load_dotenv()
        self.action = os.getenv("ACTION") or DEFAULT_ACTION
        self.repo_path = os.getenv("REPO_PATH")
        self.glob_patterns = os.getenv("GLOB_PATTERNS").split(",")
        self.language = os.getenv("LANGUAGE")
        self.embedding_model = os.getenv("EMBEDDING_MODEL") or DEFAULT_EMBEDDING_MODEL
        self.vector_store_path = os.getenv("VECTOR_STORE_PATH") or DEFAULT_VECTOR_STORE_PATH
        self.review_model = os.getenv("REVIEW_MODEL") or DEFAULT_REVIEW_MODEL
        self.template_name = os.getenv("TEMPLATE_NAME") or DEFAULT_TEMPLATE_NAME
        self.description = os.getenv("DESCRIPTION")
        self.feedback_language = os.getenv("FEEDBACK_LANGUAGE") or DEFAULT_FEEDBACK_LANGUAGE

    def validate(self) -> None:
        # Common required config
        if not self.repo_path:
            raise ValueError("Config.repo_path")
        if not self.embedding_model:
            raise ValueError("Config.embedding_model")
        if not self.description:
            raise ValueError("Config.description")

        # Action specific required config
        if self.action == 'embed':
            if not self.glob_patterns:
                raise ValueError("Config.glob_patterns")
            if not self.language:
                raise ValueError("Config.language")
            if not self.vector_store_path:
                raise ValueError("Config.vector_store_path")
        elif self.action == 'review':
            if not self.review_model:
                raise ValueError("Config.review_model")
        else:
            raise ValueError("Config.action")
        
        with open("out/config.json", "w") as f:
            f.write(json.dumps(self.__dict__, indent=4))

config = Config()