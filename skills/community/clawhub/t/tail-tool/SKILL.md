---
name: tail-tool
description: Display the last lines of files. Use for monitoring log files, checking recent entries, and following file growth in real-time.
---

# File Tail Viewer

Show the end of files, defaulting to the last 10 lines. Includes follow-mode for watching files that grow in real-time.

## Usage

```bash
tail-tool [options] [file...]
```

## Options

- `-n N`: Show last N lines
- `-f`: Follow file growth (watch mode)
- `-c N`: Show last N bytes
- `-q`: Suppress filename headers

## Examples

```bash
# Show last 10 lines
tail-tool log.txt

# Show last 50 lines
tail-tool -n 50 access.log

# Follow log in real-time
tail-tool -f /var/log/syslog
```