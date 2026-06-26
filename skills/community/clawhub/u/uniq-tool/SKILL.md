---
name: uniq-tool
description: Report or filter repeated lines in sorted text. Use for deduplication, frequency counting, and data cleanup.
---

# Duplicate Line Filter

Remove or count consecutive duplicate lines from sorted input. Works best with pre-sorted data using sort-tool.

## Usage

```bash
uniq-tool [options] [input_file [output_file]]
```

## Options

- `-c`: Count occurrences of each line
- `-d`: Only show duplicate lines
- `-u`: Only show unique (non-duplicate) lines
- `-i`: Case-insensitive comparison

## Examples

```bash
# Remove adjacent duplicates
uniq-tool sorted.txt

# Count occurrences
uniq-tool -c sorted.txt

# Only show duplicates
uniq-tool -d sorted.txt
```