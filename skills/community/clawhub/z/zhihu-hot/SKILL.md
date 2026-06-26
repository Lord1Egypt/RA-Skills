---
name: zhihu-hot
description: 获取知乎每日热搜榜单，支持搜索、统计、范围分析。数据从 2021-01-08 至今。
---

# 知乎热搜

从 [zhihu-hot-hub](https://github.com/SnailDev/zhihu-hot-hub) 获取知乎热搜数据。

**数据覆盖**: 2021-01-08 至今（1900+ 天完整归档，每小时更新）

## 快速使用

```bash
# 今日热搜
./zhihu-hot.py

# 前 10 条
./zhihu-hot.py -n 10

# 紧凑格式
./zhihu-hot.py -c

# 单行格式（适合推送）
./zhihu-hot.py -o

# 搜索热搜
./zhihu-hot.py -s AI
```

## 命令参数

| 参数 | 简写 | 说明 |
|------|------|------|
| `DATE` | | 日期 (YYYY-MM-DD)，默认今天 |
| `--limit` | `-n` | 限制显示条数 |
| `--compact` | `-c` | 紧凑格式输出 |
| `--oneline` | `-o` | 单行格式（适合推送） |
| `--json` | `-j` | JSON 格式输出 |
| `--url` | `-u` | 显示完整 URL |
| `--search` | `-s` | 搜索关键词 |
| `--range` | `-r` | 日期范围分析 |
| `--archives` | | 显示归档信息 |
| `--export` | `-e` | 导出到文件 |
| `--clear-cache` | | 清理缓存 |
| `--stats` | | 缓存统计 |
| `--no-cache` | | 不使用缓存 |
| `--version` | `-v` | 显示版本 |

## 输出格式

### 默认表格格式

```
📊 知乎热搜 - 2026-03-27

⏰ 更新：2026-03-27 08:17:05 +0800

🔥 热门搜索
┌────┬──────────────────────────────────────────┐
│  1 │ 你在低谷期学会了什么                     │
│  2 │ 郑钦文不敌萨巴伦卡                       │
│  3 │ C919 还能成批生产吗                       │
└────┴──────────────────────────────────────────┘
```

### 紧凑格式

```
📊 知乎热搜 2026-03-27 | ⏰ 08:17:05 +0800

 1. 你在低谷期学会了什么
 2. 郑钦文不敌萨巴伦卡
 3. C919 还能成批生产吗
```

### 单行格式（推送用）

```
📊 知乎热搜 2026-03-27: 你在低谷期学会了什么 | 郑钦文不敌萨巴伦卡 | C919 还能成批生产吗
```

### JSON 格式

```json
{
  "date": "2026-03-27",
  "update_time": "08:17:05 +0800",
  "hot_search": [
    {"title": "你在低谷期学会了什么", "url": "...", "decoded_url": "..."}
  ]
}
```

## 高级功能

### 🔍 搜索功能

```bash
# 搜索今日热搜
./zhihu-hot.py -s AI

# 搜索并显示 URL
./zhihu-hot.py -s 周杰伦 -u
```

### 📊 日期范围分析

```bash
# 分析本月
./zhihu-hot.py -r 2026-03-01 2026-03-26

# 分析指定周期
./zhihu-hot.py -r 2026-03-01 2026-03-15 --export report.md
```

### 📚 归档信息

```bash
./zhihu-hot.py --archives
```

输出：
```
📚 归档信息
   最早：2021-01-08
   最新：2026-03-27
   总计：1904 天
```

### 📁 导出功能

```bash
# 导出今日热搜
./zhihu-hot.py -e today.md

# 导出 JSON
./zhihu-hot.py -j -n 50 -e hot50.json

# 导出分析报告
./zhihu-hot.py -r 2026-03-01 2026-03-26 -e march-report.md
```

### 💾 缓存管理

```bash
# 查看缓存统计
./zhihu-hot.py --stats

# 清理缓存
./zhihu-hot.py --clear-cache

# 强制刷新
./zhihu-hot.py --no-cache 2026-03-20
```

### 📅 历史热搜

```bash
./zhihu-hot.py 2026-03-20
./zhihu-hot.py 2026-03-20 -n 10
./zhihu-hot.py 2021-01-08  # 最早数据
```

## 数据来源

- **GitHub**: https://github.com/SnailDev/zhihu-hot-hub
- **更新频率**: 每小时更新
- **历史数据**: 2021-01-08 至今（1900+ 天）
- **实时数据**: README.md（当前）

## 缓存配置

| 类型 | 目录 | 有效期 |
|------|------|--------|
| 日数据缓存 | `~/.cache/zhihu-hot/` | 1 小时 |
| 归档列表 | `~/.cache/zhihu-hot/` | 2 小时 |

## 集成示例

### Python 调用

```python
import subprocess
import json

# 获取 JSON 数据
result = subprocess.run(
    ["./zhihu-hot.py", "--json", "-n", "10"],
    capture_output=True, text=True
)
data = json.loads(result.stdout)
print(data["hot_search"])

# 范围分析
result = subprocess.run(
    ["./zhihu-hot.py", "-r", "2026-03-01", "2026-03-26"],
    capture_output=True, text=True
)
print(result.stdout)
```

### Shell 脚本

```bash
#!/bin/bash
# 每日推送
./zhihu-hot.py -o -n 5 | send-to-telegram

# 周报生成
./zhihu-hot.py -r $(date -d '7 days ago' +%Y-%m-%d) $(date +%Y-%m-%d) -e weekly-report.md
```

### Cron 定时任务

```cron
# 每日 9 点推送
0 9 * * * /path/to/zhihu-hot.py -o -n 10 --no-cache | mail -s "知乎热搜" user@example.com

# 每周一生成周报
0 10 * * 1 /path/to/zhihu-hot.py -r $(date -d '7 days ago' +%Y-%m-%d) $(date +%Y-%m-%d) -e /reports/weekly-$(date +%%Y%%m%%d).md
```

## 版本历史

- **v3.0** - 新增日期范围分析、归档信息查询、改进缓存管理
- **v2.1** - 新增导出功能、缓存统计、彩色输出
- **v2.0** - 新增搜索功能、URL 解码、多种输出格式
- **v1.0** - 基础功能：获取今日/历史热搜