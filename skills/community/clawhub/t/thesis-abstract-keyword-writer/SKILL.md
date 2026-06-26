---
name: thesis-abstract-keyword-writer
description: Write academically rigorous Abstract and Keywords sections for theses, dissertations, undergraduate papers, graduation theses, journal-style papers, research reports, and proposals from a user's complete thesis, chapter draft, abstract draft, results, discussion, conclusion, contribution, and school requirements. Use when users ask to write, draft, polish, shorten, expand, structure, translate, or generate 摘要/关键词, Abstract/Keywords, structured abstracts, Chinese abstracts, English abstracts, bilingual abstracts, or keyword lists. Default to the same dominant language as the thesis unless the user requests another language or bilingual output.
---

# Thesis Abstract & Keywords Writer

## Scope

Use this skill only to write the Abstract/摘要 and Keywords/关键词 part of a thesis or academic paper. The default output is a polished abstract plus 3-8 keywords based on the user's supplied thesis.

Do not write the introduction, literature review, methodology chapter, results chapter, discussion chapter, conclusion chapter, or full thesis unless the user separately asks. The abstract should be a standalone, high-clarity text derived from the completed paper, not a loose chapter-by-chapter summary.

## Required Reference

Before drafting a full abstract and keyword set, read `references/abstract-keyword-writing-guide.md`. It contains the generic abstract model, structured abstract patterns, clarity rules, contribution-ownership rules, keyword selection rules, Chinese and English templates, and quality checks derived from the local `9Abstract.txt` source.

## Input Extraction

Extract and use any information the user provides:

- Complete thesis text, title, abstract draft, or chapter excerpts
- Thesis language, discipline, degree level, school format, word/character limit, and whether bilingual output is required
- Research background, problem, aim, gap, theoretical framework, research questions, hypotheses, variables, concepts, or themes
- Method or approach: sample, participants, materials, instruments, data source, analysis method, or design type
- Key findings, results, themes, supported/unsupported hypotheses, or scheme-design outputs
- Contribution, implications, applications, limitations, future directions, and conclusion
- Required keyword count, punctuation style, and Chinese/English keyword capitalization conventions

If the user provides only a title or incomplete thesis information, do not invent methods, findings, data, or keywords that imply unsupported results. Provide a provisional abstract framework and list the missing information needed.

## Abstract Type Decision

Infer the correct abstract type before writing:

- Standard/unstructured abstract: one paragraph, common for undergraduate papers and many journal-style papers.
- Structured abstract: uses headings such as Background/Objectives/Methods/Results/Conclusion, or 目的/方法/结果/结论.
- Chinese undergraduate thesis abstract: concise paragraph or paragraphs covering background, purpose, method, results, conclusion/significance, plus keywords.
- English abstract: clear, direct, accessible academic English, usually matching the Chinese abstract in content if bilingual.
- Empirical quantitative abstract: include aim, sample/method, key statistical findings at an appropriate level, and conclusion.
- Qualitative abstract: include purpose, participants/data sources, analysis method, themes, and meaning/contribution.
- Mixed-methods abstract: include both quantitative and qualitative strands and their integration.
- Literature-review abstract: include review scope, method of literature selection if any, synthesis themes, and conclusion.
- Intervention-scheme design abstract: state the scheme was designed from theory/literature; do not claim effectiveness without implementation data.

## Drafting Workflow

1. Determine the thesis language and output language. Match the thesis unless the user requests another language or bilingual output.
2. Identify the abstract type, word/character limit, and keyword requirements.
3. Extract the central contribution from the whole thesis, not only the existing abstract.
4. Build the abstract around the generic model: background/problem, aim, method, key results, implication/contribution.
5. Prioritize the main achievement and take-home message; do not overload the abstract with minor details.
6. Make the study's own contribution explicit using phrases such as "本研究", "本文", "This study", or "The present thesis".
7. Select 3-8 keywords from the title, core concepts, variables/themes, population, method, and field.
8. Keep wording consistent: do not call the same object a model, scheme, framework, and tool unless the thesis distinguishes them.

## Output Standards

For a complete abstract/keywords task, include:

- `摘要` and `关键词` for Chinese output, or `Abstract` and `Keywords` for English output
- Bilingual abstract and keyword sections when requested or required
- A standalone abstract that can be understood without reading the thesis
- Clear statement of purpose, method, key findings, and contribution
- Keywords that reflect the core topic and are not sentence fragments
- Same language as the thesis unless otherwise requested

Quality requirements:

- Do not fabricate findings, data, citations, methods, sample details, or practical implications.
- Do not cite literature in the abstract unless the paper directly depends on a specific work and the user supplies it.
- Do not make the abstract a list of chapter contents.
- Do not use undefined acronyms unless necessary; define once if used.
- Do not overstate causality, generalizability, or effectiveness.
- Keep sentences clear and avoid long, overloaded sentences.
- Use cautious language for early-stage, correlational, qualitative, or non-implemented designs.
