---
name: symdex-code-search
description: |
  This skill should be used when finding, tracing, or understanding code in a repository
  with SymDex available. Trigger it for requests like "where is this defined?", "who
  calls this?", "what route handles this path?", "show me the file outline", "search
  this codebase by intent", or any task that would otherwise rely on broad Read/Grep/Glob
  exploration.
---

# SymDex Code Search

Use SymDex before broad file browsing.
Use it to save tokens by retrieving the exact code the agent needs instead of scanning whole files.
SymDex currently covers 21 language surfaces, including Python, Go, Kotlin, Dart, Swift, HTML, CSS, Shell, Vue/Svelte script blocks, and Markdown headings plus supported fenced code blocks.

## Current SymDex Snapshot

- Package version: `0.1.26`
- Latest public tag: `v0.1.26`
- MCP tool surface: 21 tools
- Language coverage: 21 language surfaces, including Android/Kotlin, Flutter/Dart, iOS/Swift, HTML, CSS-family stylesheets, Shell, Vue/Svelte script blocks, Markdown headings, and supported fenced code blocks
- Route extraction: Python, JavaScript/TypeScript, Spring/Kotlin, Laravel, Gin-style Go, ASP.NET, Rails/Sinatra, Phoenix, and Actix
- Search outputs: one-line CLI token-savings footers plus MCP `roi`, `roi_summary`, and `roi_agent_hint`
- Quality outputs: MCP results and CLI JSON include `quality` with confidence, freshness, parser mode, language surface, generated-file hints, and embedding availability
- Context packs: CLI `symdex pack` and MCP `build_context_pack` assemble token-budgeted evidence bundles for broader feature questions
- Semantic backends: local `sentence-transformers`, Voyage, OpenAI-compatible `/embeddings`, Gemini, and compatible proxies
- Hosted embedding support: `SYMDEX_EMBED_RPM` plus `symdex index --lazy` for foreground structural indexing with background embedding fill
- No-embedding mode: `symdex index --no-embed` skips semantic embedding work entirely
- Watch behavior: low-memory structural refresh by default; use `symdex watch --embed` only when semantic embeddings must refresh continuously
- State model: global `~/.symdex` by default, optional workspace-local `./.symdex` with `registry.json`
- Markdown support: `.md`, `.markdown`, and `.mdx` headings plus supported fenced code blocks are indexed alongside source files

## Start Here

1. If the SymDex CLI reports a newer release, prefer upgrading before long sessions.
2. Confirm the repo id.
3. If the repo id is already known, pass `repo` on every scoped tool call.
4. If the repo id is unknown, call `list_repos` and match the current worktree.
5. Check freshness with `get_index_status(repo)`.
6. If the current worktree is not indexed, call `index_folder(path=".")`.
7. If the workspace already has `.symdex`, treat it as the intended local SymDex state and reuse it.
8. Reuse the returned `repo` id for the rest of the task.

If SymDex is unavailable or indexing fails, say so clearly and fall back to normal file reads only as needed.

## Core Rules

- Search first.
- Pass `repo` whenever you know it.
- Use `build_context_pack` for broad "how does this feature work?", docs, API, or bug-investigation questions before issuing many separate narrow searches.
- Prefer `get_symbol` or `get_file_outline` over full-file reads.
- Use call graph and route tools before manual tracing.
- Re-check `get_index_status` after major edits or worktree switches.
- Read full files only when editing, reviewing unsupported or generated content, or when SymDex cannot answer.
- Optimize for lower-token retrieval, not broad context loading.
- If a search tool returns `roi`, `roi_summary`, or `roi_agent_hint`, mention the approximate token savings briefly in your response.
- Inspect `quality` before reasoning from a result. Prefer fresh, parser-backed, high-confidence evidence; warn the user when evidence is stale, generated, fallback text, or missing embeddings.
- If the repo uses workspace-local SymDex state (`./.symdex`), stay inside that workspace so the same index is auto-discovered.
- Treat `symdex watch` as low-memory by default; only request `--embed` when semantic embeddings must refresh on file changes.
- For remote embedding providers with strict request limits, prefer `symdex index --lazy` and set `SYMDEX_EMBED_RPM` instead of blocking an agent session on a long foreground embedding run.

## Tool Selection

