# `ccass_hold_detail` 接口文档

## 接口说明

- 中文说明：中央结算系统持股明细
- 动态方法：`pro.ccass_hold_detail(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：无
- 主要字段：`trade_date`, `ts_code`, `name`, `col_participant_id`, `col_participant_name`, `col_shareholding`, `col_shareholding_percent`

## 调用示例

```python
df = pro.ccass_hold_detail(
    fields="trade_date,ts_code,name,col_participant_id,col_participant_name,col_shareholding,col_shareholding_percent",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```

## 备注

- 该接口为分表查询，必须同时传 `freq` 与 `ts_code`
- 建议始终传 `start_date/end_date` 控制查询范围
- 当时间字段为 `trade_time` 时，服务端会自动补齐交易时段边界
