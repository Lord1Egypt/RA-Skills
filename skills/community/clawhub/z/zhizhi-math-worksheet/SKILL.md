---
name: zhizhi-math-worksheet
description: "Create printable elementary math worksheets and separate answer keys from a full worksheet photo/PDF or a list of questions. Make similar questions, format existing questions, or build practice from selected mistakes and review topics. Supports English and Chinese output. Use the math coach for grading, learning records, and mastery assessment."
---

# Zhizhi Math Worksheets

Design questions, diagrams, and page layouts; deliver a student worksheet and a separate answer key. This skill works independently: no learning archive, coach skill, GitHub account, or image-generation service is required. Mistakes and review topics guide upstream question selection; diagnosis is optional input.

## Optional math-coach integration

The companion is `@linzi007/zhizhi-math-coach` (skill name `zhizhi-math-coach`); this package is `@linzi007/zhizhi-math-worksheet`. When both are installed and visible to the same agent, accept the coach's selected questions, optional diagnosis, learned scope, output-language preferences and output directory without making the parent repeat them. Use the actual installed skill catalog when the coach's instructions are needed, not a guessed sibling path. This is instruction-level cooperation in the current conversation, not a separate agent or an automatic package dependency.

On completion, return student/answer PDF paths, previews, the private answer-manifest path, source-question mappings and actual review status to the calling workflow. The coach then owns any requested or already-configured archive, sync and publishing actions. Do not re-enter diagnosis or generation on return. If the user later submits completed work for grading or mastery tracking, use the installed coach when available; never treat the generated answer key as evidence of the student's performance. Standalone generation does not require installing or invoking the coach.

## Language and curriculum

- Write replies in the user's language unless they request another language.
- Honor an explicit worksheet language first. Otherwise preserve the source paper's or question list's language; if no source language is apparent, use the user's language. A parent can ask in English for a Chinese worksheet and English explanations. Keep student and parent output languages separate when requested.
- Localize titles, directions, labels, worked solutions, and answer-key headings consistently. Do not produce bilingual pages unless requested. Use fonts that cover the actual text and math symbols.
- Preserve the source's curriculum, notation, units, and mathematical meaning. Language does not determine country, grade equivalence, school calendar, currency, or measurement system. Do not infer a US or Chinese curriculum from English or Chinese alone.
- Preserve Chinese multiplication chants only when relevant to the requested curriculum. For an English adaptation, use the corresponding multiplication fact or explanation; do not literally translate a chant into unnatural English or silently change what is tested.

## Two input branches

| Input and intent | Branch | Read |
| --- | --- | --- |
| A complete worksheet photo/PDF; make a similar paper | `full_paper` | [Full-paper variants](references/full-paper.md) |
| A list of questions, including selected mistakes or review items | `question_list` | [Question-list input](references/question-list.md) |

Keep the demonstrated direct full-paper workflow. Do not require a full paper to pass through the question-list format first. A marked paper can still be a full-paper reference; red marks alone do not mean the user wants only incorrect questions.

For selected questions, use the list branch. A few question photos can first be transcribed into a complete question list. If the user requests targeted remediation and provides relevant evidence, also read [Mistake-focused practice](references/mistake-focus.md); this is an optional strategy, not a third input branch. A topic name alone is not a supplied question list: ask the upstream coach to select questions, or follow an explicit request to design questions from that scope.

## Inputs and boundaries

- Read the actual supplied files. For multiple pages, check order, duplicates, and missing pages. Do not claim to have seen inaccessible uploads.
- If a key condition, number, or diagram is unreadable, clarify that part while proceeding with complete questions when useful. Do not present a partial paper as complete.
- List entries need solvable question text, necessary options, and diagram information. Precise text descriptions can preserve quantities, grouping, positions, and labels; “use the diagram” alone is incomplete input.
- Use the source or explicit learning scope. Grade, curriculum, previous answers, and diagnosis are optional context; do not request a full learning archive just to make a worksheet.
- Generating practice is not mastery evidence. Do not update learning assessments, configure background jobs, or synchronize records here.
- Use the available reasoning model and document tools. Do not silently switch models or claim raster image generation when the output was authored as a document.

## Design and delivery

Let the model design the questions and layout without a fixed question-type registry. Choose available document tools internally: a local PDF layout program such as ReportLab or an HTML-to-PDF route can work. Do not ask the parent to choose rendering technologies.

Save to the requested directory or a new personal `worksheets/<date>-<topic>/` directory:

- `worksheet.pdf`: student worksheet, with writing space and no answers or diagnosis labels.
- `answer-key.pdf`: separate answers, matching question numbers, with needed reasoning, units, and acceptable alternatives.
- `previews/`: images rendered from the actual PDFs, separated into student and answer directories.
- Editable layout source and a private `answer-manifest.json`: question IDs, concepts, answers, and explanations. In the list branch, retain each output question's source IDs. Parents do not need to write JSON.

Keep source photos, personal information, and answers in the personal workspace. Avoid overwriting existing papers. This skill does not publish files or send messages; the caller handles any configured, authorized delivery or synchronization.

## Print and review

- Default to A4 portrait, approximately 12 mm margins. Honor an explicitly requested paper size, such as US Letter, and recheck pagination. Do not infer paper size from language.
- For a full paper, start around 12 pt body text, 18–20 pt title, and 1.4 line spacing. Short remedial practice can use 14 pt and more writing room. Keep meaningful figure labels around 10.5–11 pt or larger. Adjust for the actual script and reference density; allow extra pages instead of shrinking everything.
- Keep diagrams with their questions. Independently solve every item and compare object counts, relationships, units, and answers with the final figures. Check unique intended answers and choice-position patterns; update the key after reordering options.
- Reopen both PDFs to check dimensions, page counts, and text. Render every page with available tools such as Poppler, then inspect missing glyphs, clipping, overlap, and writing space. Follow the PDF skill when one is available.
- Previews must come from the final PDFs. Report missing output dependencies accurately; authored markup alone is not a verified PDF or preview.
- Reply with worksheet and answer links, question count, target scope, and checks actually completed. Keep internal analysis and solutions out of the student page.

## Validation status

The full-paper path has a reviewed GPT-6 Astra example. The list path has a six-question Chinese example covering written and diagram-based questions, plus a synthetic clock-reading remediation example. These were generation-quality checks within one conversation, not independent blind tests or evidence of learning outcomes. See [Validation record](references/validation.md). Do not extend those results to untested languages, curricula, or diagram types.
