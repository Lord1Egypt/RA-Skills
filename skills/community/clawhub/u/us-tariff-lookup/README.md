# us-tariff-lookup

An [agent skill](https://code.claude.com/docs/en/skills) that gives any AI
agent a deterministic **US import tariff engine**: HTS/HS code search, stacked
duty calculation (MFN + Section 301/232/338), landed cost, and tariff-refund
eligibility with deadlines (IEEPA/CAPE, protest, drawback) — plus fully
offline parsing of CBP Form 7501 entry summaries.

One bundled script, zero dependencies, zero API keys, zero network calls.
Every rate row traces to an official source (USITC / Federal Register / CBP).

Maintained by [Invoice × Tariff](https://invoicetariff.com) — free in-browser
tariff & landed-cost calculators, commercial invoice generator, batch pricing,
and a sourced tariff-change radar in 7 languages.

## Install

**ClawHub** (any OpenClaw-compatible agent):

```bash
clawhub install us-tariff-lookup
```

Skill page: https://clawhub.ai/voltaudits/skills/us-tariff-lookup

**Claude Code / manual**

```bash
git clone https://github.com/voltaudits/us-tariff-lookup.git \
  ~/.claude/skills/us-tariff-lookup
```

**Other agents** — copy the `us-tariff-lookup/` folder into your agent's
skills directory. The only requirement is `node` (≥ 18) on PATH.

## What it can answer

- *"What's the HTS code and duty rate for knitted cotton t-shirts from
  China?"* → code `6109.10.00`, layered breakdown: MFN 16.5% + China 301
  (List 4A) 7.5% + global 301 12.5%, plus MPF/HMF, landed cost per unit.
- *"I paid IEEPA tariffs on a $20k entry in June 2025 — can I get that
  back, and by when?"* → eligibility (yes, window 2025-02-04 → 2026-02-24),
  refund band, and deadline-sorted channels: CAPE / protest / drawback / PSC.
- *"Here's my ACE 7501 summary — how much of this is refundable?"* →
  line-level parse + deterministic validation, 100% locally (nothing
  uploaded).
- *"What changed in US tariffs recently?"* → dated, sourced changelog
  snapshot + live update feed.

## Example

```bash
$ node scripts/tariff.mjs calc --hts 61091000 --value 10000 --origin CN \
    --date 2026-09-21 --mode sea --units 500 --weight 250 --freight 800

{
  "ok": true,
  "layers": [
    { "layer": "Base duty (MFN)",              "rate": "16.5%", "amount": 1650 },
    { "layer": "China Section 301 (List 4A)",  "rate": "7.5%",  "amount": 750  },
    { "layer": "Global Section 301 (CN, 12.5% tier)", "rate": "12.5%", "amount": 1250 }
  ],
  "fees": [ ... MPF $34.64, HMF $12.50 ... ],
  "totalDuty": 3697.14,
  "landedTotal": 14497.14,
  "effectiveTaxRatePct": 36.97
}
```

## Honesty features

Tariff numbers move money, so the skill is built to be quotable:

- Versioned ruleset (`rulesetVersion`, `dataAsOf`) stamped on every output —
  rates are bitemporal and historical back-dating works.
- Sample/unverified/litigation flags surface on the rows themselves instead of
  being hidden.
- Refund estimates are confidence bands, never single points; ineligible
  entries return `eligible: false` with the reason — never a made-up number.
- Unknown HTS codes return a structured error and a live-DB fallback — the
  skill never guesses.

Data quality & verification chain: see
[references/data-and-sources.md](references/data-and-sources.md).

## License

MIT. Underlying rates are U.S. government data; the curated snapshot
(Chinese keywords, quality flags) is © Invoice × Tariff.
