# Australia equities overlay

Read [equity-common.md](equity-common.md) first. The universe boundary, the fund-versus-basket
redundancy test, the cash-management exclusion and the rule about regressing against the theme
rather than the index are the same in every equity market. What follows is what is true here and
is not true elsewhere.

## Identity

- One venue, `ASX`. Symbols are three to six characters; three-letter codes are the norm.
- A dual-listed line shared with London is one economic asset across two markets.

## What this market is

Mining at 4.0 and banks at 3.0. This is a resource exchange with four banks attached, and the weights are the whole opinion of the table.

Medtech at 1.5 is the one theme that outgrew both — CSL, Cochlear and ResMed are a genuine export sector.

REITs at 1.5 rather than the base's 0.75: the listed property trusts are a large and liquid part of this index.

Semiconductors and cybersecurity leave Light: neither has a listed pure play here, and the technology that is listed is software and marketplaces. Mining at 4.0 is the point of this table, and the example shows it holding about a sixth of the universe.

## Adverse flags

This market's regime issues these, and no other market's does. They cost the same as any
universal flag; what is market-specific is the vocabulary, not the price.

| Code | What it is |
|---|---|
| `asx_price_query` | Has received an ASX price or volume query |
| `capital_raising_halt` | Halted for a capital raising |
| `voluntary_administration` | In voluntary administration |

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

- ASX price and volume query letters, and any response.
- Voluntary administration and trading halts around capital raisings, which are frequent here and are the main way a small line stops being tradable.

## Report language

The report is written in English by default, so write the snapshot in English
too — names, `l1_name`, reasons and measurement methods. `--language en` overrides the report
and changes nothing else about the build.
