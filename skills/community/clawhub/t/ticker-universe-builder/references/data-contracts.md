# Data contracts

Build inputs and output records use `schema_version: 1`; the policy has its own version.

## Coverage-first default (0.6)

New builds require [coverage_plan and candidate admission](coverage-plan.md). Read that contract
before creating a new snapshot. `target_count` is an entity ceiling, excludes references, and
defaults to the plan budget. Light/Medium are leader-only; Heavy protects the reviewed backbone;
Max requires the same-date qualified Heavy seed. Default builds never use legacy bucket
fallbacks. A qualified under-ceiling result is complete with `unused_capacity` only when all
gates pass. A complete Max must grow by at least 30% in entities, with all additions admitted as satellites;
under-expansion or unresolved coverage is `needs_research`.

`policy.coverage.max_expansion` is `{ "min": 0.30 }`. The minimum must be finite
and at least `0.30`; a custom policy may tighten it. For actual Heavy entity count `H`,
require at least `H + ceil(H * min)` entities. There is no separate growth upper bound:
plan/spec entity budgets, economic sector caps, total satellite share and export limits still bind.
Reference instruments are excluded. `stats.quality.expansion` reports `heavy_entities`,
`added_beta`, `growth` (a fraction), `min_entities` and `max_entities` (the plan/spec entity ceiling,
not a promise of available eligible capacity).
Max follows Heavy display-group entity proportions. For Heavy H and actual additions A,
a group with h Heavy entities may add at most ceil(h*A/H), including only integer rounding
surplus. Build selects ceil(H*min) additions and then stops; target_count remains a ceiling.
Optional profile-keyed display_groups are documented in coverage-plan.md.

The same rules apply to stored validation and maintenance. A new explicitly marked `delivery`
partial is an authorized exception to growth only, as specified below. Unmarked underfilled
outputs remain invalid. Older below-minimum coverage-first
Max files remain historical artifacts, not current-contract completions. Legacy 0.4/0.5
records remain readable with a legacy-certification warning and their explicit replay policy.

The measurement/listing/identity contracts below remain mandatory. Sections discussing bucket
quotas, default breadth counts and theme-presence selection describe archived 0.4/0.5 replay,
not the coverage-first selector.

## Research integrity (0.4)

Eligible measured candidates require a valid per-ticker `measurement_record`.
Eligible candidates require a non-empty `reason`, tier 1/2 evidence, and `listing` with
`status: "active"`, an ISO `as_of`, and an http(s) `source` also present in their strong evidence.
An active quotation is evidence of tradability at the stated date, not proof of financial quality.
Optional `reason_summary` is a non-empty, single-line string of at most 160 characters, written
in the report's market language (prefer at most 60 characters for Chinese). It explains the
business observation briefly, without source URLs or audit narration. It is preserved in JSON
and used only for presentation; full `reason`, admissions and evidence remain authoritative.
Without a summary, Markdown uses a bounded first-sentence excerpt of `reason`.
Optional snapshot `report_translations` is a supported-language-keyed text map, for example
`{"en": {"航空产品。": "Aviation products."}}`. Keys match original display text exactly;
values are non-empty authored translations. Supply names, short reasons, theme labels/purposes,
notes, measurement descriptions and reference descriptions used by the report. The Markdown and
HTML renderers use this map only for presentation; selection, ticker codes, original research
and TXT are unchanged.
Translated member reasons retain the 160-character limit. Missing entries retain the original
text for older inputs; review language completeness before delivering an English report.
The map is preserved in universe JSON and covered by `content_hash`.
Listing checks expire after 30 calendar days; observations dated after the snapshot are refused.
Ineligible candidates may omit listing facts but must retain their exclusion code and evidence.

`independence` is measured-only and must be derived from `factor_r2`. In coverage-first builds,
`BETA_SATELLITE` with `admission.kind: satellite` means a supplementary business/token observation.
Price `factor_r2`, `beta_strength` and `beta_stability` are optional descriptors, never admission
floors or capitalization-ranking inputs. Supplied statistics still need valid measured provenance,
including at least 30 overlapping returns and gauge legs. Liquidity remains required and measured.
Legacy high-beta roles retain R² >= 30, strength >= 55 (positive beta >= 1.1) and stability >= 50.

