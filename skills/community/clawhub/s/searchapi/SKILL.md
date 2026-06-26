---
name: websearchapi
description: "Web/News/Finance/Video/Maps/Hotels/Flights search tool based on SearchAPI (Google). Supports time filtering, ideal for agents to get real-time web information."
metadata: { "openclaw": { "emoji": "🔍", "requires": { "bins": ["node"] } } }
---

# WebSearchAPI

A multi-type search tool based on SearchAPI (Google), ideal for agents to retrieve real-time web information.

## Features

- **Multiple Search Types**: Web, News, Video, Finance, Maps, Hotels, Flights
- **Time Filtering**: Search by time range
- **Auto Retry**: Automatic retry on network errors for stability
- **Structured Output**: Agent-ready JSON format
- **Zero Dependencies**: Pure Node.js built-in modules

## Installation

```bash
# Copy tools/websearchapi to your project
# Configure API Key (required)
cd tools/websearchapi
node websearchapi.js config set-key YOUR_API_KEY
```

Get API Key: https://searchapi.io (Free registration)

⚠️ **Important**: Use your own API Key, not someone else's

## Usage

Call via `exec` tool:

```bash
node <path>/websearchapi.js <command> [keyword] [options]
```

### Search Types

| Type | Command | Description |
|------|---------|-------------|
| Web | `s` or `search` | General web search |
| News | `news` | Latest news |
| Video | `video` | Video search |
| Finance | `finance` | Stock/Financial info |
| Maps | `maps` | Places/Business |
| Hotels | `hotels` | Hotel search |
| Flights | `flights` | Flight search |

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `--num` | Number of results | 5 |
| `--lang` | Language | zh-CN |
| `--gl` | Country | cn |
| `--time` | Time range | none |
| `--json` | JSON output | text |

### Time Filtering

| Value | Description |
|-------|-------------|
| `last_hour` | Past hour |
| `last_day` | Past day |
| `last_week` | Past week |
| `last_month` | Past month |
| `last_year` | Past year |

## Agent Examples

```bash
# Web search
node websearchapi.js s "MCP protocol"

# News search (past week)
node websearchapi.js news "AI" --time=last_week

# Finance search
node websearchapi.js finance "AAPL"

# Time filter (past 24 hours)
node websearchapi.js s "keyword" --time=last_day

# JSON format (recommended for parsing)
node websearchapi.js s "keyword" --json
```

## Response Format

JSON mode returns:

```json
{
  "success": true,
  "query": "keyword",
  "type": "google",
  "count": 5,
  "results": [
    {
      "title": "Result Title",
      "link": "URL",
      "snippet": "Summary",
      "source": "Source"
    }
  ],
  "metadata": {
    "totalResults": number,
    "timeTaken": seconds,
    "engine": "google"
  }
}
```

## Configuration

### First Time - Configure API Key

```bash
cd tools/websearchapi
node websearchapi.js config set-key YOUR_API_KEY
```

### View/Modify Config

```bash
# View config (Key hidden)
node websearchapi.js config

# Set API Key
node websearchapi.js config set-key YOUR_API_KEY

# Modify defaults
node websearchapi.js config set-num 10      # Default result count
node websearchapi.js config set-lang en     # Default language
node websearchapi.js config set-gl us       # Default country
node websearchapi.js config set-retry 5     # Retry count
```

## Deployment

```bash
# Copy to new machine
scp -r ./tools/websearchapi user@new-server:/path/to/tools/

# Configure your own API Key
cd /path/to/tools/websearchapi
node websearchapi.js config set-key YOUR_API_KEY

# Test
node websearchapi.js test
```

## Troubleshooting

### Search Failed
- Check API Key: `node websearchapi.js config`
- Verify Key: https://searchapi.io/dashboard

### Finance No Results
- Try stock code: `finance "AAPL"`
- Try English: `finance "Tesla stock"`

### Request Timeout
- Increase retry: `config set-retry 5`

## Security Notes

- ⚠️ Always use your own API Key
- 🔐 API Key stored in local config.json
- 🚫 Don't share packages with API Key included
