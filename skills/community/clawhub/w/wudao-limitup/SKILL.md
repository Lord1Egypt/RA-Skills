---
name: wudao-limitup
version: "1.0.0"
description: "悟道 · A股涨停板：涨停梯队、连板、炸板池、跌停池、冲刺涨停、涨跌停统计、最强风口、封板事件流、涨停筛选、涨停溢价。Use when: user asks about A股, 涨停, limit-up boards, limit-up ladder, broken limit-up, limit-down stocks, approaching limit-up, limit-up statistics, hot sectors by limit-up, seal/break events, limit-up filtering, or limit-up premium analysis. NOT for: K-line charts, capital flow, research reports, or general market data."
metadata:
  {
    "openclaw":
      {
        "emoji": "🔥",
        "requires": { "env": ["LB_API_KEY", "LB_API_BASE"] },
      },
  }
---

# 悟道 · A股涨停板

提供 9 个涨停板相关接口，覆盖短线打板交易的完整数据需求：梯队、筛选、溢价、炸板池、跌停池、冲刺涨停、统计、最强风口、事件流。

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

### 1. 涨停梯队 ⭐

核心功能。展示连板梯队（1板、2板、3板…最高板）及每层的个股详情。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/ladder?date=20260320"
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/ladder?date=2026-03-20"
```

参数：`date*`（YYYYMMDD 或 YYYY-MM-DD）。

返回结构：

```json
{
  "dateRange": "2026-03-20 至 2026-03-20",
  "dates": [
    {
      "date": "20260320",
      "dayOfWeek": "周五",
      "totalStocks": 28,
      "pauseRatio": 0.7,
      "boards": [
        { "level": 6, "stocks": [...] },
        { "level": 3, "stocks": [...] },
        { "level": 1, "stocks": [...] }
      ],
      "isRealtime": true,
      "limitUpCount": { "today": { "num": 28, "history_num": 51, "rate": 0.549, "open_num": 23 }, "yesterday": {...} },
      "limitDownCount": {...},
      "tradeStatus": { "id": "afternoon_trade", "name": "交易中" }
    }
  ]
}
```

`boards` 按 `level`（连板天数）**降序**排列。`limitUpCount`/`limitDownCount`/`tradeStatus` 仅盘中实时数据有。

每只股票的关键字段：

| 字段 | 说明 |
|------|------|
| `name`, `code` | 股票名称和代码 |
| `level`, `continue_num` | 连板天数 |
| `price`, `change`（字符串，含单位） | 显示用价格和涨幅 |
| `latest`, `change_rate` | 数值型价格和涨幅 |
| `first_limit_up_time`, `last_limit_up_time` | 首次/最后封板时间（HH:MM:SS） |
| `limit_up_type` | 涨停类型（换手板/一字板等） |
| `open_num` | 开板次数 |
| `order_volume`, `order_amount` | 封单量/封单额 |
| `currency_value`, `turnover_rate` | 流通市值/换手率 |
| `reason_type` | 涨停原因关键词 |
| `reason_info` | 涨停详细分析（AI 生成，100-300字） |
| `industry` | 所属行业 |
| `jiuyangongshe_category_name` | 扩展概念分类 |
| `jiuyangongshe_analysis` | 题材扩展解读 |
| `tags[]` | 自动标签（如"总龙头""高标龙""题材龙""中军""一字龙"等） |
| `is_margin` | 是否融资融券标的 |
| `is_new`, `is_again_limit` | 是否新股/是否回封 |

**分析思路**：`level` 最高的是空间板，决定市场高度；`tags` 含"总龙头"的是核心标的；`first_limit_up_time` 越早越强势；`open_num` 为 0 代表一封到底。

### 2. 涨停筛选

多维度筛选历史涨停股数据。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/limit-up/filter?date=2026-03-20&continueNumMin=2&limit=50"
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/limit-up/filter?date=2026-03-20&reasonType=人工智能"
```

参数：`date`, `startDate`/`endDate`, `continueNum`, `continueNumMin`/`continueNumMax`, `reasonType`（模糊匹配）, `industry`（模糊匹配）, `page`, `limit`（默认20，上限100）, `sortBy`（默认 `continue_num`）, `sortOrder`（默认 `desc`）。

返回 `{ items[], pagination: { page, pageSize, total, totalPages } }`。每只股票字段包含梯队接口的所有字段，额外包括 `main_business`（主营业务）, `business_scope`（经营范围）等。

### 3. 涨停溢价

分析涨停股次日开盘溢价率，用于评估哪些股打板后有肉吃。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/limit-up/premium?startDate=2026-03-01&endDate=2026-03-20&minLimitUpCount=3"
```

参数：`startDate*`, `endDate*`, `minLimitUpCount`（默认5）, `sortBy`（`avgPremium`/`totalCount`/`positiveRate`/`maxContinueNum`）, `sortOrder`, `page`, `limit`。

返回 `{ total, dateRange, stocks[] }`。每只股票：

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | string | 股票代码 |
| `name` | string | 名称 |
| `industry` | string | 行业 |
| `totalCount` | number | 区间内涨停次数 |
| `maxContinueNum` | number | 最大连板数 |
| `avgPremium` | number/null | 平均次日溢价率（%），正=高开，负=低开 |
| `positiveRate` | number | 正溢价比例（%） |
| `premiumSamples` | number | 有效样本数 |

**分析思路**：`avgPremium` > 1% 且 `positiveRate` > 60% 的股票次日打板有溢价保护。

### 4. 炸板池 ⭐

盘中曾触及涨停但未封住的股票。炸板后回封=强势信号，连续炸板=弱势。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/broken-limit-up?date=2026-03-20"
```

返回结构：