`measure` writes per-ticker `measurement_record`: as-of date, source, input SHA-256, actual
first/last observation dates, factor legs/model and observation counts. It clears old measured
values on refresh, including values the replacement table cannot supply. Missing required data
marks the merged snapshot incomplete; notes and coverage persist into the universe JSON.
Per-ticker missing-factor diagnostics stay in JSON rather than the readable Markdown report.
`measurement_audit` preserves dated theme fit/fund diagnostics through merge and build.
Snapshot measurement declarations describe common units; ticker records identify distinct gauges.
`content_hash` covers the complete output record separately from membership `version_hash`;
both hashes are required when validating a stored universe. Version 0.3 snapshots need listing
checks, reasons and measurement records before rebuilding; declared market guidance needs four tiers.

Profiles are `light`, `medium`, `heavy`, `max`. The 0.6 coverage contract defines their
selection roles and hard ceilings. Historical replay alone retains the former 45% expansion
and 70% incremental-beta preference. The 1,000-token file limit applies to entities, references
and headers together.

Maintenance also accepts `UPDATE_THEME` (`theme`, one or more of `weight`, `theme_name`,
`purpose`, `representative_roles`, reason, evidence)
and `REFRESH` (`ticker`, complete `candidate`, reason, evidence). REFRESH preserves ticker,
asset identity, theme, role and required status and records a fact refresh without membership churn.
ADD_THEME accepts weight. Hysteresis is a research requirement; the script guarantees turnover
limits and flip-flop disclosure, not an unimplemented two-snapshot decision rule.

## build-spec.json

```json
{
  "schema_version": 1,
  "market": "crypto",
  "profile": "light",
  "as_of": "2026-09-16",
  "target_count": 40,
  "allow_outside_guidance": false,
  "hard_ticker_cap": 1000,
  "tradingview_token_cap": 1000
}
```

`target_count` may be omitted: the coverage-plan ceiling applies (legacy replay uses policy
guidance). One market per run. `allow_outside_guidance` only affects legacy replay; it cannot
bypass economic coverage or raise a coverage-plan ceiling.

## Importing an existing watchlist

`import` reads a TradingView `.txt` — comma separated on one line, or one ticker per line — and
writes a snapshot skeleton. Sections become a draft taxonomy at coverage level 1; a section
already named in this skill's own format (`00_A_CORE_ASSETS`) keeps its codes, so the output of a
build round-trips back into an input.

Everything a txt file cannot carry is left empty rather than guessed: `role` is blank, `metrics`
and `evidence` are empty, every candidate is `eligible: false` with the reason
`unverifiable_fact: imported from a watchlist, not yet researched`, and `complete` is false. The
draft will not build until it has been researched, which is the correct behaviour — the import
saves the transcription, not the work. Tickers that do not match the named market are listed in
`notes` instead of being dropped.

## Checking a theme table

`taxonomy --check FILE --market M [--profile P] [--target N]` reads a bare taxonomy list or
the `{schema_version, market, taxonomy}` object written by `taxonomy --output`.

Default coverage-first checks structure only (`scope: "display_structure_only"`). Errors are
malformed/duplicate themes, conflicting parent labels or no Level-1 theme. Warnings identify
non-ASCII export headers and groups that first appear beyond Light. `stats.capacity[profile]`
contains the visible theme count and optional informational target. It does **not** infer a
member floor, economic budget or weighted expected membership from display headings.
Economic feasibility, duties and merged export capacity are validated at build time against
`coverage_plan` and researched admissions.

Explicit archived policies additionally check legacy per-theme presence, size guidance,
weighted concentration and `floor_share`. Those diagnostics never certify the current model.
Exit 0 with warnings, 2 with errors.

## snapshot.json

### Theme observation duties

