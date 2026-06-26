---
name: video-comment-analysis
description: "Analyze video comment sections from a seller/operator perspective and produce visible browser walkthroughs plus business-focused outputs. Use when the user asks to view comments under a TikTok, Douyin, Instagram Reels, YouTube Shorts, or other short-video post; requests comment analysis, comment browsing, ecommerce/带货 diagnosis, conversion analysis, or wants a visual report/page based on video comments. Especially use for tasks that need: (1) visible browser operation in the comment area, (2) comment sampling across multiple screens, (3) analysis by six business dimensions, and (4) a polished visual HTML deliverable rather than plain text."
---

# Video Comment Analysis

Use this skill to turn a video comment section into a **seller-facing business diagnosis**, not a generic sentiment summary.

## Core output standard

Always optimize in this order:

1. **Visible browser operation** — let the user see the page, comment area, scrolling, and reply expansion
2. **Human-paced browsing** — scroll in understandable steps, not machine-speed jumps
3. **Business-useful extraction** — focus on conversion, hesitation, demand, objections, and buying signals
4. **Visual deliverable** — default to a polished HTML page when the user wants analysis/report/showable output
5. **Clear sample boundaries** — state how many screens/comments/replies were reviewed

## Required six-dimension framework

Unless the user explicitly asks for a different framework, analyze only with these six dimensions:

1. **评论主题分布**
2. **用户关注点分析**
3. **购买意向分析**
4. **成交驱动因素**
5. **影响转化因素**
6. **优化建议**

Do not drift into broader generic sections unless the user asks.

## Default workflow

### Step 1: Open the target video and lock onto the right comment area

- Open the target video page in the browser
- Wait for page stabilization
- Click into the comment area clearly if needed
- Confirm the correct comment container before analysis
- Prefer visible, human-readable interaction over hidden extraction

### Step 2: Read comments by the fixed quantity rule

Use comments as a **defined sample**, not as vague impressions.

Default reading rule:
- If **total visible comments are 100 or fewer**, read the full main-comment set
- If **total visible comments are above 100**, read **at least 100 effective main comments**
- Treat replies as supporting evidence by default, not as part of main-comment base statistics
- Expand high-value reply threads when they help verify:
  - price / shipping disputes
  - quality / trust / authenticity concerns
  - links / buying path problems
  - color / size / detail questions
  - “I bought it” / “where link” / hesitation / objection signals

Define **effective comment** as a comment that supports at least one of the six dimensions. Low-information comments like pure emoji, generic praise with no decision value, or obvious duplicates should not be relied on to satisfy the minimum sample requirement.

If the platform or page limits reading depth, say so explicitly.

### Step 3: Record sample boundaries in the output

Always state:
- total visible comment count if available
- effective main-comment sample count used
- how many reply threads were expanded
- whether replies were excluded from chart-level statistics or only used as supporting evidence

Suggested wording:

> 本次分析基于 X 条有效主评论；额外展开 Y 组高价值回复；回复内容用于辅助解释，不纳入主评论主题占比统计。

## Seller/operator perspective rules

Interpret comments in business language:
- what is pulling users in
- what is making them hesitate
- what is preventing conversion
- what product perception is forming in the comment area
- what action the seller should take next

Avoid output that sounds like:
- generic sentiment analysis
- broad social mood summary
- abstract “content atmosphere” talk without commercial value

Prefer conclusions that help answer:
- 能不能卖
- 为什么卖
- 卡在哪里
- 怎么优化

## Visualization rules

Not every dimension should be forced into charts.

### Data-friendly dimensions

For these four dimensions, default to **counts / percentages / mention rates first**:
- 评论主题分布
- 用户关注点分析
- 购买意向分析
- 影响转化因素

Do not let these dimensions default to only “high / medium / strong” wording when defensible hard metrics are available.

### Semi-structured dimensions

Prefer ranked cards / levels for:
- 成交驱动因素

Use labels like:
- 核心驱动
- 强驱动
- 辅助驱动

