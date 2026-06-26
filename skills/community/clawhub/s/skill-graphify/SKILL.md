---
name: skill-graphify
description: Turn any folder of code, docs, papers, or images into a queryable knowledge graph. Cross-platform wrapper for graphify CLI.
---

# Skill Graphify

Turn any folder of files into a navigable knowledge graph with community detection, honest audit trail, and three outputs: interactive HTML, queryable JSON, and a plain-language report.

## When to use

- User wants to understand a codebase they're new to
- User asks "how does X connect to Y" across many files
- User has a folder of papers/notes/screenshots and wants structure
- User wants a visual map of their project's architecture

## Usage

### Step 1 — Ensure graphify is installed

```bash
python graphify_wrapper.py ensure-installed
```

Or manually: `pip install graphifyy`

### Step 2 — Build knowledge graph

```bash
python graphify_wrapper.py build /path/to/project
```

This runs the full pipeline: detect files → AST extraction → build graph → cluster → export.

Output goes to `<project>/graphify-out/`:
- `graph.html` — interactive visualization (open in browser)
- `GRAPH_REPORT.md` — plain-language audit report
- `graph.json` — queryable knowledge graph
- `cache/` — SHA256 cache for incremental updates

### Step 3 — Read the report

```bash
python graphify_wrapper.py report
```

Or read `graphify-out/GRAPH_REPORT.md` directly. Present the key findings to the user: god nodes (highly connected), surprising connections, community structure.

### Step 4 — Query the graph (optional)

```bash
python graphify_wrapper.py query "how does authentication work"
```

Or use the CLI directly for more options:

```bash
graphify query "show the auth flow" --graph graphify-out/graph.json
graphify query "what connects X to Y?" --graph graphify-out/graph.json --dfs
graphify query "explain dependency injection" --budget 1500 --graph graphify-out/graph.json
```

### Send results to user

After building, send `graphify-out/graph.html` to the user so they can explore the interactive graph. Summarize `GRAPH_REPORT.md` in your response.

## CLI reference (graphify)

If `graphify` CLI is available, you can use these directly:

| Command | Description |
|---------|-------------|
| `graphify query "..." --graph <path>` | BFS traversal of the graph |
| `graphify query "..." --dfs --graph <path>` | DFS — trace a specific path |
| `graphify query "..." --budget N --graph <path>` | Cap output at N tokens |
| `graphify path "Node1" "Node2" --graph <path>` | Shortest path between concepts |
| `graphify explain "NodeName" --graph <path>` | Plain-language explanation of a node |

## Supported file types

- **Code:** 20 languages via tree-sitter (Python, JS, TS, Go, Rust, Java, C, C++, Ruby, C#, Kotlin, Scala, PHP, Swift, Lua, Zig, PowerShell, Elixir, Objective-C, Julia)
- **Docs:** Markdown, text, reStructuredText
- **Papers:** PDF
- **Images:** Screenshots, diagrams, whiteboard photos (requires vision-capable LLM)

## Notes

- The wrapper script (`graphify_wrapper.py`) handles cross-platform compatibility (Windows CMD, Linux, macOS)
- graphify's AST extraction is deterministic and requires no LLM — it's free and fast
- Semantic extraction (docs, images) uses LLM subagents if available, otherwise is skipped
- Every edge is tagged EXTRACTED, INFERRED, or AMBIGUOUS — you always know what was found vs guessed
- Incremental updates: re-running on the same folder only processes changed files (cache-based)
- Add a `.graphifyignore` file (same syntax as `.gitignore`) to exclude directories

## Dependencies

- Python 3.10+
- `graphifyy` (pip) — automatically installed by wrapper
