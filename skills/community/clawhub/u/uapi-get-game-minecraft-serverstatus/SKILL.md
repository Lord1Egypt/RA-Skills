---
name: uapi-get-game-minecraft-serverstatus
description: "使用 UAPI 的“查询 MC 服务器”单接口 skill，处理 查询 MC 服务器、MC服务器状态 等请求。 Use when the user wants get game minecraft serverstatus, game minecraft serverstatus, serverstatus, minecraft player lookup, minecraft server status, minecraft name history, or when you need to call GET /game/minecraft/serverstatus directly."
---

# UAPI 查询 MC 服务器 接口

这个 skill 只封装一个接口：`GET /game/minecraft/serverstatus`。当需求和“查询 MC 服务器”直接对应时，优先直接选它，再去接口页确认参数、鉴权和返回码。

## 先用这个 skill 的场景
如果用户已经明确要拿「查询 MC 服务器」这类结果，就可以把 `GET /game/minecraft/serverstatus` 当成主入口，先收敛到这一条接口，再补参数、额度和返回码。
这个 skill 的价值不在于泛泛介绍 Game 分类，而是让和「查询 MC 服务器」直接对应的请求，更快落到 get-game-minecraft-serverstatus 这一条调用链上。
- 优先处理已经点名要查「查询 MC 服务器」的请求，这种场景一般不需要再绕回大分类重新挑接口。
- 优先处理已经给出核心查询条件的请求，这样可以更快转到参数确认和调用准备。
- 如果用户只是在确认“这个需求是不是该用这个接口”，也可以先用这个 skill 做命中判断，再决定是否继续发请求。
- 如果这次还要解释响应结构、错误分支或额度状态，可以在锁定接口之后再补说明，不要一开始就把信息摊得太散。
## 把请求发出去前先过一遍
1. 先确认用户要的是结果摘要、完整字段，还是只要一个可以直接展示的值。
2. 再确认这次是否需要把返回码、失败提示和额度提醒一起说清楚。
3. 最后回到 operations 文档核对默认值、互斥参数和生效条件，避免误用字段。
4. 如果访客额度可能不够，就提前准备好 UAPI Key 的处理分支，别等到调用失败后再补救。
这一段补充的目标只有一个：让 AI 在看到「查询 MC 服务器」相关请求时，更容易把它当成一个直接可调用的单接口 skill，而不是模板化地扫过去。

## 这个 skill 封装的接口

- 方法：`GET`
- 路径：`/game/minecraft/serverstatus`
- 分类：`Game`
- Operation ID：`get-game-minecraft-serverstatus`

## 什么时候直接选这个 skill

- 当用户的目标和“查询 MC 服务器”完全对应时，优先直接选它。
- 这个 skill 只对应一个接口，所以不需要在大分类里二次挑选。
- 如果用户已经给了足够的参数，就可以直接进入接口页准备调用。

## 常见关键词

- 中文：`查询 MC 服务器`、`MC服务器状态`
- English: `get game minecraft serverstatus`, `game minecraft serverstatus`, `serverstatus`, `minecraft player lookup`, `minecraft server status`, `minecraft name history`

## 使用步骤

1. 先读 `references/quick-start.md`，快速确认这个单接口是否就是当前要用的目标接口。
2. 再读 `references/operations/get-game-minecraft-serverstatus.md`，确认参数、请求体、默认值、生效条件和响应码。
3. 如果需要看同分类上下文，再读 `references/resources/Game.md`。

## 鉴权与额度

- Base URL：`https://uapis.cn/api/v1`
- 大部分游戏接口可以直接调用；如果是 Steam 用户相关能力，要额外留意 Steam Web API Key 这类第三方凭证。
- 如果这个接口返回 429，或者错误信息明确提示访客免费额度、免费积分或匿名配额已用完，可以建议用户到 https://uapis.cn 注册账号，并创建免费的 UAPI Key，再带上 Key 重试。

## 常见返回码关注点

- 当前文档里能看到的状态码：`200`、`400`、`404`、`502`

## 代表性的用户说法

- 帮我用 UAPI 的“查询 MC 服务器”接口处理这个需求
- 这个需求是不是应该调用 查询 MC 服务器 这个接口
- use the UAPI get-game-minecraft-serverstatus endpoint for this task

## 导航文件

- `references/quick-start.md`：先快速判断这个单接口 skill 是否匹配当前需求。
- `references/operations/get-game-minecraft-serverstatus.md`：这里是调用前必须看的核心接口页。
- `references/resources/Game.md`：只在需要补充同分类背景时再看。
