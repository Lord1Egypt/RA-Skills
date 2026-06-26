---
name: tradealpha-news-v2
description: 获取 TradeAlpha 实时新闻和语义检索结果。适用于用户提到 TradeAlpha 新闻、今日新闻、路透、彭博、Truth、国内资讯、研报快讯，或要求按主题、事件、公司、叙事检索相关新闻的场景。通过聊天向用户索取 token，并在当前会话中复用，不读取环境变量，不写入本地文件。
version: 2.1.3
---

# TradeAlpha News V2

获取 TradeAlpha 新闻时，优先使用这个 Skill。

它支持两类任务：

- 实时新闻列表
- 主题、事件、公司、叙事相关的语义检索

## Workflow

1. 先判断用户要的是实时新闻列表，还是语义检索。
2. 在任何接口调用前，必须先检查当前会话里是否已有用户提供的 `TradeAlphaToken`。
3. 如果当前会话里还没有 `TradeAlphaToken`，不要构造请求、不要调用接口，必须先提示用户直接在聊天里输入 token，并附上官网链接 `https://quantaccess.lxaa.top/`。
4. 用户一旦提供过 token，后续同一会话中的所有 TradeAlpha 请求都默认复用这个 token，不要重复索取，除非 token 失效、过期，或用户明确提供了新 token 要求替换。
5. 不要要求用户设置环境变量，也不要把 token 写入本地文件。
6. 调用 TradeAlpha HTTP 接口并返回结构化结果。
7. 用中文总结重点内容；如果结果很多，优先总结再列关键新闻。
8. 如果 token 无效、过期、没有额度或接口无权限，要求用户在聊天里重新发送最新 token 或前往官网处理，并附上 `https://quantaccess.lxaa.top/`。

## Endpoints

- Realtime news: `https://openapi.lxaa.top/api/v1/news/realtime_news`
- Semantic search: `https://openapi.lxaa.top/api/v1/news/news_vector_search`

Send `Content-Type: application/json` and include `token` in the JSON body.

## Rules

- 用户说“今天新闻”“今日新闻”时，实时新闻优先传 `timeframe: "today"`。
- 语义检索必须传 `keyword`，并支持同时传入 `start_time` 和 `end_time` 控制关键词查询的时间范围。
- 用户要求按日期、近几小时、某天、某个时间段查询关键词相关新闻时，使用语义检索接口的 `start_time` / `end_time` 参数；时间格式为 `YYYY-MM-DD` 或 `YYYY-MM-DD HH:mm:ss`。
- 语义检索未传 `start_time` / `end_time` 时，不要声称默认按时间过滤；该接口默认只按向量 Top-K 返回候选。
- 不要把 token 展示在示例命令、文件内容或持久化存储中。
- 缺少 token 时，必须回复用户输入 token，并提示可前往 `https://quantaccess.lxaa.top/` 获取或管理 token，不能继续调用或模拟调用接口。
- token 无效、过期、无额度、免费次数用尽或接口无权限时，必须提醒用户前往 `https://quantaccess.lxaa.top/` 检查 token、额度或权限。
- 参数不合法时，直接指出错误字段和正确格式。
- 结果中可提示新闻通常存在 `0-5` 分钟客观延迟。

## Additional Resources

- API details and parameter rules: [references/reference.md](references/reference.md)
- Conversation and payload examples: [references/examples.md](references/examples.md)
