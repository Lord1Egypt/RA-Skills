# 数据库表结构参考

## portfolios（投资组合）

| 字段 | 类型 | 说明 |
|---|---|---|
| id | TEXT PK | 组合ID，格式 PTF+8位hex |
| name | TEXT | 组合名称 |
| description | TEXT | 描述 |
| initial_cash | REAL | 初始资金 |
| cash | REAL | 当前现金 |
| created_at | TEXT | 创建时间 |
| updated_at | TEXT | 更新时间 |

## holdings（持仓）

| 字段 | 类型 | 说明 |
|---|---|---|
| id | INTEGER PK | 自增ID |
| portfolio_id | TEXT FK | 所属组合 |
| symbol | TEXT | 标的代码 |
| name | TEXT | 标的名称 |
| quantity | INTEGER | 持仓数量 |
| avg_cost | REAL | 平均成本 |
| market | TEXT | 市场（默认 A） |
| UNIQUE | (portfolio_id, symbol) | |

## orders（订单）

| 字段 | 类型 | 说明 |
|---|---|---|
| id | TEXT PK | 订单ID，格式 ORD+8位hex |
| portfolio_id | TEXT FK | 所属组合 |
| symbol | TEXT | 标的代码 |
| name | TEXT | 标的名称 |
| side | TEXT | buy / sell |
| type | TEXT | limit / market |
| price | REAL | 限价（市价单为 NULL） |
| quantity | INTEGER | 委托数量 |
| filled_quantity | INTEGER | 已成交数量 |
| status | TEXT | pending / partial / filled / cancelled / rejected |
| created_at | TEXT | 创建时间 |
| updated_at | TEXT | 更新时间 |

## trades（成交记录）

| 字段 | 类型 | 说明 |
|---|---|---|
| id | INTEGER PK | 自增ID |
| order_id | TEXT FK | 关联订单 |
| portfolio_id | TEXT FK | 所属组合 |
| symbol | TEXT | 标的代码 |
| name | TEXT | 标的名称 |
| side | TEXT | buy / sell |
| price | REAL | 成交价格 |
| quantity | INTEGER | 成交数量 |
| trade_time | TEXT | 成交时间 |

## market_prices（行情数据）

| 字段 | 类型 | 说明 |
|---|---|---|
| symbol | TEXT PK | 标的代码 |
| name | TEXT | 标的名称 |
| price | REAL | 最新价格 |
| updated_at | TEXT | 更新时间 |

## nav_history（净值历史）

| 字段 | 类型 | 说明 |
|---|---|---|
| id | INTEGER PK | 自增ID |
| portfolio_id | TEXT FK | 所属组合 |
| date | TEXT | 日期 YYYY-MM-DD |
| nav | REAL | 净值 |
| total_value | REAL | 总资产 |
| cash | REAL | 现金 |
| positions_value | REAL | 持仓市值 |
| UNIQUE | (portfolio_id, date) | |
