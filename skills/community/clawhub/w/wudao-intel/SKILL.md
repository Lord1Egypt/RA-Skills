---
name: wudao-intel
version: "1.0.0"
description: "悟道 · A股市场情报：龙虎榜、研报数据、竞价数据、智能热榜、每日简报、游资席位。Use when: user asks about A股, 龙虎榜, hot topics, trending news, research reports, analyst ratings, pre-market auction, daily briefings, dragon-tiger board, or institutional trading data. NOT for: K-line charts, limit-up boards, sector rotation, or capital flow."
metadata:
  {
    "openclaw":
      {
        "emoji": "📰",
        "requires": { "env": ["LB_API_KEY", "LB_API_BASE"] },
      },
  }
---

# 悟道 · A股市场情报

提供 5 个市场情报接口：智能热榜、研报数据、竞价数据、每日简报、龙虎榜。

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

### 1. 智能热榜

多平台聚合热点，AI 提炼后的主题列表。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/hotlist?type=general"
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/hotlist?type=financial"
```

参数：`type`（`general` 综合热榜 / `financial` 财经热榜，默认 `general`）。

返回 `{ type, themes[], totalNews, updateTime, nextUpdate }`。每个主题：

| 字段 | 说明 |
|------|------|
| `title` | 主题标题 |
| `summary` | AI 摘要 |
| `hotScore` | 热度分（1-100） |
| `category` | 分类 |
| `platforms[]` | 来源平台列表 |
| `newsCount` | 关联新闻数 |
| `representativeNews` | 代表性新闻：`{ title, summary, url, platform, hotValue }` |
| `relatedNews[]` | 关联新闻列表（最多5条） |

### 2. 研报数据

券商研报，含评级和目标价。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/research-reports?stockCode=600519&pageSize=10"
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/research-reports?keyword=人工智能&page=1&pageSize=20"
```

参数：`stockCode`, `keyword`, `startDate`/`endDate`, `page`, `pageSize`（上限50）, `sortBy`（默认 `publishDate`）, `sortOrder`。

返回 `{ reports[], pagination }`。每份研报关键字段：

| 字段 | 说明 |
|------|------|
| `title` | 研报标题 |
| `stockName`, `stockCode` | 标的股票 |
| `orgSName` | 机构简称（如"中信证券"） |
| `author[]` | 分析师列表 |
| `publishDate` | 发布日期 |
| `emRatingName` | 评级（买入/增持/中性等） |
| `ratingChange` | 评级变动（升级/下调/维持/首次） |
| `indvAimPriceT` | 目标价（上限） |
| `indvAimPriceL` | 目标价（下限） |
| `predictThisYearEps` | 预测今年 EPS |
| `predictThisYearPe` | 预测今年 PE |
| `industryName` | 行业分类 |

### 3. 竞价数据

查询个股集合竞价成交数据。支持单股、批量、历史区间三种模式。竞价数据在每个交易日 9:25 后可获取。

**单股查询**（返回单个对象）：

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/auction?code=600519"
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/auction?code=600519&trade_date=20260320"
```

**批量查询**（返回 `{ items[], total }`）：

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/auction?codes=600519,000001,300750"
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/auction?codes=600519,000001&trade_date=20260320"
```

**历史区间**（单股，返回 `{ items[], total }`）：

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/auction?code=600519&start_date=20260310&end_date=20260320"
```

参数：

| 参数 | 说明 |
|------|------|
| `code` | 单只股票代码（6位数字，如 `600519`） |
| `codes` | 批量股票代码，逗号分隔（上限50只） |
| `trade_date` | 指定日期（YYYYMMDD 或 YYYY-MM-DD），不传默认今天 |
| `start_date` / `end_date` | 历史区间查询（与 `code` 搭配使用，最多60天） |
| `limit` | 历史模式下最大返回条数（默认20，上限60） |

每条记录字段：

| 字段 | 说明 |
|------|------|
| `code` | 股票代码 |
| `name` | 股票名称 |
| `tradeDate` | 交易日期 YYYYMMDD |
| `price` | 竞价成交价 |
| `preClose` | 前收盘价 |
| `changeRate` | 竞价涨跌幅（%） |
| `vol` | 成交量 |
| `amount` | 竞价成交额（元） |
| `turnoverRate` | 换手率 |
| `volumeRatio` | 量比 |
| `floatShare` | 流通股本 |
| `bidAmountPercentile` | 竞价额60日历史分位（0-100，仅单股/批量模式） |
| `bidAmountRatio` | 竞价额占昨日全天成交额比例（%，仅单股/批量模式） |

**分析思路**：`bidAmountPercentile` > 80 说明竞价额处于近期高位，资金关注度高；`bidAmountRatio` 越高说明竞价阶段抢筹意愿越强。结合涨停板数据使用效果更佳。

### 4. 每日简报

AI 生成的市场简报，含核心摘要、热点题材、风险提示和机会板块。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/briefings?date=2026-03-20&type=morning"
```

参数：`date`（YYYY-MM-DD，默认今天）, `type`（可选筛选：`morning`/`midday`/`closing`/`evening`）。

返回简报数组。每份简报结构：

| 字段 | 说明 |
|------|------|
| `type` | 简报类型 |
| `date`, `time` | 日期和时间 |
| `content.coreSummary` | 核心摘要 |
| `content.fullContent` | 完整内容（Markdown） |
| `content.marketSummary` | 市场概要：`{ indices[], capitalFlow, sentiment }` |
| `content.hotTopics[]` | 热点题材：`{ title, content, stocks[], tags[] }` |
| `content.risks[]` | 风险提示：`{ content, level: high/medium/low }` |
| `content.opportunities` | 机会：`{ stocks[], sectors[], suggestion }` |
| `content.dataBoard` | 数据面板：`{ upDownCount, limitUp, limitDown, volume, turnover }` |
| `relatedNews[]` | 关联新闻 |

### 5. 龙虎榜

查询龙虎榜数据，包含上榜原因、买卖营业部明细、净买入金额等。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/dragon-tiger?date=2026-03-20"
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/dragon-tiger?stockCode=600519"
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/dragon-tiger?stockName=茅台&page=1&pageSize=20"
```

参数：`date`（YYYY-MM-DD 或 YYYYMMDD）, `stockCode`, `stockName`（模糊搜索）, `page`（默认1）, `pageSize`（默认50，上限100）。

返回数组，每条龙虎榜记录：

| 字段 | 类型 | 说明 |
|------|------|------|
| `date` | string | 日期 |
| `stockCode`, `stockName` | string | 股票代码/名称 |
| `reason` | string | 上榜原因（如"日涨幅偏离7%"） |
| `close` | number | 收盘价 |
| `chgPct` | number | 涨跌幅（%） |
| `volume` | number | 成交量 |
| `amount` | number | 成交额 |
| `netBuy` | number | 净买入额 |
| `totalBuy` | number | 总买入额 |
| `totalSell` | number | 总卖出额 |
| `buyBranches[]` | array | 买入前5营业部：`{ name, buyAmt, sellAmt, netAmt }` |
| `sellBranches[]` | array | 卖出前5营业部：`{ name, buyAmt, sellAmt, netAmt }` |
| `limitUpInfo` | object/null | 关联涨停板信息 |

**分析思路**：`netBuy` > 0 说明机构/游资净买入；关注知名游资席位出现在 `buyBranches` 中的股票。

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
