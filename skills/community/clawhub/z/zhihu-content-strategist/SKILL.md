---
name: Zhihu Content Strategist
slug: zhihu-content-strategist
description: Analyze Zhihu hot trends & community dynamics; generate high-engagement answer strategies and first drafts.
tags: [zhihu, content-strategy, writing, social-media, chinese-platform, creator]
version: 1.0.0
license: MIT-0
---

# Zhihu Content Strategist (知乎内容策略师)

Analyze Zhihu trending topics and high-performing answers to generate data-driven content strategies, topic recommendations, and ready-to-publish answer drafts tailored to your niche.

## Scripts

| Path | Description |
|------|-------------|
| `scripts/strategist.py` | Main CLI script — domain analysis, gap detection, draft generation |
| `schemas/input.schema.json` | JSON Schema for workflow input |
| `schemas/output.schema.json` | JSON Schema for workflow output |
| `references/engagement_patterns.json` | Zhihu engagement pattern reference (hooks, structures, timing) |
| `references/topic_templates.json` | Topic recommendation templates and cold-start roadmap |

### CLI Usage

```bash
# Recommend topics with gap analysis
python scripts/strategist.py --domain AI --task recommend

# Generate answer strategy for a specific topic
python scripts/strategist.py --domain career --task strategy --topic "远程办公效率"

# Generate full answer draft
python scripts/strategist.py --domain AI --task draft --topic "AI Agent 落地案例"

# Pattern analysis of high-performing answers
python scripts/strategist.py --domain AI --task analyze

# Publishing optimization
python scripts/strategist.py --domain AI --task publish --topic "大模型应用实践"

# JSON output for programmatic use
python scripts/strategist.py --domain AI --task recommend --output json
```

## 🚀 First-Success Path (3 Steps)

1. **Step 1**: Run `python scripts/strategist.py --domain AI --task recommend`
2. **Step 2**: Review the gap matrix and pick one topic
3. **Step 3**: Run `python scripts/strategist.py --domain AI --task draft --topic "AI Agent 落地案例"` to receive a complete answer draft with hooks and golden lines in <30 seconds

## Core Capabilities

- **Hot trend analysis**: Scrape Zhihu hot list (热榜) and extract trending topics in your domain
- **High-engagement answer dissection**: Analyze top-20 answers for structural patterns, emotional hooks, data usage, and opening techniques
- **Content gap detection**: Identify subtopics with high question volume but low answer quality
- **Topic recommendation engine**: Suggest topics with competition level, estimated exposure, and recommended angles
- **Draft generation**: Produce complete answer drafts with hook → argument → golden lines → CTA structure
- **Post timing optimization**: Recommend best publishing windows based on historical engagement data
- **Competitor analysis**: Analyze why similar creators succeed, extract replicable patterns

## Workflow (8 Steps)

### Step 1: Define Target Domain
**Input**: User specifies target area (e.g., AI, career, psychology, finance) OR provides a specific Zhihu hot-list URL.
**Output**: Domain definition with sub-topic taxonomy.
**Logic**: If user gives a URL, extract the topic directly. If a broad domain, generate 5-8 sub-topics for exploration. Verify domain has sufficient question volume on Zhihu.

### Step 2: Scrape Hot List & Top Answers
**Input**: Target domain or topic URL.
**Action**: Scrape Zhihu hot list + top 20 answers under the target domain/topic.
**Output**: Dataset of trending questions and high-engagement answers with metrics (upvotes, comments, publish time, author follower count).
**Logic**: Prioritize answers with 1K+ upvotes from the past 6 months. Respect Zhihu's rate limits.

### Step 3: Pattern Analysis of High-Performing Answers
**Input**: Top-20 answer dataset.
**Analysis dimensions**:
- **Opening hooks**: Question-based, story-based, counter-intuitive claim, data drop
- **Structure patterns**: Problem-solution, timeline narrative, listicle, deep-dive analysis
- **Emotional tone**: Empathetic, authoritative, humorous, contrarian
- **Data usage**: Academic citations, personal experience, statistics, case studies
- **Length sweet spot**: Character count distribution of top answers
- **Golden lines**: Extract most-upvoted sentences and analyze why they resonate

**Output**: Pattern report with examples and replicable templates.

### Step 4: Content Gap Detection
**Input**: Target domain question corpus + existing answers.
**Analysis**: For each sub-topic, compute:
- Question volume: how many related questions exist
- Answer quality: average upvotes of top answers
- Competition index: number of established creators in this niche
- Gap score = question volume × (1 - answer quality percentile)

