# Shapes, Lengths, and Channels

Scope: what the summary looks like once you know what it says. Length comes from the Length Ladder in `SKILL.md`; this file covers the shape, the channel's hard limits, and the header that makes a summary usable later.

**Before producing a shape for a recurring job**, check `templates/` via the `## Boxes` index in `~/Clawic/data/summarizer/memory.md` — an approved shape exists for anything the user has asked for twice, and re-deriving it breaks the series.

**Contents:** [Choosing a Shape](#choosing-a-shape) · [Bullets vs Prose](#bullets-vs-prose) · [The Shapes](#the-shapes) · [The Header](#the-header) · [The Omission Line](#the-omission-line) · [Channel Limits](#channel-limits) · [Markers and Formatting](#markers-and-formatting) · [Hitting a Word Count](#hitting-a-word-count) · [Templates](#templates)

## Choosing a Shape

| Reader will | Shape |
|---|---|
| Decide something | Conclusion-first block: answer, three supports, the ask (`audience.md`) |
| Scan for their item | Bulleted list, one line each, front-loaded keywords |
| Act in sequence | Numbered steps with owner and date |
| Compare things | Table, with the decision dimensions as rows |
| Understand a chain of reasoning | Prose paragraph — bullets cannot carry "because" |
| File it and return in six months | Structured sections with a header block |
| Forward it to someone else | Self-contained: title, date, source, and no unresolved references |
| Read it aloud or hear it | Prose, short sentences, no nested structure, spelled-out symbols |
| Anything else | `default_length` at conclusion-first, with a header |

## Bullets vs Prose

The real distinction, and the one most often decided by habit:

- **Bullets are for parallel, independent items.** Five findings, five action items, five options. Parallel structure is what makes a list scannable: same grammatical shape, same level of abstraction, sorted by consequence.
- **Prose is for dependent claims.** "X happened because Y, despite Z, and only if W holds" cannot be bulleted without destroying the logical connectives, which were the finding.
- **The tell**: if your bullets need "however", "therefore", or "which means" to make sense in sequence, the content is prose and the list is hiding an argument.
- **Nesting past one level** is a structural failure — a sub-sub-bullet means the outline is the content and the summary has not been written.
- **Never mix**: a paragraph followed by bullets restating the same thing is the most common padding shape in this domain.

## The Shapes

**Conclusion-first block** — the default for anything a reader acts on.
```
<The answer, one sentence.>
- <support with number>
- <support with number>
- <support with number>
<The ask, with a date. Or: "No decision needed.">
```

**Findings list** — for a document with independent points.
```
<Source, date, one-line scope.>
- <Finding stated as an outcome, not a topic>
- <Finding>
Omitted: <what was cut>
```

**Structured sections** — for anything filed and re-read. Fixed slots make a series comparable; the slots differ by genre and are given in each genre file.

**Q&A** — for explainers and onboarding: questions in the reader's words, answers in two sentences. Effective where the reader's questions are predictable and the source's structure is not.

**Timeline** — for incidents, negotiations, and any story where causality is the content: absolute timestamps, one event per line, no interpretation between events.

**Table** — for comparisons and for anything with the same fields repeated. Rows are the decision dimensions, columns are the things compared (`multi-source.md`).

**Abstract** — fixed slots, ~250 words, for papers and formal reports (`research.md`).

**One-liner** — headline or TLDR level: the single claim, no verb required for a headline, one sentence for a TLDR. Front-load the distinguishing word: a list of 40 one-liners is scanned by first words.

## The Header

Three or four elements that cost fifteen words and make the summary usable a month later. Every stored summary has one; a chat reply can drop it when the source is right there in the conversation.

| Element | Why |
|---|---|
| Source identity and date | Which document, which version, published when |
| Coverage | Full document, or a cut-off / page range / timestamp range |
| Level and actual length | So the reader knows what was possible at that size |
| Assumptions made | Audience or purpose you inferred, so the reader can correct in one word |

`Q2 report (published 2026-07-14) — full document, standard (210 words), written for an operator.`

## The Omission Line

Governed by `omission_note`; the most valuable line in most summaries because it is the only one that tells the reader whether to open the source.

- **Name what was cut, not that cutting happened.** "Omitted: the methodology and the two dissenting cost estimates" works; "some details were omitted" is noise.
- **Material means decision-changing**: a reader acting on the summary alone would choose differently. Under `when-material`, only these ship.
- **Always ship it** when the cut removed a dissent, a limitation, a cost, a deadline, or a risk — even under `never`, because those are not omissions, they are the summary being wrong.
- **One line, at the end**, never distributed as hedges through the text.

## Channel Limits

`delivery_channel` sets these. Exceeding a channel's limit is not a style problem — the text gets truncated or silently reformatted.

| Channel | Hard constraints | Consequence for the shape |
|---|---|---|
| Slack / Teams | Long messages collapse behind "show more"; tables render poorly or not at all | Put the answer above the fold; use bold labels and line breaks instead of tables |
| Email | The preview line is the first ~90 characters and decides whether it is opened | First sentence is the summary of the summary; no greeting above it |
| Chat reply | No header needed; the source is in the conversation | Answer only; skip the metadata block |
| Markdown / docs | Full structure available | Headings, tables, and nesting are all fine |
| Plaintext | No bold, no tables, no links | Labels in CAPS, indentation for structure, URLs on their own line |
| Issue tracker | Markdown plus a title field | The title is a one-liner and does its own work |
| Slide | ~6 lines, ~8 words per line | One claim per slide; the rest goes to speaker notes |
| Social post | Fixed character count | Write to the count, not to a length band |
| Voice / audio | No visual structure at all | Prose, short sentences, numbers rounded and spoken, no symbols |
| Anything else | Assume markdown, no truncation | Use the ladder default |

## Markers and Formatting

- `markers: plain` (default) — bare labels: `Decided`, `Open`, `Omitted`. Survives every channel.
- `markers: emoji` — the same labels with a leading emoji. Costs nothing on Slack, breaks in plaintext and in some document pipelines.
- `markers: none` — no labels, structure carried by paragraph breaks alone. Use for prose deliverables and voice.
- **Bold is for labels and for the one number that matters**, not for emphasis scattered through sentences; bold everywhere is bold nowhere.
- **Never bold or capitalize a whole sentence** to signal importance — reorder instead; importance is expressed by position.

## Hitting a Word Count

When a count is hard (a channel limit, an abstract limit, a form field):

1. **Cut branches first** (SKILL.md Rule 2) until the point count fits `target ÷ 25`.
2. **Then cut the connective tissue**: "it is worth noting that", "in order to", "the fact that". This is the only genuinely free compression and it typically recovers 10-15% of a first draft.
3. **Then cut adjectives and adverbs**, which carry almost no claim.
4. **Never cut**: negations, hedges, quantifiers, units, attributions, dates. If the count cannot be met without cutting one of these, the count is wrong for this content — say so and give the shortest honest version.
5. **Count before delivering.** "Under 100 words" delivered at 140 is a failed instruction, and it is the most common one.

## Templates

- A shape becomes a template the second time the user asks for it, or the first time they edit yours into a form they approve.
- **Templates are stored, not remembered**: `~/Clawic/data/summarizer/templates/<name>.md`, with a one-line note of when to use it at the top.
- A template records the slots and their order, never sample content that could be mistaken for real data.
- When a template exists for a job, follow it exactly; propose changes rather than making them silently, because a series' value comes from being comparable across editions (`recurring.md`).

**After a shape is approved or reused**, write it to `~/Clawic/data/summarizer/templates/<name>.md` and add its `## Boxes` line with a read condition in the same turn; record a channel or formatting preference the user states (marker style, bullet punctuation, heading depth) as a key in `config.yaml` under the conventions area; and if the user supplies a house style guide as a long text, save it to `~/Clawic/data/summarizer/style-<name>.md` and point `style_file` at it. Formats and thresholds: `memory-template.md`.
