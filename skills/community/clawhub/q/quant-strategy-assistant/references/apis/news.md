# `news` 接口文档

## 接口说明

- 中文说明：新闻快讯
- 动态方法：`pro.news(...)`
- 默认时间字段：`datetime`
- 典型过滤参数：`start_date`(必填, 格式 YYYYMMDD HH:mm:ss), `end_date`, `src`(必填)
- 主要字段：`datetime`, `content`, `title`, `channels`, `src`

## 调用示例

```python
df = pro.news(
    start_date="",
    end_date="",
    src="",
    fields="datetime,content,title,channels,src",
    order_by="datetime",
    sort="desc",
    limit=50,
)
```

## 备注

`src` 参数可选值：`sina`, `wallstreetcn`, `10jqka`, `eastmoney`, `yuncaijing`, `fenghuang`, `jinrongjie`, `cls`, `yicai`。
