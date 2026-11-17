# Repeat Editions of the Same Stream

Scope: the same source summarized again — a weekly project digest, a monthly report roundup, a channel recap, a running summary of a long book being read in parts, a series of releases. The product of edition two is the delta, not a second full summary.

Sourcing and filtering external feeds is the `digest` skill; this covers what changes when the reader has already read last time's summary.

**Before writing any edition**, read `## Sources` in `~/Clawic/data/summarizer/memory.md` (or `sources.md` per the `## Boxes` index) for the last edition's cut-off, and open the previous edition at `editions/<stream>-<year>.md` when the `## Boxes` index names it. Writing an edition without reading the last one produces the failure that kills digests: repetition.

**Contents:** [The Delta Is the Product](#the-delta-is-the-product) · [Cut-Offs](#cut-offs) · [Deduplicating Against Last Time](#deduplicating-against-last-time) · [Carry-Forward Items](#carry-forward-items) · [The Quiet Period](#the-quiet-period) · [Stable Structure](#stable-structure) · [Cadence](#cadence) · [Corrections](#corrections) · [Output Shape](#output-shape)

## The Delta Is the Product

A reader of edition N has read edition N−1. Everything they already know is padding, and padding is why recurring summaries get unsubscribed from.

| Content | Edition 1 | Edition N |
|---|---|---|
| Background and context | Included | Omitted; one clause of orientation at most |
| Ongoing item, unchanged | Included | One line under "unchanged"; from the second quiet edition it moves to the "still open" list with its age and stays there until it resolves or hits the five-edition cut (Ageing rule) |
| Ongoing item, changed | Included | The change, with the previous state in a clause: "slipped from 14 May to 4 June" |
| New item | — | Full treatment, marked new |
| Resolved item | — | Stated once, with the outcome, then never again |
| Item that disappeared | — | Named as dropped; silent disappearance is the failure readers notice |

State changes are written as `was → now` with both values. "The launch date is 4 June" tells a returning reader nothing; "launch slipped 14 May → 4 June" is the entire message.

## Cut-Offs

Every edition declares `covers <start> to <end>`, and the next edition starts exactly where this one ended.

- **Gaps lose content silently.** If an edition was skipped, the next one covers the whole interval and says so.
- **Overlaps produce duplicates** that make a reader distrust the series.
- Store the end timestamp with the edition (below); reconstructing it later from the content is guesswork.
- For a live stream (a channel, an active thread), the cut-off is a timestamp, not a date.

## Deduplicating Against Last Time

1. **Load the previous edition** before reading the new material.
2. **Match by entity and subject, not by wording** — the same issue described differently is the same issue.
3. **For each candidate item, classify**: new, changed, unchanged, resolved, dropped.
4. **Unchanged items are cut from the body by default.** They keep their one line in the "still open" list with their age — "still blocked, now 3 weeks" — and return to the body only when the persistence itself becomes the news.
5. **Watch for the re-announcement**: sources routinely restate an old fact as though it were new, especially press releases and status updates. Check the date of the underlying event, not the date of the message (`news.md`).

## Carry-Forward Items

The thing a recurring summary does that a one-off cannot: track an item across editions.

- **Open items carry their age.** "Awaiting legal — 3 weeks" is a different message from "awaiting legal", and the age is the escalation signal.
- **Deadlines approach.** An item with a date gets more prominent as the date nears; the edition before the deadline says so explicitly.
- **Ageing rule** (the single threshold for a quiet item): at two consecutive editions with no change it leaves the body for a compact "still open" list with its age — it is never deleted at this point, because a silent disappearance is the failure readers notice. At five it is either escalated or explicitly closed as abandoned, and the closure ships under "Dropped" with its date. A perpetual open list nobody prunes is how a digest becomes unreadable.
- **Resolved items are stated once and retired.** Repeating a resolution is the second most common padding after background.

## The Quiet Period

A week where nothing happened is the hardest edition to write and the one most often padded.

- **Say it.** "Nothing changed this week; three items remain open, oldest 19 days." That is a complete and useful edition.
- **Never manufacture content** by lowering the significance bar, restating background, or reporting activity that is not change ("14 commits, all internal").
- **Consider skipping** and saying the cadence will resume — but only if the `## Due` row is updated so the next edition covers the double interval.
- A quiet edition is also a signal in itself: two silent weeks on an urgent project is the story.

## Stable Structure

A series is read as a series; the shape must not move.

- **Same sections, same order, every edition** — even when a section is empty ("Decisions: none this week"). A disappearing section reads as an omission.
- **Same length band**, so a reader learns what to budget.
- **Same names for the same things** — pull them from `glossary.md`; a project renamed between editions reads as a new project.
- Store the agreed shape in `templates/<stream>.md` the first time it survives a round of feedback, and follow it thereafter rather than re-deriving it.

## Cadence

- Every recurring stream has a row in the `## Due` table of `memory.md`: what, every how often, last run, next due. At session start, an overdue edition is stated in one line — a statement, not a question.
- **Match the cadence to the change rate, not to the calendar.** A project with a decision a month produces a monthly digest; a weekly cadence over it produces eleven quiet editions a quarter and trains the reader to skip.
- **Cadence changes are decisions**: record the new period in `config.yaml` under the cadence preference area and update the `## Due` row in the same turn.

## Corrections

When a previous edition was wrong, the correction leads the next one.

- Name the edition, the claim, the correct version, and the consequence: "The 4 June date in last week's edition was the internal target, not the announced date; the announced date remains 14 May."
- Correct once, at the top, then continue normally.
- Every correction also goes to `## Corrections` in `memory.md` — that box is what stops the same mistake recurring across a year of editions, and it is the highest-value box this skill has.

## Output Shape

```
<Stream> — edition <N>, covers <start> to <end>. <"Nothing changed" if true.>

Corrections: <only if the previous edition was wrong>
New: <item> — <one line>
Changed: <item> — <was → now>
Still open: <item> — <age>, awaiting <who>
Resolved: <item> — <outcome>
Dropped: <item> — no activity since <date>
Next: <deadline or scheduled event inside the coming period>
```

**After every edition**, append it to `~/Clawic/data/summarizer/editions/<stream>-<year>.md` — the append-only log of the series, cut by year — and record the new cut-off in `## Sources` in `memory.md`; update the stream's row in `## Due` with the run date and the next due date; store the shape in `templates/<stream>.md` once it is agreed; and log any correction in `## Corrections`. Formats and thresholds: `memory-template.md`.
