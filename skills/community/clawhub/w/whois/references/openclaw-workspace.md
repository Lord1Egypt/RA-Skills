# OpenClaw Workspace Guide

## Instance Types

OpenClaw can run as a container or directly on the host:

### Container Instance (`containerId` is set)
- Runs in Docker container (image: `alpine/openclaw:latest`)
- File operations via `docker exec`
- Workspace inside container: `/home/node/.openclaw/workspace/`
- Agent workspaces: `/workspace/{agentId}/` (Docker volume mount)
- Python: 3.11.2, uv pre-installed, pip3 available

### External Instance (`workspacePath` is set, `containerId` is null)
- Runs on host machine (e.g., `~/.openclaw`)
- File operations via direct filesystem
- Workspace at `{workspacePath}/` (the `.openclaw` directory)
- Agent workspace MD files at `{workspacePath}/workspace/` (or `workspace-{profile}/`)
- Python/uv depends on host environment

### How to Distinguish

```
containerId != null  →  Container instance  →  Use docker exec
workspacePath != null  →  External instance  →  Use filesystem
```

## Python Environment Setup

### Container Instance
- Python 3.11.2 at `/usr/bin/python3`
- uv 0.10.6 at `/usr/local/bin/uv`
- pip3 23.0.1 at `/usr/bin/pip3`
- Home: `/home/node/`

### Host Environment (macOS example)
- System Python 3.9.6 at `/usr/bin/python3`
- uv at `/opt/homebrew/bin/uv` (via Homebrew)

### TOOLS.md Python Section Template
```markdown
## Python Environment
- Package manager: `uv` (preferred over pip/pip3)
- Create venv: `uv venv .venv`
- Install package: `uv pip install <package>`
- Run script: `uv run python script.py`
- NEVER use `pip install` directly — always use `uv`
- If `uv` is missing, install: `curl -LsSf https://astral.sh/uv/install.sh | sh`
```

## Agent Creation Rules

### Agent ID Format
- Regex: `^[a-z0-9][a-z0-9_-]*$` (1-50 chars)
- Lowercase alphanumeric, hyphens, underscores
- Must start with letter or digit
- Examples: `main`, `internet`, `dev-assistant`, `code_review`

### Workspace Path Conventions
- Container default agent: `/workspace/default/`
- Container named agent: `/workspace/{agentId}/`
- External default: `~/.openclaw/workspace/`
- External named agent: `~/.openclaw/workspace-{agentId}/`

### Non-Main Agent Workspaces
Each agent gets an **independent workspace**. Files, venvs, and memory are per-agent.
System tools (python, uv, brew) are shared across agents on the same instance.

When initializing a non-main agent, the workspace MD files need to be written to
the agent's own workspace directory, not the default workspace.

## Config Patch Behavior

- `config.patch` uses **union merge** for `agents.list` — send only new entries
- Every `config.patch` triggers OpenClaw restart via SIGUSR1 (~10-20s downtime)
- `config.get` returns `__OPENCLAW_REDACTED__` for secrets — NEVER send these back
- Container must have `restart: unless-stopped` to survive SIGUSR1