| Need | Tool |
|------|------|
| Index the current worktree | `index_folder` |
| Register and index a repo explicitly | `index_repo` |
| Find a function, class, or method by name | `search_symbols` |
| Find code by intent or behavior | `semantic_search` |
| Find literal text or regex matches | `search_text` |
| Build a query-shaped evidence bundle | `build_context_pack` |
| Read exact source for one symbol | `get_symbol` |
| Get a file outline before reading | `get_file_outline` |
| Get a repo map or summary | `get_repo_outline` or `get_file_tree` |
| Trace who calls a symbol | `get_callers` |
| Trace what a symbol calls | `get_callees` |
| Find HTTP routes | `search_routes` |
| Check repo freshness | `get_index_status` |
| Get code metrics and language mix | `get_repo_stats` |
| List indexes | `list_repos` |
| Clean deleted-worktree indexes | `gc_stale_indexes` |

## Typical Flow

1. Confirm the repo id and freshness.
2. Index with `index_folder` if needed.
3. For broad feature, API, docs, or bug-investigation questions, start with `build_context_pack`.
4. For narrow lookups, start with `search_symbols`, `semantic_search`, or `search_text`.
5. Narrow to `get_symbol` or `get_file_outline`.
6. Check `quality` fields on returned items before making code-understanding claims.
7. Use `get_callers`, `get_callees`, `search_routes`, or `get_repo_stats` for deeper analysis.
8. Fall back to direct file reads only when SymDex cannot answer precisely enough.

## Decision Guide

- "Where is X defined?" -> `search_symbols`
- "What does this do?" -> `semantic_search`, then `get_symbol`
- "How does this feature work?" -> `build_context_pack`
- "Gather evidence before documenting this API" -> `build_context_pack` with `include=["routes", "docs", "tests"]`
- "Who uses this?" -> `get_callers`
- "What does this call?" -> `get_callees`
- "Where is the endpoint?" -> `search_routes`
- "Show me the file structure first" -> `get_file_outline`
- "Give me a repo-level picture" -> `get_repo_outline` or `get_repo_stats`
- "Is the index current?" -> `get_index_status`

## Good Trigger Phrases

- "Find the function that validates JWTs"
- "Who calls this route handler?"
- "Show me the outline of this file"
- "Search for the code that parses webhook payloads"
- "Find the HTTP route for `/api/checkout`"
- "Give me the repo summary before I edit anything"
- "Find the code path that might explain this bug"
- "Check whether this logic is coherent across callers and callees"
- "Build a context pack for this feature"

## Bug And Logic Investigation

Use SymDex as evidence retrieval, not as proof by itself.

1. Start with the symptom, route, function, or text clue.
2. Use `build_context_pack` when the bug spans multiple symbols, routes, docs, or tests.
3. Retrieve the exact symbol, route, caller chain, callee chain, and relevant docs.
4. Inspect `quality.index_fresh`, `quality.confidence`, `quality.parser_mode`, `quality.is_generated`, and `quality.has_embeddings`.
5. If evidence quality is weak, say what is missing before claiming a bug.
6. Cite the concrete symbol, file, route, or call edge behind any bug hypothesis.

## Editing

When you need to edit code:

1. Use SymDex to find the exact symbol or file location.
2. Read only that file or symbol slice.
3. Make the smallest change needed.

## Watch And Semantic Search

- `symdex watch` refreshes structural indexes by default without loading local embedding models.
- Use `symdex watch --embed` only when the task needs semantic search to stay fresh continuously.
- If `semantic_search` has no embeddings, fall back to `search_symbols` or `search_text`, or re-index after enabling `symdex[local]`, Voyage, OpenAI-compatible, Gemini, or another hosted embedding backend.
- Use `symdex index --lazy` when embeddings may be slow because of hosted-model latency or RPM limits.
- Workspace-local state keeps watcher metadata under `./.symdex`, so commands should run from that workspace or pass the matching `--state-dir`.

## Use Normal Browsing Only When Needed

- SymDex is unavailable.
- The repo is not indexed and cannot be indexed in the current environment.
- The target file type is unsupported or generated.
- You need surrounding context that the symbol-level response does not provide.

## Output Checklist

- [ ] Repo id confirmed or derived
- [ ] Index freshness checked
- [ ] SymDex tool chosen before broad file reads
- [ ] Context pack used for broad multi-file questions
- [ ] Exact symbol or file outline used before whole-file reads when possible
- [ ] Quality metadata inspected before logic or bug claims
- [ ] Direct file reads used only when SymDex could not answer cleanly
