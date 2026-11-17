# Coverage-first research contract (0.6)

Read with [data-contracts.md](data-contracts.md). The default builder requires this plan. It does
not infer leadership from Core membership, market cap, ANCHOR, provider tags or a high score.
Historical replay alone uses [the archived policy](../assets/legacy-policy.json).

## Plan before candidates

`snapshot.coverage_plan` is an object with these required fields:

| Field | Shape / meaning |
|---|---|
| `schema_version` | `1` |
| `origin` | `new` or `migration`; migrating a user Core requires `baseline` |
| `scope` | Explicit market, venues, instrument types, exclusions; do not silently narrow Crypto to Binance |
| `evidence` | Dated tier 1/2 evidence for the stable market structure, not recent news heat |
| `budgets` | `{light: int, medium: int, heavy: int, max: int}` positive, nondecreasing **entity ceilings**, excluding references |
| `sectors` | List of `{id, weight, rationale, caps}`; positive stable weight and four nondecreasing integer absolute caps keyed by profile |
| `branches` | List of `{id, sector, purpose, min_profile, representatives}`; `representatives` is a nonempty list of necessary economic `asset_id`s; each entity has one primary branch |
| `roster` | Every branch representative exactly once: `{asset_id, kind, min_profile}`; kind `leader` or `peer`, admitted by Heavy |
| `references` | List described below, may be empty; BTC/ETH/SOL are Crypto entities, not references |
| `display_groups` | Optional four-profile object; rows have constituent `id`, ASCII `name`, disjoint known `themes`, and economic-similarity `reason`; Heavy/Max maps must match |

Economic sectors/branches remain separate from presentation. Merge sparse one/two-entity
groups with economically adjacent duties for readability, preserving member facts and duties.
Light/Medium may use broader display groups; Heavy/Max use identical groups. Max follows Heavy
entity proportions: for total added A and Heavy H, group h can add at most ceil(h*A/H).
Rounding is the only surplus; split headings cannot create capacity. A branch's `min_profile` is Light,
Medium or Heavy; when reached, it needs a researched core representative. All roster entries
must exist as eligible, researched candidates before building the ladder. The budget must fit
all representatives due at that depth. Do not silently change their tier to fit.

Leader `min_profile` describes the breadth of necessary leaders: Light is concise and leader-only;
Medium contains at least 70% of the reviewed leader roster; Heavy contains every reviewed leader
and necessary differentiated peer. Peers enter at Heavy. This denominator is the **declared
research roster**, not a claim to know every leader in the market. Audit Core blind spots too.

Heavy satellite share is at most 20%, Max at most 35%, measured on selected entities. These
are transparent initial engineering limits, not empirically optimal market weights. Policy may
tighten them. Sector caps also bind necessary representatives: an infeasible plan is returned for
research, never resolved by evicting a leader. Heavy optional allocation uses stable sector weights and existing counts. Max uses Heavy
group proportions; candidate shortages are research gaps, not permission to overweight another
group. Stop at the minimum qualified expansion. Recent heat and label weights do not enter.

Use roughly comparable Core budgets for the first migration: the supplied review has CN 463,
US 378 security-layer entries and Crypto 53 asset/tool entries. These are comparison scales,
not pre-approved counts or an assertion that all entries are distinct verified leaders.

## Candidate admission

Every selected entity keeps the existing candidate contract plus an `admission` object:

| Field | Meaning |
|---|---|
| `kind` | `leader`, `peer`, `satellite`; selection function, distinct from measured beta or observation role |
| `branch` | One economic branch id; determines primary sector independently of display theme |
| `min_profile` | Light/Medium/Heavy for leaders; Heavy for peers; Heavy/Max for satellites |
| `business` | Why this entity represents this business function; source-supported leadership/necessary differentiation |
| `quality` | Required for leaders/peers: domain-specific continuing quality/observability reasoning; optional for satellites |
| `evidence` | Tier 1/2 evidence for those assertions, no future dates and within 180 days of snapshot |
| `instrument` | `{kind, quote_currency, units}`; kind equity/spot/perpetual/etf, positive units; explicit contract multiplier |
| `ecosystem_id`, `token_role` | Required for Crypto; distinguish VET/VTHO roles without claiming two independent networks |
| `market_cap` | Satellites: `{value, currency, basis, as_of, source}`; positive finite capitalization, equity/native quote currency for stocks, circulating/USD for Crypto (never FDV); within 30 days, matching dated tier 1/2 admission evidence |
| `distinct_from`, `incremental_value` | Satellites only: nonempty core asset-id list and what is missing without this candidate |

