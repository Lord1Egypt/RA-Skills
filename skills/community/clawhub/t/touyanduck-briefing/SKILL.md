---
name: touyanduck-briefing
description: 投研鸭二级市场每日策略简报，每工作日更新，每4小时刷新行情。覆盖美股M7、GICS全板块、亚太、大宗、加密、聪明钱、AI产业链、预测市场，一键获取专业级市场洞察。支持历史归档查询和跨天趋势对比。
---
# 🦆 投研鸭 — 二级市场每日策略简报 v1.2.0

> 数据源: 投研鸭投资分析系统 v10.0 | 覆盖: 美股/M7/亚太/大宗/加密/聪明钱/AI产业链/预测市场
> 更新频率: 每工作日全量采集 + 每4小时刷新行情
> 数据质量: 八大铁律 + 29条致命错误零容忍
> **v1.2.0 新增**: 自定义域名 api.touyanduck.com（HTTPS）

## 触发关键词

当用户提到以下任意关键词时自动执行本 Skill：

- 中文：`投研鸭` / `二级市场` / `今天市场` / `美股怎么样` / `策略简报` / `市场分析` / `每日简报` / `投资简报` / `股市行情` / `大盘走势` / `聪明钱` / `M7` / `上周市场` / `这周趋势` / `历史行情`
- English：`touyanduck` / `market briefing` / `stock market today` / `daily briefing` / `investment briefing` / `market history` / `weekly trend`

## 使用方式

### 第一步：获取最新简报（默认）

```bash
curl -s "https://api.touyanduck.com/briefing.md"
```

这会返回一整页 Markdown 格式的简报（约 14KB），包含：

| 区块                 | 内容                                                |
| -------------------- | --------------------------------------------------- |
| Situation Assessment | 市场情绪分数 + 风险评分 + 7项红绿灯安全信号         |
| 核心结论             | 一句话核心判断（【】标记重点）                      |
| 核心事件链           | 当日驱动事件（含来源URL + 多源验证标记 ◆/◇）      |
| 市场数据             | 美股指数/M7/亚太/大宗/加密/GICS 11板块（含7日趋势） |
| 三大核心判断         | 置信度 + 逻辑链 + 参考来源                          |
| 行动建议             | hold/add/reduce/buy/sell/watch 等具体操作           |
| 聪明钱动向           | 桥水/伯克希尔/ARK/段永平等T1-T2基金动态             |
| 重点持仓快照         | 巴菲特、段永平、ARK最新13F持仓                      |
| 预测市场             | Polymarket/CME FedWatch 概率 + 24h变化              |
| 本周前瞻             | 重要事件日历（含影响等级）                          |
| 异动信号             | 实时异动（danger/warning/info三级）                 |
| 🧭 AI 交互引导       | 根据当日数据自动生成的高价值追问方向                |

### 第二步：检查时效性

简报第一行包含 `Updated:` 时间戳，**先检查再回答**：

| 时间差    | 处理方式                          |
| --------- | --------------------------------- |
| ≤ 12小时 | ✅ 数据新鲜，正常展示             |
| 12~24小时 | ⚠️ 提示数据可能不含最新盘后变动 |
| > 24小时  | 🔴 警告数据已过期，告知用户       |

### 第三步：根据用户问题回答

阅读简报 Markdown 内容，从中提取对应信息回答用户。

**回答原则**：

1. 简报已包含所有数据和分析，直接从中提取即可
2. 保留 ◆/◇ 证据标记和来源链接，让用户知道信息可信度
3. 保留【】重点标记，这是核心强调
4. 简报末尾的「🧭 你可以继续问我」列出了当日高价值追问，回答完后可主动提示用户
5. 如果用户问的标的不在简报中，明确告知

## 历史归档查询（v1.1.0 新增）

### 查看有哪些历史数据

```bash
curl -s "https://api.touyanduck.com/archive/index.json"
```

返回所有可用历史日期的索引：
```json
{
  "latest": "2026-04-08",
  "count": 2,
  "dates": ["2026-04-08", "2026-04-07"],
  "updatedAt": "2026-04-08T20:14:35+08:00"
}
```

### 获取某天的精简摘要（用于跨天对比）

```bash
curl -s "https://api.touyanduck.com/archive/2026-04-08/summary.json"
```

返回 ~1-2KB 的关键指标：
```json
{
  "date": "2026-04-08",
  "sentiment": { "score": 52, "label": "中性" },
  "risk": { "score": 80, "level": "high" },
  "trafficLights": { "red": 1, "yellow": 3, "green": 3 },
  "coreEvent": "美伊停火震动全球市场...",
  "usMarkets": {
    "sp500": { "price": 6616.85, "change": 0.08 },
    "nasdaq": { "price": 22017.85, "change": 0.1 },
    "vix": { "price": 20.4, "change": 15.6 }
  },
  "topMovers": [{ "name": "GOOGL", "change": 3.95 }],
  "smartMoneySummary": "ARK Invest: 连续两日买入TSLA...",
  "actionSummary": "停火窗口期油价快速回落...",
  "briefingUrl": "archive/2026-04-08/briefing.md"
}
```

### 获取某天的完整简报

```bash
curl -s "https://api.touyanduck.com/archive/2026-04-07/briefing.md"
```

### AI 使用策略（历史查询）

| 用户问题 | AI 动作 |
|---------|---------|
| "今天市场怎么样" | curl `briefing.md`（默认行为，不变） |
| "这周市场情绪变化" | curl `archive/index.json` → 获取本周日期 → curl 各天 `summary.json` → 比较 sentimentScore 趋势 |
| "上周五聪明钱在干嘛" | curl `archive/index.json` → 找到上周五日期 → curl `archive/{date}/briefing.md` → 提取聪明钱段落 |
| "VIX 最近一周走势" | curl 最近5天 `summary.json` → 提取 VIX 数据 → 绘制趋势 |
| "风险评分最近变化" | curl 各天 `summary.json` → 对比 risk.score 变化 + trafficLights 红黄绿变化 |

**重要**：跨天对比时，优先用 `summary.json`（~1KB），只在需要详细内容时才 curl 完整的 `briefing.md`（~14KB），以减少数据量。

## 按需深挖（可选）

简报 Markdown 已覆盖 80%+ 的问题。如需原始 JSON 数据（如精确到小数的价格、sparkline 数组等），可按需获取：

```bash
curl -s "https://api.touyanduck.com/briefing.json"   # 核心简报
curl -s "https://api.touyanduck.com/markets.json"    # 全球市场详情
curl -s "https://api.touyanduck.com/watchlist.json"  # 重点标的分析
curl -s "https://api.touyanduck.com/radar.json"      # 风险雷达
```

## 免责声明

⚠️ 本简报仅供投资参考，不构成投资建议。数据虽经严格审核，仍可能存在延迟或偏差。

---

📱 微信小程序: 搜索「投研鸭」 | 🦆 投研鸭 v10.0
