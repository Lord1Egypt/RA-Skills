# `irm_qa_sh` 接口文档

## 接口说明

- 中文说明：上证E互动
- 动态方法：`pro.irm_qa_sh(...)`
- 默认时间字段：无
- 典型过滤参数：`ann_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`ts_code`, `name`, `trade_date`, `q`, `a`, `pub_time`

## 调用示例

```python
df = pro.irm_qa_sh(
    ann_date="",
    start_date="",
    end_date="",
    fields="ts_code,name,trade_date,q,a,pub_time",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```

## 备注

接口有频率限制：每分钟最多访问3次，每小时最多访问10次。
