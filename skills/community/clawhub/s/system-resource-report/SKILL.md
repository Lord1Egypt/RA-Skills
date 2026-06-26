---
name: system-resource-report
description: Check current Linux system resource usage and report load, memory, swap, disk, and top CPU/memory processes. Use when the user asks about system resources, resource usage, CPU/memory/disk occupancy, or wants periodic machine health/resource summaries.
---

# System Resource Report

Use this skill when the user wants current machine resource usage or recurring resource summaries.

## What to collect
Run the bundled script:

`./scripts/report.sh`

It reports:
- load average / uptime
- memory and swap usage
- root disk usage
- top CPU processes
- top memory processes

## Response style
Summarize briefly first, then list:
- load
- memory/swap
- disk
- top CPU consumers
- top memory consumers

Call out clearly if:
- free memory is low
- swap is in active use
- load is abnormally high
- one process family dominates resource usage
