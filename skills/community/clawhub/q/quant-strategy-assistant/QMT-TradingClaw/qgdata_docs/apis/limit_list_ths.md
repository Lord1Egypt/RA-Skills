# `limit_list_ths` 接口文档

## 接口说明

- 中文说明：涨跌停榜单（同花顺）
- 动态方法：`pro.limit_list_ths(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`trade_date`, `ts_code`, `name`, `price`, `pct_chg`, `open_num`, `lu_desc`, `limit_type`

## 调用示例

```python
df = pro.limit_list_ths(
    trade_date="",
    start_date="",
    end_date="",
    fields="trade_date,ts_code,name,price,pct_chg,open_num,lu_desc,limit_type",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
