# YouTube Transcript Fetcher (Apify)

Fetch YouTube video transcripts from anywhere, including cloud servers where YouTube blocks direct access.

## Features

- Works from cloud IPs (AWS, GCP, VPS, etc.)
- Runs the request through Apify proxies
- Local caching (v1.1.0+) so repeat requests do not start an actor run
- Batch mode (v1.1.0+) for multiple videos
- Cache management: `--cache-stats`, `--clear-cache`, `--no-cache`
- Text or JSON output
- Python script, no Apify SDK

`--lang` is a CLI flag only. The default actor `topaz_sharingan/youtube-transcript-scraper-1` has no language input field; the script does not send `--lang` to that actor.

## Default actor

`topaz_sharingan/youtube-transcript-scraper-1`. Store sheet: https://apify.com/topaz_sharingan/youtube-transcript-scraper-1

Checked against the Apify API on 2026-08-31: public, not deprecated, last code change 2026-07-19. Pay per event: **$0.01 per result** ($10.00 per 1,000). Older docs that said $0.007 were wrong.

Input schema: `startUrls` (string[], required) and `timestamps` (boolean, default `false`). No `lang` / `language` field.

## Free Tier

Apify Free plan: $5 prepaid usage per month, no credit card. Unused credits do not roll over.

At $0.01 per video, $5 covers **500 videos per month**, not 714 (714 was $5 / $0.007).

[Sign up](https://apify.com/)

## Quick Start

```bash
# 1. Set your API token
export APIFY_API_TOKEN="apify_api_YOUR_TOKEN"

# 2. Install the Python dependency (OpenClaw has no pip installer kind)
python3 -m pip install requests

# 3. Fetch a transcript
python3 scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"
```

## Documentation

See [SKILL.md](SKILL.md) for setup, input/output schema, and usage examples.

## Links

- [Apify Free plan](https://apify.com/pricing): $5/month prepaid usage
- [Get API token](https://console.apify.com/account/integrations)
- [YouTube Transcripts Actor](https://apify.com/topaz_sharingan/youtube-transcript-scraper-1)

## Requirements

- Python 3.6+
- `requests` library (`python3 -m pip install requests`)
- Apify API token

## License

MIT
