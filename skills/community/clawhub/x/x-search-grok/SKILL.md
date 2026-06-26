---
name: x-search
description: Search X (Twitter) for account posts, trending topics, or topic discussions using Grok API. Outputs Obsidian-ready Markdown.
trigger: Use when user wants to search X or Twitter, check someone's posts on X, find trending topics, or search discussions. Triggers include "x search", "search X", "/x-search", "twitter search", "X上搜索", "推特搜索", "搜索X", mentions of checking @accounts on X.
user-invocable: true
metadata:
  openclaw:
    version: "1.0.0"
    author: wangyue55
    license: MIT
    source: https://github.com/wangyue55/x-search-skill
    requires:
      - XAI_API_KEY
    install:
      pip: requests pyyaml
---

# X Search

Search X (Twitter) via Grok API. Outputs Obsidian-ready Markdown.

## Prerequisites

Ensure `XAI_API_KEY` is set:
```bash
export XAI_API_KEY=your_key_here
```

Get your API key at **x.ai/api** (xAI developer console).

Default model is `grok-4-1-fast-reasoning`. To override:
```bash
export XAI_MODEL=grok-4
```

Install dependency if needed:
```bash
pip install requests
```

## Invocation

### Slash Command
```
/x-search account @elonmusk --time 24h
/x-search account @user1 @user2 --time 48h
/x-search account @sama --count 10
/x-search --lang en account @elonmusk --count 5
/x-search trends "#AI" "#LLM"
/x-search --lang en trends "#AI" "#crypto"
/x-search topic "Claude MCP"
/x-search --lang ja topic "AI規制"
```

`--lang` controls the language of summaries, keyword explanations, and translations (default: `zh`).
When `--lang en`, the translation field is omitted since the original is already in English.

`--output` saves the result to a Markdown file (stdout is preserved):
- Pass a **directory** → auto-named file: `karpathy-2026-03-22.md`, `trends-AI-2026-03-22.md`, etc.
- Pass a **full path** → saved directly to that path
- Same-day runs overwrite the existing file (no duplicate accumulation)

`--progress-only` suppresses full Markdown on stdout — prints one summary line instead. Use with `--output` in automated pipelines (watchlist, cron) to avoid injecting large outputs into the agent context.

### Natural Language
- "Search X for @elonmusk's posts in the last 24 hours"
- "X上搜索@sama和@elonmusk最新的10条推文"
- "Find trending posts about #AI on X in English"
- "X上关于Claude MCP的热点讨论"

## How to Run

Find the script at `~/.claude/skills/x-search/x_search.py` (or the symlinked path).

```bash
# Account mode — by time range
python3 ~/.claude/skills/x-search/x_search.py account @elonmusk --time 24h

# Account mode — by post count
python3 ~/.claude/skills/x-search/x_search.py account @user1 @user2 --count 10

# Trends mode — top 10 posts per trend
python3 ~/.claude/skills/x-search/x_search.py trends "#AI" "#LLM"

# Topic mode — hot discussions
python3 ~/.claude/skills/x-search/x_search.py topic "Claude MCP"
```

## Output

Results are printed as Obsidian-ready Markdown.

**Context efficiency:** When results are large (multiple accounts, long time ranges) or when `--output` is provided, save to file and show only a brief summary to the user (e.g., "Found 12 posts from @karpathy, saved to `~/obsidian/X/karpathy-2026-03-22.md`"). Only present the full content inline when the result is short or the user explicitly asks to see it.

For **account mode**, after showing results (or summary) ask:
> "是否保存到文件？（例如：`~/obsidian/X/@elonmusk-2026-03-22.md`）"

If the user provides a path, run again with `--output <path>`.

## Watchlist

Run all your monitored accounts, trends, and topics in one command via `watchlist.py`.

### Setup

Copy the sample config and edit it:
```bash
cp ~/.claude/skills/x-search/watchlist.yaml ~/.x-search.yaml
```

```yaml
# ~/.x-search.yaml
accounts:
  - "@karpathy"
  - "@elonmusk"

trends:
  - "#AI"
  - "#LLM"

topics:
  - "Claude MCP"
  - "crude oil price"
```

> **Note:** all accounts share the same execution parameters. For per-account customization, call `x_search.py` directly.

### Usage

```bash
# Run everything
python3 ~/.claude/skills/x-search/watchlist.py --time 24h --lang zh --output ~/obsidian/X/

# Run one section only
python3 ~/.claude/skills/x-search/watchlist.py --only accounts --time 24h --output ~/obsidian/X/

# Custom config path
python3 ~/.claude/skills/x-search/watchlist.py --config ~/work-watchlist.yaml --time 24h
```

## Scheduled Use (OpenClaw)

See [`OPENCLAW.md`](./OPENCLAW.md) for full scheduling documentation — schedule formats, cron scenarios, delivery channels, and job management.

## Error Handling

- **`XAI_API_KEY` not set**: Tell the user to run `export XAI_API_KEY=your_key`
- **No results**: Inform the user and suggest broadening the time range or checking the account name
- **API error**: Show the error message and suggest checking the API key validity
