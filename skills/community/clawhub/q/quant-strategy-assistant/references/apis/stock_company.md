# `stock_company` 接口文档

## 接口说明

- 中文说明：上市公司基本信息
- 动态方法：`pro.stock_company(...)`
- 默认时间字段：`setup_date`
- 典型过滤参数：`exchange`
- 主要字段：`ts_code`, `com_name`, `com_id`, `exchange`, `chairman`, `manager`, `secretary`, `reg_capital`

## 调用示例

```python
df = pro.stock_company(
    exchange="",
    fields="ts_code,com_name,com_id,exchange,chairman,manager,secretary,reg_capital",
    order_by="setup_date",
    sort="desc",
    limit=50,
)
```
