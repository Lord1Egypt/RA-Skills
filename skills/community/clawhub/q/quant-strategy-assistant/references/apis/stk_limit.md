# `stk_limit` 接口文档

## 接口说明

- 中文说明：每日涨跌停价格
- 动态方法：`pro.stk_limit(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`ts_code`(必填), `trade_date`, `start_date`(必填), `end_date`
- 主要字段：`trade_date`, `ts_code`, `pre_close`, `up_limit`, `down_limit`

## 调用示例

```python
df = pro.stk_limit(
    ts_code="",
    trade_date="",
    start_date="",
    end_date="",
    fields="trade_date,ts_code,pre_close,up_limit,down_limit",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
