---
name: top-tool
description: Display real-time view of running processes. Use for system monitoring, performance debugging, and resource management.
---
# Top - Process Activity Monitor

Show real-time listing of running processes sorted by CPU or memory usage. Essential for identifying resource-intensive processes and system performance issues.

## Usage
```bash
top-tool [options]
```

## Options

- `-d N`: Update interval in seconds
- `-u user`: Show only processes for a user
- `-b`: Batch mode for logging
- `-o FIELD`: Sort by specific field

## Examples

```bash
top-tool
top-tool -u root
top-tool -b -n 1
```