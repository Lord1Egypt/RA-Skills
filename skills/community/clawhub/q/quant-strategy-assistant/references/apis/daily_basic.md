# `daily_basic` 接口文档

## 接口说明

- 中文说明：每日指标
- 动态方法：`pro.daily_basic(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`ts_code`(必填), `trade_date`, `start_date`(必填), `end_date`
- 主要字段：`ts_code`, `trade_date`, `close`, `turnover_rate`, `turnover_rate_f`, `volume_ratio`, `pe`, `pe_ttm`

## 调用示例

```python
df = pro.daily_basic(
    ts_code="",
    trade_date="",
    start_date="",
    end_date="",
    fields="ts_code,trade_date,close,turnover_rate,turnover_rate_f,volume_ratio,pe,pe_ttm",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
