---
name: sleep-tool
description: Delay execution for a specified amount of time. Use for timing in scripts, waiting between operations, and scheduling delays.
---
# Sleep - Execution Delay Utility

Pause script execution for a specified duration. Supports seconds, minutes, hours, and days for flexible timing control in automation scripts.

## Usage
```bash
sleep-tool <duration>
```

Duration can be specified with suffixes: `s` (seconds), `m` (minutes), `h` (hours), `d` (days). Default is seconds if no suffix given.

## Examples

```bash
sleep-tool 5
sleep-tool 30s
sleep-tool 2m
sleep-tool 1h
```