# semgrepll - AI Agent Semantic Code Search Skill

Local semantic code search skill for AI coding agents. 100% offline capable.

## Supported Agents

| Agent | Config File | Install Command |
|-------|-------------|------------------|
| OpenClaw | clawhub.yaml | Via ClawHub skill registry |
| Claude Code | installers/claude_code.md | `pip install semgrepll` |
| Cursor | installers/cursor.json | `pip install semgrepll` |
| OpenCode | installers/opencode.json | `pip install semgrepll` |
| KiloCode | installers/kilo.json | `pip install semgrepll` |
| Windsurf | installers/windsurf.json | `pip install semgrepll` |
| Codex | installers/codex.json | `pip install semgrepll` |

## Quick Install (all agents)

```bash
pip install semgrepll
```

## Usage

```bash
# Index a project
semgrep index ./my-project

# Search semantically  
semgrep search "authentication"

# List indexed
semgrep ls
```

## Environment Variables

- `EMBED_BACKEND` - Backend: auto, llama, onnx, ollama
- `SEMGREP_BACKEND` - Storage: auto, sqlite, lance
- `LLM_MODEL_PATH` - Path to GGUF model (llama.cpp)
- `ONNX_MODEL_PATH` - Path to ONNX model

## For OpenClaw

Use ClawHub to install:
```bash
clh skill install semgrepll --token clh_kGzZkmMzlFFQOG7wuuZRMFmZkmlrelVNUrbZ1LvR0xA
```

Or manually copy SKILL.md to your skills folder.
