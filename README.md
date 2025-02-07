# Project Description
A Proof of Concept for code review with OpenAI's embedding and reasoning models.

## Installation
```bash
pip install -r requirements.txt
```

## Setup
1. Provide a valid OPENAI_API_KEY in environment variable.

## Usage
To embed a codebase, run the following command:
```bash
python src/main.py --repo_path /path/to/repo --glob_patterns "pattern1,pattern2" --languange codebase_language
```

Vector database for the embedding can be found in /store upon successful execution, which must exist before starting a review.

To start a review, run the following command:

```bash
python src/main.py --repo_path /path/to/repo
```

Used config, prompt and returned feedback can be found in /out upon successful execution.

## Custom Template
Create custom templates in the template folder and update the env to use it.