# Task: Compare (Cross-Segment Comparison)

Compare behavior differences across segments (audiences) on the same page.

## Inputs

- `base_metric`: Per-segment page metrics
- `block_data[]`: Per-segment block data with assigned_phase, phase_name, etc.
- `segments[]`: Array of `{ index, description }` — labels for each segment
- `page_type`: Classified page type
- `language`: CHINESE | ENGLISH | JAPANESE (default ENGLISH)

## Segment Naming

- ALWAYS use `segments[].description` — never hard-coded labels like "Segment A", "compare_1"
- If description is raw filter (e.g. `"都道府県=Tokyo"`): extract value, translate to target language
  - NEVER copy raw expression verbatim into output
  - Translation is mandatory: romanized/English forms must become native expressions

### Common filter value translations

| Filter value | JAPANESE | CHINESE | ENGLISH |
|---|---|---|---|
| new_visitor / 新規 | 新規訪問者 | 新访客 | New visitors |
| returning_visitor / 再訪 | 再訪問者 | 回访用户 | Returning visitors |
| male / 男性 | 男性 | 男性 | Male users |
| female / 女性 | 女性 | 女性 | Female users |
| age=20-29 | 20代 | 20-29岁 | Ages 20-29 |
| Tokyo / 東京 | 東京 | 东京 | Tokyo |
| Osaka / 大阪 | 大阪 | 大阪 | Osaka |

### Array filter handling

If segment description is an array (e.g. `["广告来源=Instagram | line", "参考页面=https://..."]`):
- Combine all conditions into ONE readable label in target language
- For each `key=value`: extract value and translate; ignore URL-type values
- Join with natural connectors:
  - JA: 「〜からの〜ユーザー」 or 「〜かつ〜のユーザー」
  - CN: 「来自〜的〜用户」 or 「〜且〜的用户」
  - EN: "〜 users from 〜" or "〜 and 〜 users"
- Use combined label consistently in ALL output fields

## Phase Grouping

Use `assigned_phase` and `phase_name` from block_data directly.

## 1) narrative_comparison: Full Block Coverage

### Coverage rules
- ALL blocks into phase_1..phase_4 by assigned_phase — no omissions
- Keep block order consistent with page order

### Per-block comparison writing
For each block:
- `insight.summary`: One sentence describing the difference between segments
- Per-segment `behavior`: Natural flowing narrative (no "Fact:"/"Hypothesis:" labels)

**Narrative arc per segment**:
1. Behavior observed (cite dwell + exit)
2. Prior-context clue (only when logically supporting)
3. Psychological reasoning with hedging, referencing segment traits when relevant
4. Sequential mindset: explain from arriving-user perspective

## 2) Barriers and Opportunities Per Segment

For EACH segment independently:
1. Generate barriers first (top N by high exit, recommended 1-2)
2. Generate opportunities, HARD-EXCLUDE:
   - Blocks already in that segment's barriers, OR
   - Blocks with high exit
3. High-exit blocks MUST NEVER appear in opportunities

### Writing requirements
- `title`: Reason first, then decision/friction
- `analysis`: Exactly 2 sentences — fact (dwell+exit) + hypothesis (segment traits + mindset)
- No block_name in title; reference in analysis

## Output Format (human-readable Markdown report)

Write the entire report in the target language. Placeholders below are in English for clarity.

```markdown
# Segment Comparison Analysis

> **[summary_title]**: [one-sentence overall difference]

## Overview

| Segment | Key behavior | Key metrics |
|---------|-------------|-------------|
| [segment_0 description] | [behavior] | [metrics] |
| [segment_1 description] | [behavior] | [metrics] |

---

## Phase-by-Phase Comparison

### Phase 1: [phase_name]
> [phase_summarize]

**[block_name]** — [one-sentence difference]
- **[segment_0]**: [facts + hypothesis]
- **[segment_1]**: [facts + hypothesis]

(repeat for all 4 phases, all blocks — no omissions)

---

## Barriers (per segment)

### [segment_0 description]
**1. [barrier title]**
- **Block**: [block_name]
- **Analysis**: [2 sentences: fact + hypothesis]

### [segment_1 description]
...

---

## Opportunities (per segment)

### [segment_0 description]
**1. [opportunity title]**
- **Block**: [block_name]
- **Analysis**: [2 sentences: fact + hypothesis]

---

## Recommendations
1. [actionable suggestion targeting specific segment]
2. [actionable suggestion]
```
