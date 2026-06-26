---
name: tavily-metered-search
description: "Web search via Tavily API with built-in monthly usage tracking and quota management. Use when the user asks to search the web / look up sources / find links. Features: automatic usage counting, monthly limit enforcement, warning alerts. Alternative to Brave web_search."
metadata:
  openclaw:
    requires:
      env: ["TAVILY_API_KEY"]
---

# Tavily Metered Search

Web search with built-in usage tracking and quota management for Tavily API (free tier: 1000 searches/month).

## Quick Start

```bash
# Basic search (Markdown output, default)
python3 {baseDir}/scripts/tavily_search.py --query "AI news today"

# With short answer
python3 {baseDir}/scripts/tavily_search.py --query "what is RAG" --include-answer

# JSON output
python3 {baseDir}/scripts/tavily_search.py --query "python tutorial" --format raw
python3 {baseDir}/scripts/tavily_search.py --query "python tutorial" --format brave

# Skip counting (for testing)
python3 {baseDir}/scripts/tavily_search.py --query "test" --no-count
```

## Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--query` | (required) | Search query string |
| `--max-results` | 5 | Number of results (1-10), configurable via config file |
| `--format` | `md` | Output: `raw` (JSON), `brave` (JSON), `md` (Markdown) |
| `--include-answer` | false | Include AI-generated short answer |
| `--search-depth` | `basic` | `basic` or `advanced`, configurable via config file |
| `--no-count` | false | Skip usage tracking (still consumes API quota) |

## Configuration

Edit `config/config.json` to customize default settings:

```json
{
  "limit": 900,
  "warningThreshold": 800,
  "searchDepth": "basic",
  "defaultMaxResults": 5
}
```

| Setting | Description | Default |
|---------|-------------|---------|
| `limit` | Monthly limit, blocks search when reached | 900 |
| `warningThreshold` | Warning threshold, shows alert when reached | 800 |
| `searchDepth` | Default search depth | basic |
| `defaultMaxResults` | Default number of results | 5 |

## Usage Tracking

- **Automatic tracking**: Each successful search increments a counter stored in `data/tavily-usage.json`
- **Monthly reset**: Counter resets on the 1st of each month
- **Limit enforcement**: When `limit` is reached, search is blocked with a message suggesting `web_fetch` as alternative
- **Warning alert**: When `warningThreshold` is reached, a reminder is appended to search results

## Output Formats

### `md` (default)
Human-readable Markdown list:
```
1. Title
   https://example.com
   - Snippet text...
```

### `raw`
Full JSON with `query`, `answer?`, `results: [{title, url, content}]`

### `brave`
Brave-like format: `{query, results: [{title, url, snippet}], answer?}`

## Requirements

- Tavily API key via either:
  - Environment variable: `TAVILY_API_KEY`
  - `~/.openclaw/.env` file: `TAVILY_API_KEY=tvly-...`

Get a free API key at https://tavily.com

## File Structure

```
tavily-metered-search/
├── SKILL.md                    # Skill documentation
├── scripts/
│   └── tavily_search.py        # Main search script
├── config/
│   └── config.json             # User configuration
└── data/
    └── tavily-usage.json       # Runtime state (auto-maintained)
```

## Notes

- Free tier: 1000 searches/month (default limit is 900 to leave buffer)
- Keep `--max-results` small (3-5) to reduce token usage
- Use `--no-count` for testing without affecting quota