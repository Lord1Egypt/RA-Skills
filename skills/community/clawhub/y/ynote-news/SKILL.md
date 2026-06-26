---
name: ynote-news
version: '1.2.4'
description: 有道云笔记资讯推送：基于收藏笔记分析关注话题，推送最新相关资讯。支持对话触发与每日定时推送（如早上9点）。触发词：资讯推送、设置资讯推送、生成资讯推送。
metadata: {"openclaw": {"emoji": "📰", "requires": {"bins": ["curl", "jq", "node"], "env": ["YNOTE_API_KEY", "PERPLEXITY_API_KEY"]}, "primaryEnv": "YNOTE_API_KEY"}}
---

# YNote News — 有道云笔记资讯推送

基于用户最近收藏的笔记，自动提取关注话题，搜索最新资讯，生成结构化简报并推送给用户。

> **⚠️ Context 管控**：本 Skill 涉及大量数据（笔记全文 + 搜索结果）。每步完成后**只保留结构化摘要，立即丢弃原始输出**，避免 context window 溢出。详见各 Step 中的「🔴 Context 管控」标注。

## 使用场景与用法总结

| 场景 | 说明 | 怎么用 |
|------|------|--------|
| **对话随时触发** | 在 OpenClaw 里随时要一份「基于最近收藏的资讯推送」 | 输入触发语，Agent 执行 4 步后直接展示简报 |
| **定时自动执行** | 每天固定时间自动整理收藏并生成简报 | 配置定时任务，到点自动触发；未设置则默认 9:00 |

**触发语示例**：资讯推送、最近关注、热点推送、每日简报、生成资讯推送、帮我整理收藏的简报

**前置**：需配置 `YNOTE_API_KEY`（拉取笔记）；Step 3 搜索使用 Perplexity（有内置默认 Key，开箱即用，支持时间过滤），若失败降级到 Brave（需 `BRAVE_API_KEY`）或 open-websearch（免 Key 兜底）。详见「前置条件」。

## 前置条件

1. **YNote MCP**（必需）：`export YNOTE_API_KEY="your-api-key-here"`
2. **网页搜索**（Step 3，三级降级）：
   - **Perplexity**（首选）：使用本 Skill 的 Search API 脚本（`perplexity-search-call.sh`），返回文章列表；Key 已内置，开箱即用。
   - **Brave**（fallback）：需在 `openclaw.json` 中配置 `BRAVE_API_KEY`。文档：<https://docs.openclaw.ai/brave-search>
   - **open-websearch**（兜底，免 Key）：只需 Node.js，通过 `websearch-call.sh` 调用
3. **CLI 工具**：`curl`、`jq`、`node`

## Quick Reference

| 操作 | 命令 |
|------|------|
| 获取最近收藏笔记 | `bash {baseDir}/get-favorite-notes.sh` （自动截断正文，默认 limit=30） |
| 创建笔记 | `bash {baseDir}/mcp-call.sh createNote '{"title":"标题","content":"# 内容","folderId":""}'` |
| 搜索笔记 | `bash {baseDir}/mcp-call.sh searchNotes '{"keyword":"关键词"}'` |
| 获取笔记内容 | `bash {baseDir}/mcp-call.sh getNoteTextContent '{"fileId":"<id>"}'` |
| Perplexity 搜索（文章列表） | `echo '{"query":"关键词","max_results":5,"search_recency_filter":"day"}' &#124; bash {baseDir}/perplexity-search-call.sh`（或 heredoc 传 JSON） |
| 网页搜索（兜底） | `bash {baseDir}/websearch-call.sh search '{"query":"关键词","limit":10,"engines":["duckduckgo","bing","baidu"]}'` |

## 核心工作流

收到用户的资讯推送请求后，按以下步骤执行。**每步完成后仅保留结构化摘要，丢弃原始输出。**

### Step 1：获取最近收藏的笔记内容

```bash
bash {baseDir}/get-favorite-notes.sh
```

包装脚本自动调用 `getRecentFavoriteNotes` 并**截断每条笔记正文为前 500 字**，确保 30 条笔记总量 ≤ 45KB，不会撑爆 context。

返回字段：`fileId`、`title`、`content`（前 500 字，超出部分截断）、`collectTime`（毫秒时间戳）。

可选参数：`get-favorite-notes.sh [limit] [每条字数]`，默认 `30 500`。

### Step 2：分析笔记内容，提取话题

Agent 分析 Step 1 获取的笔记内容，按内容相关性聚类，提取**不超过 5 个**话题。每个话题用一句可搜索的主题表述概括，便于 Step 3 检索到相关文章。

**排序权重**：收藏时间新旧 > 关联笔记数量 > 话题区分度。相似主题应合并。

每个话题包含：

| 字段 | 说明 |
|------|------|
| 话题名称 | 简洁明确的主题描述（如"AI 大模型技术趋势"） |
| 主题表述（用于搜索） | 一句或若干词，作为 Step 3 的搜索 query，便于检索相关文章 |
| 关联笔记 | 相关收藏笔记标题列表 |
| 简要描述 | 1-2 句话概括内容倾向 |

### Step 3：搜索每个话题的最新文章

用 Step 2 各话题的**主题表述**作为搜索 query，对每个话题检索**5 篇**最新文章。**逐个话题搜索，每次搜索后立即提取摘要、丢弃原始响应。**

**搜索工具**（按配置自动降级）：

