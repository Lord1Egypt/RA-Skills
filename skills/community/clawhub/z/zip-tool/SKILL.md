---
name: zip-tool
description: Package and compress files into ZIP archives with configurable compression levels, password protection, directory recursion, and cross-platform compatibility. Create, update, list, and extract ZIP archives.
---

# ZIP Tool — Archive Manager

Create, update, list, and extract ZIP archives. Supports recursive directory inclusion, compression level control, password encryption, and cross-platform compatibility.

## Quick Start

```bash
# Create a ZIP archive
zip-tool -r archive.zip ./documents/

# List archive contents
zip-tool -l archive.zip

# Extract archive
zip-tool -x archive.zip -d ./output/
```

## Usage

```bash
zip-tool [OPTIONS] ARCHIVE [FILES...]

Options:
  -r, --recursive      Recursively include directories
  -l, --list           List contents of an archive
  -x, --extract        Extract an archive
  -d, --delete PATTERN Remove entries matching pattern
  -u, --update         Update existing entries or add new ones
  -P, --password PASS  Protect archive with password
  -c, --compress N     Compression level (0-9, default: 6)
  -o, --output DIR     Extract destination directory
  --overwrite          Overwrite existing files when extracting
  --json               Output archive metadata as JSON
```

## Examples

```bash
# Create a ZIP with directory
zip-tool -r backup.zip ./my-project/

# Create with maximum compression
zip-tool -r -c 9 archive.zip ./data/

# List archive contents
zip-tool -l backup.zip

# Extract to specific directory
zip-tool -x archive.zip -d ./restored/

# Password-protected archive
zip-tool -r -P secret123 confidential.zip ./docs/

# Update an existing archive
zip-tool -u archive.zip ./new-file.txt

# Delete entries matching pattern
zip-tool -d "*.tmp" archive.zip

# Archive metadata as JSON
zip-tool -l backup.zip --json
```

## Features

- **Create/extract/update** — full archive lifecycle
- **Directory recursion** — pack entire folder trees
- **Compression levels** — 0 (store) to 9 (maximum)
- **Password encryption** — AES-256 and traditional ZIP encryption
- **List contents** — inspect archives without extracting
- **Pattern deletion** — selective entry removal
- **Cross-platform** — compatible with all major OS ZIP tools
- **JSON output** — structured archive metadata
