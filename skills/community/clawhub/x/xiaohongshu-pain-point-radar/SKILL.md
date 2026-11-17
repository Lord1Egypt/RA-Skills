---
name: xiaohongshu-pain-point-radar
description: "痛点雷达 / Pain-point radar for Xiaohongshu + Douyin. 给一个产品、品类或品牌：先看百度、淘宝、Bing 的搜索联想（大家在搜什么），再读小红书和抖音上排在前面的内容和热门评论，把相同的痛点、需求、购买顾虑归到一起，由代码数出每一条出现在几篇里（N/M 篇），每条附逐字核对过的原话；有人在搜、读到的内容都没讲的列成「机会」；同一个话题再跑会告诉你变了什么。用于选品、新品立项、写卖点、看竞品口碑、找内容选题。速查 12 篇约 47 积分（每篇最多 5 积分，读过的 0 积分）。不登录小红书、不要 Cookie。需要 LinkDigest API Key（注册送 10 积分，¥9.9 支付宝 50 积分）。"
version: 1.0.0
homepage: https://linkdigest.dev/zh/tongdian-leida?ref=skill-xiaohongshu-pain-point-radar
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-xiaohongshu-pain-point-radar&next=/app/keys 创建，注册送 10 积分"}],"homepage":"https://linkdigest.dev/zh/tongdian-leida?ref=skill-xiaohongshu-pain-point-radar"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_)"
    help: "https://linkdigest.dev/signin?ref=skill-xiaohongshu-pain-point-radar&next=/app/keys"
    required_for: "searching and reading Xiaohongshu and Douyin posts and counting the pain points; sign-up gives 10 free credits, no card"
---

# 痛点雷达（小红书 + 抖音）

做选品、做新品、写内容之前，先回答三个问题：大家在**搜**什么？在**抱怨**什么？有什么**还没人回答**？这个技能一次跑完，结果按「出现在几篇里」排好，每一条都能点回原帖。

## 一条命令

```bash
export LINKDIGEST_API_KEY=ld_live_...   # https://linkdigest.dev/signin?ref=skill-xiaohongshu-pain-point-radar&next=/app/keys
python3 {baseDir}/scripts/radar.py "扫地机器人"
```

- `--size standard`（24 篇）/ `--size deep`（48 篇），默认速查 12 篇。
- `--preview`：只看搜索需求词（1 积分），先判断这个品类值不值得细看。
- `--weekly`：每周自动再跑一次，新出现的痛点和搜索词单独列出来。
- `--format json`：结构化结果；`--radar-id <id>`：接着取一次已开始的雷达，不重复扣费。
- 一次通常 10–20 分钟（读取在服务端排队），脚本自己等；超时会给出 `--radar-id`。

## 一次返回什么

| 部分 | 字段 | 说明 |
| --- | --- | --- |
| 痛点 | `sections.pain` | 抱怨、故障、后悔，每条 `count_posts`/读到的篇数 |
| 需求与卖点 | `sections.needs` | 大家看重的点、帖子在夸的点（热门帖可能是商业合作） |
| 购买顾虑 | `sections.blockers` | 价格、信任、适不适合、安装等卡住购买的原因 |
| 被点名的产品 | `sections.products` | 品牌和型号，按出现篇数 |
| 没人回答的问题 | `sections.open_questions` | 评论和帖子里的提问 |
| 搜索需求 | `sections.demand` | 百度 / 淘宝 / Bing 联想词，按需求分组（选购、值不值、对比、价格、故障、场景） |
| 机会 | `sections.gaps` | 有人在搜、读到的帖子都没讲的问题 |
| 变化 | `diff` | 和上一次同话题相比：新出现的、上升的、消失的、新的搜索词 |

**计数是代码数的，不是模型说的**：模型只负责把说同一件事的原话归到一组，篇数由代码按帖子编号去数。每条原话都是引擎在帖子正文、图上文字、口播或热评里逐字找到的（`verified: true`）。和品类无关的帖子（同名的游戏、段子）会被剔除，`missing` 里写明剔除了哪几篇。

真实运行（2026-11-07，「扫地机器人」速查，12 篇）：2 篇是同名游戏的视频，被剔除；需求「热水洗拖与高温除菌」8/10 篇、「强力避障与防缠绕」6/10 篇；顾虑「价格敏感与售后疑虑」4/10 篇；机会里有「值不值：智商税」「对比：云鲸和石头对比」「场景：尺寸预留」——大家在搜，读到的帖子没讲。

## agent 怎么用

1. 用户问「这个品类大家在吐槽什么」「做 XX 有什么机会」「竞品口碑怎么样」时跑它；先 `--preview` 也可以。
2. 回答时引用 `count_posts/posts`，原话只用返回里的 `quotes`，并给出原帖链接（`notes[n-1].url`）。
3. 说明样本：只读了公开搜索排在前面的 N 篇，不代表全平台；热门帖子可能有商业合作。
4. 告诉用户这次花了多少积分（stderr 最后一行）和分享链接（30 天有效）。

## 费用

两次搜索（小红书、抖音各 4 积分）+ 每篇读取和洞察（每篇最多 5 积分，读过的 0 积分）+ 汇总 3–6 积分。速查 12 篇约 47 积分。积分不够时返回 402、不扣费，返回体里有 ¥9.9 买 50 积分（支付宝，一次性，不订阅）的链接。少于 3 篇读成时不汇总、不收汇总费。

## 读不到的

私密、已删除、需要登录才能看的帖子；抖音的评论文字（抖音只给评论数）；分享页以外的评论（只读分享页自带的热评，不翻页）。

## 隐私

只把你给的品类词发给 linkdigest.dev，不要也不读任何小红书、抖音账号或 Cookie。https://linkdigest.dev/privacy · 品类库（每周更新的公开样例）：https://linkdigest.dev/zh/tongdian-leida · support@linkdigest.dev
