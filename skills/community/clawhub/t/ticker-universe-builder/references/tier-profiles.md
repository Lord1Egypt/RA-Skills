# Light / Medium / Heavy / Max

Depth describes representative coverage, not how many codes a data provider can return.

| Depth | Entity selection | Satellite maximum |
|---|---|---:|
| Light | Concise leader-only skeleton | 0% |
| Medium | Most reviewed leaders (at least 70% of the declared roster) | 0% |
| Heavy | All reviewed leaders and necessary differentiated peers | 20% |
| Max | The same qualified Heavy, expanded by at least 30% with justified supplementary Beta | 35% total |

These proportions are explicit starting constraints, not empirically optimal weights. A leader
may itself have high measured beta; admission role describes its function, not volatility.
Light means all its entity members are leaders, not every leader in the whole market.
Reference instruments are additional, separately audited, and exported in the same TXT.

## Counts are ceilings

Declare four nondecreasing entity budgets in the [coverage plan](coverage-plan.md). Reference
instruments do not consume them. First fit the necessary roster; remaining capacity can be left
unused, provided Max also satisfies its minimum growth. There is no bucket fallback. A spec `target_count`
may lower the planned ceiling, but cannot raise it or silently discard necessary coverage.

For the first Core migration, compare at roughly CN 463 securities, US 378 securities and
Crypto 53 assets/tools, then explain any extra economic coverage that justifies a larger budget.
These are the supplied review's comparison counts, not verified leader totals or fixed market
defaults. In particular, Crypto Heavy no longer defaults to 260.

## Fair expansion

Economic parent-sector caps remain hard bounds. Heavy optional seats use stable weights;
Max additions follow Heavy group proportions, with only integer rounding surplus. Merge sparse
related themes for readability, preserving economic duties. Light/Medium can use broader
groups; Heavy/Max must share their group map. Splitting headings cannot add capacity. Branch duties and all necessary representatives come first, including cold
industries. A shortage of qualified optional candidates leaves Max in `needs_research`;
it is not proof that the market has no more candidates.

Max must use `--seed heavy.json`, from the same market, plan and source date. Every retained
member and instrument binding stays identical. Every new member must be a sourced satellite
with measured liquidity; missing necessary representatives must be repaired in Heavy first. No theme has to
expand. For Heavy's actual entity count `H`, add at least `ceil(H * 0.30)` Beta entities.
References never enter either count. There is no separate growth upper bound: the plan/spec
entity ceiling, economic sector caps, total satellite share and export limits still bind.
A plan/spec ceiling below `H + ceil(H * 0.30)` blocks the build.

Growth and total satellite share are different constraints. For example, a Heavy already at
20% satellites cannot grow 30% entirely through Beta while keeping Max at 35% satellites.
An infeasible pair of constraints, sector/export limits must be reported explicitly; never drop protected members, relabel roles or loosen gates.
Below-minimum results retain a resumable research checkpoint, not a completed watchlist.

## Historical compatibility

The 60/160/400/580 bases, market breadth multipliers, taxonomy coverage levels and bucket targets
remain for archived 0.4/0.5 replay and legacy display-table checks. They do not size or allocate
new coverage-first builds. Use [legacy-policy.json](../assets/legacy-policy.json) explicitly to
reproduce archived inputs; their validation does not certify current coverage quality.
Previously published coverage-first Max files below 30% growth are historical outputs;
they do not pass the current contract and must be expanded before republication.
