---
name: timestamp-toolkit
description: Timestamp conversion tool. Convert between Unix timestamp, datetime, and various date formats.
metadata: { "openclaw": { "emoji": "🕐", "requires": { "bins": ["python3"] } } }
---

# Timestamp Toolkit

A simple timestamp conversion and formatting tool.

## Features

- **Timestamp to DateTime** - Convert Unix timestamp to readable datetime
- **DateTime to Timestamp** - Convert datetime string to Unix timestamp
- **Format Conversion** - Convert between various date formats
- **Current Time** - Get current timestamp in multiple formats
- **Relative Time** - Calculate time differences

## Usage

```bash
python3 skills/timestamp-toolkit/scripts/timestamp.py <action> [options]
```

## Actions

| Action | Description |
|--------|-------------|
| `now` | Get current timestamp |
| `to-datetime` | Convert timestamp to datetime |
| `to-timestamp` | Convert datetime to timestamp |
| `format` | Format datetime string |
| `diff` | Calculate time difference |

## Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--input` | string | - | Input timestamp or datetime |
| `--format` | string | %Y-%m-%d %H:%M:%S | Output format |
| `--tz` | string | local | Timezone (local, utc, or timezone name) |
| `--unit` | string | s | Timestamp unit (s=seconds, ms=milliseconds) |

## Examples

```bash
# Get current timestamp
python3 skills/timestamp-toolkit/scripts/timestamp.py now

# Convert timestamp to datetime
python3 skills/timestamp-toolkit/scripts/timestamp.py to-datetime --input 1700000000

# Convert datetime to timestamp
python3 skills/timestamp-toolkit/scripts/timestamp.py to-timestamp --input "2024-03-22 14:00:00"

# Format datetime
python3 skills/timestamp-toolkit/scripts/timestamp.py format --input "2024-03-22" --format "%Y年%m月%d日"

# Calculate time difference
python3 skills/timestamp-toolkit/scripts/timestamp.py diff --input "2024-01-01" --input2 "2024-03-22"
```

## Supported Formats

| Format | Example |
|--------|---------|
| ISO 8601 | 2024-03-22T14:00:00Z |
| Standard | 2024-03-22 14:00:00 |
| Chinese | 2024年3月22日 14:00:00 |
| Custom | Any Python strftime format |

## Use Cases

1. **Log Analysis** - Convert timestamps in logs to readable format
2. **API Development** - Handle timestamp conversions
3. **Data Processing** - Normalize time formats
4. **Debugging** - Quick timestamp conversions

## Current Status

In development.
