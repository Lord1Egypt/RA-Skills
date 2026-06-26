# `libor` 接口文档

## 接口说明

- 中文说明：Libor拆借利率
- 动态方法：`pro.libor(...)`
- 默认时间字段：`date`
- 典型过滤参数：`start_date`(必填), `end_date`
- 主要字段：`date`, `d10_rate`, `m1_rate`, `m3_rate`, `m6_rate`, `m12_rate`, `long_rate`

## 调用示例

```python
df = pro.libor(
    start_date="",
    end_date="",
    fields="date,d10_rate,m1_rate,m3_rate,m6_rate,m12_rate,long_rate",
    order_by="date",
    sort="desc",
    limit=50,
)
```

## 备注

该接口已停用。Libor已于2023年6月30日停止发布，该接口不再有新数据。
