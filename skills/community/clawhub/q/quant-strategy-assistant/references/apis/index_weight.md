# `index_weight` 接口文档

## 接口说明

- 中文说明：指数成分和权重
- 动态方法：`pro.index_weight(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`index_code`(必填), `start_date`(必填), `end_date`
- 主要字段：`index_code`, `con_code`, `trade_date`, `weight`

## 调用示例

```python
df = pro.index_weight(
    index_code="399300.SZ",
    start_date="20260101",
    end_date="20260310",
    fields="index_code,con_code,trade_date,weight",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
