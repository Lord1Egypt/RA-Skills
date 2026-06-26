---
name: techsnif
description: Query TechSnif tech news intelligence via bundled CLI. Continuously updated articles across AI, Startups, Venture, and Robotics. Use when asked about tech news, AI news, startup funding, robotics, venture capital, trending tech stories, company news, or anything requiring current technology news coverage. Triggers on phrases like "what's happening in tech", "AI news", "tech news", "trending in AI", "startup funding news", "latest in robotics", "search tech news for", "summarize tech news about", "what's trending in tech", "any news about [company/topic]", "tech headlines", "startup news", "VC funding", "robot news".
homepage: https://techsnif.com/
source: https://www.npmjs.com/package/@techsnif/cli
---

# TechSnif CLI

Query TechSnif's public tech news API. No API key needed. CLI is bundled — no remote downloads.

**Run:** `node <skill-path>/scripts/techsnif-cli.cjs <command> [options] --json`

Always use `--json` for structured output. Check `ok` field before reading `data`.

## Commands

```bash
# What's trending right now (default 5, max 20)
node scripts/techsnif-cli.cjs trending --json
node scripts/techsnif-cli.cjs trending --category AI --last 24h --limit 10 --json

# Latest articles with filters (default 10, max 50)
node scripts/techsnif-cli.cjs feed --json
node scripts/techsnif-cli.cjs feed --category Robotics --limit 5 --json
node scripts/techsnif-cli.cjs feed --limit 10 --offset 10 --json

# Keyword search (max 50)
node scripts/techsnif-cli.cjs search "nvidia GPU" --last 7d --limit 5 --json

# Full article by slug (formats: markdown, text, html)
node scripts/techsnif-cli.cjs article <slug> --format markdown --json

# Topic coverage summary (counts + category/tag breakdown)
node scripts/techsnif-cli.cjs summary --topic "semiconductors" --last 7d --json

# List valid categories
node scripts/techsnif-cli.cjs categories --json
```

## Categories

Exact values for `--category`: `AI`, `Startups`, `Venture`, `Robotics`. Case-sensitive.

See `references/categories.md` for full descriptions and common tags.

## Shared Options

- `--last` — Time window: `24h`, `48h`, `7d`, `30d`
- `--limit N` — Result count (server caps: trending=20, feed/search=50)
- `--offset N` — Pagination offset (feed only)
- `--category` — Filter by category (trending, feed)
- `--json` — Always include for structured output

## Response Envelope

```json
{ "ok": true, "data": { ... }, "targetEnv": "https://api.techsnif.com" }
```

Errors: `{ "ok": false, "error": "message" }`. Always check `ok` first.

Listing commands (trending, feed, search) return articles with `content: ""`. Use `article <slug>` for full content.

## Workflows

**"What's happening in AI?"**
→ `trending --category AI --last 24h --json`

**"Any news about [company]?"**
→ `search "[company]" --last 7d --json`

**"Full story on [headline]"**
→ Get slug from trending/feed/search → `article <slug> --format markdown --json`

**"Summarize [topic] this week"**
→ `summary --topic "[topic]" --last 7d --json` for overview → `feed` or `search` for articles → `article` for top 2-3 full texts → synthesize

**"Research [topic] for a newsletter/briefing"**
→ `search "[topic]" --last 7d --limit 10 --json` → read top 3 via `article` → synthesize with source links

**Multi-category scan**
→ Run `trending --category AI --last 24h --json`, then `trending --category Startups --last 24h --json`, etc. Combine results.

## Key Details

- No API key or auth needed — public read-only
- CLI is bundled in `scripts/techsnif-cli.cjs` — no remote package downloads
- Slugs come from listing responses — use as-is for `article` command
- Empty search results return `ok: true` with empty array (not an error)
- Invalid category returns `ok: false` with 400 error
- Invalid slug returns `ok: false` with 404 error
- `--format text` without `--json` gives clean terminal output for `article`