New research tables declare `purpose` (a non-empty sentence explaining the economic variable
being observed) and `representative_roles` (a non-empty list drawn from `BENCHMARK`, `ANCHOR`,
`THEME_LEADER`, `QUALITY_LEADER`). In archived selection, at least one eligible member
with one of these roles must
represent each reachable theme (an OR condition). Coverage-first protects necessary
representatives and branch duties declared in `coverage_plan`; a display theme does not
create another seat floor. Satellites cannot silently replace those required representatives.
A role declaration needs a purpose. Legacy tables may omit both and retain their old
coverage checks, with missing duties disclosed in validation statistics/warnings.

`purpose` describes a duty, not a promise about a company's business. Candidate `reason` and
strong `evidence` must explain why that member serves it. Source classification, liquidity rank
or low R² alone is not leadership evidence. A duty may have multiple representatives; it does
not impose a one-leader limit. Both fields survive hashing, rendering and `ADD_THEME`.
`UPDATE_THEME` may explicitly revise them with reason/evidence; retire an obsolete duty with
`REMOVE_THEME`, never empty it to conceal a coverage gap.

```json
{
  "schema_version": 1,
  "market": "crypto",
  "as_of": "2026-09-16",
  "complete": true,
  "sources": [{"url": "https://...", "as_of": "2026-09-16", "kind": "exchange", "tier": 1}],
  "measurement": {
    "liquidity": {
      "basis": "measured",
      "method": "cross-sectional percentile of 30d USDT notional turnover",
      "window": "30d",
      "source": "https://..."
    },
    "quality": {"basis": "judged", "method": "revenue durability read from official documentation"}
  },
  "taxonomy": [
    {
      "l1_code": "00",
      "l1_name": "Core Assets",
      "theme_code": "00_A",
      "theme_name": "CORE_ASSETS",
      "coverage_level": 1,
      "weight": 2.5,
      "purpose": "Observe the common crypto market factors.",
      "representative_roles": ["BENCHMARK", "ANCHOR"]
    }
  ],
  "candidates": [
    {
      "ticker": "BINANCE:BTCUSDT.P",
      "asset_id": "BTC",
      "name": "Bitcoin Perpetual",
      "theme_code": "00_A",
      "role": "BENCHMARK",
      "required": true,
      "eligible": true,
      "exclusion_reasons": [],
      "reason": "Core benchmark with an active contract check",
      "listing": {"status": "active", "as_of": "2026-09-16", "source": "https://..."},
      "measurement_record": {"as_of": "2026-09-16", "source": "https://...",
        "data_sha256": "<64 hexadecimal characters from the input file>",
        "first_session": "2026-08-01", "last_session": "2026-09-16",
        "liquidity_observations": 30, "observations": 0, "benchmarks": []},
      "metrics": {"liquidity": 100, "quality": 95},
      "evidence": [{"url": "https://...", "as_of": "2026-09-16", "kind": "listing", "tier": 1}]
    }
  ]
}
```

### market_spec

Only for a market this skill does not register. `cn`, `us` and `crypto` carry reviewed rules and
refuse a declaration; anything else is buildable by researching the same handful of facts a
registry row would have held:

```json
"market_spec": {
  "code": "th",
  "label": "Thailand SET",
  "language": "en",
  "venues": ["SET"],
  "symbol_pattern": "[A-Z][A-Z0-9\\-]{0,9}",
  "symbol_hint": "one to ten characters starting with a letter",
  "venue_in_asset_id": false,
  "asset_id_strip": [],
  "factor_r2_required": false,
  "breadth": 0.7,
  "evidence": [{"url": "https://www.set.or.th/...", "as_of": "2026-09-17", "tier": 1}]
}
```

The declaration still requires exactly one of `breadth` or four-tier `guidance` for
compatibility with archived records. These describe legacy sizing only. Coverage-first always
sizes from `coverage_plan.budgets`; neither field overrides it. `breadth` scales historical
60/160/400/580 bases only when an explicit legacy policy is used.

The same coverage-plan, admissions, evidence tiers,
measurement rules, turnover budgets and hashing apply as for a registered market. This
block is the *only* thing a market gets to decide for itself, which is why it is checked like any
other researched fact:

