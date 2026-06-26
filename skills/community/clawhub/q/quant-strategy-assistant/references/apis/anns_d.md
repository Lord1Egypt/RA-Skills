# `anns_d` 接口文档

## 接口说明

- 中文说明：上市公司全量公告
- 动态方法：`pro.anns_d(...)`
- 默认时间字段：无
- 典型过滤参数：`ann_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`ann_date`, `ts_code`, `name`, `title`, `url`, `rec_time`

## 调用示例

```python
df = pro.anns_d(
    ann_date="",
    start_date="",
    end_date="",
    fields="ann_date,ts_code,name,title,url,rec_time",
    order_by="ann_date",
    sort="desc",
    limit=50,
)
```

## 备注

该接口当前未启用，原因：抱歉，您没有接口访问权限。
