# TradeAlpha News Reference

## Endpoints

- Realtime news: `https://openapi.lxaa.top/api/v1/news/realtime_news`
- Semantic search: `https://openapi.lxaa.top/api/v1/news/news_vector_search`
- Method: `POST`
- Token source: user provides `TradeAlphaToken` directly in chat
- Token placement: JSON request body field `token`
- Session rule: once the user provides a token, remember and reuse it for all later TradeAlpha requests in the same conversation/session
- Storage rule: do not write the token to files, env vars, shell commands, or local config
- Official site: `https://quantaccess.lxaa.top/`
- Missing token rule: before every API call, check whether the current conversation already has a user-provided `TradeAlphaToken`; if not, ask the user to provide it in chat, include the official site link, and stop.

## Realtime Fields

- `token`: required non-empty string
- `timeframe`: `today` or `latest`
- `start_time`: `YYYY-MM-DD` or `YYYY-MM-DD HH:mm:ss`
- `end_time`: `YYYY-MM-DD` or `YYYY-MM-DD HH:mm:ss`
- `source`: `domestic` | `truth` | `bloomberg` | `rtrs` | `research_report`
- `category`: `政治军事` | `社会` | `娱乐体育` | `公司` | `超大型公司` | `政策` | `市场与货币`
- `level`: `很重要` | `重要` | `一般`
- `page`: integer, default `1`
- `page_size`: integer, default `20`, max `100`

## Semantic Search Fields

- `token`: required non-empty string
- `keyword`: required non-empty string
- `top_k`: integer, default `20`, max `50`
- `start_time`: optional `YYYY-MM-DD` or `YYYY-MM-DD HH:mm:ss`; only keep news after this time using the database `createtime` field
- `end_time`: optional `YYYY-MM-DD` or `YYYY-MM-DD HH:mm:ss`; only keep news before this time using the database `createtime` field
- `source`: `domestic` | `truth` | `bloomberg` | `rtrs` | `research_report`
- `category`: `政治军事` | `社会` | `娱乐体育` | `公司` | `超大型公司` | `政策` | `市场与货币`
- `level`: `很重要` | `重要` | `一般`

## Semantic Search Behavior

- The semantic search endpoint vectorizes `keyword` and returns semantically similar news in descending similarity order.
- Semantic search supports time filtering with `start_time` and `end_time`; pass them whenever the user asks for keyword news within a date, time window, or recent period.
- If semantic search does not include `start_time` or `end_time`, the API does not apply MySQL-side time filtering; results are determined by vector Top-K and other explicit filters.
- Semantic search has no pagination. Use `top_k` as the candidate limit. The response `page` is fixed at `1`, and `page_size` equals the actual returned list length.

## Mapping

- 路透 -> `rtrs`
- 彭博 -> `bloomberg`
- Truth -> `truth`
- 国内 -> `domestic`
- 研报 -> `research_report`

## Validation Rules

- If the user says "今天新闻", prefer `timeframe: "today"`.
- If no time range is provided for realtime news, the upstream API default recent-window behavior is acceptable.
- For `timeframe: "today"`, expand it to today's `start_time` and current `end_time`.
- If the user asks for keyword or semantic news search with a time expression, send the time range through semantic search `start_time` and `end_time`.
- For a whole-day semantic search, expand `YYYY-MM-DD` to `start_time: "YYYY-MM-DD 00:00:00"` and `end_time: "YYYY-MM-DD 23:59:59"` unless the user specified exact times.
- For "今天" in semantic search, expand to today's `start_time` and current `end_time`.
- For recent windows such as "近 24 小时" or "过去 3 天" in semantic search, calculate explicit `start_time` and `end_time`.
- Date values earlier than `2025-04-01 00:00:00` are rejected.
- `start_time` cannot be later than `end_time`.
- `page` must be greater than or equal to `1`.
- `page_size` must be within `1-100`.
- `top_k` must be within `1-50`.
- If the token is missing, ask the user to provide it in chat before proceeding and include `https://quantaccess.lxaa.top/`; do not build a payload, call the API, or simulate API results.
- If the token has already been provided in this conversation, reuse it automatically and do not ask again.
- If the token is invalid or expired, ask the user to provide a refreshed token in chat and include `https://quantaccess.lxaa.top/`.
- If the API returns no quota, free usage exhausted, permission unavailable, interface not configured, or semantic search not configured, tell the user to check quota and permissions at `https://quantaccess.lxaa.top/`.

## Error Handling

- `1001`: token invalid or expired. Ask for a refreshed token and include `https://quantaccess.lxaa.top/`.
- `1003`: rate limit exceeded. Tell the user to retry later; include the official site only if the response indicates quota/account issues.
- `1004`: no permission, free usage exhausted, interface unavailable, or semantic search not configured. Tell the user to check API permission, quota, or product access at `https://quantaccess.lxaa.top/`.

## Response Shape

Success result:

```json
{
  "success": true,
  "auth_required": false,
  "next_action": "none",
  "token_source": "chat",
  "request": {},
  "total": 0,
  "page": 1,
  "page_size": 20,
  "list": [],
  "note": "..."
}
```

Semantic search with time range request example:

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

Failure result:

```json
{
  "success": false,
  "auth_required": true,
  "next_action": "ask_token_in_chat",
  "token_source": "none",
  "error": "...",
  "message": "请直接在聊天里发送 TradeAlphaToken。你也可以前往 https://quantaccess.lxaa.top/ 获取或管理 token。"
}
```
