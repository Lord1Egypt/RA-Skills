---
name: github-trending
description: "通过网页抓取获取 GitHub 按日/周/月增长的热门仓库。当用户询问 GitHub 趋势、热门项目、本周热点或「什么在 GitHub 上 trending」时使用。可输出列表或 JSON，无需 API Key。"
---

# GitHub Trending

Fetches GitHub Trending repositories (daily/weekly/monthly). Uses only Python standard library; no external packages.

## When to Use

- User asks for **GitHub trending**, **popular repos**, **本周热点** / this week's hotspots
- User wants **daily** / **weekly** / **monthly** trending
- User wants trending filtered by **programming language**

## Quick Start

Run from the skill directory (e.g. `github-trending/`):

```bash
# Weekly trending (default), 15 repos
python scripts/github_trending.py weekly

# Daily trending, 10 repos
python scripts/github_trending.py daily --limit 10

# Weekly trending in Python
python scripts/github_trending.py weekly --language python

# JSON output (for piping or tooling)
python scripts/github_trending.py weekly --json
```

## Parameters

| Argument | Values | Default | Description |
|----------|--------|---------|-------------|
| `period` | `daily`, `weekly`, `monthly` | `weekly` | Time range for "stars gained" |
| `--limit` | integer | 15 | Max number of repos to return |
| `--language` | string | (all) | Filter by language (see below) |
| `--json` | flag | — | Output JSON instead of human-readable text |

**Language**: Use full name or alias. Script supports aliases: `py`→python, `ts`→typescript, `js`→javascript, `cpp`/`c++`→c++, `c#`/`csharp`→c#, `rs`→rust, `rb`→ruby, `go`→go. Others are passed as-is (e.g. `--language "c"`).

## Output

### Text (default)

- Rank (numeric), repo `full_name`, description (trimmed to 90 chars)
- 每行统计符号含义：
  - **🔧** 编程语言（Language）
  - **⭐** 总 Star 数（total stars）
  - **📈** 本周期新增 Star 数（stars gained in the selected period）
- 时间以北京时区 (UTC+8) 显示

### JSON (`--json`)

```json
{
  "period": "weekly",
  "updated_at": "2026-03-13T21:00:00+08:00",
  "data": [
    {
      "rank": 1,
      "full_name": "owner/repo",
      "url": "https://github.com/owner/repo",
      "description": "...",
      "language": "Python",
      "stars_total": "12345",
      "stars_gained": 1234
    }
  ]
}
```

## Data Source

- **URL**: `https://github.com/trending` (and `.../trending/<language>?since=<period>`)
- **Method**: HTTP + `html.parser.HTMLParser` (no browser, no auth)
- **Fresh**: Each run fetches the current page

## Dependencies

Python standard library only: `urllib.request`, `html.parser`, `json`, `argparse`, `datetime`. **No pip install required.**

## Troubleshooting

| Issue | What to do |
|-------|------------|
| Empty `data` / no repos | Network may have closed early (IncompleteRead). Retry; if script supports it, use chunked read. |
| Parse errors / wrong structure | GitHub may have changed HTML; script may need selector/parser updates. |
| Timeout | Check network; default timeout 15s. |
| Windows console encoding error on emoji | Set `PYTHONIOENCODING=utf-8` or run with `--json` and parse elsewhere. |

## Notes

- Trending is by **stars gained** in the chosen period, not total stars.
- For GitHub API (e.g. search by stars, auth), use a separate GitHub API skill.
