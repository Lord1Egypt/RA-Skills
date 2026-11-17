# Validation record

Date: 2026-10-01. File-generation quality, input recognition, and learning outcomes are separate claims.

## Full-paper photo branch

A GPT-6 Astra session produced a Chinese variant paper and answer key from a complete worksheet photo, each one A4 page. The rendered pages and solutions were reviewed. Findings included concentrated answer positions and some small figure labels. This demonstrated route remains available without requiring conversion to the list format.

## General question-list branch

Six representative questions were transcribed from the reference paper into text JSON and readable Markdown. Inputs included stems, choices, concepts, and essential diagram descriptions, without learner identity, incorrect answers, or diagnosis.

Coverage included equal groups, deriving multiplication facts, adding/removing a group, station intervals, addition versus multiplication, and equal-length jumps. New questions retained all six source mappings. The layout program read text JSON without opening the original photo.

Observed checks:

- Student paper and answers each occupied one A4 page (595.28 × 841.89 pt), with approximately 12 pt body and 11 pt figure labels.
- Object counts, route ordering, jump counts, and solutions agreed.
- The three multiple-choice items each had one correct answer, in positions 2, 3, and 1.
- Initial preview inspection found a missing Unicode minus glyph in the chosen Chinese font. It was replaced and both PDFs were rendered again. Text extraction alone had not exposed the issue.
- Transcription and generation took place in the same conversation, not an independent blind test. This example exercised `variants`; `typeset` did not receive a separate end-to-end check.

For this batch, complete text descriptions were sufficient to produce diagram-based printable variants. This does not establish that brief descriptions can reconstruct arbitrary complex geometry. Real source files and generated samples remain in the personal workspace.

## Optional error-focused strategy

A separate synthetic example treated a half-hour time written as a whole hour. A five-question paper covered reading clocks, contrasting whole/half hours, hour-hand position, drawing hands, and the 12-to-1 boundary. Student and answer PDFs each occupied one A4 page, with figures and previews checked.

The first answer field was changed from explicit hour/minute blanks to free writing so the form would not cue the omitted minutes. Causes remained hypotheses and no real learner records were updated.

Real-photo mistake extraction, mixed-error sets, and learning outcomes still need further evidence.

## Language coverage

The reviewed PDF examples above are Chinese. The public skill instructions and examples are now English, with explicit output-language selection and curriculum boundaries. Do not represent this documentation change as an English-PDF end-to-end test. English and Chinese rendering-helper checks are recorded separately in the repository tests.