- **Strong evidence is required.** A venue code and a symbol shape are easier to invent than a
  ticker, and a wrong one changes what counts as the same asset for every member at once.
- **A size is not optional.** The deeper tiers are defined relative to the shallower ones, so
  a build with no stated Light size would have to invent one — and an invented range reports
  nothing when a universe comes out the wrong size.
- **`language` must have a locale.** Omit it for English rather than naming a language this skill
  cannot write.
- **It is recorded and hashed.** The universe carries the declaration, `validate` re-resolves the
  rules from that record rather than from the registry, and `version_hash` covers it — two
  universes built under different identity rules are not the same universe. A change set may not
  redeclare it; different rules mean a rebuild.
- **Every report says so.** A build and every later validation both warn that the rules were
  declared rather than reviewed, and `.md` carries a `Market rules: declared` line that a
  registered market never prints.

### measurement

Every metric that appears on any candidate needs a declaration, and a metric with no declaration
stops the build. `basis` is `measured`, `judged` or `blended`:

- `measured` additionally requires `window` and a `source` URL.
- `judged` requires only `method`, and is **refused** for `liquidity`, `factor_r2`,
  `beta_strength` and `beta_stability`. Those are window-dependent statistics: a model that has
  not run the computation does not have the number, and a filled-in guess is indistinguishable
  from one that was measured. [measurement.md](measurement.md) is how you compute them.
- `blended` applies to `quality` alone and requires a `source` for the facts. It is not optional:
  if any candidate carries `quality_facts` the declaration must say `blended`, and if none does
  it may not claim otherwise.

This block is the difference between a universe whose numbers can be re-derived and one whose
numbers merely look quantitative.

### metrics

All scores are `0..100`. `factor_r2` is stored as a percentage, and the builder recomputes
`independence = 100 - factor_r2` from it so the two cannot contradict each other. Unknown metric
fields are rejected rather than ignored.

Role-specific requirements the builder enforces:

| Role | Requires |
|---|---|
| any non-anchor | `liquidity` |
| `INDEPENDENT_SENSOR` | `independence >= 50` |
| legacy `BETA_SATELLITE` | `beta_strength` and `beta_stability`; coverage satellites require measured liquidity, with factor metrics optional |
| `LIQUIDITY_SENSOR`, `NEW_LISTING` | `heat` |
| established Crypto core / legacy members | `factor_r2`; coverage satellites may omit factor metrics |

`null` means not measurable. It is not a bad score, and it must not be replaced by a low one.
In explicit legacy replay, a member is scored against the **full** weight of its bucket's fields, so an
absent field costs exactly what it weighs. Renormalizing over the fields that happen to be
present would make silence profitable — a candidate carrying only `liquidity 0.95` would outrank
one carrying `0.90 / 0.85 / 0.80 / 0.75` — and the silence is manufactured by the rule above,
which forbids replacing an unmeasurable number with a guess.

Normalized members retain legacy metadata `scored_on`, `{"present": n, "of": m}`: how many of its bucket's
weighted fields carried a value. `0.62` from four fields and `0.62` from two are not the same
claim, and only the second is partly a statement about missing research. Only legacy build reports count partially scored members. Coverage-first selection does not
use composite scores or interpret absent optional price metrics as incomplete Beta research.

### quality_facts

Core requires researched quality; coverage satellites may omit it. Optional `quality_facts`
retain separately checkable facts and historical blended metadata. The blend ranks only in
explicit legacy replay, not coverage-first Beta selection.

```json
"quality_facts": {
  "listing_age_days": 4380,
  "size_rank_pct": 96,
  "adverse_flags": []
}
```

The rule half is the mean of the components present, less 25 points per adverse flag, clamped to
`0..100`. Listing age is banded — five years scores 100, three 85, two 70, one 50, half a year 30,
anything shorter 10 — because the difference between four and five years of listing is not
information. `size_rank_pct` is a cross-sectional percentile within the market.

`adverse_flags` is a closed vocabulary, for the same reason the exclusion codes are. Seven codes
are universal, because every market states them in some form:

