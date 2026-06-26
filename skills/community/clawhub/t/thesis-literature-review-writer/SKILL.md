---
name: thesis-literature-review-writer
description: Write detailed, academically rigorous Chinese literature review chapters or literature review sections for theses, dissertations, and undergraduate papers from a user's topic, research problem, variables/concepts, theory, method, population, references, and extra information. Use when users ask to write, expand, polish, organize, synthesize, or structure only the Literature Review/Chapter Two/文献综述/国内外研究现状 section, including search scope, conceptual review, theoretical review, empirical review, themes, gaps, critique, summary, and transition to research questions or design.
---

# Thesis Literature Review Writer

## Scope

Use this skill only to write the literature review part of a Chinese academic paper. The default output is a polished Chinese "第二章 文献综述" or "国内外研究现状" section.

Do not write the introduction, methodology, results, discussion, or conclusion chapters except for brief transitions that explain how the literature review supports the research problem, research questions, hypotheses, or study design.

## Required Reference

Before drafting a full literature review, read `references/literature-review-writing-guide.md`. It contains the search logic, chapter structure, synthesis strategies, Chinese templates, citation safeguards, and method-specific adaptations derived from the local `2review.txt` source.

## Input Extraction

Extract and use any information the user provides:

- Thesis title, research topic, or research problem
- Discipline and degree level
- Research type: quantitative, qualitative, mixed methods, literature review, intervention-scheme design, theoretical analysis
- Research object/population, setting, and data source
- Variables, concepts, themes, theory/model, intervention framework, or mechanisms
- Research questions, hypotheses, or research content
- Supplied references, notes, article summaries, citation style, and required databases
- School format requirements, word count, heading style, and domestic/foreign literature requirements

If the user does not provide references, draft with citation placeholders and recommend search terms. Do not invent exact references, author names, years, journal titles, findings, statistics, or DOI information.

## Drafting Workflow

1. Decide whether the user needs a full literature review chapter, a short "国内外研究现状" section, or one subsection.
2. Identify the organizing principle:
   - By variables/concepts for quantitative studies
   - By themes/experiences/context for qualitative studies
   - By theory, mechanism, intervention components, and evaluation evidence for intervention-scheme papers
   - By search scope, themes, debates, and gaps for review papers
3. Use a funnel structure: general literature first, then increasingly specific studies closest to the user's topic, population, method, and research questions.
4. Be selective: emphasize sources directly related to the study; summarize tangential sources briefly or exclude them.
5. Synthesize rather than list. Organize the chapter around concepts, theories, themes, trends, gaps, contradictory findings, practical significance, or continuing lines of inquiry.
6. Include an introduction/advance organizer at the start of the chapter and a summary at the end.
7. Use headings, subheadings, transitions, and topic sentences to make the review coherent.
8. Use placeholders for missing citations and flag where the user must add real sources.

## Output Standards

For a full literature review, include:

- A concise note listing assumptions, missing references, and recommended search terms if needed
- A complete Chinese draft with numbered headings
- An opening paragraph that states the scope and sequence of the review
- Thematic synthesis, not article-by-article annotation
- Critical evaluation of existing research gaps, contradictions, methods, populations, and limitations
- A short chapter summary that leads to the user's study
- Citation placeholders when exact sources are unavailable

Quality requirements:

- Every major subsection must connect to the research problem.
- The chapter must not be a pile of "某某认为/某某发现" summaries.
- Primary sources are preferred over secondary summaries.
- The most relevant literature receives the most detailed coverage.
- The summary should make the rationale for the user's research apparent.
- The writing should be formal Chinese academic prose.
