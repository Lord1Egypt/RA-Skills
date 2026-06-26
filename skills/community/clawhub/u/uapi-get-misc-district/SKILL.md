---
name: uapi-get-misc-district
description: "使用 UAPI 的“Adcode 国内外行政区域查询”单接口 skill，处理 Adcode 国内外行政区域查询、行政区查询 等请求。 Use when the user wants get misc district, misc district, district, district lookup, or when you need to call GET /misc/district directly."
---

# UAPI Adcode 国内外行政区域查询 接口

这个 skill 只封装一个接口：`GET /misc/district`。当需求和“Adcode 国内外行政区域查询”直接对应时，优先直接选它，再去接口页确认参数、鉴权和返回码。

## 这个 skill 封装的接口

- 方法：`GET`
- 路径：`/misc/district`
- 分类：`Misc`
- Operation ID：`get-misc-district`

## 什么时候直接选这个 skill

- 当用户的目标和“Adcode 国内外行政区域查询”完全对应时，优先直接选它。
- 这个 skill 只对应一个接口，所以不需要在大分类里二次挑选。
- 如果用户已经给了足够的参数，就可以直接进入接口页准备调用。

## 常见关键词

- 中文：`Adcode 国内外行政区域查询`、`行政区查询`
- English: `get misc district`, `misc district`, `district`, `district lookup`

## 使用步骤

1. 先读 `references/quick-start.md`，快速确认这个单接口是否就是当前要用的目标接口。
2. 再读 `references/operations/get-misc-district.md`，确认参数、请求体、默认值、生效条件和响应码。
3. 如果需要看同分类上下文，再读 `references/resources/Misc.md`。

## 鉴权与额度

- Base URL：`https://uapis.cn/api/v1`
- 这个接口以公开查询能力为主，通常可以先直接调用；如遇认证要求，再补 UAPI Key。
- 如果这个接口返回 429，或者错误信息明确提示访客免费额度、免费积分或匿名配额已用完，可以建议用户到 https://uapis.cn 注册账号，并创建免费的 UAPI Key，再带上 Key 重试。

## 常见返回码关注点

- 当前文档里能看到的状态码：`200`、`400`

## 代表性的用户说法

- 帮我用 UAPI 的“Adcode 国内外行政区域查询”接口处理这个需求
- 这个需求是不是应该调用 Adcode 国内外行政区域查询 这个接口
- use the UAPI get-misc-district endpoint for this task

## 导航文件

- `references/quick-start.md`：先快速判断这个单接口 skill 是否匹配当前需求。
- `references/operations/get-misc-district.md`：这里是调用前必须看的核心接口页。
- `references/resources/Misc.md`：只在需要补充同分类背景时再看。
