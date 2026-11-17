# Notes That Get Reused

Most student notes are written once and never opened again. A note earns its cost only if it becomes a question, a summary produced from memory, or a lookup that is faster than the source.

**Contents:** [The Three Jobs of a Note](#the-three-jobs-of-a-note) · [Cornell, Outline, and When Each Wins](#cornell-outline-and-when-each-wins) · [The Question Bank](#the-question-bank) · [Summary Sheets](#summary-sheets) · [Formula and Fact Sheets](#formula-and-fact-sheets) · [Diagrams and Maps](#diagrams-and-maps) · [Organizing Across a Term](#organizing-across-a-term) · [Digital, Paper, and Sync](#digital-paper-and-sync) · [Notes for an Open-Book Exam](#notes-for-an-open-book-exam)

**Before building any summary or sheet**, read `## Topics` for what is already at criterion and `errors.md` for what keeps failing. A summary sheet built from the syllabus covers what you know; one built from the error log covers what you do not.

## The Three Jobs of a Note

Only three, and a note doing none of them is a transcript:

| Job | Shape | Read when |
|---|---|---|
| Retrieval cue | A question with the answer elsewhere | Every review pass |
| Compressed reconstruction | A one-pager written from memory, then corrected | Before an exam, and at each spaced review |
| Fast lookup | Formula, table, procedure, with the condition that selects it | After a failed retrieval, and in an open-book exam |

Decide which job a note is doing before writing it. The same lecture produces different notes for a viva than for an MCQ paper (SKILL.md Rule 5).

## Cornell, Outline, and When Each Wins

- **Cornell** — main column for content, left margin for questions added afterwards, bottom for a summary written from memory. Its entire value is that the margin and the summary are *retrieval* steps; a Cornell page with an empty margin is an outline with wasted space.
- **Outline** — hierarchical, fast, ideal when the material has a clean structure and the lecturer follows it. Weak when the structure is what you are trying to work out.
- **Two-column: claim / evidence** — for argumentative and humanities material, where the examinable skill is attaching support to positions.
- **Problem-solution log** — for problem subjects: the problem, the approach chosen, why that approach, and the step that broke. Far more useful than a copied solution (`subjects.md`).
- **Sketchnote or map** — only for material whose difficulty is relationships, and only drawn from memory (below).

The format matters less than whether the reconstruction step happens. Pick one and hold it for the term: format switching mid-term is a well-loved way to avoid studying.

## The Question Bank

The single most reusable artifact this domain produces, and the one most students never build.

- Every heading, every lecture, every chapter section yields questions. Write them while the content is fresh, answers **not** included on the same line.
- Store them **by topic, not by date**. A question file named after a week is unfindable in May.
- Grow it from four sources: the student's own generation, past-paper stems verbatim, end-of-chapter questions, and every item in `errors.md`.
- Mark each question with its state — unanswered, missed once, at criterion — and drill from the missed set, not the whole bank (`retrieval.md`).
- A question bank for a course that will be revisited is worth `artifacts/<kebab-name>.md` with its `## Boxes` line; rebuilding one from scratch next term is pure loss.

## Summary Sheets

A summary written with the source open is copying and rates low-utility. Written from memory, it is a retrieval and a gap map.

The procedure that makes one worth its hours:

1. Close everything. Write the topic's whole structure from memory onto one page.
2. Diff against the source in a second colour: missing, wrong, vague.
3. **Rewrite it once, clean**, from the corrected version — again without looking.
4. Compress it: one page per topic, and the compression itself forces decisions about what matters.
5. Rebuild it from scratch before the exam rather than re-reading it. The second build takes a fraction of the time and is a full retrieval.

A sheet is re-readable, so it is an artifact from the first one, not a section of `memory.md` (`memory-template.md`).

## Formula and Fact Sheets

- **Each formula carries the condition that selects it**, not just the expression. `s/√n` is useless without "population sd unknown, sample size, independence". Selection is what exams test; recall of the expression is the easy half.
- Group by *when you would reach for it*, not by chapter. A sheet ordered like the textbook is a sheet you cannot search under time.
- Include the **worked micro-example** next to anything with an easy misuse — one line, real numbers.
- If the exam supplies a formula sheet, get that exact sheet and practise with it from week one: knowing where things are on it is a timed skill, and the supplied sheet is often less complete than expected (`exams.md`).
- Build it from memory like a summary sheet, then verify every entry against the source. A formula sheet with one transcription error is worse than none.

## Diagrams and Maps

- **Drawn from memory, then corrected** — a copied diagram is a photograph of someone else's understanding.
- Mind maps rate low as a study act and high as an end-of-topic index: build one at the close of a topic to expose which branches are thin.
- For processes and pathways, redraw **from a different entry point** each time (backwards, from the exception) so the structure is not tied to one cue.
- Anatomy, circuits, maps and UI layouts are the case where image occlusion cards beat any note (`flashcards.md`).

## Organizing Across a Term

- **One folder per course, files named by topic**, never by date. "Week 6" is meaningless the moment you are looking for hypothesis testing.
- Keep exactly one canonical note per topic. Three partial versions is the standard state and it means none of them gets used — merge on sight.
- An index page per course listing topics and their file names takes five minutes and is what makes the folder usable in exam week.
- **Notes are not the record of what you know** — that is `## Topics`. Keeping "am I on track" inside a note file is how it stops being answerable.
- Where notes live outside this system entirely (a note app, a shared vault), record the location in `## Materials` and treat the app as the source of truth; general note capture and vault mechanics belong to the `notes` skill.

## Digital, Paper, and Sync

- Digital wins for search, reorganization and reuse across terms; paper wins for notation, diagrams, and for people who transcribe when they type.
- **Handwritten notes photographed into the same folder** is the standard hybrid and costs a minute a page.
- Back up on a cadence, and put the cadence in `## Due`. A term of notes lost in week 11 is unrecoverable, and it happens at a rate that justifies the two-minute setup.
- Sync conflicts and duplicate files are a vault problem, not a study problem — one canonical location per course, chosen once.
- Anything pasted from a portal, a shared drive link that grants access, or a credential goes nowhere near these files (`memory-template.md`, Secrets).

## Notes for an Open-Book Exam

An open-book exam is a **speed test against an index**, not a knowledge-free exercise. The notes are the deliverable and they are built to be searched under pressure:

- **An index or table of contents on page one**, with page numbers. Without it, permitted notes cost more time than they save.
- Ordered by the shape of the exam's questions, not by the syllabus: the question types are the headings.
- **Worked examples, not theory** — under time, the fastest route is pattern-matching to a solved instance.
- Tabs, colour-coding by topic, and a fixed physical layout you have rehearsed.
- **Practise with the exact permitted materials, timed**, at least twice. The first attempt reveals that the notes are in the wrong order, and that discovery is worthless on exam day.
- Check the rules precisely: annotated textbook, own notes only, printed or handwritten, page limit. Getting this wrong is an academic-integrity incident, not an inconvenience (`coursework.md`).

**When a sheet, a question bank, an index or a map is finished**, write it to `artifacts/<kebab-name>.md` with a line saying when to read it, and add its `## Boxes` line in `memory.md` in the same turn. Every gap the from-memory build exposed goes to `errors.md`, and any source adopted or abandoned along the way updates `## Materials` (`memory-template.md`).
