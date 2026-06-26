# `margin_secs` 接口文档

## 接口说明

- 中文说明：融资融券标的（盘前更新）
- 动态方法：`pro.margin_secs(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`trade_date`, `ts_code`, `name`, `exchange`

## 调用示例

```python
df = pro.margin_secs(
    trade_date="",
    start_date="",
    end_date="",
    fields="trade_date,ts_code,name,exchange",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
