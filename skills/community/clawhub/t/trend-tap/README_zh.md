# 📡 Trend Tap — 全网热点一触即达

[![ClawHub](https://img.shields.io/badge/ClawHub-trend--tap-blue)](https://clawhub.ai)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-brightgreen)](https://python.org)
[![Zero Dependencies](https://img.shields.io/badge/依赖-零-orange)]()

**[English](README.md)**

实时全网热点聚合技能，适用于 [OpenClaw](https://openclaw.ai)。同时扫描 **7 大平台**，无需 API Key，零成本，零依赖。

## 支持平台

| 平台 | 数据来源 | 需要登录 |
|------|---------|:---:|
| 🐦 X/Twitter | [trends24.in](https://trends24.in) 网页解析 | 否 |
| 👽 Reddit | 公开 RSS 订阅 | 否 |
| 🔍 Google Trends | RSS 订阅源 | 否 |
| 💻 Hacker News | Firebase 公开 API | 否 |
| 📖 知乎 | [今日热榜](https://tophub.today) + API 降级 | 否 |
| 📺 Bilibili | 公开 API | 否 |
| 🔥 微博 | AJAX 接口 + 网页降级 | 否 |

## 安装

```bash
clawhub install trend-tap
```

或手动克隆：

```bash
git clone https://github.com/XiaoYiWeio/trend-tap.git ~/.openclaw/workspace/skills/trend-tap
```

## 使用方式

### 在 OpenClaw 中（推荐）

直接对 Agent 说：
- "trends"
- "今天有什么热点"
- "热搜"
- "全网在聊什么"

Agent 会自动触发 Trend Tap，按照**渐进式披露**模式回复：

1. **第一轮 — 概览**：展示 7 个平台各自的 #1 热点，问你想展开哪个
2. **第二轮 — 展开**：展示你选的平台 Top 10，带可点击链接
3. **第三轮 — 深挖**：想了解某条热点的来龙去脉？Agent 会帮你分析

### 命令行

```bash
# 大盘概览（~5秒完成）
python3 scripts/trends.py --mode overview

# 展开某个平台
python3 scripts/trends.py --source weibo --top 10

# 多平台同时展开
python3 scripts/trends.py --source zhihu,weibo,bilibili --top 5

# 全部平台展开
python3 scripts/trends.py --mode all --top 5

# JSON 格式输出
python3 scripts/trends.py --mode overview --json
```

### 地区过滤（Twitter 和 Google）

```bash
python3 scripts/trends.py --source twitter --region japan --top 10
python3 scripts/trends.py --source google --region CN --top 10
```

### 定时推送

```bash
# 每天早上 11 点推送热点
python3 scripts/scheduler.py --set "0 11 * * *"

# 查看当前定时任务
python3 scripts/scheduler.py --list

# 删除定时任务
python3 scripts/scheduler.py --remove
```

## 技术特点

- **零成本** — 所有数据源免费、无需注册
- **零依赖** — 纯 Python 标准库，无需 `pip install`
- **并发抓取** — 7 个源同时请求，5 秒内完成
- **自动重试** — 每个源最多 3 次机会，超时自动重试
- **多级降级** — 知乎/B站/微博各有 2-3 种备选抓取策略
- **渐进式披露** — 先概览后展开，不信息过载

## 环境要求

- Python 3.9+
- 无需安装任何第三方包

## 许可证

MIT
