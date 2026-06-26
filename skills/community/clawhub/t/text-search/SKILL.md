---
name: text-search
version: 1.0.0
description: >-
  Search for a text pattern in files within a directory. Shows matching lines
  with filenames and line numbers. Use when the user wants to find where a
  word or phrase appears in their files.
allowed-tools: Bash(grep:*)
metadata: >-
  {"openclaw":{"emoji":"🔍","requires":{"bins":["grep"],"env":[]},"install":[]}}
---

# Text Search

Find a word or phrase in files within a directory with a single command.

## Usage

```bash
grep -rn <PATTERN> <DIR_PATH>
```

**Arguments:**
| # | Name | Description |
|---|------|-------------|
| 1 | PATTERN | Text or pattern to search for |
| 2 | DIR_PATH | Directory to search in |

## Example

```bash
grep -rn "TODO" /home/user/project
```

**Output:**
```
/home/user/project/main.py:12:# TODO: fix this
/home/user/project/utils.py:5:# TODO: add tests
```

Format: `FILENAME:LINE_NUMBER:MATCHING_LINE`

## Success / Failure

- **Success**: Matching lines printed (exit code 0)
- **No matches**: No output (exit code 1 — this is normal, not an error)
- **Failure**: Error message (exit code 2, e.g. directory not found)
