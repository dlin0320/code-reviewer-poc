import json
import os

TEMPLATE_PATH = 'template'

class Template:
    new_feature: dict = {
        "description": "Basic prompt for a new feature PR.",
        "content": (
            "You are a senior engineer tasked with reviewing a Pull Request.\n"
            "\nPR Type: New Feature\n"
            "\nDescription: {description}\n"
            "\nPR Diff:\n"
            "{diff}\n"
            "\nRelavent Code Snippet:\n"
            "{code}\n"
            "\nRequirement:\n"
            "1. The feature is implemented correctly.\n"
            "2. The code is clean and maintainable.\n"
            "3. Provide feedback in {language}.\n"
            "\nFeedback Guideline:\n"
            "1. Use markdown.\n"
            "2. Be clear and concise.\n"
        )
    }

    bug_fix: dict = {
        "description": "Basic prompt for a bug fix PR.",
        "content": (
            "You are a senior engineer tasked with reviewing a Pull Request.\n"
            "PR Type: Bug Fix\n"
            "Description: {description}\n"
            "PR Diff:\n"
            "{diff}\n"
            "Relavent Code Snippet:\n"
            "{code}\n"
            "Requirement:\n"
            "1. The bug is resolved.\n"
            "2. The code is clean and maintainable.\n"
            "3. Provide feedback in {language}.\n"
            "Feedback Guideline:\n"
            "1. Use markdown.\n"
            "2. Be clear and concise.\n"
        )
    }

    @classmethod
    def _load(cls, name: str) -> dict:
        name = name + '.json' if not name.endswith('.json') else name
        with open(os.path.join(TEMPLATE_PATH, name), 'r') as f:
            return json.load(f)
        
    @classmethod
    def use(cls, name: str) -> str:
        if hasattr(cls, name):
            return getattr(cls, name)['content']
        else:
            if content := cls._load(name).get('content', ''):
                return content
            else:
                raise ValueError(f"Template {name}.content is invalid")