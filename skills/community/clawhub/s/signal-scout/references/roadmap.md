# Roadmap: what's built, and what's still a per-run offer

Every item below is now implemented as scripts + workflow steps in
SKILL.md — none of it runs automatically. Scan this list after delivering a
report and offer, in one or two sentences, whichever items fit the current
product; skip the ones that clearly don't apply (e.g. don't pitch "watch
mode" for a one-off competitor teardown the user called a one-time check).
Only *turn on* an item (schedule a job, start logging, add a pack) when the
user says yes — the mechanism existing doesn't mean it's opted into.

## FROZEN: do not add item 8 (2026-07-16)

**No new roadmap items until `outputs/<slug>/outcomes.jsonl` has real
outcomes in it.** As of this writing that file has never been written on any
product, which means items 1 and 5 (the feedback loop and the recalibration
that reads it) have never executed against real data, and item 7 (portfolio
mode) has never had two products to cross-reference.

This matters more than it looks. Prompts and scripts here are MIT-licensed
text in a public repo — anyone can fork the taxonomy, the query buckets, and
the scoring rubric in an afternoon. Logged outcomes are the only asset that
compounds and the only one a fork can't take: which source types and query
buckets actually produced a reply, across many products over time. The
flywheel is built. It has no fuel. Adding an eighth mechanism to an empty
flywheel makes it more elaborate, not more valuable.

The bar to unfreeze: one real run, for one real user, with one logged
outcome. Until then, the highest-value change to this repo is not a feature.

## ICP decision (2026-07-16): GTM, not the adjacent fields

Two research passes, each with verbatim-quote-only sourcing and every quote
independently re-checked through `verify_sources.py`, converged on the same
uncomfortable finding: GTM-specific complaints about AI fabrication/hallucination
are a hard zero (exact-phrase search across "AI SDR," "AI BDR," "Claygent,"
"prospect research" surfaces nothing). The same complaint is loud and specific
one field over — researchers, consultants, lawyers hand-checking AI citations,
with real scandals attached (KPMG, EY Canada, Deloitte Australia all pulled or
refunded AI-assisted reports over fabricated citations).

Decision: stay GTM. The adjacent-field pull is real but is a different-shaped
product (checking an existing AI-generated document's citations, not finding
prospects). Positioning instead leads with the pain GTM *does* voice, which
both passes documented directly: credit/tool cost burn, and output needing a
manual cleanup pass before it's send-ready. Verification is the mechanism that
makes "no cleanup needed" true, not the pitch itself — see README's
"What this actually fixes." If GTM traction doesn't materialize, the adjacent
finding is still here, verified and ready to revisit — don't re-run this
research from scratch.

## 1. Outcome feedback loop — shipped, opt-in per product

`scripts/log_outcome.py` appends replied/no_reply/converted/not_pursued
records (including `source_url`, added 2026-07-16) to
`outputs/<slug>/outcomes.jsonl`. `scripts/recalibrate.py` reads that file and
reports which source types and query buckets are outperforming or
underperforming, so the next research run (SKILL.md step 2) can weight
toward what's actually converting instead of trusting self-graded scores
alone. `diff_reports.py --outcomes` separately consumes the same file at the
per-prospect level (see item 3) — `recalibrate.py` never touches individual
prospect identity, only aggregate hit rates. Wired in as SKILL.md step 8.
Propose logging once the user is also using signal-outreach and reports back
a real outcome — don't ask them to fill out a form proactively, just log it
when they mention one.

## 2. Automated source verification — shipped, always runs

`scripts/verify_sources.py` fetches every `source_url` and checks whether the
cited evidence is contained in the live page. Required in the workflow
(SKILL.md, report-generation step 3) — nothing to propose, just don't skip it.

This is the only capability here that the rest of the category does not have.
Every mainstream verification primitive (Vectara HHEM, Google
`checkGrounding`, Ragas, Patronus Lynx, Galileo Luna, Guardrails) is
closed-book: it scores a claim against text the caller already supplies, and
leaves fetching the URL — the actual hard part — to someone else. Google's
`checkGrounding` explicitly cannot fetch. Meanwhile "verified" across GTM
tooling (ZoomInfo, Apollo) universally means *verified contact data* — is
this email deliverable — never *verified claim*. Treat this script as the
product's load-bearing claim, not a lint step, and be correspondingly
paranoid about regressions in it: an inverted check would certify
fabricated evidence as "Verified".

## 3. Watch mode / recurring scout — shipped, opt-in per product