```text
risk_warning   going_concern   regulatory_action   audit_qualification
monitoring_tag restructuring   loss_making
```

Beyond those, the vocabulary follows the market. A regime issues flags no other regime has, and
a vocabulary wide enough to cover all of them would be too coarse to record any of them — an ST
designation is not `risk_warning` in general, and an NT 10-K is not a thing the A-share market
can have. So each market spec names its own, and they are accepted only in that market:

| Market | Adds |
|---|---|
| `cn` | `special_treatment`, `share_pledge_risk`, `exchange_inquiry` |
| `us` | `late_filing`, `listing_deficiency`, `material_weakness` |
| `crypto` | `unlock_overhang`, `supply_concentration`, `unaudited_contract` |

What the flag costs does not follow the market: every flag, universal or not, is the same 25
points. The rule stays one rule; only the vocabulary is local. A flag belonging to another market
is refused by name — a CN snapshot carrying `late_filing` is not a typo, it is a researcher
reaching for the wrong regime — and no two markets may claim the same code, because then a count
in two reports would look comparable when it is not. A declared market may name up to six of its
own in `market_spec.quality_flags`, may not redefine a universal one, and its codes are part of
`version_hash`. The report counts the flags it found, translated where a locale knows the code
and printed as the bare code where it cannot.

The block is optional, and needs at least one of `listing_age_days` or `size_rank_pct` — flags
alone do not make a score. It does not replace the judged value: `metrics.quality` is still
required for core and stays in the record exactly as supplied, while the built member carries
`quality_rule_score` and the blended `quality_score` beside it. Legacy selection reads the blend; the
inputs stay separable, so re-validating a built universe reaches the same number rather than
compounding it. A universe where no member carries facts validates, with a warning saying so.

### asset_id

The economic identity, which is not the same as the symbol. Crypto merges a spot pair and its
perpetual; US can merge two share classes of one company; CN keeps the venue by default, so
`SSE:000001` and `SZSE:000001` stay distinct. Two candidates sharing an `asset_id` are one
information source and the second is rejected.

### eligibility

`complete: false` blocks a formal build. An ineligible candidate must carry `exclusion_reasons`,
which enter the selection audit instead of disappearing. Each reason starts with one of these
codes, optionally followed by `: detail`:

```text
not_listed            delisted_or_halted      risk_warning_status    wrong_venue
excluded_instrument_type                      insufficient_liquidity insufficient_history
redundant_with_member unverifiable_fact       duplicate_asset        other
```

The audit also carries reasons the builder writes itself: `outside_profile_coverage`,
`not_selected_under_budget`, `removed_by_maintenance`.

Counting these is the point of the closed vocabulary, so the `.md` reports and the CLI's JSON line
both report rejections by code. A universe losing most of its candidates to `unverifiable_fact`
has a research problem; one losing them to `not_selected_under_budget` has a budget
problem. Free text cannot tell you which.

### evidence

Every item needs an `http(s)` URL, an `as_of`, and a `tier` of 1, 2 or 3 (see
[source-policy.md](source-policy.md)). Evidence older than the policy window, or dated after the
snapshot, is reported as a warning rather than silently trusted.

## changes.json

```json
{
  "schema_version": 1,
  "market": "crypto",
  "as_of": "2026-09-16",
  "complete": true,
  "sources": [{"url": "https://...", "as_of": "2026-09-16", "kind": "exchange", "tier": 1}],
  "measurement": {},
  "base_version_hash": "0123456789ab",
  "review_depth": "routine",
  "summary": "Binance listing and 30-day liquidity refresh",
  "deferred": [{"ticker": "BINANCE:TIAUSDT.P", "deferred_because": "budget spent elsewhere"}],
  "ops": [
    {
      "op": "ADD",
      "candidate": {"...": "a complete snapshot candidate"},
      "reason": "Current listing and liquidity evidence supports a tactical slot",
      "evidence": [{"url": "https://...", "as_of": "2026-09-16", "tier": 1}]
    },
    {"op": "NO_CHANGE", "scope": "00_A", "reason": "Fresh evidence supports current membership"}
  ]
}
```

