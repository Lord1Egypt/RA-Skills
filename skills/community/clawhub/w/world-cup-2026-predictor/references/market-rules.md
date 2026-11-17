# Market Rules

These rules apply the V2 cross-market framework to international and club football. Observable prices and movement may reveal the risk a market is protecting; they do not prove manipulation or that a bookmaker knows the result.

## Core Priority

1. Use 90-minute moneyline movement for win/draw/loss direction.
2. Compare qualification/to-lift market with 90-minute moneyline to detect extra-time or penalty risk.
3. Use Asian handicap/spread to decide whether a favorite can cover or only win narrowly.
4. Use totals and BTTS to shape the scoreline.
5. Explain whether news is confirmed by price movement or just public sentiment.
6. Use correct score only after market structure is understood.

## Competition Context

Confirm context before interpreting motivation or advancement:

| Match type | Required interpretation |
| --- | --- |
| `league_or_group` | Forecast the 90-minute result; table position, goal difference, and draw incentives may matter. Do not invent an advancement probability when no such market applies. |
| `single_leg_knockout` | Keep 90-minute and qualification markets separate; extra time and penalties create real divergence. |
| `two_leg_first` | Expect aggregate caution and asymmetric risk. Do not assume the home favorite must chase a large margin. |
| `two_leg_second` | Require the current aggregate score and tiebreak rules. The side trailing on aggregate may accept early risk; the leading side may protect space even when its 90-minute price is short. |
| `friendly` | Rotation, substitutions, and motivation are unstable; apply the confidence penalty and avoid strong edge language. |

If match type is unknown, calculate market consensus only. Do not infer advancement or tactical incentives.

## Favorite Movement

| Signal | Read |
| --- | --- |
| Favorite shortens and handicap also strengthens | Favorite direction is credible; cover becomes more plausible. |
| Favorite shortens but handicap does not follow | Favorite may win, but narrow win is more likely than a blowout. |
| Favorite drifts near kickoff | Warning signal; protect draw, underdog +0.5, or upset. |
| Favorite drifts while totals stay high | Underdog scoring threat rises; protect 1-1, 1-2, 2-2. |
| Favorite qualification price is strong but 90-minute price is weak | Favorite may advance after draw/extra time; protect 90-minute draw. |

## Asian Handicap Cross-Check

Asian handicap answers "can the team cover the line?", not just "will the team win?"

| Combined signal | Read |
| --- | --- |
| 1X2 favorite shortens and Asian line moves from -1.0 to -1.25/-1.5 | Favorite win and cover are both being confirmed. |
| 1X2 favorite shortens but Asian line stays flat or weakens | Favorite may win, but narrow win/failed cover is live. |
| Favorite Asian line weakens from -1.5 to -1.25/-1.0 | Market is protecting the underdog; reduce blowout confidence. |
| Favorite line deepens but favorite water gets much higher | Book is asking for favorite backers at a better payout; treat cover as unconfirmed. |
| Underdog + handicap water keeps dropping | Underdog protection is real; protect one-goal favorite win, draw, or upset. |
| Moneyline and Asian handicap disagree | Prefer split conclusion: ML/advance for winner, Asian handicap for margin risk. |

## Big Favorite Pattern

Big favorites often win, but the spread and over can fail in knockout matches.

- If favorite is very short and opponent sits deep, prefer 1-0 or 2-0 over automatic 3-0/4-0.
- If favorite ML is very short but Asian handicap does not deepen, do not infer a blowout from ML alone.
- If favorite leads early and tempo-control incentives are high, reduce cover confidence.
- If the favorite's defense has shown leaks and BTTS/over shortens, 2-1 or 3-1 becomes more plausible than 2-0.

## Medium Favorite Pattern

Medium favorites are often where 2-1, 1-1, and extra time live.

| Market shape | Score tendency |
| --- | --- |
| Favorite around modest moneyline favorite, BTTS yes firm | 2-1 or 1-1. |
| Favorite price strong but handicap weak | 1-goal favorite win or 1-1. |
| Qualification favorite, 90-minute market close | 1-1, 0-0, extra time/penalties. |
| Over 2.5 near even and both teams have transition threats | 2-1, 2-2, 3-2. |

## Small Favorite / Coin-Flip Pattern

- Do not lean on team reputation alone.
- If draw price shortens and under is firm, make 0-0 or 1-1 a main scenario.
- If one side's qualification price is favored but 90-minute ML is close, separate "advance" from "win in 90".
- In strong-versus-strong matches, small favorite plus under often points to 1-0, 1-1, or 0-0.

## Totals and BTTS

| Signal | Read |
| --- | --- |
| Over 2.5 shortens steadily | Prefer 2-1, 2-2, 3-1, 3-2; avoid 1-0 as main score. |
| Under 2.5 shortens steadily | Prefer 1-0, 0-0, 1-1, 2-0. |
| Under shortens and BTTS Yes also shortens | 1-1 is the central score. |
| Under shortens and BTTS No shortens | 1-0, 2-0, 0-0 are central. |
| Over stays high while favorite drifts | Upset with goals or both teams scoring becomes more plausible. |

Related derivative markets are consistency checks, not extra independent votes. DNB, double chance, team totals, BTTS, and correct score often reuse the same underlying information, so cap each market family's influence.

## News Filter

Classify every news item:

- **Hard signal**: confirmed starting XI, major injury, suspension, formation change, goalkeeper change, extreme weather, rest/travel disadvantage.
- **Public/emotional signal**: star return hype, host-country narrative, media pressure, brand-name team reputation, revenge story.

News is trustworthy only when the relevant market confirms it. If public news moves ML but handicap and totals do not confirm, mark it as possible sentiment trap.

## Final Forecast Template

Produce in the user's language. Use English labels for English users and Chinese labels for Chinese users. The required content is:

- 90-minute / 90 分钟: favorite/draw/underdog with confidence.
- Advancement / 晋级: who advances and whether extra time is live.
- Asian handicap / 亚盘: whether the favorite can cover or underdog protection is better.
- Totals / 大小球: over/under lean.
- BTTS / 双方进球: yes/no lean.
- Score ladder / 比分阶梯: main score, defensive score, chaos/upset score.
- Flip triggers / 反转条件: exact market/news moves that would change the call.
