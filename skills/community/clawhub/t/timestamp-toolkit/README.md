# Timestamp Toolkit

时间戳转换工具，支持多种格式互转。

## 功能

- ✅ **当前时间** - 获取当前时间戳（秒/毫秒）
- ✅ **时间戳转日期** - Unix timestamp → 可读日期
- ✅ **日期转时间戳** - 日期字符串 → Unix timestamp
- ✅ **格式化** - 自定义日期格式输出
- ✅ **时间差** - 计算两个时间之间的差值

## 测试

```bash
# 当前时间
python3 scripts/timestamp.py now

# 时间戳转日期
python3 scripts/timestamp.py to-datetime --input 1700000000

# 日期转时间戳
python3 scripts/timestamp.py to-timestamp --input "2024-03-22 14:00:00"

# 格式化
python3 scripts/timestamp.py format --input "2024-03-22" --format "%Y年%m月%d日"

# 时间差
python3 scripts/timestamp.py diff --input "2024-01-01" --input2 "2024-03-22"
```

## 状态

✅ 开发完成，测试通过
