# Audience Analysis

Analyze audience segments using the same 4-quadrant model as ad performance.
Answer: Who came? How did they perform? How to acquire more high-quality visitors?

## Inputs

- `audience_data`: Object keyed by segment name, each containing metrics and quadrant
- `quadrantThresholds`: { visitsThreshold, qualityThreshold }
- `language`: CHINESE | ENGLISH | JAPANESE (default ENGLISH)

## Metric Standard

- `visits` = sessions (not pageviews, not unique users)
- All rates are decimals → express as percentages
- `avgDuration` in milliseconds → convert to seconds

## Quadrant Model (internal reasoning only — NEVER output labels)

- **concentrated** (>95% of total visits): dominant segment
- **Q1** (high visits + high CVR): Star → protect and reinforce
- **Q2** (low visits + high CVR): High-potential → scale carefully
- **Q3** (high visits + low CVR): Needs attention → triage (intent match → first-view → CTA friction)
- **Q4** (low visits + low CVR): To validate → set observation threshold, low budget

## Segment Key Translations

| Segment key | JAPANESE | CHINESE | ENGLISH |
|---|---|---|---|
| newVisitor | 新規訪問者 | 新访客 | New visitors |
| returningVisitor | リピーター | 回访用户 | Returning visitors |
| NonBounceVisits | 直帰なし訪問者 | 非跳出访客 | Non-bounce visitors |
| BounceVisits | 直帰訪問者 | 跳出访客 | Bounce visitors |
| Campaign | キャンペーン経由 | 广告流量 | Campaign traffic |
| Direct | 直接流入 | 直接访问 | Direct traffic |
| Organic | 自然検索 | 自然搜索 | Organic search |

Infer dimension from keys: Campaign/Direct/Organic → channel; Japan/Tokyo → region; Android/iOS → device; newVisitor/returningVisitor → visitor type

## Analysis Steps

### Step 1: Identify key segments
- Identify composition driver (especially "concentrated")
- Group by quadrant internally

### Step 2: Select 1 best and 1 worst
**Best**: Q1 highest CVR (Q2 if Q1 empty)
**Worst**: Q3 lowest CVR (Q4 if Q3 empty)

### Step 3: Write summary
- `<strong>...</strong>` for emphasis
- Cautious tone, 1 action phrase
- Max 2 objects + 2 numbers + 1 action
- Length: CN 35-65 chars (cap 80), JA ≤120 chars (cap 140), EN ≤180 chars (cap 220)

### Step 4: Write description
- 2-3 sentences: main profile → opportunity → issue → 1-2 actions
- Max 2 dimensions (channel/region/device/visitor type)
- Length: CN 80-140 chars (cap 160), JA ≤200 chars (cap 240), EN ≤300 chars (cap 360)

## Metric Labels (same as ad-performance.md)

| Field | JAPANESE | CHINESE | ENGLISH |
|---|---|---|---|
| conversionRate | コンバージョン率 | 转化率 | conversion rate |
| bounceRate | 直帰率 | 跳出率 | bounce rate |
| clickRate | クリック率 | 点击率 | click-through rate |
| ctaClickRate | CTAクリック率 | CTA点击率 | CTA click rate |
| visits | セッション数 | 访问次数 | sessions |
| avgDuration | 平均滞在時間 | 平均停留时长 | avg. duration |
| completions | 完了数 | 完成次数 | completions |

## FORBIDDEN in output

`concentrated`, `quadrant`, `Q1`, `Q2`, `Q3`, `Q4`, raw camelCase field names, raw segment keys (always translate)

## Output Format (human-readable Markdown report)

Write the entire report in the target language.

```markdown
# Audience Analysis

> **Core Insight**: [summary — 1 sentence, emphasize key segments and numbers]

---

## Detailed Analysis

[description — 2-3 sentences: main audience profile → opportunity → issue → 1-2 actions]

## Audience Overview

| Segment | Sessions | CVR | Bounce rate | Avg. duration | Assessment |
|---------|----------|-----|-------------|---------------|------------|
| [segment, translated] | [visits] | [cvr] | [bounce] | [duration] | Core / High potential / Needs attention / To validate |

---

## Recommendations
1. [actionable acquisition/optimization suggestion]
2. [actionable suggestion]
```

Notes:
- Always translate segment keys to target language (never raw keys like "newVisitor")
- The "Assessment" column uses human-friendly labels, NEVER quadrant labels
- Translate all column headers to target language
