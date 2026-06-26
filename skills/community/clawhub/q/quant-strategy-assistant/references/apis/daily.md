# `daily` 接口文档

## 接口说明

- 中文说明：日线行情
- 动态方法：`pro.daily(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`ts_code`(必填), `trade_date`, `start_date`(必填), `end_date`
- 主要字段：`ts_code`, `trade_date`, `open`, `high`, `low`, `close`, `pre_close`, `change`

## 调用示例

```python
df = pro.daily(
    ts_code="",
    trade_date="",
    start_date="",
    end_date="",
    fields="ts_code,trade_date,open,high,low,close,pre_close,change",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
