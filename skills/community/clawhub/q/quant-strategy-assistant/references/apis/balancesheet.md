# `balancesheet` 接口文档

## 接口说明

- 中文说明：资产负债表
- 动态方法：`pro.balancesheet_vip(...)`
- 默认时间字段：`ann_date`
- 典型过滤参数：`ann_date`, `start_date`(必填), `end_date`, `period`, `report_type`, `comp_type`
- 主要字段：`ts_code`, `ann_date`, `f_ann_date`, `end_date`, `report_type`, `comp_type`, `end_type`, `total_share`

## 调用示例

```python
df = pro.balancesheet_vip(
    ann_date="",
    start_date="",
    end_date="",
    period="",
    report_type="",
    comp_type="",
    fields="ts_code,ann_date,f_ann_date,end_date,report_type,comp_type,end_type,total_share",
    order_by="ann_date",
    sort="desc",
    limit=50,
)
```
