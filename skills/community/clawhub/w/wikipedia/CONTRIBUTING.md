# Contributing to Wikipedia MCP

Contributions are welcome — new tools especially. The codebase is deliberately
small: one server file (`src/server.py`), one smoke-test file
(`tests/test_server.py`), stdlib + `requests` only.

## Adding a tool

**One tool per PR.** Each tool is three small pieces in `src/server.py`:

1. **Definition** — append an entry to the `TOOLS` list:
   - `name`: snake_case, e.g. `article_extract`
   - `description`: what it does *and when to use it*. This text is what LLMs
     see when choosing between tools — write it for an agent, not a human.
   - `inputSchema`: a JSON Schema object describing the arguments.
     **Every tool must declare one** — directory checks (e.g. Glama's) fail
     listings where it's missing.
2. **Implementation** — a plain function, e.g.
   `search_wikipedia(query, limit=5, lang="en")`, that returns a Markdown string.
3. **Dispatch** — one branch in `_call_tool`:
   `if name == "my_tool": return my_tool(**args)`.

Rules for new tools:

- **Read-only.** Only `GET` requests, only to `*.wikipedia.org` /
  `wikimedia.org`. Use the `_get()` helper — it sets Wikipedia's required
  User-Agent and a sane timeout.
- **No new dependencies.** `requests` + stdlib is the entire stack.
- **Fail gracefully.** Return a helpful message (`No results found`) instead of
  raising on empty or missing data. Clamp numeric arguments to sane ranges
  (see how `limit` is clamped in `search_wikipedia`).
- **Markdown output.** Tools return text; format it as Markdown for readability.
- **Don't bump `SERVER_VERSION`.** Versioning happens at release time.

## Tests

Add a smoke test to `tests/test_server.py` that calls your function directly
(no stdio plumbing needed — see the existing sections for the pattern), then run:

```bash
python3 tests/test_server.py
```

## Docs

Add one row to the tools table at the top of `README.md`:

```markdown
| `my_tool` | One-line description of what it does |
```

## PR process

Fork → branch → PR against `master`. There's no CI: green smoke tests and a
clear PR description are the whole review bar. One tool per PR keeps review fast.
