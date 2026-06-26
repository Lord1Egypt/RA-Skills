# `cn_m` 接口文档

## 接口说明

- 中文说明：货币供应量
- 动态方法：`pro.cn_m(...)`
- 默认时间字段：无
- 典型过滤参数：无
- 主要字段：`month`, `m0`, `m0_yoy`, `m0_mom`, `m1`, `m1_yoy`, `m1_mom`, `m2`

## 调用示例

```python
df = pro.cn_m(
    fields="month,m0,m0_yoy,m0_mom,m1,m1_yoy,m1_mom,m2",
    order_by="month",
    sort="desc",
    limit=50,
)
```
