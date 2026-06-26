# `fund_company` 接口文档

## 接口说明

- 中文说明：基金管理人
- 动态方法：`pro.fund_company(...)`
- 默认时间字段：`无`
- 典型过滤参数：无
- 主要字段：`name, shortname, short_enname, province, city, address, phone, office`

## 调用示例

```python
df = pro.fund_company(
    fields="name,shortname,short_enname,province,city,address,phone,office",
    order_by="name",
    sort="desc",
    limit=50,
)
```