**Output**: Gap matrix sorted by opportunity score.

| Sub-topic | Questions | Avg. Upvotes | Competition | Gap Score |
|-----------|-----------|--------------|-------------|-----------|
| AI Agent 落地案例 | 230 | 42 | Low | ⭐⭐⭐⭐⭐ |
| Prompt 工程技巧 | 1500 | 180 | High | ⭐⭐ |

### Step 5: Topic Recommendation
**Input**: Gap matrix + user's expertise level.
**Output**: Top 5-10 topic recommendations with:
- **Topic title**: The question to answer
- **Competition level**: Low / Medium / High
- **Estimated exposure**: Views range
- **Suggested angle**: Unique perspective to stand out
- **Difficulty**: Quick answer vs deep research required

**Logic**: Balance high-gap (low competition) with high-volume (high exposure) topics. Consider user's stated expertise.

### Step 6: Answer Strategy Generation
**Input**: 1-3 selected topics.
**Output**: Per-topic strategy brief:
- **Hook (first 3 sentences)**: 2-3 opening variants to A/B test
- **Argument structure**: Logical flow with sub-points
- **Evidence plan**: What data/stories/citations to include
- **Golden lines**: 2-3 memorable statements to embed
- **CTA (call to action)**: Follow, comment bait, profile link strategy
- **Visual suggestions**: Where to add images, charts, or code blocks
- **Style profile**: Tone and complexity level

### Step 7: Draft Generation
**Input**: Strategy brief.
**Output**: Complete answer draft in markdown.
**Logic**: Optionally mimic a specified KOL's writing style (requires providing 3+ sample answers from that creator). Include SEO optimization for Zhihu's internal search.

### Step 8: Publishing Optimization
**Input**: Completed draft.
**Output**: Publishing recommendations:
- **Best publish time**: Day of week + hour (based on domain analysis)
- **Tag strategy**: Primary + secondary tags for maximum reach
- **Promotion hooks**: 1-sentence share text for WeChat/Weibo cross-promotion
- **Engagement plan**: How to respond to first 10 comments to boost algorithm ranking

## Sample Prompts

### Prompt 1: Topic Recommendation (AI Domain)
**User:**
```bash
python scripts/strategist.py --domain AI --task recommend
```
**Expected Output:**
```
Zhihu Content Strategist v1.0.0
Domain: AI | Task: recommend

[Step 5/8] Recommending topics in AI

Topic                          Score      Competition   Difficulty                   Angle
------------------------------------------------------------------------------------------------------------------------
AI Agent 落地案例              ⭐⭐⭐⭐⭐   Low           Quick answer (1-2 hours)      Tell a specific story with measurable results; include code/data snippets
大模型应用实践                 ⭐⭐⭐⭐    Medium        Moderate research (3-6 hours)  Don't just list resources — share your personal learning path with specific mistakes and breakthroughs
AI 在行业中的应用              ⭐⭐⭐⭐⭐   Low           Quick answer (1-2 hours)      Start with a counter-intuitive claim or personal story to hook readers
AI 创业                        ⭐⭐⭐⭐⭐   Low           Quick answer (1-2 hours)      Start with a counter-intuitive claim or personal story to hook readers
AI 产品经理                    ⭐⭐⭐⭐    Low           Moderate research (3-6 hours)  Don't just list resources — share your personal learning path with specific mistakes and breakthroughs
------------------------------------------------------------------------------------------------------------------------

  Task 'recommend' complete!
```

### Prompt 2: Answer Draft Generation
**User:**
```bash
python scripts/strategist.py --domain career --task draft --topic "远程办公效率"
```
**Expected Output:**
```
Zhihu Content Strategist v1.0.0
Domain: CAREER | Task: draft

[Step 7/8] Generating draft for: 远程办公效率

  Draft generated (1210 chars, ~3-5 min)

============================================================
# 远程办公效率

> 我分析了远程办公效率领域的100个案例，发现…

## 先说说背景

在过去的半年里，我花了大量时间研究远程办公效率。这篇文章不讲大道理，只分享真实经历和可复用的方法。

## 核心观点

**1. 远程办公效率的核心在于理解本质** — 大多数人只看到表面

**2. 实践中的三个关键发现** — 每一项都有数据支持
...

## 写在最后

如果这篇文章对你有帮助，欢迎**点赞+关注**，我会持续分享更多实战经验。

评论区说说你的想法：你在这方面的经历是怎样的？

---

*本文由 Zhihu Content Strategist 辅助生成。内容仅供参考，请结合实际体验调整。*
============================================================

  Task 'draft' complete!
```

