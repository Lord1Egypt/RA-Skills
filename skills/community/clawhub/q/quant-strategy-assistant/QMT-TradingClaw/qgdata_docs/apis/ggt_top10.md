# `ggt_top10` 接口文档

## 接口说明

- 中文说明：港股通十大成交股
- 动态方法：`pro.ggt_top10(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`ts_code`, `trade_date`(必填), `start_date`(必填), `end_date`, `market_type`
- 主要字段：`trade_date`, `ts_code`, `name`, `close`, `p_change`, `rank`, `market_type`, `amount`

## 调用示例

```python
df = pro.ggt_top10(
    ts_code="",
    trade_date="",
    start_date="",
    end_date="",
    market_type="",
    fields="trade_date,ts_code,name,close,p_change,rank,market_type,amount",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
