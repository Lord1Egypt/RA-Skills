# Data & Sources

How the bundled ruleset is produced, what the quality flags mean, and how to
verify any number this skill outputs.

## What's inside the bundle

`scripts/tariff.mjs` embeds a **versioned ruleset snapshot** compiled from the
Invoice × Tariff data pipeline:

| Dataset | Role |
|---|---|
| MFN seed | High-frequency HTS8 codes with USITC `general` column text (English + Chinese keywords) |
| China Section 301 | List 1–4A + review rates per code |
| Global Section 301 | Tier rates + caps + exclusions for 60 economies (FR 2026-15181) |
| Section 232 / 338 | Sector tariffs (steel/aluminum, autos, semiconductors, timber, …) with scope + mutual-exclusion groups |
| IEEPA historical layer | 2025-02-04 → 2026-02-24 fentanyl tariff (10%), retained for refund estimation |
| Fee schedules | MPF/HMF by fiscal year, informal (postal) fixed-fee tiers |
| Refund channel table | CAPE / protest / drawback / PSC windows, versioned separately |
| Changelog snapshot | Dated, sourced tariff-change entries |

The current bundle is `ruleset v0.3.1` (data as of 2026-09-19), refund table
`v0.1.0` (as of 2026-09-21). Run `tariff.mjs meta` to see the stamp of your
copy.

## Quality flags — read before quoting numbers

The engine carries its data-quality state on every row instead of hiding it:

- `sampleData: true` (search results) / `Sample rate` (calc layers): the number
  is structurally correct but pending **per-code verification against the
  USITC seed**. Present it as indicative.
- `status: "litigation"`: the layer is being challenged in court; CBP
  enforcement continues meanwhile. Report both facts.
- `unverified` scopes/tiers: boundary or tier digit not yet confirmed from the
  Federal Register original.
- Fee schedule FY2026 is verified; FY2027 values switch automatically on
  2026-10-01.

This discipline is deliberate: the site would rather show a flagged estimate
than a clean-looking wrong number. Keep the flags visible in your answers.

## Verification chain (why the numbers are traceable)

1. Rules are sourced from originals: USITC HTS reststop export, Federal
   Register documents (URLs included per row), CBP CSMS notices.
2. Every rate/deadline lives in the versioned JSON snapshot — zero hardcoded
   numbers in code.
3. Rule changes go through `FR original → versioned JSON bump → golden-case
   regression` before release; the version increments on every change.
4. Refund deadlines come from `data/refund-channels.json` (legal basis cited
   per channel: 19 U.S.C. § 1501 / § 1514 / § 1313, CBP CAPE guidance).

To verify any row yourself, follow the `source` URL printed in `calc` layer
output, or open the HTS page on the site (same engine, same snapshot, with
inline example calculations).

## Offline coverage & fallbacks

The offline MFN seed covers ~469 high-frequency HTS8 codes. The full DB
(~5,689 codes) is behind the live search endpoint:

```
curl "https://invoicetariff.com/api/hts/search?q=<query>"
```

- No API key; rate limit 30 req/min per IP; responses cached 5 min.
- `calc` only computes codes present in the offline seed. A full-DB code
  returns `HTS_NOT_FOUND` — in that case, link the user to
  `https://invoicetariff.com/tariff-calculator?ref=agent-skill` (same engine
  against the full library) instead of estimating by hand.

Tariff changes published after the snapshot date:

```
curl "https://invoicetariff.com/api/radar/updates"
```

## Updates

The snapshot is regenerated from the engine pipeline on every release — check
the repo for a newer tag, or compare `tariff.mjs meta → rulesetVersion`
against the version shown on [invoicetariff.com](https://invoicetariff.com).

## License

MIT for the code. The underlying rates are U.S. government data (HTS general
rates, Federal Register text); the snapshot's editorial layer (Chinese
keywords, curation, quality flags) is © Invoice × Tariff.
