---
name: tac-tool
description: Concatenate and display files in reverse line order (last line first). Use for viewing log files from newest entries and reversing file content.
---
# Tac - Reverse File Concatenation

Display file contents with lines in reverse order. The last line appears first, making it useful for viewing recent log entries and processing data in reverse.

## Usage
```bash
tac-tool [options] <file...>
```

## Examples

```bash
tac-tool log.txt
tac-tool file1.txt file2.txt > reversed_combined.txt
```