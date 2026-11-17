# Scanner Pattern Reference

The scanner applies 16 pattern classes plus protected-name enforcement to a
draft. Each hit carries a severity and a repair. Severities:

- **CUT** — remove entirely; no rewrite preserves it. −18 points each.
- **SOFTEN** — the impulse is fine, the wording isn't. −7 points each.
- **CHECK** — context-dependent; read aloud and judge. −3 points each.

Score = 100 − 18·CUT − 7·SOFTEN − 3·CHECK, floored at 0. Ship at ≥85.

## Pattern table

| # | Class | Severity | Trigger examples |
|---|---|---|---|
| 1 | ex-partner reference | CUT | "his ex", "ex-wife", "ex-girlfriend" |
| 2 | drunk/intoxication story | CUT | drunk, wasted, blackout, vomit, passed out |
| 3 | strip club / vegas | CUT | strip, gentleman's club, lap dance, vegas |
| 4 | divorce / pessimism joke | CUT | divorce, "half of marriages", ball and chain, "game over", "last free day" |
| 5 | "finally settled" framing | CUT | "finally settled", "took you long enough", "never thought he'd get married" |
| 6 | pregnancy mention | CUT | pregnant, "baby on the way", shotgun |
| 7 | profanity | SOFTEN | damn, hell, ass, bitch, shit and variants |
| 8 | money/finance joke | SOFTEN | prenup, "her money", dowry, meal ticket |
| 9 | looks-focused compliment | SOFTEN | hot, sexy, smoking, trophy wife/husband |
| 10 | dating-app swipe joke | CHECK | "swiped right", tinder, bumble, "hinge match" |
| 11 | inside-joke marker | CHECK | parenthetical asides `(you had to be there)` |
| 12 | religion/faith assumption | CHECK | "God's plan", "blessed by", prayers |
| 13 | "However" early dig | CHECK | "however" in first 60 chars of a line |
| 14 | cliché opener | SOFTEN | "Good evening", "for those who don't know me", "when I was asked..." |
| 15 | filler on paper | SOFTEN | um, uh, "like, I guess", "sort of like" |
| 16 | protected name | CUT | any name passed via `--protected` |

## Known false positives
- "hell" in "hello" — prevented by word boundaries; but "hell of a guy" will
  flag. That's intended: it's a softener judgment.
- "vegas" in an approved how-they-met story (couple met in Vegas) — acceptable
  false positive; document the override in your notes, not the code.
- Parentheses used for stage directions like `(pause)` — rare in drafts;
  if you use stage directions, expect one CHECK noise.
- "chain" alone (without "ball and") flags via the alternation — check the
  match context before cutting.

## Extending the scanner
Add to the `FLAGS` list: `(label, re.compile(pattern, re.I), severity, advice)`.
Guidelines for new patterns:
1. One concept per entry — don't bundle "drunk OR gambling" into one class.
2. Choose severity by the grandparent test: would both grandmothers wince?
   Wince = CUT. Squirm = SOFTEN. Shrug = CHECK.
3. Word-boundary every pattern (`\b`) to avoid substring hits.
4. Advice must be actionable in one sentence: name the replacement move.

## Protected names
`--protected "Jordan,Riley"` adds a hard CUT for each name, case-insensitive,
word-bounded. Use for: ex-partners, estranged relatives, deceased friends the
speaker might reflexively mention, anyone with a restraining order, minors
whose privacy the couple wants protected.

Names are matched exactly — "Jordan" won't match "Jordan's"; if the draft uses
possessives, the count may underreport. Always read the final draft once with
your own eyes for the protected set.

## Interaction with word budgets
Every CUT shortens the draft; after repairs, re-run `scan` to confirm the
draft still hits 60-125% of target words. A speech cut to ribbons (under 60%)
needs story deepening, not flag work — return to the `build` budget.
