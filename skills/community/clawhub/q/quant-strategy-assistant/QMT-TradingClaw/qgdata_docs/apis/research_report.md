# `research_report` 接口文档

## 接口说明

- 中文说明：券商研究报告
- 动态方法：`pro.research_report(...)`
- 默认时间字段：`trade_date`
- 典型过滤参数：`trade_date`(必填), `start_date`(必填), `end_date`
- 主要字段：`trade_date`, `abstr`, `title`, `report_type`, `author`, `name`, `ts_code`, `inst_csname`

## 调用示例

```python
df = pro.research_report(
    trade_date="",
    start_date="",
    end_date="",
    fields="trade_date,abstr,title,report_type,author,name,ts_code,inst_csname,ind_name,url",
    order_by="trade_date",
    sort="desc",
    limit=50,
)
```

## 备注

每天只能调用5次接口。