### Prompt 3: Content Gap Detection
**User:**
```bash
python scripts/strategist.py --domain AI --task gap
```
**Expected Output:**
```
Zhihu Content Strategist v1.0.0
Domain: AI | Task: gap

[Step 4/8] Detecting content gaps in AI

Sub-topic                      Questions    Avg Upvotes    Competition  Gap
------------------------------------------------------------------------------
AI Agent 落地案例              230          42             Low          ⭐⭐⭐⭐⭐
AI 在行业中的应用              1200         35             Low          ⭐⭐⭐⭐⭐
AI 创业                        320          28             Low          ⭐⭐⭐⭐⭐
AI 产品经理                    280          38             Low          ⭐⭐⭐⭐
AI 编程助手                    680          55             Medium       ⭐⭐⭐⭐
大模型应用实践                 890          65             Medium       ⭐⭐⭐⭐
AI 绘画与生成                  1800         120            High         ⭐⭐
Prompt 工程技巧                1500         180            High         ⭐⭐
------------------------------------------------------------------------------

  Task 'gap' complete!
```

### Prompt 4: Answer Strategy Generation
**User:**
```bash
python scripts/strategist.py --domain AI --task strategy --topic "AI Agent 落地案例"
```
**Expected Output:**
```
Zhihu Content Strategist v1.0.0
Domain: AI | Task: strategy

[Step 6/8] Generating strategy for: AI Agent 落地案例

  Topic: AI Agent 落地案例

  Hook Variants:
    - 数据切入: 我分析了AI Agent 落地案例领域的100个案例，发现…
    - 故事切入: 去年我亲身经历了一个AI Agent 落地案例项目，结果让我…
    - 反直觉: 你可能不相信，但AI Agent 落地案例的真相和大部分人想的恰恰相反

  Structure:
    - 1. 开篇：用数据或故事建立信任
    - 2. 核心论点：分3-4个方面展开
    - 3. 个人经验：为什么我的观点值得信
    - 4. 可操作建议：读者能立刻做的事
    - 5. 金句收尾：值得转发的浓缩总结

  Golden Lines:
    - 关于AI Agent 落地案例，大多数人看到的是XX，但真正重要的是YY
    - 短期来看AI Agent 落地案例是ZZ，但长期来看…

  Task 'strategy' complete!
```

### Prompt 5: High-Performing Answer Pattern Analysis
**User:**
```bash
python scripts/strategist.py --domain AI --task analyze
```
**Expected Output:**
```
Zhihu Content Strategist v1.0.0
Domain: AI | Task: analyze

[Steps 2-3/8] Analyzing high-performing answers in AI
  Sample size: 20
  Opening hook types: ['data_drop', 'counter_intuitive', 'story_based']
  Common structures: Problem-Solution, Step-by-step tutorial, Comparative analysis
  Avg length: 2500 chars
  Golden line pattern: 短期XX vs 长期XX 的反转认知

  Task 'analyze' complete!
```

### Prompt 6: Publishing Optimization
**User:**
```bash
python scripts/strategist.py --domain AI --task publish --topic "大模型应用实践"
```
**Expected Output:**
```
Zhihu Content Strategist v1.0.0
Domain: AI | Task: publish

[Step 8/8] Publishing optimization for: 大模型应用实践

  Best time: Tuesday 10:00 AM (tech audience peak) or Thursday 8:00 PM (evening readers)
  Tags: primary=['AI'], secondary=['大模型应用实践', '经验分享', '实战']

  Promotion hooks:
    - 写了一篇关于大模型应用实践的深度回答，分享一些真实经验
    - 这可能是你今年看过最实用的分享

  Comment plan:
    - 前30分钟务必回复每条评论（算法权重最高）
    - 对已赞评论点赞表示认可
    - 1小时后回复较长的评论（展示深度）
    - 第2天补充1-2条高质量回复（推动二次曝光）

  Task 'publish' complete!
```


## Boundary Conditions

[Boundary conditions unchanged from design doc]

## Error Handling

[Error handling unchanged from design doc]

## Security Requirements

- **Original content only**: Never plagiarize; generate original content inspired by patterns, not copies
- **No misinformation**: Flag when generating content on medical, legal, or financial topics; include disclaimer
- **Zhihu ToS compliance**: Respect robots.txt; don't automate posting (this is strategy + draft only)
- **Data privacy**: Discard scraped answer content after analysis; don't store full answer texts
- **Content safety**: Refuse to generate content violating Chinese internet regulations
