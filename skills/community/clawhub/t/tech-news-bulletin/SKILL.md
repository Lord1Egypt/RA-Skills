---
name: tech-news-bulletin
description: Collect latest technology and AI news from RSS feeds AND the TLDR.tech AI newsletter, merge them into a unified daily digest, and send via email.
metadata:
  {
    "openclaw":
      {
        "emoji": "📬",
        "requires":
          {
            "bins": ["python3"],
            "packages": ["feedparser", "requests", "beautifulsoup4"]
          },
        "env": ["SMTP_EMAIL", "SMTP_PASSWORD"]
      }
  }
---

# Tech News Bulletin

Collect the latest technology and AI news from two sources:
1. **RSS feeds** — e.g., TechCrunch, Wired AI, Google AI Blog
2. **TLDR.tech AI Newsletter** — yesterday's edition, fetched and sanitized automatically

Merge both into a single deduplicated digest and send it to a list of email addresses.

## When to use (trigger phrases)

Use this skill immediately when the user asks any of:

- "tech news bulletin"
- "daily tech bulletin"
- "send tech bulletin"
- "run tech bulletin"
- "create tech bulletin"

## Workflow

1. **Fetch RSS feeds** from configured sources
2. **Fetch TLDR.tech AI newsletter** for the previous day (`https://tldr.tech/ai/YYYY-MM-DD`)
3. **Sanitize TLDR HTML** — extract article title, canonical link, and summary; strip sponsor blocks, navigation, footers
4. **Merge & deduplicate** all articles by URL
5. **Sort by date** (newest first) and limit to `MAX_ARTICLES`
6. **Summarize** each article via Ollama (falls back to the description snippet if unavailable)
7. **Build HTML digest** with per-article source badges (RSS source name vs. "TLDR AI")
8. **Send digest** to all configured email addresses via SMTP

## Installation

Install required Python packages:

```bash
pip install feedparser requests beautifulsoup4
```

Ensure environment variables are set:

```bash
export SMTP_EMAIL="your-email@example.com"
export SMTP_PASSWORD="your-app-password"
```

## Configuration

Edit `scripts/bulletin.py` to customize:

- `RSS_FEEDS` — list of RSS URL endpoints
- `EMAIL_ADDRESSES` — recipients for the bulletin
- `MAX_ARTICLES` — maximum articles in the combined digest (default 15)
- `TLDR_BASE_URL` — base URL for the TLDR newsletter (default `https://tldr.tech/ai/`)

The Ollama endpoint is `http://172.20.86.203:11434` with model `glm-4.7-flash:latest`.

## Usage

To run the bulletin now:

```bash
python3 /home/juniarto/.openclaw/workspace/skills/tech-news-bulletin/scripts/bulletin.py
```

Check the log output:

```bash
tail -f /tmp/openclaw-debug.log
```

Or let the skill handle it automatically via cron:

```bash
openclaw cron add --job='{
  "name": "daily-tech-bulletin",
  "schedule": { "kind": "every", "everyMs": 86400000, "anchorMs": 42000000 },
  "payload": { "kind": "systemEvent", "text": "run-tech-news-bulletin" },
  "sessionTarget": "isolated",
  "enabled": true
}'
```

## Digest Format

**Subject:** Daily Tech & AI News Bulletin

**Body (HTML):**
- Header with date and source attribution
- Per article:
  - Linked title
  - Source badge (RSS feed name or "TLDR AI")
  - 1–5 sentence summary

## Differences from `tech-news-digest`

| Feature | tech-news-digest | tech-news-bulletin |
|---|---|---|
| RSS feeds | ✅ | ✅ |
| TLDR.tech AI newsletter | ❌ | ✅ |
| Source badges in digest | ❌ | ✅ |
| HTML sanitizer (inline) | ❌ | ✅ |
| Combined deduplication | ❌ | ✅ |

## Rules

- Send emails via the SMTP credentials in the environment (`SMTP_EMAIL`, `SMTP_PASSWORD`)
- Keep each article summary to 1–5 sentences
- Strip sponsor articles from TLDR content
- Total digest should be readable within ~5 minutes
- TLDR date is always computed as `today - 1 day` at runtime, so no manual date config is needed
