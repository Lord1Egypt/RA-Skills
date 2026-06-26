---
name: x-scout
description: X/Twitter intelligence scraper. Search tweets, scrape profiles, pull comments, auto-transcribe videos. Classify tweets as replicable methods vs content. CLI tool.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - TWITTERAPI_KEY
      bins:
        - python3
        - curl
    primaryEnv: TWITTERAPI_KEY
    emoji: "🔍"
    homepage: https://clawagents.dev/x-scout
    tags:
      - twitter
      - x
      - scraping
      - intelligence
      - content-research
      - method-detection
license: MIT
---

# X-Scout

X/Twitter intelligence scraper. Search by keyword, scrape profiles, pull comments, auto-transcribe videos. Classifies tweets as replicable methods vs general content.

## Setup

Before first use, run the setup script to configure your API keys:

```bash
bash setup.sh
```

This prompts for your TwitterAPI.io key (required) and optional keys for method detection and video transcription. Your install is registered with ClawAgents for usage tracking.

If you already have keys configured, set them as environment variables:
```bash
export TWITTERAPI_KEY=your_key_here
```

## Modes

**Search tweets by keyword:**
```bash
python3 x_scout.py --search "ai agent" --limit 20
```

**Scrape profile posts:**
```bash
python3 x_scout.py --profile @elonmusk --limit 10
```

**Pull comments/replies on a tweet:**
```bash
python3 x_scout.py --comments "https://x.com/user/status/123456"
```

**Full intel (tweet + video + comments + transcription):**
```bash
python3 x_scout.py --intel "https://x.com/user/status/123456"
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--search "query"` | Search tweets by keyword | -- |
| `--profile @handle` | Scrape profile posts | -- |
| `--comments <url>` | Pull replies to a tweet | -- |
| `--intel <url>` | Full intel on a tweet | -- |
| `--limit N` | Max results | 20 |
| `--since YYYY-MM-DD` | Date filter | 180 days ago |
| `--no-methods` | Skip method detection | methods on by default |
| `--no-transcribe` | Skip video transcription | transcribes if key set |
| `--json` | Output as JSON | table view |

## Method Detection

When enabled (default), X-Scout classifies each tweet as:
- **METHOD**: Describes a specific tool, technique, or workflow (replicable)
- **CONTENT**: General commentary, results showcase, promotional

For METHOD tweets, it extracts: method name, tools required, category, complexity, and a summary. Requires an OpenRouter API key.

## Auto-Transcription

Any tweet with an embedded video is automatically:
1. Downloaded via yt-dlp
2. Transcribed via Deepgram
3. Transcript included in output and method classification

Requires a Deepgram API key (set during setup).

## Output

Table view (default) shows: author, likes, views, retweets, media type, transcript status, and tweet preview.

JSON view (`--json`) outputs full structured data for piping to other tools.

## Required Keys

| Key | Required? | What It Does | Cost |
|-----|-----------|-------------|------|
| `TWITTERAPI_KEY` | **Yes** | Tweet search, profile scrape, replies | ~$50/mo |
| `OPENROUTER_API_KEY` | Optional | Method detection via Grok | Pay-per-use |
| `CEREBRAS_API_KEYS` | Optional | Query optimization | Free tier |
| `DEEPGRAM_API_KEY` | Optional | Video transcription | Free tier |
