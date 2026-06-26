---
name: zenquote
description: Daily inspirational quotes from ZenQuotes.io. Get daily wisdom, random quotes, quote images. Supports automated daily delivery via cron scheduling.
---

# ZenQuote - Daily Inspirational Quotes

## Overview

ZenQuote skill fetches inspirational quotes from ZenQuotes.io API and delivers them to users. All features use the free API tier.

## Features

- ✅ Daily quote (`today`)
- ✅ Random quote (`random`)
- ✅ Multiple quotes (`quotes`)
- ✅ Quote images (`image`)
- ✅ Automated daily delivery (`setup`)

**API Limits:** 5 requests per 30 seconds. Attribution required.

## Dependencies

This skill requires the following system tools:
- `curl` - For HTTP requests to ZenQuotes API
- `jq` - For JSON parsing

These are usually pre-installed on most Linux/macOS systems.

## Quick Start

### Get Today's Quote
```bash
bash ~/.openclaw/skills/zenquote/scripts/zenquote.sh today
```

### Get Random Quote
```bash
bash ~/.openclaw/skills/zenquote/scripts/zenquote.sh random
```

### Setup Daily Morning Quote (9:00 AM)
```bash
bash ~/.openclaw/skills/zenquote/scripts/zenquote.sh setup <chat_id>
```

## User Commands

- `/zenQuote` or `/zenQuote today` - Today's inspirational quote
- `/zenQuote random` - Random quote
- `/zenQuote quotes` - Get 5 quotes
- `/zenQuote image` - Get and send quote image
- `/zenQuote setup` - Configure daily delivery (text or image)

## Image Command Handling

When user requests `/zenQuote image`, execute:
```bash
bash ~/.openclaw/skills/zenquote/scripts/zenquote.sh image
```

The script will download the image and output:
```json
{"image_path": "/tmp/zenquote_image.jpg", "caption": "Provided by ZenQuotes API https://zenquotes.io/"}
```

**AI must then send the image using the message tool with the provided caption. No additional text should be added.**

## Daily Cron Setup

To automatically send a quote every morning at 9:00 AM:

### Daily Text Quote (default)
```bash
bash ~/.openclaw/skills/zenquote/scripts/zenquote.sh setup <chat_id> text [account_id]
```

### Daily Image Quote
```bash
bash ~/.openclaw/skills/zenquote/scripts/zenquote.sh setup <chat_id> image [account_id]
```

This creates a cron job that runs daily at 9:00 AM.

## Examples

### Natural Language Usage
- "Give me today's quote"
- "Show me a random inspirational quote"
- "Send me the quote of the day"
- "Setup daily quotes for me"

### Command Examples

```bash
# Today's quote
bash ~/.openclaw/skills/zenquote/scripts/zenquote.sh today

# Random quote
bash ~/.openclaw/skills/zenquote/scripts/zenquote.sh random

# 3 quotes
bash ~/.openclaw/skills/zenquote/scripts/zenquote.sh quotes 3

# Get quote image URL
bash ~/.openclaw/skills/zenquote/scripts/zenquote.sh image

# Setup daily delivery
bash ~/.openclaw/skills/zenquote/scripts/zenquote.sh setup <chat_id> text
```

## API Response Format

```json
[
  {
    "q": "Quality means doing it right when no one is looking.",
    "a": "Henry Ford",
    "h": "<blockquote>\"Quality means doing it right when no one is looking.\" — <footer>Henry Ford</footer></blockquote>"
  }
]
```

## Attribution (Required)

⚠️ **When using the free API, you MUST include the following attribution:**

> Inspirational quotes provided by [ZenQuotes API](https://zenquotes.io/)

**Markdown format:**
```markdown
Inspirational quotes provided by [ZenQuotes API](https://zenquotes.io/)
```

**HTML format:**
```html
Inspirational quotes provided by <a href="https://zenquotes.io/" target="_blank">ZenQuotes API</a>
```

This skill automatically includes attribution in all outputs.

## API Limits

| Feature | Limit |
|---------|-------|
| Requests | 5 per 30 seconds |
| Endpoints | today, random, quotes, image |

## Installation

```bash
# Install from GitHub
git clone https://github.com/chrisluo5311/zenquote-skill.git

# Or install via OpenClaw
openclaw skills install zenquote
```

## External API

This skill uses the ZenQuotes.io API:
- Website: https://zenquotes.io/
- API Docs: https://docs.zenquotes.io/

## License

MIT

## Author

Created for OpenClaw AI Assistant
