# Form: technical-blog

**Register:** `technical-blog`

A form file supplies slots. Only the voice may fill them. Every quoted phrase in this file is under Tells, and every one of them is a phrase to avoid.

A post whose subject is code, architecture, or a system, written for someone who will act on it. A genre column rather than a rung on the formality spine: what it relaxes has nothing to do with how formal the writing is and everything to do with the fact that technical vocabulary carries real meaning here.

The incident-writeup band below is the public one: narrative, for readers outside the organization, with the internal detail removed. `forms/incident-report.md` is the internal record of the same event, the one carrying severity, owners, and action items.

## Slots

- **Title.** The thing built, broken, or measured.
- **Opening.** The problem, in terms a reader can recognize from their own system. Not the solution, and not the history of the field.
- **Context.** Versions, scale, constraints. The reader needs to know whether this applies to them before they read how it worked.
- **Body.** The approach, then the evidence: code, numbers, traces. Code blocks are never edited by any pass in this skill, in any mode.
- **Result.** What actually happened, including what did not work. A post with no failed attempt in it is usually a post with the failed attempts edited out.
- **Close.** What a reader should take away and where the approach stops applying.

## Bands

| Purpose | Band |
|---|---|
| A note on one technique | 600 to 1,200 words |
| A full writeup | 1,200 to 3,000 words |
| An incident writeup | as long as the timeline, and the timeline is not padding |

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "In this article, we'll explore."
- "This is a game-changer for developers."
- "It's important to understand that" before a sentence that stands alone.
- A benchmark with no methodology, no hardware, and no error bars.
- "Blazingly fast" and every unquantified performance adjective.
- A bulleted list of pros and cons where every entry is one noun phrase.
- Numbered steps that explain why in the middle of the execution. The reasoning goes above the steps, once.

## What the mechanical layer sees here

Two relaxations, both about vocabulary meaning what it says. The three vocabulary tiers run in partial mode, which drops the words that carry real technical meaning (the list is `technical_exempt` in `lexicon.json`) while still flagging the ones that never do. And hedging is relaxed to two stacked hedges, because a qualified claim about a system is accuracy rather than throat-clearing.

Curly quotes are relaxed rather than skipped, at four, because a technical post is full of plain-text contexts where a curly quote is a copy-paste artifact rather than typography.

Diff-anchored writing is skipped here, since a post about a change is legitimately anchored to the change.

Everything else runs at full strength, including significance inflation and promotional language. A technical post is the form where an inflated claim costs the most, because the reader can check it.
