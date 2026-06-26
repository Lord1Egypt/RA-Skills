# `hibor` 接口文档

## 接口说明

- 中文说明：Hibor利率
- 动态方法：`pro.hibor(...)`
- 默认时间字段：`date`
- 典型过滤参数：`start_date`(必填), `end_date`
- 主要字段：`date`, `on`, `1w`, `2w`, `1m`, `2m`, `3m`, `6m`

## 调用示例

```python
df = pro.hibor(
    start_date="",
    end_date="",
    fields="date,on,1w,2w,1m,2m,3m,6m",
    order_by="date",
    sort="desc",
    limit=50,
)
```

## 备注

该接口已停用。2024年后无数据，暂不抓取。
