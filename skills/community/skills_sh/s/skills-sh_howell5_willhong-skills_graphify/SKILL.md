---
name: graphify
description: "Use when exploring unfamiliar codebases, before searching for code, or after editing files. Builds a structural AST index (classes, functions, imports, call graph) from 12 languages via tree-sitter. Trigger: /graphify"
allowed-tools: Bash(graphify:*)
---

# graphify — Code Navigation Layer

Structural index of the codebase. Know what exists, where, and how it connects — before you grep.

**Requires CLI:** `npm i -g graphify-ts` (uses Bun runtime).

**Manual updates only.** The graph does not refresh on its own — you (or the user) run `graphify update` or `graphify build` when you want a fresh index. This avoids write conflicts in git worktrees and other multi-session setups.

## First-time setup (one-time per machine)

```bash
npm i -g graphify-ts    # install CLI
```

Then, once per project:

```bash
graphify build .
```

After that, refresh manually whenever the index drifts from the code (see `graphify update` below).

## Commands

### `/graphify build` — Build index (first time, or full rebuild)

```bash
graphify build .
```

Scans all source files, extracts AST structure, saves to `graphify-out/graph.json`.

Report: "Indexed {files} files, {nodes} symbols, {edges} relationships"

### `/graphify query <name>` — Search for symbols

```bash
graphify query graphify-out/graph.json <name>
```

Case-insensitive search. Returns matching symbols with file locations.

### `/graphify update <files...>` — Incremental update after edits

```bash
graphify update graphify-out/graph.json <file1> [file2...]
```

Re-extract only the specified files. Run this after editing code if you plan to query the graph again in the same session.

### `/graphify auto-update` — Bulk update from git diff

```bash
graphify auto-update [dir]
```

Computes changed code files via `git diff` + untracked files, then calls `updateIndex`. Silent when there's nothing to do. Convenient for refreshing after a batch of edits without naming each file.

## When to Use

**Before searching code:** If `graphify-out/graph.json` exists, query it before Glob or Grep. The graph tells you which files contain which symbols. This is the main value — replace blind keyword search with structured lookup.

**After editing:** If you'll query the graph again in the same session, run `graphify update <edited-files>` (or `graphify auto-update` for a bulk refresh). Otherwise leave it — the next `graphify build` or update will catch up.

**Exploring unfamiliar code:** Run `/graphify query <concept>` to find entry points without guessing filenames.

## Supported Languages

Python, JavaScript, TypeScript (JSX/TSX), Go, Rust, Java, C, C++, Ruby, C#, Kotlin, Scala, PHP

## Graph Output

Saved as `graphify-out/graph.json`:

```json
{
  "nodes": [{ "id": "main::app", "label": "App", "sourceFile": "main.py", "sourceLocation": "main.py:5" }],
  "edges": [{ "source": "file::main", "target": "main::app", "relation": "contains", "confidence": "EXTRACTED" }],
  "metadata": { "files": 10, "nodes": 45, "edges": 62 }
}
```

Edge relations: `contains`, `method`, `imports`, `imports_from`, `calls` (INFERRED), `inherits`
