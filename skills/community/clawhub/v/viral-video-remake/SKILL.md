---
name: viral-video-remake
description: "爆款同款视频：给一条抖音、小红书、B站、TikTok 或 YouTube 爆款链接，先读出逐字稿和画面文字并拆成开头钩子、带时间的结构节拍、标题公式、封面文字和行动号召，再生成一份「只借结构、内容用你自己的」同款视频脚本说明，交给你已经装好的视频 skill（HyperFrames、huashu-art-motion、lemo-opuscar 等）去做。用户说「做同款」「照着这条爆款做一条」「仿这个结构做视频」时使用。通过 LinkDigest API 读取，不需要平台账号或 Cookie；需要 LINKDIGEST_API_KEY，在读取费用上加 1 积分拆解。"
version: 1.0.0
homepage: https://linkdigest.dev/zh/docs?ref=skill-viral-video-remake
metadata: {"openclaw":{"requires":{"env":["LINKDIGEST_API_KEY"],"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-viral-video-remake&next=/app/keys 创建"}],"homepage":"https://linkdigest.dev/zh/docs?ref=skill-viral-video-remake"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_)"
    help: "https://linkdigest.dev/signin?ref=skill-viral-video-remake&next=/app/keys"
    required_for: "reading the post and its breakdown"
---

# 爆款同款视频（读懂对标 → 同款脚本 → 交给视频 skill）

> 脚本路径 `scripts/` 相对于本技能目录。只用 Python 3.8+ 标准库。

现在用 Claude Code、WorkBuddy 这类 agent 加一个视频 skill 就能写代码出视频，难的是**拍什么、怎么开头、节奏怎么排**。这个技能把一条已经火了的视频读透，拆成结构，再写成一份能直接交给视频 skill 的同款脚本说明：

1. 读：逐字稿、屏幕字、画面要点（不用下载视频，不需要平台账号）。
2. 拆：开头 3 秒的钩子（说了什么、屏幕上写了什么、画面是什么、为什么有效）、带时间的结构节拍、标题公式、封面文字、行动号召、可复用模板。拆解里标成原话的引用都和原文逐字核对过。
3. 写说明：时长按原视频取整；**只借结构和节奏，主题、例子和画面换成你自己的**，并要求先给你看口播稿和分镜再渲染。

## 什么时候用

- 「照着这条爆款做一条同款」「这个结构帮我做一版我的产品」「用 huashu-art-motion / HyperFrames 做一条类似的视频」。
- 做账号前先研究几条对标，挑一条结构最适合自己的来做。

## 什么时候不用

- 想原样搬运、换个配音就发：这个技能不做，也会在说明里写明不要用原视频的台词和画面。
- 只要文案：用 `linkdigest-video-transcript`，少花 1 积分。
- 私密、已删除、需要登录才能看的内容读不了（返回 422，不扣费）。

## 准备（一次）

在 https://linkdigest.dev/signin?ref=skill-viral-video-remake&next=/app/keys 登录并创建 API Key（`ld_live_` 开头），然后：

```bash
export LINKDIGEST_API_KEY=ld_live_...
```

Key 只放在环境变量或配置里，不要贴进对话、代码或提交记录。

## 用法

```bash
# 1. 读 + 拆解（视频用逐字稿优先，便宜一半；拆解 +1 积分）
python3 scripts/linkdigest.py "<爆款链接或整段分享文案>" --breakdown --depth transcript --format json > post.json

# 2. 写同款脚本说明（--topic 写你自己的主题；英文说明加 --lang en）
python3 scripts/remake_brief.py post.json --topic "我们的露营推车，三秒展开"
```

第 2 步打印的说明，原样交给你装好的视频 skill（比如对 Claude Code 说「用 hyperframes 按下面的说明做」，后面贴说明）。说明的结构：

```
帮我做一条约 60 秒的视频，参考一条已经验证过的爆款的结构：「…」（douyin）。
只借它的结构、节奏和钩子的写法；不要用原视频的台词、画面和图片——主题、例子和画面都用我自己的。

我的主题：我们的露营推车，三秒展开

开头钩子（前 3 秒）——原视频是这样起作用的：
- 说的：…
- 屏幕字：…
- 画面：…
- 为什么有效：…

结构节拍（顺序和大致时间照着来，按我的时长缩放）：
1. [0:00] 钩子——…
2. [0:12] …

标题公式：…
封面文字的写法：…
结尾行动号召：…
目标人群：…

先写口播稿给我看，再出分镜，最后再渲染。
```

- 视频较长时第 1 步先返回 202，脚本自动轮询；退出码 4 是积分不够或超长（未扣费），5 是链接读不了（未扣费）。
- 同一条链接读过以后再读不收读取费，拆解有缓存时也不再收费。

## 注意

- 结构可以学，内容要原创：说明里不带原视频的画面和图片，原话引用只用来理解钩子，不要直接放进你的视频。
- 拆解是对一条内容的分析，不保证你的同款也会火。
