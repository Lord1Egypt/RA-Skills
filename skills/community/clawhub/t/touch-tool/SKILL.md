---
name: touch-tool
description: Create empty files or update file timestamps. Use for file creation, timestamp management, and build system operations.
---
# Touch - File Timestamp Manager

Create empty files or update the access and modification timestamps of existing files. If the file doesn't exist, it is created empty.

## Usage
```bash
touch-tool [options] <file...>
```

## Options

- `-a`: Change access time only
- `-m`: Change modification time only
- `-t STAMP`: Use specified time instead of current time
- `-c`: Don't create file if it doesn't exist

## Examples

```bash
touch-tool newfile.txt
touch-tool -a oldfile.log
touch-tool -t 202605011200 file.txt
```