# `etf_index` 接口文档

## 接口说明

- 中文说明：ETF基准指数列表
- 动态方法：`pro.etf_index(...)`
- 默认时间字段：`pub_date`
- 典型过滤参数：无
- 主要字段：`ts_code`, `indx_name`, `indx_csname`, `pub_party_name`, `pub_date`, `base_date`, `bp`, `adj_circle`

## 调用示例

```python
df = pro.etf_index(
    fields="ts_code,indx_name,indx_csname,pub_party_name,pub_date,base_date,bp,adj_circle",
    order_by="pub_date",
    sort="desc",
    limit=50,
)
```
