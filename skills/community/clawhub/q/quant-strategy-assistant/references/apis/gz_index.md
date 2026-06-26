# `gz_index` 接口文档

## 接口说明

- 中文说明：广州民间借贷利率
- 动态方法：`pro.gz_index(...)`
- 默认时间字段：`date`
- 典型过滤参数：`start_date`(必填), `end_date`
- 主要字段：`date`, `d10_rate`, `m1_rate`, `m3_rate`, `m6_rate`, `m12_rate`, `long_rate`

## 调用示例

```python
df = pro.gz_index(
    start_date="",
    end_date="",
    fields="date,d10_rate,m1_rate,m3_rate,m6_rate,m12_rate,long_rate",
    order_by="date",
    sort="desc",
    limit=50,
)
```

## 备注

该接口已停用。2024年后无数据，暂不抓取。
