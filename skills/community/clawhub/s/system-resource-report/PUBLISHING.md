# System Resource Report — Publishing Notes

## Formal Name
System Resource Report

## Slug
system-resource-report

## Version
1.0.0

## Short Description
A lightweight Linux system resource reporting skill that summarizes load average, memory, swap, root disk usage, and top CPU/memory-consuming processes.

## Long Description
System Resource Report is a lightweight operational skill for Linux hosts. It collects and summarizes current system resource usage, including load average, memory and swap usage, root disk occupancy, top CPU consumers, and top memory consumers. It is designed for quick health checks, recurring status summaries, and early detection of abnormal load or memory pressure.

This skill is intentionally simple, transparent, and low-risk. It only reads local system metrics using standard shell commands and does not modify system state.

## Suggested Tags
linux, monitoring, system, resources, devops, observability

## Category Suggestion
Operations / Monitoring

## Changelog
Initial release: report load, memory, swap, disk, top CPU and memory processes.

## Why publish this skill
This skill solves a frequent operational need: quickly understanding whether a Linux machine is healthy or under pressure. It reduces repetitive manual inspection, standardizes summary output, and is especially useful for periodic automated reporting or direct ad-hoc diagnostics.

## Risk Signals
- Low risk: read-only local inspection only.
- No destructive commands.
- No outbound network requirement for normal execution.
- No credential handling.
- Main caveat: output accuracy depends on the underlying Linux tools available on the host.

## License Statement
I have the rights to this skill and agree to publish it under MIT-0.
