---
name: social-science-abstract-polisher
description: "Reusable prompt for refining social science academic abstracts to align with peer-reviewed journal requirements including APA 7th edition compliance. Use when polishing, revising, or improving a social science abstract for journal submission, or when asked to make an abstract APA-compliant, strengthen its logical flow, or reduce wordiness."
---

# Social Science Journal Abstract Polisher

## Purpose

Refine social science abstracts for peer-reviewed journal submission without altering core research content.

## Input

An English abstract (plain text) from a social science manuscript.

## Procedure

Apply the following transformations **sequentially**. Do not add, remove, or reinterpret substantive research claims.

### 1. APA 7th Edition Compliance

- Enforce APA 7th abstract standards: ≤250 words unless a journal specifies otherwise; no citations or references; no abbreviation without prior definition; use past tense for completed research; use active voice as default.
- Replace first-person plural/singular with appropriate third-person constructions where APA style prefers objectivity (e.g., "The authors conducted…" or passive where conventional), unless the journal's guidelines explicitly permit first person.

### 2. Structural Flow Enhancement

- Ensure the abstract contains four clearly sequenced components: **Background → Method → Findings → Implications**.
- If any component is missing or underdeveloped, flag it explicitly in the output rather than fabricating content.
- Insert brief transitional phrasing between components so the logical arc is explicit (e.g., "Building on this gap,…", "To address this,…", "Results revealed…", "These findings suggest…").
- Maintain proportional balance: roughly 20-25% Background, 20-25% Method, 30-35% Findings, 15-20% Implications.

### 3. Formal Academic Register

- Upgrade informal or conversational phrasing to formal academic prose.
- Replace vague quantifiers ("a lot of", "some") with precise descriptors or retain the original specificity.
- Ensure terminology is consistent throughout (no synonym-switching for the same construct).
- Eliminate hedging that undercuts the research (e.g., "might possibly indicate" → "suggests"), while preserving appropriate caution where the original is genuinely tentative.

### 4. Redundancy Elimination

- Remove redundant modifiers ("completely eliminated" → "eliminated"; "future implications" → "implications").
- Merge overlapping sentences that repeat the same idea.
- Delete filler phrases ("It is important to note that", "In this study, we", "The purpose of this paper is to") unless they serve a genuine structural role.
- Verify the final word count; if still over limit, continue trimming redundancy before cutting substance.

## Output Format

Return the polished abstract followed by a brief change summary:

1. **Polished Abstract** — the refined text, under APA word limits.
2. **Change Summary** — bullet list of the most significant edits grouped by category (APA compliance / Flow / Register / Redundancy), noting anything flagged as missing or underdeveloped.

## Constraints

- Never invent data, results, or implications not present in the input.
- Never alter the study's theoretical framing or core argument.
- If the input is too short or too incomplete to polish meaningfully, return the original with a diagnostic note instead of guessing.
