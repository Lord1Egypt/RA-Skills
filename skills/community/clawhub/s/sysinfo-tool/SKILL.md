---
name: sysinfo-tool
description: Display comprehensive system hardware and software information. Use for diagnostics, inventory, and system profiling.
---
# Sysinfo - System Information Reporter

Gather and display detailed system information including CPU model and cores, memory capacity, disk layout, OS version, kernel, uptime, and network configuration. Useful for system documentation and troubleshooting.

## Usage
```bash
sysinfo-tool [options]
```

## Options

- `--cpu`: Show CPU details only
- `--memory`: Show memory details only
- `--disk`: Show disk information
- `--os`: Show OS information

## Examples

```bash
sysinfo-tool
sysinfo-tool --cpu --memory
sysinfo-tool --disk
```