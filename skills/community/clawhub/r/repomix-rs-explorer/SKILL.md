---
name: repomix-rs-explorer
description: Pack a local or remote codebase with repomix-rs and analyze the generated output. Invoke for high-level exploration, structure summaries, or pattern discovery when targeted edits are not needed.
version: 2.0.0
---

# Repomix-rs Explorer

Use `repomix` (the `repomix-rs` CLI) to pack a codebase into a single AI-friendly file, then analyze it with agent tools.

## When to use

- Explore an unfamiliar local or remote repository
- Summarize structure, entry points, or module boundaries
- Find patterns (auth, routes, models, error handling) across many files
- Get token/file metrics before deciding what to read in detail

Use `repomix-context-skill` instead when a MindMesh index already exists at `.mind-mesh/agent/repomix.md`.

## Installation

### npm (recommended)

Package name is **`repomix-rs`**; the installed command is **`repomix`**.

```bash
# Global install — `repomix` available everywhere
npm install -g repomix-rs

# One-off run without global install
npx repomix-rs .

# Run the MCP server on stdio
npx -y repomix-rs --mcp
```

Supported platforms: Linux (x64, arm64), macOS (x64, arm64), Windows (x64). Node >= 18 required.

> If both the original TypeScript `repomix` and `repomix-rs` are installed globally, the last install wins the `repomix` command. Use `npx repomix-rs` or `npx repomix` explicitly if both are present.

### From source

```bash
# Install to ~/.cargo/bin/repomix
cargo install --path crates/cli

# Or build a release binary at ./target/release/repomix
cargo build --release
```

### Prerequisites

Git-related features (`--remote`, `--include-diffs`, `--include-logs`, sort-by-changes, MCP `pack_remote_repository`) shell out to the **`git`** executable on `PATH`. If `git` is missing, these features are skipped with a warning rather than failing the pack.

## Core commands

| Intent | Command |
|--------|---------|
| Pack current directory | `repomix .` |
| Pack a remote repository | `repomix --remote https://github.com/owner/repo --output /tmp/<name>.xml` |
| Pack with compression | `repomix --compress .` |
| Pack only specific files | `repomix --include "**/*.{ts,tsx}" --ignore "tests/**" .` |
| Markdown output | `repomix --style markdown --output /tmp/<name>.md .` |
| Include git diff/log | `repomix --include-diffs --include-logs .` |
| Start MCP server | `repomix --mcp` |
| Show all options | `repomix --help` |

Default output file is style-dependent (`repomix-output.xml`, `.md`, `.json`, or `.txt`). Always use `--output` to place the file where you expect.

## Agent workflow

1. **Pack**
   - Local: `repomix [ROOT]`
   - Remote: `repomix --remote <URL> --output /tmp/<repo>.xml`
   - Note the metrics printed by the command (files, characters, tokens, output path).

2. **Inspect structure**
   - Read the start of the output file for the file tree and metrics summary.
   - For large outputs, read with `offset`/`limit` rather than loading the whole file.

3. **Search patterns**
   - Use the agent's `Grep` tool on the output file, not shell `grep`.
   - Common patterns: `export.*function`, `export.*class`, `import.*from`, `router\.|route\.|endpoint`, `auth|login|jwt`, `model|schema|database`, `error|exception|try.*catch`.

4. **Read slices**
   - After locating a relevant `### path` or `<file path="...">` boundary, read that slice with `offset`/`limit`.

5. **Summarize**
   - Report metrics, top-level structure, and findings.
   - Cite output file paths and line numbers.
   - Suggest next steps for deeper exploration or targeted edits.

## Best practices

- **Remote repos**: always write to `/tmp` or a temp directory to avoid polluting the current workspace.
- **Large repos**: use `--compress` to extract signatures via tree-sitter and reduce token count.
- **Narrow scope**: use `--include` / `--ignore` before reading large outputs.
- **Output path**: explicitly pass `--output` so you know exactly where the pack lives.
- **Clean up**: delete large `/tmp` output files after analysis unless the user asks to keep them.
- **Security**: suspicious files are detected and excluded automatically; trust the exclusion list in the output report.

## Do not

- Use this skill for targeted file edits — pack, analyze, then switch to direct file tools.
- Read entire multi-megabyte output files into context; grep first, then read slices.
- Run `rm` on project files unless you are certain they are temporary output files you created.
- Confuse `repomix-rs` (Rust, npm package `repomix-rs`) with the original TypeScript `repomix` (npm package `repomix`).

## Error handling

| Symptom | Action |
|---------|--------|
| `repomix: command not found` | Install via `npm install -g repomix-rs` or use `npx repomix-rs`. |
| Remote clone fails | Verify the URL, network, and that `git` is on `PATH`. Try a local clone instead. |
| Output is too large | Re-run with `--compress`, narrower `--include`, or `--split-output <tokens>`. |
| Expected files missing | Check the file tree and ignored/excluded files section in the output report. |
| Git features missing | Ensure `git` is installed and the target is inside a git repository. |

## Resources

- Run `repomix --help` for the complete flag reference.
- Repository: https://github.com/sopaco/repomix-rs
- npm package: https://www.npmjs.com/package/repomix-rs
