# `report_rc` 接口文档

## 接口说明

- 中文说明：卖方盈利预测数据
- 动态方法：`pro.report_rc(...)`
- 默认时间字段：`report_date`
- 典型过滤参数：无
- 主要字段：`ts_code`, `name`, `report_date`, `report_title`, `report_type`, `classify`, `org_name`, `author_name`

## 调用示例

```python
df = pro.report_rc(
    fields="ts_code,name,report_date,report_title,report_type,classify,org_name,author_name",
    order_by="report_date",
    sort="desc",
    limit=50,
)
```
