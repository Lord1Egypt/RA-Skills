# `cctv_news` 接口文档

## 接口说明

- 中文说明：新闻联播
- 动态方法：`pro.cctv_news(...)`
- 默认时间字段：`date`
- 典型过滤参数：`date`(必填), `start_date`(必填), `end_date`
- 主要字段：`date`, `title`, `content`

## 调用示例

```python
df = pro.cctv_news(
    date="",
    start_date="",
    end_date="",
    fields="date,title,content",
    order_by="date",
    sort="desc",
    limit=50,
)
```
