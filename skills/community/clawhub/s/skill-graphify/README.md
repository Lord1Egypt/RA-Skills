# skill-graphify

Universal skill wrapper for [graphify](https://github.com/safishamsi/graphify) — turn any folder of code, docs, papers, or images into a queryable knowledge graph.

## What it does

Wraps the graphify CLI into a cross-platform skill that works on any AI agent platform (nanobot, OpenClaw, Claude Code, Cursor, etc.). Handles installation, graph building, querying, and report reading — no bash-isms, no platform-specific tricks.

## Quick start

```bash
# Install graphify
python graphify_wrapper.py ensure-installed

# Build a knowledge graph from any folder
python graphify_wrapper.py build /path/to/project

# Read the audit report
python graphify_wrapper.py report

# Query the graph
python graphify_wrapper.py query "how does auth work?"
```

Output lives in `graphify-out/`:
- `graph.html` — interactive visualization
- `GRAPH_REPORT.md` — plain-language audit report  
- `graph.json` — queryable knowledge graph

## Why a wrapper?

graphify's native skill.md is 8KB+, uses bash-specific syntax (`$()` subshells, `which`, `mkdir -p`), and requires multi-step orchestration with parallel subagents. This wrapper provides:

- **Cross-platform** — works on Windows CMD, PowerShell, Linux, macOS
- **Single entry point** — one Python script handles everything
- **Graceful fallbacks** — tries CLI first, falls back to Python API
- **Clean output** — presents results without requiring the agent to orchestrate subagents

## Supported file types

- **Code:** 20 languages via tree-sitter (Python, JS, TS, Go, Rust, Java, C, C++, Ruby, C#, Kotlin, Scala, PHP, Swift, Lua, Zig, PowerShell, Elixir, Objective-C, Julia)
- **Docs:** Markdown, text, reStructuredText
- **Papers:** PDF
- **Images:** Screenshots, diagrams, whiteboard photos

## Requirements

- Python 3.10+
- `graphifyy` pip package (auto-installed by wrapper)

## License

MIT
