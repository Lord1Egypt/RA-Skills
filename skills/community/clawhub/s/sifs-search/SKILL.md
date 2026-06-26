---
name: sifs-search
description: Use this skill when you need to find code in a local checkout or Git source by behavior, intent, symbol, file path, related implementation, or indexed chunk context. Use it before broad file reads or grep-style sweeps for exploratory codebase questions, architecture tracing, call-site discovery, and "where/how is X implemented?" tasks. Do not use it for general web search or non-code files unless the user asks to search a source tree.
license: MIT
compatibility: Requires the local `sifs` binary on PATH. Works in OpenClaw/Hermes-style agent runtimes with shell access on macOS/Linux; MCP tools are optional.
metadata: {"openclaw":{"version":"0.1.0","os":["darwin","linux"],"requires":{"bins":["sifs"]},"install":[{"id":"brew","kind":"brew","label":"Install SIFS with Homebrew","tap":"tristanmanchester/tap","formula":"sifs","bins":["sifs"]},{"id":"cargo","kind":"cargo","label":"Install SIFS with Cargo","package":"sifs","bins":["sifs"]}]}}
---

Use SIFS from the shell when you need codebase context. The CLI is the reliable path; MCP tools are optional and should only be used when they are visible in the current agent session.

## When to Use

- Use for local code search, symbol discovery, behavior tracing, related-code lookup, and indexed file/chunk inspection.
- Use before reading many files by hand when the task starts with "where is...", "how is...", "find the implementation...", or "what code handles...".
- Do not use for general web research, package documentation lookup, or non-code document search unless the user explicitly points SIFS at a source tree.

Start by discovering the local contract:

```bash
sifs agent-context --json
```

Search by intent, behavior, symbol, or exact text:

```bash
sifs search "authentication flow" --source <project>
sifs search "save_pretrained" --source <project> --mode bm25
sifs search "save model to disk" --source <project> --limit 10
```

Inspect indexed files and chunks before reading broad files:

```bash
sifs list-files --source <project> --limit 200 --json
sifs get src/auth.rs 42 --source <project>
sifs find-related src/auth.rs 42 --source <project>
```

Use `--source <project>` when the agent may not be running from the target checkout. Use `--filter-path <repo-relative-path>` for path narrowing and `--limit` for bounded results.

If MCP tools named `search`, `get_chunk`, or `list_files` are visible, they may be used for the same workflow. If they are missing, configured-but-invisible, or failing, fall back to the CLI immediately.

Bundled support files:

- `references/commands.md` contains command recipes.
- `references/mcp.md` explains MCP fallback rules.
- `references/troubleshooting.md` covers setup and stale-instruction checks.
- `scripts/check-setup.sh` verifies that `sifs` is on `PATH` and can print the agent contract.
