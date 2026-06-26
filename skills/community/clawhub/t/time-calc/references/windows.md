# Windows (PowerShell) 命令参考

## 目录
- 1. today -- 获取当前日期时间
- 2. info -- 日期元信息查询
- 3. weekday -- 相对星期查找
- 4. offset -- 日期/时间加减
- 5. diff -- 日期/时间差值
- 6. convert -- 时区转换（含 IANA→Windows ID 映射）
- 7. epoch -- Unix 时间戳互转

Windows 使用 PowerShell 的 `Get-Date` cmdlet 和 `[datetime]` 类型进行日期时间计算。

核心工具：
- `Get-Date` 获取和格式化日期时间
- `[datetime]` .NET 日期类型，支持算术运算
- `[DateTimeOffset]` 支持时区的日期类型
- `[TimeZoneInfo]` 时区转换

## 1. today -- 获取当前日期时间

```powershell
# 当前日期 + 星期
Get-Date -Format "yyyy-MM-dd dddd"
# 输出: 2026-04-09 Thursday

# 当前日期时间 + 时区
Get-Date -Format "yyyy-MM-dd HH:mm K"
# 输出: 2026-04-09 14:30 +08:00

# 当前 ISO 周数
$d = Get-Date; "$($d.ToString('yyyy'))-W$(Get-Date -UFormat '%V')"
# 输出: 2026-W15
```

## 2. info -- 日期元信息查询

```powershell
# 指定日期的星期
([datetime]"2026-06-15").DayOfWeek
# 输出: Monday

# 指定日期的 ISO 周数（需要用 .NET 方法）
$d = [datetime]"2026-06-15"
$cal = [System.Globalization.CultureInfo]::InvariantCulture.Calendar
$week = $cal.GetWeekOfYear($d, [System.Globalization.CalendarWeekRule]::FirstFourDayWeek, [DayOfWeek]::Monday)
"$($d.Year)-W$($week.ToString('D2'))"
# 输出: 2026-W25

# 指定日期是年内第几天
([datetime]"2026-12-31").DayOfYear
# 输出: 365
```

**月天数和闰年判断：**

```powershell
# 某月有多少天
[datetime]::DaysInMonth(2026, 2)
# 输出: 28

# 闰年判断
[datetime]::IsLeapYear(2024)
# 输出: True

[datetime]::IsLeapYear(2025)
# 输出: False
```

## 3. weekday -- 相对星期查找

PowerShell 没有内置的 this/next/last weekday 语法，通过计算 ISO 周的周一偏移来实现：

```powershell
# 辅助函数：获取当前 ISO 周的周一
function Get-ISOMonday {
  $today = Get-Date
  # PowerShell DayOfWeek: Sunday=0, Monday=1, ..., Saturday=6
  # ISO 周: Monday=1, ..., Sunday=7
  $isoDow = if ($today.DayOfWeek -eq [DayOfWeek]::Sunday) { 7 } else { [int]$today.DayOfWeek }
  $today.AddDays(1 - $isoDow).Date
}

# 本周三（当前 ISO 周的周三）
$monday = Get-ISOMonday
$monday.AddDays(2).ToString("yyyy-MM-dd dddd")

# 下周五（下一个 ISO 周的周五）
$monday = Get-ISOMonday
$monday.AddDays(7 + 4).ToString("yyyy-MM-dd dddd")
# 下周一 = $monday + 7，下周五 = 下周一 + 4

# 上周一（上一个 ISO 周的周一）
$monday = Get-ISOMonday
$monday.AddDays(-7).ToString("yyyy-MM-dd dddd")
```

通用公式：目标日期 = ISO 周一 + (周偏移 * 7) + (目标星期几 - 1)
- 目标星期几：Monday=0, Tuesday=1, ..., Sunday=6
- 周偏移：this=0, next=1, last=-1

## 4. offset -- 日期/时间加减

```powershell
# 当前日期 +3天
(Get-Date).AddDays(3).ToString("yyyy-MM-dd")
# 输出: 2026-04-12

# 当前日期 -2周
(Get-Date).AddDays(-14).ToString("yyyy-MM-dd")
# 输出: 2026-03-26

# 当前日期 +1月
(Get-Date).AddMonths(1).ToString("yyyy-MM-dd")
# 输出: 2026-05-09

# 指定日期 +1月（含月末截断）
([datetime]"2026-01-31").AddMonths(1).ToString("yyyy-MM-dd")
# 输出: 2026-02-28 (.NET 自动回退到月末)

# 指定日期 +1年（闰年边界）
([datetime]"2024-02-29").AddYears(1).ToString("yyyy-MM-dd")
# 输出: 2025-02-28 (.NET 自动回退)

# 指定时间 +5小时（跨日）
([datetime]"2026-04-09 22:00").AddHours(5).ToString("yyyy-MM-ddTHH:mm")
# 输出: 2026-04-10T03:00

# 指定时间 +45分钟
([datetime]"2026-04-09 14:30").AddMinutes(45).ToString("HH:mm")
# 输出: 15:15

# 组合调整：+1月 +2天 +3小时
([datetime]"2026-04-09").AddMonths(1).AddDays(2).AddHours(3).ToString("yyyy-MM-dd HH:mm")
```