```json
{
  "data": {
    "stocks": [...],
    "total": 19,
    "stats": {
      "limitUpCount": { "today": { "num": 24, "history_num": 43, "rate": 0.558, "open_num": 19 }, "yesterday": { ... } },
      "limitDownCount": { "today": { "num": 51, "history_num": 65, "rate": 0.785, "open_num": 14 }, "yesterday": { ... } },
      "tradeStatus": { "id": "afternoon_trade", "name": "交易中", "start_time": "13:00", "end_time": "14:57" }
    }
  }
}
```

`stocks[]` 每只股票字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | string | 股票代码 |
| `name` | string | 股票名称 |
| `changePercent` | number | 当前涨幅（%） |
| `price` | number | 最新价 |
| `currencyValue` | number | 流通市值（元） |
| `turnoverRate` | number | 换手率（%） |
| `openNum` | number | 开板次数（越多说明封不住） |
| `firstLimitUpTime` | number | 首次触及涨停的 Unix 时间戳 |
| `lastLimitUpTime` | number | 最后一次触及涨停的 Unix 时间戳 |
| `limitUpSucRate` | number | 历史封板成功率 |
| `changeTag` | string | `"LIMIT_FAILED"`=炸板未回封 |
| `reasonType` | string | 涨停原因关键词 |
| `market_id` | number | `17`=上交所, `33`=深交所 |

`stats` 是全市场涨跌停统计快照（today vs yesterday），含 `num`（封板数）、`history_num`（触及总数）、`rate`（封板率 0~1）、`open_num`（炸板数）。

### 5. 跌停池

当前跌停的股票列表。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/limit-down?date=2026-03-20"
```

返回结构与炸板池完全一致（`stocks[]` + `stats`）。

**分析思路**：跌停数 > 涨停数是极端弱势信号。跌停池中出现前期强势题材股说明板块退潮。

### 6. 冲刺涨停

涨幅接近涨停但尚未触及涨停价的股票。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/approaching-limit-up?date=2026-03-20"
```

返回结构与炸板池一致。

**分析思路**：冲刺涨停的股票如果最终封板，往往是尾盘资金抢筹信号。

### 7. 涨跌停统计 ⭐

实时涨跌停统计：封板数、触及总数、封板率、炸板数（今日 vs 昨日对比）。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/limit-stats?date=2026-03-20"
```

返回结构：

```json
{
  "data": {
    "limitUp": {
      "today": { "num": 24, "history_num": 43, "rate": 0.558, "open_num": 19 },
      "yesterday": { "num": 28, "history_num": 51, "rate": 0.549, "open_num": 23 }
    },
    "limitDown": {
      "today": { "num": 51, "history_num": 65, "rate": 0.785, "open_num": 14 },
      "yesterday": { "num": 13, "history_num": 19, "rate": 0.684, "open_num": 6 }
    },
    "tradeStatus": { "id": "afternoon_trade", "name": "交易中" },
    "date": "20260323"
  }
}
```

**分析思路**：封板率 > 60% = 强势，< 45% = 弱势；今日 vs 昨日对比判断情绪升降温；跌停数突增是恐慌信号。

### 8. 最强风口 ⭐

按涨停股聚集度排名的板块列表，含 AI 涨停原因分析。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/hot-sectors?date=2026-03-20"
```

返回板块数组，每个板块字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `code` | string | 板块代码 |
| `name` | string | 板块名称 |
| `changePercent` | number | 板块整体涨幅（%） |
| `limitUpNum` | number | 涨停股数量 |
| `continuousPlateNum` | number | 连板股数量 |
| `highBoard` | string | 最高连板描述，如 `"2天2板"` |
| `days` | number | 板块持续活跃天数 |
| `stocks[]` | array | 涨停股列表 |

`stocks[]` 每只股票：`code`, `name`, `changePercent`, `price`, `continueNum`, `highDays`, `reasonType`（简因）, `reasonInfo`（AI 详细分析 100-300字）, `changeTag`, `isSt`, `isNew`。

**分析思路**：`days` 越大题材持续性越强；`continuousPlateNum` > 0 有连板支撑，是主线方向。

### 9. 封板/炸板事件流 ⭐

盘中实时封板/炸板事件流，精确到秒级。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/limit-events?type=limit_up"
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/limit-events?type=limit_down"
```

type: `limit_up`（默认）或 `limit_down`。无需传 `date`，返回当日盘中实时数据。

返回 `{ events[], total }`。数组按 `time` **倒序**（最新在前），通常数百条。

```json
{
  "code": "002896", "name": "中大力德",
  "type": "LIMIT_BACK",
  "orderVolume": "124000.000", "orderAmount": "9548000.0",
  "turnover": "725580960.0", "time": 1774247310
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `code`, `name` | string | 股票代码/名称 |
| `type` | string | `"LIMIT_BACK"` = 封板; `"LIMIT_FAILED"` = 炸板 |
| `orderVolume` | string | 封单量（股）。**字符串**。炸板时为 `"0"` |
| `orderAmount` | string | 封单金额（元），字符串 |
| `turnover` | string | 累计成交额（元），字符串 |
| `time` | number | Unix 时间戳（秒） |

**重要特征**：
- 数值字段（`orderVolume`、`orderAmount`、`turnover`）均为**字符串类型**
- 同一股票反复出现：`LIMIT_BACK` → `LIMIT_FAILED` 交替
- 最终事件为 `LIMIT_BACK` = 收盘封板，`LIMIT_FAILED` = 最终炸板

**分析思路**：按股票分组统计封板 vs 炸板次数得出"封板成功率"；封/炸 > 10次说明多空极度分裂；一封到底零炸板的是最强标的。

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
- A 股交易时间：9:15-15:00（北京时间）
- 查询当日数据前建议先用交易日历确认是否为交易日
