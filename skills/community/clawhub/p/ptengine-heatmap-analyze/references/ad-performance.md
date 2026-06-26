# Ad Performance Analysis

Evaluate ad sources using a 4-quadrant model. Identify which ads to scale and which to pause.

## Inputs

- `ad_data`: Object keyed by ad source name, each containing metrics and quadrant
- `quadrantThresholds`: { visitsThreshold, qualityThreshold }
- `language`: CHINESE | ENGLISH | JAPANESE (default ENGLISH)

## Metric Standard

- `visits` = sessions (not pageviews, not unique users)
- All rates are decimals → express as percentages in output
- `avgDuration` in milliseconds → convert to seconds

## Quadrant Model (internal reasoning only — NEVER output quadrant labels)

- **concentrated** (>95% of total visits from one source): dominant, describe composition
- **Q1** (high visits + high CVR): Star → maintain, extract success factors, replicate
- **Q2** (low visits + high CVR): High-potential → scale carefully, monitor as volume grows
- **Q3** (high visits + low CVR): Needs attention → highest ROI optimization target. Diagnose:
  intent-message match → landing-page friction → drop-off points. Reduce or pause if no quick fix.
- **Q4** (low visits + low CVR): To validate → sample too small for conclusions, set observation
  threshold and exit criteria, keep only small test budget

**Threshold awareness**: The computed thresholds (average visits, average CVR) can be skewed by one
very high-volume source. When one source dominates traffic (>60%), the "average" may not represent
a meaningful dividing line. In such cases, note this limitation and focus the narrative on absolute
performance rather than quadrant placement.

## Analysis Steps

### Step 1: Identify key ads
- Identify main traffic source (especially "concentrated")
- Group by quadrant (internal only)

### Step 2: Select 1 best and 1 worst
**Best**: Q1 highest CVR (Q2 if Q1 empty)
**Worst**: Q3 lowest CVR (Q4 if Q3 empty)

### Step 3: Write summary
- Use `<strong>...</strong>` for emphasis (NOT Markdown bold)
- Contrast best vs worst with cautious tone + 1 short action
- Max 2 objects + 2 numbers + 1 action phrase
- Length: CN 40-70 chars (cap 80), JA ≤120 chars (cap 140), EN ≤180 chars (cap 220)

### Step 4: Write description
- 2-3 sentences: main source → opportunity → issue → 1-2 actions
- Length: CN 80-140 chars (cap 160), JA ≤200 chars (cap 240), EN ≤300 chars (cap 360)
- Max 3 objects + 3 numbers

## Metric Labels (use in output, never camelCase)

| Field | JAPANESE | CHINESE | ENGLISH |
|---|---|---|---|
| conversionRate | コンバージョン率 | 转化率 | conversion rate |
| bounceRate | 直帰率 | 跳出率 | bounce rate |
| clickRate | クリック率 | 点击率 | click-through rate |
| ctaClickRate | CTAクリック率 | CTA点击率 | CTA click rate |
| visits | セッション数 | 访问次数 | sessions |
| avgDuration | 平均滞在時間 | 平均停留时长 | avg. duration |

## Language-specific hedging

- **EN**: "data suggests", "may indicate", "likely", "consider"
- **CN**: 可能、或许、数据显示、可以考虑、建议
- **JA**: 可能性がある、推測される、と思われる、検討できる

## Japanese terminology check (before output)

Scan for Chinese contamination: 転化率→コンバージョン率, 跳出→直帰率, 点击→クリック率, 访问→セッション数

## FORBIDDEN in output

`concentrated`, `quadrant`, `Q1`, `Q2`, `Q3`, `Q4`

## Output Format (human-readable Markdown report)

Write the entire report in the target language.

```markdown
# Ad Performance Analysis

> **Core Insight**: [summary — 1 sentence, emphasize key ad names and numbers]

---

## Detailed Analysis

[description — 2-3 sentences: main traffic source → opportunity → issue → 1-2 actions]

## Ad Source Overview

| Source | Sessions | CVR | Bounce rate | Avg. duration | Assessment |
|--------|----------|-----|-------------|---------------|------------|
| [source] | [visits] | [cvr] | [bounce] | [duration] | Best / High potential / Needs attention / To validate |

---

## Recommendations
1. [actionable budget/optimization suggestion]
2. [actionable suggestion]
```

Notes:
- Use bold or emphasis for key names/numbers in the summary
- The "Assessment" column uses human-friendly labels, NEVER quadrant labels (Q1/Q2/Q3/Q4)
- Translate all column headers and assessments to target language
