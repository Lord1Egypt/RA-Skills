---
name: sort
version: "3.0.2"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [sort, tool, utility]
description: "Sort files, lines, and columns with custom ordering and dedup. Use when scanning duplicates, monitoring changes, reporting results, alerting anomalies."
---

# sort

File & Text Sorting Tool.

## Commands

### `lines`

Sort lines (flags: -r reverse, -n numeric, -u unique)

```bash
scripts/script.sh lines <file> [-r] [-n] [-u]
```

### `csv`

Sort CSV file by column number (1-based)

```bash
scripts/script.sh csv <file> <column>
```

### `json`

Sort JSON array by a key

```bash
scripts/script.sh json <file> <key>
```

### `dedup`

Remove duplicate lines (preserving order)

```bash
scripts/script.sh dedup <file>
```

### `shuffle`

Randomly shuffle lines

```bash
scripts/script.sh shuffle <file>
```

### `rank`

Rank/sort tabular data by a numeric column

```bash
scripts/script.sh rank <file> <column>
```

### `top`

Show top N entries by column value

```bash
scripts/script.sh top <file> <column> [n]
```

### `freq`

Frequency analysis — count occurrences of each line

```bash
scripts/script.sh freq <file>
```

### `stats`

Show basic stats about the file content

```bash
scripts/script.sh stats <file>
```

## Requirements

- python3
- jq (optional)

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*

## Data Storage

Operation history is logged to `~/.local/share/sort/history.log` for audit purposes.
