---
name: scopecheck
description: "Analyze an OpenClaw SKILL.md and extract its permission scope — what env vars, CLI tools, filesystem paths, and network URLs it accesses. Compares declared requirements against actual usage and flags undeclared access."
metadata: {"openclaw":{"emoji":"🔬","requires":{"bins":["python"]},"install":[{"id":"pip","kind":"uv","packages":["fastapi","uvicorn","pydantic","pyyaml"]}]}}
---

# ScopeCheck

Find out what a skill actually accesses vs what it claims to need.

## Start the server

```bash
uvicorn scopecheck.app:app --port 8002
```

## Check a skill's scope

```bash
curl -s -X POST http://localhost:8002/v1/check-scope \
  -H "Content-Type: application/json" \
  -d "{\"skill_content\": $(cat path/to/SKILL.md | jq -Rs)}" | jq
```

Returns `declared` (env vars and bins from metadata), `detected` (what the skill actually references), and `undeclared_access` (detected but not declared — potential risk).

## What it extracts

- **env_vars** — environment variables like $HOME, $API_KEY
- **cli_tools** — binaries used in Run/Execute commands
- **filesystem_paths** — /etc/hosts, ~/.ssh/config, etc.
- **network_urls** — any http/https URLs referenced

## Undeclared access format

Each undeclared item is prefixed with its type: `env:SECRET_KEY`, `bin:curl`, `fs:/etc/passwd`, `net:https://example.com`.
