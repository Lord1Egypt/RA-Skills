---
name: trainclaw
description: 3-in-1 China 12306 query — tickets, route stops, transfer plans. Zero login. Filter 高铁/动车/火车 by type, time, duration. Pure Python, text/json/csv output. 火车票/余票/经停站/中转换乘.
version: 0.0.7
icon: 🚄
---

# TrainClaw 🚄 - China Rail Ticket Query / 车票查询AI助手

## 概述 / Overview

**3-in-1 China 12306 query: tickets + route stops + transfer plans, zero login.**
**三合一 12306 查询：余票 + 经停站 + 中转换乘，零登录。**

调用 `trainclaw.py` 一条命令完成查询。无需登录、无需API Key、无需额外配置——仅依赖 Python + requests，开箱即用。支持车次类型筛选、时间窗口、排序，text/json/csv 多格式输出。

One command via `trainclaw.py`. No login, no API key, no extra config — just Python + requests, ready to go. Filter by train type, time window, sort by duration. Output: text / json / csv.

## 触发方式 / Trigger

用户提到火车票、高铁票、动车票、车次查询、余票、经停站、中转换乘、12306等关键词时触发。

Trigger when user mentions train tickets, bullet train, remaining tickets, route stops, transfer, 12306, China rail, etc.

### 快速示例 / Quick Examples

- **"查一下明天北京到上海的高铁票"** → 余票查询
- **"Any bullet trains from Beijing to Shanghai tomorrow?"** → Ticket query
- **"G1033 经停哪些站？"** → 经停站查询
- **"What stops does G1033 make?"** → Route stops
- **"从深圳到拉萨怎么中转？"** → 中转查询
- **"How to get from Shenzhen to Lhasa by train?"** → Transfer plan
- **"南京到上海的动车，上午出发，按时长排序"** → 带筛选的余票查询
- **"EMU trains Nanjing to Shanghai, morning only, sort by duration"** → Filtered query

## 工作流程 / Workflow

```
用户说："查明天北京到上海的高铁"
    ↓
提取参数：出发=北京，到达=上海，日期=明天，类型=G
    ↓
执行命令：
  python trainclaw.py query -f 北京 -t 上海 -d 2026-03-04 --type G
    ↓
返回余票信息（text 格式，直接展示给用户）
```

## 子命令 / Subcommands

### 1. 余票查询 / Ticket Query (query)

查询两站之间的余票信息，支持筛选和排序。

```bash
# 基础查询
python trainclaw.py query -f 北京 -t 上海

# 完整参数
python trainclaw.py query -f 北京 -t 上海 -d 2026-03-04 \
  --type G --earliest 8 --latest 18 --sort duration -n 10 -o text
```

### 2. 经停站查询 / Route Stops (route)

查询某车次的所有经停站信息。

```bash
python trainclaw.py route -c G1033 -d 2026-03-04
python trainclaw.py route -c G1 -d 2026-03-04 -o json
```

### 3. 中转查询 / Transfer Plans (transfer)

查询需要换乘的中转方案。

```bash
# 自动推荐中转站
python trainclaw.py transfer -f 深圳 -t 拉萨 -n 5

# 指定中转站
python trainclaw.py transfer -f 深圳 -t 拉萨 -m 西安 -d 2026-03-04
```

## 参数说明 / Parameters

### 通用参数 / Common Parameters

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-d, --date` | 查询日期 (yyyy-MM-dd) | 今天 |
| `-o, --format` | 输出格式: text / json / csv | text |

### 筛选参数 / Filter Parameters (query / transfer)

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-f, --from` | 出发站（站名/城市名/三字母代码） | **必填** |
| `-t, --to` | 到达站（站名/城市名/三字母代码） | **必填** |
| `--type` | 车次类型筛选（见下表） | 不筛选 |
| `--earliest` | 最早出发小时 (0-24) | 0 |
| `--latest` | 最晚出发小时 (0-24) | 24 |
| `--sort` | 排序: startTime / arriveTime / duration | 不排序 |
| `--reverse` | 倒序排列 | 否 |
| `-n, --limit` | 最大结果数 | query: 不限, transfer: 10 |

### 车次类型代码 / Train Type Codes

| 代码 | 含义 |
|------|------|
| G | 高铁/城际（G/C 开头） |
| D | 动车 |
| Z | 直达特快 |
| T | 特快 |
| K | 快速 |
| O | 其他（非 GDZTK） |
| F | 复兴号 |
| S | 智能动车组 |

可组合使用，如 `--type GD` 表示高铁+动车。

## 车站名解析 / Station Name Input

支持三种输入格式，自动识别：

1. **精确站名**: `北京南`、`上海虹桥`、`南京南` → 直接匹配
2. **城市名**: `北京`、`上海`、`南京` → 匹配该城市代表站
3. **三字母代码**: `BJP`、`SHH`、`NJH` → 直接使用

## 输出格式 / Output Formats

### text 格式（默认，推荐给用户阅读）
```
车次 | 出发站→到达站 | 出发→到达 | 历时 | 席位信息 | 标签
G25 | 北京南→上海虹桥 | 17:00→21:18 | 04:18 | 商务座:1张/2318.0元, 一等座:有票/1060.0元 | 复兴号
```

### json 格式（推荐程序处理）
完整 JSON 数组，包含所有字段。

### csv 格式（仅 query 支持）
标准 CSV，含表头行。

## 文件位置 / Files

- **主程序**: `trainclaw.py`
- **配置文件**: `config.py`
- **缓存目录**: `cache/`（车站数据自动缓存 7 天）

## 注意事项 / Notes

1. **日期限制**: 仅支持查询今天及未来 15 天内的车票
2. **网络依赖**: 首次运行需下载车站数据（~3000 站），之后使用本地缓存
3. **错误输出**: 错误信息输出到 stderr，数据输出到 stdout，支持管道操作
4. **中转限制**: 中转查询结果取决于 12306 的推荐，非所有组合都有结果
5. **依赖**: 仅需 Python 3.8+ 和 `requests` 库

## 使用场景示例 / Usage Scenarios

### 日常查票 / Daily Check
```
用户: "明天北京到上海有什么高铁？"
→ python trainclaw.py query -f 北京 -t 上海 -d {明天日期} --type G
```

### 时间筛选 / Time Filter
```
用户: "上午 8 点到 12 点从南京到杭州的动车"
→ python trainclaw.py query -f 南京 -t 杭州 --type D --earliest 8 --latest 12
```

### 查经停站 / Route Stops
```
用户: "G1033 都停哪些站？"
→ python trainclaw.py route -c G1033 -d {今天日期}
```

### 中转方案 / Transfer Plan
```
用户: "从北京怎么坐火车去成都？"
→ python trainclaw.py transfer -f 北京 -t 成都 -n 5
```

## 作者 / Author

公益技能，免费开源。 / Community-driven, open-source, free for everyone.

- **Email**: nuaa02@gmail.com
- **小红书 / Xiaohongshu**: @深度连接
- **GitHub**: [AI4MSE/TrainClaw](https://github.com/AI4MSE/TrainClaw)
