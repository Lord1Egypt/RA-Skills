---
name: wc-tool
description: Count lines, words, characters, and bytes in one or more files with per-file and total summary. Use for document statistics, code analysis, and data volume estimation.
---

# WC Tool — Word, Line & Character Counter

Multi-file word count utility. Count lines, words, characters (multibyte-aware), and bytes across one or more files with per-file breakdown and grand total. Supports standard input for pipeline use.

## Quick Start

```bash
# Count everything for a file
wc-tool document.txt

# Count lines only
wc-tool -l script.py

# Count from stdin
cat file.txt | wc-tool -w
```

## Usage

```bash
wc-tool [OPTIONS] [FILE...]
cat INPUT | wc-tool [OPTIONS]

Options:
  -l, --lines     Count lines only
  -w, --words     Count words only
  -c, --bytes     Count bytes only
  -m, --chars     Count characters (multibyte-aware)
  -L, --max-line  Print length of longest line
  --files0-from FILE   Read input file list from FILE (null-separated)
  --total          Show grand total (default with multiple files)
  --json          Output as structured JSON
```

## Examples

```bash
# Full count (lines, words, chars, bytes)
wc-tool README.md

# Lines only (code file size metric)
wc-tool -l src/main.py src/utils.py

# Characters in a file (UTF-8 aware)
wc-tool -m document.txt

# Longest line length
wc-tool -L src/main.py

# Pipe from another command
ls /usr/bin | wc-tool -l

# JSON output for automation
wc-tool -l -w *.py --json

# Multiple files with total
wc-tool *.txt
```

## Features

- **4 modes** — lines, words, characters (multibyte), bytes
- **Multi-file** — process many files, show per-file + total
- **Stdin support** — pipe input from other commands
- **Longest line** — detect max line length
- **JSON output** — structured for scripts
- **Null-separated file list** — safe file name handling
- **Exit code 0/1** — script-friendly
