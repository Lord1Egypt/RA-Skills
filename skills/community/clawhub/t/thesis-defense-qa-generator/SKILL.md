---
name: thesis-defense-qa-generator
description: Generate likely thesis, dissertation, undergraduate paper, or graduation-project defense questions and strong reference answers from a user's complete thesis, proposal, abstract, chapter draft, or defense materials. Use when users ask for oral defense preparation, viva questions, committee questions, likely questions and answers, mock defense Q&A, thesis defense scripts, or rebuttal practice. The questions and answers must use the same dominant language as the thesis unless the user requests another language.
---

# Thesis Defense Q&A Generator

## Scope

Use this skill to analyze a user's thesis or proposal and produce likely defense questions with evidence-based reference answers. Default to the same dominant language as the thesis. If the thesis is Chinese, output Chinese. If the thesis is English, output English. If the thesis is bilingual or the user specifies a language, follow the user's explicit language preference.

This skill does not rewrite the thesis itself. It prepares defense questions, answer scripts, and response strategies based on the existing document.

## Required Reference

Before generating a full defense Q&A set, read `references/defense-qa-guide.md`. It contains defense formats, question categories, answer construction rules, language-matching rules, proposal/final-defense differences, difficult-question strategies, and quality checks derived from the local `6questions.txt` source.

## Input Extraction

Extract and use any information the user provides:

- Thesis title, abstract, keywords, discipline, degree level, school requirements, and defense format
- Full thesis chapters: introduction, literature review, methodology, results, discussion, conclusion, references, appendices
- Research problem, purpose, significance, theoretical framework, research questions, hypotheses, variables, themes, or model
- Method: sample/participants, instruments, data collection, data analysis, validity/reliability, trustworthiness, ethics, limitations
- Results: main findings, non-significant results, unexpected results, qualitative themes, tables, figures, or case findings
- Discussion: interpretation, contribution, practical implications, limitations, future research, and conclusions
- Known weak points: small sample, limited literature, instrument issues, data constraints, formatting concerns, or advisor comments

If the user provides only a title or abstract, generate a smaller provisional Q&A set and clearly mark answers that require confirmation from the full thesis. Do not invent findings, methods, sample details, citations, or conclusions.

## Defense Type Decision

Infer the likely defense type:

- Proposal/opening defense: focus on problem, purpose, literature gap, theoretical framework, research questions/hypotheses, methodology, feasibility, ethics, and planned analysis.
- Final oral defense: focus on what the student did, what was found, what the findings mean, contribution, limitations, implications, and future research.
- Undergraduate thesis defense: use practical, concise answers and prioritize topic choice, method rationale, results, innovation, limitations, and revisions.
- Master's/doctoral viva: include deeper theoretical, methodological, statistical, literature, contribution, and critical evaluation questions.

If the user provides a complete thesis, default to final oral defense.

## Drafting Workflow

1. Determine the dominant language of the thesis and use that language for all questions and answers.
2. Identify the defense type and degree level.
3. Build a concise thesis profile: topic, purpose, method, data, findings, contribution, limitations.
4. Generate questions across all relevant categories: topic, literature, theory, method, ethics, results, discussion, limitations, implications, future research, and document quality.
5. Tailor each question to the user's actual thesis rather than giving generic questions only.
6. Write answers that are respectful, concise, scientific, and grounded in the thesis.
7. Include difficult or critical questions that a committee might ask, especially about weak points.
8. When information is missing, provide a cautious answer template with placeholders and specify what the user must verify.

## Output Standards

For a full thesis defense Q&A set, include:

- A short thesis profile
- 15-30 likely defense questions for undergraduate work, or more if the user requests depth
- Grouped categories with clear headings
- For each item: likely question, reference answer, answer basis in the thesis, and optional preparation note
- A small section for difficult follow-up questions and response strategies
- Same language as the thesis unless otherwise requested

Quality requirements:

- Do not fabricate thesis content.
- Do not invent citations, data, findings, sample details, or statistical results.
- Keep answers complete but not lecture-length.
- Use a calm, professional, evidence-based defense tone.
- Acknowledge limitations directly and convert reasonable suggestions into future research or revision plans.
- If the question is outside the thesis scope, explain the boundary and show how it can be addressed in future research.
