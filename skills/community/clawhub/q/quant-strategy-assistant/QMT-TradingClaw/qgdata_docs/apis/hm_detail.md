# `hm_detail` 接口文档

## 接口说明

- 中文说明：游资每日明细
- 动态方法：`pro.hm_detail(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`trade_date`, `ts_code`, `ts_name`, `buy_amount`, `sell_amount`, `net_amount`, `hm_name`, `hm_orgs`

## 调用示例

```python
df = pro.hm_detail(
    trade_date="",
    start_date="",
    end_date="",
    fields="trade_date,ts_code,ts_name,buy_amount,sell_amount,net_amount,hm_name,hm_orgs",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
