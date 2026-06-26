# `ci_daily` 接口文档

## 接口说明

- 中文说明：中信行业指数行情
- 动态方法：`pro.ci_daily(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`ts_code`, `trade_date`, `close`, `open`, `high`, `low`, `pre_close`, `change`, `pct_chg`, `vol`, `amount`

## 调用示例

```python
df = pro.ci_daily(
    trade_date="20260310",
    fields="ts_code,trade_date,close,open,high,low,pct_chg,vol,amount",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
