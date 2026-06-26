# `kpl_concept_cons` 接口文档

## 接口说明

- 中文说明：开盘啦题材成分
- 动态方法：`pro.kpl_concept_cons(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`ts_code`, `name`, `con_name`, `con_code`, `trade_date`, `desc`, `hot_num`

## 调用示例

```python
df = pro.kpl_concept_cons(
    trade_date="",
    start_date="",
    end_date="",
    fields="ts_code,name,con_name,con_code,trade_date,desc,hot_num",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```
