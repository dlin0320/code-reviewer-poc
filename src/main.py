from config import config
from agent import Agent
import argparse
import os

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    os.makedirs("store", exist_ok=True)
    parser = argparse.ArgumentParser(description="Create embeddings from source code.")
    parser.add_argument("--action", "-a", choices=["embed", "review"], type=str, help="Action to perform.")
    parser.add_argument("--repo_path", "-s", type=str, help="Path to the source code directory.")
    parser.add_argument("--glob_patterns", "-g", type=str, help="Glob patterns to match files.")
    parser.add_argument("--language", "-l", type=str, help="Language of the source code.")
    parser.add_argument("--embedding_model", "-e", type=str, help="Text embedding model.")
    parser.add_argument("--vector_store_path", "-v", type=str, help="Path to store the vector store.")
    args = parser.parse_args()
    for arg, val in vars(args).items():
        if val and hasattr(config, arg):
            setattr(config, arg, val)

    config.validate()

    Agent.run()