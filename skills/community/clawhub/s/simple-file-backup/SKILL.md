---
name: file-backup
version: 1.0.0
description: >-
  Create a timestamped backup copy of a file in the same directory.
  Use when the user wants to save a copy of a file before making changes.
allowed-tools: Bash(cp:*)
metadata: >-
  {"openclaw":{"emoji":"📋","requires":{"bins":["cp","date"],"env":[]},"install":[]}}
---

# File Backup

Create a timestamped backup copy of any file with a single command.

## Usage

```bash
cp <FILE_PATH> <FILE_PATH>.bak.$(date +%Y%m%d_%H%M%S)
```

**Arguments:**
| # | Name | Description |
|---|------|-------------|
| 1 | FILE_PATH | Path to the file to back up |

## Example

```bash
cp /home/user/config.yaml /home/user/config.yaml.bak.$(date +%Y%m%d_%H%M%S)
```

**Output:**
```
(no output on success)
```

The backup file is created as: `ORIGINAL_NAME.bak.YYYYMMDD_HHMMSS`

Example: `config.yaml` → `config.yaml.bak.20260328_143022`

## Success / Failure

- **Success**: No output, exit code 0. Backup file created in same directory.
- **Failure**: Error message from `cp` (exit code non-zero, e.g. file not found)

## Verify Backup

To confirm the backup was created:
```bash
ls -la <FILE_PATH>.bak.*
```
