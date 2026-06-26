---
name: sunsetbot-monitor-cn
description: >
  查询中国国内火烧云/晚霞/朝霞预报 (sunsetbot.top)。
  当用户询问火烧云预报、设置定时火烧云通知时使用。
version: "2.0.0"
author: "FrankMei (neverland_83@163.com)"
metadata:
  openclaw:
    category: weather
    tags: ["sunset", "sunrise", "火烧云", "晚霞", "朝霞", "sunsetbot", "weather-monitoring"]
---

# SunsetBot 火烧云预报（国内版）

> 基于 sunsetbot.top JSON API，纯 HTTP 请求获取火烧云预报数据。无需浏览器，单次查询 ~0.6秒。

**Core Pipeline**: `web_fetch API → JSON 解析 → 等级判定 → 阈值通知`

---

> [!CAUTION]
> ## 🚨 全局执行准则
>
> 1. **config.json 优先**：通知目标（飞书 Open ID）必须从 `config/config.json` 读取 `userOpenId` 字段，禁止在 SKILL.md 或 payload 中硬编码
> 2. **阈值通知**：鲜艳度 ≥ 0.2 才发飞书通知，< 0.2 仅写日志不打扰用户
> 3. **双格式日志**：每次查询必须同时写入 JSONL（`data/sunsetbot-monitor.log`）和 Markdown（`data/log.md`），追加不覆盖

---

## 工具索引

| 工具 | 用途 | 命令格式 |
|------|------|----------|
| `web_fetch` | 查询火烧云数据 | `web_fetch(url="https://sunsetbot.top/?intend=select_city&query_city={城市}&event={事件}&model={数据源}")` |
| `message` | 发送飞书通知 | `message(channel="feishu", to="<config.json userOpenId>", message="...")` |

---

## Workflow

### Step 1: 构造 API URL

🚧 **GATE**: 确认查询参数（城市、日期类型、数据源）

API URL 模板：

```
https://sunsetbot.top/?intend=select_city&query_city={城市}&event={事件}&model={数据源}
```

#### 参数说明

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `query_city` | 城市名称 | 深圳、上海、北京、广州、杭州等 |
| `event` | 日期类型 | `rise_1`(今天日出) `set_1`(今天日落) `rise_2`(明天日出) `set_2`(明天日落) |
| `model` | 数据源 | `GFS` `EC` |
| `intend` | 固定值 | `select_city` |

> 💡 **GFS 更新节奏**：大更新 7:30-8:30 和 19:30-20:30，小更新 13:30 和 1:30。建议 cron 在 **9:00**（早间大更新后）和 **21:00**（晚间大更新后）触发。

### Step 2: 调用 API 获取数据

一次 `web_fetch` 即可，返回 JSON：

```
web_fetch(url="https://sunsetbot.top/?intend=select_city&query_city=深圳&event=set_2&model=GFS")
```

#### 响应结构和提取规则

```json
{
  "status": "ok",
  "display_city_name": "广东省-深圳",
  "display_event_name_cn": "日落",
  "tb_quality": "0.36（中小烧）",
  "tb_aod": "0.245（还不错）",
  "tb_event_time": "2026-05-20 18:57:50",
  "display_times_str": "2026051900z"
}
```

**提取规则**：
- 从 `tb_quality` 提取数字：正则 `/^([\d.]+)/` → `0.36`
- 从 `tb_aod` 提取数字：同样方式 → `0.245`
- `display_event_name_cn` 直接使用
- `tb_event_time` 直接使用

### Step 3: 等级判定

| 鲜艳度 | 等级 | 通知标题 |
|--------|------|----------|
| < 0.2 | 不烧 | —（无需通知） |
| 0.2 - 0.5 | 中小烧 | 【注意：明日中小烧】 |
| 0.5 - 1.0 | 中大烧 | 【号外！中大烧】 |
| 1.0 - 2.0 | 大烧 | 【大烧！大烧】 |
| > 2.0 | 世纪大烧 | 【世纪大烧！冲！冲！冲！】 |

