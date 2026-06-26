---
name: stat-tool
description: Display detailed file or filesystem status information. Use for checking file permissions, sizes, timestamps, and metadata.
---
# Stat - File Status Utility

Show comprehensive file metadata including size, permissions, ownership, access/modification/change timestamps, and file type. Also supports filesystem statistics.

## Usage
```bash
stat-tool [options] <file...>
```

## Options

- `-c FORMAT`: Custom output format
- `-f`: Show filesystem status instead of file status
- `-t`: Terse output format

## Examples

```bash
stat-tool file.txt
stat-tool -f /
stat-tool -c "%s %y" document.pdf
```