---
name: wenxuecity-news-rankings
description: Fetch and format Wenxuecity News rankings from https://www.wenxuecity.com/news/, specifically the two 24-hour lists (hot ranking and discussion ranking). Use when you need to collect, summarize, monitor, or diff these ranking entries and output Markdown/JSON for a daily digest or automation.
---

# Wenxuecity News Rankings

## Quick start

Fetch both 24-hour ranking lists and print Markdown.

Windows (PowerShell):

```powershell
py scripts/fetch_rankings.py --format md
```

Linux/macOS (bash/zsh):

```bash
python3 scripts/fetch_rankings.py --format md
```

Output JSON (for storage/diff/automation).

Windows (PowerShell):

```powershell
py scripts/fetch_rankings.py --format json --pretty --top 50 --output rankings.json
```

Linux/macOS (bash/zsh):

```bash
python3 scripts/fetch_rankings.py --format json --pretty --top 50 --output rankings.json
```

## Output conventions

- Two groups: `hot_24h`, `discussion_24h`
- Each item: `rank`, `title`, `url` (optional: `image_url`)
 - Default behavior: `--top 15` (override via `--top N`; use `--top 0` for all)

## Notes

- This skill only fetches the ranking entries (not article bodies).
- If Wenxuecity page structure changes, update `scripts/fetch_rankings.py` and validate against the live page.
- The source page may contain fewer than 15 entries for a given list; the script outputs what is available.