`measurement` may be omitted, in which case the universe keeps the declarations it already carries.
Supply it when the method or the window changed.

### Operations

| Op | Fields | Notes |
|---|---|---|
| `ADD` | `candidate`, `reason`, `evidence` | `candidate` carries every snapshot candidate field |
| `REMOVE` | `ticker`, `reason`, `evidence` | Refused for a benchmark, anchor or `required` member |
| `REPLACE` | `ticker`, `candidate`, `reason`, `evidence` | An anchor may only be replaced by an anchor |
| `MOVE` | `ticker`, `to_theme` | Re-files a member without changing membership |
| `ADD_THEME` | `l1_code`, `l1_name`, `theme_code`, `theme_name`, `coverage_level`, `reason`, `evidence` | Its coverage level must be reachable by the current profile |
| `REMOVE_THEME` | `theme`, `reason`, `evidence` | Refused while the theme still holds members |
| `NO_CHANGE` | `reason` | A first-class result, recorded in the history |

Operations are applied in a fixed order regardless of how they are listed: `ADD_THEME`, then
`REMOVE` / `MOVE` / `REPLACE` / `ADD`, then `REMOVE_THEME`. A theme created this round can be
populated this round, and a theme can only be retired once its members have been placed. Merging
two themes is `MOVE` plus `REMOVE_THEME`; splitting one is `ADD_THEME` plus `MOVE`.

`ADD`, `REMOVE`, `REPLACE`, `ADD_THEME` and `REMOVE_THEME` all require at least one tier 1 or
tier 2 evidence item. Market narrative alone cannot admit or remove anything.

## Output

See [output-artifacts.md](output-artifacts.md) for the standard bundle, destination convention,
receipt and delivery status. The following defines hashing/checkpoint compatibility.

### Build-run checkpoint

