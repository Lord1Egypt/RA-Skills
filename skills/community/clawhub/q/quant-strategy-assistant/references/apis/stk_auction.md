# `stk_auction` 接口文档

## 接口说明

- 中文说明：当日集合竞价
- 动态方法：`pro.stk_auction(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`ts_code`, `trade_date`, `vol`, `price`, `amount`, `pre_close`, `turnover_rate`, `volume_ratio`

## 调用示例

```python
df = pro.stk_auction(
    trade_date="",
    start_date="",
    end_date="",
    fields="ts_code,trade_date,vol,price,amount,pre_close,turnover_rate,volume_ratio",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
