# Report Review Checklist

Load this file when `--review` is called and as the silent final review pass during `--generate`.

This checklist is designed for **one-pass automatic refinement**. It is not an interactive approval workflow.

## Overview

The report review system keeps only the rules that fit `kai-report-creator`'s operating model:

- the AI can judge the issue from source/IR/HTML alone
- the AI can fix it directly with a rewrite or structural adjustment
- the rule does not depend on outside human feedback or image-level interpretation

The system has **13 checkpoints**:

- **Category 0: Visual Hard Rules (5)** — auto-apply during the silent final pass
- **Category 1: Hard Rules (5)** — auto-apply when violated
- **Category 2: AI-Advised Rules (3)** — apply only when confidence is high

## Category 0: Visual Hard Rules (auto-apply during `--generate` silent pass)

These are structural checks from `references/design-quality.md` §7 (Pre-Output Self-Check). Fix automatically before writing HTML.

### 0.1 KPI Value Validity

**Trigger:** Every `.kpi-value` element and `report-summary` JSON `kpis[].value` field.

**Detection:** If any KPI value is a placeholder (`[数据待填写]` / `[INSERT VALUE]`), lacks a real number, or contains a sentence/paragraph longer than 8 Chinese characters or 3 English words, it fails.

**Auto-fix:** Extract the key number for the KPI value. Move status words to badges and move explanations to adjacent prose, a callout, or a table cell. If there is no real number, remove the KPI card and use a callout, timeline, or table row instead.

### 0.2 Badge Coverage

**Trigger:** Every report.

**Detection:** Count `.badge` elements in the HTML. If fewer than 2 distinct locations contain badges, it fails.

**Auto-fix:** Add badges at appropriate locations — section headers (category tags), KPI labels (status), table cells (progress), or timeline items (milestones). See `references/rendering-rules.md` for badge generation rules.

### 0.3 Summary Card Poster Hierarchy

**Trigger:** Every generated report with a summary card.

**Detection:** Flag summary cards that read like compact metadata panels instead of poster-style entry cards:

- title is not visually dominant
- title and subtitle are merged into one dense line
- audience/byline/filler copy is injected into the card
- the card exposes small tags but no clear poster headline

**Auto-fix:** Only use `poster_title` / `poster_subtitle` when the report truly needs a stronger poster headline than the document title. Keep subtitle below the poster title, remove filler meta copy, and make the poster title dominate the card. Remove chips, bottom notes, and metadata filler if they weaken the poster read. If the left panel reads like a paragraph block instead of a poster, compress it to one short sentence at the bottom. If the left panel shows broken line wraps or wasted width, reduce title size and widen subtitle/note measure before changing content. If wrap quality is fixed but the title loses visual weight, increase the title within the available width before adding more copy.

### 0.4 Timeline Content Validity

**Trigger:** Every `:::timeline` / `.timeline` component.

**Detection:** If timeline items use generic labels instead of actual dates/timestamps (e.g. "真诚服务" as a date), it fails. If items could be reordered without changing meaning, they are not timeline content.

**Auto-fix:** Convert to `:::list` or prose with `:::callout`. Preserve the content, change the component type.

### 0.5 Export Menu Completeness

**Trigger:** Every generated HTML report.

**Detection:** The shell fails if any of these are missing:

- `id="export-btn"`
- `id="export-menu"`
- `id="export-print"`
- `id="export-png-desktop"`
- `id="export-png-mobile"`
- `id="export-im-share"`
- JS bindings for all four export entries

An export menu with only some items still fails.

**Auto-fix:** Reconstruct the entire export button/menu + JS wiring block from `references/html-shell-template.md`. Do not patch the menu incrementally if one item is missing.

**Fallback:** None. This is a shell integrity failure.

## Category 1: Hard Rules

These rules are deterministic enough to apply automatically.

### 1.1 BLUF Opening

**Trigger:** Every report.

**Detection:** Check the opening paragraph. It should establish at least two of:

- the document's purpose
- the core finding
- the expected action

If the opening is mostly background, definitions, or scene-setting, it fails.

**Auto-fix:** Rewrite the first paragraph into a short executive summary:

- sentence 1: what this report is for
- sentence 2: the main finding or most important judgment
- sentence 3: what the reader should do, watch, or decide next

**Fallback:** If the source does not support a concrete action, keep purpose + finding and avoid inventing a recommendation.

### 1.2 Heading Stack Logic

**Trigger:** Reports with H1/H2/H3 structure.

**Detection:** Read the heading stack alone. It should form a meaningful outline, not a bag of disconnected nouns.

Bad patterns:

- headings that are all pure labels
- repeated generic section types with no progression
- adjacent headings that do not imply problem, mechanism, implication, or action

