---
name: x-reader
description: Read X (Twitter) posts without official API. Supports both Nitter (free) and RapidAPI (detailed) methods.
version: 1.0.0
author: Dohoon Kim
license: MIT
tags: [twitter, x, social-media, scraper, api]
requirements:
  - Python 3.8+
  - requests library
  - Optional: RapidAPI key for detailed results
install: |
  pip install requests
  
  # Optional: For better results, get RapidAPI key
  # 1. Visit https://rapidapi.com/alexanderxbx/api/twitter-api45
  # 2. Sign up and get free tier (100 requests/month)
  # 3. Set environment variable: export RAPIDAPI_KEY="your_key"
---

# X-Reader

Read X (Twitter) posts without official API key.

## Features

- **Nitter Mode** (Default): Free, no API key required
- **RapidAPI Mode**: Detailed tweet info with API key
- Simple CLI interface
- JSON output for easy integration

## Usage

### Basic (Nitter - Free)

```bash
python3 x-reader.py "https://x.com/username/status/1234567890"
```

### Advanced (RapidAPI - Detailed)

```bash
export RAPIDAPI_KEY="your_rapidapi_key"
python3 x-reader.py "https://x.com/username/status/1234567890"
```

## Output Format

```json
{
  "id": "1234567890",
  "text": "Tweet content...",
  "author": "Display Name",
  "username": "username",
  "created_at": "2024-01-01T00:00:00.000Z",
  "likes": 100,
  "retweets": 50,
  "replies": 25,
  "url": "https://x.com/username/status/1234567890"
}
```

## Notes

- Nitter mode may have rate limits
- RapidAPI free tier: 100 requests/month
- For production use, consider RapidAPI paid tier
