---
name: time-tool
description: Measure execution time of commands. Use for performance benchmarking, script optimization, and timing analysis.
---
# Time - Command Execution Timer

Measure how long a command takes to execute. Displays real time, CPU time, and system time for performance analysis and benchmarking.

## Usage
```bash
time-tool <command> [args...]
```

## Output

- `real`: Wall clock time elapsed
- `user`: CPU time in user mode
- `sys`: CPU time in kernel mode

## Examples

```bash
time-tool sleep 2
time-tool curl https://example.com
time-tool python3 script.py
```