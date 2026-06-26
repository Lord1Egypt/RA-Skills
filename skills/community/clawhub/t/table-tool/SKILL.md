---
name: table-tool
description: Format data into aligned table columns. Use for displaying structured data with organized rows and columns.
---
# Table - Data Table Formatter

Organize text data into visually aligned tables with configurable column widths, separators, and header rows. Supports pipe-delimited and space-separated input formats.

## Usage
```bash
table-tool [options] <file>
```

## Options

- `-s SEP`: Column separator (default: pipe |)
- `-a`: Auto-fit column widths
- `-h`: Treat first line as header

## Examples

```bash
table-tool data.txt
table-tool -s ',' -h data.csv
echo "a|b|c\n1|2|3" | table-tool
```