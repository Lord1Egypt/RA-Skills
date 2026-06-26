---
name: singapore-pools-toto-results
description: Fetch and summarize latest Singapore Pools TOTO results from official Singapore Pools data files (normal, cascade, hongbao, special). Use when users ask for latest TOTO winning numbers, additional number, draw number/date, Group 1 prize, winning shares, or need JSON output sourced from singaporepools.com.sg.
---

# Singapore Pools Toto Results

## Overview

Fetch the latest TOTO result directly from Singapore Pools generated result files and return clean text or JSON.

## Workflow

1. Run the fetch script from this skill directory.
2. Choose draw type (`normal`, `cascade`, `hongbao`, `special`) as needed.
3. Use `--format text` for chat replies and `--format json` for automation.
4. Include the reported `Source` URL when citing results.

## Commands

```bash
python3 scripts/fetch_toto_latest.py
python3 scripts/fetch_toto_latest.py --draw-type cascade
python3 scripts/fetch_toto_latest.py --draw-type hongbao --format json
python3 scripts/fetch_toto_latest.py --draw-type special --format json
```

## Output Contract

The script returns:

- draw date
- draw number
- 6 winning numbers
- additional number
- Group 1 prize
- winning shares table
- single-draw page URL (`/en/product/sr/Pages/toto_results.aspx?...`)
- source file URL used for retrieval

## Troubleshooting

- If network fetch fails, retry with a larger timeout: `--timeout 30`.
- If parsing fails, inspect endpoint HTML structure and update regexes in `scripts/fetch_toto_latest.py`.
- If Singapore Pools changes filenames or hosting paths, update mappings in `references/source-endpoints.md`.

## Resources

- `scripts/fetch_toto_latest.py`: Fetch and parse latest result payload.
- `references/source-endpoints.md`: Official endpoint mapping and parser assumptions.
