---
name: voc-growth-report
description: Turn exported social media comments — especially Xiaohongshu/小红书 CSV exports from 社媒助手 — into VOC insight, growth analysis, Feishu-ready operating structures, and boss-ready HTML report delivery links. Use this whenever the user wants to analyze comment CSVs, extract user sentiment/needs/commercial intent, segment audiences, build VOC reports, generate HTML decision reports, create Feishu/Bitable comment libraries, or turn comment exports into growth recommendations. Make sure to use this skill when the user mentions 社媒助手, 评论抓取, 评论CSV, VOC分析, 用户需求洞察, 商机分析, 飞书评论库, HTML报告, Trae/Cursor/Claude Code report prompts, or asks for a link instead of raw HTML code.
---

# VOC Growth Report

This skill converts exported social comment data into a repeatable growth-analysis workflow.

The core idea is simple:
1. ingest a CSV export,
2. analyze comments through a VOC + growth lens,
3. generate a boss-ready HTML report,
4. prefer delivering a preview link/path instead of dumping raw HTML.

Use this skill especially for 小红书 / 社媒助手 CSV exports, but it also works for similar social comment exports.

## What this skill should produce
Depending on the user's ask, produce one or more of these:
- a cleaned analysis brief,
- a prompt pack for Trae / Cursor / Claude Code / Codex,
- a field schema for Feishu Bitable,
- a boss-ready HTML report prompt,
- a local preview link delivery workflow.

## Default workflow

### Step 1: Confirm the real deliverable
First identify which of these the user actually wants:
- **analysis only**: sentiment / needs / intent / opportunity
- **report prompt**: a prompt for another coding agent to generate the report
- **report artifact**: a real HTML file or preview link
- **Feishu workflow**: import/sync results into Feishu / Bitable
- **skill/systemization**: package the whole VOC workflow into a reusable system

If the user says things like:
- “不要给我代码，给我链接”
- “社媒助手抓完 csv 后怎么交给 Trae”
- “给我老板能看的报告”
then optimize for **delivery**, not code verbosity.

### Step 2: Understand the input data
Identify or ask for:
- CSV path or file
- likely columns: comment text, username, time, likes, replies, post title, link, platform
- source platform / export tool
- time range / sample size if relevant

If columns differ, infer the closest mapping instead of blocking on exact names.

This skill has already been validated against a real 社媒助手 / 小红书 comment export structure with fields like:
- 评论ID
- 评论内容
- 点赞量
- 评论时间
- IP地址
- 子评论数
- 笔记ID / 笔记链接
- 用户ID / 用户链接 / 用户名称
- 一级评论ID / 一级评论内容
- 引用的评论ID / 引用的评论内容 / 引用的用户名称

### Step 3: Analyze comments in 4 layers
When doing actual VOC analysis, prefer this four-layer model:

#### 1. Emotion
Classify into:
- 正向
- 中性
- 负向

Output:
- distribution
- positive highlights
- negative complaints

#### 2. Intent
Classify into:
- 咨询价格
- 咨询功能
- 咨询购买
- 使用反馈
- 吐槽抱怨
- 夸赞认可
- 对比竞品
- 无效灌水
- 其他

Output:
- type distribution
- representative comments
- common questions

#### 3. Commercial opportunity
Classify into:
- 高
- 中
- 低
- 无

Use these definitions:
- 高：明确咨询价格、购买方式、联系方式、合作、试用、下单
- 中：明确咨询功能、效果、适用人群、区别、使用方法
- 低：普通兴趣表达、轻度认可、一般互动
- 无：灌水、无关内容、纯表情

Output:
- opportunity distribution
- top high-opportunity comments
- conversion blockers

#### 4. Need discovery
Split needs into:
- 已被满足的需求
- 未被满足的需求
- 潜在需求

Important: latent needs must be inferred from actual complaints, hesitation, comparisons, or repeated asks — never from pure imagination.

Output:
- need categories
- representative comments
- why each need is classified that way

### Step 4: Upgrade analysis into growth decisions
Do not stop at “analysis”. Convert outputs into growth decisions:
- who to prioritize,
- what pain points to solve first,
- what value propositions to amplify,
- what content topics to create,
- what sales talking points to use,
- what operations team should reply to first.

When appropriate, use a Kotler-flavored framing:
- segmentation,
- need discovery,
- value proposition mapping,
- conversion opportunity,
- growth actions.

## Default report structure
For boss/CEO-ready reports, prefer this structure:

1. 封面 / 数据概况
2. 用户情绪总览
3. 用户分群分析
4. 用户需求图谱
5. 商机与转化机会
6. 价值主张与增长建议
7. CEO Summary

## Delivery-first rule
If the user wants a usable deliverable, do **not** stop at raw HTML code.
Prefer to instruct the coding agent / ACP harness to:
1. generate the HTML,
2. save it to a file,
3. start a local static preview,
4. return a preview link and file path.

Use language like:
- “你的任务不是输出源码，而是完成交付”
- “最终返回访问链接、本地文件路径、报告标题、简短说明”

## Output modes

### Mode A: Prompt pack
When the user wants something to paste into Trae / Cursor / Claude Code / Codex, provide:
- one consolidated instruction block,
- explicit input/output contract,
- delivery requirement: link > raw code.

### Mode B: Feishu workflow
When the user wants Feishu integration, provide:
- comment library field schema,
- suggested analysis fields,
- optional Bitable views,
- minimal workflow from CSV/comment sync to reporting.

Recommended 12-field base schema:
- 平台
- 帖子标题
- 帖子链接
- 评论内容
- 评论用户
- 评论时间
- 情绪倾向
- 意图类型
- 商机等级
- 是否需要回复
- 跟进状态
- 备注

### Mode C: Executive summary
For direct advice in chat, use this order:
1. conclusion,
2. why,
3. next action.

Keep it concise and business-oriented.

## Example trigger cases
- “帮我把社媒助手抓下来的评论 csv 做成老板能看的报告”
- “不要给我 html 代码，我要最终链接”
- “帮我做小红书 voc 分析”
- “把评论做成需求洞察 + 商机分析”
- “给 Trae 一段完整指令，从 csv 到 html 报告链接”
- “封装一个 VOC 分析 skill”

## Anti-patterns
Avoid these mistakes:
- stopping at sentiment only,
- giving a word cloud as the main output,
- dumping raw HTML when the user asked for delivery,
- inventing latent needs with no textual basis,
- overcomplicating the workflow before the CSV/report path is usable.

## Success standard
A strong result should make it easy for the user to go from:
**comment export → user insight → growth decisions → report delivery**
with minimal repeated prompting.

A stronger result should also be capable of producing a real executive-facing HTML demo report with sections such as:
- 封面 / 数据概况
- 用户情绪总览
- 用户分群分析
- 用户需求图谱
- 商机与转化机会
- 价值主张与增长建议
- CEO Summary
