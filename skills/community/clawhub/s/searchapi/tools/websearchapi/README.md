# WebSearchAPI

Multi-type search tool based on SearchAPI (Google) for AI agents.

## Features

- Multiple search types: Web, News, Video, Finance, Maps, Hotels, Flights
- Time filtering support
- Auto retry on failure
- Structured JSON output
- Zero external dependencies

## Installation

```bash
cd tools/websearchapi
node websearchapi.js config set-key YOUR_API_KEY
```

Get API Key: https://searchapi.io

## Usage

```bash
# Web search
node websearchapi.js s "query"

# News search
node websearchapi.js news "AI"

# Finance search
node websearchapi.js finance "AAPL"

# With time filter
node websearchapi.js news "tech" --time=last_week

# JSON output
node websearchapi.js s "query" --json
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--num` | Result count | 5 |
| `--lang` | Language | zh-CN |
| `--gl` | Country | cn |
| `--time` | Time filter | - |
| `--json` | JSON output | text |

## Time Values

- `last_hour` - Past hour
- `last_day` - Past day
- `last_week` - Past week
- `last_month` - Past month
- `last_year` - Past year

## Config

```bash
node websearchapi.js config set-key YOUR_KEY
node websearchapi.js config set-num 10
node websearchapi.js config set-lang en
```

## Troubleshooting

- Check API Key: `node websearchapi.js config`
- Test: `node websearchapi.js test`
