---
name: unzip-tool
description: List, test, and extract files from ZIP archives. Use when you need to decompress or inspect ZIP file contents.
---

# ZIP Extraction Utility

Extract files from ZIP archives with support for selective extraction, overwrite control, and archive inspection.

## Usage

```bash
unzip-tool [options] <archive> [file...]
```

## Options

- `-l`: List archive contents without extracting
- `-d dir`: Extract to specified directory
- `-o`: Overwrite files without prompting
- `-n`: Never overwrite existing files

## Examples

```bash
# Extract to current directory
unzip-tool archive.zip

# Extract to specific folder
unzip-tool archive.zip -d /target/dir

# List contents only
unzip-tool -l archive.zip
```