# `dc_daily` 接口文档

## 接口说明

- 中文说明：东财概念板块行情
- 动态方法：`pro.dc_daily(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`trade_date`, `ts_code`, `name`, `close`, `pct_change`, `turnover_rate`, `amount`, `l_sell`

## 调用示例

```python
df = pro.dc_daily(
    trade_date="",
    start_date="",
    end_date="",
    fields="trade_date,ts_code,name,close,pct_change,turnover_rate,amount,l_sell",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
