# Quality Constraints

All analysis output must comply with these quality rules. They cover metric definitions, evidence
policy, language enforcement, and terminology validation.

## 1. Output Format

Output is a **human-readable Markdown report**, not JSON. Follow the report template defined in
each task's reference file. The report should be well-structured with headers, bullet points,
and tables for easy scanning by marketing practitioners and site operators.

## 2. Metric Dictionary

### Metric Direction Table (cross-version / cross-segment)

| metricKey | Better direction | Worse direction |
|---|---|---|
| `visits` | higher | lower |
| `conversionsRate` | higher | lower |
| `clickRate` | higher | lower |
| `ctaClickRate` | higher | lower |
| `avgDuration` | higher | lower |
| `avgStayTime` | higher | lower |
| `impressionRate` | higher | lower |
| `readingContributionRate` | higher | lower |
| `elementConversionRate` | higher | lower |
| `avgPageViews` | higher | lower |
| `fvDropOffRate` | **lower** | higher |
| `bounceRate` | **lower** | higher |
| `exitRate` | **lower** | higher |

**Counter-intuitive metrics**: fvDropOffRate, bounceRate, exitRate are **lower-is-better**.
A decrease = improvement. An increase = degradation.

### Direction-Language Alignment

- "improved" / "改善" / "改善した" → ONLY when value moved in **better** direction
- "declined" / "低下" / "悪化" → ONLY when value moved in **worse** direction

### Core Metric Definitions

**impressionRate** (PV-based): Share of page PVs where the block was visible.
- CHINESE: 在页面总PV中，用户滚动到能看见该区块的PV占比
- ENGLISH: Of all page PVs, the percentage where users scrolled far enough to see this block
- JAPANESE: ページ全体のPVのうち、このブロックが表示されたPVの割合

**exitRate** (PV-based): Among PVs that reached this block, the proportion where it was the deepest scroll point.
- CHINESE: 在看过该区块的PV中，该区块是用户本次浏览最深触达位置的PV占比
- ENGLISH: Among PVs that reached this block, the proportion where this block was the user's maximum scroll depth
- JAPANESE: このブロックに到達したPVのうち、このブロックがそのPVにおける最深スクロール位置だったPVの割合

**readingContributionRate** (session-based, Block conversion rate):
- CHINESE: 区块转化贡献率是指：在发生【Conversion Name】的用户里，认真阅读该区块（>5秒）的用户占比
- ENGLISH: Block conversion means the share of users who converted (【Conversion Name】) and read this block for more than 5 seconds
- JAPANESE: ブロックコンバージョンとは、【Conversion Name】が発生したユーザーのうち、このブロックを5秒以上読んだ人の割合

### Metric Labels (i18n)

| metricKey | CHINESE | ENGLISH | JAPANESE |
|---|---|---|---|
| visits | 访问次数 | Visits | 訪問数 |
| fvDropOffRate | 首屏流失率 | First-view drop-off rate | ファーストビュー離脱率 |
| bounceRate | 跳出率 | Bounce rate | 直帰率 |
| avgDuration | 平均停留时间 | Average duration | 平均滞在時間 |
| clickRate | 点击率 | Click rate | クリック率 |
| ctaClickRate | CTA总点击率 | CTA click rate | CTAクリック率 |
| conversionsRate | 页面转化率 | Conversion rate | コンバージョン率 |
| impressionRate | 区块到达率 | Block impression rate | インプレッション率 |
| avgStayTime | 区块平均停留时长 | Avg. block dwell time | ブロック平均滞在時間 |
| exitRate | 区块流失率 | Block exit rate | ブロック離脱率 |
| readingContributionRate | 区块转化率 | Block conversion rate | ブロックコンバージョン率 |

### Metric Units (i18n)

| metricKey | CHINESE | ENGLISH | JAPANESE |
|---|---|---|---|
| visits | 次 | visits | 回 |
| avgDuration / avgStayTime | 秒 | s | 秒 |
| All rate metrics | % | % | % |

### Rankings Interpretation

Block data may include `rankings` with `stay_time`, `exit_rate`, `conversion` sub-objects.
Each contains: `rank`, `vs_median`, `is_extreme`, `extreme_type` ("top"/"bottom"/null).

- **rank 1 = best for ALL metrics**
- `extreme_type: "top"` = best performer
- `extreme_type: "bottom"` = worst performer
- For exit_rate: `extreme_type: "bottom"` = HIGHEST exit rate = most problematic (counter-intuitive)
- Do NOT mention rank numbers, vs_median values, or field names in output. Translate to natural language.

