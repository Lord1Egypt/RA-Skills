# `shibor_quote` 接口文档

## 接口说明

- 中文说明：Shibor报价数据
- 动态方法：`pro.shibor_quote(...)`
- 默认时间字段：`date`
- 典型过滤参数：`date`(必填), `start_date`(必填), `end_date`
- 主要字段：`date`, `bank`, `on_b`, `on_a`, `1w_b`, `1w_a`, `2w_b`, `2w_a`

## 调用示例

```python
df = pro.shibor_quote(
    date="",
    start_date="",
    end_date="",
    fields="date,bank,on_b,on_a,1w_b,1w_a,2w_b,2w_a",
    order_by="date",
    sort="desc",
    limit=50,
)
```
