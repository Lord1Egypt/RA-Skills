# `cn_cpi` 接口文档

## 接口说明

- 中文说明：居民消费价格指数(CPI)
- 动态方法：`pro.cn_cpi(...)`
- 默认时间字段：无
- 典型过滤参数：无
- 主要字段：`month`, `nt_val`, `nt_yoy`, `nt_mom`, `nt_accu`, `town_val`, `town_yoy`, `town_mom`

## 调用示例

```python
df = pro.cn_cpi(
    fields="month,nt_val,nt_yoy,nt_mom,nt_accu,town_val,town_yoy,town_mom",
    order_by="month",
    sort="desc",
    limit=50,
)
```
