---
name: timestamp-tool
description: Convert between Unix timestamps and human-readable dates. Use for time conversion, log analysis, and date arithmetic.
---
# Timestamp - Time Conversion Utility

Convert Unix epoch timestamps to human-readable date/time formats and vice versa. Supports multiple timezones and common date formats for log processing.

## Usage
```bash
timestamp-tool [options] <value>
```

## Options

- `-u`: Output as Unix timestamp
- `-f FORMAT`: Custom output format
- `-z TIMEZONE`: Convert to timezone

## Examples

```bash
timestamp-tool 1714896000
timestamp-tool -u "2026-05-05 12:00:00"
timestamp-tool -z Asia/Shanghai now
```