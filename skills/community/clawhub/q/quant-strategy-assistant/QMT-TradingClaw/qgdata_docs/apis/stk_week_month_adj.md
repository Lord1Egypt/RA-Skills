# `stk_week_month_adj` 接口文档

## 接口说明

- 中文说明：股票周/月线行情(复权--每日更新)
- 动态方法：`pro.stk_week_month_adj(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`ts_code`, `trade_date`(必填), `start_date`(必填), `end_date`, `freq`(必填)
- 主要字段：`ts_code`, `trade_date`, `end_date`, `freq`, `open`, `high`, `low`, `close`

## 调用示例

```python
df = pro.stk_week_month_adj(
    ts_code="",
    trade_date="",
    start_date="",
    end_date="",
    freq="",
    fields="ts_code,trade_date,end_date,freq,open,high,low,close",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
