---
name: xiaohongshu-search-to-text
description: "小红书按话题搜笔记再读成文字 / Search Xiaohongshu (RedNote) by topic, then read the notes. 给一个话题（如 成都 咖啡店、通勤穿搭、skincare routine），返回网页已收录的小红书笔记链接和标题；再挑几条读出正文、每张图上的文字（OCR）和描述、分享页热评、要点和点赞收藏数。用于选品调研、看同行、找达人、整理用户怎么评价。搜到笔记每次 4 积分（搜不到不扣）；读一条图文笔记 1 积分起。不登录小红书、不要 Cookie。需要 LinkDigest API Key（注册送 10 积分，不用绑卡）。"
version: 1.0.1
homepage: https://linkdigest.dev/zh/xiaohongshu-shichang-diaoyan?ref=skill-xiaohongshu-search-to-text
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-xiaohongshu-search-to-text&next=/app/keys 创建，注册送 10 积分"}],"homepage":"https://linkdigest.dev/zh/xiaohongshu-shichang-diaoyan?ref=skill-xiaohongshu-search-to-text"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_)"
    help: "https://linkdigest.dev/signin?ref=skill-xiaohongshu-search-to-text&next=/app/keys"
    required_for: "searching and reading Xiaohongshu; sign-up gives 10 free credits, no card"
---

# 小红书搜索 → 文字

小红书自己的搜索要登录，agent 直接打开笔记链接也只拿到一个"打开 App"的壳。这个技能分两步：先按话题找到网页已收录的公开笔记，再把挑中的几条读成文字——正文、每张图上的字、分享页上的热评。

## 用法

```bash
export LINKDIGEST_API_KEY=ld_live_...   # https://linkdigest.dev/signin?ref=skill-xiaohongshu-search-to-text&next=/app/keys
python3 {baseDir}/scripts/xhs_search.py "成都 咖啡店"            # 列出笔记（找到时 4 积分）
python3 {baseDir}/scripts/xhs_search.py "成都 咖啡店" --read 3   # 再读前 3 条
python3 {baseDir}/scripts/xhs_search.py "skincare routine" --format json
```

单独读一条链接：`python3 {baseDir}/scripts/linkdigest.py "<小红书链接或整段分享文案>"`。

## 每条笔记读回来什么

- 标题、作者、发布时间、正文和话题标签
- 图文笔记：每张图的描述，以及图上的文字（OCR），按图排列
- 视频笔记：口播逐字稿和画面上的字
- 分享页上能看到的热评（不翻页、不登录）
- 要点，每条都能在原文里找到出处；点赞、收藏、评论数（读取当天）

## 给 agent 的流程

1. 用用户的话题搜索；中文越具体越好（"吉隆坡 咖啡馆 探店" 比 "咖啡" 好）。
2. 把列表给用户看；用户说"读前 3 条"就 `--read 3`，否则问读哪几条。
3. 读完后：用户要原文就给原文；要总结就基于读回来的文字总结，并标出来自哪条笔记。
4. 告诉用户花了多少积分（stderr 最后一行）。

## 费用

| 动作 | 积分 |
| --- | --- |
| 搜索找到笔记 | 4 |
| 搜索没找到 | 0 |
| 图文笔记（6 张图以内） | 1 |
| 视频笔记 | 1 分钟 2，之后每分钟加 1 |
| 别人读过的链接 | 0 |
| 读不出来 | 0 |

积分不够时返回 402，不扣费，stderr 里有付款链接。最小的积分包 50 积分 ¥9.9（支付宝）或 $1.50，一次性、不订阅、不过期；250 积分 ¥36。

## 限制，照实说

- 搜的是网页已收录的小红书公开笔记，不是小红书 App 里的搜索，不保证最全、也不按热度排。
- 小红书有时会对自动读取加验证码；遇到时读取会自动等一等再试，还是读不到就返回 503，不扣费，稍后再试。
- 读不了：私密、已删除、需要登录才能看的笔记；不看完整评论区；不下载图片或视频。
- 自己的信息流或收藏夹：用 LinkDigest 浏览器扩展在自己的页面上读（https://linkdigest.dev/extension）。

## 隐私

只把话题和挑中的链接发给 linkdigest.dev。从不要求、也不读取小红书账号、Cookie 或登录态。图片和视频读完即删，只保留文字结果。https://linkdigest.dev/privacy

也可以接远程 MCP：`https://linkdigest.dev/mcp`（工具 `search_links`、`digest_url`）。问题发 support@linkdigest.dev。
