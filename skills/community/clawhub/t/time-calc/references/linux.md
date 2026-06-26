# Linux (GNU date) 命令参考

## 目录
- 1. today -- 获取当前日期时间
- 2. info -- 日期元信息查询
- 3. weekday -- 相对星期查找
- 4. offset -- 日期/时间加减（含安全方案）
- 5. diff -- 日期/时间差值
- 6. convert -- 时区转换
- 7. epoch -- Unix 时间戳互转

Linux 使用 GNU 版本的 `date` 命令。同样适用于 WSL 和 Git Bash (MINGW)。
核心标志：
- `-d` 解析日期字符串和进行日期运算
- `--date` 同 `-d` 的长格式

## 1. today -- 获取当前日期时间

```bash
# 当前日期 + 星期
date "+%Y-%m-%d %A"
# 输出: 2026-04-09 Wednesday

# 当前日期时间 + 时区
date "+%Y-%m-%d %H:%M %Z"
# 输出: 2026-04-09 14:30 CST

# 当前 ISO 周数
date "+%G-W%V"
# 输出: 2026-W15
```

## 2. info -- 日期元信息查询

```bash
# 指定日期的星期
date -d "2026-06-15" "+%A"
# 输出: Monday

# 指定日期的 ISO 周数
date -d "2026-06-15" "+%G-W%V"
# 输出: 2026-W25

# 指定日期是年内第几天
date -d "2026-12-31" "+%j"
# 输出: 365
```

**月天数和闰年判断：**

```bash
# 某月有多少天（取下月1号的前一天）
date -d "2026-03-01 - 1 day" "+%d"
# 输出: 28 (2026年2月有28天)

# 闰年判断
date -d "2024-03-01 - 1 day" "+%d"
# 输出: 29 (2024是闰年)

date -d "2025-03-01 - 1 day" "+%d"
# 输出: 28 (2025非闰年)
```

## 3. weekday -- 相对星期查找

GNU date 的 `next friday` 语义是"最近的下一个周五"，与 ISO 周定义不同。要实现 ISO 周语义，通过先定位到目标周再取星期几：

```bash
# 本周三（当前 ISO 周内的周三）
# 先找到本周一，再加 2 天
date -d "$(date -d 'last monday + 0 days' +%F 2>/dev/null || date -d 'monday - 7 days' +%F) + 2 days" "+%Y-%m-%d %A"

# 更简洁的方式：GNU date 的 "this wednesday" 通常返回当前周的周三
date -d "this wednesday" "+%Y-%m-%d %A"

# 下周五（下一个 ISO 周的周五）
date -d "this friday + 7 days" "+%Y-%m-%d %A"
# 取本周五再加 7 天 = 下周五

# 上周一（上一个 ISO 周的周一）
date -d "this monday - 7 days" "+%Y-%m-%d %A"
# 取本周一再减 7 天 = 上周一
```

注意：
- `date -d "this friday"` 返回当前周的周五（ISO 周语义，可靠）
- 下周/上周通过在 this 基础上 +7/-7 天来实现，避免 `next/last` 的歧义
- 不要用 `date -d "next friday"` 表示"下周五"，它的语义是"最近的下一个周五"

## 4. offset -- 日期/时间加减

```bash
# 当前日期 +3天
date -d "+3 days" "+%Y-%m-%d"
# 输出: 2026-04-12

# 当前日期 -2周
date -d "-2 weeks" "+%Y-%m-%d"
# 输出: 2026-03-26

# 当前日期 +1月
date -d "+1 month" "+%Y-%m-%d"
# 输出: 2026-05-09

# 指定日期 +1月（含月末回退）
date -d "2026-01-31 + 1 month" "+%Y-%m-%d"
# 输出: 2026-03-03 (GNU date 不回退，而是溢出！需注意)

# 指定日期 +1年（闰年边界）
date -d "2024-02-29 + 1 year" "+%Y-%m-%d"
# 输出: 2025-03-01 (GNU date 溢出到3月1日)

# 指定时间 +5小时（跨日）
date -d "2026-04-09 22:00 + 5 hours" "+%Y-%m-%dT%H:%M"
# 输出: 2026-04-10T03:00

# 指定时间 +45分钟
date -d "14:30 + 45 minutes" "+%H:%M"
# 输出: 15:15

# 组合调整：+1月 +2天 +3小时
date -d "2026-04-09 + 1 month + 2 days + 3 hours" "+%Y-%m-%d %H:%M"
```

**GNU date 月份/年份加减的重要差异：**

GNU date 在月份和年份加减时都不会回退到月末，而是溢出。必须使用以下安全方案：

