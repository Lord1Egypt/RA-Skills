# `shibor` 接口文档

## 接口说明

- 中文说明：Shibor利率数据
- 动态方法：`pro.shibor(...)`
- 默认时间字段：无
- 典型过滤参数：`start_date`(必填), `end_date`
- 主要字段：`date`, `on`, `1w`, `2w`, `1m`, `3m`, `6m`, `9m`

## 调用示例

```python
df = pro.shibor(
    start_date="",
    end_date="",
    fields="date,on,1w,2w,1m,3m,6m,9m",
    order_by="date",
    sort="desc",
    limit=50,
)
```
