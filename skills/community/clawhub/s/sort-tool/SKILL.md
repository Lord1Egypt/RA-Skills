---
name: sort-tool
description: Sort lines of text files alphabetically or numerically. Use for data preparation, list organization, and output formatting.
---

# Line Sorting Utility

Arrange text file lines in specified order with support for numeric, month-name, and reverse sorting. Handles large files efficiently.

## Usage

```bash
sort-tool [options] [file...]
```

## Options

- `-n`: Numeric sort
- `-r`: Reverse order
- `-u`: Unique lines (remove duplicates)
- `-k N`: Sort by column N
- `-t SEP`: Use SEP as field separator

## Examples

```bash
# Alphabetical sort
sort-tool names.txt

# Numeric sort
sort-tool -n numbers.txt

# Sort by column 2
sort-tool -k 2 -t ',' data.csv
```