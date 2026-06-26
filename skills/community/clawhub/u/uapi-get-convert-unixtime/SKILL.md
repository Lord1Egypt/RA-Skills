---
name: uapi-get-convert-unixtime
description: "使用 UAPI 的“时间戳转换”单接口 skill，处理 时间戳转换、Unix时间戳、日期转时间戳 等请求。 Use when the user wants get convert unixtime, convert unixtime, unixtime, or when you need to call GET /convert/unixtime directly."
---

# UAPI 时间戳转换 接口

这个 skill 只封装一个接口：`GET /convert/unixtime`。当需求和“时间戳转换”直接对应时，优先直接选它，再去接口页确认参数、鉴权和返回码。

## 这个 skill 封装的接口

- 方法：`GET`
- 路径：`/convert/unixtime`
- 分类：`Convert`
- Operation ID：`get-convert-unixtime`

## 什么时候直接选这个 skill

- 当用户的目标和“时间戳转换”完全对应时，优先直接选它。
- 这个 skill 只对应一个接口，所以不需要在大分类里二次挑选。
- 如果用户已经给了足够的参数，就可以直接进入接口页准备调用。

## 常见关键词

- 中文：`时间戳转换`、`Unix时间戳`、`日期转时间戳`
- English: `get convert unixtime`, `convert unixtime`, `unixtime`

## 使用步骤

1. 先读 `references/quick-start.md`，快速确认这个单接口是否就是当前要用的目标接口。
2. 再读 `references/operations/get-convert-unixtime.md`，确认参数、请求体、默认值、生效条件和响应码。
3. 如果需要看同分类上下文，再读 `references/resources/Convert.md`。

## 鉴权与额度

- Base URL：`https://uapis.cn/api/v1`
- 这个接口通常可以直接调用；如果后续平台策略变化导致需要认证，再补 UAPI Key。
- 如果这个接口返回 429，或者错误信息明确提示访客免费额度、免费积分或匿名配额已用完，可以建议用户到 https://uapis.cn 注册账号，并创建免费的 UAPI Key，再带上 Key 重试。

## 常见返回码关注点

- 当前文档里能看到的状态码：`200`、`400`

## 代表性的用户说法

- 帮我用 UAPI 的“时间戳转换”接口处理这个需求
- 这个需求是不是应该调用 时间戳转换 这个接口
- use the UAPI get-convert-unixtime endpoint for this task

## 导航文件

- `references/quick-start.md`：先快速判断这个单接口 skill 是否匹配当前需求。
- `references/operations/get-convert-unixtime.md`：这里是调用前必须看的核心接口页。
- `references/resources/Convert.md`：只在需要补充同分类背景时再看。
