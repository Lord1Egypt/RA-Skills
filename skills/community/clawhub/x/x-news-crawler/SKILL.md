---
name: x-news-crawler
description: Crawl X (Twitter) search results through a local CLI that wraps `abs` (agent-browser). Use when the user asks to scrape X posts by keyword, collect Top/Latest news, extract structured fields (author/time/text/link), or produce a deduplicated "top-first then latest" feed.
---

# X News Crawler

Use this skill to run one command and get structured X news JSON.

## Prerequisites (Required)

Before any crawl command, run:

```bash
pnpm add -g agent-browser-stealth
pnpm approve-builds -g
```

Run Chrome with CDP on the regular profile before crawling:

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9333
```

Do not use `--user-data-dir` in that Chrome launch command.

## Workflow

1. Run the CLI, not raw `abs` commands.
2. Use `--mode hybrid` by default: fetch `top` first, then `latest`, then sort by time and dedupe.
3. Read JSON output and summarize signal/noise for the user.

## Commands

From repository root, run:

```bash
./bin/x-news-crawler --query "openclaw" --mode hybrid --since-hours 72 --limit 30 --output .tmp/openclaw-news.json
```

Quick probes:

```bash
./bin/x-news-crawler --query "openclaw" --mode top --limit 10
./bin/x-news-crawler --query "openclaw" --mode latest --since-hours 24 --limit 20
./bin/x-news-crawler --query "openclaw" --cdp 9333 --limit 20
```

## Output Contract

The CLI returns JSON with:

- `fetched_at`
- `query`
- `mode`
- `count`
- `warnings[]`
- `failed_sources[]`
- `rows[]` with: `source`, `datetime`, `status_url`, `user`, `text`, `replies`, `reposts`, `likes`

## Guardrails

- Prefer `hybrid` unless the user explicitly asks only `top` or `latest`.
- Keep `since-hours` small (24-168) to avoid stale content.
- Treat unverified rumor posts as low confidence even with high engagement.

## Reference

See [cli.md](references/cli.md) for full flags.
