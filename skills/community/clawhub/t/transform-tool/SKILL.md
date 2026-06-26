---
name: transform-tool
description: Apply data transformations like case changes, encoding conversion, and format conversion. Use for text processing and data cleaning.
---
# Transform - Data Transformation Utility

Apply various text transformations including case conversion (upper/lower/title), whitespace trimming, character replacement, and encoding changes.

## Usage
```bash
transform-tool [options] <file>
```

## Options

- `--upper`: Convert to uppercase
- `--lower`: Convert to lowercase
- `--title`: Convert to Title Case
- `--trim`: Remove leading/trailing whitespace
- `--reverse`: Reverse text

## Examples

```bash
transform-tool --upper file.txt
transform-tool --lower input.txt
echo "  hello  " | transform-tool --trim
```