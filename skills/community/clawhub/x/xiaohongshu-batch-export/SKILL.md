---
name: xiaohongshu-batch-export
description: "小红书笔记批量导出 / Xiaohongshu (RedNote) batch export to Markdown. 用户收藏了一批小红书笔记（攻略、测评、竞品、选题素材），想一次导出成文字留档或交给 AI 分析时使用。每条笔记存成一个 Markdown 文件：正文、每张图上的字（OCR）和图片描述、视频笔记的口播逐字稿、话题、互动数据、分享页热评；另附一张索引表。不登录小红书、不要 Cookie，不导出图片和视频文件。需要 LinkDigest API Key（注册送 10 积分，不用绑卡）。"
version: 1.0.0
homepage: https://linkdigest.dev/zh/xiaohongshu-biji-daochu?ref=skill-xiaohongshu-batch-export
metadata: {"openclaw":{"requires":{"anyBins":["python3"]},"primaryEnv":"LINKDIGEST_API_KEY","envVars":[{"name":"LINKDIGEST_API_KEY","required":true,"description":"LinkDigest API Key（ld_live_ 开头），在 https://linkdigest.dev/signin?ref=skill-xiaohongshu-batch-export&next=/app/keys 创建，注册送 10 积分"}],"homepage":"https://linkdigest.dev/zh/xiaohongshu-biji-daochu?ref=skill-xiaohongshu-batch-export"}}
required_environment_variables:
  - name: LINKDIGEST_API_KEY
    prompt: "LinkDigest API key (starts with ld_live_)"
    help: "https://linkdigest.dev/signin?ref=skill-xiaohongshu-batch-export&next=/app/keys"
    required_for: "reading the notes; sign-up gives 10 free credits, no card"
---

# 小红书笔记批量导出

小红书笔记的干货常常写在图片里，复制正文拿不到；一条条截图识别又太慢。这个技能把一批笔记链接整批读完：图上的字一起 OCR，视频笔记出口播逐字稿，每条存一个 Markdown 文件。

**什么时候用：** 用户发来多条 xiaohongshu.com、xhslink.com 或 rednote.com 链接（或 App 里复制的整段分享文案），说「帮我把这些笔记导出来」「存成文档」「整理成资料库」。只有一条时，用单条读取 `python3 {baseDir}/scripts/linkdigest.py "<链接>"` 更快。

**怎么跑：**

```bash
export LINKDIGEST_API_KEY=ld_live_...   # https://linkdigest.dev/signin?ref=skill-xiaohongshu-batch-export&next=/app/keys
python3 {baseDir}/scripts/batch_export.py --file notes.txt --out 防晒笔记 --label "防晒 11 月"
```

`--file` 每行一条；`--out` 是输出目录；`--label` 给批次起名，之后在控制台能找到。脚本读完才写文件，最后打印 `index.md` 路径。

**真实运行结果（2026-11-12，两条笔记）：**

```markdown
| # | 标题 | 作者 | 发布 | 点赞 | 文件 |
|---|---|---|---|---|---|
| 1 | 自进化（Self-evolving／RSI），一篇就够了 | 周星星 | 2026-07-31 |  | 01-自进化（Self-evolving／RSI），一篇就够了.md |
| 2 | 目前最稳的外贸模式 | 专注跨境 | 2026-10-30 | 6011 | 02-目前最稳的外贸模式.md |
```

第一条是 16 张图的长图文：文件里逐张列出图片描述和图上的字。点赞空着表示分享页没给这个数。

**交付给用户时：**
1. 先给 `index.md`，说明读到几条、没读到几条（没读到的不扣费，原因写在表末）。
2. 用户要分析时，把对应的 `.md` 文件交给模型，引用原话从文件里摘。
3. 报积分用量（stderr 最后一行）。

**费用：** 读过的笔记 0 积分；图文笔记 6 张图以内 1 积分；视频笔记 1 分钟 2 积分、之后每分钟加 1；读不出来 0。一批最多 10 条（Dev 套餐 50 条）。积分不够返回 402、不扣费，stderr 里有付款链接；最小积分包 50 积分 ¥9.9（支付宝），一次性、不过期。

**读不了的：** 私密、已删除、过期的分享链接（重新从 App 复制即可）；不导出图片和视频文件本身；不抓整个账号或收藏夹，只读你给的链接。

**隐私：** 只把你给的链接发给 linkdigest.dev，不要也不读小红书账号或 Cookie；图片读完即删，只留文字。https://linkdigest.dev/privacy · support@linkdigest.dev
