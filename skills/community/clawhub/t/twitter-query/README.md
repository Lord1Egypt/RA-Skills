# Twitter Query

**Query X (Twitter) by account or keyword** via [twitterapi.io](https://docs.twitterapi.io/introduction). **JSON output**, Python stdlib only, **no bundled LLM**.

[![ClawHub](https://img.shields.io/badge/ClawHub-twitter--query-blue)](https://clawhub.ai/alexander10011/twitter-query)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## Features

| Mode | API | Script |
|------|-----|--------|
| User timeline | `GET /twitter/user/last_tweets` | `scripts/query_by_user.py` |
| Keyword search | `GET /twitter/tweet/advanced_search` | `scripts/query_by_keyword.py` |

- Cursor pagination (`cursor` / `has_next_page`)
- `queryType`: `Latest` or `Top` for advanced search
- Retries on HTTP 429 with backoff

## Requirements

- **Python 3.10+** (uses `from __future__ import annotations`; stdlib only)
- **twitterapi.io API key** → set `TWITTER_API_KEY`
- Optional: `TWITTER_API_BASE` (default `https://api.twitterapi.io`)

## Install (OpenClaw / ClawHub)

```bash
npx skills add alexander10011/twitter-query
```

> If you fork under another GitHub user, replace `alexander10011` with your username in this command and in `claw.json` / `clawhub.json` / badge URLs.

## Quick start

```bash
export TWITTER_API_KEY="your_key_here"
cd /path/to/twitter-query   # skill root after install

python3 scripts/query_by_user.py VitalikButerin --max-pages 3
python3 scripts/query_by_keyword.py '"$BTC" min_faves:2' --query-type Latest --max-pages 2
```

## Privacy

- Your **API key** is sent only to **twitterapi.io** in the `X-API-Key` header.
- **Queries and usernames** are sent as URL parameters to that API.
- This repo does not phone home or collect telemetry.

See `claw.json` → `privacy.externalServices` for OpenClaw disclosure.

## Publish checklist (maintainer)

1. Create GitHub repo `twitter-query` under your account (default links assume `alexander10011/twitter-query`).
2. Push this folder as repo root (`SKILL.md`, `scripts/`, `claw.json`, `clawhub.json`, `LICENSE`, `README.md`).
3. On [ClawHub](https://clawhub.ai), submit or sync the skill per current ClawHub docs (CLI or web).
4. After listing is live, confirm badge URL `https://clawhub.ai/<owner>/twitter-query`.

维护者发布步骤见本仓库 [PUBLISH.md](PUBLISH.md)。若本目录放在更大 monorepo 中，另有一份汇总说明：`docs/twitter-query-release-summary.md`（仅在该 monorepo 中存在）。

## License

MIT — see [LICENSE](LICENSE).
