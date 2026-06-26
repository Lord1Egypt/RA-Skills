# `stock_basic` 接口文档

## 接口说明

- 中文说明：股票基础信息
- 动态方法：`pro.stock_basic(...)`
- 默认时间字段：`list_date`
- 典型过滤参数：无
- 主要字段：`ts_code`, `symbol`, `name`, `area`, `industry`, `fullname`, `enname`, `cnspell`

## 调用示例

```python
df = pro.stock_basic(
    fields="ts_code,symbol,name,area,industry,fullname,enname,cnspell",
    order_by="list_date",
    sort="desc",
    limit=50,
)
```
