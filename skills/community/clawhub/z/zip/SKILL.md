---
name: zip
version: "3.0.1"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [zip, tool, utility]
description: "Compress, extract, list, and encrypt ZIP archives in batch. Use when archiving files, extracting packages, listing contents, encrypting backups, or batching."
---

# zip

ZIP archive tool.

## Commands

### `create`

Create ZIP archive

```bash
scripts/script.sh create <archive.zip> <files...>
```

### `extract`

Extract archive

```bash
scripts/script.sh extract <archive.zip> [dir]
```

### `list`

List contents

```bash
scripts/script.sh list <archive.zip>
```

### `add`

Add files to archive

```bash
scripts/script.sh add <archive.zip> <files...>
```

### `password`

Create encrypted ZIP

```bash
scripts/script.sh password <archive> <pass> <files...>
```

### `info`

Archive metadata

```bash
scripts/script.sh info <archive.zip>
```

### `test`

Test integrity

```bash
scripts/script.sh test <archive.zip>
```

### `find`

Search for files

```bash
scripts/script.sh find <archive.zip> <pattern>
```

### `diff`

Compare two archives

```bash
scripts/script.sh diff <a1.zip> <a2.zip>
```

## Requirements

- bash 4.0+

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
