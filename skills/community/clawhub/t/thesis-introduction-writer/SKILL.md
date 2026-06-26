---
name: thesis-introduction-writer
description: Write detailed, academically rigorous Chinese introduction chapters or introduction sections for theses, dissertations, and undergraduate papers from a user's topic, study background, research content, method, variables/concepts, population, theory, and extra information. Use when users ask to write, expand, polish, or structure only the Introduction/Chapter One/绪论/引言, including background, problem statement, purpose, significance, definitions, theoretical framework, research questions or hypotheses, limitations, delimitations, assumptions, and organization of the study.
---

# Thesis Introduction Writer

## Scope

Use this skill only to write the introduction part of a Chinese academic paper. The default output is a polished Chinese "第一章 绪论" or "引言" section that the user can continue editing.

Do not write the literature review, methods, results, or discussion chapters except for a brief "论文结构安排" overview inside the introduction.

## Required Reference

Before drafting a full introduction, read `references/introduction-writing-guide.md`. It contains the section logic, Chinese wording templates, quality checks, and method-specific adaptations derived from the local `1intro.txt` source.

## Input Extraction

Extract and use any information the user provides:

- Thesis title or research topic
- Discipline and degree level
- Research type: quantitative, qualitative, mixed methods, literature review, intervention-scheme design, theoretical analysis
- Research object/population, setting, time, and data source
- Research content, variables, concepts, theory/model, or intervention framework
- Research problem, literature gap, or practical problem
- Research purpose, questions, or hypotheses
- Significance, innovation, limitations, delimitations, and assumptions
- School format requirements, word count, heading style, and citation style

If important information is missing, proceed with clearly marked placeholders rather than stopping, unless the missing choice would change the research design.

## Drafting Workflow

1. Decide whether the user needs a full introduction chapter, a short journal-style introduction, or one specific subsection.
2. Choose headings that match the paper type and school convention.
3. Build the introduction in this order unless the user provides another format:
   - 研究背景
   - 问题提出
   - 研究目的
   - 研究意义
   - 核心概念界定
   - 理论基础/理论框架
   - 研究问题或研究假设
   - 研究限制、研究界定与研究假设条件
   - 论文结构安排
4. Adapt question/hypothesis wording to method:
   - Quantitative studies may use descriptive, relationship, or difference questions and hypotheses.
   - Qualitative studies should normally use open research questions, not formal hypotheses.
   - Grounded-theory studies may treat hypotheses or propositions as possible outcomes, not starting assumptions.
   - Review and intervention-scheme papers should use research objectives/content rather than statistical hypotheses.
5. Write in formal Chinese academic style with coherent transitions and no casual advice language inside the drafted section.
6. Do not invent exact citations. If the user has not supplied sources, use placeholders such as "已有研究表明……（此处补充文献）". Browse only when the user asks for current sources or exact references.

## Output Standards

For a full introduction, include:

- A concise note listing assumptions and missing items, if any
- A complete Chinese draft with numbered headings
- Section content that is aligned with the user's method and topic
- Placeholders for missing citations, data, names, or local context
- A short revision checklist after the draft, unless the user asks for draft-only output

Quality requirements:

- The background must lead logically to the problem statement.
- The problem statement must identify the exact research problem, not just a broad topic.
- The purpose must directly answer the problem statement.
- The significance must argue theoretical, practical, and when relevant methodological value.
- Definitions must cover key variables, concepts, population attributes, and theory/model names.
- Theoretical framework must connect theory to research questions, data collection, analysis, and interpretation.
- Limitations, delimitations, and assumptions must be distinguished.
