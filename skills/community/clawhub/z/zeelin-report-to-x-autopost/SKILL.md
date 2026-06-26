---
name: ZeeLin Report-to-X AutoPost
description: >
  Automatically picks the latest unposted report from a report website or JSON feed, drafts an English X/Twitter post summarizing the report, publishes it via the logged-in X web session, records posted ids to avoid duplicates, and can be scheduled with OpenClaw cron. Use when the user wants daily report-to-X posting, website report promotion, non-repeating social posting from a report list, or automated sharing of research/report updates to X.
user-invocable: true
metadata: {"openclaw":{"emoji":"📰","skillKey":"zeelin-report-to-x-autopost"}}
---

# ZeeLin Report-to-X AutoPost 📰

把“报告网站/报告 JSON 列表 → 选最新未发报告 → 生成英文推文 → 发布到 X → 记录已发状态避免重复”封成一个可复用工作流。

适合场景：
- 每天自动发一篇报告到 X
- 从一个固定网站持续推广最新报告
- 同一批报告只发一次，不重复
- 需要通过网页端 X 发布，而不是 API

## 何时触发

当用户表达类似需求时使用：
- 「把这个报告网站每天发到我的推特」
- 「自动把最新报告发到 X」
- 「一天一个报告，不要重复」
- 「从 JSON / 网站里抓报告然后自动发推」
- 「帮我把报告站做成自动社媒分发」

## 默认工作原则

1. **优先从结构化列表读取**：先找 `reports_config.json`、RSS、JSON、静态配置，再考虑网页渲染内容
2. **先去重，再发帖**：发布前必须检查本地 state 文件，避免重复发同一篇
3. **先摘要，再发布**：推文应简洁介绍报告核心内容，并附源站网址
4. **默认英文发帖**：除非用户要求中文或双语
5. **网页端发 X，不碰密码**：用户需提前登录 X 网页版
6. **定时任务用 cron**：日更/周更统一用 OpenClaw cron 管理

## 推荐目录结构

```text
skill/
├── SKILL.md
└── scripts/
    └── post_daily_report.py
```

## 一次性发布流程

### Step 1：确认数据源
优先确认报告源是否存在结构化入口，例如：
- `reports_config.json`
- RSS / Atom
- sitemap / JSON API
- 站点静态配置 JS 中引用的 JSON

如果是前端渲染站点，不要急着浏览器点击；先从 HTML/JS 中找数据源。

### Step 2：挑选未发过的最新报告
- 读取报告列表
- 加载本地状态文件（例如 `memory/report-post-state.json`）
- 找到第一个未发过的报告
- 如果没有未发报告，就停止，不要硬发旧内容

### Step 3：生成推文
推文建议结构：
- 第一行：`Today's report: {title}`
- 第二段：1–2 句总结核心价值
- 最后一行：站点首页 URL（必要时可补具体报告 URL）

要求：
- 280 字符内
- 避免夸张营销腔
- 不要与上一条高度重复

### Step 4：调用现成的 X 发帖脚本
优先复用已有网页端 X 发帖脚本，例如：

```bash
bash /path/to/tweet.sh "tweet text" https://x.com
```

如果发帖成功：
- 立刻把报告 id 写入 state 文件

如果失败：
- 不要写入已发状态
- 把错误保留下来，方便重试

## 定时发布流程

用户要求“每天一条、不重复”时：
- 创建本地脚本处理“读取报告列表 + 去重 + 生成推文 + 发布 + 更新状态”
- 再用 `cron` 建每日任务

推荐时间：
- `Asia/Shanghai` 每天上午 10:00

## 状态文件建议

用 JSON 保存已发报告 id，例如：

```json
{
  "posted": [
    "report-id-1",
    "report-id-2"
  ]
}
```

## 关键防错规则

1. **只有发帖成功后才能记录已发状态**
2. **如果找不到新报告，直接退出，不要重复发旧文**
3. **如果网站是 React/Vue 前端渲染，先找 JSON 数据源，不要一上来就人工点网页**
4. **如果用户指定“不要重复”，就必须持久化状态到文件**
5. **推文要附网址，默认附站点首页；用户要求更细时可附具体报告链接**

## 最小可复用脚本

这个 skill 适合把通用逻辑写进 `scripts/post_daily_report.py`：
- 拉取远程报告列表
- 读/写状态文件
- 生成 tweet 文本
- 调用现有 tweet.sh

## 回报格式

完成后告诉用户：
- 今天发的是哪篇报告
- 是否已成功发到 X
- 定时任务是否创建成功
- 下次运行时间

TL;DR：
- 先找结构化报告列表
- 再选最新未发
- 生成英文推文 + 附网址
- 通过网页端 X 发出
- 记录状态避免重复
- 日更用 cron 挂起来
