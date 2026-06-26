---
name: clawhub-skill-rank
description: "Track and monitor the search ranking position of any ClawHub skill across multiple keywords. Check where your skill ranks for 'stock price', 'todo app', etc. Supports single keyword lookup, batch keyword tracking, competitor comparison, and JSON export. Use when: user wants to check their skill's search ranking on ClawHub, monitor SEO position, compare with competitors, or track keyword performance — like Google Search Console but for ClawHub skills."
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["python3"] },
        "tags":
          [
            "clawhub",
            "search",
            "ranking",
            "SEO",
            "analytics",
            "skill-rank",
            "keyword-tracking",
            "position-monitor",
            "skill-search",
            "developer-tools",
          ],
      },
  }
---

# ClawHub Skill Search Rank Checker

Track the search ranking position of any skill on ClawHub across multiple keywords.

## When to Use

Use this skill when the user wants to:

- Check where their skill ranks for specific search keywords on ClawHub
- Monitor search position changes across multiple keywords
- Compare their skill's ranking against competitors
- Understand which keywords their skill performs best/worst on
- Get keyword ranking data in JSON format for tracking over time

Trigger phrases: "check my skill's ranking", "where does my skill rank", "search position", "keyword ranking", "ClawHub SEO", "排名", "搜索排名", "关键词排名"

## How to Use

### 1. Single Keyword Rank Check

To check where a skill ranks for a single keyword:

```bash
python3 {{SKILL_DIR}}/scripts/rank_checker.py SKILL_SLUG "keyword"
```

Replace `SKILL_SLUG` with the skill's slug (the last part of `https://clawhub.ai/owner/SLUG`) and `"keyword"` with the search term.

### 2. Batch Keyword Rank Check

To check ranking across multiple keywords at once:

```bash
python3 {{SKILL_DIR}}/scripts/rank_checker.py SKILL_SLUG "keyword1" "keyword2" "keyword3"
```

This will output a summary table showing the rank for each keyword.

### 3. Show Top Results

To see the top N results for each keyword (useful for seeing who ranks above you):

```bash
python3 {{SKILL_DIR}}/scripts/rank_checker.py SKILL_SLUG "keyword" --top 5
```

### 4. Competitor Analysis

To see skills ranked immediately above and below your skill:

```bash
python3 {{SKILL_DIR}}/scripts/rank_checker.py SKILL_SLUG "keyword1" "keyword2" --competitors
```

### 5. Verbose Output

To see full details including scores and descriptions:

```bash
python3 {{SKILL_DIR}}/scripts/rank_checker.py SKILL_SLUG "keyword" --verbose --top 10
```

### 6. JSON Export

To get machine-readable output for tracking/scripting:

```bash
python3 {{SKILL_DIR}}/scripts/rank_checker.py SKILL_SLUG "keyword1" "keyword2" --json
```

## Output Format

### Text Output (default)

The text output shows:
- A summary table with keyword → rank mapping
- Emoji medals for top 3 positions (🥇🥈🥉)
- Overall statistics (ranked count, average rank, best rank)

Present the results to the user in a clean markdown table:

| Keyword | Rank | Notes |
|---------|------|-------|
| stock price | 🥇 #1/10 | Best position |
| stock query | 🥈 #2/10 | |
| finance | Not in top 10 | Need optimization |

### JSON Output

The JSON output includes:
- `skill`: the queried slug
- `checked_at`: timestamp
- `results[]`: array of per-keyword results, each with `keyword`, `rank`, `total`, `rank_display`, and optionally `top_results[]` or `competitors[]`

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `SKILL_SLUG` | Yes | The slug of the skill to check (from ClawHub URL) |
| `keywords` | Yes (1+) | One or more search keywords to check ranking for |
| `--top N` | No | Show top N results per keyword |
| `--verbose` | No | Show detailed output with scores and descriptions |
| `--competitors` | No | Show skills ranked near the target |
| `--json` | No | Output in JSON format |

## Edge Cases

- **Skill not in results**: Reports "Not in top N" — ClawHub search returns up to 10 results per query
- **No search results**: Some keywords (especially non-English) may return empty results from ClawHub
- **Rate limiting**: Built-in 0.3s delay between requests; auto-retries on 429 errors
- **Network errors**: Gracefully reported per-keyword, does not abort the entire batch
- **Empty keyword**: Rejected with error message

## Notes

- Uses the public ClawHub search API (`GET https://clawhub.ai/api/search?q={keyword}`), no authentication needed
- Search results are limited to top 10 by ClawHub's API
- Rankings are real-time snapshots; they may fluctuate based on ClawHub's search algorithm
- For tracking trends over time, use `--json` output and save/compare results periodically
