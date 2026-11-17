---
name: tiktok-transcript
description: "TikTok video to transcript: the spoken words with timestamps, on-screen captions, title, hashtags, key points and like/comment counts. Use when the user shares a tiktok.com or vm.tiktok.com link and wants the transcript, the captions, a summary or a translation. Works without a key for one free summary a day; with a free API key (10 credits on sign-up, no card) you get the full transcript, 2 credits per minute of video. No download, no TikTok account or cookie needed."
version: 1.0.3
homepage: https://linkdigest.dev/zh/docs?ref=skill-tiktok-transcript
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":false,"description":"可选。LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-tiktok-transcript&next=/app/keys 创建，注册送 10 积分；没有 Key 时每天可免费看 1 条摘要"}],"homepage":"https://linkdigest.dev/zh/docs?ref=skill-tiktok-transcript"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_); optional"
    help: "https://linkdigest.dev/signin?ref=skill-tiktok-transcript&next=/app/keys"
    required_for: "the full output; without it the script gives one free summary a day"
---

# TikTok transcript / TikTok 视频转文字

> 没有 Key 也可以直接运行：脚本会用网站的免费看一条（每天 1 条，返回摘要）。要完整输出，在 https://linkdigest.dev/signin?ref=skill-tiktok-transcript&next=/app/keys 创建 Key（注册送 10 积分，不用卡）。

把抖音、小红书视频笔记、TikTok、YouTube、X 的视频链接读成文字：口播逐字稿（没有平台字幕时用 Qwen3-ASR 语音识别；YouTube 例外，由 Gemini 看视频写出）、画面上出现的字和大致时间、标题和简介、要点、点赞评论收藏分享数、话题标签。不用下载视频，不用在本机装 ffmpeg 或语音识别模型，不需要你的平台账号或 Cookie。

## 什么时候用

- 「提取这条抖音的文案」「视频转文字」「把口播扒下来」「这个视频讲了什么」。
- 整理对标账号的视频内容（一条一条调；一次多条见文档里的批量接口 `POST /api/v1/digest/batch`，最多 50 条）。
- 画面上的字幕、花字比口播更重要的视频（教程、带货、知识类）。

## 什么时候不用

- 需要逐句时间轴（比如生成 SRT 字幕）：逐字稿的时间是分段级的，见下文「时间戳的精度」。
- B站链接：可以读（2026-10-24 起）。
- 直播、私密、已删除、需要登录才能看的视频：读不了（返回 422，不扣费）。
- 只想下载无水印视频：这个技能不提供视频文件。

## 准备（一次）

1. 打开 https://linkdigest.dev/signin?ref=skill-tiktok-transcript&next=/app/keys ，用 Google 或邮箱登录（邮箱会收到一封登录链接），创建 API Key（`ld_live_` 开头）。新账户送 10 积分，只送一次，不用绑卡。
2. 设置环境变量：

```bash
export LINKDIGEST_API_KEY=ld_live_...
```

也可以写进 OpenClaw 配置（`~/.openclaw/openclaw.json`）里这个技能的 `env`：

```json5
{ skills: { entries: { "linkdigest-video-transcript": { env: { LINKDIGEST_API_KEY: "ld_live_..." } } } } }
```

Key 只放在环境变量或配置里，不要贴进对话、代码或提交记录。

## 用法

推荐用自带脚本（Python 3.8+ 标准库，已经处理好 202 排队和轮询）：

```bash
python3 {baseDir}/scripts/linkdigest.py "<视频链接或整段分享文案>"
python3 {baseDir}/scripts/linkdigest.py "<视频链接>" --format json
python3 {baseDir}/scripts/linkdigest.py "<视频链接>" --translate-to en    # 另附英文译文，+1 积分，原文保留
python3 {baseDir}/scripts/linkdigest.py "<视频链接>" --max-credits 5      # 超过 5 积分的视频不读、不扣费
```

- 抖音「复制链接」得到的整段分享文案可以直接传，服务端会从里面取出链接。文案里有引号或换行时，从标准输入传：`printf '%s' "$SHARE_TEXT" | python3 {baseDir}/scripts/linkdigest.py -`
- 视频较长时，提交后约 20 秒内会先返回 202 和 jobId。脚本会自动用 `?wait=20` 轮询，默认最多等 900 秒（`--timeout` 可改）。
- 等待超时不会丢任务：任务继续在服务端跑，按 stderr 的提示用 `--job-id <jobId>` 接着取。同一个 jobId 只扣一次费。任务完成后在服务端保留 15 分钟，尽快取；过期了就重新提交同一链接。
- 本次扣了几个积分、是否命中缓存、是否只读了一部分，打印在 stderr 的最后一行。
- 退出码：0 成功；2 参数错误或没设 Key；3 Key 无效（401）；4 积分不够或视频超长（402，未扣费，stderr 里有付款链接）；5 链接读不了（422）；6 调用太频繁，或这个 Key 在 /app/keys 设的 30 天积分上限已用完（429，未扣费）；7 等待超时。

