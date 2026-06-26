---
name: ai-news-digest
description: "AI industry news aggregator and structured report generator. Automatically collects, deduplicates, ranks, and categorizes the latest AI developments from multiple sources into professional daily or weekly digests. Supports topic deep-dives, competitor tracking, trend analysis, bilingual output, and multi-format delivery (chat, file, Feishu doc). Zero dependencies — pure prompt-driven. Use when user asks for AI news, tech digest, industry update, competitor analysis, or weekly AI roundup."
---

# AI News Digest | AI 科技新闻日报

> Zero-config AI news aggregation. No scripts, no APIs, no setup.
> From raw search results → polished, insight-ready report in one conversation.

---

## Why This Skill Wins

| Problem with other tools | How we solve it |
|-------------------------|----------------|
| Need RSS feeds, Python scripts, cron jobs | Pure prompt-driven, zero setup |
| Dumps raw links at you | Structured categories with summaries |
| No deduplication | Smart merge: same event from 5 sources → 1 entry |
| No ranking | Significance-based prioritization (critical → minor) |
| One-size output | 4 depth levels + custom topics |
| English-only | Bilingual (Chinese + English) by default |

---

## Activation Triggers

- "AI 新闻" / "科技日报" / "AI 动态"
- "What's new in AI today?"
- "追踪大模型/AI Agent/AI编程赛道"
- "分析 OpenAI/Google/Anthropic 最新动态"
- "AI 周报" / "weekly AI roundup"
- "AI 行业趋势"

---

## Workflow: Daily Digest (Default Mode)

### Phase 1 — Discovery (8 parallel searches)

Use `web_search` with `count: 8` for each. Run all searches before proceeding.

| # | Query | Purpose |
|---|-------|---------|
| 1 | `"AI breaking news today {current_year}"` | General breaking |
| 2 | `"LLM model release launch {current_year}"` | New model releases |
| 3 | `"AI startup funding investment {current_year}"` | Funding rounds |
| 4 | `"人工智能 最新消息 今天"` | Chinese-language news |
| 5 | `"AI product launch announcement"` | Product updates |
| 6 | `"AI research breakthrough paper"` | Academic/research |
| 7 | `"OpenAI Google Anthropic Meta AI update"` | Big tech moves |
| 8 | `"AI regulation policy government"` | Policy changes |

**Focus mode** — If user specified a topic, replace queries 5-8 with topic-specific searches:

| Topic | Replacement queries |
|-------|-------------------|
| AI Agents | `"AI agent framework launch"`, `"autonomous agent 2026"`, `"AI agent startup"`, `"MCP tool use agent"` |
| AI Coding | `"AI coding assistant update"`, `"Copilot Cursor Windsurf Claude Code"`, `"AI developer tool"`, `"code generation model"` |
| AI Video/Image | `"AI video generation Sora Runway Kling"`, `"AI image Midjourney DALL-E"`, `"AI creative tool"`, `"generative AI art"` |
| AI Hardware | `"AI chip GPU NVIDIA AMD"`, `"AI inference hardware"`, `"edge AI chip"`, `"AI data center"` |
| Robotics | `"humanoid robot"`, `"AI robotics startup"`, `"autonomous vehicle AI"`, `"embodied AI"` |

### Phase 2 — Extraction

For each result that looks relevant:
1. Use `web_fetch` with `maxChars: 3000`
2. Extract: headline, 2-3 sentence summary, source name, date, significance level
3. Skip if: paywalled with no content, clearly outdated (>7 days), duplicate of already-extracted article, **product was already released before the report period** (verify launch date before listing as "new release")

**Date filtering rules (STRICT — NO EXCEPTIONS):**
- 默认只收录**当天**（today）的新闻。用户说"今天"就是今天，说"3月31日"就是3月31日。
- 不要包含昨天、前天、上周的新闻。用户如果需要最近几天/几周的新闻，会明确说"最近3天"、"本周"、"最近一周"等。
- 每条新闻发布前必须确认发布日期是今天，不确定的标注"[日期待确认]"，不得放入头条。
- 空板块显示"暂无相关动态"，绝不用旧新闻填充。

**Source credibility tiers** (prefer higher-tier when multiple sources cover same story):
- 🥇 Tier 1: Official blogs (openai.com, blog.google, anthropic.com, ai.meta.com), arxiv.org
- 🥈 Tier 2: techcrunch.com, theverge.com, arstechnica.com, 36kr.com, theinformation.com
- 🥉 Tier 3: General news, blogs, social media posts

### Phase 3 — Deduplication & Ranking

**Deduplication rules:**
1. Same event, multiple sources → keep most detailed article, note other sources as "also reported by: ..."
2. Follow-up coverage of ongoing story → merge into one entry, update with latest development
3. Translation of same article (EN/CN) → keep in user's preferred language

**Significance ranking:**
| Level | Criteria | Examples |
|-------|----------|----------|
| 🔴 Critical | Industry-changing event | New GPT release, major AI safety incident, billion-dollar deal, government ban |
| 🟡 Notable | Significant but expected | Product update, $10M+ funding, benchmark record, partnership |
| 🟢 Routine | Normal activity | Minor feature, opinion piece, routine update, rumor |

