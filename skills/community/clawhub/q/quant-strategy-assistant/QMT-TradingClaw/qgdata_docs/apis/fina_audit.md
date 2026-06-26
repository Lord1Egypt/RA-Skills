# `fina_audit` 接口文档

## 接口说明

- 中文说明：财务审计意见
- 动态方法：`pro.fina_audit_vip(...)`
- 默认时间字段：`ann_date`
- 典型过滤参数：`ann_date`, `start_date`(必填), `end_date`, `period`
- 主要字段：`ts_code`, `ann_date`, `end_date`, `audit_result`, `audit_fees`, `audit_agency`, `audit_sign`

## 调用示例

```python
df = pro.fina_audit_vip(
    ann_date="",
    start_date="",
    end_date="",
    period="",
    fields="ts_code,ann_date,end_date,audit_result,audit_fees,audit_agency,audit_sign",
    order_by="ann_date",
    sort="desc",
    limit=50,
)
```
