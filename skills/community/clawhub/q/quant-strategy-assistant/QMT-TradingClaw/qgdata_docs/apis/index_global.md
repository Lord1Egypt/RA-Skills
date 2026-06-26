# `index_global` 接口文档

## 接口说明

- 中文说明：国际指数
- 动态方法：`pro.index_global(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`ts_code`, `trade_date`, `open`, `close`, `high`, `low`, `pre_close`, `change`, `pct_chg`, `swing`, `vol`, `amount`

## 调用示例

```python
df = pro.index_global(
    trade_date="20260310",
    fields="ts_code,trade_date,open,close,high,low,pct_chg,swing",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