Leaders/peers must carry a compatible core observation role; satellites require
`BETA_SATELLITE` as the supplementary-business observation role. Price R²/beta/stability
are optional descriptors, not admission floors; supplied values retain measurement integrity checks.
Entity liquidity must be measured.
Unannotated eligible candidates remain a research bench and are audited as unverified admission;
malformed supplied admissions fail rather than silently passing. Breadth/tactical roles remain
readable in old records but are not a fallback that fills new production lists.

Evidence validation checks provenance shape and dates; it cannot verify that a cited document
actually proves a business claim. The agent must read it and compare the candidate against peers.
Beta research stops after broad business/token identity and complementarity checks plus sourced market cap. Rank eligible Beta by capitalization within the planned distribution; equal caps break ties by ticker. Detailed profitability, tokenomics, supply unlock or revenue analyses are not Beta prerequisites. Core research remains unchanged. For Crypto core representatives, research use, token value capture, supply, liquidity and residual redundancy; a token
with no holder revenue can still represent a network, but is not a revenue-producing protocol by
analogy. Old strict new-token thresholds are research context, not universal leader criteria.

## Reference instruments

Each row: `{id, ticker, theme_code, kind, observes, evidence}`. `kind` is index/yield/fx/commodity/
etf/spot/future/ratio. Use the exact observed instrument, full venue-prefixed ticker and existing
display theme. Evidence must verify the instrument and its observation meaning. Do not fabricate
a trading-volume requirement for a direct yield or index series. For an intentional proxy, add
`proxy_for` and a nonempty `limitation`; an ETF remains an ETF, never rename it to an index.

References do not consume entity/sector/satellite budgets. They do consume export ticker and
TradingView token caps, appear in the same script-rendered TXT and are listed in the report.
Do not use this layer for companies, protocols or otherwise eligible entities to evade ceilings.

## Core migration

Start a reproducible queue without guessing identities:

```bash
python scripts/universe.py audit-core --watchlist core.txt --universe old-heavy.json \
  --output core-audit.json
```

The audit contains the exact original text/SHA-256, full-code differences and one `pending`
decision per original symbol. It does not mark a retained code as a verified leader. For the
researched plan, `baseline` holds `{watchlist, sha256, decisions}`. Each decision holds
`{ticker, action, reason, evidence}`; retain/replace additionally binds exactly one `asset_id`
or `reference_id`. Allowed actions: retain/replace/remove/pending. Retain preserves the full
code; venue or spot/perpetual conversion requires replace and a sourced explanation of identity,
units and observation changes. Deletion needs a sourced reason and surviving branch coverage.
Every original symbol must occur exactly once. Pending blocks Heavy/Max; a retained or
replaced target must actually be selected in Heavy. There is no automatic alias resolution.

## Building and continuing

Default `target_count` is the plan's entity ceiling; a spec can lower it, never expand the plan.
A qualified result below the ceiling is **complete** with `unused_capacity` only when all gates
pass, including Max's minimum growth.
Unresolved backbone, identity or Core decisions are `needs_research` with archived inputs and
resume command. Repair the failed assertions, remeasure affected candidates, then resume; retain
successful research instead of restarting a broad screen. Do not spend retries on unchanged input.

Max requires `--seed heavy.json`: same market, source date and complete plan, validated Heavy,
identical retained member facts/bindings, and only satellites added. With `H` Heavy entities,
Max needs at least `H + ceil(0.30 * H)` entities. References are excluded.
An underfilled bench is `needs_research`; preserve inputs, widen research and resume. The
effective target remains the plan/spec entity ceiling; growth has no separate maximum. Incompatible
sector, satellite-share or export ceilings cannot be waived to achieve the minimum.
The embedded `heavy_base`
allows standalone validate to recheck this without external files. Updating Heavy requires
rebuilding Max; maintenance cannot silently diverge the pair.

Legacy `taxonomy --check` remains a display-table compatibility/preflight diagnostic, not the
0.6 economic feasibility test. Formal build/validate checks the coverage plan instead. Existing
`measure`, qualification gates, content/version hashes, atomic artifacts and retry receipts remain
in use. `validate` of a legacy record explicitly discloses the absence of coverage certification.

A small growth-only shortfall may now be delivered as an explicit validated `partial`, never
complete: gap <=5% of the required total entities, all member/core/identity/evidence and cap
checks passed, planned group quotas retained. See [delivery contract](data-contracts.md#max-shortfall-delivery-071)
and [recovery handler](recovery.md). Unmarked or larger shortfalls remain needs_research.
