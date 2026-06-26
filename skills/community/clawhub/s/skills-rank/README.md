# 🔍 ClawHub Skill Search Rank Checker

Track and monitor the search ranking position of any skill on [ClawHub](https://clawhub.ai) across multiple keywords — like Google Search Console, but for ClawHub skills.

## Features

- **Single Keyword Lookup** — Check where your skill ranks for a specific search term
- **Batch Keyword Tracking** — Query multiple keywords in one go with a summary table
- **Competitor Analysis** — See who ranks above and below you
- **Top Results View** — See the top N results for any keyword
- **JSON Export** — Machine-readable output for trend tracking
- **Zero Dependencies** — Pure Python 3 standard library, no pip install needed

## Supported Metrics

| Metric | Description |
|--------|-------------|
| Rank Position | Where the skill appears in search results (#1–#10) |
| Total Results | How many results were returned for the keyword |
| Search Score | ClawHub's internal relevance score |
| Competitors | Skills ranked immediately above/below |

## Installation

### Via ClawHub CLI

```bash
npx clawhub install clawhub-skill-rank
```

### Manual Install

Copy the `clawhub-skill-rank/` folder into your skills directory:

```bash
cp -r clawhub-skill-rank/ ~/.openclaw/skills/clawhub-skill-rank/
```

## Usage Examples

### As an AI Skill

Just ask naturally:

- "Check where stock-price-query ranks for 'stock price' and 'finance'"
- "What's my skill's ranking for these keywords: stock, price, query"
- "Show me the top 5 results for 'todo app' on ClawHub"
- "查看 stock-price-query 在 'stock price' 关键词下的排名"
- "批量查询我的 skill 在这些关键词下的排名：stock, finance, query"

### Standalone CLI

```bash
# Basic rank check
python3 scripts/rank_checker.py stock-price-query "stock price"

# Multiple keywords
python3 scripts/rank_checker.py stock-price-query "stock price" "stock query" "finance"

# See top 5 results per keyword
python3 scripts/rank_checker.py stock-price-query "stock price" --top 5

# Competitor analysis with details
python3 scripts/rank_checker.py stock-price-query "stock price" --competitors --verbose

# JSON output for scripting
python3 scripts/rank_checker.py stock-price-query "stock" "price" --json
```

## Sample Output

```
=== ClawHub Search Rank: stock-price-query ===
Checked: 2026-03-17 14:30:00

  Keyword      Rank
  ───────────  ────────────────────
  stock price  🥈 #2/10
  stock query  🥇 #1/10
  finance      Not in top 10

Summary: 2 ranked / 1 not found / 0 errors out of 3 keywords
Best rank: #1 for "stock query"
Average rank: #1.5 (across 2 ranked keywords)
```

## API Reference

- **Search Endpoint**: `GET https://clawhub.ai/api/search?q={keyword}`
- **Auth**: None required (public API)
- **Rate Limit**: Built-in 0.3s delay between requests; auto-retry on 429
- **Max Results**: 10 per search query (ClawHub API limit)

## Project Structure

```
clawhub-skill-rank/
├── SKILL.md                # Skill definition (OpenClaw format)
├── README.md               # This file
├── CHANGELOG.md            # Version history
├── scripts/
│   └── rank_checker.py     # Core rank checking script
└── references/
    └── api-docs.md         # ClawHub Search API documentation
```

## Requirements

- Python 3.6+ (uses only standard library)
- Internet connection (to reach ClawHub API)

## License

MIT
