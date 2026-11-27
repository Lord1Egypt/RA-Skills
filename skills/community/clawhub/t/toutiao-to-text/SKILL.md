---
name: toutiao-to-text
description: "今日头条转文字 / 今日头条文案提取 / 头条文章提取 / 今日头条 API：一条头条链接读成文字——文章的标题、作者、发布日期、正文全文、每张配图的描述和图上的字；视频的口播逐字稿（带时间）和画面文字；再加逐字核对的要点。用户发来 toutiao.com 或 m.toutiao.com 的文章、视频链接，要提取正文、扒视频文案、让 AI 总结或改写时使用。不用登录头条，不用 Cookie，不用自己起浏览器。文章 1 积分起，1 分钟视频 2 积分；注册送 10 积分。"
version: 1.0.3
homepage: https://linkdigest.dev/zh/toutiao-api?ref=skill-toutiao-to-text
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":false,"description":"可选。LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-toutiao-to-text&next=/app/keys 创建，注册送 10 积分；没有 Key 时每天可免费看 2 条摘要"}],"homepage":"https://linkdigest.dev/zh/toutiao-api?ref=skill-toutiao-to-text"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_); optional"
    help: "https://linkdigest.dev/signin?ref=skill-toutiao-to-text&next=/app/keys"
    required_for: "the full output; without it the script gives a free summary, two a day"
---

# 今日头条转文字 · Toutiao to text

把一条今日头条的文章或视频链接，读成 AI 能直接用的文字。

为什么需要它：头条的页面要在浏览器里执行脚本才出现内容。2026-11-20 实测直接请求一篇文章的地址，返回 72,914 字节，可见文字 0 个——所以把链接丢给模型，它只能说「打不开」。这个技能让服务端在浏览器里把页面读出来，视频再转写口播。

## 什么时候用

- 用户贴了 `toutiao.com/article/…`、`toutiao.com/video/…`，或 App 分享出来的 `m.toutiao.com/group/…`、`/item/…` 链接；
- 要正文、要视频文案、要总结、要改写、要把几篇头条文章整理成资料。

## 一条命令

```bash
python3 {baseDir}/scripts/linkdigest.py "https://www.toutiao.com/article/7709705250554266155"
python3 {baseDir}/scripts/linkdigest.py "$VIDEO_LINK" --depth transcript   # 长视频省钱：只要逐字稿，每开始 2 分钟 1 积分
python3 {baseDir}/scripts/linkdigest.py "<头条链接>" --format json
python3 {baseDir}/scripts/linkdigest.py "<头条链接>" --translate-to en                               # 另附英文译文，+1 积分
```

页面要在浏览器里读，脚本会自动等待并轮询；本次扣了几个积分、是否命中缓存打印在 stderr 最后一行。

直接调 HTTP 也行：

```bash
curl -sS -X POST https://linkdigest.dev/api/v1/digest \
  -H "Authorization: Bearer $LINKDIGEST_API_KEY" -H "Content-Type: application/json" \
  -d '{"url": "https://www.toutiao.com/article/7709705250554266155", "format": "json"}'
```

返回 `202` 时用响应里的 `poll_url` 约 15 秒后 GET。

**不要自己编链接或编号来测试。** 上面尖括号里的是占位符：带尖括号的链接会得到 `400 placeholder_link`，编出来的编号会得到 `422`，都不扣费，也读不到东西。用户还没给链接就先向用户要。只想确认 Key 能用，读这条真实的示例笔记（已读过，0 积分）：

```bash
python3 {baseDir}/scripts/linkdigest.py "https://www.xiaohongshu.com/discovery/item/6a6bf662000000002402de7e?xsec_token=CBCe01s1uyd2C8uMx6ycYcnEwPV5_31OX1u_I19FCSd54=&xsec_source=app_share"
```

Never invent a link or an id to test with; ask the user for one, or read the sample above (already read, 0 credits) to check the key.

## 返回的字段

| 内容 | 字段 |
| --- | --- |
| 标题、作者（头条号）、发布日期 | `title`、`author`、`posted_at` |
| 文章正文全文 | `caption` |
| 每张配图的描述和图上的字 | `images[]`、`ocr_text[]` |
| 视频口播逐字稿，带时间；完整深度再加画面文字 | `transcript[]`、`on_screen[]` |
| 要点，每条附原文引用并逐字核对 | `key_points[]`、`key_point_support[]` |
| 读到了什么、没读到什么，实际请求的是哪个地址 | `coverage`、`degraded[]` |

实测（2026-11-20）：

- 文章 `toutiao.com/article/7709705250554266155`：标题、作者、发布日期、正文全文、6 张配图的描述和图上文字、14 条要点。1 积分。
- 视频 `toutiao.com/video/7628244045329563689`（4 分 15 秒）：40 段带时间的口播逐字稿（到 4:12）、7 条要点。只要逐字稿 4 积分，完整深度 6 积分。

## 链接写法

| 你手里的链接 | 怎么读 |
| --- | --- |
| `www.toutiao.com/article/<编号>/`、`/video/<编号>/` | 直接读 |
| `m.toutiao.com/group/<编号>/`、`/item/<编号>/`（App 分享） | 只用来取编号，实际请求 `/article/<编号>/` |

头条自己的 robots.txt 不允许程序访问 `/group/` 和 `/item/`，所以分享地址本身不会被请求；`degraded` 里会写明读的是哪个地址。同一篇内容不同写法认成同一条，读过再读 0 积分。

## 读不了的（都不扣费）

- 微头条（`/w/` 开头的短内容）、专栏、直播页：目前不读，会返回明确的错误。
- 已删除或还在审核的内容。
- 评论：不读。

## 准备

没有 Key 也能先跑：脚本会用网站的免费看一条（每个地址每天 2 条，只给摘要）。

要完整结果：

1. 在 https://linkdigest.dev/signin?ref=skill-toutiao-to-text&next=/app/keys 登录（邮件里有 6 位验证码，也可以点链接），创建 API Key。新账户送 10 积分，不用绑卡。
2. `export LINKDIGEST_API_KEY=ld_live_...`（只放在环境变量或技能配置里，不要贴进对话）。

## 交给用户时

- 用户要「文案」：文章给 `caption` 全文；视频给 `transcript` 全文，没有口播时（`transcript_source` 为 `none`）文字在 `on_screen` 里，告诉用户视频没有人声。
- 引用要点时带上 `key_point_support` 里的原文，便于用户核对。
- 告诉用户这次用了几个积分（`credits`；缓存命中为 0）。

价格：文章 1 积分起；视频是基础 1 积分加每开始 1 分钟 1 积分（1 分钟的视频共 2 积分，4 分 15 秒共 6 积分）；只要逐字稿（`--depth transcript`）是基础 1 积分加每开始 2 分钟 1 积分。积分用完后支付宝 ¥9.9 买 50 积分，一次性、不订阅、不过期。
