---
name: wudao-analysis
version: "1.0.0"
description: "悟道 · A股资金分析：异动检测、资金流向、北向资金、板块轮动、股票关联、概念排行与成分股。Use when: user asks about A股, 资金, stock anomalies, capital flow, money flow, northbound capital, sector rotation, sector analysis, stock correlation, concept rankings, or concept constituent stocks. NOT for: K-line charts, limit-up boards, research reports, or news."
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "env": ["LB_API_KEY", "LB_API_BASE"] },
      },
  }
---

# 悟道 · A股资金分析

提供 6 个深度分析接口：异动检测、资金流向、板块轮动四象限、股票关联、概念排行、概念成分股。

## Instructions for the hosting agent

1. **环境变量**：若缺少 `LB_API_KEY` 或 `LB_API_BASE`，先提示用户按下方 **Setup** 配置。
2. **仅使用本文「Endpoints」中列出的路径与参数**，勿臆造接口。

## Setup

### 获取 API Key

1. 访问 [https://stock.quicktiny.cn](https://stock.quicktiny.cn) 注册账号并登录
2. 进入「开发者 API」页面（路径：`/developer`）
3. 点击「创建密钥」，系统会生成一个以 `lb_` 开头的 API Key
4. **立即复制保存**，密钥仅显示一次

### 配置环境变量

```bash
export LB_API_KEY="lb_your_key_here"
export LB_API_BASE="https://stock.quicktiny.cn/api/openclaw"
```

## Authentication

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/endpoint"
```

## Endpoints

### 1. 异动检测

检测个股异常交易行为（相对板块的异常偏离）。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/anomalies?date=2026-03-20"
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/anomalies?code=600519"
```

参数：`date`（按日期查所有异动股）或 `code`（查单只股票）。

每条异动记录关键字段：

| 字段 | 说明 |
|------|------|
| `code`, `name` | 股票代码/名称 |
| `date` | 异动日期 YYYYMMDD |
| `has_anomaly` | true/false |
| `anomaly_level` | `"none"` / `"normal"` / `"severe"` |
| `normal_triggered` | 是否触发普通异动 |
| `normal_deviation` | 偏离度（相对板块） |
| `normal_direction` | `"up"` / `"down"` |
| `severe_triggered` | 是否触发严重异动 |
| `severe_deviation` | 严重偏离度 |
| `severe_3strikes_triggered` | 是否触发"三振"（连续3天异动） |
| `severe_3strikes_dates[]` | 三振日期列表 |

**分析思路**：`severe` + `direction: up` 是暴力拉升信号；`3strikes` 触发说明持续异动，值得重点关注。

### 2. 资金流向

多维度资金流向数据。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/capital-flow?date=2026-03-20"
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/capital-flow?flowType=stock&stockCode=600519&date=2026-03-20"
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/capital-flow?flowType=sector&sectorType=概念&date=2026-03-20&limit=20"
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/capital-flow?flowType=hsgt&limit=5"
```

参数：
- `flowType`：`market`（大盘，默认）, `stock`（个股）, `sector`（板块）, `hsgt`（北向资金）
- `stockCode`：个股代码（flowType=stock 时必填）
- `sectorType`：`行业`/`概念`（默认）/`地域`（flowType=sector 时）
- `date`, `limit`

返回数据结构随 `flowType` 不同而变化。个股资金流向包含：`buy_sm_amount`/`sell_sm_amount`（小单）, `buy_md_amount`/`sell_md_amount`（中单）, `buy_lg_amount`/`sell_lg_amount`（大单）, `buy_elg_amount`/`sell_elg_amount`（超大单）, `net_mf_amount`（主力净流入）等。北向资金包含 `north_money`（北向净买入）, `south_money`（南向净买入）等。

### 3. 板块分析

板块轮动四象限分析（动量 vs 强度），用于判断板块所处阶段。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/sector-analysis?source=dongcai_concept&period=60&strengthPeriod=5"
```

参数：`source`（`industry`/`dongcai_concept`/`theme`，默认 `dongcai_concept`）, `period`（5/10/20/60/120，默认60）, `strengthPeriod`（3/5/10，默认5，不能超过 period）。

返回结构：

```json
{
  "quadrants": {
    "highStrong": [...],
    "highWeak": [...],
    "lowStrong": [...],
    "lowWeak": [...]
  },
  "allSectors": [...],
  "thresholds": { "strengthLine": 0, "periodLine": 0 },
  "meta": { "source", "period", "strengthPeriod", "sectorCount" }
}
```

每个板块字段：`name`, `todayChange`（今日涨幅%）, `periodChange`（区间涨幅%）, `recentChange`（近期强度%）, `recentUpDays`, `stockCount`, `volumeRatio`, `positionPctRank`（0-100百分位）。

**四象限含义**：`highStrong` = 强势主升（持有）; `highWeak` = 高位回调（减仓）; `lowStrong` = 底部反转（关注）; `lowWeak` = 弱势下跌（回避）。

### 4. 股票关联

基于概念共现分析，找到与目标股票历史上高度联动的关联股。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/correlation/600519"
```

参数：`code*`（路径参数）。

返回：`{ code, name, industry, correlations[], totalRelatedStocks, strongRelationCount, dataRange }`。

每条关联记录：

| 字段 | 说明 |
|------|------|
| `relatedCode`, `relatedName`, `relatedIndustry` | 关联股信息 |
| `score` | 综合关联度分数 |
| `strengthLevel` | `"强关联"` / `"中等关联"` / `"弱关联"` |
| `relationshipType` | `"本股领涨"` / `"对方领涨"` / `"同步联动"` / `"无明显规律"` |
| `strongestConcept` | 最强共现概念 |
| `conceptBreakdown[]` | 概念维度明细：`{ concept, count, avgTimeDiff, leadCount, lagCount }` |
| `recentDates[]` | 最近共现日期（最多5个） |

**分析思路**：`strengthLevel: 强关联` + `relationshipType: 本股领涨` 的关联股可作为跟随标的。

### 5. 概念排行

当日热门概念板块排名。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/concepts/ranking?date=20260320&limit=30"
```

参数：`date*`（YYYYMMDD）, `limit`（默认50）。

返回数组，按涨停数降序。每个概念：`trade_date`, `ts_code`（概念代码，如 `885760.KP`）, `name`, `z_t_num`（涨停股数量）, `up_num`（排名变化）。

### 6. 概念成分股

获取概念板块内的成分股详情。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/concepts/885760.TI/stocks?date=20260320"
```

参数：`tsCode*`（路径参数，概念代码）, `date`（可选，YYYYMMDD）。

返回数组，每只股票：`trade_date`, `ts_code`, `concept_name`, `con_code`（股票完整代码，如 `600519.SH`）, `con_name`（股票名称）, `desc`（概念关联描述）, `hot_num`（热度）。

## Response Format

成功：`{ "success": true, "data": {...}, "meta": {...} }`
失败：`{ "success": false, "error": "ERROR_CODE", "message": "..." }`

## Error Codes

| Code | HTTP | 说明 |
|------|------|------|
| `MISSING_API_KEY` | 401 | 未提供 API Key |
| `INVALID_API_KEY` | 401 | Key 无效 |
| `KEY_EXPIRED` | 403 | Key 已过期 |
| `RATE_LIMIT_EXCEEDED` | 429 | 限流 |
| `MISSING_PARAM` | 400 | 缺少必填参数 |
| `INVALID_PARAM` | 400 | 参数格式错误 |

## Notes

- 日期格式：同时支持 `YYYY-MM-DD` 和 `YYYYMMDD`
- 股票代码：6 位数字（`600519`）或完整代码（`600519.SH`）
- A 股交易时间：9:15-15:00（北京时间）
