# macOS (BSD date) 命令参考

## 目录
- 1. today -- 获取当前日期时间
- 2. info -- 日期元信息查询
- 3. weekday -- 相对星期查找
- 4. offset -- 日期/时间加减（含安全方案）
- 5. diff -- 日期/时间差值
- 6. convert -- 时区转换
- 7. epoch -- Unix 时间戳互转

macOS 使用 BSD 版本的 `date` 命令。核心标志：
- `-v` 日期调整（可叠加多个）
- `-j` 不设置系统时间（解析时必加）
- `-f` 指定输入格式
- `-r` 从 epoch 转换

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
date -j -f "%Y-%m-%d" "2026-06-15" "+%A"
# 输出: Monday

# 指定日期的 ISO 周数
date -j -f "%Y-%m-%d" "2026-06-15" "+%G-W%V"
# 输出: 2026-W25

# 指定日期是年内第几天
date -j -f "%Y-%m-%d" "2026-12-31" "+%j"
# 输出: 365
```

**月天数和闰年判断** -- BSD date 无直接命令，通过计算获取：

```bash
# 某月有多少天（取下月1号再减1天）
date -j -v-1d -f "%Y-%m-%d" "2026-03-01" "+%d"
# 输出: 28 (2026年2月有28天)

# 闰年判断：检查该年2月是否有29天
date -j -v-1d -f "%Y-%m-%d" "2024-03-01" "+%d"
# 输出: 29 (2024是闰年)

date -j -v-1d -f "%Y-%m-%d" "2025-03-01" "+%d"
# 输出: 28 (2025非闰年)
```

## 3. weekday -- 相对星期查找

BSD date 的 `-v +day` 和 `-v -day` 语义是"下一个/上一个出现的该星期几"，与 ISO 周定义不同。要实现 ISO 周语义（本周/下周/上周），使用 `-v <day>` 配合 `-v +Nw`：

```bash
# 本周三（当前 ISO 周内的周三）
date -v wed "+%Y-%m-%d %A"
# 输出: 本周三的日期（可能在今天之前）

# 下周五（下一个 ISO 周的周五）
date -v +1w -v fri "+%Y-%m-%d %A"
# 先跳到下周同一天，再设为周五

# 上周一（上一个 ISO 周的周一）
date -v -1w -v mon "+%Y-%m-%d %A"
# 先跳到上周同一天，再设为周一
```

注意：
- `-v wed` 设置为当前周的周三（ISO 周语义，正确）
- `-v +1w -v fri` 先前进一周再设为周五 = 下一个 ISO 周的周五（正确）
- 不要用 `-v +fri`，它的语义是"最近的下一个周五"，在今天是周四时会返回明天（本周五）而不是下周五

## 4. offset -- 日期/时间加减

```bash
# 当前日期 +3天
date -v +3d "+%Y-%m-%d"
# 输出: 2026-04-12

# 当前日期 -2周
date -v -2w "+%Y-%m-%d"
# 输出: 2026-03-26

# 当前日期 +1月
date -v +1m "+%Y-%m-%d"
# 输出: 2026-05-09

# 指定日期 +1月（含月末截断）
date -j -v+1m -f "%Y-%m-%d" "2026-01-31" "+%Y-%m-%d"
# 输出: 2026-02-28 (BSD date 自动回退到月末)

# 指定日期 +1年（闰年边界）-- 原生命令会溢出
date -j -v+1y -f "%Y-%m-%d" "2024-02-29" "+%Y-%m-%d"
# 输出: 2025-03-01 (溢出! 不是期望的 2025-02-28)

# 安全的年份加减（处理闰年边界溢出）
base="2024-02-29"
base_month=$(date -j -f "%Y-%m-%d" "$base" "+%m")
result=$(date -j -v+1y -f "%Y-%m-%d" "$base" "+%Y-%m-%d")
result_month=$(date -j -f "%Y-%m-%d" "$result" "+%m")
if [ "$result_month" != "$base_month" ]; then
  # 发生了溢出（月份变了），回退到目标月的最后一天
  result_year=$(date -j -f "%Y-%m-%d" "$result" "+%Y")
  result=$(date -j -v+1m -v-1d -f "%Y-%m-%d" "$result_year-$base_month-01" "+%Y-%m-%d")
