# `cn_pmi` 接口文档

## 接口说明

- 中文说明：采购经理人指数(PMI)
- 动态方法：`pro.cn_pmi(...)`
- 默认时间字段：无
- 典型过滤参数：无
- 主要字段：`month`, `pmi010000`, `pmi010100`, `pmi010200`, `pmi010300`, `pmi010400`, `pmi010401`, `pmi010402`

## 调用示例

```python
df = pro.cn_pmi(
    fields="month,pmi010000,pmi010100,pmi010200,pmi010300,pmi010400,pmi010401,pmi010402",
    order_by="month",
    sort="desc",
    limit=50,
)
```
