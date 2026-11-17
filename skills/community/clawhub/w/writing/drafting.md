# Drafting — From Nothing to a Complete Zero Draft

Scope: producing text that reaches its last line. Making it good is a different pass and a different file (`revision.md`). Mixing the two is the single most common reason a piece never finishes.

**Before drafting**, read `## Voice`, `## Formats` and `## Pieces` in `~/Clawic/data/writing/memory.md` — the last one tells you whether this piece already has an agreed outline, a deadline, or a word target you are about to contradict.

## The Rule That Makes Drafting Work

Generation and criticism use the same attention. Run them together and you get a perfect opening paragraph attached to nothing. The zero draft is finished when it has a last line, not when it is good — and a bad complete draft is worth more than an excellent half, because a complete draft can be measured, cut and reordered while a half cannot.

Signal you are editing while drafting: you have rewritten the opening more than twice and the piece has no ending yet. Fix: write `[TK]` and move on. Never stop to look something up mid-draft — leave the marker.

## Deciding the Shape Before the First Word

Three lines, always, whatever the format. Under two minutes.

1. **One reader.** Not "founders" — one person who will read this and what they currently believe. Every ambiguity in the draft is resolved by asking what that person needs.
2. **One thing that must happen after reading.** A decision, a reply, a changed mind, a click. If you cannot name it, the piece has no ending, and it will trail off (`structure.md`).
3. **Three to five moves, in order.** Not headings — claims. "Their current setup costs more than they think" is a move; "Background" is not.

If the three lines do not come, the problem is that you do not yet know what you think. Fifteen minutes of notes beats two hours of drafting into fog.

## Outline First or Draft First

| The piece exists to... | Method | Why |
|---|---|---|
| Transmit a conclusion someone must act on (memo, proposal, op-ed, email) | Outline first, and get the outline agreed if a human is waiting on it | The reader must be able to stop after paragraph one and still act correctly |
| Reach a conclusion the writer does not have yet (essay, personal writing, an argument still forming) | Discovery draft, then reverse-outline what you actually wrote | An outline pre-decides the conclusion, and the interesting turn is the one you did not plan |
| Follow a format with a fixed skeleton (release notes, status update, report, review) | Fill the skeleton | The shape is the convention; inventing one costs the reader |
| Anything else | Outline first — it is cheaper to be wrong in five bullets than in 800 words | — |

Reverse outlining: after a discovery draft, write one sentence per paragraph stating what that paragraph *does*. The result is the real outline. Fix it there, then restructure (`structure.md`).

## Beating the Blank Page

Ordered by how reliably they work, most reliable first:

1. **Start in the middle.** Draft the section you already know — usually the third move. Openings are the hardest paragraph in any piece and the worst place to begin.
2. **Write the ending first.** If you know what must be true for the reader at the end, the middle is navigation toward a known point.
3. **Say it out loud and transcribe.** Speech bypasses the critic. Spoken drafts run long and loose, but a loose complete draft is exactly what the cut pass wants.
4. **Write the email version.** Explain the whole thing to one person in 150 words as if they had asked. That email is the piece's spine; expand it.
5. **Write the bad version deliberately.** Give yourself permission to write the cliché opening. It occupies the slot so the real opening can arrive later.
6. **Lower the unit.** Not "write the post" but "write the second subhead's first sentence".

The one that does not work: waiting for the right first sentence. Openings are written last in most finished pieces (`structure.md`).

## Timeboxing and Velocity

- Draft in blocks with a stated end, not to a word count — a word count encourages padding, a timebox encourages finishing.
- Useful planning figure: prose generation runs far slower than typing, and a realistic sustained rate for original prose is a few hundred words per focused hour once thinking is included. Estimate a first draft from the format's budget in `SKILL.md`, then double it for anything requiring research.
- Stop mid-sentence, not at a section end. Restarting is nearly free when the next words are obvious and expensive when the next decision is structural.
- One draft, one sitting, for anything under 800 words. Splitting a short piece across days costs a re-read and a voice reset each time.

## Deadline Arithmetic

Work backwards from the due date in `## Pieces`, in this order:

```
send/publish date
 − review or approval time (ask; never assume same-day)
 − final proof pass (never on the same day as the last edit; `revision.md`)
 − revision passes (roughly the drafting time again, for anything argued)
 = the date the zero draft must exist
```

A schedule with no slack for the review step is the usual cause of a piece shipping unproofed. When the arithmetic does not fit, cut scope from the piece — a shorter piece delivered proofed beats a longer one delivered raw.

## Placeholders and Research Debt

- `[TK]` for a missing fact, `[CITE]` for a source to find, `[?]` for a claim you are not sure survives. All three are greppable and none of them are English words that could survive into a published draft by accident.
- Never invent a statistic, a quotation, a name or a date to keep the draft moving. Write `[TK number of X]` — a placeholder costs one search; a fabricated figure costs the piece's credibility and cannot be un-published.
- Before the piece leaves the drafting stage, search for every marker. A `[TK]` that ships is a career-grade embarrassment and takes two seconds to prevent.

## Reusing What Already Exists

Check before writing anything from scratch:

- `artifacts/` for a template that covers this format — cold emails, intros, declines, bios and boilerplate are written once and reused forever.
- `pieces/<year>.md` for whether this angle has already been published. Re-covering your own ground unknowingly is a real cost for anyone with a body of work.
- The user's own previous piece in the same series, if `~/Clawic/data/projects/<project>.md` names it.

**When a piece is commissioned, started, or given a deadline**, write its row to `## Pieces` in `memory.md` — piece, format, who for, word target, due date, status. **When a first draft produces a template, outline or standing text that will be reused**, save it to `artifacts/<kebab-name>.md` with its `## Boxes` line, in the same turn (`memory-template.md`). An outline that only exists in the chat gets rebuilt from scratch next month.
