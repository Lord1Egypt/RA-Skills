# Maintenance contract

## Maintenance is not regeneration

The agent emits operations, never a rewritten universe. The script applies them to one exact
`base_version_hash`, then revalidates and re-renders. A hard finding produces no new version at
all — a partially applied universe is worse than an unchanged one.

Rewriting a full membership list cannot be reviewed: silently dropping twenty names, reordering
sections or mistyping a venue would all pass unnoticed. Operations can each be checked, rejected
individually and reversed.

## Coverage-first invariants

Build, validate and maintenance share the same economic-coverage, satellite-share and sector-cap
checks. Removing a necessary leader or changing an admission cannot bypass the roster. Changes
to the economic plan or Core migration decisions require a researched rebuild of Heavy; then
rebuild Max against that Heavy. References are part of that immutable plan, so a reference
substitution also follows this path. Max maintenance may not change its embedded Heavy's
facts or bindings, fall below 30% growth relative to Heavy's entity count. Sector, satellite, entity and export ceilings
still bound expansion; there is no separate percentage growth ceiling.
The existing operation engine remains for valid local maintenance.

## Three review depths

| depth | Purpose | Turnover warning |
|---|---|---:|
| `routine` | Liveness, venue, liquidity, recent leadership, tactical slots | 5% |
| `deep` | Taxonomy, sector structure, quality, redundancy, coverage gaps | 10% |
| `event` | Delisting, merger, regime or theme break with a dated cause | 20% |

These are how deep to dig, not calendar periods you must wait for. Exceeding the warning line
produces a warning; exceeding twice the line is a hard failure. An urgent delisting still needs
evidence.

## A verdict comes with an operation

Judging a theme overweight means issuing `REMOVE` or `MOVE` in the same round. Judging it
underweight or missing means issuing `ADD` or `ADD_THEME` in the same round. A note that says "to
be handled in the next deep review" is a verdict nobody owns, and it is the mechanism by which a
universe quietly rots.

The turnover budget is a ranking pressure, not a reason to do nothing: take the highest-information
changes first, spend the budget, and write the rest into `deferred` with a stated reason so the
next round inherits them as machine-readable input.

Restraint applies to chasing heat — do not create a permanent theme out of three months of price —
not to fixing a known defect.

## Live-information priority

1. Listing, contract or spot status, halts, delistings, venue changes.
2. 7 / 20 / 30 / 60-day turnover and data completeness.
3. 30 / 63 / 90 / 126 / 180 / 252-day correlation, beta, R² and residual stability.
4. ETF holdings, company disclosures, protocol and exchange announcements.
5. Theme heat and news — used to explain priority, never to decide permanent membership alone.

## Low turnover and hysteresis

- A challenger must clearly beat the entry threshold, not merely edge past the incumbent.
- Incumbents are held to a looser exit threshold.
- Outside a hard event, a failure should be confirmed by two consecutive snapshots.
- Re-adding a ticker removed within the last four rounds raises a flip-flop warning.
- High-value candidates that did not fit this round's budget go into `deferred`.
- When there is not enough information gain, `NO_CHANGE` is the correct result.

The first three hysteresis bullets are research policy, not a numerical state machine in Python.
The script enforces turnover budgets and the recorded flip-flop warning.

`REFRESH` updates verified facts without membership churn; `UPDATE_THEME` updates a theme
weight/name. Both require reason and strong evidence. Supply `base_content_hash` alongside
`base_version_hash` so a proposal cannot apply over another fact-only refresh.

## Review checklist

- Is every existing member still live, tradable and on the right venue?
- Is a current theme leader or a genuinely new sector missing?
- Is a highly redundant member occupying a seat?
- Do cold sectors and market breadth still have representation?
- Is every high-beta label still supported by stable beta and R²?
- For Crypto: is each member still active on its Binance market with sustained turnover?
- Do tier, theme, role and concentration still match the policy?
- Has any bucket drifted above its target share? The validator reports this; act on it.

## Preserve observation duties

Read the current taxonomy's `purpose` before proposing REMOVE, REPLACE or MOVE. Explain in the
operation reason how the remaining/new member preserves the business, supply-chain or gauge
function. Final validation refuses a reachable theme without a member in its declared
`representative_roles`, including after maintenance. Several complementary core representatives
are allowed; this is a coverage floor, not a quota per role or a permanent ticker whitelist.

`UPDATE_THEME` can change purpose or representative roles only as an explicit evidence-backed
research decision. It cannot clear a duty to conceal a missing representative. Obsolete themes
use the existing REMOVE_THEME operation after their members have been dealt with. Avoid
recency-driven replacement; retain NO_CHANGE when incremental information is not established.
