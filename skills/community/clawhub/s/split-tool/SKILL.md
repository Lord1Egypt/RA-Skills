---
name: split-tool
description: Split files into smaller pieces by size, line count, or number of chunks. Use for breaking large files into manageable parts.
---
# Split - File Fragmenter

Divide large files into smaller segments based on line count, byte size, or number of output files. Useful for breaking up logs or data files.

## Usage
```bash
split-tool [options] <file> [prefix]
```

## Options

- `-l N`: Split every N lines (default: 1000)
- `-b SIZE`: Split by byte size (e.g. 10M, 1G)
- `-n N`: Split into N chunks

## Examples

```bash
split-tool -l 500 large_log.txt log_part_
split-tool -b 10M data.bin part_
split-tool -n 5 bigfile.txt chunk_
```