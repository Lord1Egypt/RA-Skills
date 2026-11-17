# <SERIES TITLE>: season grid

One row per episode. Write each episode only from its own row: events from later rows stay in later episodes.
Spring is COMPRESS (pressure piles on the lead) or RELEASE (the pressure pays off).
Cliffhanger types come from references/cliffhangers.md; never the same type twice in a row.
Pay is PAYWALL on the last free episode (apps), HOOK on later pay hooks (around 30 and 60), blank otherwise.
Check with: python3 scripts/grid_check.py grid.md

| Ep | Title | Spring | Open (resolves the last cliffhanger) | Hook (first 3 s) | Reversal | Payoff | Cliffhanger type | Cliffhanger beat | Cast | Places | Rung | Secrets | Pay |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | <title> | COMPRESS | (cold open) | <image and first line> | <the turn at 30 to 50%> | <the small win> | <type> | <the last beat> | <names, comma separated> | <places, comma separated> | 1 | <secret: teased / partial / revealed> | |
| 2 | | | | | | | | | | | | | |
| 3 | | | | | | | | | | | | | |
| 4 | | | | | | | | | | | | | |

Checks before writing episodes:
- [ ] Every row has a reversal, a payoff and a cliffhanger; no type twice in a row; no type on more than a third of the rows.
- [ ] No more than two COMPRESS rows in a row; a RELEASE at least every three rows.
- [ ] Episodes 1 to 3: identity, crisis, first payoff. Episode 3 ends on the strongest cliffhanger so far.
- [ ] The PAYWALL row asks a question; the answer lands one or two rows later.
- [ ] Each villain rung falls in public before the next rung appears.
- [ ] Each secret goes teased, then partial, then revealed, once each, at planned rows.
- [ ] Four cast members or fewer per row; two places per row (a third only as a short insert).
- [ ] The lead makes a choice or strikes back in most rows.
