# Task: Single Page Analysis

Deep behavior analysis for one page. Generates core insight, phase-by-phase narrative covering
ALL blocks, and identifies barriers (friction) and opportunities (engagement).

## Inputs

- `base_metric`: Page-level metrics (visits, bounceRate, fvDropOffRate, avgDuration, clickRate, conversionsRate, etc.)
- `block_data[]`: Array of enriched block data (block_id, block_name, assigned_phase, phase_name, contentSummary, impressionRate, avgStayTime, exitRate, readingContributionRate, rankings, etc.)
- `page_type`: Classified page type
- `language`: CHINESE | ENGLISH | JAPANESE (default ENGLISH)
- `segment` (optional): Audience/filter context (e.g. "新訪問者", "Instagram流量")

## Segment Handling

If `segment` is provided:
- **core_insight MUST always mention segment** — open with framing sentence:
  - JAPANESE: 「本分析は【segment_label】のデータに基づいています。」
  - CHINESE: 「本分析基于【segment_label】的数据。」
  - ENGLISH: "This analysis is based on data for 【segment_label】."
- Other fields: mention segment ONLY when it directly explains the observed behavior
- Always use segment description value, never segment_type technical values

## Phase Grouping

Use `assigned_phase` and `phase_name` from block_data directly. Do NOT re-classify.

## 1) narrative_structure: Full Block Coverage

### Coverage rules
- Assign ALL blocks into phase_1..phase_4 by assigned_phase
- Each phase's blocks[] must include ALL block_ids in that phase — no omissions
- Keep block order consistent with page order

### How to write each block insight

Write `insight` as a **natural flowing narrative** (no "Fact:" / "Hypothesis:" labels).

**Narrative arc**:
1. **Behavior observed**: What did users do? (cite dwell + exit as evidence)
2. **Prior-context clue** *(conditional)*: Only mention preceding blocks if directly supporting reasoning
3. **Psychological reasoning**: Why? Use hedging ("may", "might", "possibly", "と考えられる")
4. **Improvement hint**: One concrete, actionable direction

**Example (JA)**: "97.4%のユーザーがここまでスクロールしたにもかかわらず、66.8%が離脱している。13秒という比較的長い滞在から、ブランドを確認した後に「自分向けか」を判断しようとしたが、その答えが得られなかった可能性がある。価値提案をより明確にすることで、離脱を減らせるかもしれない。"

**Example (CN)**: "停留9秒但有58%的用户在此离开，结合上方详细列出了多项产品功能，用户可能是在仔细比较后仍未找到决定购买的关键理由。可以考虑增加真实用户评价或具体使用效果数据。"

### insight_summary

Format: **data clue → user intent → implication** (one sentence, max 20 chars)
- Avoid exact seconds/% unless extreme
- Do not repeat block_name
- Target language only

### impressionRate usage

Use only as reach/coverage context, not as core performance judgement.

### Title ↔ body consistency

- If core_insight mentions a theme, narrative_structure MUST explain it
- If phase_summarize mentions a theme, at least one block insight MUST explain it

## 2) Barriers and Opportunities

### Barriers (top N by high exit, recommended 1-3)
- Primary signal: exitRate
- Cite: exit (primary) + dwell (secondary) + impression (optional)
- If dwell also high → still a barrier, emphasize "read but still left"

**Position-aware interpretation**: Blocks near the page bottom naturally have higher exit rates
(users reaching the end simply leave). When selecting barriers, weigh early/mid-page high-exit
blocks more heavily than final blocks. A 40% exit rate at block 3 is far more alarming than
40% at the last block. If the highest-exit block is the page's final block, check whether it
carries a meaningful CTA — if not, it may be a structural issue (missing closing CTA) rather
than a content problem.

**Exit acceleration pattern**: Look for adjacent blocks where exitRate suddenly jumps (e.g., block
5 has 15% exit, block 6 has 45% exit). This transition point often reveals the moment users
disengage — the content shift between these blocks may be the real friction point. Mention
the transition in the barrier analysis when detected.

