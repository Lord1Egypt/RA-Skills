---
name: ps-tool
description: Display information about active processes. Use for monitoring running programs, checking resource usage, and system diagnostics.
---
# PS - Process Status Viewer

Show snapshot of current processes with PID, CPU usage, memory consumption, and status. Essential for system monitoring and process management.

## Usage
```bash
ps-tool [options]
```

## Common Options

- `aux`: Detailed view of all processes
- `-ef`: Full-format listing
- `-u user`: Filter by user
- `--sort=-%mem`: Sort by memory usage

## Examples

```bash
ps-tool aux
ps-tool -ef
ps-tool -u root
```