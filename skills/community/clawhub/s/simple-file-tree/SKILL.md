---
name: file-tree
version: 1.0.0
description: >-
  Show the directory tree structure of a folder. Displays files and subdirectories
  in a visual tree format. Use when the user wants to see what files are in a folder.
allowed-tools: Bash(find:*)
metadata: >-
  {"openclaw":{"emoji":"🌳","requires":{"bins":["find","sort","sed"],"env":[]},"install":[]}}
---

# File Tree

Show the directory tree structure of any folder with a single command.

## Usage

```bash
find <DIR_PATH> -maxdepth 3 | sort | sed 's|[^/]*/|  |g'
```

**Arguments:**
| # | Name | Description |
|---|------|-------------|
| 1 | DIR_PATH | Path to the directory to display |

## Example

```bash
find /home/user/project -maxdepth 3 | sort | sed 's|[^/]*/|  |g'
```

**Output:**
```
  project
    src
      main.py
      utils.py
    README.md
```

## Success / Failure

- **Success**: Indented file listing printed to stdout (exit code 0)
- **Failure**: Error message (exit code non-zero, e.g. directory not found)
