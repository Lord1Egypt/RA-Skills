---
name: yep-search
description: Web search via Yep Search API. Own index, fast results with domain filtering and date ranges.
homepage: https://platform.yep.com
compatibility: Requires Python 3.8+ (stdlib only, no pip install needed)
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["python3"],"env":["YEP_API_KEY"]},"primaryEnv":"YEP_API_KEY"}}
---

# Yep Search

Web search using the Yep Search API. Independent index — not a Google/Bing proxy. Returns URLs, titles, descriptions, and optional content highlights.

## Search

```bash
python3 {baseDir}/scripts/search.py "query"
python3 {baseDir}/scripts/search.py "query" -n 20
python3 {baseDir}/scripts/search.py "query" --highlights
python3 {baseDir}/scripts/search.py "query" --mode fast
python3 {baseDir}/scripts/search.py "query" --lang en
python3 {baseDir}/scripts/search.py "query" --include-domains "docs.rs,crates.io"
python3 {baseDir}/scripts/search.py "query" --safe
python3 {baseDir}/scripts/search.py "query" --after 2026-01-01
```

## Options

- `-n <count>`: Number of results (default: 10, max: 100)
- `--highlights`: Return content highlights (costs ~$0.009/call vs $0.004 basic)
- `--mode <mode>`: `fast` or `balanced` (default)
- `--lang <code>`: ISO 639-1 language code (e.g., `en`, `de`, `ja`)
- `--include-domains <domains>`: Comma-separated domains to restrict search to
- `--exclude-domains <domains>`: Comma-separated domains to exclude
- `--safe`: Enable safe search (exclude adult content)
- `--after <date>`: Only results published after this date (ISO 8601)
- `--before <date>`: Only results published before this date (ISO 8601)
- `--crawl-after <date>`: Only results crawled after this date
- `--crawl-before <date>`: Only results crawled before this date

Notes:
- Requires `YEP_API_KEY` from https://platform.yep.com/app
- $10 free credit on signup (no card required)
- Basic search: $0.004/call ($4/1k), Highlights: ~$0.009/call (~$9/1k)
- Rate limits: 60/min, 3,600/hr, 86,400/day
- 180+ languages supported
- Zero external dependencies — uses only Python stdlib
