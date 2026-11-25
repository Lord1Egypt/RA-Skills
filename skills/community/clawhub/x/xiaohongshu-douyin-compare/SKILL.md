---
name: xiaohongshu-douyin-compare
description: "小红书/抖音多条笔记对比分析 / Compare several Xiaohongshu, Douyin, TikTok or YouTube posts in one page. 用户丢来一批对标账号、竞品或爆款的链接（2–10 条，可混平台），想知道它们有什么共同主题、开头钩子、内容形式、共同卖点、评论区的顾虑、还有谁都没讲的空白时使用。每条先读成文字（正文、图上文字、逐字稿、热评），再写一页对比，每个例子标明出自第几条并逐字核对。读过的链接 0 积分，新链接按单条计费，对比每 10 条 1 积分。不登录、不要 Cookie。需要 LinkDigest API Key（注册送 10 积分，不用绑卡）。"
version: 1.0.2
homepage: https://linkdigest.dev/zh/duibiao-zhanghao?ref=skill-xiaohongshu-douyin-compare
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-xiaohongshu-douyin-compare&next=/app/keys 创建，注册送 10 积分"}],"homepage":"https://linkdigest.dev/zh/duibiao-zhanghao?ref=skill-xiaohongshu-douyin-compare"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_)"
    help: "https://linkdigest.dev/signin?ref=skill-xiaohongshu-douyin-compare&next=/app/keys"
    required_for: "reading and comparing posts; sign-up gives 10 free credits, no card"
---

# 一批链接 → 一页对比

做对标、看竞品、拆爆款，难的不是读一条，而是把十条放在一起看出规律。这个技能把一批小红书、抖音、TikTok、YouTube、B站 链接逐条读成文字，再写一页对比。

## 先看结果长什么样

下面是一次真实运行的节选（3 条：一条成都美食小红书图文、一条吉隆坡茨厂街抖音视频、一条游戏实况 B站视频）：

```markdown
## 批量综合

_3 篇笔记_

本批次涵盖美食探店、城市旅游与文化、游戏实况吐槽……

### 钩子

- 情感/遗憾开场 (1/3) — ✓ #1 “错过了露思宝宝请客”
- 描述性/定义式开场 (1/3) — ✓ #2 “吉隆坡的唐人街：茨厂街，热闹非凡”

### 读者顾虑

- 口味稳定性担忧 (1/3) — ✓ #1 “好多人说分店口味不稳定”
```

- `(1/3)` 是出现在几条里，靠例子撑得住才算数。
- `#1` 是第几条链接；`✓` 表示这句引文在那条原文里逐字找到了，`✗` 表示没找到，别当原话用。

## 怎么跑

```bash
export LINKDIGEST_API_KEY=ld_live_...   # https://linkdigest.dev/signin?ref=skill-xiaohongshu-douyin-compare&next=/app/keys
python3 {baseDir}/scripts/compare.py "<链接1>" "<链接2>" "<链接3>"
python3 {baseDir}/scripts/compare.py --file links.txt --label "防晒对标 10 月"
python3 {baseDir}/scripts/compare.py "<链接1>" "<链接2>" --format json
```

- 链接可以是完整地址、短链（xhslink、v.douyin.com），或从 App 复制的整段分享文案。
- 脚本提交后每几秒查一次进度，读完、对比写完才打印。视频多的话要几分钟。
- 只读一条用 `python3 {baseDir}/scripts/linkdigest.py "<链接>"`。

## agent 什么时候用、怎么交付

用户说"帮我看看这几个账号/这几条爆款有什么共同点""对比一下这几条""竞品都在讲什么"，并且给了 2 条以上链接时用。

1. 链接不够 2 条，先问要不要补，或者改用单条读取。
2. 跑完后，先给用户对比页，再按用户的问题挑重点（比如"开头怎么写"就讲钩子那一节）。
3. 引用原话时只用带 `✓` 的；`✗` 的要说明没核对上。
4. 告诉用户花了多少积分（stderr 最后一行），以及哪几条没读到（没读到的不扣费）。

## 花多少积分

拿 6 条链接举例：2 条之前有人读过（0），3 条图文笔记（各 1），1 条 1 分钟视频（2），对比 1。合计 6 积分，约 ¥1.2。

- 读过的链接：0
- 图文笔记 6 张图以内：1
- 视频：1 分钟 2，之后每分钟加 1
- 对比：每开始 10 条 1 积分，整批只收一次；对比写失败不收
- 读不出来的链接：0

一次最多 10 条（Dev 套餐 50 条）。积分不够返回 402，不扣费，stderr 里有付款链接。最小积分包 50 积分 ¥9.9（支付宝），一次性、不订阅、不过期。

## 读不了的

私密、已删除、要登录才能看的帖子；完整评论区（只看分享页上的热评）；平台临时加验证码时会返回"没读到"并且不扣费，可以过一会儿再跑同一批。

## 隐私

只把你给的链接发给 linkdigest.dev，不要也不读任何平台账号或 Cookie。图片和视频读完即删，只留文字结果。https://linkdigest.dev/privacy

也可以接远程 MCP：`https://linkdigest.dev/mcp`，工具 `compare_links`。问题发 support@linkdigest.dev。
