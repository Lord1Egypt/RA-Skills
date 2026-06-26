# `new_share` 接口文档

## 接口说明

- 中文说明：IPO新股列表
- 动态方法：`pro.new_share(...)`
- 默认时间字段：`ipo_date`
- 典型过滤参数：`start_date`, `end_date`
- 主要字段：`ts_code`, `sub_code`, `name`, `ipo_date`, `issue_date`, `amount`, `market_amount`, `price`

## 调用示例

```python
df = pro.new_share(
    start_date="",
    end_date="",
    fields="ts_code,sub_code,name,ipo_date,issue_date,amount,market_amount,price",
    order_by="ipo_date",
    sort="desc",
    limit=50,
)
```
