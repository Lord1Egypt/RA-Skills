# `dc_hot` 接口文档

## 接口说明

- 中文说明：东方财富热榜
- 动态方法：`pro.dc_hot(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`trade_date`, `data_type`, `ts_code`, `ts_name`, `rank`, `pct_change`, `current_price`, `rank_time`

## 调用示例

```python
df = pro.dc_hot(
    trade_date="",
    start_date="",
    end_date="",
    fields="trade_date,data_type,ts_code,ts_name,rank,pct_change,current_price,rank_time",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
