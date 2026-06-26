# `income` 接口文档

## 接口说明

- 中文说明：利润表
- 动态方法：`pro.income_vip(...)`
- 默认时间字段：`ann_date`
- 典型过滤参数：`ann_date`, `f_ann_date`, `start_date`(必填), `end_date`, `period`, `report_type`, `comp_type`
- 主要字段：`ts_code`, `ann_date`, `f_ann_date`, `end_date`, `report_type`, `comp_type`, `end_type`, `basic_eps`

## 调用示例

```python
df = pro.income_vip(
    ann_date="",
    f_ann_date="",
    start_date="",
    end_date="",
    period="",
    report_type="",
    comp_type="",
    fields="ts_code,ann_date,f_ann_date,end_date,report_type,comp_type,end_type,basic_eps",
    order_by="ann_date",
    sort="desc",
    limit=50,
)
```
