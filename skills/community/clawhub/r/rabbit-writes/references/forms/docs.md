# Form: docs

**Register:** `docs`

A form file supplies slots. Only the voice may fill them. Every quoted phrase in this file is under Tells, and every one of them is a phrase to avoid.

Reference and instruction: a guide, a how-to, an API page, a runbook. A genre column rather than a rung on the formality spine. The reader is not reading, they are looking something up while blocked on it, and every relaxation this register carries follows from that.

A file named `README.md` is not this form. It belongs to the `rabbit-readme-improver` skill, which holds the measured section conventions this one does not. Hand it over rather than treating it as a docs page. A file named `CLAUDE.md` or `AGENTS.md` is the same case: it belongs to the `rabbit-claude-md` skill, which holds the altitude and disposition rules this form does not.

## Slots

- **Title.** The task or the thing, named the way a reader would search for it.
- **What this is for.** One or two sentences. A reader who landed here from a search needs to know within seconds whether this is the right page.
- **Prerequisites.** Versions, permissions, prior steps. Before the steps, never inside them.
- **Steps or reference body.** Ordered if sequence matters, unordered if it does not, and the difference is not decorative. Reasoning does not go inside a step: it goes above the list, once.
- **Verification.** How the reader knows it worked. The slot most often missing, and its absence is what turns a doc into a set of instructions nobody can check.
- **What to do when it fails.** Optional, and worth more than most of the prose above it.

## Bands

| Purpose | Band |
|---|---|
| A single task | one screen, which is roughly 300 words plus the code |
| A guide | as long as the task, split by step |
| A reference page | no cap, and its structure is the API's structure |

Paragraph length is not a useful measure here. A parameter list is one paragraph to the engine, so the paragraph-length number on a list-heavy page is measuring list length rather than prose. Measure the non-list blocks separately before treating that number as a defect.

## Tells

Phrases and shapes named here are the ones to avoid. Nothing in this file is a phrase to use.

- "Simply run the following command." Nothing a reader is blocked on is simple.
- "Just" as a modifier on any instruction.
- "As you can see" and "Obviously."
- "This comprehensive guide will walk you through everything you need to know."
- A concept section explaining background the reader did not ask for, above the steps they came for.
- A step that explains why in the middle of telling the reader what to type.
- An example with a placeholder that was never filled in. The engine reports those at P0 for a reason: a copied command with a placeholder in it fails in a way that wastes the reader's afternoon.

## What the mechanical layer sees here

The most relaxed register outside `chat`, and every cell has a reason. The vocabulary tiers run in partial mode for the same reason as `technical-blog`. Em dashes are relaxed to six and curly quotes to four, because a long reference page accumulates both without either being a tell. Transition phrases relax to three and hedging to two, since a doc legitimately qualifies. Emoji in headers, excessive bullets, bullet-NP lists, uniform paragraph length, and list-label periods are skipped outright, because each of them is the correct form for a parameter list and reporting them would report the genre.

Significance inflation is relaxed rather than skipped, at one. A reference page that says something `plays a key role` is writing in the register. Two of them is a habit.

What still runs at full strength is the whole `safety` band, every P0 fingerprint, and the placeholder check.
