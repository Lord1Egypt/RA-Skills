# `etf_basic` 接口文档

## 接口说明

- 中文说明：ETF基础信息
- 动态方法：`pro.etf_basic(...)`
- 默认时间字段：`list_date`
- 典型过滤参数：无
- 主要字段：`ts_code`, `csname`, `extname`, `cname`, `index_code`, `index_name`, `setup_date`, `list_date`

## 调用示例

```python
df = pro.etf_basic(
    fields="ts_code,csname,extname,cname,index_code,index_name,setup_date,list_date",
    order_by="list_date",
    sort="desc",
    limit=50,
)
```
