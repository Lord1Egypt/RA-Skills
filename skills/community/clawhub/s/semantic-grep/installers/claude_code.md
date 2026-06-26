# semgrepll for Claude Code

## Installation
```bash
pip install semgrepll
```

## Usage in Claude Code

Use semgrepll when you need to:
- Search code semantically (find by meaning, not just keywords)
- Index a project for AI-powered search
- Find related code across a codebase

### Commands
```bash
# Index a project
semgrep index ./my-project

# Search semantically
semgrep search "authentication logic"

# List indexed projects
semgrep ls
```

### Environment (optional)
```bash
export EMBED_BACKEND=auto    # llama, onnx, or ollama
export SEMGREP_BACKEND=sqlite # or lance for large projects
```

## Example Prompts
- "Index this project with semgrepll"
- "Find all authentication-related code using semgrep"
- "Search for payment processing logic semantically"