1. **Perplexity**（首选）：使用 Search API 返回文章列表（title、url、date、snippet）。调用：`echo '{"query":"<主题表述>","max_results":5,"search_recency_filter":"<见下表>"}' | bash {baseDir}/perplexity-search-call.sh`（建议用 heredoc 或临时文件传 JSON，避免中文经 argv 编码问题）。调用失败时降级到 Brave。
2. **Brave**（fallback）：`web_search("关键词", provider: "brave", freshness: "pd")`
3. **open-websearch**（兜底）：`bash {baseDir}/websearch-call.sh search '{"query":"关键词","limit":5,"engines":["duckduckgo","bing"]}'`

**时间范围**：Perplexity 使用 `search_recency_filter`，与用户表述的对应关系（未指定默认 `day`）：

| 用户表述 | freshness | search_recency_filter |
|---------|-----------|------------------------|
| 未指定 / 最近 / 24 小时内 | `pd` | `day` |
| 最近几天 | `pw` | `week` |
| 最近一个月 | `pm` | `month` |
| 近一年 | `py` | `year` |

**时间过滤**：结果未必符合设定时间范围，需按日期再筛一次：范围内保留、超出剔除；无日期的可保留，优先用有日期的。每话题仍约 5 篇，不足则保留现有数量。

**筛选**：同一来源 ≤ 3 篇；相同 URL 去重；跨话题命中归入匹配度更高的话题。

**🔴 Context 管控**：每个话题搜索完成后，只保留「标题、来源、日期、URL、80-150 字内容介绍」，丢弃原始搜索响应。

### Step 4：生成简报并展示

将 Step 3 的摘要按下方「简报模板」格式输出，在对话中直接展示。

## 简报模板（必须遵守）

```markdown
# 资讯推送 — yyyy-MM-dd

基于最近 N 条收藏笔记，为您梳理了以下 M 个关注话题的最新动态。

## 话题 1: xxx
> 关注原因：基于您收藏的《笔记A》《笔记B》等

### 最新动态
（有日期时按时间倒序排列，最新在前）
1. **文章标题** — 来源 (日期)
   文章内容介绍：覆盖三要素——① 主题（讲什么）② 核心观点（主要结论）③ 阅读价值（为什么值得读）。3-5 句话或 80-150 字，禁止「介绍了…」「讨论了…」等空泛开头。
   🔗 链接

2. **文章标题** — 来源 (日期)
   文章内容介绍：……
   🔗 链接

## 话题 2: xxx
> 关注原因：基于您收藏的《笔记C》等

### 最新动态
1. …
```

## 响应格式（必须遵守）

输出简报正文后，**紧接着**输出统计摘要：

```
| 项目 | 详情 |
|------|------|
| 📋 话题数量 | {M} 个话题 |
| 📰 文章数量 | {总文章数} 篇最新文章 |
| 📂 数据来源 | 最近 {N} 条收藏笔记 |
| ⏰ 生成时间 | {yyyy-MM-dd HH:mm} |
```

### Step 5：引导与通知

**定时任务触发时**，额外发送桌面通知：`openclaw nodes notify "📰 今日资讯推送已生成，共 M 个话题 N 篇文章"`（用户手动触发时不发）。

**引导开启资讯推送**：简报展示后，执行 `openclaw cron list --json | jq '.jobs[] | select(.name == "ynote-daily-briefing")'` 检测定时任务。未设置时追加：`💡 想每天自动收到这样的简报吗？说「设置资讯推送」即可开启，默认每天早上 9 点推送。`

## 资讯推送管理

### 设置资讯推送

**设置**（触发词：设置资讯推送、开启资讯推送、资讯推送设置）：
1. `openclaw cron list --json | jq '.jobs[] | select(.name == "ynote-daily-briefing")'` 检测是否已存在
2. 已存在 → 告知用户当前配置（推送时间），询问是否修改
3. 不存在 → 创建（默认每天 9:00，用户指定时间则替换）：`openclaw cron add --name "ynote-daily-briefing" --cron "0 9 * * *" --session isolated --message "生成资讯推送"`
4. 回复确认，含推送时间、修改/关闭方式提示

**修改时间**（触发词：修改资讯推送时间）：
1. 解析目标时间（如"改到 8 点"→ `0 8 * * *`，"晚上 8 点"→ `0 20 * * *`）
2. `openclaw cron remove --name "ynote-daily-briefing"` 后重新 `cron add`
3. 确认修改成功

**关闭**（触发词：关闭资讯推送、取消资讯推送）：
1. `openclaw cron remove --name "ynote-daily-briefing"`
2. 确认关闭，告知可随时重新开启

## 环境变量

| 变量 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| `YNOTE_API_KEY` | ✅ | — | MCP Server API Key |
| `PERPLEXITY_API_KEY` | — | 内置默认值 | Perplexity 搜索，开箱即用 |
| `BRAVE_API_KEY` | — | — | Brave 搜索（Perplexity 失败时使用） |
| `YNOTE_MCP_URL` | — | `https://open.mail.163.com/api/ynote/mcp/sse` | MCP SSE 端点 |
| `YNOTE_MCP_TIMEOUT` | — | `30` | 超时秒数 |

## 常见问题

**Q: 报错缺少搜索 API key？**
搜索按 Perplexity → Brave → open-websearch 自动降级，最终兜底免 Key，只需 Node.js。

**Q: 搜索结果太少？**
调整关键词组合，或在 open-websearch 中增加 `engines`（如 `["duckduckgo","bing","baidu"]`）。

**Q: 没有最近收藏？**
先用 `ynote-clip` Skill 收藏一些网页，再生成话题简报。

**Q: 如何设置每天自动推送资讯？**
说「设置资讯推送」即可，默认早上 9 点，可自定义时间。
