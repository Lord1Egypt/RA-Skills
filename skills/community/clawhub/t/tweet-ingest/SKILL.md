---
name: tweet-ingest
version: 1.0.0
description: Read Twitter/X content (single tweet, thread, or user profile) from a
  URL via TwitterAPI.io. Use when a Twitter/X URL appears in conversation and you
  need to read its content without browser automation.
metadata:
  openclaw:
    emoji: 🐦
    primaryEnv: TWITTER_API_KEY
    requires:
      env:
      - TWITTER_API_KEY
    network:
      outbound: true
      reason: Fetches tweet content from TwitterAPI.io.
---

# Tweet Ingest Skill

Use this skill whenever a Twitter/X URL appears in conversation and you need to read its content — single tweet, thread, or user profile.

## When to Use

- A Twitter/X URL is shared and you need the text to summarise, analyse, or index
- You want to fetch a tweet thread for context
- You need recent tweets from a specific account for RAG or research
- An agent needs Twitter content without an API key or paid subscription

**Do NOT use for:** sending/posting tweets (use Buffer — `skills/buffer-publisher/SKILL.md`), or monitoring streams in real-time.

---

## Quick Reference

```bash
# Single tweet (default) — fast, free, no API key needed
python3 /Users/loki/.openclaw/workspace/scripts/tweet-ingest.py \
  https://x.com/solanamobile/status/2034675043033375103

# Thread — fetches tweet + replies by same author via Apify (costs small Apify credits)
python3 /Users/loki/.openclaw/workspace/scripts/tweet-ingest.py \
  https://x.com/solanamobile/status/2034675043033375103 --mode thread

# Profile — recent tweets from an account (requires Apify)
python3 /Users/loki/.openclaw/workspace/scripts/tweet-ingest.py \
  https://x.com/solanamobile --mode profile --max-tweets 20

# Pipe output to a file for RAG indexing
python3 /Users/loki/.openclaw/workspace/scripts/tweet-ingest.py \
  https://x.com/solanamobile/status/2034675043033375103 \
  > /Users/loki/.openclaw/workspace/content/tweets/solanamobile-grants.md
```

---

## Modes

| Mode | Backend | Cost | Use Case |
|------|---------|------|----------|
| `single` (default) | Jina AI (`r.jina.ai`) | Free | Grab one tweet's text + author + timestamp |
| `thread` | Jina (root) + Apify | Apify credits | Full thread by same author |
| `profile` | Apify | Apify credits | Recent tweets from an account |

### Apify credits
- Actor: `apidojo/tweet-scraper` at ~$0.40/1K tweets
- `$5/mo` free credit included — very low cost for occasional use
- Key auto-loaded from env `APIFY_API_KEY` or 1Password `op://OpenClaw/Apify API Credentials/credential`

---

## Output Format

Always clean markdown to stdout:

```markdown
# Tweet Thread: @solanamobile
_Source: https://x.com/solanamobile/status/2034675043033375103_
_Fetched: 2026-03-20 09:00 AEST_

## Tweet 1 — @solanamobile (2026-03-19 21:44 UTC)
Solana Mobile Builder Grants are live...

## Tweet 2 — @solanamobile (2026-03-19 21:45 UTC)
Here's what qualifies...
```

Errors are also returned as markdown (never crashes):
```markdown
# Tweet Ingest Error
> ❌ Jina fetch failed: ...
```

---

## Graceful Degradation

- **No Apify key** → thread/profile modes warn and fall back to single (or error for profile)
- **Apify returns no results** → falls back to root tweet only with a warning note in the markdown
- **Jina timeout** → error markdown, exit 1
- **Any unexpected error** → error markdown, never a Python traceback to stdout

---

## Integration with RAG

Pipe output directly into the RAG indexer:

```bash
python3 scripts/tweet-ingest.py https://x.com/solanamobile/status/... \
  > /tmp/tweet.md
python3 scripts/rag_index.py /tmp/tweet.md --collection agent-research-kb
```

Or in Python:
```python
import subprocess
result = subprocess.run(
    ["python3", "scripts/tweet-ingest.py", url, "--mode", "single"],
    capture_output=True, text=True
)
markdown = result.stdout  # Clean markdown, ready to index
```

---

## URL Formats Supported

```
https://x.com/username/status/TWEET_ID       → tweet, thread modes
https://twitter.com/username/status/TWEET_ID  → same (auto-normalised)
https://x.com/username                        → profile mode
https://twitter.com/username                  → same (auto-normalised)
```

---

## Notes

- Thread mode fetches the handle's recent tweets from Apify and filters to those matching the conversation. If Apify's window doesn't include the full thread (e.g., thread is old), it falls back to just the root tweet with a warning.
- Profile mode returns tweets newest-first.
- Jina parses tweet content as a logged-out user — no engagement metrics (likes/RTs) are returned in single mode.
- Python path: `/Users/loki/.pyenv/versions/3.14.3/bin/python3`
