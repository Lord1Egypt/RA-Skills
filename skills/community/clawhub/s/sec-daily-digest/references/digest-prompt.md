# Sec Daily Digest — Trigger Prompt Templates

Copy-paste these prompts directly to Claude Code to generate a digest.

---

## Daily Digest (48h)

```
Generate a cybersecurity daily digest using sec-daily-digest.

Parameters:
- MODE: daily
- HOURS: 48
- PROVIDER: claude
- OUTPUT: ~/digests/sec-$(date +%Y%m%d).md
- EMAIL: (optional: your@email.com)

Run:
bun scripts/sec-digest.ts \
  --mode daily \
  --provider PROVIDER \
  --opml tiny \
  --output OUTPUT
```

---

## Weekly Digest (168h)

```
Generate a weekly cybersecurity digest using sec-daily-digest.

Parameters:
- MODE: weekly
- HOURS: 168
- PROVIDER: openai
- OUTPUT: ~/digests/weekly-$(date +%Y%m%d).md

Run:
bun scripts/sec-digest.ts \
  --mode weekly \
  --provider PROVIDER \
  --opml full \
  --output OUTPUT
```

---

## Full-featured (Twitter + Enrich + Email)

```
Generate a full-featured cybersecurity digest with Twitter KOL updates,
full text enrichment, and email delivery.

Prerequisites:
- Set TWITTERAPI_IO_KEY or X_BEARER_TOKEN in environment
- Install gog for email delivery

Run:
TWITTERAPI_IO_KEY=your-key bun scripts/sec-digest.ts \
  --mode daily \
  --provider claude \
  --enrich \
  --email EMAIL \
  --output OUTPUT
```

---

## Dry Run (no AI, testing only)

```
Generate a rule-scored digest without any AI API calls.
Useful for testing configuration or checking source health.

Run:
bun scripts/sec-digest.ts \
  --dry-run \
  --no-twitter \
  --output /tmp/test-digest.md
```

---

## Variable Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `MODE` | `daily` or `weekly` | `daily` |
| `HOURS` | Time window (set automatically by `--mode`) | `48` |
| `PROVIDER` | `openai\|gemini\|claude\|ollama` | `claude` |
| `OUTPUT` | Output file path | `~/digests/sec-20260306.md` |
| `EMAIL` | Recipient email for `gog` delivery | `you@example.com` |