### Phase 4 — Output

**Depth levels** (user can specify, default: standard):

| Level | Content | Best for |
|-------|---------|----------|
| Brief | Headlines + one-liners only | Quick glance, mobile reading |
| Standard | Headlines + 2-3 sentence summaries + links | Default daily use |
| Deep | Full summaries + context + analysis | Research, decision-making |
| Executive | 3-5 bullet points only | Busy leaders, standup prep |

**Standard depth output format:**

```markdown
# 🤖 AI 科技日报 | {YYYY-MM-DD 周X}

---

## 🔴 今日头条

### {Headline}
{2-3 sentences: what happened, why it matters, what's next}
🔗 [{Source}]({url}) | 也被报道: {Other Source 1}, {Other Source 2}

---

## 📰 行业动态
| 事件 | 要点 | 来源 |
|------|------|------|
| {Title} | {One-line summary} | [🔗]({url}) |

## 💰 投融资
- **{Company}** — {金额} {轮次} (领投: {Investor}) → 用途: {use of funds}
  🔗 [{Source}]({url})

## 🛠️ 技术突破
- **{What}** — {Why it matters, technical detail}
  🔗 [{Source}]({url})

## 📱 产品发布
- **{Product}** ({Company}) — {Key feature or change}
  🔗 [{Source}]({url})

## 📜 政策法规
- {What changed} — {Who is affected}
  🔗 [{Source}]({url})

---

💡 **趋势洞察**: {1-2 sentences connecting today's stories to broader patterns}
📋 **明日关注**: {Upcoming events, expected announcements, developing stories}
```

---

## Advanced Modes

### Mode: Topic Deep-Dive

User: "深入分析 {topic}" / "deep dive into {topic}"

1. Run 10+ focused searches from different angles
2. Fetch top 15 articles
3. Output a **research brief**:

```markdown
# 📊 {Topic} 深度分析 | {Date}

## 背景概述
{What led to this topic becoming relevant — 3-4 sentences}

## 最新进展
{Timeline of recent events, newest first}

## 核心玩家
| 公司/团队 | 动作 | 策略方向 |
|-----------|------|----------|
| {Name} | {What they did} | {Where they're heading} |

## 技术分析
{Deeper look at the technology, 1-2 paragraphs}

## 市场影响
{How this affects the industry, investment landscape, etc.}

## 未来展望
{What to expect in next 3-6 months}

## 完整来源
1. [{Title}]({url}) — {Source}
2. ...
```

### Mode: Competitor Radar

User: "分析 {Company} 的最新 AI 动态"

```markdown
# 🔍 {Company} 竞品雷达 | {Date}

## 近30天动态
| 日期 | 事件 | 类型 |
|------|------|------|
| {Date} | {What happened} | 产品/技术/人事/战略 |

## 产品路线分析
{Where their product is heading based on recent moves}

## 关键人才变动
{Notable hires or departures}

## 研究/专利
{Recent papers, patents, or open-source releases}

## 对我们的启示
{Actionable insights for the user's own strategy}
```

### Mode: Weekly Roundup

User: "AI 周报" / "weekly AI roundup"

Daily format + these extra sections:

```markdown
## 📈 本周趋势
1. **{Trend 1}**: {Evidence from multiple stories}
2. **{Trend 2}**: {Evidence}

## 📊 数据亮点
- 融资总额: ${amount} across {n} rounds
- 新模型发布: {n} 个
- 重要产品: {highlights}

## 📅 下周看点
- {Upcoming event 1}
- {Expected announcement}
- {Ongoing story to follow}
```

---

## Quality Guarantee Checklist

Before delivering output, verify EVERY item:

- [ ] Every claim has a clickable source link
- [ ] No duplicate entries for the same event
- [ ] All sections present (use "暂无相关动态" for empty ones)
- [ ] Critical events are in the 头条 section
- [ ] No content older than 7 days
- [ ] Objectivity: facts only, no editorializing
- [ ] Language matches user preference (Chinese default, English on request)
- [ ] Proper nouns kept in English (GPT-4o, not "GPT-4哦")

## Error Handling

| Situation | Action |
|-----------|--------|
| Search API fails for a query | Skip, continue with remaining searches |
| Article fetch returns empty | Use search snippet, mark "[摘要来自搜索结果]" |
| All searches fail | Return: "⚠️ 搜索服务暂时不可用，请稍后再试" |
| No news in a category | Show "暂无相关动态" — never omit the section |
| Source is paywalled | Use snippet, mark "[付费文章，仅摘要]" |

## Delivery Options

| Target | How |
|--------|-----|
| Chat (default) | Markdown inline |
| Feishu doc | `feishu_doc` tool → `create` → `write` |
| File | Save to user-specified path |
| English | User says "in English" → all labels switch to English |

## User Satisfaction Tips

- **Speed matters**: Run searches in parallel (batch all web_search calls)
- **Be concise**: Don't pad with filler — every sentence should inform
- **Add value**: Don't just list news; connect dots in 趋势洞察
- **Respect time**: If user asks for "简报", don't give them a wall of text
- **Follow up**: If a story seems incomplete, note it in 明日关注
