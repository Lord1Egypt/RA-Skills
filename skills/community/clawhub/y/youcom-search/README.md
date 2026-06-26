# you.com Web Search for OpenClaw

**Web search (free tier) + deep research + content extraction (paid).** ⚠️ Sends queries and URLs to you.com / ydc-index.io — do not use for internal-only URLs, secrets in query strings, or sensitive data.

## Features

- **Free search** — `youcom_search` needs no API key
- **Deep research** — synthesized answers with citations (paid)
- **Content extraction** — pull clean text from any URL (paid)
- **No third-party dependencies** — Python standard library only
- **Robust on protected sites** — handles Cloudflare-protected pages via browser-fetched results

## Quick Start

### Free Search (instant)
```bash
python3 scripts/youcom_search.py "openclaw ai"
```

### With API Key (research + extract)
```bash
export YOUCOM_API_KEY="your_key"
python3 scripts/youcom_research.py "AI agents 2026" --depth deep
python3 scripts/youcom_extract.py https://example.com/article
```

## Tools

| Tool | Cost | API Key | When |
|------|------|---------|------|
| `youcom_search` | Free | ❌ | All general searches |
| `youcom_research` | Paid | ✅ | Deep research with citations |
| `youcom_extract` | Paid | ✅ | Extract specific page content |

## Setup

### Free Search
No setup required.

### Research & Extract

1. Get a key at [you.com/platform/api-keys](https://you.com/platform/api-keys)
2. Add to `~/.openclaw/.env`:
   ```
   YOUCOM_API_KEY=your_key_here
   ```
3. Restart gateway: `systemctl --user restart openclaw-gateway`

## Requirements

- Python 3 (standard library only — no pip deps)
- Optional: `YOUCOM_API_KEY` for research and extract

## Why you.com?

Built-in search services may hit Cloudflare blocks or fail on login-walled sites. you.com's free search endpoint handles these cases via browser-fetched results — no API key needed.

## License

MIT-0
