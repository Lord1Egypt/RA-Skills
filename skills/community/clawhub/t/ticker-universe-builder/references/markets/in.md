# India equities overlay

Read [equity-common.md](equity-common.md) first. The universe boundary, the fund-versus-basket
redundancy test, the cash-management exclusion and the rule about regressing against the theme
rather than the index are the same in every equity market. What follows is what is true here and
is not true elsewhere.

## Identity

- Two venues, `NSE` and `BSE`, and the same company lists on both. They are one economic asset: the venue is not part of identity, so pick the line with the real turnover — almost always NSE — and put the other in the audit as `duplicate_asset`.
- Symbols are alphanumeric and may carry `&` or `-` (`NSE:M&M`, `NSE:BAJAJ-AUTO`).

## What this market is

Banks and IT services are the two heaviest themes at 3.0. The IT services theme is promoted from level 2 in the base to level 1 here, because the Indian export-services complex is a primary theme and not a support sector.

There is no listed semiconductor complex, so `10_B` and `10_C` are dropped rather than weighted down. A theme with no eligible member fails the build, which is the correct outcome — it is better than a table that quietly promises coverage it cannot give.

NBFCs and housing finance are their own group. Treating them as banks is the mistake that makes every Indian financials universe look like five copies of one balance sheet.

Megacap platforms and the AI-infrastructure group leave the table: the platform layer is mostly private here and what is listed files under IT services, while the AI build-out is observed through the power complex. A theme with nothing to put in it would invent coverage instead of researching it.

## Adverse flags

This market's regime issues these, and no other market's does. They cost the same as any
universal flag; what is market-specific is the vocabulary, not the price.

| Code | What it is |
|---|---|
| `asm_surveillance` | Under the exchange's Additional Surveillance Measure |
| `gsm_surveillance` | Under the Graded Surveillance Measure |
| `promoter_pledge` | A material share of the promoter holding is pledged |

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

- ASM and GSM surveillance stage — the exchange publishes it and it changes weekly.
- Promoter pledge percentage from the quarterly shareholding pattern.
- F&O eligibility, which is the practical liquidity floor for a large-cap universe.

## Report language

The report is written in English by default, so write the snapshot in English
too — names, `l1_name`, reasons and measurement methods. `--language en` overrides the report
and changes nothing else about the build.
