---
name: wc-lines-tool
description: Count lines, blank lines, code lines, and comment lines in text files. Useful for code statistics, log file sizing, and document analysis.
---

# WC Lines Tool — Line Counting Utility

Count lines in text input with smart detection of blank lines, code lines, comment lines, and non-empty content. Ideal for codebases, log analysis, and document statistics.

## Quick Start

```bash
# Count lines in a string
wc-lines-tool "line1\nline2\nline3"

# Count lines from stdin
cat README.md | wc-lines-tool

# Count lines in a file
wc-lines-tool --file log.txt
```

## Usage

```bash
wc-lines-tool [TEXT] [OPTIONS]
wc-lines-tool --file FILE [OPTIONS]

Options:
  --file FILE       Read from file instead of argument
  --non-blank       Count only non-empty lines
  --blank           Count only blank/empty lines
  --code            Count lines likely containing code (non-comment, non-blank)
  --max N           Report if line count exceeds N (exit 1 if over)
  --min N           Report if line count is below N (exit 1 if under)
  --json            Output as structured JSON
```

## Examples

```bash
# Total line count
wc-lines-tool --file server.log

# Non-blank lines only
wc-lines-tool --file app.py --non-blank

# Blank line count
wc-lines-tool --file main.go --blank

# Check log file size threshold (alert if > 10000 lines)
wc-lines-tool --file errors.log --max 10000

# Machine-readable output
wc-lines-tool --file data.csv --json
```

## Features

- **Line counting** — total, blank, non-blank, code
- **File, stdin, and argument input** — flexible sources
- **Threshold alerts** — --min/--max with exit codes for CI/CD
- **JSON output** — pipeline-friendly
- **Fast** — handles large files efficiently
- **UTF-8 safe** — handles arbitrary encodings
