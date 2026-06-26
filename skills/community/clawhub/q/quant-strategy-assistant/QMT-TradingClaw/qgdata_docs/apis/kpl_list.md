# `kpl_list` 接口文档

## 接口说明

- 中文说明：开盘啦榜单数据
- 动态方法：`pro.kpl_list(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`ts_code`, `name`, `trade_date`, `lu_time`, `ld_time`, `open_time`, `last_time`, `lu_desc`

## 调用示例

```python
df = pro.kpl_list(
    trade_date="",
    start_date="",
    end_date="",
    fields="ts_code,name,trade_date,lu_time,ld_time,open_time,last_time,lu_desc",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