`scripts/diff_reports.py` takes every saved snapshot for a product (not just
the last two — fixed 2026-07-16, see CHANGELOG) and prints new prospects
(never seen in any prior snapshot), recurring prospects (seen before,
cross-referenced against `--outcomes` so an already-decided prospect
resurfacing is flagged rather than silently repeated), dropped prospects,
and growing patterns. Wired as SKILL.md step 7 — runs before *any* re-run of
a previously-researched product, not only scheduled ones. The *scheduling*
half (pairing it with the `schedule` skill for a recurring trigger) is what
still needs explicit opt-in every time; the diff itself just runs whenever
saved history exists.

As of 2026-07-16, `generate_report.py` surfaces the same classification
directly on the HTML report, not only in the CLI diff: it auto-detects
sibling `analysis-*.json` snapshots and an `outcomes.jsonl` in the same
directory (override with `--history`/`--no-history`/`--outcomes`) and badges
each prospect New / Seen Nx / Resurfacing, reusing `diff_reports.py`'s own
`accumulate_history()` and `OutcomeIndex` so the report and the CLI diff
never disagree about what counts as new. This closes the original gap where
a report reopened weeks later looked identical to a fresh one — see
CHANGELOG.

## 4. Vertical query packs — shipped, extend on repeated signal

`references/query-packs/` ships three starting packs: devtools, health &
wellness, marketplace/SaaS. SKILL.md step 2 checks this directory before
falling back to generic buckets. Only propose *adding a new pack* after 2+
runs in the same untracked vertical show a repeatable pattern in which
queries/sources actually produced qualified prospects — don't write one from
a single run, and don't re-propose the three packs that already exist.

## 5. Scoring recalibration — shipped, data-gated

`recalibrate.py` (see item 1) is the recalibration mechanism — it surfaces
per-bucket/per-source hit rates once ≥3 outcomes are logged for a group
(`--min-samples`, default 3). The freshness decay function in
research-framework.md ("Signal freshness") is still a fixed step function
uniform across signal types; if outcome data clearly shows one signal type
decays slower or faster than the schedule assumes (e.g. hiring posts staying
relevant longer than forum complaints), propose editing that section — but
only once outcome data justifies it, not speculatively.

## 6. Verification tiers + clean handoff — shipped, always runs

`verify_sources.py` now tags every prospect in-place with `verification_tier`/
`verification_note` (via `--annotate-out`) so `generate_report.py` can render
a Verified/Snippet-only/Low match/Broken source badge instead of the tier
existing only in terminal output. `--handoff-out` writes a filtered copy with
broken-source prospects dropped, ready to pass to signal-outreach or any
other downstream consumer without carrying dead links forward. Wired as
SKILL.md step 3 — part of the required verification step, not a separate
offer.

Two extensions shipped 2026-07-16, both always-on like the rest of this item:
every prospect is now also stamped with `verified_at` (today's date,
regardless of tier), which `generate_report.py` renders as a client-side
"· Nd ago" age suffix on the badge — computed against the viewer's clock, not
baked in at render time, so a report reopened weeks later shows its true age
instead of looking permanently fresh. And every Individual's `opener` is
checked against its own `evidence` (not the live page) and flagged with
`opener_grounding_note` if it invents specifics the evidence doesn't
support — a softer, separate signal from `verification_tier` that doesn't
fail the run, since openers legitimately paraphrase. See CHANGELOG.

## 7. Portfolio mode — shipped, opt-in once 2+ products exist

`scripts/portfolio_merge.py` cross-references saved reports from multiple
products, grouping prospects that share an exact `source_url` or normalized
name and surfacing only those appearing in 2+ products — e.g. a person or
company relevant to more than one product, worth one shared outreach
conversation. Wired as SKILL.md step 9. Only offer this once a user has run
signal-scout against a second product with saved snapshots (per the storage
convention) — it's meaningless with a single product's data.

As of 2026-07-16, each product argument accepts a glob (e.g.
`outputs/<slug>/analysis-*.json`) matching every snapshot saved for that
product, not just one file — cross-referencing then runs against that
product's full cumulative history (reusing item 3's `accumulate_history()`),
so a prospect dropped from product A's latest run still surfaces if it's
currently live in product B's. Single-file-per-product usage still works
unchanged. See CHANGELOG.

## 8. Repeat-usage tracking — shipped, maintainer-facing only

`scripts/usage_stats.py` reads the `outputs/<slug>/analysis-<date>.json`
storage convention (item 3's prerequisite) and reports how many products get
re-run, how often, and the average gap — entirely local, no telemetry. Not
part of the agent workflow; a separate, manually-invoked check.

## 9. MCP server (agent-to-agent interface) — v0 scaffold

`mcp-server/` wraps the research workflow as callable tools
(`find_first_customers`, `classify_and_score`) for other agents to call
directly, instead of only a human invoking the skill inside Claude Code. See
`mcp-server/README.md` for setup and what's tested vs. not. Calls are
metered locally to `usage.jsonl` only, with a global daily call cap.
