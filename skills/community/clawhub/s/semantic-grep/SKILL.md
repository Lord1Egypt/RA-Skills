# semgrepll - Local Semantic Code Search

## Description
Local semantic grep using embeddings - 100% offline capable with llama.cpp, ONNX, and Ollama backends. Use when searching code semantically, finding code by meaning, or indexing projects for AI-powered search.

## Triggers
- "search code semantically"
- "find code by meaning"  
- "semantic grep"
- "index project for search"
- Commands: semgrep index, semgrep search

## Actions
- Index projects: `semgrep index /path/to/project`
- Search: `semgrep search "query"`
- List: `semgrep ls`
- Remove: `semgrep rm <project>`

## Environment Variables (optional)
| Variable | Default | Description |
|-----------|---------|-------------|
| EMBED_BACKEND | auto | Backend: llama, onnx, ollama |
| LLM_MODEL_PATH | - | Path to GGUF model (llama.cpp) |
| ONNX_MODEL_PATH | auto | Path to ONNX model |
| SEMGREP_BACKEND | auto | Storage: sqlite, lance |
| EMBED_MODEL | mxbai-embed-large-v1 | Embedding model |

## Installation
```bash
pip install semgrepll
# Optional: ONNX support
pip install semgrepll[onnx]
```

## Examples
- "Index my project for semantic search" → runs `semgrep index ./project`
- "Find authentication code" → runs `semgrep search "authentication"`
- "Search for payment processing" → runs `semgrep search "payment processing"`

## Requirements
- Python 3.10+
- One of: llama-cpp-python, onnxruntime, or Ollama running locally

## Notes
- 100% offline - no external API calls
- Auto-detects fastest available backend
- Embeddings cached for fast re-indexing
