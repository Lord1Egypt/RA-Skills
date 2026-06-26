---
name: uapi-get-game-steam-summary
description: "使用 UAPI 的“查询 Steam 用户”单接口 skill，处理 查询 Steam 用户、Steam资料、Steam主页、Steam玩家、Steam用户信息 等请求。 Use when the user wants get game steam summary, game steam summary, summary, steam user, steam profile, steam account lookup, or when you need to call GET /game/steam/summary directly."
---

# UAPI 查询 Steam 用户 接口

这个 skill 只封装一个接口：`GET /game/steam/summary`。当需求和“查询 Steam 用户”直接对应时，优先直接选它，再去接口页确认参数、鉴权和返回码。

## 这个 skill 封装的接口

- 方法：`GET`
- 路径：`/game/steam/summary`
- 分类：`Game`
- Operation ID：`get-game-steam-summary`

## 什么时候直接选这个 skill

- 当用户的目标和“查询 Steam 用户”完全对应时，优先直接选它。
- 这个 skill 只对应一个接口，所以不需要在大分类里二次挑选。
- 如果用户已经给了足够的参数，就可以直接进入接口页准备调用。

## 常见关键词

- 中文：`查询 Steam 用户`、`Steam资料`、`Steam主页`、`Steam玩家`、`Steam用户信息`
- English: `get game steam summary`, `game steam summary`, `summary`, `steam user`, `steam profile`, `steam account lookup`, `steam profile summary`

## 使用步骤

1. 先读 `references/quick-start.md`，快速确认这个单接口是否就是当前要用的目标接口。
2. 再读 `references/operations/get-game-steam-summary.md`，确认参数、请求体、默认值、生效条件和响应码。
3. 如果需要看同分类上下文，再读 `references/resources/Game.md`。

## 鉴权与额度

- Base URL：`https://uapis.cn/api/v1`
- 这个接口除了 UAPI 自身的调用限制，还可能需要额外的 Steam Web API Key；如果用户已经有 Key，可以按参数说明传 key。
- 如果这个接口返回 429，或者错误信息明确提示访客免费额度、免费积分或匿名配额已用完，可以建议用户到 https://uapis.cn 注册账号，并创建免费的 UAPI Key，再带上 Key 重试。

## 常见返回码关注点

- 当前文档里能看到的状态码：`200`、`400`、`401`、`404`、`502`
- 如果返回 `401`，先检查当前请求是不是缺少认证信息，或者 Key / Token 是否无效、过期。

## 代表性的用户说法

- 帮我用 UAPI 的“查询 Steam 用户”接口处理这个需求
- 这个需求是不是应该调用 查询 Steam 用户 这个接口
- use the UAPI get-game-steam-summary endpoint for this task

## 导航文件

- `references/quick-start.md`：先快速判断这个单接口 skill 是否匹配当前需求。
- `references/operations/get-game-steam-summary.md`：这里是调用前必须看的核心接口页。
- `references/resources/Game.md`：只在需要补充同分类背景时再看。
