---
name: thesis-conclusion-writer
description: Write detailed, academically rigorous Conclusion sections or final conclusion chapters for theses, dissertations, undergraduate papers, graduation theses, journal-style papers, and research reports from a user's complete thesis, abstract, results, discussion, findings, contribution, limitations, and future-research information. Use when users ask to write, draft, expand, polish, or structure only the Conclusion/Conclusions/结论/研究结论/结论与展望 section. Default to the same dominant language as the thesis unless the user requests another language.
---

# Thesis Conclusion Writer

## Scope

Use this skill only to write the conclusion part of a thesis or academic paper. The default output is a polished "结论", "研究结论", "结论与展望", or English "Conclusion/Conclusions" section based on the user's supplied thesis.

Do not write a new introduction, literature review, methodology, results chapter, or full discussion chapter. The conclusion should synthesize the study's outcome and take-home message; it should not introduce new data, new literature, new analysis, or unsupported claims.

## Required Reference

Before drafting a full conclusion section, read `references/conclusion-writing-guide.md`. It contains conclusion structures, the generic conclusion model, language rules, contribution-ownership rules, Chinese and English templates, and quality checks derived from the local `8conclusion.txt` source.

## Input Extraction

Extract and use any information the user provides:

- Complete thesis text, abstract, or chapter excerpts
- Thesis title, discipline, degree level, school format, and target language
- Research problem, aim, gap, theoretical framework, research questions, hypotheses, variables, concepts, or themes
- Method or approach, only as much as needed to identify what the study did
- Key results, findings, supported/unsupported hypotheses, qualitative themes, or case conclusions
- Discussion points, contribution, practical implications, applications, limitations, and future research
- Required conclusion length, heading style, and whether the school expects "研究结论", "创新点", "不足与展望", or "建议"

If the user provides no findings or only a title, do not invent conclusions. Produce a conclusion framework with placeholders and list the exact thesis materials needed.

## Conclusion Type Decision

Infer the conclusion format before writing:

- Short conclusion: one to three paragraphs, suitable for article-style papers or when the discussion already contains limitations and implications.
- Thesis conclusion chapter: a longer final section/chapter with research conclusions, contribution, implications, limitations, and future directions.
- Undergraduate Chinese conclusion: concise and concrete, usually including "研究结论", "实践启示/研究意义", and "不足与展望".
- Empirical quantitative conclusion: answer each research question or hypothesis using defensible conclusion statements.
- Qualitative conclusion: synthesize themes, experience patterns, theoretical insight, transferability, and contextual limits.
- Intervention-scheme design conclusion: summarize the designed scheme and its theoretical/practical value; do not claim effectiveness without implementation data.
- Literature-review conclusion: synthesize evidence patterns, main gaps, and future research directions.

## Drafting Workflow

1. Determine the thesis language and use that language unless the user requests otherwise.
2. Identify the conclusion type and school heading requirements.
3. Extract the study's main achievement and take-home message from the whole thesis, not only the abstract.
4. Select relevant conclusion components: what the paper did, what it achieved, key findings, implications, limitations, applications, contribution, and future directions.
5. Convert results into conclusion statements that answer the research questions without repeating detailed statistics or raw data.
6. Make the study's own contribution explicit using phrases such as "本研究发现", "本文表明", "This study shows", or "The present thesis demonstrates".
7. Keep conclusions proportional to the evidence, sample, method, and design.
8. End with a clear closing sentence that states the study's overall value and remaining direction.

## Output Standards

For a full conclusion section, include:

- Complete conclusion text with appropriate numbered headings when needed
- Main research conclusions derived from findings
- Explicit take-home message
- Contribution or advancement of knowledge/practice when supported
- Practical application or implication when appropriate
- Limitations and future directions if the target format includes them
- Same language as the thesis unless otherwise requested

Quality requirements:

- Do not fabricate findings, data, citations, applications, or future work.
- Do not copy the abstract; use the thesis as the source and synthesize.
- Do not overstate causality, generalizability, or effectiveness.
- Do not introduce new evidence in the conclusion.
- Do not simply summarize chapter contents; state what the study has established.
- Keep the conclusion explicit enough for readers who skip directly from title or abstract to conclusion.
