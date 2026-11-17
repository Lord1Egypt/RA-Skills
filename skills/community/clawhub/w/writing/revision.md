# Revision — The Pass System, the Cut, and Knowing When to Stop

Scope: turning a complete draft into a deliverable. Everything here assumes a draft with a last line (`drafting.md`).

**Before revising**, read `## Voice`, `## Never` and `## Corrections` in `~/Clawic/data/writing/memory.md`, plus `edit_depth`, `cut_target_pct` and `feedback_mode` from `config.yaml`. `edit_depth` decides which of the passes below you are allowed to run at all.

## The Passes, In Order

Each pass looks at one thing. Running them together means missing all of them, because the eye that is checking commas cannot see a misplaced section.

| # | Pass | Question | Never do here |
|---|---|---|---|
| 1 | **Structure** | Is the claim right, and are the moves in the right order? | Fix a sentence |
| 2 | **Cut** | What can go without losing an idea? | Add anything |
| 3 | **Clarity** | Does each sentence say one thing, once, in the right order? | Reorder sections |
| 4 | **Voice** | Does it sound like the person whose name is on it? | Introduce new claims |
| 5 | **Proof** | Are the names, numbers, quotes, links and spellings right? | Rewrite a sentence |

Order is not negotiable: polishing a sentence in pass 3 that pass 1 was going to delete is the most common waste in revision, and cutting after voice-matching means re-matching what survives.

`edit_depth` maps to passes: `light` = 2 and 5 only, plus mechanical fixes; `standard` = 2-5, structure left alone unless it is broken enough to say so; `heavy` = all five, including reordering and rewriting sections.

## The Cut

Arithmetic, not taste (SKILL.md Rule 3). Target reduction = draft words × `cut_target_pct`, default 20%; target length = draft words × (1 − `cut_target_pct`). The percentage is what leaves, never what stays.

Worked example — a 1,400-word post at the default:
```
target reduction = 1,400 × 0.20 = 280 words
deliver at        ≤ 1,120 words
```

Cut in this order, and stop when the target is met:

1. **Whole sections** that repeat another section's job (the reverse outline names them — `structure.md`). This is where 280 words come from in one move.
2. **The first paragraph.** Delete it and check what was lost. Throat-clearing is the most reliably deletable text in any draft.
3. **The summary paragraph**, wherever it is. If the piece needs it, the body failed and the fix is upstream.
4. **Sentences that restate the sentence before them** in different words.
5. **Subordinate clauses that qualify a claim nobody disputed.**
6. **The cutting formulas** (`clarity.md`) — mechanical, safe, roughly a tenth of most business prose.
7. **Adjectives and adverbs**, last. On their own they recover a marginal fraction of the target; as the final pass on an already-cut draft they are worth doing.

King's rule of thumb — second draft = first draft − 10% — is the floor. Prose written to be read tolerates more; prose written to be heard tolerates less, because a listener cannot re-read (SKILL.md Where Experts Disagree).

When the target cannot be met without losing an idea, say so and name the idea. Cutting content to hit an arbitrary number, without saying what left, is how a piece loses its point unnoticed.

## Proofing: Change the Medium

The eye completes what it expects. Proofing in the window where the text was written finds perhaps half the errors that are there.

Ordered by how many errors they catch per minute:

1. **Read aloud.** Catches missing words, doubled words, and every rhythm problem.
2. **Read the last paragraph first**, then the second-to-last. Breaks narrative expectation, so each sentence is read as itself.
3. **Change the rendering**: different font, different width, print, or the actual destination (the email client, the CMS preview, the phone).
4. **Sleep on it.** The single most effective and least available technique; if the deadline arithmetic in `drafting.md` allows even two hours, take them.
5. **Grep the mechanical set**: `[TK]`, `[CITE]`, `[?]`, doubled spaces, `the the`, unmatched brackets and quotes, placeholder names from a template (`[Name]`, `Acme` in a real client's letter).

Always check by hand, never by reading: every proper name, every number, every URL, every date and day-of-week pairing ("Tuesday the 14th" — verify both), and every quotation against its source.

## Deciding What Not to Change

The most damaging edits are the confident ones.

- **Anything inside quotation marks, code, a citation, a legal clause, or a name** — flag, never fix (SKILL.md Rule 7).
- **Deliberate rule-breaking that is the voice**: fragments, comma splices used for pace, a preferred non-standard spelling. Check `## Voice` before "correcting" one.
- **A claim you think is wrong**: mark it, do not soften it. Hedging someone's claim behind their back changes what they said.
- **Jargon the audience shares.** Removing the term everyone in the field uses makes the text longer and less precise.
- **Their structure, when `edit_depth` is `light` or `standard`.** Say the structure is the problem; do not rebuild it without saying so.

## When to Stop

Revision has a real stopping point, and past it, edits start being lateral — different, not better.

Stop when all of these hold:
- The reverse outline matches the intended moves.
- The word count is inside the budget and the cut target was met or the shortfall was named.
- The Output Gates in `SKILL.md` pass.
- Your last pass changed only preferences, not errors — two consecutive passes that produce only synonym swaps means you are done.

Signals you are past the point: reversing a change you made two passes ago; rewriting a sentence that was fine to avoid touching the section that is not; polishing the opening for the fifth time. All three mean the remaining problem is structural and you are avoiding it.

## Rescuing a Draft That Is Not Working

When three passes have not fixed it, the draft is not the unit of repair.

| Symptom | Diagnosis | Move |
|---|---|---|
| Every paragraph is fine, the whole is dull | No tension — nothing is at stake or contested | Find the claim someone would argue with and lead with it |
| It keeps growing | Two pieces in one | Split; the second half is usually the better piece |
| The ending will not come | The piece never had a "one thing that must happen" (`drafting.md`) | Decide it now; the ending writes itself and the middle needs re-cutting |
| You dread re-reading it | Usually a voice mismatch, not a quality problem | Read a sample aloud, then the draft (`voice.md`) |
| Fixing one paragraph breaks another | The order is wrong | Reverse-outline and reorder before any more sentence work |
| Nothing helps | Rewrite from the outline without looking at the draft | The second attempt takes a third of the time and is usually better |

Deleting a draft and rewriting from its outline is a legitimate move, not a failure. It is faster than the fifth pass and it is how most stuck pieces get finished.

**After a revision session**, write in the same turn: every edit the user reversed or corrected to `## Corrections` with its trait, any rule they stated to `## Never`, and the finished piece's row to `pieces/<year>.md` if it shipped — leaving `## Pieces` when it does (`memory-template.md`). A correction that is not recorded will be made again on the next piece, and the user will notice.
