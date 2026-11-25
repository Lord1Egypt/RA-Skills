---
name: sichang-api
description: 用思畅 AI 开发者 API 生成图片、视频与文本对话。需要用户提供 API Key(sc_ 开头)。
---

# 思畅 AI 开发者 API

Base URL `https://api.sichang.xyz/v1`,全部 JSON。每个请求带 `Authorization: Bearer <API Key>`。
key 由用户在 https://sichang.xyz/settings?tab=api 创建,只在创建时展示一次;不要把它写进代码仓库或日志。
使用 API 须遵守 https://sichang.xyz/docs/terms(禁止转售与代生成、产物内容责任归用户)。完整字段定义见 https://sichang.xyz/developers/openapi.yaml 。

## 先自检

```bash
curl -s https://api.sichang.xyz/v1/me -H "Authorization: Bearer $SICHANG_API_KEY"
```

返回余额(`credits` + `subscriptionCredits`)、这把 key 的 `scopes`(`chat` / `image` / `video`)与限额。没有对应 scope 就不要调那个端点。

## 看模型

```bash
curl -s "https://api.sichang.xyz/v1/models?type=chat" -H "Authorization: Bearer $SICHANG_API_KEY"
curl -s "https://api.sichang.xyz/v1/models?type=image" -H "Authorization: Bearer $SICHANG_API_KEY"
curl -s "https://api.sichang.xyz/v1/models?type=video" -H "Authorization: Bearer $SICHANG_API_KEY"
```

不带 `type` 则一次返回 `{ image, video }` 两份目录。
图片目录里 `kind: generate` 的模型用于文生图,`kind: edit` 的用于改图;`creditCost` 是每张积分。
视频目录里 `mode` 决定要不要传首帧(`image-to-video`)、参考图(`reference-to-video`)或源视频(`video-extend` / `video-edit`),`durations` / `resolutions` / `aspectRatios` 是可选值。

## 生成图片(异步)

```bash
curl -s -X POST https://api.sichang.xyz/v1/images \
  -H "Authorization: Bearer $SICHANG_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d '{"prompt":"a corgi surfing at sunset","model":"z-image-turbo","aspectRatio":"16:9","resolution":"1K"}'
```

返回 `202 { "job": { "id": "...", "status": "PROCESSING", ... } }`。改图:先上传(见下),再把 `inputs: [{ "key": "<上传返回的 key>" }]` 加进请求体,`model` 换成 `kind: edit` 的模型。

## 生成视频(异步)

```bash
curl -s -X POST https://api.sichang.xyz/v1/videos \
  -H "Authorization: Bearer $SICHANG_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d '{"prompt":"a corgi surfing at sunset","model":"<video model id>","duration":"5s","resolution":"720p","aspectRatio":"16:9"}'
```

首帧用 `imageKey`,参考图用 `referenceImageKeys`,源视频用 `videoKey` 或 `sourceJobId`(你之前的视频 job id)。

## 文本对话(OpenAI 兼容,同步返回)

