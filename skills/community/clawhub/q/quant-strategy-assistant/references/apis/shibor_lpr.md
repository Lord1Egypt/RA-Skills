# `shibor_lpr` 接口文档

## 接口说明

- 中文说明：LPR贷款基础利率
- 动态方法：`pro.shibor_lpr(...)`
- 默认时间字段：`date`
- 典型过滤参数：`start_date`(必填), `end_date`
- 主要字段：`date`, `1y`, `5y`

## 调用示例

```python
df = pro.shibor_lpr(
    start_date="",
    end_date="",
    fields="date,1y,5y",
    order_by="date",
    sort="desc",
    limit=50,
)
```
