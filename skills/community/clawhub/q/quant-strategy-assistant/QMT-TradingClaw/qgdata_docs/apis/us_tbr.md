# `us_tbr` 接口文档

## 接口说明

- 中文说明：短期国债利率
- 动态方法：`pro.us_tbr(...)`
- 默认时间字段：无
- 典型过滤参数：`start_date`(必填), `end_date`
- 主要字段：`date`, `w4_bd`, `w4_ce`, `w8_bd`, `w8_ce`, `w13_bd`, `w13_ce`, `w17_bd`

## 调用示例

```python
df = pro.us_tbr(
    start_date="",
    end_date="",
    fields="date,w4_bd,w4_ce,w8_bd,w8_ce,w13_bd,w13_ce,w17_bd",
    order_by="date",
    sort="desc",
    limit=50,
)
```