> 💡 日出和日落取鲜艳度**最大值**判定。最大值 < 0.2 时不发通知（仅写日志）。

### Step 4: 发送通知

🚧 **GATE**: 鲜艳度 ≥ 0.2

先从 `config/config.json` 读取 `userOpenId` 作为通知目标。

通知格式：

```
{通知标题}

📍 {城市} {日期类型}
⏰ {时间}
🔥 鲜艳度: {数值}
🌫️ 气溶胶: {数值}
🔗 https://sunsetbot.top/
```

> ⚠️ 日出和日落都有烧时取最大值那次，只发一次通知。

✅ **Checkpoint** — 通知已发送（或无需通知已跳过）。

### Step 5: 写日志（双格式）

无论是否通知，同时写入两种格式：

#### 5.1 JSONL 日志（机器可读）

文件：`data/sunsetbot-monitor.log`

```jsonl
{"ts":"2026-05-14 13:13","date":"2026-05-15","city":"深圳","type":"🌅日落","c":0.36,"a":0.413,"notify":true}
```

| 字段 | 说明 |
|------|------|
| `ts` | 查询时间 `YYYY-MM-DD HH:mm` |
| `date` | 预报日期 `YYYY-MM-DD` |
| `city` | 城市名 |
| `type` | `🌄日出` 或 `🌅日落` |
| `c` | 鲜艳度数值 |
| `a` | 气溶胶数值 |
| `notify` | 是否已通知 |

#### 5.2 Markdown 日志（人可读）

文件：`data/log.md`

追加一行表格，有烧时加 🔥 标记：

```markdown
## 火烧云监控日志

| 时间 | 预报 | 城市 | 类型 | 鲜艳度 | 气溶胶 | 等级 |
|------|------|------|------|--------|--------|------|
| 0514 13:13 | 0515 | 深圳 | 🌅日落 | 0.36 | 0.41 | 🔥中小烧 |
| 0519 15:50 | 0520 | 深圳 | 🌄日出 | 0.017 | 0.24 | — |
```

> 💡 首次写入时创建文件头（标题 + 表头），后续追加数据行。

✅ **Checkpoint** — 日志已写入。

---

## 定时监控（Cron）

```json
{
  "name": "sunset-monitor-morning",
  "agentId": "main",
  "enabled": true,
  "schedule": {
    "kind": "cron",
    "expr": "0 9 * * *",
    "tz": "Asia/Shanghai"
  },
  "sessionTarget": "isolated",
  "wakeMode": "now",
  "payload": {
    "kind": "agentTurn",
    "message": "使用 sunsetbot 技能查询深圳明天火烧云（日出+日落），读取 config.json 获取通知配置，按 SKILL.md 流程执行。"
  },
  "delivery": { "mode": "none" }
}
```

> 💡 两个 cron job（早 9:00 / 晚 21:00），payload 相同。

---

## 配置

配置文件 `config/config.json`：

```json
{
  "notifyChannel": "feishu",
  "userOpenId": "你的飞书Open ID"
}
```

| 字段 | 说明 |
|------|------|
| `notifyChannel` | 通知渠道（当前仅支持 `feishu`） |
| `userOpenId` | 飞书用户 Open ID，从飞书开发者后台获取 |

---

## 默认设置

| 配置 | 默认值 |
|------|--------|
| 城市 | 深圳 |
| 数据源 | GFS |
| 查询日期 | 明天日出 + 明天日落 |
| 通知渠道 | 飞书 |

---

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0.0 | 2026-04-15 | 初始版本，基于 browser 工具执行 DOM 操作获取数据 |
| v1.1.0 | 2026-04-18 | 尝试 web_fetch 重写（`check_web_fetch.js`），但调用方式有误未生效 |
| v2.0.0 | 2026-05-19 | **重大重构**：发现 sunsetbot.top JSON API，完全移除 browser 依赖；纯 web_fetch 调用，0.6 秒/次；双格式日志（JSONL + Markdown）；config.json 独立管理通知配置，SKILL.md 零隐私泄露 |