Do not fake precision with numbers like 9.4/10 unless the user explicitly wants a scoring model and the scoring rule is documented.

### Text/strategy dimensions

Prefer action cards / roadmap / priority blocks for:
- 优化建议

Use structures like:
- P1 立即优化
- P2 下一轮内容补充
- P3 后续测试

These judgment-style expressions should be used primarily for:
- 成交驱动因素
- 优化建议

Do not overextend them into dimensions that should first be expressed with counts / percentages / mention rates.

## Data-definition rules

Use only three kinds of numbers:

### 1. Counting metrics
Hard counts:
- comment count
- percentage
- mention count
- reply-thread count

### 2. Classified metrics
Human-coded categories:
- high / medium / low purchase intent
- link objection / shipping objection / trust objection

### 3. Analyst judgment
Business interpretation:
- 核心驱动
- 第一优先阻力
- 第一优先优化项

Never disguise analyst judgment as exact statistics.

## Standard output structure for HTML report

Use this order by default:

1. **封面 / 项目概览**
   - video title / link
   - analysis target summary
   - visible total comment count if available
   - effective main-comment count used
   - reply-thread count if expanded
   - one-line business conclusion

2. **核心结论摘要**
   - purchase intent level
   - biggest selling point
   - biggest conversion blocker
   - overall seller judgment

3. **评论主题分布**
   - chart + short interpretation

4. **用户关注点分析**
   - chart + short interpretation

5. **购买意向分析**
   - chart or structured blocks + short interpretation

6. **成交驱动因素**
   - ranked business cards / levels

7. **影响转化因素**
   - blocker chart + explanation

8. **优化建议**
   - P1 / P2 / P3 action roadmap

9. **代表性评论证据**
   - 4–8 comments that support the conclusion

10. **统计口径 / 方法说明**
   - sample boundary explanation
   - effective comment definition
   - whether replies are excluded from chart-level statistics
   - what is counted vs what is analyst interpretation

## Visual quality standard

For user-facing HTML, use a **Warm Editorial commercial proposal style** by default.

Prefer:
- warm white / cream / sand / brown-gray base palette
- one main accent color plus one supporting accent color
- strong visual hierarchy
- generous spacing and readable pacing
- editorial / strategy-deck feeling rather than dashboard feeling
- simple charts with clear labels

Avoid:
- overly dark dashboard style by default
- high-saturation purple/blue gradient default styling
- noisy card walls and excessive badges
- fake precision numbers without methodology
- long walls of text with no structure
- pages that feel like an AI-generated admin panel instead of a business proposal

## Delivery rule

If the user wants something to view or share, create a polished HTML deliverable by default and place it in:

`~/Desktop/OpenClaw Outputs/<date-task-folder>/`

Keep raw notes and intermediate artifacts in the workspace.

After the report is finished, automatically open the final analysis report page so the user can immediately view the result.

## Quality checklist

Before finishing, verify:
- the six dimensions are all present
- no extra framework replaced them unless requested
- sample size and reply usage are stated
- 评论主题分布 / 用户关注点分析 / 购买意向分析 / 影响转化因素 use counts / percentages / mention rates first
- 成交驱动因素 / 优化建议 use judgment-style labels appropriately
- charts only use defensible metrics
- judgment labels are not disguised as precise stats
- output is readable at a glance
- the page feels like a business deliverable, not a generic AI dump
- the final report page is opened after generation

## Reusable page skeleton

When building the final HTML deliverable, reuse the bundled page skeleton instead of starting from a blank page whenever speed or consistency matters.

Use:
- `references/page-skeleton.md` for module order and layout guidance
- `assets/html-report-template/index.html` as the default HTML starting point

Replace the placeholder tokens with task-specific content, sample counts, charts, evidence comments, and method notes.

## Reference

For detailed metric definitions, chart suitability, and page-structure rules, read:

`references/visualization-spec.md`

For execution rules covering comment-reading quantity, default report modules, and web-report style direction, read:

`references/execution-manual.md`

For module ordering and final-page layout structure, read:

`references/page-skeleton.md`
