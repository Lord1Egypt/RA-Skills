# ZenQuote Skill for OpenClaw

Daily inspirational quotes from ZenQuotes.io

## Overview

ZenQuote skill fetches inspirational quotes from ZenQuotes.io API and delivers them to users. All features use the free API tier.

## Features

- ✅ Daily quote (`today`)
- ✅ Random quote (`random`)
- ✅ Multiple quotes (`quotes`)
- ✅ Quote images (`image`)
- ✅ Automated daily delivery (`setup`)

## Dependencies

This skill requires:
- `curl` - For HTTP requests (usually pre-installed)
- `jq` - For JSON parsing (usually pre-installed)

## Quick Start

```bash
# Get today's quote
bash ~/.openclaw/skills/zenquote/scripts/zenquote.sh today

# Get random quote
bash ~/.openclaw/skills/zenquote/scripts/zenquote.sh random

# Setup daily delivery at 9:00 AM
bash ~/.openclaw/skills/zenquote/scripts/zenquote.sh setup <chat_id>
```

## Commands

| Command | Description |
|---------|-------------|
| `today` | Get today's quote |
| `random` | Get random quote |
| `quotes [count]` | Get multiple quotes (default 5) |
| `image` | Get and download quote image |
| `setup <chat_id> [type]` | Setup daily cron job (type: text or image) |

## User Commands

- `/zenQuote` or `/zenQuote today` - Today's quote
- `/zenQuote random` - Random quote
- `/zenQuote quotes` - Get 5 quotes
- `/zenQuote image` - Quote image
- `/zenQuote setup` - Configure daily delivery

## Daily Cron Setup

### Text Quote (default)
```bash
bash ~/.openclaw/skills/zenquote/scripts/zenquote.sh setup <chat_id> text [account_id]
```

### Image Quote
```bash
bash ~/.openclaw/skills/zenquote/scripts/zenquote.sh setup <chat_id> image [account_id]
```

This creates a cron job that sends a quote/image every day at 9:00 AM.

## API Limits & Attribution

- **Rate Limit**: 5 requests per 30 seconds
- **Attribution Required**: You MUST display the following attribution when using quotes:

> Inspirational quotes provided by [ZenQuotes API](https://zenquotes.io/)

Or in HTML:
```html
Inspirational quotes provided by <a href="https://zenquotes.io/" target="_blank">ZenQuotes API</a>
```

## Installation

```bash
# Via OpenClaw
openclaw skills install zenquote

# Or from GitHub
git clone https://github.com/chrisluo5311/zenquote-skill.git
cp -r zenquote-skill ~/.openclaw/skills/zenquote
```

## External API

- Website: https://zenquotes.io/
- API Docs: https://docs.zenquotes.io/

## License

MIT

## Author

Created for OpenClaw AI Assistant
