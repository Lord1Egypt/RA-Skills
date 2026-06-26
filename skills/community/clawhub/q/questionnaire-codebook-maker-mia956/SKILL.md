---
name: questionnaire-codebook-maker
description: Turn questionnaire items into clean research codebooks, scoring rules, reverse-scoring checks, variable names, and analysis-ready TSV/Markdown tables.
version: 1.0.0
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
    emoji: "🧾"
---

# Questionnaire Codebook Maker

## Purpose
Use this skill when the user needs to organize questionnaire items, scale dimensions, variable names, scoring rules, reverse-scored items, or data-entry specifications for psychology, education, public-health, social-science, or student research projects.

The core output is a clean codebook that can be copied into Word, Excel, SPSS, R, Mplus, or a research protocol.

## When to activate
Activate this skill when the user asks for any of the following:

- Convert questionnaire items into a codebook.
- Generate variable names for survey items.
- Mark reverse-scored items and compute scoring rules.
- Build a table for dimensions, item numbers, response anchors, and total scores.
- Prepare data-entry rules for Excel/SPSS/R/Mplus.
- Check whether questionnaire scoring is internally consistent.
- Convert a messy scale description into an analysis-ready table.

## Required output behavior
When the user provides questionnaire items, output the following sections unless they request a different format:

1. **量表代码本 / Codebook**  
   Provide a TSV table with these columns:
   `variable`, `item_id`, `dimension`, `item_text`, `response_range`, `reverse_scored`, `scoring_note`, `missing_rule`.

2. **计分规则 / Scoring rules**  
   Explain how to compute dimension scores and total scores. State whether to use sum scores or mean scores. If missing-value rules are not provided, recommend a transparent rule such as "calculate the mean score only when at least 80% of items in the dimension are non-missing".

3. **反向计分检查 / Reverse-scoring check**  
   List reverse-scored variables and give the formula. For a 1–5 item, use `reversed = 6 - original`. For a 0–4 item, use `reversed = 4 - original`.

4. **分析软件变量建议 / Analysis-ready variable names**  
   Provide short, readable variable names. Avoid spaces, Chinese punctuation, hyphens, and overly long names. Use prefixes such as `dep_`, `anx_`, `smu_`, `sleep_`, `neuro_`, or `eant_` when relevant.

5. **质量控制提示 / QC checklist**  
   Mention duplicate item IDs, inconsistent response ranges, missing dimensions, and reverse-scoring ambiguity.

## Variable-naming rules

- Use lowercase letters, numbers, and underscores only.
- Start with a letter.
- Keep names under 20 characters when possible.
- Preserve scale order using two-digit item numbers: `dep_01`, `dep_02`, `anx_01`.
- Use dimension prefixes when multiple dimensions exist.
- For Mplus compatibility, avoid names longer than 8 characters if the user explicitly asks for legacy Mplus-safe names.

## Reverse-scoring formulas

For an item with minimum `min` and maximum `max`:

`reversed_score = min + max - original_score`

Common examples:

- 1–5 scale: `reverse = 6 - original`.
- 1–7 scale: `reverse = 8 - original`.
- 0–4 scale: `reverse = 4 - original`.
- 0–10 scale: `reverse = 10 - original`.

## Missing-value rule recommendations

Use the user's stated rule when available. If no rule is given:

- Dimension mean score: compute if at least 80% of dimension items are valid.
- Total mean score: compute if at least 80% of all scale items are valid.
- Never silently impute missing values unless the user explicitly asks for imputation.

## Optional helper script
This skill includes `scripts/make_codebook.py`, which converts a simple CSV item file into a Markdown codebook and a TSV variable map. It uses only Python standard-library modules.

Input CSV columns:

`item_id,item_text,dimension,scale_min,scale_max,reverse`

Example command:

```bash
python3 scripts/make_codebook.py examples/demo_items.csv --out-dir output
```

If `python3` is not available, try:

```bash
python scripts/make_codebook.py examples/demo_items.csv --out-dir output
```

## Safety and integrity

- Do not invent item wording or scoring rules.
- Mark uncertain reverse-scoring decisions as uncertain.
- Do not change original item meaning when shortening labels.
- Do not assume a clinical cutoff unless the user provides the scale manual or asks for verified lookup.
- When converting scoring rules, distinguish between item-level reverse scoring, dimension score calculation, and total score calculation.
