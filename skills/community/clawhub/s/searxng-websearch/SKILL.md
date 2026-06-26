---
name: searxng-websearch
description: >
  Use this skill whenever the user wants to search the web, do research on a topic, fetch a webpage,
  or gather information from online sources using a self-hosted SearXNG instance. Triggers include:
  'search for', 'look up', 'find online', 'deep research', 'fetch this page', 'web search', or any
  request that needs current/external information. Also use when the user wants to run websearch.py,
  deep_research.py, or fetch_page.py scripts. Do NOT use for local file operations, code execution
  unrelated to search, or tasks that don't require web data.
---

# SearXNG Web Search Skill

A skill for searching the web and fetching pages via a self-hosted [SearXNG](https://docs.searxng.org/) instance.
Three entry-point scripts cover the main use cases:

| Script | Purpose |
|---|---|
| `websearch.py` | Single query, structured results |
| `fetch_page.py` | Fetch and extract text from one URL |
| `deep_research.py` | Multi-query research with page fetching and ranking |

---

## Environment Setup

All scripts read configuration from a `.env` file (or real environment variables).
Copy `_env` → `.env` and fill in your values:

```bash
cp _env .env
```

### `.env` reference

| Variable | Default | Description |
|---|---|---|
| `SEARXNG_URL` | `http://localhost:8080` | Base URL of your SearXNG instance |
| `SEARXNG_LANGUAGE` | `en` | Default search language |
| `SEARXNG_SAFE_SEARCH` | `0` | 0 = off, 1 = moderate, 2 = strict |
| `SEARXNG_TIMEOUT` | `20` | HTTP timeout in seconds |

> **CLI override** — every script now also accepts `--searxng-url` to override the env value
> for one-off runs without editing `.env`.

---

## Quick Start

### Install dependencies

```bash
pip install requests beautifulsoup4 lxml python-dotenv
```

### Install PATH shims (recommended — fixes CWD issues in OS)

```bash
bash ~/.openclaude/skills/searxng-websearch/install.sh
# reload shell, then:
wsearch   "Claude Sonnet 4 release notes" --format agent
wfetch    https://example.com --max-chars 3000
wresearch "transformer attention mechanisms" --fetch-top-pages 3
```

### Or call directly with full path (no install needed)

```bash
SKILL=~/.openclaude/skills/searxng-websearch
python3 "$SKILL/websearch.py"    "Claude Sonnet 4 release notes" --format agent
python3 "$SKILL/fetch_page.py"   https://example.com --max-chars 3000
python3 "$SKILL/deep_research.py" "transformer attention mechanisms" --fetch-top-pages 3
```

---

## Script Reference

### `websearch.py`

```
python websearch.py <query> [options]

Options:
  --searxng-url URL       SearXNG base URL (overrides SEARXNG_URL env var)
  --category CATEGORY     general | images | news | science | files |
                          social_media | map | music | videos | it
                          (default: general)
  --max-results N         Number of results to return (default: 5)
  --language LANG         Language code, e.g. en, de, fr
  --safe-search 0|1|2     Safe-search level
  --page N                Result page number (default: 1)
  --time-range RANGE      day | week | month | year
  --format FORMAT         markdown | text | json | agent (default: markdown)
```

### `fetch_page.py`

```
python fetch_page.py <url> [options]

Options:
  --searxng-url URL       Unused here but accepted for consistency
  --max-chars N           Max characters to print (default: 5000)
```

### `deep_research.py`

```
python deep_research.py <topic> [options]

Options:
  --searxng-url URL       SearXNG base URL (overrides SEARXNG_URL env var)
  --max-results N         Results per sub-query (default: 4)
  --fetch-top-pages N     Number of top pages to fetch (default: 3)
  --max-chars N           Max chars per fetched page (default: 2500)
  --output FORMAT         markdown | text (default: markdown)
```

---

## Source Ranking (deep_research.py)

Pages are scored before fetching so the most authoritative content is prioritised:

| Domain signal | Points |
|---|---|
| `github.com` / `gitlab.com` | +5 |
| `arxiv.org` / `openreview.net` | +5 |
| `docs.*` / `readthedocs.*` | +4 |
| `research` / `paper` in domain | +3 |
| Has a publication date | +1 |
| Has a snippet | +1 |

---

## ⚠️ Critical: How to Invoke These Scripts (OpenClaude / Claude Code)

**NEVER use `cd` before calling a script.** Each `Bash()` call spawns a fresh shell;
`cd skill-dir && python3 script.py` silently resets the CWD and the script never runs.

**Always call scripts by their full absolute path in a single command:**

```bash
# ✅ CORRECT — full path, no cd
python3 ~/.openclaude/skills/searxng-websearch/websearch.py "my query" --format agent

# ✅ CORRECT — SKILL_DIR variable makes it readable
SKILL_DIR=~/.openclaude/skills/searxng-websearch
python3 "$SKILL_DIR/websearch.py" "my query" --format agent

# ❌ WRONG — cd resets on the next Bash() call
cd ~/.openclaude/skills/searxng-websearch && python3 websearch.py "my query"
```

If the skill path is unknown, resolve it first:
```bash
SKILL_DIR=$(find ~/.openclaude/skills -name "websearch.py" -printf '%h' -quit 2>/dev/null \
            || find ~/skills -name "websearch.py" -printf '%h' -quit 2>/dev/null)
python3 "$SKILL_DIR/websearch.py" "my query" --format agent
```

---

## Tips for Claude

- Run `websearch.py` with `--format agent` when you need compact, token-efficient context to pass
  back to the model.
- For broad topics, prefer `deep_research.py` — it fans out into sub-queries automatically.
- If SearXNG is unreachable, `deep_research.py` exits with a clear error message; check that
  `SEARXNG_URL` is correct and the instance is running.
- Pipe markdown output into a file for later use:
  ```bash
  python3 ~/.openclaude/skills/searxng-websearch/deep_research.py "RAG retrieval strategies" > research.md
  ```