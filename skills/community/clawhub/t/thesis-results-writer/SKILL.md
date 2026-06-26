---
name: thesis-results-writer
description: Write detailed, academically rigorous Chinese results chapters or results sections for theses, dissertations, and undergraduate papers from a user's quantitative data, tables, statistical outputs, research questions, hypotheses, qualitative themes, interview excerpts, case summaries, or extra information. Use when users ask to write, expand, polish, organize, or structure only the Results/Chapter Four/研究结果/结果分析/资料分析结果 section, including descriptive statistics, hypothesis testing, research-question results, tables, figures, additional analyses, qualitative themes, case results, and chapter summary.
---

# Thesis Results Writer

## Scope

Use this skill only to write the results part of a Chinese academic paper. The default output is a polished Chinese "第四章 研究结果" or "第四章 结果与分析" section.

Do not write the literature review, methodology, discussion, recommendations, or conclusion chapters. Results should report and organize findings objectively. Interpretation, comparison with previous studies, value judgments, and recommendations belong mainly in the discussion chapter.

## Required Reference

Before drafting a full results chapter, read `references/results-writing-guide.md`. It contains quantitative and qualitative results structures, table/figure rules, research-question reporting steps, Chinese templates, and quality checks derived from the local `4result.txt` source.

## Input Extraction

Extract and use any information the user provides:

- Thesis title, research type, research questions, hypotheses, and chapter format
- Quantitative data: sample demographics, descriptive statistics, reliability results, t tests, ANOVA, chi-square, correlations, regressions, effect sizes, p values, tables, charts, software output
- Qualitative data: themes, subthemes, codes, interview excerpts, participant IDs, case summaries, observation/document findings, cross-case results
- Mixed methods: quantitative results, qualitative themes, and how they are organized by research question or phase
- Additional analyses: demographic analyses, instrument analyses, post hoc analyses, assumption checks
- School style requirements, table numbering, decimal rules, and word count

If the user does not provide actual results, do not fabricate numbers, tables, quotes, themes, or statistical significance. Provide a results-chapter skeleton with placeholders and instructions for where to insert real findings.

## Research Type Decision

Infer the result type before writing:

- Quantitative: statistics, p values, means, standard deviations, sample counts, tests, hypotheses, SPSS/R/Excel output.
- Qualitative: themes, categories, codes, quotations, participants, cases, field notes, documents.
- Mixed methods: both numeric results and qualitative themes.
- Intervention-scheme design without implementation: do not call the scheme "results" unless the user's school expects a "方案设计结果" chapter; write the scheme output objectively and state no effectiveness results are available.
- Literature review/systematic review: results are literature screening, study characteristics, theme synthesis, and evidence summary.

## Drafting Workflow

1. Identify the research type and the safest results structure.
2. Start with a brief chapter introduction/advance organizer.
3. For quantitative studies, report descriptive statistics first, then research questions or hypotheses one by one, then additional analyses if any.
4. For qualitative studies, organize results by themes, subthemes, cases, participants, phases, or data sources, whichever best fits the data.
5. For mixed methods, separate or integrate quantitative and qualitative findings by research question, and avoid discussing implications too early.
6. Refer to every table/figure in the text before presenting it.
7. State results plainly and consistently, with statistics at the end of sentences where readable.
8. End with a chapter summary that synthesizes findings at a higher level and transitions to the discussion chapter.

## Output Standards

For a full results chapter, include:

- Research type and data availability note when needed
- Complete Chinese draft with numbered headings
- Tables or table placeholders when data are tabular
- Objective reporting of findings, not discussion
- Quantitative result statements aligned with each research question/hypothesis
- Qualitative theme statements supported by short anonymized excerpts when supplied
- Additional analyses only when the user provides or requests them
- Chapter summary and transition to the next chapter

Quality requirements:

- Do not invent data.
- Do not interpret causes from correlations or cross-sectional results.
- Do not repeat methodology in detail.
- Do not cite literature unless the user specifically asks for a combined results-discussion chapter.
- Keep sentence structures consistent for similar statistical tests.
- Report non-significant results as clearly as significant results.
- Preserve uncertainty and limitations for the discussion chapter.
