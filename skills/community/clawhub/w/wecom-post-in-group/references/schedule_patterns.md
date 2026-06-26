# Schedule Patterns Reference

This document provides the complete mapping from natural language schedule descriptions to automation RRULE configurations and date guard logic.

## RRULE Limitations

The automation system only supports two RRULE frequencies:
- `FREQ=HOURLY` with `INTERVAL=N` (every N hours)
- `FREQ=WEEKLY` with `BYDAY`, `BYHOUR`, `BYMINUTE`

For monthly or more complex schedules, combine a frequent RRULE trigger with a **date guard** in the automation prompt that checks the current date and skips execution if conditions aren't met.

---

## Daily Schedules

| User Input | RRULE | Date Guard |
|------------|-------|------------|
| 每天 / 每日 / daily | `FREQ=HOURLY;INTERVAL=24` | None |
| 每天上午10点 | `FREQ=HOURLY;INTERVAL=24` | None (RRULE handles time) |
| 每个工作日 / weekdays | `FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR;BYHOUR=10;BYMINUTE=0` | None |

---

## Weekly Schedules

| User Input | RRULE | Date Guard |
|------------|-------|------------|
| 每周一 / every Monday | `FREQ=WEEKLY;BYDAY=MO;BYHOUR=10;BYMINUTE=0` | None |
| 每周五下午3点 | `FREQ=WEEKLY;BYDAY=FR;BYHOUR=15;BYMINUTE=0` | None |
| 每周一三五 | `FREQ=WEEKLY;BYDAY=MO,WE,FR;BYHOUR=10;BYMINUTE=0` | None |
| 每两周一次（周一） | `FREQ=WEEKLY;BYDAY=MO;BYHOUR=10;BYMINUTE=0` | Check if ISO week number is odd/even |

### Day Mapping

| Chinese | English | RRULE |
|---------|---------|-------|
| 周一 / 星期一 | Monday | MO |
| 周二 / 星期二 | Tuesday | TU |
| 周三 / 星期三 | Wednesday | WE |
| 周四 / 星期四 | Thursday | TH |
| 周五 / 星期五 | Friday | FR |
| 周六 / 星期六 | Saturday | SA |
| 周日 / 星期日 | Sunday | SU |

---

## Monthly Schedules (Fixed Date)

For fixed-date monthly schedules, use a daily RRULE with a date guard.

| User Input | RRULE | Date Guard |
|------------|-------|------------|
| 每月1日 / 每月1号 | `FREQ=HOURLY;INTERVAL=24` | `day == 1` |
| 每月15号 | `FREQ=HOURLY;INTERVAL=24` | `day == 15` |
| 每月27日 | `FREQ=HOURLY;INTERVAL=24` | `day == 27` |
| 每月最后一天 | `FREQ=HOURLY;INTERVAL=24` | `day == last_day_of_month` |

**Date guard prompt template (fixed date):**

```
首先检查今天的日期，如果今天不是每月的 {N} 日，则直接结束，不执行任何操作，不输出任何内容。

如果今天是每月的 {N} 日，则执行以下步骤：
```

**Date guard prompt template (last day of month):**

```
首先检查今天是否为本月的最后一天（即明天的月份与今天不同）。如果不是最后一天，则直接结束，不执行任何操作。

如果今天是本月最后一天，则执行以下步骤：
```

---

## Monthly Schedules (Pattern-Based)

For pattern-based monthly schedules, use a weekly RRULE filtered to the target weekday, combined with a date guard for the week position.

### Last [Weekday] of Month

| User Input | RRULE | Date Guard |
|------------|-------|------------|
| 每月最后一个周一 / 每月最后一周的周一 | `FREQ=WEEKLY;BYDAY=MO;BYHOUR=10;BYMINUTE=0` | `day + 7 > last_day_of_month` |
| 每月最后一个周五 | `FREQ=WEEKLY;BYDAY=FR;BYHOUR=10;BYMINUTE=0` | `day + 7 > last_day_of_month` |

**Date guard prompt template (last weekday):**

```
首先检查今天的日期。计算本月的总天数，如果今天的日期加上 7 仍然不超过本月总天数（即今天不在本月的最后一周），则直接结束，不执行任何操作。

如果今天在本月最后一周内，则执行以下步骤：
```

### First [Weekday] of Month

| User Input | RRULE | Date Guard |
|------------|-------|------------|
| 每月第一个周一 | `FREQ=WEEKLY;BYDAY=MO;BYHOUR=10;BYMINUTE=0` | `day <= 7` |
| 每月第一个周五 | `FREQ=WEEKLY;BYDAY=FR;BYHOUR=10;BYMINUTE=0` | `day <= 7` |

**Date guard prompt template (first weekday):**

```
首先检查今天的日期，如果今天的日期大于 7（即不在本月第一周），则直接结束，不执行任何操作。

如果今天的日期在 1-7 号之间，则执行以下步骤：
```

### Second / Third [Weekday] of Month

| User Input | RRULE | Date Guard |
|------------|-------|------------|
| 每月第二个周一 | `FREQ=WEEKLY;BYDAY=MO;BYHOUR=10;BYMINUTE=0` | `8 <= day <= 14` |
| 每月第三个周五 | `FREQ=WEEKLY;BYDAY=FR;BYHOUR=10;BYMINUTE=0` | `15 <= day <= 21` |
| 每月第四个周一 | `FREQ=WEEKLY;BYDAY=MO;BYHOUR=10;BYMINUTE=0` | `22 <= day <= 28` |

**Date guard prompt template (Nth weekday):**

```
首先检查今天的日期，如果今天的日期不在 {START}-{END} 号之间，则直接结束，不执行任何操作。

如果今天的日期在 {START}-{END} 号之间，则执行以下步骤：
```

Where:
- 1st: START=1, END=7
- 2nd: START=8, END=14
- 3rd: START=15, END=21
- 4th: START=22, END=28

---

## Default Push Time

When the user doesn't specify a time, default to **10:00 AM** (local time).

## Schedule Description for User Confirmation

Always generate a human-readable description for the user. Examples:

| Configuration | Description |
|---------------|-------------|
| Daily at 10:00 | 每天上午 10:00 |
| Weekly Mon at 10:00 | 每周一上午 10:00 |
| Monthly 27th at 10:00 | 每月 27 日上午 10:00 |
| Last Mon of month at 10:00 | 每月最后一个周一上午 10:00 |
| First Fri of month at 15:00 | 每月第一个周五下午 3:00 |