**PowerShell 的月份加减行为与 macOS (BSD) 一致**：1月31日 +1月 = 2月28日（自动回退到月末），与 GNU date 的溢出行为不同。

## 5. diff -- 日期/时间差值

```powershell
# 两个日期的天数差
([datetime]"2026-04-15" - [datetime]"2026-04-09").Days
# 输出: 6

# 跨年日期差
([datetime]"2026-01-03" - [datetime]"2025-12-25").Days
# 输出: 9

# datetime 差值（含时分）
$span = [datetime]"2026-04-11 17:30" - [datetime]"2026-04-09 08:00"
"$($span.Days)天$($span.Hours)小时$($span.Minutes)分钟"
# 输出: 2天9小时30分钟
```

PowerShell 的 `TimeSpan` 对象自带 `.Days`, `.Hours`, `.Minutes` 属性，无需手动换算。

## 6. convert -- 时区转换

```powershell
# 北京时间 15:00 转纽约时间
# 使用 GetUtcOffset 获取指定日期的实际偏移量（含夏令时）
$shanghaiTz = [TimeZoneInfo]::FindSystemTimeZoneById("China Standard Time")
$nyTz = [TimeZoneInfo]::FindSystemTimeZoneById("Eastern Standard Time")
$dt = [datetime]::new(2026,4,9,15,0,0)
$shanghaiOffset = $shanghaiTz.GetUtcOffset($dt)
$shanghaiTime = [DateTimeOffset]::new($dt, $shanghaiOffset)
$nyTime = [TimeZoneInfo]::ConvertTime($shanghaiTime, $nyTz)
$nyTime.ToString("yyyy-MM-dd HH:mm zzz")
# 输出: 2026-04-09 03:00 -04:00

# UTC 转北京时间
$utcTime = [DateTimeOffset]::new(2026,4,9,12,0,0, [TimeSpan]::Zero)
$shanghaiTime = [TimeZoneInfo]::ConvertTime($utcTime, $shanghaiTz)
$shanghaiTime.ToString("yyyy-MM-dd HH:mm zzz")
# 输出: 2026-04-09 20:00 +08:00

# 东京时间转纽约时间（可能跨日）
$tokyoTz = [TimeZoneInfo]::FindSystemTimeZoneById("Tokyo Standard Time")
$dt2 = [datetime]::new(2026,4,9,2,0,0)
$tokyoOffset = $tokyoTz.GetUtcOffset($dt2)
$tokyoTime = [DateTimeOffset]::new($dt2, $tokyoOffset)
$nyTime = [TimeZoneInfo]::ConvertTime($tokyoTime, $nyTz)
$nyTime.ToString("yyyy-MM-dd HH:mm zzz")
# 输出: 2026-04-08 13:00 -04:00
```

注意：使用 `GetUtcOffset($datetime)` 获取指定日期的实际 UTC 偏移量，它会自动处理夏令时。不要用 `BaseUtcOffset`，那只返回标准时间偏移，不含夏令时调整。

**IANA 时区名到 Windows 时区 ID 的转换：**

SKILL.md 中使用 IANA 时区名（如 Asia/Shanghai），但 PowerShell 需要 Windows 时区 ID。

常用映射表：
| IANA | Windows ID |
|------|------------|
| Asia/Shanghai | China Standard Time |
| Asia/Tokyo | Tokyo Standard Time |
| America/New_York | Eastern Standard Time |
| America/Los_Angeles | Pacific Standard Time |
| America/Chicago | Central Standard Time |
| Europe/London | GMT Standard Time |
| Europe/Paris | Romance Standard Time |
| Europe/Berlin | W. Europe Standard Time |
| Australia/Sydney | AUS Eastern Standard Time |
| UTC | UTC |

如果需要查找不在上表中的时区，用以下命令搜索：

```powershell
# 按关键词搜索 Windows 时区 ID
[TimeZoneInfo]::GetSystemTimeZones() | Where-Object { $_.Id -match "Tokyo" -or $_.DisplayName -match "Tokyo" } | Select-Object Id, DisplayName
```

## 7. epoch -- Unix 时间戳互转

```powershell
# 时间戳 → 可读时间 (UTC)
[DateTimeOffset]::FromUnixTimeSeconds(1775701378).UtcDateTime.ToString("yyyy-MM-dd HH:mm:ss 'UTC'")
# 输出: 2026-04-09 02:22:58 UTC

# 时间戳 → 可读时间 (本地时区)
[DateTimeOffset]::FromUnixTimeSeconds(1775701378).LocalDateTime.ToString("yyyy-MM-dd HH:mm:ss")
# 输出: 2026-04-09 10:22:58 (取决于本地时区)

# 毫秒时间戳
[DateTimeOffset]::FromUnixTimeMilliseconds(1775701378000).UtcDateTime.ToString("yyyy-MM-dd HH:mm:ss 'UTC'")

# 可读时间 → 时间戳
[DateTimeOffset]::new([datetime]"2026-04-09 12:00:00").ToUnixTimeSeconds()
# 输出: epoch 值（本地时区解释）

# 指定 UTC 时间 → 时间戳
[DateTimeOffset]::new(2026,4,9,12,0,0,[TimeSpan]::Zero).ToUnixTimeSeconds()

# 当前时间戳
[DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
```
