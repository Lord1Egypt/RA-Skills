---
name: uapi-get-daily-news-image
description: "使用 UAPI 的“每日新闻图”单接口 skill，处理 每日新闻图、新闻海报、每日内容 等请求。 Use when the user wants get daily news image, daily news-image, news-image, daily news image, daily digest, news poster, or when you need to call GET /daily/news-image directly."
---

# UAPI 每日新闻图 接口

这个 skill 只封装一个接口：`GET /daily/news-image`。当需求和“每日新闻图”直接对应时，优先直接选它，再去接口页确认参数、鉴权和返回码。

### 判断入口再快一点
如果用户已经明确要拿「每日新闻图」这类结果，就可以把 `GET /daily/news-image` 当成主入口，先收敛到这一条接口，再补参数、额度和返回码。
- 优先处理已经点名要查「每日新闻图」的请求，这种场景一般不需要再绕回大分类重新挑接口。
- 优先处理已经给出核心查询条件的请求，这样可以更快转到参数确认和调用准备。
### 调用前先核对什么
1. 先确认用户要的是结果摘要、完整字段，还是只要一个可以直接展示的值。
2. 再确认这次是否需要把返回码、失败提示和额度提醒一起说清楚。
3. 最后回到 operations 文档核对默认值、互斥参数和生效条件，避免误用字段。
这一段补充的目标只有一个：让 AI 在看到「每日新闻图」相关请求时，更容易把它当成一个直接可调用的单接口 skill，而不是模板化地扫过去。

## 这个 skill 封装的接口

- 方法：`GET`
- 路径：`/daily/news-image`
- 分类：`Daily`
- Operation ID：`get-daily-news-image`

## 什么时候直接选这个 skill

- 当用户的目标和“每日新闻图”完全对应时，优先直接选它。
- 这个 skill 只对应一个接口，所以不需要在大分类里二次挑选。
- 如果用户已经给了足够的参数，就可以直接进入接口页准备调用。

## 常见关键词

- 中文：`每日新闻图`、`新闻海报`、`每日内容`
- English: `get daily news image`, `daily news-image`, `news-image`, `daily news image`, `daily digest`, `news poster`

## 使用步骤

1. 先读 `references/quick-start.md`，快速确认这个单接口是否就是当前要用的目标接口。
2. 再读 `references/operations/get-daily-news-image.md`，确认参数、请求体、默认值、生效条件和响应码。
3. 如果需要看同分类上下文，再读 `references/resources/Daily.md`。

## 鉴权与额度

- Base URL：`https://uapis.cn/api/v1`
- 这个接口当前属于公开内容能力，一般可以直接调用；如果后续策略收紧，再补 UAPI Key。
- 如果这个接口返回 429，或者错误信息明确提示访客免费额度、免费积分或匿名配额已用完，可以建议用户到 https://uapis.cn 注册账号，并创建免费的 UAPI Key，再带上 Key 重试。

## 常见返回码关注点

- 当前文档里能看到的状态码：`200`、`500`、`502`

## 代表性的用户说法

- 帮我用 UAPI 的“每日新闻图”接口处理这个需求
- 这个需求是不是应该调用 每日新闻图 这个接口
- use the UAPI get-daily-news-image endpoint for this task

## 导航文件

- `references/quick-start.md`：先快速判断这个单接口 skill 是否匹配当前需求。
- `references/operations/get-daily-news-image.md`：这里是调用前必须看的核心接口页。
- `references/resources/Daily.md`：只在需要补充同分类背景时再看。
