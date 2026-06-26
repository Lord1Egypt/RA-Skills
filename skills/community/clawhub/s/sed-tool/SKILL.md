---
name: sed-tool
description: Stream editor for filtering and transforming text using scripts. Use for find-and-replace, text manipulation, and batch file editing.
---

# Stream Editor

Perform basic text transformations on input streams using scripting commands. Supports find-and-replace, deletion, insertion, and conditional operations.

## Usage

```bash
sed-tool [options] <script> [file...]
```

## Common Commands

- `s/old/new/`: Substitute text
- `/pattern/d`: Delete matching lines
- `Np`: Print line N
- `-i`: Edit files in-place

## Examples

```bash
# Find and replace
sed-tool 's/foo/bar/g' file.txt

# Edit in-place
sed-tool -i 's/old/new/g' config.ini

# Delete lines matching pattern
sed-tool '/debug/d' log.txt
```