---
name: wudao-market
version: "1.0.0"
description: "悟道 · A股行情数据：股票搜索、K线、分时、排行榜、市场概况、交易日历。Use when: user asks about A股, stock search, K-line charts, minute data, stock rankings, market overview, trading calendar, or basic A-share market data. NOT for: limit-up board analysis, capital flow, sector rotation, or news intelligence."
metadata:
  {
    "openclaw":
      {
        "emoji": "📈",
        "requires": { "env": ["LB_API_KEY", "LB_API_BASE"] },
      },
  }
---

# 悟道 · A股行情数据

提供 6 个 A 股基础行情接口：股票搜索、K线、分时、排行榜、市场概况、交易日历。

## Instructions for the hosting agent

1. **环境变量**：若缺少 `LB_API_KEY` 或 `LB_API_BASE`，先提示用户按下方 **Setup** 配置，不要猜测 Base URL。
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

### 1. 股票搜索

按名称、代码、行业、拼音搜索股票。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/search?query=茅台&limit=10"
```

参数：`query*`（搜索词，支持名称/代码/行业/拼音首字母）, `limit`（最大返回数，默认20，上限50）。

返回 `{ items[], total }`。每只股票字段：`ts_code`（如 `600519.SH`）, `symbol`（如 `600519`）, `name`, `area`（地区）, `industry`（行业）, `market`（主板/创业板/科创板）, `list_status`（L=上市）, `list_date`（上市日期 YYYYMMDD）。

### 2. K线数据

获取合并的历史+实时K线。代码格式：`600519` 或 `600519.SH`。支持个股和指数（如 `000001.SH` 上证指数）。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/kline/600519?days=30"
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/kline/600519?days=60&endDate=2026-03-20"
```

参数：`code*`（路径参数）, `days`（K线天数，默认15）, `endDate`（截止日期）。

返回 K 线数组，每根 K 线字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `date` | string | `YYYYMMDD` |
| `open` | number | 开盘价 |
| `high` | number | 最高价 |
| `low` | number | 最低价 |
| `close` | number | 收盘价 |
| `volume` | number | 成交量（股） |
| `amount` | number | 成交额（元） |
| `pre_close` | number | 昨收价（部分数据源可能缺失） |
| `change` | number | 涨跌额 |
| `pct_chg` | number | 涨跌幅（%） |

**注意**：盘中「今日」K线来自实时行情合并结果，可能缺少 `pre_close`/`change`/`pct_chg`。

### 3. 分时数据

分钟级分时数据，来自实时行情接口。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/minute/600519?ndays=1"
```

参数：`code*`（路径参数）, `ndays`（天数，默认1）。

返回接口原始格式。核心数据在 `data.trends` 数组中，每条是**逗号分隔的字符串**（非 JSON 对象）：

```
"2026-03-20 09:31,1800.00,1805.50,1810.00,1798.00,1234,22300000.00,1803.20"
```

字段顺序：`时间, 开盘, 最新价, 最高, 最低, 成交量(手), 成交额, 均价`。解析时需 `split(',')` 并 `parseFloat`。

`data.prePrice` 为昨收价，可用于计算涨跌幅。

### 4. 股票排行

多维度股票排行榜。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/rank?type=gainers&market=all&limit=20"
```

参数：
- `type`：`gainers`（涨幅）, `losers`（跌幅）, `volume`, `turnover_rate`, `amount`, `gainers_Nd`/`losers_Nd`（N=3/5/10/20日涨跌幅）, `intraday_drawdown`, `intraday_profit`, `overnight_drawdown`, `overnight_profit`
- `market`：`all`（默认）, `main`, `gem`, `star`
- `limit`：默认50，上限200

返回排行数组，每只股票字段：`rank`, `code`, `name`, `price`（收盘价）, `changePercent`（涨跌幅%）, `amount`（成交额，元）, `turnoverRate`（换手率，可能为 null）, `high`, `low`, `open`, `preClose`, `amplitude`（振幅%）, `volumeRatio`。

N 日排行额外返回 `metricValue`（N日累计涨跌幅%），但不含 `high`/`low` 等日内字段。

### 5. 市场概况

每日市场总览，判断大盘强弱的核心数据。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/market-overview?date=2026-03-20"
```

参数：`date*`（YYYY-MM-DD）。

返回字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| `date` | string | YYYY-MM-DD |
| `rise_count` | number | 上涨家数 |
| `fall_count` | number | 下跌家数 |
| `limit_up_count` | number | 涨停家数 |
| `limit_down_count` | number | 跌停家数 |
| `limit_up_broken_count` | number | 炸板家数 |
| `limit_up_broken_ratio` | number | 炸板率 |
| `yesterday_limit_up_avg_pcp` | number | 昨日涨停股今日平均涨幅（衡量接力意愿） |
| `market_temperature` | number | 市场温度（综合情绪指标） |

**分析思路**：`rise_count` vs `fall_count` 判断多空力量；`yesterday_limit_up_avg_pcp` > 0 说明市场有赚钱效应；`market_temperature` 越高市场越活跃。

### 6. 交易日历

查询某天是否为交易日。

```bash
curl -s -H "Authorization: Bearer $LB_API_KEY" "$LB_API_BASE/trading-calendar?date=2026-03-20"
```

参数：`date*`（YYYY-MM-DD 或 YYYYMMDD）。

返回：`{ date, isTradingDay: true/false, pretrade_date: "YYYYMMDD" }`。`pretrade_date` 为前一个交易日。

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

- 日期格式：大多数接口同时支持 `YYYY-MM-DD` 和 `YYYYMMDD`
- 股票代码：6 位数字（`600519`）或完整代码（`600519.SH`）
- A 股交易时间：9:15-15:00（北京时间），K 线盘中每 9 秒更新
- 查询当日数据前建议先用交易日历确认是否为交易日