**Auto-fix:** Rewrite headings into information-bearing statements that preserve the original content but improve progression.

**Fallback:** If the overall outline is sound, only rewrite the weak headings rather than reordering sections.

### 1.3 Anti-Template Section Headings

**Trigger:** Every H2/H3.

**Detection:** Flag headings such as:

- `Overview` / `概述` / `简介` / `背景`
- `Background` / `背景`
- `Key Findings` / `关键发现`
- `Summary` / `总结` / `结论`
- `Next Steps` / `下一步` / `展望`
- `身份定位` / `核心能力` / `核心原则` / `使用场景` / `方法论`
- `问题分析`
- Any heading that is a generic label without content-specific information

when they do not carry section-specific information.

**Auto-fix:** Rewrite the heading into a concrete, content-specific statement or implication.

**Fallback:** If the section itself is too vague, tighten the opening lines of that section along with the heading.

### 1.4 Prose Wall Detection

**Trigger:** Every prose section.

**Detection:** Flag paragraphs that are too dense to skim:

- Chinese paragraphs over ~150 characters
- English paragraphs over ~120 words
- or visually 5+ lines with no list, no sub-break, and no emphasis anchor

**Auto-fix:** Split the text into shorter paragraphs, bullets, or a `claim -> explanation` structure. When the section has a strong thesis, promote a decisive opening sentence into a lead block. In HTML terms, that means upgrading it into a `lead-block`. When one sentence carries the whole judgment, use a `section-quote`. When the section resolves into several concrete moves, use an `action-grid`.

These are optional upgrades, not a quota. When unsure, prefer paragraph splits or one ordinary scan anchor over decorative cadence blocks.

**Fallback:** If the text is a continuous argument, preserve the reasoning but add paragraph breaks and one scan anchor.

### 1.5 Takeaway After Data

**Trigger:** Every `:::kpi`, `:::chart`, and `:::table` block.

**Detection:** Check the adjacent prose. If the component appears without a clear interpretation of what it means, it fails.

**Auto-fix:** Add a takeaway sentence after the component, such as:

- "This shows ..."
- "The key implication is ..."
- "What matters here is ..."

**Fallback:** If the source does not justify causal claims, summarize pattern or contrast only.

## Category 2: AI-Advised Rules

These rules require judgment. Apply them only when the source supports the move with high confidence.

### 2.1 Insight Over Data

**Trigger:** A section is dominated by KPI/chart/table content.

**Detection:** The section repeats numbers but does not explain significance, cause, risk, or action.

**Auto-fix:** Add a short insight paragraph connecting the numbers to implication, risk, or next move.

**Fallback:** If root cause is not supported, provide implication only and avoid speculation.

### 2.2 Scan-Anchor Coverage

**Trigger:** Long sections or multiple consecutive prose paragraphs.

**Detection:** Flag sections that have no skim anchors, such as:

- bold phrase
- callout
- highlight sentence
- list
- explicit mini-summary sentence

**Auto-fix:** Add the lightest anchor that improves scanning without adding visual noise.

Preferred order:

1. mini-summary sentence
2. `highlight-sentence`
3. local bold emphasis
4. `:::callout`

**Fallback:** If the section is already visually dense, add one strong concluding sentence instead of a new component.

### 2.3 Conditional Reader Guidance

**Trigger:** Tutorial, implementation guide, solution proposal, or internal methodology report.

**Detection:** If the report is clearly instructional, check whether the opening tells the reader:

- who this is for
- what prior knowledge is assumed
- what the reader will gain

**Auto-fix:** Add a compact audience / prerequisite / outcome block near the summary.

**Fallback:** Skip entirely for dashboards, business updates, research summaries, or general analysis reports.

## Rejected Candidates

These ideas were considered and intentionally excluded from the automated system.

- **"Can a coworker understand this chart with no context?"**
  Rejected because it depends on external human validation.

- **"Every screenshot must have red boxes, blur, and precise highlighting."**
  Rejected because the current workflow does not include reliable image review/editing.

- **"MECE must be fully exhaustive."**
  Rejected because the AI can spot overlap and jump cuts, but cannot reliably prove completeness.

- **"Every report must declare target reader and prerequisite knowledge."**
  Rejected because that would over-constrain summary and reporting documents.

## Execution Order

Run the review in this order:

0. **Visual Hard Rules** (KPI Value Length, Badge Coverage, Timeline Content Validity, Export Menu Completeness)
1. BLUF Opening
2. Heading Stack Logic
3. Anti-Template Section Headings
4. Prose Wall Detection
5. Takeaway After Data
6. Insight Over Data
7. Scan-Anchor Coverage
8. Conditional Reader Guidance

This order prioritizes:

- why the reader should keep going
- how the argument is organized
- how easily the document can be skimmed
- how data gets interpreted into action
