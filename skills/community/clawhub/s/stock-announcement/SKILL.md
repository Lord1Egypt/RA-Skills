# Stock Announcement Skill

Daily stock portfolio analysis with Gmail report delivery and Sonos voice announcement.

## What it does

1. Fetches portfolio performance via yfinance
2. Sends an HTML email report via Gmail API
3. Announces a summary on a Sonos speaker via TTS + sonoscli

## Prerequisites

- Python 3.9+ with `yfinance`, `pandas`, `google-api-python-client`, `google-auth-oauthlib`, `gtts`
- `sonos` CLI installed and speakers discoverable on the network
- Gmail OAuth token at `config/token.json` (relative to workspace root)
- Environment variables: `RECIPIENT_EMAIL`, `SONOS_SPEAKER` (optional, defaults to "Living Room")

## Usage

```bash
python scripts/daily_stock_announcement.py
```

## Changelog (v1.1.0)

- Fix: Gmail token path now resolved as absolute from script directory
- Fix: Sonos announcement uses TTS audio generation + `sonos queue play` instead of unsupported `sonos say`
- Fix: Retry with exponential backoff for Gmail and Sonos (3 retries, 5s base)
- Fix: Non-zero exit code on critical step failure
