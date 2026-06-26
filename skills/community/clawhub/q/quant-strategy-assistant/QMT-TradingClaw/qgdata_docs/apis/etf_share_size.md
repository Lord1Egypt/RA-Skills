# `etf_share_size` 接口文档

## 接口说明

- 中文说明：ETF份额规模
- 动态方法：`pro.etf_share_size(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`trade_date`, `ts_code`, `etf_name`, `total_share`, `total_size`, `nav`, `close`, `exchange`

## 调用示例

```python
df = pro.etf_share_size(
    trade_date="",
    start_date="",
    end_date="",
    fields="trade_date,ts_code,etf_name,total_share,total_size,nav,close,exchange",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
