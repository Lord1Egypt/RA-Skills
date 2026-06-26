# Examples

## Conversation Examples

First use, ask for token:

```text
用户：帮我看今天的彭博市场新闻
助手：可以，先把你的 TradeAlphaToken 直接发在聊天里。我只会在当前会话中使用它，不会要求你写到环境变量或本地文件。你也可以前往 https://quantaccess.lxaa.top/ 获取或管理 token。
```

Missing token, stop before API call:

```text
用户：查一下美联储降息预期相关新闻
助手：需要先提供 TradeAlphaToken 才能查询。请直接在聊天里发送 token，我会在当前会话中使用它，不会保存到本地文件。你也可以前往 https://quantaccess.lxaa.top/ 获取或管理 token。
```

Continue after the user provides a token:

```text
用户：token 是 xxxxx
用户：帮我看今天的彭博市场新闻
助手：调用实时新闻接口，请求条件为 timeframe=today, source=bloomberg, category=市场与货币。
```

Do not ask for the token again in the same conversation:

```text
用户：再帮我看一下路透近 24 小时快讯
助手：继续复用当前会话里已提供的 TradeAlphaToken，调用实时新闻接口，请求条件为 timeframe=latest, source=rtrs。
```

Ask again when the token expires:

```text
助手：当前 token 无效或已过期，请直接在聊天里发送最新的 TradeAlphaToken，我会在当前会话中继续使用它。你也可以前往 https://quantaccess.lxaa.top/ 检查或管理 token。
```

No quota or permission:

```text
助手：当前 token 可能没有额度、免费次数已用尽，或该接口权限未开通。请前往 https://quantaccess.lxaa.top/ 检查额度、权限或产品访问状态。
```

## Payload Examples

Realtime news:

```json
{
  "token": "<USER_PROVIDED_TOKEN>",
  "timeframe": "today",
  "source": "bloomberg",
  "category": "市场与货币",
  "page_size": 5
}
```

Semantic search:

```json
{
  "token": "<USER_PROVIDED_TOKEN>",
  "keyword": "美联储降息预期",
  "top_k": 10
}
```

Semantic search with time range:

```json
{
  "token": "<USER_PROVIDED_TOKEN>",
  "keyword": "K形债务市场 庭外债权人协议",
  "top_k": 10,
  "start_time": "2026-04-25 00:00:00",
  "end_time": "2026-04-25 23:59:59",
  "source": "bloomberg",
  "category": "市场与货币",
  "level": "重要"
}
```

## Prompt Mapping

- "帮我看今天的彭博市场新闻" -> realtime + `{"token":"<USER_PROVIDED_TOKEN>","timeframe":"today","source":"bloomberg","category":"市场与货币"}`
- "拉近 24 小时路透快讯" -> realtime + `{"token":"<USER_PROVIDED_TOKEN>","timeframe":"latest","source":"rtrs"}`
- "查美联储降息预期相关新闻" -> search + `{"token":"<USER_PROVIDED_TOKEN>","keyword":"美联储降息预期"}`
- "查今天美联储降息预期相关新闻" -> search + `{"token":"<USER_PROVIDED_TOKEN>","keyword":"美联储降息预期","start_time":"<TODAY 00:00:00>","end_time":"<NOW>"}`
- "查 2026-04-25 彭博 K 形债务市场相关新闻" -> search + `{"token":"<USER_PROVIDED_TOKEN>","keyword":"K 形债务市场","start_time":"2026-04-25 00:00:00","end_time":"2026-04-25 23:59:59","source":"bloomberg"}`
- "搜近 24 小时路透原油相关新闻" -> search + `{"token":"<USER_PROVIDED_TOKEN>","keyword":"原油","start_time":"<NOW-24H>","end_time":"<NOW>","source":"rtrs"}`
- "搜一下 K 形债务市场相关新闻" -> search + `{"token":"<USER_PROVIDED_TOKEN>","keyword":"K 形债务市场"}`
