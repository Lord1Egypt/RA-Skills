# TrainClaw 🚄

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://github.com/AI4MSE/TrainClaw/blob/master/LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-AI4MSE%2FTrainClaw-black.svg)](https://github.com/AI4MSE/TrainClaw)

[English](README_ENG.md) | 中文

**3-in-1 China 12306 查询：余票 + 经停站 + 中转换乘，零登录。**
**3-in-1 China 12306 query: tickets + route stops + transfer plans, zero login.**

12306 铁路火车票 CLI 查询工具 — 无需登录、零 API Key、开箱即用。查询余票、经停站、中转方案。

12306 China Rail ticket CLI query tool — no login, no API key, plug & play. Query remaining tickets, route stops, and transfer plans.

> 更多技能：查航班 (FlyClaw)、导航 (NavClaw) 等，详见 https://github.com/AI4MSE/
>
> More skills: flight query (FlyClaw), navigation (NavClaw), etc. See https://github.com/AI4MSE/

## 功能 / Features

- **OpenClaw 技能** — 支持作为 OpenClaw 技能使用，参考 SKILL.md / Supports OpenClaw skill integration, see SKILL.md
- **余票查询** (`query`) — 查询两站之间的余票信息，支持按车次类型、出发时间筛选，按时间/历时排序，输出 text/json/csv / Query remaining tickets between two stations with train type, time window filtering, sorting, and multi-format output
- **经停站查询** (`route`) — 查询指定车次的全部经停站信息，输出 text/json / Query all stops for a given train, output text/json
- **中转查询** (`transfer`) — 查询需要换乘的中转方案，支持指定中转站，输出 text/json / Query transfer plans with optional mid-station, output text/json
- **日志系统** (`-v/--verbose`) — 可选的详细日志输出，DEBUG 级别显示 HTTP 请求细节 / Verbose logging with HTTP request details
- **查询冷却** — API 请求间隔可设置，避免请求过于频繁 / Configurable cooldown between API requests
- **友好错误信息** — 中文错误提示、车站名候选建议、空结果操作建议 / Friendly error messages with station name suggestions

## 安装 / Install

```bash
# 仅需 Python 3.8+ 和 requests 库 / Requires only Python 3.8+ and requests
pip install requests
```

## 使用示例 / Usage

### 余票查询 / Ticket Query

```bash
# 基础查询 / Basic query
python trainclaw.py query -f 北京 -t 上海

# 明天的高铁，上午出发，按历时排序，取前 5 条
# Tomorrow's bullet trains, morning departure, sort by duration, top 5
python trainclaw.py query -f 北京 -t 上海 -d 2026-03-04 --type G \
  --earliest 8 --latest 12 --sort duration -n 5

# JSON 输出 / JSON output
python trainclaw.py query -f 南京 -t 杭州 --type D -o json

# CSV 输出 / CSV output
python trainclaw.py query -f 广州 -t 深圳 -o csv

# 详细日志模式 / Verbose mode (DEBUG to stderr)
python trainclaw.py -v query -f 北京 -t 上海
```

### 经停站查询 / Route Stops

```bash
python trainclaw.py route -c G1 -d 2026-03-04
python trainclaw.py route -c G1033 -o json
```

### 中转查询 / Transfer Plans

```bash
# 自动推荐中转站 / Auto-recommend transfer stations
python trainclaw.py transfer -f 深圳 -t 拉萨 -n 5

# 指定中转站 / Specify transfer station
python trainclaw.py transfer -f 深圳 -t 拉萨 -m 西安 -d 2026-03-04
```

## 车站名输入 / Station Name Input

支持三种格式，自动识别 / Three formats, auto-detected:

| 格式 / Format | 示例 / Example | 说明 / Description |
|------|------|------|
| 精确站名 / Exact name | `北京南`、`上海虹桥` | 直接匹配 / Direct match |
| 城市名 / City name | `北京`、`上海` | 匹配代表站 / Maps to main station |
| 三字母代码 / 3-letter code | `BJP`、`SHH` | 直接使用 / Used directly |

## 车次类型代码 / Train Type Codes

| 代码 / Code | 含义 / Meaning |
|------|------|
| G | 高铁/城际 / High-speed / Intercity (G/C) |
| D | 动车 / EMU |
| Z | 直达特快 / Direct express |
| T | 特快 / Express |
| K | 快速 / Fast |
| O | 其他 / Other (non-GDZTK) |
| F | 复兴号 / Fuxing |
| S | 智能动车组 / Smart EMU |

可组合使用，如 `--type GD` 表示高铁+动车。Combinable, e.g. `--type GD` = high-speed + EMU.

## 版本 / Version

**当前版本 / Current**: 0.0.4

## 注意事项 / Notes

1. 一般仅支持查询今天及未来 15 天内的车票 / Generally supports today + next 15 days only
2. 首次运行需下载车站数据（~3000 站），之后使用本地缓存（7 天有效） / First run downloads station data (~3000 stations), then cached for 7 days
3. 错误信息输出到 stderr，数据输出到 stdout，支持管道操作 / Errors to stderr, data to stdout, pipe-friendly
4. 中转查询结果取决于查询网站的推荐算法 / Transfer results depend on 12306's recommendation algorithm

## 免责声明 / Disclaimer

本工具仅供学习和研究技术之用，不建议任何实际使用，使用时请遵守当地法律和法规。本项目与中国铁路无任何关联。

This tool is for educational and technical research purposes only. Not recommended for production use. Please comply with local laws and regulations. This project is not affiliated with China Railway.

## 作者 / Author

本项目为公益技能，免费开源。 / This is a community-driven, open-source skill — free for everyone.

- **Email**: nuaa02@gmail.com
- **小红书**: @深度连接
- **GitHub**: [AI4MSE/TrainClaw](https://github.com/AI4MSE/TrainClaw)

## 许可证 / License

[Apache License 2.0](LICENSE)
