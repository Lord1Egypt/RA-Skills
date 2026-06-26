---
name: time-converter
description: Convert time between different timezones using IANA timezone database. Supports 12/24-hour formats, specific dates, and automatic DST handling.
version: v1.0.0
tags: timezone-conversion, time-management, developer-tools, world-clock
---
# time-converter

Convert time between different timezones.


## Usage Scenarios

### Scenario 1: Cross-Timezone Meeting Time
**User input:** "纽约上午10点对应北京时间几点？"

**Expected output:** 2026-06-19 10:00 America/New_York = 2026-06-19 22:00 Asia/Shanghai. Offset: -04:00 (EDT) → +08:00 (CST). Difference: 12 hours ahead.

### Scenario 2: Convert to UTC
**User input:** "伦敦下午2点半转成UTC时间。"

**Expected output:** 2026-06-19 14:30 Europe/London = 2026-06-19 13:30 UTC (BST active, UTC+1). Offset: +01:00 → +00:00.

### Scenario 3: International Call Planning
**User input:** "东京晚上9点换算到洛杉矶时间。"

**Expected output:** 2026-06-19 21:00 Asia/Tokyo (JST) = 2026-06-19 05:00 America/Los_Angeles (PDT). Note: this is 5:00 AM same day in Los Angeles. Difference: 16 hours behind.
### Scenario 4: 国内外团队会议时间配对
**User input:** "我上海的，美国那边同事在纽约，我们想每周开一次远程会议，对方说周三上午10点（EST），那是北京时间几点？"
**Expected output:** 进行时区转换：纽约EST（冬令时UTC-5）→北京时间（UTC+8）时差13小时，EST周三上午10点即北京时间周三晚上23点。如果在美国夏令时（EDT，UTC-4），时差12小时，即周三晚上22点。自动识别当前是否夏令时。建议双方各让一步，选在双方都方便的折中时间（如北京时间上午9点=EST前一天晚8点/EDT晚9点）。

## Description

A simple command-line tool to convert time from one timezone to another. Supports various time formats and displays the converted time with timezone offsets.

## Installation

```bash
chmod +x ~/.openclaw/skills/time-converter/convert_time
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
