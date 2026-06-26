# Odds Movement Monitor 盘口变化监控

实时监控足球、篮球等体育赛事的亚盘、欧赔、大小球盘口变化。

## 功能特性

- 📊 **实时监控** — 多平台盘口数据采集
- 🔍 **变化检测** — 盘口升降、水位变动识别
- 🚨 **异常预警** — 大额注单信号、诱盘检测
- 📈 **趋势分析** — 历史数据追踪、变化轨迹
- 🔔 **自动通知** — 关键变化即时提醒

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 设置 API Key

```bash
export ODDS_API_KEY="your_api_key_here"
```

获取 API Key: [the-odds-api.com](https://the-odds-api.com/)

### 运行演示

```bash
python monitor.py --demo
```

## 使用方法

### 启动持续监控

```bash
# 监控足球盘口，每60秒扫描一次
python monitor.py --monitor --sport soccer --interval 60

# 监控篮球
python monitor.py --monitor --sport basketball
```

### 查看监控报告

```bash
python monitor.py --report
```

### 高级分析演示

```bash
python change_detector.py
```

## 监控信号类型

| 信号 | 说明 | 严重度 |
|------|------|--------|
| `late_line_drop` | 临场降盘 | 🔴 高 |
| `late_line_rise` | 临场升盘 | 🟡 中 |
| `heavy_betting` | 大额注单 | 🔴 高 |
| `trap_favorite` | 诱盘信号 | 🔴 高 |
| `value_opportunity` | 价值机会 | 🟢 低 |
| `bookmaker_disagreement` | 机构分歧 | 🟡 中 |
| `reversal_warning` | 变盘反转 | 🔴 高 |

## 数据存储

SQLite 数据库存储:
- `odds_snapshots` — 赔率快照
- `odds_changes` — 变化记录
- `monitoring_config` — 监控配置

## 技术栈

- Python 3.8+
- 异步采集: `aiohttp`
- 数据存储: `sqlite3`
- 定时任务: `asyncio`

## 注意事项

⚠️ **免责声明**: 本工具仅供数据监控参考，不构成投注建议。

## License

MIT
