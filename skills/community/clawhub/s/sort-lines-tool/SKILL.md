---
name: sort-lines-tool
description: Sort lines of text alphabetically or numerically. Use for data organization, list management, and text file preparation.
---
# Sort Lines - Line Sorting Tool

Arrange text lines in alphabetical or numerical order. Supports case-insensitive sorting, reverse order, and unique line filtering.

## Usage
```bash
sort-lines-tool [options] <file>
```

## Options

- `-n`: Numeric sort (instead of alphabetical)
- `-r`: Reverse order
- `-u`: Unique lines only
- `-f`: Case-insensitive sort

## Examples

```bash
sort-lines-tool names.txt
sort-lines-tool -n numbers.txt
sort-lines-tool -r data.txt
```