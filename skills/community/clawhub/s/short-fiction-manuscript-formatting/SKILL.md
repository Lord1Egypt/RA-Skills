---
name: short-fiction-manuscript
description: Format one short story in Courier New, modern rules.
version: 0.2.0
author: Grok Build
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Writing, ShortFiction, Courier, Shunn]
    category: writing
---

# Short Fiction Manuscript Skill

Formats **one short story** as a submission `.docx` in Courier New 12 pt. Spacing and emphasis stay with Shunn's modern short-fiction rules: one space between sentences, italics, curly quotes. A dash is two hyphens (`--`) with no spaces, because in Courier an em dash is easy to mistake for a hyphen. One title, one byline, scene breaks marked `#`. It does not format novels, and it does not add the second space used in Shunn Classic. It does not copy Shunn's guide. The definitive short-fiction article is [format.ms/story](https://format.ms/story) (mirror: [shunn.net/format/story](https://www.shunn.net/format/story/)), last updated 13 July 2026. If a market explicitly requires Times New Roman, stop and say so. Otherwise do not swap this font.

The guide's own text is CC BY-NC-ND 4.0 and must not be reproduced in a submission or in this skill's output. The emitter refuses a paragraph beginning with `Copyright` rather than silently reformatting it, and `--self-test` checks that refusal. Do not paste the guide's text or its license line into a manuscript.

## When to Use

- The user wants a short story or flash piece laid out for submission.
- They ask for Shunn's **short story** / modern manuscript format, or a tidy `.docx` of one story.
- They already have the prose and need the contact block, a word count rounded to the nearest hundred, the title, the byline, the header, and scene breaks fixed.

Don't use for:

- **Novels.** No chapter titles, no "Chapter 1" openers, no parts, no prologue or epilogue as a book division, no per-chapter restart a third of the way down a new page. Shunn's novel notes are a different spec: <https://www.shunn.net/format/novels/>. Stop and say this skill does not implement that.
- A novella that is really a book with chapters. A single continuous story still uses this layout; the moment it grows chapters, stop.
- **Shunn Classic**, meaning two spaces after a period. Courier New is already the font here; the extra space is the part to refuse. Differences: `references/classic-vs-modern.md`.
- Screenplays, poetry, academic papers, or a typeset book look.
- Pasting or reformatting Shunn's article. It is CC BY-NC-ND.

## Prerequisites

- Python 3.9+ standard library only. No pip packages, no API keys, no network.
- The story text and, unless the writer is deliberately omitting them, legal name, postal address, phone, and email. A writing affiliation is optional. Byline may differ from the legal name.

## How to Run

```bash
python3 ${HERMES_SKILL_DIR}/scripts/format_manuscript.py manuscript.md -o Story.docx
```

Install: copy this folder to `~/.hermes/skills/writing/short-fiction-manuscript/`. It loads on the next Hermes session, not the current one.

`--classic` exits 2 and writes nothing. A chapter heading also exits 2 and writes nothing. `--self-test` checks both refusals. Input shape: `templates/example-story.md`.

## Quick Reference

| Job | Rule |
|---|---|
| Scope | One short story. Not a novel. |
| Page | Plain white, no decoration. 1 inch margins on all four sides. |
| Type | Courier New, 12 pt, black. Not Times New Roman. Not sans-serif. Not bold display type. |
| Story | Double-spaced, left aligned, ragged right. First line indent 0.5 inch. No blank line between paragraphs. |
| Sentences | One space. Italics for emphasis. Dash as `--` with no spaces. Curly quotes. |
| Scene break | A centered `#` on its own line. Never a blank line, and never a chapter title. |
| Page 1 | Contact upper left. `N words` upper right, N rounded to the nearest 100. No header, no SSN, no copyright line. |
| Title | The story title only, centered, about 40% of the way down the text area of page 1 (a third to halfway down). Byline centered under it as `by Name`. |
| Later pages | Flush-right header `Surname / Keyword / 2`. Surname comes from the byline. Not on page 1. |
| End | Optional centered `END`. Do not add a copyright notice. |

Full checklist: `references/modern-rules.md`.

## Procedure

1. Confirm the job is one short story. Completion: if the source has chapters, parts, a prologue, or an epilogue division, stop without running the script and say novel format is out of scope.
2. If the user supplied market guidelines, extract any format rules. Completion: a one-line decision, either "short fiction, Courier New, one space, no conflicts" or a listed override. If they require two spaces, Shunn Classic, Times New Roman, or novel chapters, stop.
3. Collect legal name, address, phone, email, optional affiliation, byline, title, and the story. Omit a contact field only when the writer refuses it. Completion: every retained field is the writer's, not a placeholder from the template or from Shunn's sample.
4. Write `manuscript.md` in the shape of `templates/example-story.md`. Mark scene breaks as a line containing only `#`. Mark emphasis with `*asterisks*`. Do not restyle the prose and do not insert chapter headings. Completion: the file has closing front matter and at least one story paragraph.
5. Run the emitter and read stdout. Completion: the process exits 0 and stdout contains `VERIFY PASS`, the rounded word-count line, and the header pattern.
6. Confirm the keyword. The default for a long title is the last significant word (Shunn's own sample uses `Format`). Override with `header_keyword` when a clearer one or two words exist, then re-run. Completion: the header in stdout is the one that should be submitted.
7. Give the writer the `.docx` plus the rounded count and header string. Completion: the reply calls it a short-fiction manuscript, not a novel and not Classic, and does not tell them to add a copyright line.

Hand-building the `.docx` is a fallback only when Python cannot run. Follow `references/modern-rules.md` item by item and say the verifier did not run.

## Duplicate skills to ignore

Two older skills describe the same job and disagree with this one. They are superseded; do not follow them.

- `manuscript-formatting` (top level). It claims "no running headers" and "round to the nearest thousand" — both wrong. Shunn wants a flush-right running header on page 2 onward, and the word count rounded to the nearest hundred. It also builds files with python-docx and textutil, which is a fallback path, not the preferred one.
- `creative/manuscript-formatting-short`. It defaults the word count to plain `N words`. Shunn's own specimen reads `about 1,500 words`.

When either is loaded by name, use the rules here instead and say the difference. If the writer asks for a `.doc` rather than a `.docx`, build it with python-docx or convert the `.docx` with `textutil`, and say the emitter's verifier did not run on that conversion.

## Pitfalls

- This is the short-story spec at format.ms/story. Do not invent novel machinery (chapter half-title pages, a new "one third down" for every chapter, book/part divisions) when the user says "manuscript."
- Shunn's printed modern specimen is Times New Roman. This skill uses Courier New anyway, because that is the writer's preference. Shunn still allows Courier New. Do not "correct" the file back to Times New Roman unless the writer asks.
- Courier does not mean Classic. Classic is the second space after sentences. This skill keeps one space.
- In Courier, write a dash as `--` with no spaces around it. Do not insert a real em dash; it looks like a hyphen in a monospaced font.
- Two spaces, underlining, full justification, sans-serif fonts, bold or enlarged titles, and a header on page 1 are wrong. The script collapses double spaces and turns underline markup into italics.
- A blank line is not a scene break. The source must use a lone `#`. Extra blank lines are collapsed, not turned into `#`.
- Header surname is the **byline** surname, not the legal surname, when they differ. `header_surname` overrides the guess.
- Straight quotes and a leading apostrophe in `'em`, `'tis`, `'cause`, or `'90s` are easy to get wrong. Don't "fix" `’em` back to an opening quote.
- Do not put a Social Security number, tax ID, or copyright notice on the manuscript.
- Word count is the story body only, rounded to the nearest 100 (half up). There is no novel-length or nearest-500 mode.
- The guide says to round to the nearest 500 only "if you're edging into novella territory." This skill has no novella mode: a long single story is still one short story and still rounds to the nearest 100. Do not apply the 500 step to a short story.
- Title sits about 40% of the way down the text area, once. Do not repeat that treatment per chapter.
- `END` is optional. The script adds it only when `include_end: true` or the source already has a lone `END` line.
- `.docx` only. Do not also make a PDF unless that market asks.
- Contact block text (name, address, email) does not go through `smarten`. A straight apostrophe in the address (e.g., "Writer's Lane") will fail verification. Use curly quotes in front matter or avoid apostrophes in contact fields.
- The word count is placed via a right tab stop at the margin, not paragraph right-alignment. The paragraph's `w:jc` is "left"; the word count appears at the right because of `<w:tab/>` before it. Do not "fix" the paragraph alignment to "right" — that would left-align the contact block.

## Verification

Run:

```bash
python3 ${HERMES_SKILL_DIR}/scripts/format_manuscript.py --self-test
```

Completion: stdout ends with `SELF-TEST PASS`.

On a real story, completion is all of:

- Exit code 0 and the line `VERIFY PASS`.
- Stdout `word_count_line` matches `N words` with N rounded to the nearest 100.
- Stdout `header` is `Surname / Keyword / #` and was checked against the byline.
- The `.docx` is Courier New, one story: page 1 has contact and the story title and no running header; page 2's header is flush right; there are no chapter openings.

If verification fails, fix the input and re-run. Do not hand the writer a file that failed.
