---
name: tar
version: "3.0.1"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [tar, tool, utility]
description: "Create, extract, list, and compress tar archives with format support. Use when scanning contents, monitoring sizes, reporting results, alerting corruption."
---

# tar

Archive management tool.

## Commands

### `create`

Create tar archive (.tar/.tar.gz/.tar.bz2/.tar.xz)

```bash
scripts/script.sh create <archive> <files...>
```

### `extract`

Extract archive contents

```bash
scripts/script.sh extract <archive> [dir]
```

### `list`

List archive contents with details

```bash
scripts/script.sh list <archive>
```

### `add`

Add files to uncompressed .tar archive

```bash
scripts/script.sh add <archive.tar> <files...>
```

### `info`

Show archive metadata (size, entries, format)

```bash
scripts/script.sh info <archive>
```

### `diff`

Compare contents of two archives

```bash
scripts/script.sh diff <a1> <a2>
```

### `verify`

Check archive integrity

```bash
scripts/script.sh verify <archive>
```

### `find`

Search for files matching pattern

```bash
scripts/script.sh find <archive> <pattern>
```

## Requirements

- bash 4.0+

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
