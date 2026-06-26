---
name: system-info-skill
description: Query system information including OS, CPU, memory, and disk usage. Use when users ask about system configuration, resource usage, performance diagnostics, or basic system info. Supports Windows, Linux, and macOS.
---

# System Information Query

Quick system information query including OS, CPU, memory, and disk.

## Installation

Install from ClawHub:

```bash
npx clawhub install system-info-skill
```

Or install from local .skill file:

```bash
openclaw skills install system-info-skill.skill
```

## Usage

### Query All System Information

```bash
python scripts/system_info.py
```

### Query Specific Information

```bash
# CPU only
python scripts/system_info.py --cpu

# Memory only
python scripts/system_info.py --memory

# Disk only
python scripts/system_info.py --disk
```

## Example Output

```
=== System Information ===

OS: Windows 10
CPU: Intel Core i7-9700K
CPU Cores: 8
Total Memory: 16.0 GB
Memory Used: 8.5 GB (53%)
Total Disk: 512.0 GB
Disk Used: 256.0 GB (50%)
```

## Notes

- Requires Python 3.6+
- Cross-platform support
- No additional dependencies required