按 token 计费(单价见 `GET /v1/models?type=chat` 的 `pricing`,单位:积分 / 百万 token),请求前预扣、结束后多退少补,不足 1 积分的零头累计到下次;首 token 前失败自动全额退;非流式请求上游中途断开也全额退(此时不返回任何内容);流式已开始输出后断开按已产生的 token 结算。图片:`image_url` 分段(data URL 或 http 链接)原样交给模型,能看图的是 GLM 5.3 Flash(`z-ai/glm-5.3-flash-uncensored`)、DeepSeek V4.1 Flash(`deepseek-v4-1-flash`)、DeepSeek V4.1 Flash 无审查版(`deepseek-v4-1-flash-uncensored`)、Gemma 4(`gemma-4-uncensored`),其余模型被上游拒绝时自动去掉图片(换成文字占位)重试一次,不报错;图片按上游实际 token 计费;tool 消息里的图片会挪进紧随其后的一条 user 消息;`file` 分段换成文字占位;上下文上限按模型(`contextWindow`,扣除本次输出上限);`max_tokens` / `max_completion_tokens` 超过模型的最大输出时按最大输出截断(各模型的值见 https://sichang.xyz/docs/models/chat );思考:接受 `reasoning_effort`(none / minimal / low / medium / high / xhigh)与 `reasoning: {enabled, effort, max_tokens, exclude}`,不支持思考的模型静默忽略、不报错,档位就近映射到模型提供的档位;每个模型的 `supportsReasoning` / `reasoningDefault`(不传时默认开或关)/ `reasoningEfforts` / `reasoningDefaultEffort` 以 `GET /v1/models?type=chat` 为准,别写死;思考内容在 `message.reasoning_content`(流式 `delta.reasoning_content`),不混进 `content`,上游报了思考 token 数时在 `usage.completion_tokens_details.reasoning_tokens`,`reasoning.exclude: true` 则不返回思考文本;思考 token 按输出价计费;`supportsTools` 为 true 的模型支持 OpenAI 格式的工具调用(`tools` / `tool_choice` / `parallel_tool_calls`,历史里的 assistant `tool_calls` 与 `tool` 消息原样传)。联网搜索:请求里带 `web_search_options: {}`(可选 `max_uses`,1~3,默认 3)或 `plugins: [{"id":"web"}]` 开启,默认不开;仅 `GET /v1/models?type=chat` 里 `supportsWebSearch` 为 true 的模型可用,其余模型传了会 400。回复的 `choices[0].message.annotations` 带 `url_citation`(`url_citation.url` / `title`),`usage.server_tool_use.web_search_requests` 是本次实际搜索次数。**实际搜了才收**:我们自己的搜索工具每次搜索 3 积分,与 token 费合并进同一笔结算;上游原生搜索的模型,回复带来源时按一次(3 积分)收,没带来源不收。请求体超过 4.5 MB 会被平台直接拒绝并返回 HTTP 413(纯文本,不是 JSON 错误体)。模型 id 用 `GET /v1/models?type=chat` 里的。

```bash
# 非流式
curl -s -X POST https://api.sichang.xyz/v1/chat/completions -H "Authorization: Bearer $SICHANG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"<model-id>","messages":[{"role":"user","content":"你好"}]}'

# 流式(SSE,以 data: [DONE] 结束;中途断开会收到 data: {"error":...})
curl -sN -X POST https://api.sichang.xyz/v1/chat/completions -H "Authorization: Bearer $SICHANG_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"<model-id>","stream":true,"messages":[{"role":"user","content":"你好"}]}'
```

OpenAI SDK:`new OpenAI({ baseURL: 'https://api.sichang.xyz/v1', apiKey: process.env.SICHANG_API_KEY })`。

### Anthropic 兼容(Claude Code)

`POST /v1/messages` 兼容 Anthropic Messages API 的常用子集(system、tool_use / tool_result、tools、tool_choice、stream),鉴权可用 `x-api-key`;`POST /v1/messages/count_tokens` 只返回估算的 `input_tokens`、不扣费。Claude Code 设 `ANTHROPIC_BASE_URL=https://sichang.xyz/api`、`ANTHROPIC_AUTH_TOKEN=<API Key>` 即可;`claude-*` 模型名会映射到后台默认模型。image 块(base64 / url)转成 `image_url` 透传,规则同上;不支持 Anthropic 服务端工具;思考:`thinking`(`enabled` + `budget_tokens` / `adaptive` / `disabled`)与 `output_config.effort`(low / medium / high / xhigh / max),**不带 `thinking` 字段就是不思考**,单独的 `output_config.effort` 不会打开思考,不支持思考的模型静默忽略;上游有思考时返回 thinking 块,签名是占位值 `sichang-unsigned`(不可校验,别转发给真正的 Anthropic),`thinking.display: "omitted"` 时块文本为空;Claude Code 在支持思考的模型上默认开启、档位 high,`/effort` 或 `--effort` 调档,`MAX_THINKING_TOKENS=0` 或 `CLAUDE_CODE_DISABLE_THINKING=1` 关闭,`MAX_THINKING_TOKENS=<数字>` 对思畅模型名不改变深度,界面只显示正在思考;工具循环里需要回传思考的模型只回传当前这一轮工具循环的思考;错误体为 Anthropic 格式。

## 轮询直到完成

```bash
curl -s "https://api.sichang.xyz/v1/jobs/$JOB_ID?wait=30" -H "Authorization: Bearer $SICHANG_API_KEY"
```

`wait=30` 让服务器最多等 30 秒再返回;`status` 不是 `COMPLETED` / `FAILED` / `EXPIRED` 就再调一次。图片通常 10–90 秒,视频 1–10 分钟。
完成后 `outputs[0].url`(查看)与 `outputs[0].downloadUrl`(下载)**15 分钟后失效,拿到就下载,不要保存 URL**;之后要再取,重新 GET 一次 job 即可。
`FAILED` 的任务已自动退款(`credits.refunded`),`error.code` 说明原因。

## 上传素材(两步)

```bash
# 1. 拿预签名 URL(target=image 用于改图输入,target=video 用于视频素材;size 必须等于文件字节数)
curl -s -X POST https://api.sichang.xyz/v1/uploads \
  -H "Authorization: Bearer $SICHANG_API_KEY" -H "Content-Type: application/json" \
  -d "{\"kind\":\"image\",\"target\":\"video\",\"contentType\":\"image/png\",\"size\":$(stat -c%s in.png)}"
# 2. 直接 PUT 到 uploadUrl(Content-Type 必须与第 1 步一致)
curl -s -X PUT "$UPLOAD_URL" -H "Content-Type: image/png" --data-binary @in.png
```

之后把第 1 步返回的 `key` 填进 `inputs` / `imageKey` 等字段。素材有效期见 `expiresAt`。

## 列出任务

```bash
curl -s "https://api.sichang.xyz/v1/jobs?type=image&limit=20" -H "Authorization: Bearer $SICHANG_API_KEY"
```

含网页端提交的任务,`origin` 区分;翻页用返回的 `nextCursor`。

## 错误处理

所有错误都是 `{ "error": { "code", "message", "details"? } }`:

| HTTP | code | 怎么办 |
|---|---|---|
| 400 | `VALIDATION_ERROR` | 看 `details.field` 改请求;`details.allowed` 列出可选值 |
| 401 | `UNAUTHENTICATED` | key 无效 / 吊销 / 过期,让用户重新创建 |
| 402 | `CREDITS_EXHAUSTED` | 积分不足,提示用户到 https://sichang.xyz/pricing 充值;`details.required` 是本次需要的积分 |
| 403 | `SCOPE_DENIED` / `API_NOT_ELIGIBLE` / `API_DISABLED` / `ACCOUNT_SUSPENDED` | key 没这个权限 / 账号未达准入 / API 未开放 / 账号停用;都不是重试能解决的 |
| 409 | `IDEMPOTENCY_*` | 同一个 `Idempotency-Key` 已经用过:换新 key,或按 `IDEMPOTENCY_IN_FLIGHT` 稍后查询 |
| 422 | `CONTENT_VIOLATION` | 提示词被内容审核拦下,**不要原样重试**,改写描述 |
| 429 | `RATE_LIMITED` / `CONCURRENCY_LIMIT` / `DAILY_CAP_REACHED` | 按响应头 `Retry-After`(秒)等待;`X-RateLimit-Remaining` 告诉你还剩多少 |
| 503 | `MODERATION_UNAVAILABLE` / `UPSTREAM_UNAVAILABLE` | 未扣费或已退费,稍后重试一次 |

每次提交都带一个新的 `Idempotency-Key`(UUID);网络超时后用**同一个** key 重发,会拿回同一个 job 而不会重复扣费。

## 积分

与网页同价、无附加费:图片按模型每张计,视频按模型 × 时长 × 分辨率计,提交时扣、失败自动退。
每把 key 每天最多用 20,000 积分(创建时可调低),每分钟最多 10 次提交,在途任务图片 10 / 视频 5。