### 直接调 HTTP（没有 Python 时）

```bash
curl -sS -X POST https://linkdigest.dev/api/v1/digest \
  -H "Authorization: Bearer $LINKDIGEST_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://v.douyin.com/<短链>/", "format": "json"}'
```

- `200`：结果 JSON。
- `202`：`{"pending":true,"jobId":"…","poll":"/api/v1/digest/…","retryAfter":15}`。用 jobId 取，不要重新提交：

```bash
curl -sS "https://linkdigest.dev/api/v1/digest/<jobId>?wait=20" \
  -H "Authorization: Bearer $LINKDIGEST_API_KEY"
```

`wait=20` 让服务端最多等 20 秒再回复；仍是 `202`（会带 `stage` 表示进行到哪一步）就再取一次，直到 `200`。要 Markdown 时，提交用 `"format": "markdown"`，取结果加 `&format=markdown`（`202` 响应始终是 JSON）。其他可选参数：`"translate_to": "en"`、`"max_credits": 5`、`"partial_ok": true`、`"breakdown": true`。

可以直接运行的 bash/zsh 版本（提交 + 轮询，最多约 15 分钟）：

```bash
API=https://linkdigest.dev/api/v1/digest
AUTH="Authorization: Bearer $LINKDIGEST_API_KEY"
LINK='https://v.douyin.com/<短链>/'
res=$(curl -sS -w '\n%{http_code}' -X POST "$API" -H "$AUTH" \
  -H "Content-Type: application/json" -d "{\"url\": \"$LINK\", \"format\": \"json\"}")
code=${res##*$'\n'}; body=${res%$'\n'*}
n=0
while [ "$code" = 202 ] && [ $n -lt 45 ]; do
  n=$((n+1))
  job=$(printf '%s' "$body" | sed -n 's/.*"jobId":"\([^"]*\)".*/\1/p')
  res=$(curl -sS -w '\n%{http_code}' "$API/$job?wait=20" -H "$AUTH")
  code=${res##*$'\n'}; body=${res%$'\n'*}
done
echo "HTTP $code" >&2
printf '%s\n' "$body"
```

## 返回字段（视频）

| 字段 | 内容 |
| --- | --- |
| `title` / `author` / `posted_at` / `caption` | 标题、作者、发布日期、简介原文 |
| `transcript[]` | 口播逐字稿，`[{t, text}]`，`t` 是这一段开始的秒数 |
| `transcript_source` | 逐字稿来源：`asr`（Qwen3-ASR 语音识别）、`native_captions`（平台自带字幕）、`gemini_video`（YouTube：Gemini 看视频写出，见下文）、`none`（没有可识别的语音） |
| `on_screen[]` | 画面上的字，`[{t, text}]`，`t` 是大致时间（秒）。YouTube 没有这一项 |
| `ocr_text[]` | 画面文字的汇总列表（不带时间）。YouTube 的画面文字只在这里，也是 Gemini 写出的 |
| `key_points[]` | 要点，用原文语言 |
| `stats` | `likes`、`comments`、`collects`、`shares`、`plays`；读取当天平台给的数，`as_of` 是日期，拿不到的是 `null` |
| `tags[]` | 话题标签 |
| `duration_seconds` / `read_seconds` | 视频总长、实际读了多长 |
| `partial` | 只读了开头时才有：`read_seconds`、`duration_seconds`、`read_credits`、`full_credits`（读全片要多少积分） |
| `translation` | 加了 `translate_to` 才有；原文字段保持不变 |
| `raw_markdown` | 整条内容的 Markdown：`## Transcript`（每段前面是 `` `mm:ss` ``）、`## On-screen text`（前面是 `` `≈mm:ss` ``） |
| `credits` / `cached` | 本次扣了几个积分；读过的链接 `cached=true`，0 积分 |
| `degraded[]` | 处理中没做完的部分的说明，正常为空 |

### 时间戳的精度

- `transcript[]`（`asr`）：Qwen3-ASR 只返回文字、不返回逐句时间，所以音频按最长约 170 秒切段上传，每段一个开始时间。时间是段级的：不到 170 秒的视频只有一段（`t=0`）；一条 15:42 的抖音视频返回的段落从 0、170、340、510、680、850 秒开始。这不是逐句时间轴。
- `on_screen[]`：全片均匀抽帧读字（目前最多 40 帧），时间取最近的关键帧，误差在一个关键帧间隔内（通常 2–5 秒）；同样的字连续出现只记一次。视频越长抽帧越稀，一闪而过的字可能漏掉。要按秒定位，看 `on_screen`。
- YouTube 例外：YouTube 不让我们的服务器地址下载视频，所以 YouTube 链接一般由 Gemini 直接看视频来读，`degraded` 里会写 `read by Gemini watching the video directly`。这时 `transcript_source` 是 `gemini_video`，逐字稿和它的时间 `t`、画面文字（`ocr_text`）、标题和作者都是 Gemini 写出的，属于模型输出，不是平台字幕，也不是 Qwen3-ASR；没有 `on_screen`。

## 把结果交给用户时

