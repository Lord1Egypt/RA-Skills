# A股 API 字段参考

## 个股实时行情 `/api/stock/individual_spot` 常见字段

| item 字段名 | 含义 |
|---|---|
| 最新价 | 当前价格 |
| 涨跌幅 | 相对昨收的涨跌百分比 |
| 涨跌额 | 相对昨收的涨跌绝对值 |
| 成交量 | 当日累计成交量（手） |
| 成交额 | 当日累计成交额（元） |
| 换手率 | 当日换手率（%） |
| 市盈率-动态 | 动态市盈率 |
| 总市值 | 总市值（元） |
| 流通市值 | 流通市值（元） |
| 昨收 | 前一交易日收盘价 |
| 今开 | 今日开盘价 |
| 最高 | 今日最高价 |
| 最低 | 今日最低价 |
| 涨停 | 今日涨停价 |
| 跌停 | 今日跌停价 |

## 龙虎榜 `/api/stock/lhb_detail_em` 字段说明

| 字段 | 含义 |
|---|---|
| rankingDate | 上榜日期 |
| rankingReason | 上榜原因（如"连续3日涨幅偏离值超过20%"） |
| lhbNetBuyAmount | 龙虎榜净买额（元） |
| lhbBuyAmount | 龙虎榜买入总额 |
| lhbSellAmount | 龙虎榜卖出总额 |
| netBuyRatio | 净买额占当日成交额比例 |
| after1d/2d/5d/10d | 上榜后1/2/5/10个交易日涨跌幅 |

## 行业板块 `/api/stock/board_industry_name_em` 字段说明

| 字段 | 含义 |
|---|---|
| rank | 板块涨跌排名 |
| boardName | 板块名称 |
| changePercent | 板块涨跌幅（%） |
| totalMarketCap | 板块总市值 |
| risingCount | 上涨家数 |
| fallingCount | 下跌家数 |
| leadingStock | 领涨股名称 |
| leadingStockChange | 领涨股涨跌幅 |

## 分时行情 `/api/stock/zh_a_hist_min_em` 字段说明

| 字段 | 含义 |
|---|---|
| 时间 | 分钟级时间戳 |
| 开盘 | 该分钟开盘价 |
| 收盘 | 该分钟收盘价（即最新价） |
| 最高 | 该分钟最高价 |
| 最低 | 该分钟最低价 |
| 成交量 | 该分钟成交量（手） |
| 成交额 | 该分钟成交额 |
| adjust | 复权方式：qfq前复权 / hfq后复权 / 空不复权 |
