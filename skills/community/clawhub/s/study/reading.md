# Reading Textbooks, Papers, and Dense Sources

Reading is the least efficient way to learn and the unavoidable way to acquire. The job is to spend as little time in the text as possible and as much as possible retrieving from it.

**Contents:** [Decide the Reading Mode First](#decide-the-reading-mode-first) · [The Question-First Pass](#the-question-first-pass) · [Textbook Chapters](#textbook-chapters) · [Research Papers](#research-papers) · [Primary Sources and Case Law](#primary-sources-and-case-law) · [Annotation That Earns Its Ink](#annotation-that-earns-its-ink) · [Reading Speed and Throughput](#reading-speed-and-throughput) · [Choosing and Abandoning Sources](#choosing-and-abandoning-sources) · [The Reading Backlog](#the-reading-backlog)

**Before starting a source that is already in flight**, read `## Materials` in `~/Clawic/data/study/memory.md`: it records what has been covered, what was abandoned and why. Re-adopting a source that failed in March is a common and expensive loop.

## Decide the Reading Mode First

Four modes, and reading a text in the wrong one is most wasted reading time.

| Mode | Speed | Use when | Exit artifact |
|---|---|---|---|
| Survey | Minutes per chapter | Deciding what the source contains and whether to read it | The chapter's questions, from headings |
| Reference lookup | Seconds | A specific fact or formula is missing after a failed retrieval | The answer, and a card if arbitrary |
| Study read | Slow, section by section | This is examinable material | Blank-page recall per section |
| Critical read | Slowest | Evaluating a paper's claim, writing about it | The argument reconstructed with its weaknesses |

Choose out loud before opening: "this is a survey pass, twelve minutes". Most students default to study-read on everything, which is why the reading list never finishes.

## The Question-First Pass

The one procedure that converts reading into retrieval, and the working core of SQ3R:

1. **Survey**: headings, figures, chapter summary, end-of-chapter questions. Two to five minutes.
2. **Question**: turn every heading into a question, in writing. "Osmotic regulation" → "what senses the osmolarity change, and what does it do about it?"
3. **Read one section**, looking for the answers, not from start to finish.
4. **Recite**: close the book, answer that section's question from memory, in writing.
5. **Review** at the end: all questions, from memory, then the diff against the text.

The compression: reading the summary and the questions first means the whole text is read looking for something. Reading it linearly means it is read waiting for something to feel important.

## Textbook Chapters

- **Worked examples are the most valuable part** of any problem-subject textbook and the most skipped. Read one line, predict the next, then check — a worked example read passively is a worked example wasted (`subjects.md`).
- **Read the figures before the prose.** In science texts the figure plus its caption often carries the whole argument, and the prose is elaboration.
- **The end-of-chapter questions are the syllabus's own retrieval set.** Do them before deciding the chapter is finished, not after finishing the course.
- Skip nothing on a first survey pass and skip freely on the study pass — the survey is what makes the skipping informed.
- When a section resists after two attempts, move on and mark it. A later chapter frequently explains it better than a third re-read of the same paragraph.

## Research Papers

Three passes, and most papers stop at the first:

1. **Triage** (5 min): title, abstract, figures, conclusion. Decide: relevant, background, or discard. Record the verdict in `## Materials` so it is not re-triaged next month.
2. **Content** (20-30 min): introduction, methods enough to know what was done, results with the figures, limitations. Write the paper's claim in one sentence, in your own words. If you cannot, you have not read it.
3. **Critical** (an hour or more): the design, what it cannot show, sample and power, alternatives the authors did not test, what would change the conclusion. Only for papers you must defend or attack.

- **Read the methods before believing the abstract.** The abstract states what the authors wish they had shown.
- Capture the full citation the moment you decide you will need the source again — in its row in `## Materials`, or in the thesis reading list inside `projects/<project>.md`. Hunting a half-remembered paper later costs more than the line did (`coursework.md`).
- For a literature review, read backwards through the citation graph from the most recent survey, and stop when new papers stop appearing — that saturation point is the honest end of the search.

## Primary Sources and Case Law

- Legal and historical primary sources are read for **structure and holding**, not for coverage: what did this decide, on what facts, and what is the rule it produces?
- Brief in a fixed template — facts, issue, holding, reasoning, dissent — so the fifteenth case is comparable with the second. The template is the artifact worth keeping (`artifacts/`).
- The examinable content is nearly always the *distinction* between two similar cases or sources; card the distinction, never the summary (`flashcards.md`).
- Translation and archaic language are throughput problems: budget in pages per hour measured on this specific source, not on prose.

## Annotation That Earns Its Ink

Highlighting rates low-utility for a reason: it produces zero retrievals and marks what felt important on a first read, when you were least able to judge.

Annotation that is worth the time:

- **Margin questions**, not margin summaries. "Why does this fail for n=1?" beats "important".
- **A one-line section header in your own words** written after the section is read with the book closed.
- **A symbol scheme with fewer than five symbols**: contradiction with an earlier claim, examinable, do not understand, need a card. More than five and it is never used consistently.
- **The two-colour rule** on printouts: one colour on the reading pass, a second for what turned out to matter after the recall attempt. The second colour is the useful one.

Never annotate a first read of an unfamiliar text at all. There is not enough information yet to judge importance.

## Reading Speed and Throughput

- **Measure your own pages per hour on this source once**, then plan with that number. Technical text runs several times slower than prose, and averages from anywhere else make plans wrong by a factor.
- Comprehension, not words per minute, is the constraint on examinable material. Speed-reading techniques trade the thing you are paying for.
- Sub-vocalization is not a defect to be trained out of technical reading; it is the pace at which dense material is processed.
- A chapter that takes three hours is a signal to check prerequisites, not to read harder — the missing earlier concept is usually the whole problem.
- Audio versions of textbooks are for review of already-read material, never for first exposure to anything with figures or notation.

## Choosing and Abandoning Sources

- **One primary source per course**, plus past papers. A second source is added for a specific topic that failed twice, not as a general upgrade.
- Choose the source whose **worked examples and problem sets** are best, not the one with the best prose. Problems are what the exam asks for.
- The lecturer's own notes and slides outrank a famous textbook when the lecturer writes the exam.
- **Abandon explicitly and record it**: source, date, why (`## Materials`). An abandoned source with no verdict comes back recommended in October.
- Collecting more sources is procrastination with a productive appearance (Traps). The third textbook has never been the missing piece.

## The Reading Backlog

- A backlog is a scope problem, and it is triaged like any other: rank by `examinable weight × gap`, survey-pass the rest, and say what is being skipped.
- **Never study-read a source that is not examinable** during exam season. Interesting is not the same as assessed.
- Papers and chapters read for a thesis are governed by the project's question, not by completeness; that reading list belongs to the project box (`coursework.md`).
- If the backlog exists because reading is not starting at all, it is a starting problem (`motivation.md`), and adding a reading schedule will not touch it.

**After finishing or abandoning any source**, write its row to `## Materials` — type, coverage, status, and a one-line verdict with the date. Every gap the recall pass exposed goes to `errors.md` with cause `never encoded`, and the questions generated during the question-first pass are worth keeping in `artifacts/<kebab-name>.md` with their `## Boxes` line if the source will be revisited (`memory-template.md`).