The CLI's `OUTPUT.run/run.json` is `{schema_version: 1, kind: "build_run", inputs, status,
attempts, resume_command}`. `inputs` stores absolute spec/snapshot/policy/seed/output paths and
optional language; `attempts` holds numbered receipts with input SHA-256, archived `inputs.json`,
UTC timestamps, status, diagnostics and output artifact paths when present. Each archived input
contains the parsed spec/snapshot/resolved policy/seed and language, not executable instructions.
Statuses are `running`, `needs_research`, `partial`, `complete`. A validated subset remains
`partial` until it fills the original target in legacy replay. Coverage-first completion instead
requires quality acceptance, including Max's minimum 30% growth; capacity above the minimum
may remain unused. See [recovery.md](recovery.md) for continuation and
exit codes; validation success and requested-size completion are different claims.

All stemmed `{market}-{profile}-{as_of}` — `crypto-light-2026-09-17.json`, `.validation.json`,
`.txt`, and one `.md` and `.html` per report language: `.en.md`/`.en.html` always,
plus `.zh-Hans.md`/`.zh-Hans.html`, `.ja.md`/`.ja.html` and so
on where the market reads in something else. The watchlist leaves its directory as soon as it is
useful, so the name has to say which universe and when without the directory around it; the
reports carry their language for the same reason, and carry it even when there is only one, so
that `{stem}.en.md` is where the English report lives in all fourteen markets rather than in nine
of them. The command prints every path it wrote under `artifacts`, with the reports keyed by
language under `artifacts.reports` (Markdown) and `artifacts.html_reports` (HTML);
read them from there instead of reconstructing them. HTML is a self-contained, escaped rendering
of all members/references with the same display groups and short reasons, not a separate selector.

The `.json` is the record: spec limits, policy hash, sources, measurement, taxonomy, members, the
selection audit and the review history. For coverage-first, `version_hash` additionally covers the coverage plan and admissions.
For legacy replay, `version_hash` covers membership and taxonomy only, so
re-running with fresher metrics does not churn the version. The TXT, validation and reports are derived from it
and are never edited by hand.

An explicit legacy build’s `.validation.json` carries `stats.stability` and omits it on re-validation:
`{shift, draws, survived, of, share}` — how much of the membership two independently perturbed
re-runs agree on. Answering it needs the whole bench, including the candidates that lost, and the
universe file keeps only the members and the codes the rest were turned down under. So `validate`
on a stored file reports no stability rather than a stale one, and a reader has to treat the field
as absent, not as zero.

`version_hash` is not the skill's release number and does not move with it. The skill is
versioned in `SKILL.md` so a registry and a git tag have something to point at; a universe is
versioned by its own content so two files can be compared. Upgrading does not rewrite old artifacts. Changed contracts can require an explicit archived
policy or renewed research to revalidate them. `policy_version` records the producing policy,
and `diff` is what answers whether two universes are the same instrument.

## Comparing two universes

`diff before.json after.json` answers the question a maintenance report cannot: not "what did
this review change" but "are these two the same instrument at all". Two universes of one market
built in different sessions, months apart, or by two people.

`market_spec` comes first in the output on purpose. For a declared market the venue list and the
symbol shape were researched at run time, so a session that researched them differently did not
build a later version of the same universe — it built something incomparable, and every other
line of the diff would be misleading.

`identical` is about the instrument: membership, themes, roles and the declared rules. Metric
drift is reported separately and does not make two universes different, because metrics move on
every refresh and that is the design working rather than the universe changing. Only the largest
twenty moves are listed; the tail of a 250-member drift list is noise.

The `.md` is written in the market's own language, because a universe is read by the people who
trade that market: CN is Simplified Chinese, US and Crypto are English. It is written in English
too, because a universe is also read by someone allocating across several markets who reads none
of their languages — the reasons and the evidence are the point of the file, and a table of
headings they cannot parse withholds exactly that. So both, always; `--language` names the
companion rather than replacing English, and a market that already reads in English gets one file
rather than the same file twice. Fixed headings and vocabulary come from locale files, printed
as `基准 (BENCHMARK)` so the code a reader greps for survives translation. Human content comes
from the research, with authored `report_translations` for companion languages. Do not label
Chinese research prose an English report merely because its headings are English.
`.validation.json` stays English, diagnostics included; it is the machine surface, and its
messages name policy fields and code paths.
[markets/adding-a-market.md](markets/adding-a-market.md) carries the language for every
above-scale market, decided ahead of implementation.

Coverage-first satellite admission requires `market_cap` as specified in [coverage-plan.md](coverage-plan.md): positive sourced equity/native quote-currency capitalization or Crypto circulating USD capitalization, dated within 30 days. FDV is rejected. `quality` is optional for satellites; core still requires it. Ranking uses cap within the fixed distribution, not the legacy composite Beta score.

## Max shortfall delivery (0.7.1)

`build-spec.shortfall_action` is `auto` (default), `deliver` or `retry`; CLI `--shortfall-action`
overrides and persists in the checkpoint. Auto/deliver can emit partial only when the sole
unmet requirement is Max minimum growth, at least one Beta was added, and
`required_entities - actual_entities <= 0.05 * required_entities`. Deliver cannot waive this
bound. Retry preserves full-growth requirements and returns diagnostics for an agent repair.

A partial universe includes `delivery: {status: "partial", reason: "max_growth_shortfall",
required_entities: int, shortfall: int, allowed_gap_ratio: 0.05}`. All values are recomputed
by validation; this field is valid only for an underfilled Max within the bound. Membership,
listing, identity, measurements, admission, Heavy retention, core coverage and all other caps
still apply. Partial group ceilings use the original planned addition count
`required_entities - Heavy_entities`, keeping vacancies instead of transferring seats. Complete
Max uses actual additions as before. References do not count as growth.

Validation has `passed: true` for a contract-valid partial, `qualified: false`, and
`stats.quality.status: "partial"`. Full qualification remains `qualified: true`. The runner
returns exit 3/status partial, a continuation, and MD/TXT/JSON filenames ending `-partial`
before their extension/language. The Markdown and JSON show actual growth, required count
and shortfall; TXT stays TradingView-compatible and carries partial status in its filename.
Never change a stored partial to complete by relabeling metadata; rebuild with revised inputs.
