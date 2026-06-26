---
name: unexpand-tool
description: Convert spaces to tabs in text files. Use for consistent indentation and reducing file size by replacing spaces with tabs.
---
# Unexpand - Space to Tab Converter

Replace sequences of spaces with tab characters. The inverse operation of expand-tool. Ideal for converting space-indented code to tab-indented format.

## Usage
```bash
unexpand-tool [options] <file>
```

## Options

- `-t N`: Set tab width in spaces (default: 8)
- `-a`: Convert all spaces, not just leading
- `--first-only`: Only convert leading sequences

## Examples

```bash
unexpand-tool -t 4 file.py
unexpand-tool -a -t 2 data.txt
cat spaces.txt | unexpand-tool
```