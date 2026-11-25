---
name: xiaohongshu-daily-draft
description: "小红书 / 抖音赛道日报 + 照着就能发的稿：告诉它一个赛道，每天固定时间读赛道里最火的新帖、排热榜、写对比，再按你的口吻写一篇稿（标题三选一、正文、话题、封面文字，每个数字都来自笔记），发到邮箱并附可分享的链接。用户说「每天帮我看 XX 赛道」「帮我写今天的小红书稿」「订阅赛道日报」「下一篇发什么」时使用。每次约 7–12 积分，没有新帖那天不扣费；注册送 10 积分，先免费体检一次自己的账号。不碰用户账号，不替用户发。"
version: 1.0.0
homepage: https://linkdigest.dev/zh/docs?ref=skill-xiaohongshu-daily-draft
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-xiaohongshu-daily-draft&next=/app/keys 创建，注册送 10 积分"}],"homepage":"https://linkdigest.dev/zh/docs?ref=skill-xiaohongshu-daily-draft"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_)"
    help: "https://linkdigest.dev/signin?ref=skill-xiaohongshu-daily-draft&next=/app/keys"
    required_for: "every call: a watch runs on the account's credits"
---

# Xiaohongshu daily draft / 赛道日报 + 成稿

> 每天早上，稿已经写好了。告诉 LinkDigest 你的赛道，每天固定时间：搜赛道里的新帖 → 读最火的 5 条（读不了的自动换下一条，不扣费）→ 按 赞 + 2×收藏 + 评论 排热榜 → 写一页对比 → 照着写一篇你能直接发的稿，用你自己的口吻。稿里每个数字都必须出现在读到的笔记里，否则那句会被删掉（代码里的硬规则，不是提示词）。结果发到账号邮箱，附可分享的链接。

## 什么时候用

- 「每天帮我看看露营装备这个赛道」「订阅考研英语的日报」「每天早上给我一篇可以发的稿」。
- 「下一篇发什么」「照着赛道里最火的写一篇」「把这几条读完写一篇我的」（一次性的，用 `draft` 子命令）。
- 自己的账号为什么没人看：先体检（`checkup` 子命令），贴 3–5 条自己的笔记。

## 什么时候不用

- 想自动发布、自动回评、养号：这个技能不发布、不碰账号。稿写好后由人自己发（Chrome 扩展可以预填发布页，发布仍由人点）。
- 要实时热搜：日报每天一次；要即时搜索用 `douyin-search-to-text` 或 `search_links`。

## 准备（一次）

1. 打开 https://linkdigest.dev/signin?ref=skill-xiaohongshu-daily-draft&next=/app/keys ，登录并创建 API Key（`ld_live_` 开头）。注册送 10 积分，不用绑卡。
2. `export LINKDIGEST_API_KEY=ld_live_...`（或写进 OpenClaw 配置里这个技能的 `env`）。Key 只放在环境变量或配置里，不要贴进对话。

## 用法

```bash
# 订阅一个赛道（第一次马上跑；默认北京时间早上 9 点送达）
python3 {baseDir}/scripts/watch.py add "露营装备 推荐" --platform xiaohongshu --voice "家人们，我是刚开始露营的小白……" --hour-utc 1 --reads 10

# 看看订阅了什么、上次跑的结果和分享链接
python3 {baseDir}/scripts/watch.py list

# 立刻跑一次 / 暂停 / 继续 / 删除
python3 {baseDir}/scripts/watch.py run <watch_id>
python3 {baseDir}/scripts/watch.py pause <watch_id>
python3 {baseDir}/scripts/watch.py resume <watch_id>
python3 {baseDir}/scripts/watch.py delete <watch_id>

# 一次性：搜一个话题，读完，写一篇稿（不订阅）
python3 {baseDir}/scripts/watch.py draft "露营装备 推荐" --platform xiaohongshu --voice "……"

# 账号体检：贴 3–5 条自己的笔记，读完、排热榜、写对比、写下一篇
python3 {baseDir}/scripts/watch.py checkup "https://www.xiaohongshu.com/explore/…?xsec_token=…" "https://xhslink.com/…"
```

`--platform xiaohongshu` 出图文稿；`--platform douyin` 搜抖音、出口播稿。`--voice` 贴一两条用户自己写过的笔记，稿就按那个口吻写。

## 返回什么

`add` 返回 `watch_id`、`next_run_at`。`list` 里每个 watch 的 `last` 有 `outcome`（page / nothing_new / credits_short / search_failed / batch_failed）、`new_posts`、`credits`、`batch_id`、`share_url`。`draft` 和 `checkup` 轮询到批次完成后打印稿：标题三选一、正文、话题、封面文字，以及 `made_by`（model / model_retry / fallback——两次都写了笔记里没有的数字时退回到笔记自己的标题和要点）和热榜。

## 价格与边界

- 每次日报 ≈ 搜索 2 + 读 3–5 条（图文 1–3 积分一条）+ 对比 1 + 成稿 1，7–12 积分；没有新帖那天不扣费也不发邮件；积分不够那天发一封提醒，第二天再试。
- 免费账号可订阅 1 个赛道，Dev 5 个，Studio 20 个（超出返回 402 `watch_limit`）。
- 网页搜索收录的小红书笔记有限：冷门赛道一天只有两三条新帖，稿就只能照着这几条写。
- 不登录平台账号、不要 Cookie、不发布、不回评。

文档：https://linkdigest.dev/zh/docs?ref=skill-xiaohongshu-daily-draft · 价格：https://linkdigest.dev/pricing
