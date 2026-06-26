# `fund_share` 接口文档

## 接口说明

- 中文说明：基金规模
- 动态方法：`pro.fund_share(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填)、`start_date`(必填)、`end_date`
- 主要字段：`ts_code, trade_date, fd_share`

## 调用示例

```python
df = pro.fund_share(
    trade_date="",
    start_date="",
    end_date="",
    fields="ts_code,trade_date,fd_share",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
