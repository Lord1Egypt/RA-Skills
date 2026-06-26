---
name: semanticfs
description: Search your local filesystem and codebase semantically. Use instead of grep/find/ls/cat chains when looking for files, functions, symbols, or code patterns. Returns exact file paths, line numbers, and code snippets. Much faster and uses far fewer tokens than manual file exploration.
version: 1.0.0
homepage: https://github.com/Navneeth08k/semanticFS
metadata:
  openclaw:
    requires:
      bins:
        - semanticfs
      os:
        - linux
        - darwin
        - win32
user-invocable: true
---

# SemanticFS Skill

SemanticFS provides semantic search over your local filesystem. Instead of running multiple grep/find/ls/cat commands to locate code or files, ask SemanticFS once and get back exact paths and line ranges.

## When to use

Use this skill whenever you need to:
- Find a file, function, class, or symbol by name or description
- Locate where a concept is implemented (e.g. "authentication logic", "error handling for uploads")
- Navigate an unfamiliar codebase without reading every file
- Replace a chain of `grep`, `find`, `ls`, or `cat` commands

Do **not** use this skill if:
- The directory hasn't been indexed yet (run `semanticfs index build` first)
- You need to write or modify files (SemanticFS is read-only)

## Prerequisites

SemanticFS must be installed and the target directory must be indexed:

```bash
# Install (Linux/macOS)
curl -sSfL https://raw.githubusercontent.com/Navneeth08k/semanticFS/main/scripts/install.sh | bash

# Index your workspace
semanticfs --config ~/semanticfs.toml index build
```

## Starting the server

SemanticFS must be running before you can search:

```bash
# Start HTTP server (runs in background)
semanticfs --config ~/semanticfs.toml serve mcp &

# Check it's up
curl -s http://localhost:9464/health/live && echo "SemanticFS is running"
```

If you get a connection refused error, the server is not running. Start it with the command above.

## Searching the codebase

Replace `grep -r "pattern" .` with:

```bash
curl -s -X POST http://localhost:9464/search \
  -H "Content-Type: application/json" \
  -d '{"query": "YOUR QUERY HERE", "limit": 10}' \
  | python3 -c "
import sys, json
data = json.load(sys.stdin)
for r in data.get('hits', []):
    print(f\"{r['path']}:{r['start_line']}-{r['end_line']}  {r.get('snippet','')[:100]}\")
"
```

**Example queries:**
- `"Python function signature extraction"`
- `"CLI argument parsing entry point"`
- `"database connection pool"`
- `"error handling file upload"`
- `"AuthService login method"`

## Getting a directory map

Replace `ls -la src/` or `tree src/` with:

```bash
curl -s "http://localhost:9464/map?path=src" \
  | python3 -c "import sys, json; print(json.dumps(json.load(sys.stdin), indent=2))"
```

Use `path=.` for the workspace root.

## Output format

Search results are returned as:
```
path/to/file.py:40-95  extract_signatures_python — extracts function signatures from...
```

Each result includes:
- **path**: file path relative to workspace root
- **start_line / end_line**: exact line range containing the relevant code
- **snippet**: short excerpt of the matching content

Always read the specific lines from the file to verify before acting on them.

## Guardrails

- SemanticFS is **read-only** — it never modifies files
- Only searches directories that have been indexed (`semanticfs index build`)
- If results look wrong, re-run `semanticfs index build` to refresh
- Index automatically includes only source files (excludes node_modules, .venv, target/, .git, etc.)

## Troubleshooting

**No results returned:**
- Check the index was built: `semanticfs --config ~/semanticfs.toml health`
- Try a broader query (e.g. "authentication" instead of "JWT token refresh logic")

**Connection refused:**
- Start the server: `semanticfs --config ~/semanticfs.toml serve mcp &`

**Stale results after code changes:**
- Re-index: `semanticfs --config ~/semanticfs.toml index build`
- Or run incremental update: `semanticfs --config ~/semanticfs.toml index update`

**Diagnose the full setup:**
```bash
semanticfs --config ~/semanticfs.toml doctor
```
