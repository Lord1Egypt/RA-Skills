---
name: weibo-to-text
description: "微博转文字 / 微博视频文案提取 / 微博 API：一条微博链接读成文字——正文、作者和时间、转发评论点赞数、每张图的描述和图上的字、视频口播逐字稿和画面文字、话题、前几条热评、逐字核对的要点。用户发来 weibo.com、m.weibo.cn 链接，要提取微博内容、扒视频文案、整理热评、做舆情或竞品资料时使用。不用申请微博开放平台，不用微博账号或 Cookie。图文 1 积分起，1 分钟视频 2 积分；注册送 10 积分。"
version: 1.0.0
homepage: https://linkdigest.dev/zh/weibo-api?ref=skill-weibo-to-text
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":false,"description":"可选。LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-weibo-to-text&next=/app/keys 创建，注册送 10 积分；没有 Key 时每天可免费看 2 条摘要"}],"homepage":"https://linkdigest.dev/zh/weibo-api?ref=skill-weibo-to-text"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_); optional"
    help: "https://linkdigest.dev/signin?ref=skill-weibo-to-text&next=/app/keys"
    required_for: "the full output; without it the script gives one free summary a day"
---

# 微博转文字 · Weibo to text

一条微博，读成 AI 能直接用的文字。不用申请微博开放平台、不用写爬虫、不用登录微博：服务端通过微博自己的访客页读公开微博。

## 能拿到什么

| 内容 | 字段 |
| --- | --- |
| 正文、作者、发布时间、话题 | `caption` / `title`、`author`、`posted_at`、`tags[]` |
| 转发、评论、点赞数（读取当时） | `stats` |
| 每张图的描述和图上的字 | `images[]`、`ocr_text[]` |
| 视频口播逐字稿（有声音时）和画面文字，带时间 | `transcript[]`、`on_screen[]` |
| 分享页显示的前几条热评，带点赞和回复数 | `comments[]` |
| 要点，每条附原文引用并逐字核对 | `key_points[]`、`key_point_support[]` |
| 读到了什么、没读到什么 | `coverage`、`degraded[]` |

实测（2026-11-01，`m.weibo.cn/detail/5351369302084798`）：61 秒视频，4,761 赞 · 547 评论 · 218 转发，29 段带时间的画面文字，5 条核对过的要点，前 8 条热评；回执写明「视频没有音轨」。3 积分。

## 准备

1. 在 https://linkdigest.dev/signin?ref=skill-weibo-to-text&next=/app/keys 登录（邮件里有 6 位验证码，也可以点链接），创建 API Key。新账户送 10 积分，不用绑卡。
2. `export LINKDIGEST_API_KEY=ld_live_...`（只放在环境变量或技能配置里，不要贴进对话）。

没有 Key 也能先跑：脚本会用网站的免费看一条（每个地址每天 2 条，只给摘要）。

## 用法

```bash
python3 {baseDir}/scripts/linkdigest.py "https://m.weibo.cn/detail/<ID>"
python3 {baseDir}/scripts/linkdigest.py "https://weibo.com/<用户>/<微博ID>" --format json
python3 {baseDir}/scripts/linkdigest.py "<微博链接>" --depth script      # 只要视频口播：每开始 2 分钟 1 积分
python3 {baseDir}/scripts/linkdigest.py "<微博链接>" --translate-to en   # 另附英文译文，+1 积分
```

视频要读几十秒，脚本会自动等待并轮询；本次扣了几个积分、是否命中缓存打印在 stderr 最后一行。同一条微博的不同链接写法（`weibo.com/<用户>/<ID>`、`m.weibo.cn/detail/<数字ID>`、`m.weibo.cn/status/<ID>`）认成同一条，读过再读 0 积分。

直接调 HTTP：

```bash
curl -sS -X POST https://linkdigest.dev/api/v1/digest \
  -H "Authorization: Bearer $LINKDIGEST_API_KEY" -H "Content-Type: application/json" \
  -d '{"url": "https://m.weibo.cn/detail/<ID>", "format": "json"}'
```

返回 `202` 时用响应里的 `poll_url` 约 15 秒后 GET（或把同样的 POST 再发一次，只扣一次费）。

## 读不了的情况（都不扣费）

- 只有关注者能看的微博（关注可见、好友圈）：如实返回读不了，不会猜内容。带视频的这种微博可以用浏览器扩展在自己登录的浏览器里读。
- `t.cn` 短链：先在浏览器里打开，复制展开后的 `weibo.com` / `m.weibo.cn` 地址。
- 已删除的微博、微博主页（不是单条微博）。
- 评论只读分享页显示的前几条热评，不是全部评论。

## 交给用户时

- 用户要「文案」：给 `transcript` 全文；没有口播时（`transcript_source` 为 `none`），文字在 `on_screen` / `ocr_text` 里，告诉用户视频没有人声。
- 引用要点时带上 `key_point_support` 里的原文，便于用户核对。
- 告诉用户这次用了几个积分（`credits`；缓存命中为 0）。

价格：图文 1 积分起，视频每开始 1 分钟 2 积分，只要口播（`--depth script`）每开始 2 分钟 1 积分。积分用完后支付宝 ¥9.9 买 50 积分，一次性、不订阅、不过期。