- 用户要「文案」：给 `transcript` 的全文，按原样，不改写、不总结，除非用户要求。画面文字单独列出，不要混进口播。
- `transcript_source` 是 `asr` 时，`transcript` 是语音识别结果，方言、口音、专有名词、中英混说时可能有错字；人名、品牌名、数字提醒用户核对。
- `transcript_source` 是 `gemini_video`（YouTube）时，告诉用户逐字稿是模型看视频写出的，要逐字引用请以视频本身为准。
- `transcript_source` 是 `none` 或逐字稿为空时，说明视频没有可识别的人声（比如纯音乐），这时文字主要在 `on_screen` 里。
- 有 `partial` 时，告诉用户只读了前多少秒，以及读全片要多少积分。
- 告诉用户这次用了几个积分（`credits`，缓存命中是 0）。

## 费用

每条 1 积分，另加每开始的 1 分钟 1 积分（1 分 01 秒按 2 分钟算）。按加量包 ¥36 = 250 积分折算，1 积分约 ¥0.144。

| 视频长度 | 积分 | 约合 |
| --- | --- | --- |
| 1 分钟以内 | 2 | ¥0.29 |
| 3 分钟 | 4 | ¥0.58 |
| 5 分钟 | 6 | ¥0.86 |
| 10 分钟 | 11 | ¥1.58 |
| 加译文（`--translate-to`） | +1 | +¥0.14 |
| 加爆款拆解（`--breakdown`） | +1 | +¥0.14 |
| 任何人读过的链接（缓存） | 0 | 0 |
| 读不出内容 | 0 | 0 |

注册送 10 积分（每个账户一次，不按月补），够读一条 9 分钟的视频，或 5 条 1 分钟以内的视频。加量包 $5 = 250 积分，可用支付宝付款（按 ¥36 结算），不过期；或 Dev 月付 $9 = 每月 500 积分（银行卡）。价格以 https://linkdigest.dev/zh/docs?ref=skill-tiktok-transcript 为准。

## 长视频

- 单条视频长度上限：免费账户和只买了加量包的账户 10 分钟；Dev 月付 30 分钟。
- 超过上限默认返回 402（`error_code: media_too_long`），不扣费。
- 免费账户和加量包账户可以加 `--partial-ok`（HTTP 里是 `"partial_ok": true`）：只读开头，读多长取决于剩余积分，最多 10 分钟；结果里的 `partial` 写明读了多少秒。
- 长视频省钱档 `--depth transcript`（HTTP 里是 `"depth": "transcript"`，2026-10-06 起）：全程逐字稿 + 少量截帧，基础 1 积分 + 每开始的 2 分钟 1 积分（44 分钟的视频 23 积分，完整档要 45）。长度上限也更高：免费和加量包账户 60 分钟，Dev 月付 2 小时。画面文字只读少量截帧，结果里的 `coverage` 会写明。YouTube 不支持这一档。
- 长视频处理要几分钟，一定会走 202 + 轮询，不要因为第一次返回 202 就重新提交。

## 限制

- B站：可以读（2026-10-24 起）。B 站偶尔拒绝时返回 503，不扣费，稍后重试即可。
- 直播、私密、已删除、需要登录才能看的视频读不了。
- 互动数据是读取当天的快照，不是实时数据；缓存里的结果保留第一次读取那天的数。
- 每个账户每小时最多 60 次 API 调用。
- 不下载、不提供视频文件；不搜索、不读评论、不发帖。

## 隐私

- 只把你给的链接发给 linkdigest.dev，不需要也不会读取你的抖音、小红书等账号或 Cookie。
- 视频、音频、图片只在处理时放在临时目录，返回前删除，不保存、不转发。
- 文字结果按链接缓存（所以同一链接再读免费），可能提供给请求同一公开链接的其他用户。不要提交私密内容的链接。
- 读取时会用到第三方模型服务，详见 https://linkdigest.dev/privacy 。
- `scripts/linkdigest.py` 只读环境变量 `LINKDIGEST_API_KEY`，只连 `linkdigest.dev`，不读写本地文件。

## 其他接入方式

- 远程 MCP（Streamable HTTP）：`https://linkdigest.dev/mcp`，请求头 `Authorization: Bearer <key>`，工具 `digest_url`。Claude Code：
  `claude mcp add --transport http linkdigest https://linkdigest.dev/mcp --header "Authorization: Bearer <key>"`
- 只支持本地（stdio）MCP 的客户端：`npx mcp-remote https://linkdigest.dev/mcp --header "Authorization: Bearer <key>"`
- Dify 插件市场：`jcaiagent7143-ui/linkdigest`
- OpenAPI：https://linkdigest.dev/openapi.json
- 开源客户端与接入示例：https://github.com/jcaiagent7143-ui/linkdigest-mcp
- 中文文档：https://linkdigest.dev/zh/docs?ref=skill-tiktok-transcript

LinkDigest 由独立开发者 Jack（GitHub `jcaiagent7143-ui`）开发和维护。问题和反馈：support@linkdigest.dev
