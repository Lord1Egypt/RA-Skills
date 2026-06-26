---
name: tar-tool
description: Create and extract tar archives with optional compression. Use for file bundling, backup, and distribution.
---
# Tar - Tape Archive Utility

Create, maintain, and extract tar archives. Supports gzip, bzip2, and xz compression for efficient storage and transfer.

## Usage
```bash
tar-tool [options] <archive> [files...]
```

## Common Commands

- `-cf archive.tar files`: Create archive
- `-xf archive.tar`: Extract archive
- `-tf archive.tar`: List contents
- `-czf archive.tar.gz files`: Create gzip compressed
- `-cjf archive.tar.bz2 files`: Create bzip2 compressed

## Examples

```bash
tar-tool -cf backup.tar ./docs/
tar-tool -czf archive.tar.gz ./project/
tar-tool -xf archive.tar.gz
```