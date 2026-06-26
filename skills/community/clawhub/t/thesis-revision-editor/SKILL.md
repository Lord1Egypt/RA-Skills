---
name: thesis-revision-editor
description: Review, revise, and save a complete thesis, dissertation, undergraduate paper, graduation thesis, proposal, or chapter draft from a user's full text or file path. Use when users ask for thesis revision suggestions, a modification list, line-by-line or chapter-by-chapter academic editing, rewriting according to comments, improving logic and scholarly quality, producing a complete revised thesis, saving the revised version, and explaining what was changed and why. Default to the same language as the thesis unless the user requests another language.
---

# Thesis Revision Editor

## Scope

Use this skill to turn a supplied thesis or thesis file into a revised thesis with a clear modification plan, completed edits, saved revised file, and concise explanation of changes.

This skill can handle full theses, undergraduate papers, proposals, chapter drafts, and advisor-reviewed drafts. It should improve academic quality, structure, logic, clarity, consistency, and defensibility while preserving the user's research design, data, findings, and voice unless the user explicitly asks for substantive rewriting.

## Required Reference

Before performing a full thesis review or revision, read `references/thesis-revision-guide.md`. It contains the chapter-by-chapter quality checklist, issue severity rules, revision workflow, saving rules, change-log format, and academic safeguards derived from the local `7suggestion.txt` source.

## Input Extraction

Extract and use any information the user provides:

- Thesis title, discipline, degree level, school format, advisor comments, rubric, and target language
- Full thesis text or file path
- Chapter structure and headings
- Research problem, purpose, significance, theory, research questions, hypotheses, variables, concepts, or themes
- Literature review scope, reference style, source currency, and citation issues
- Method: participants, instruments, data collection, data analysis, ethics, validity/reliability, trustworthiness
- Results: tables, figures, statistics, qualitative themes, interpretations, and missing transitions
- Discussion/conclusion: interpretation, implications, limitations, future research, and conclusion logic
- Formatting requirements, word count, section order, and requested output filename

If the user provides only a partial chapter, revise only that material and do not claim the whole thesis has been checked. If the full thesis is too long for one response, revise and save the complete file when possible, then summarize changes by chapter.

## Revision Workflow

1. Determine the thesis language and write suggestions, revised text, and change explanations in that language unless the user requests otherwise.
2. Read the thesis or supplied file carefully. If the user provides a file path, preserve the original and create a revised copy.
3. Build a brief thesis profile: title, topic, method, data type, chapter structure, and main quality risks.
4. Produce a prioritized modification list before editing. Group by chapter and severity.
5. Revise item by item according to the modification list.
6. Preserve factual content: do not invent data, findings, citations, sample details, instruments, or references.
7. Save the revised thesis:
   - If the input is a local file, save a new copy next to it using a suffix such as `_revised` or `_修改稿`.
   - If the input is pasted text, save a Markdown file in the current working directory unless the user specifies another path.
   - Do not overwrite the original unless the user explicitly asks.
8. Report the saved path, what changed, and why the changes improve the thesis.

## Revision Standards

Use chapter-appropriate standards:

- Introduction: clear background, problem, purpose, significance, definitions, theory, research questions, limitations, and chapter organization.
- Literature review: comprehensive and relevant coverage, concept/variable alignment, synthesis rather than source-by-source listing, accurate citations, summary and transition.
- Methodology: clear participants/data sources, sampling, instruments/materials, data collection, data analysis, validity/reliability or trustworthiness, ethics, and replicability.
- Results: objective presentation, table/figure clarity, correct organization by research question/hypothesis/theme, no premature discussion.
- Discussion and conclusion: interpretation grounded in findings, links to theory and literature, implications derived from findings, limitations, future research, and defensible conclusions.

## Output Standards

For a full thesis revision task, provide:

- A prioritized modification list
- A short note about the revision strategy
- The saved revised file path
- A change log with each major change and reason
- The complete revised thesis text when it fits comfortably in the response; otherwise provide the saved file path and a concise chapter-by-chapter summary
- Any remaining issues that require user-supplied data, references, school format, or advisor confirmation

Quality requirements:

- Do not fabricate academic content.
- Do not add fake citations or unsupported recent literature.
- Do not change the study design, sample, data, results, or conclusions beyond what the supplied thesis supports.
- Do not erase the user's original argument unless it is logically inconsistent or unsupported.
- Preserve citation markers and reference entries where possible.
- Keep edits academically formal but readable.
- Flag unresolved factual gaps instead of silently filling them.