### Opportunities (top N by high dwell, MUST exclude barriers)
**De-duplication order**:
1. Generate barriers first → get barrier_block_ids
2. Select opportunities from high-dwell blocks, HARD-EXCLUDE any block where:
   - block_id is in barrier_block_ids, OR
   - block has high exit (exitTag = High or exitRate is extreme)
3. A high-exit block MUST NEVER appear in opportunities

### Writing requirements
- `title`: Reason first (why selected), then user decision/friction. No block_name in title.
- `analysis`: Facts (dwell+exit) + hypothesis (arriving-user mindset). Reference block_name here.

### Prioritization guidance
When presenting barriers and opportunities, help the user understand relative impact:
- **High impressionRate + high exitRate** barriers deserve the most attention (many users see it
  and leave — large absolute impact)
- **Low impressionRate** barriers affect fewer users — mention the reach limitation
- **Opportunities near conversion points** (Phase 3-4 blocks with high dwell + low exit) are
  especially valuable as they indicate strong engagement close to the decision moment

## 3) readingContributionRate usage
- Allowed but not mandatory
- If used: MUST include target-language definition sentence
- Treat as post-hoc hint, not primary ranking signal
- title MUST NOT mention readingContributionRate or its i18n terms

### When conversion.extreme_type = "top" or cvTag = "high" (MUST enrich)

When a block's conversion contribution is an extreme top performer, `insight` MUST include ALL THREE:

1. **Relative standing in plain language** — state this block has the highest conversion contribution:
   - CN: "全页转化贡献最高" / "转化贡献在所有区块中最突出"
   - EN: "highest conversion contributor among all blocks"
   - JA: "全ブロック中最もコンバージョン貢献が高い"

2. **User psychology** — explain what mindset led users to engage deeply AND convert here. Ground in
   what they experienced in preceding blocks (use prior-context when logically relevant). Use hedging.

3. **Percentage value** — cite the actual readingContributionRate value after the above context.

## 4) benchmark_fv comparison

First-view blocks (IS_FV = 1) may include `benchmark_fv` — the category benchmark for first-view
drop-off. Drop-off is lower-is-better:
- `fvDropOffRate < benchmark_fv` → good (below benchmark, do NOT call it "high")
- `fvDropOffRate > benchmark_fv` → concern (above benchmark)

When benchmark_fv exists, ALWAYS judge fvDropOffRate relative to it before framing as good or bad.

## Output Format (human-readable Markdown report)

Output a structured Markdown report in the **target language** — NOT JSON.
The template below uses English placeholders for clarity. Replace ALL headers, labels, and
analysis text with the target language. Use metric labels from quality-constraints.md.

### Report template

```markdown
# [page_type label] Analysis

> **Core Finding**: [core_insight — 1-2 sentences]

**Key Metrics**: [visits_label] [value] | [bounceRate_label] [value] | [fvDropOffRate_label] [value] | [avgDuration_label] [value] | [conversionsRate_label] [value]

---

## User Behavior Path

### Phase 1: [phase_name]
> [phase_summarize — one line]

**[block_name]** ([impressionRate_label] [val] | [avgStayTime_label] [val] | [exitRate_label] [val])
[insight — natural flowing narrative]

**[block_name]** (...)
[insight]

### Phase 2: [phase_name]
> [phase_summarize]
...

(repeat for all 4 phases, covering ALL blocks — no omissions)

---

## Barriers

### 1. [title — selection reason + user friction]
- **Block**: [block_name] ([phase_name])
- **Key metric**: [metricLabel] [value][unit]
- **Analysis**: [facts (dwell+exit) + hypothesis (arriving-user mindset)]

---

## Opportunities

### 1. [title — selection reason + engagement signal]
- **Block**: [block_name] ([phase_name])
- **Key metric**: [metricLabel] [value][unit]
- **Analysis**: [facts + hypothesis]

---

## Recommendations
1. [concrete, actionable suggestion]
2. [concrete, actionable suggestion]
3. [concrete, actionable suggestion]
```

### Template rules
- **Entire report in target language** — all headers, labels, analysis, suggestions
- Block metrics inline with block name for easy scanning
- All blocks must appear — no omissions
- Barriers before opportunities
- Suggestions specific enough to act on immediately
- Metric labels in target language (never camelCase field names)
