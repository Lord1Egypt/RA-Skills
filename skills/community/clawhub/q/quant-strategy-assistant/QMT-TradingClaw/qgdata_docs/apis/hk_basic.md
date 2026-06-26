# `hk_basic` 接口文档

## 接口说明

- 中文说明：港股列表
- 动态方法：`pro.hk_basic(...)`
- 默认时间字段：`无`
- 典型过滤参数：无
- 主要字段：`ts_code, name, fullname, enname, cn_spell, market, list_status, list_date`

## 调用示例

```python
df = pro.hk_basic(
    fields="ts_code,name,fullname,enname,cn_spell,market,list_status,list_date",
    order_by="ts_code",
    sort="desc",
    limit=50,
)
```