fi
echo "$result"
# 输出: 2025-02-28

# 指定时间 +5小时（跨日）
date -j -v+5H -f "%Y-%m-%dT%H:%M" "2026-04-09T22:00" "+%Y-%m-%dT%H:%M"
# 输出: 2026-04-10T03:00

# 指定时间 +45分钟
date -j -v+45M -f "%H:%M" "14:30" "+%H:%M"
# 输出: 15:15

# 叠加多个调整：+1月 +2天 +3小时
date -j -v+1m -v+2d -v+3H -f "%Y-%m-%d" "2026-04-09" "+%Y-%m-%d %H:%M"
```

## 5. diff -- 日期/时间差值

BSD date 没有直接的 diff 命令，通过 epoch 秒数相减计算：

```bash
# 两个日期的天数差
d1=$(date -j -f "%Y-%m-%d" "2026-04-09" "+%s")
d2=$(date -j -f "%Y-%m-%d" "2026-04-15" "+%s")
echo $(( (d2 - d1) / 86400 ))
# 输出: 6

# 跨年日期差
d1=$(date -j -f "%Y-%m-%d" "2025-12-25" "+%s")
d2=$(date -j -f "%Y-%m-%d" "2026-01-03" "+%s")
echo $(( (d2 - d1) / 86400 ))
# 输出: 9

# datetime 差值（含时分）
t1=$(date -j -f "%Y-%m-%dT%H:%M" "2026-04-09T08:00" "+%s")
t2=$(date -j -f "%Y-%m-%dT%H:%M" "2026-04-11T17:30" "+%s")
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
# 方法：在源时区环境下解析为 epoch，再在目标时区环境下输出
epoch=$(TZ=Asia/Shanghai date -j -f "%Y-%m-%dT%H:%M" "2026-04-09T15:00" "+%s")
TZ=America/New_York date -r "$epoch" "+%Y-%m-%d %H:%M %Z"
# 输出: 2026-04-09 03:00 EDT

# UTC 转北京时间
epoch=$(TZ=UTC date -j -f "%Y-%m-%dT%H:%M" "2026-04-09T12:00" "+%s")
TZ=Asia/Shanghai date -r "$epoch" "+%Y-%m-%d %H:%M %Z"
# 输出: 2026-04-09 20:00 CST

# 东京时间转纽约时间（可能跨日）
epoch=$(TZ=Asia/Tokyo date -j -f "%Y-%m-%dT%H:%M" "2026-04-09T02:00" "+%s")
TZ=America/New_York date -r "$epoch" "+%Y-%m-%d %H:%M %Z"
# 输出: 2026-04-08 13:00 EDT
```

## 7. epoch -- Unix 时间戳互转

```bash
# 时间戳 → 可读时间 (UTC)
TZ=UTC date -r 1775701378 "+%Y-%m-%d %H:%M:%S %Z"
# 输出: 2026-04-09 02:22:58 UTC

# 时间戳 → 可读时间 (本地时区)
date -r 1775701378 "+%Y-%m-%d %H:%M:%S %Z"
# 输出: 2026-04-09 10:22:58 CST (取决于本地时区)

# 毫秒时间戳 → 先除以 1000
date -r $(( 1775701378000 / 1000 )) "+%Y-%m-%d %H:%M:%S %Z"

# 可读时间 → 时间戳
date -j -f "%Y-%m-%dT%H:%M:%S" "2026-04-09T12:00:00" "+%s"
# 输出: epoch 值（本地时区解释）

# 指定时区的时间 → 时间戳
TZ=UTC date -j -f "%Y-%m-%dT%H:%M:%S" "2026-04-09T12:00:00" "+%s"

# 当前时间戳
date "+%s"
```
