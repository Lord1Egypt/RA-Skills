# Euronext Paris equities overlay

Read [equity-common.md](equity-common.md) first. The universe boundary, the fund-versus-basket
redundancy test, the cash-management exclusion and the rule about regressing against the theme
rather than the index are the same in every equity market. What follows is what is true here and
is not true elsewhere.

## Identity

- **The one real limitation of this overlay.** TradingView's `EURONEXT` venue code covers Paris, Amsterdam, Brussels, Lisbon and Dublin, so the venue prefix cannot tell you which of them a line trades on. The identity rule cannot enforce the boundary; the research has to. Restrict candidates to Paris-listed issuers and cite the listing for each one.
- Symbols are one to five characters.

## What this market is

Luxury at 4.0. Four names carry a quarter of this index and a universe that gives them the same shelf as utilities is not observing France.

Aerospace and defence at 2.5 is the second theme, and construction-concession is promoted to level 1 — Vinci, Bouygues and Eiffage are toll roads and airports as much as they are builders.

No megacap platform theme and no AI compute theme. They are dropped.

Autos come up to Light. Paris lists Stellantis, Renault, Michelin and Valeo, and treating the sector as German-only would leave four of the larger CAC names unobserved. Cybersecurity leaves Light in the same edit: the listed French cyber names are growth-market microcaps.

## Adverse flags

This market's regime issues these, and no other market's does. They cost the same as any
universal flag; what is market-specific is the vocabulary, not the price.

| Code | What it is |
|---|---|
| `amf_injunction` | Subject to an AMF injunction |
| `tender_offer_period` | In a public tender offer period |
| `transfer_to_growth` | Transferring to Euronext Growth |

## Size

Research the leader/necessary-peer roster and declare four entity ceilings in `coverage_plan`.
Reference instruments are additional. Medium covers most reviewed leaders; Heavy protects the
full necessary backbone; Max adds at least 30% sourced Beta following that Heavy's distribution.
Starter theme levels/weights do not set current member quotas.

## Example

No dedicated current example ships for this market. Use the closest
[worked Medium example](../../examples/README.md), then research this market under the overlay above.

## Suggested live fields

Beyond the ones in equity-common.md:

- AMF offer-period and injunction filings.
- Euronext compartment and any transfer to Euronext Growth, which changes the disclosure regime.

## Report language

The report is written in French by default, so write the snapshot in French
too — names, `l1_name`, reasons and measurement methods. `--language en` overrides the report
and changes nothing else about the build.
