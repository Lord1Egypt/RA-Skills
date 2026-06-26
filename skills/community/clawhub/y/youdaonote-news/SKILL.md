---
name: youdaonote-news
version: '1.7.8'
description: 有道云笔记资讯推送：基于收藏笔记分析关注话题，推送最新相关资讯。支持对话触发与每日定时推送（如早上9点）。触发词:资讯推送、设置资讯推送、生成资讯推送。
metadata: {"openclaw": {"emoji": "📰", "requires": {"bins": ["node", "mcporter", "jq"], "env": ["YOUDAONOTE_API_KEY"]}, "primaryEnv": "YOUDAONOTE_API_KEY"}}
---

# YoudaoNote News — 有道云笔记资讯推送

基于最近收藏提取关注话题并推送资讯。对话触发或定时（默认 9:00）；依赖见 metadata。

**触发词**：生成 — 资讯推送、最近关注、热点推送、每日简报、生成资讯推送、帮我整理收藏的简报；设置 — 设置/开启/资讯推送设置；修改时间 — 修改资讯推送时间；关闭 — 关闭/取消资讯推送。

> **Context 管控**：每步完成后只保留结构化摘要，立即丢弃原始输出（笔记全文、搜索原始响应），避免 context 溢出。

## 核心工作流

收到资讯推送请求后按 Step 1～5 执行。

### Step 1：获取最近收藏的笔记内容

```bash
bash {baseDir}/get-favorite-notes.sh
```

默认 30 条、每条正文截断 500 字，总量 ≤45KB。可选：`get-favorite-notes.sh [limit] [每条字数]`。

### Step 2：分析笔记内容，提取话题

分析 Step 1 内容，按相关性聚类，提取**不超过 5 个**话题。排序：收藏时间新旧 > 关联笔记数 > 话题区分度；相似主题合并。每话题包含：话题名称、主题表述（作 Step 3 搜索 query）、关联笔记标题、简要描述（1～2 句）。

### Step 3：搜索每个话题的最新文章

用各话题的**主题表述**作 query，每话题检索 **5 篇**。逐个话题搜索，**每次搜索后立即提取摘要、丢弃原始响应**。

**搜索工具**（按序降级）：1) Perplexity（可选，需要配置 `PERPLEXITY_API_KEY`；heredoc 方式，安全传递中文 query）：

```bash
bash {baseDir}/perplexity-search-call.sh <<'ARGS_EOF'
{"query":"<主题表述>","max_results":5,"search_recency_filter":"day"}
ARGS_EOF
```

2) Brave：`web_search(..., provider: "brave", freshness: "pd")`；
3) 兜底（需预先配置 mcporter open-websearch server）：`bash {baseDir}/websearch-call.sh search '{"query":"关键词","limit":5,"engines":["duckduckgo","bing"]}'`。（优先 DuckDuckGo，失败自动换 Bing；若都失败可试 `"engines":["baidu"]`）。

**时间范围**（两套参数不可混用）：Perplexity 用 `search_recency_filter`，取值为 `day`、`week`、`month`、`year`（默认 `day`）。web_search 用 `freshness`，取值为 `pd`、`pw`、`pm`、`py`（默认 `pd`）。结果按日期再筛，同来源 ≤3 篇、URL 去重。**Context 管控**：每话题只保留「标题、来源、日期、URL、80～150 字介绍」。

### Step 4：生成简报并展示

按下方模板输出简报，对话中直接展示；正文后紧跟统计摘要。

**简报模板**（必须遵守）：

```markdown
# 资讯推送 — yyyy-MM-dd

基于最近 N 条收藏笔记，为您梳理了以下 M 个关注话题的最新动态。

## 话题 1: xxx
> 关注原因：基于您收藏的《笔记A》《笔记B》等

### 最新动态
（有日期按时间倒序）
1. **文章标题** — 来源 (日期)
   文章内容介绍：主题+核心观点+阅读价值，80～150 字，禁止空泛开头。
   🔗 链接
```

**响应格式**（简报后紧跟）：

```
| 项目 | 详情 |
|------|------|
| 📋 话题数量 | {M} 个话题 |
| 📰 文章数量 | {总文章数} 篇最新文章 |
| 📂 数据来源 | 最近 {N} 条收藏笔记 |
| ⏰ 生成时间 | {yyyy-MM-dd HH:mm} |
```

### Step 5：引导与通知

定时触发时：`openclaw nodes notify "📰 今日资讯推送已生成，共 M 个话题 N 篇文章"`（手动触发不发）。简报后检测定时任务：`openclaw cron list --json | jq '.jobs[] | select(.name == "youdaonote-news")'`；未设置时追加：`💡 想每天自动收到？说「设置资讯推送」即可，默认早上 9 点。`

## 资讯推送管理

**设置**（触发词：设置资讯推送、开启资讯推送、资讯推送设置）：先 `openclaw cron list --json | jq '.jobs[] | select(.name == "youdaonote-news")'` 检测；已存在则告知配置并问是否修改；不存在则 `openclaw cron add --name "youdaonote-news" --cron "0 9 * * *" --session isolated --message "生成资讯推送"`（用户指定时间则替换 cron）。确认并提示修改/关闭方式。

**修改时间**（触发词：修改资讯推送时间）：解析目标时间（如 8 点→`0 8 * * *`，晚 8 点→`0 20 * * *`），`openclaw cron remove --name "youdaonote-news"` 后重新 `cron add`，确认成功。

**关闭**（触发词：关闭资讯推送、取消资讯推送）：`openclaw cron remove --name "youdaonote-news"`，确认并告知可随时重开。
