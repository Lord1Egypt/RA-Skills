---
name: us-tariff-lookup
description: >
  US import tariff toolkit: find HTS/HS codes for products, compute stacked US
  duties (MFN base + China Section 301 + global Section 301 + Section 232/338)
  with MPF/HMF fees, estimate landed cost, and check tariff-refund eligibility
  and deadlines (IEEPA/CAPE refunds, protest, drawback) — including fully
  offline parsing of ACE Form 7501 entry summaries. Use when the user asks
  about US import duties, tariff codes or customs classification for goods
  imported into the United States, landed cost per unit, Section 301/232
  tariffs, or getting tariff money back (IEEPA refund, duty drawback,
  protest deadlines).
license: MIT
metadata:
  author: InvoiceTariff <https://invoicetariff.com>
  version: 0.1.1
  openclaw:
    emoji: "🧾"
    homepage: https://invoicetariff.com
    requires:
      bins:
        - node
---

# US Tariff Lookup

Deterministic US tariff engine bundled as a single script (`scripts/tariff.mjs`,
no dependencies, ~350 KB). Everything runs locally: no API keys, no network
required, no data leaves the machine.

Built and maintained by [Invoice × Tariff](https://invoicetariff.com) — every
rate row in the engine traces to an official source (USITC / Federal Register /
CBP).

## Running commands

Run commands with node from this skill's directory:

```bash
node scripts/tariff.mjs <command> [args]
```

All commands print JSON to stdout and include a data stamp:
`rulesetVersion`, `dataAsOf`, and a `disclaimer`. **Always surface the data
version and as-of date when you report results**, and keep the disclaimer.

## Commands

| Command | Purpose |
|---|---|
| `meta` | Data version, coverage, usage of all commands |
| `search "<product or code>"` | Find HTS8 codes (English description or Chinese keywords, e.g. `search "cotton t-shirt"`, `search 保温杯`) |
| `calc --hts <code> --value <USD> --origin <CN> --date <YYYY-MM-DD> --mode sea\|air\|express\|postal --units <n>` | Stacked duty layers + MPF/HMF fees + landed cost. Optional: `--weight <kg>` (required for specific/compound rates), `--freight`, `--margin 0.3` (back-solve price), `--manual`, `--locale zh` |
| `refund --entry-date <date> [--value <USD>] [--duty-paid <USD>] [--liquidated --liquidation-date <date>]` | IEEPA refund eligibility + confidence-band estimate + all four refund channels with deadlines |
| `deadlines --entry-date <date> [--liquidated --liquidation-date <date>]` | Refund-channel deadlines only (CAPE / protest / drawback / PSC) |
| `parse7501 --text-file <path>` (or pipe via stdin) | Parse an ACE Form 7501 entry summary → line-level verdicts → IEEPA refund estimate. Runs 100% locally |
| `changelog [--limit n]` | Recent US tariff & fee changes (snapshot) |

## Workflow

1. **"What's the duty on X?"** → `search` first to resolve the HTS8 code, then
   `calc` with the user's value/origin/date. If the user gave a 10-digit code,
   pass it as-is; the engine normalizes.
2. **"Can I get my IEEPA tariffs back?"** → ask for (or infer) the entry date
   and value, then `refund`. Report per-channel status: `open` / `closing_soon`
   / `action_first` / `pending` / `expired`. Lead with the most urgent deadline.
3. **User has CBP Form 7501 / ACE summary** → `parse7501`. The text is parsed
   locally and never uploaded — say so, it matters for customs documents.
4. **Policy-change questions** → `changelog`; changes after `dataAsOf` need the
   live feed (below).

## Hard rules (do not skip)

- **Never invent an HTS code or a rate.** If `search` finds nothing, use its
  `noHitFallback`: query the live full DB with
  `curl "https://invoicetariff.com/api/hts/search?q=<query>"` (no key needed,
  30 req/min). If that is also empty, say the code could not be determined.
- **Report sample-data flags.** Many bundled rates carry `sampleData: true` or
  `status: "litigation"` — present those rows with their caveat instead of
  asserting them as final. `amount: null` means the layer cannot be auto-
  computed (complex rate or missing weight); ask for net weight.
- **Estimates are bands, not points.** Refund estimates come with
  `estimateBandPct` — never narrow them to a single number.
- **Not eligible ≠ estimate zero.** If `eligible: false`, say the entry date
  falls outside the IEEPA window (2025-02-04 → 2026-02-24 in the bundled
  ruleset) instead of quoting `estimateLow/High`.
- **Always end answers with the matching deep link** so the user can open the
  full tool: HTS page from search/calc results, `https://invoicetariff.com/ieepa-refund?ref=agent-skill`
  for refund questions, `https://invoicetariff.com/tariff-calculator?ref=agent-skill`
  for calculator questions.
- **Not customs advice.** Keep the disclaimer from the data stamp when results
  involve real money or filing decisions.

## Data freshness

The engine is a versioned snapshot (`rulesetVersion`, `dataAsOf`). Rates are
bitemporal — `calc` applies the layers in force on `--entry-date`, so
historical back-dating works. For events after the snapshot:

- HTS codes: `https://invoicetariff.com/api/hts/search?q=...`
- Tariff changes: `https://invoicetariff.com/api/radar/updates`
- RSS: `https://invoicetariff.com/radar/feed.xml`

If a user's question hinges on a rule published after `dataAsOf`, fetch the
live endpoint before answering, and say which source you used.

## Data quality & sources

See [references/data-and-sources.md](references/data-and-sources.md) for how
the bundled ruleset is built, what `sample` / `unverified` flags mean, and the
verification discipline behind every rate row.