## 3. Evidence Policy

### Technical Field Prohibitions in Natural Language

NEVER include in output text:
- `block_id` / `blockId` numbers (e.g. "332230")
- `block_index` position numbers (e.g. "区块3", "ブロック2")
- `IS_FV` / `IS_SV` flags → use "首屏" / "First view" / "ファーストビュー"
- `assigned_phase` numbers → use `phase_name`
- `segment_type` values (utmSource, etc.) → use segment description
- Raw tag values (exitTag: high) → express as natural language
- camelCase metric keys → use metricLabel from dictionary
- Raw milliseconds → convert to seconds with unit
- Raw decimals → convert to percentages

### Block Referencing Rules

- Single block: always use `block_name`
- Multiple blocks: use `phase_name` + position description
- NEVER enumerate blockId values

### Evidence Requirements

- Ground narrative in observable data: cite dwell + exit (impression optional)
- Use hedging language: "may", "might", "possibly", "と考えられる", "可能是"
- Do NOT claim strong causality

### Source Separation (strict)

`fvDropOffRate` and `exitRate` come from DIFFERENT data sources and MUST NOT be conflated:

- `fvDropOffRate` → ONLY from `base_metric.fvDropOffRate` (page-level). When reporting first-view
  drop-off across versions, ALWAYS source from base_metric.fvDropOffRate of each version.
- `exitRate` → ONLY from `block_data[].exitRate` (block-level). Reflects how many PVs reaching a
  specific block left from there.

FORBIDDEN:
- Using a first-view block's `exitRate` to describe or approximate `fvDropOffRate`
- Deriving or estimating `fvDropOffRate` from any combination of block-level data
- In `data_performance[].change` for fvDropOffRate: MUST cite exact `base_metric.fvDropOffRate` value

## 4. Language Policy

- Output language controlled ONLY by `language` parameter (CHINESE | ENGLISH | JAPANESE)
- Default: ENGLISH
- NO mixed-language in natural-language fields
- Allowed original-language content (whitelist): block_name, quoted content, Conversion Name, brand terms

## 5. Terminology Enforcement (Final Self-Check)

Execute on EVERY natural-language field before output.

### Step A — Scan for non-target-language fragments
### Step B — Apply forced replacements:

**JAPANESE context** (forbidden → replacement):
- 首屏 → ファーストビュー
- 区块 → ブロック
- 流失 → 離脱
- 到达率 → インプレッション率
- 转化率/転化率 → コンバージョン率
- 阅读贡献率/区块转化贡献率 → ブロックコンバージョン

**ENGLISH context**: No Chinese/Japanese analysis terms (except whitelist)

**CHINESE context**: No English/Japanese analysis terms (except whitelist)
- First view/ファーストビュー → 首屏
- block/ブロック → 区块

### Step C — Re-scan after replacements

### Step D — Rewrite (FAIL-CLOSED)

If the field still violates (non-target-language fragments remain, or "pseudo target language"
patterns detected like Chinese grammar markers in Japanese), MUST rewrite the ENTIRE field:

- Keep numbers/percentages unchanged. Keep block_name and quoted content as-is (whitelist).
- Use short, fixed structure — do not "freestyle":

**1-sentence (insight/summary)**:
- EN: `<data clue>, suggesting <user intent or friction>.`
- CN: `<数据线索>，说明<用户意图或卡点>。`
- JA: `<データの手がかり>。そこから<意図または詰まり>が示唆される。`

**2-sentence (block insight — fact + hypothesis)**:
- EN: `<dwell + exit (+ impression)>. This may indicate <1–2 possible reasons>.`
- CN: `<停留+离开（可选到达）>。这可能意味着<1-2个可能原因>。`
- JA: `<滞在+離脱（必要なら到達）>。これにより<可能性のある理由を1〜2つ>が考えられる。`

## 6. Directional Consistency Self-Check (Execute Before Output)

Before emitting final JSON, verify across ALL output fields:

1. **Direction-language match**: For every metric using directional language (improved/worsened/改善/悪化),
   confirm it matches the metric direction table above. If mismatched, rewrite.
2. **Counter-intuitive metrics**: Pay special attention to fvDropOffRate, bounceRate, exitRate —
   these are lower-is-better. Higher value = worse, NOT better.
3. **Numeric consistency**: When citing X% → Y%, verify directional word matches arithmetic.
   If Y > X = increased, do NOT write "低下". If Y < X = decreased, do NOT write "上昇".
4. **win_version_index** (ab_test only): Must point to version with HIGHER conversionsRate.
