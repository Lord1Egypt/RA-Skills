# Canada equities overlay

Read [equity-common.md](equity-common.md) first. The universe boundary, the fund-versus-basket
redundancy test, the cash-management exclusion and the rule about regressing against the theme
rather than the index are the same in every equity market. What follows is what is true here and
is not true elsewhere.

## Identity

- Two venues, `TSX` and `TSXV`. They are different boards with different issuers, so a symbol on one is not the symbol on the other. Venture names rarely clear a large-cap liquidity floor; admit them deliberately or not at all.
- A company cross-listed in New York is one economic asset. Hold the Canadian line in a Canadian universe.

## What this market is

Banks at 3.5 — six of them are the index — then miners at 3.0 and the energy infrastructure complex at 2.5. Metals and mining and uranium are both promoted to level 1.

Digital-asset equities keep a level-1 seat here, which they do not get in most markets. Toronto actually lists them.

Technology is thin on purpose: one enterprise software theme, no semiconductors, no AI compute.

Semiconductors, payments and medtech leave Light: Toronto lists no semiconductor of scale, the payments names were taken private, and the medtech that remains is microcap. What is left is banks, energy, mining and a software cluster that is genuinely world-class.

## Adverse flags

This market's regime issues these, and no other market's does. They cost the same as any
universal flag; what is market-specific is the vocabulary, not the price.

| Code | What it is |
|---|---|
| `cease_trade_order` | Subject to a cease trade order |
| `delisting_review` | Under exchange delisting review |
| `management_cto` | Subject to a management cease trade order |

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

- Cease trade orders and management cease trade orders, published per province.
- For miners: reserve and resource statements, and which of the two a figure is.

## Report language

The report is written in English by default, so write the snapshot in English
too — names, `l1_name`, reasons and measurement methods. `--language en` overrides the report
and changes nothing else about the build.
