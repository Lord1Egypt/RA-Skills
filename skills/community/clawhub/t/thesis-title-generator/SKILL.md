---
name: thesis-title-generator
description: Generate three academically appropriate alternative thesis titles in both Chinese and English from a user's complete thesis, dissertation, undergraduate paper, graduation thesis, abstract, chapter draft, conclusion, research design, findings, or keywords. Use when users ask to refine, rename, translate, compare, or generate Chinese and English thesis titles, bilingual title options, final paper titles, or title recommendations based on a completed paper. Default to producing exactly three Chinese-English title pairs unless the user requests a different number.
---

# Thesis Title Generator

## Scope

Use this skill to generate final thesis title options after reading the user's thesis content. The default output is exactly three bilingual title pairs: each option includes a Chinese title and a corresponding English title.

This skill does not write the thesis body, abstract, or keywords. It focuses on title quality: accuracy, discoverability, academic tone, bilingual consistency, and whether the title's promise is fulfilled by the paper.

## Required Reference

Before generating full title options, read `references/title-generation-guide.md`. It contains title-design principles, quality checks, bilingual translation rules, title patterns, and output templates derived from the local `10title.txt` source.

## Input Extraction

Extract and use any information the user provides:

- Full thesis text, abstract, conclusion, or chapter excerpts
- Current title, advisor comments, school title requirements, discipline, and degree level
- Research object, population, setting, variables, concepts, themes, or cases
- Method, design, theory, model, intervention approach, or data source
- Main findings, contribution, application value, limitations, and research scope
- Keywords or required terminology in Chinese and English

If the user provides only a rough topic, generate provisional titles and clearly state that final titles should be checked against the completed thesis. Do not imply findings, methods, populations, or causal claims that are not present in the supplied material.

## Title Generation Workflow

1. Determine the thesis topic, study type, discipline, and final output language requirements.
2. Identify the title's essential content: object/population, core phenomenon or variable/theme, method or perspective when useful, and contribution or application when supported.
3. Avoid using the early working title if it only names the research activity. Convert it into a final title that signals what the thesis actually offers.
4. Generate exactly three Chinese-English title pairs by default:
   - Option 1: conservative and academically standard.
   - Option 2: method- or perspective-focused.
   - Option 3: contribution-, application-, or problem-focused when supported by the thesis.
5. Check every title against the paper: the reader's expectations from the title must be fulfilled by the thesis content.
6. Provide a short recommendation explaining which option is strongest and why.

## Output Standards

For a full title-generation task, include:

- A brief basis for title extraction when useful
- Three Chinese-English title pairs
- One-sentence rationale for each pair
- A recommended title
- Optional notes on terms to avoid, overclaiming, or title risks

Quality requirements:

- Do not fabricate results, methods, populations, interventions, theories, or contributions.
- Do not overstate causal effects, effectiveness, innovation, or application value.
- Do not overload titles with too many nouns, prepositions, variables, or keywords.
- Avoid unexplained acronyms unless they are standard in the discipline and the thesis audience will understand them.
- Keep Chinese and English titles equivalent in meaning, not word-for-word when natural academic translation requires adjustment.
- Preserve required technical terms from the thesis when they are central.
