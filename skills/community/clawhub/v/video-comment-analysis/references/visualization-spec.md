# Video Comment Analysis Visualization Spec

Use this reference when building formal comment-analysis outputs.

## 1. Sample definition

Always document:
- effective main-comment count
- reply-thread count expanded
- whether replies are included in chart-level statistics
- reading mode (full read when total comments are 100 or fewer / at least 100 effective main comments when total comments exceed 100)

Recommended default:
- main comments are the primary statistical unit
- replies support interpretation, but are excluded from top-level distribution charts unless explicitly stated
- if total visible comments are 100 or fewer, read the full main-comment set
- if total visible comments exceed 100, read at least 100 effective main comments

## 2. Suitable chart types by dimension

### 评论主题分布
Suitable:
- horizontal bar chart
- ranked bars
- stacked bars

Metric:
- count by primary theme
- percentage by primary theme

### 用户关注点分析
Suitable:
- horizontal bars
- ranked cards
- tier labels (only after hard metrics are stated)

Metric:
- mention count by concern
- mention rate by concern
- concern-level ranking only as a secondary layer

### 购买意向分析
Suitable:
- segmented bars
- funnel
- intent blocks

Metric:
- high / medium / low / churn-risk comment count
- percentage by intent layer

### 成交驱动因素
Suitable:
- priority cards
- level labels
- top-3 blocks

Metric:
- use business judgment labels, not fake precise scores

### 影响转化因素
Suitable:
- ranked blocker bars
- risk ranking
- top blocker cards

Metric:
- blocker mention rate
- blocker priority level

### 优化建议
Suitable:
- roadmap
- P1 / P2 / P3 cards
- immediate / next / later structure

Metric:
- usually no hard numbers required

## 3. Metric honesty rules

Allowed as hard metrics:
- counts
- percentages
- mention rates
- reply-thread counts

Default priority rule:
- 评论主题分布 / 用户关注点分析 / 购买意向分析 / 影响转化因素 should use hard metrics first
- 成交驱动因素 / 优化建议 may use labeled analyst judgment first

Allowed as labeled judgments:
- 核心驱动
- 强驱动
- 高优先级阻力
- 第一优先优化项

Avoid unless methodology is explicitly defined:
- 91 heat score
- 8.7 / 10 conversion effect
- any exact-looking number that is really analyst intuition

## 4. Standard disclaimer patterns

### Sample statement
> 本次分析基于 X 条有效主评论；额外展开 Y 组高价值回复；回复内容用于辅助解释，不纳入主评论主题占比统计。

### Driver statement
> 成交驱动为基于评论证据与卖家视角的综合判断，不代表平台原始统计值。

### Blocker statement
> 转化阻力基于评论中明确出现的犹豫、劝退与疑虑信号归类统计。

### Suggestion statement
> 以下建议基于评论分析结果形成，属于卖家策略动作，不属于评论原始数据指标。

## 5. Visual tone

Prefer:
- editorial / strategy deck feel
- restrained palette
- clean chart labels
- readable hierarchy

Avoid:
- noisy dark dashboard look by default
- excessive badges
- decorative charts with weak business meaning
- walls of text with no scannability
