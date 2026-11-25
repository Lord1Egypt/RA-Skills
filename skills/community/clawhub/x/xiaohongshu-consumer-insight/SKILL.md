---
name: xiaohongshu-consumer-insight
description: "小红书消费者洞察 / Xiaohongshu consumer insight. 给一条小红书笔记链接，读出正文、每张图上的字和分享页热评，再整理成：这条笔记在跟谁说话（受众）、讲了哪些卖点、读者有什么顾虑和吐槽、有没有购买意向、提到的产品和价格、读者在问什么——每一条都附一句在原文里逐字核对过的引用。用于选品、看竞品口碑、写卖点、找用户痛点。读笔记 1 积分起，洞察 +1 积分；同一条再看免费。不登录小红书、不要 Cookie。需要 LinkDigest API Key（注册送 10 积分，不用绑卡）。"
version: 1.0.2
homepage: https://linkdigest.dev/zh/xiaohongshu-shichang-diaoyan?ref=skill-xiaohongshu-consumer-insight
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-xiaohongshu-consumer-insight&next=/app/keys 创建，注册送 10 积分"}],"homepage":"https://linkdigest.dev/zh/xiaohongshu-shichang-diaoyan?ref=skill-xiaohongshu-consumer-insight"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_)"
    help: "https://linkdigest.dev/signin?ref=skill-xiaohongshu-consumer-insight&next=/app/keys"
    required_for: "reading Xiaohongshu notes and writing the consumer insight; sign-up gives 10 free credits, no card"
---

# 小红书消费者洞察

一条笔记能告诉商家的，不只是「它说了什么」，还有「谁在看、他们担心什么、想不想买」。这个技能把一条小红书笔记读完（正文、每张图上的字、分享页上的热评），再按六个问题整理，每个结论都带一句原文。

## 一条命令

```bash
export LINKDIGEST_API_KEY=ld_live_...   # https://linkdigest.dev/signin?ref=skill-xiaohongshu-consumer-insight&next=/app/keys
python3 {baseDir}/scripts/linkdigest.py "<小红书链接或整段分享文案>" --insight
```

还想就这条笔记问一个具体问题：加 `--ask "她觉得哪道菜最值得点？"`（+1 积分，回答附依据的原文）。要结构化数据：加 `--format json`，洞察在 `insight` 字段。

## 六个问题

| 问题 | 字段 | 返回什么 |
| --- | --- | --- |
| 在跟谁说话 | `audience` | 作者在对谁说、以什么身份说 |
| 讲了哪些卖点 | `claims` | 帖子主张的好处和承诺 |
| 读者担心什么 | `objections` | 顾虑、吐槽、踩雷点 |
| 想不想买 / 去 | `purchase_intent` | 表达购买或想去的原话 |
| 提到哪些产品、多少钱 | `products` | 产品名和价格（帖子里写了才有） |
| 读者在问什么 | `questions` | 评论里的提问（没有热评时为空） |

真实运行（2026-10-28，一条怡保茶楼探店笔记）里的两条：`audience` 引了「身为怡保人」——本地人写给游客；`objections` 引了「繁忙时间是需要排队」。

每一条都是 `{text, quote, verified}`：`quote` 是从笔记正文、图上文字或热评里原样摘出来的，`verified: true` 表示代码在原文里逐字找到了它。帖子里没有的东西不会编出来——空着，并在 `missing` 里说明为什么判断不了。

## agent 怎么用

1. 用户给笔记链接、问「大家怎么评价」「卖点是什么」「有什么槽点」时，带 `--insight` 跑。
2. 回答时按用户的问题挑字段，引用只用 `verified: true` 的原话，并说明来自正文、图片还是评论。
3. 多条笔记要一起看：一条条跑完再汇总，或者用 `xiaohongshu-douyin-compare` 技能出一页对比。
4. 告诉用户这次花了多少积分（stderr 最后一行）。

## 费用

图文笔记 6 张图以内 1 积分，视频笔记按分钟；洞察 +1 积分，问答 +1 积分。同一条笔记已经有人读过、洞察也写过，再看 0 积分；读不出来不扣费。积分不够时返回 402、不扣费，返回体里有中文付款说明：¥9.9 买 50 积分（支付宝），一次性、不订阅、不过期。

## 读不到的

私密、已删除、需要登录才能看的笔记；分享页上没有的评论（只读分享页自带的热评，不翻页）。热评少的笔记，`questions` 和 `purchase_intent` 可能是空的，这是如实反映，不是失败。

## 隐私

只把你给的链接发给 linkdigest.dev，不要也不读任何小红书账号或 Cookie；图片读完即删，只留文字结果。https://linkdigest.dev/privacy · 远程 MCP：`https://linkdigest.dev/mcp`（`digest_url` 带 `insight: true`）· support@linkdigest.dev
