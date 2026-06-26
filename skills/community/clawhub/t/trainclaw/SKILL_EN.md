---
name: trainclaw
description: 3-in-1 China 12306 query — tickets, route stops, transfer plans. Zero login. Filter 高铁/动车/火车 by type, time, duration. Pure Python, text/json/csv output. 火车票/余票/经停站/中转换乘.
version: 0.0.7
icon: 🚄
---

# TrainClaw 🚄 - China Rail Ticket Query

## Overview

**3-in-1 China 12306 query: tickets + route stops + transfer plans, zero login.**

One command via `trainclaw.py`. No login, no API key, no extra config — just Python + requests, ready to go. Filter by train type, time window, sort by duration. Output: text / json / csv.

## Trigger

Trigger when user mentions train tickets, bullet train, remaining tickets, route stops, transfer, 12306, China rail, 火车票, 高铁, 经停站, 中转, etc.

### Quick Examples

- **"Any bullet trains from Beijing to Shanghai tomorrow?"** → Ticket query
- **"查一下明天北京到上海的高铁票"** → 余票查询
- **"What stops does G1033 make?"** → Route stops
- **"G1033 经停哪些站？"** → 经停站查询
- **"How to get from Shenzhen to Lhasa by train?"** → Transfer plan
- **"从深圳到拉萨怎么中转？"** → 中转查询
- **"EMU trains Nanjing to Shanghai, morning only, sort by duration"** → Filtered query
- **"南京到上海的动车，上午出发，按时长排序"** → 带筛选的余票查询

## Workflow

```
User: "Check tomorrow's bullet trains from Beijing to Shanghai"
    ↓
Extract params: from=Beijing, to=Shanghai, date=tomorrow, type=G
    ↓
Run command:
  python trainclaw.py query -f 北京 -t 上海 -d 2026-03-04 --type G
    ↓
Return ticket info (text format, display directly to user)
```

## Subcommands

### 1. Ticket Query (query / filter)

Query remaining tickets between two stations with filtering and sorting.

```bash
# Basic query
python trainclaw.py query -f 北京 -t 上海

# Full parameters
python trainclaw.py query -f 北京 -t 上海 -d 2026-03-04 \
  --type G --earliest 8 --latest 18 --sort duration -n 10 -o text
```

### 2. Route Stops (route)

Query all stops for a given train.

```bash
python trainclaw.py route -c G1033 -d 2026-03-04
python trainclaw.py route -c G1 -d 2026-03-04 -o json
```

### 3. Transfer Plans (transfer)

Query transfer/connection plans for multi-leg journeys.

```bash
# Auto-recommend transfer stations
python trainclaw.py transfer -f 深圳 -t 拉萨 -n 5

# Specify transfer station
python trainclaw.py transfer -f 深圳 -t 拉萨 -m 西安 -d 2026-03-04
```

## Parameters

### Common Parameters

| Parameter | Description | Default |
|------|------|--------|
| `-d, --date` | Query date (yyyy-MM-dd) | Today |
| `-o, --format` | Output format: text / json / csv | text |

### Filter Parameters (query / transfer)

| Parameter | Description | Default |
|------|------|--------|
| `-f, --from` | Departure station (name / city / 3-letter code) | **Required** |
| `-t, --to` | Arrival station (name / city / 3-letter code) | **Required** |
| `--type` | Train type filter (see table below) | All |
| `--earliest` | Earliest departure hour (0–24) | 0 |
| `--latest` | Latest departure hour (0–24) | 24 |
| `--sort` | Sort by: startTime / arriveTime / duration | None |
| `--reverse` | Reverse sort order | No |
| `-n, --limit` | Max results | query: unlimited, transfer: 10 |

### Train Type Codes

| Code | Meaning |
|------|------|
| G | High-speed / Intercity (G/C prefix) |
| D | EMU (D prefix) |
| Z | Direct Express |
| T | Express |
| K | Fast |
| O | Other (non-GDZTK) |
| F | Fuxing (CR series) |
| S | Smart EMU |

Combinable — e.g. `--type GD` matches both high-speed and EMU trains.

## Station Name Input

Three formats, auto-detected:

1. **Exact station name**: `北京南`, `上海虹桥`, `南京南` → Direct match
2. **City name**: `北京`, `上海`, `南京` → Maps to the city's main station
3. **3-letter code**: `BJP`, `SHH`, `NJH` → Used directly

## Output Formats

### text (default, human-readable)
```
Train | From→To | Depart→Arrive | Duration | Seats | Tags
G25   | 北京南→上海虹桥 | 17:00→21:18 | 04:18 | Business:1/¥2318, First:Avail/¥1060 | Fuxing
```

### json (for programmatic use)
Full JSON array with all fields.

### csv (query only)
Standard CSV with headers.

## Files

- **Main script**: `trainclaw.py`
- **Config**: `config.py`
- **Cache**: `cache/` (station data cached for 7 days)

## Notes

1. **Date range**: Generally supports today + next 15 days only (12306 limitation)
2. **Network**: First run downloads station data (~3000 stations), then uses local cache
3. **Streams**: Errors to stderr, data to stdout — fully pipe-friendly
4. **Transfers**: Results depend on 12306's recommendation algorithm, not all combinations available
5. **Dependencies**: Python 3.8+ and `requests` only

## Usage Scenarios

### Daily ticket check
```
User: "Any bullet trains from Beijing to Shanghai tomorrow?"
→ python trainclaw.py query -f 北京 -t 上海 -d {tomorrow} --type G
```

### Time filter
```
User: "EMU trains from Nanjing to Hangzhou, 8am to noon"
→ python trainclaw.py query -f 南京 -t 杭州 --type D --earliest 8 --latest 12
```

### Route stops
```
User: "What stops does G1033 make?"
→ python trainclaw.py route -c G1033 -d {today}
```

### Transfer plan
```
User: "How to get from Beijing to Chengdu by train?"
→ python trainclaw.py transfer -f 北京 -t 成都 -n 5
```

## Author

Community-driven, open-source skill — free for everyone.

- **Email**: nuaa02@gmail.com
- **Xiaohongshu (小红书)**: @深度连接
- **GitHub**: [AI4MSE/TrainClaw](https://github.com/AI4MSE/TrainClaw)