```bash
# 安全的月份/年份加减（通用方案，处理所有溢出场景）
# 用法：safe_offset "2026-01-31" "1 month" 或 safe_offset "2024-02-29" "1 year"
safe_offset() {
  local base="$1" delta="$2"
  local base_month=$(date -d "$base" "+%m")
  local result=$(date -d "$base + $delta" "+%Y-%m-%d")
  local result_month=$(date -d "$result" "+%m")
  # 如果月份发生了意外变化，说明溢出了
  # 对于 +Nm 场景：期望月份 = base月 + N；对于 +Ny 场景：期望月份不变
  if [ "$result_month" != "$base_month" ]; then
    # 检查是否是月份加减导致的跨月（期望的）
    local expected_month
    if echo "$delta" | grep -q "month"; then
      local n=$(echo "$delta" | grep -oP '\d+')
      expected_month=$(printf "%02d" $(( ((10#$base_month - 1 + n) % 12) + 1 )))
    else
      expected_month="$base_month"
    fi
    if [ "$result_month" != "$expected_month" ]; then
      # 发生了溢出，回退到期望月份的最后一天
      local result_year=$(date -d "$result" "+%Y")
      result=$(date -d "$result_year-$expected_month-01 + 1 month - 1 day" "+%Y-%m-%d")
    fi
  fi
  echo "$result"
}

# 示例：
safe_offset "2026-01-31" "1 month"
# 输出: 2026-02-28 (而非 GNU date 原生的 2026-03-03)

safe_offset "2024-02-29" "1 year"
# 输出: 2025-02-28 (而非 GNU date 原生的 2025-03-01)
```

## 5. diff -- 日期/时间差值

GNU date 也没有直接的 diff 命令，通过 epoch 秒数计算：

```bash
# 两个日期的天数差
d1=$(date -d "2026-04-09" "+%s")
d2=$(date -d "2026-04-15" "+%s")
echo $(( (d2 - d1) / 86400 ))
# 输出: 6

# 跨年日期差
d1=$(date -d "2025-12-25" "+%s")
d2=$(date -d "2026-01-03" "+%s")
echo $(( (d2 - d1) / 86400 ))
# 输出: 9

# datetime 差值（含时分）
t1=$(date -d "2026-04-09 08:00" "+%s")
t2=$(date -d "2026-04-11 17:30" "+%s")
diff_sec=$(( t2 - t1 ))
days=$(( diff_sec / 86400 ))
hours=$(( (diff_sec % 86400) / 3600 ))
mins=$(( (diff_sec % 3600) / 60 ))
echo "${days}天${hours}小时${mins}分钟"
# 输出: 2天9小时30分钟
```

## 6. convert -- 时区转换

```bash
# 北京时间 15:00 转纽约时间
TZ=America/New_York date -d "TZ=\"Asia/Shanghai\" 2026-04-09 15:00" "+%Y-%m-%d %H:%M %Z"
# 输出: 2026-04-09 03:00 EDT

# UTC 转北京时间
TZ=Asia/Shanghai date -d "TZ=\"UTC\" 2026-04-09 12:00" "+%Y-%m-%d %H:%M %Z"
# 输出: 2026-04-09 20:00 CST

# 东京时间转纽约时间（可能跨日）
TZ=America/New_York date -d "TZ=\"Asia/Tokyo\" 2026-04-09 02:00" "+%Y-%m-%d %H:%M %Z"
# 输出: 2026-04-08 13:00 EDT
```

GNU date 的时区转换语法：`TZ=目标时区 date -d 'TZ="源时区" 时间'`。注意内层 TZ 需要用引号包裹。

## 7. epoch -- Unix 时间戳互转

```bash
# 时间戳 → 可读时间 (UTC)
date -u -d @1775701378 "+%Y-%m-%d %H:%M:%S %Z"
# 输出: 2026-04-09 02:22:58 UTC

# 时间戳 → 可读时间 (本地时区)
date -d @1775701378 "+%Y-%m-%d %H:%M:%S %Z"
# 输出: 2026-04-09 10:22:58 CST (取决于本地时区)

# 毫秒时间戳 → 先除以 1000
date -d @$(( 1775701378000 / 1000 )) "+%Y-%m-%d %H:%M:%S %Z"

# 可读时间 → 时间戳
date -d "2026-04-09 12:00:00" "+%s"
# 输出: epoch 值（本地时区解释）

# 指定时区的时间 → 时间戳
date -d "TZ=\"UTC\" 2026-04-09 12:00:00" "+%s"

# 当前时间戳
date "+%s"
```
