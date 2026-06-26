---
name: rm-tool
description: Remove files and directories permanently. Use for file deletion, cleanup, and disk space management.
---
# RM - File Removal Utility

Delete files and directories from the filesystem. Supports recursive directory removal, interactive confirmation, and force deletion.

## Usage
```bash
rm-tool [options] <target...>
```

## Options

- `-r`: Recursively remove directories
- `-f`: Force removal (ignore nonexistent files)
- `-i`: Interactive (prompt before each removal)
- `-v`: Verbose (show what is being removed)

## Examples

```bash
rm-tool file.txt
rm-tool -rf temp_directory/
rm-tool -i *.log
```