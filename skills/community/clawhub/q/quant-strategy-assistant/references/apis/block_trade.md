# `block_trade` 接口文档

## 接口说明

- 中文说明：大宗交易
- 动态方法：`pro.block_trade(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：无
- 主要字段：`ts_code`, `trade_date`, `price`, `vol`, `amount`, `buyer`, `seller`

## 调用示例

```python
df = pro.block_trade(
    fields="ts_code,trade_date,price,vol,amount,buyer,seller",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
