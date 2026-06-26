# Time Converter

Convert time between different timezones.

## Description

A simple command-line tool to convert time from one timezone to another. Supports various time formats and displays the converted time with timezone offsets.

## Installation

```bash
chmod +x convert_time
```

## Usage

```bash
convert_time --from <source_timezone> --to <target_timezone> --time <time> [--date <date>]
```

### Arguments

- `--from`: Source timezone (e.g., `America/New_York`, `Asia/Shanghai`, `Europe/London`)
- `--to`: Target timezone (e.g., `Asia/Tokyo`, `UTC`, `America/Los_Angeles`)
- `--time`: Time to convert (formats: `HH:MM`, `HH:MM:SS`, `HH:MM AM/PM`)
- `--date`: Optional date for conversion (format: `YYYY-MM-DD`, default: today)

## Examples

### Basic conversion
```bash
convert_time --from "America/New_York" --to "Asia/Shanghai" --time "10:00"
```
Output:
```
2024-03-20 10:00:00 America/New_York
  =
2024-03-20 23:00:00 Asia/Shanghai

Offset: -04:00 → +08:00
```

### With specific date
```bash
convert_time --from "Europe/London" --to "UTC" --time "14:30" --date "2024-12-25"
```

### Using 12-hour format
```bash
convert_time --from "Asia/Tokyo" --to "America/Los_Angeles" --time "9:00 PM"
```

## Common Timezones

- `UTC` - Coordinated Universal Time
- `America/New_York` - Eastern Time (US)
- `America/Los_Angeles` - Pacific Time (US)
- `America/Chicago` - Central Time (US)
- `Europe/London` - London Time
- `Europe/Paris` - Central European Time
- `Asia/Shanghai` - China Standard Time
- `Asia/Tokyo` - Japan Standard Time
- `Asia/Singapore` - Singapore Time
- `Australia/Sydney` - Australian Eastern Time

## Notes

- Uses Python's `zoneinfo` module (Python 3.9+)
- Automatically handles daylight saving time transitions
- Timezone names follow the IANA timezone database format
