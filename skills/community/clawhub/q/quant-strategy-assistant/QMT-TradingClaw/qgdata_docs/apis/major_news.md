# `major_news` 接口文档

## 接口说明

- 中文说明：新闻通讯
- 动态方法：`pro.major_news(...)`
- 默认时间字段：无
- 典型过滤参数：`start_date`(必填, 格式 YYYYMMDD HH:mm:ss), `end_date`, `src`(必填)
- 主要字段：`title`, `content`, `pub_time`, `src`

## 调用示例

```python
df = pro.major_news(
    start_date="",
    end_date="",
    src="",
    fields="title,content,pub_time,src",
    order_by="pub_time",
    sort="desc",
    limit=50,
)
```

## 备注

`src` 参数可选值：`新华网`, `凤凰财经`, `同花顺`, `新浪财经`, `华尔街见闻`, `中证网`, `财新网`, `第一财经`, `财联社`。
