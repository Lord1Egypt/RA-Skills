# Korea equities overlay

Read [equity-common.md](equity-common.md) first. The universe boundary, the fund-versus-basket
redundancy test, the cash-management exclusion and the rule about regressing against the theme
rather than the index are the same in every equity market. What follows is what is true here and
is not true elsewhere.

## Identity

- One venue, `KRX`, covering both KOSPI and KOSDAQ. Codes are six digits.
- Preferred lines (`005935`) are the same economic asset as their common line. Hold the common one and audit the preferred as `duplicate_asset` unless the preferred is the liquid line, which does happen.

## What this market is

Semiconductors at 4.0 is the heaviest single weight in any shipped table, and it is not an opinion: two memory makers are most of what this index does. A universe that spreads its slots evenly here is not observing Korea.

The battery chain is its own theme under materials rather than being filed with chemicals, and shipbuilding is its own group. Both are cyclical complexes with their own order books.

Entertainment and music is a level-1 theme. The listed agencies are a real export sector here and nowhere else in the table.

Managed care leaves Light: national health insurance means there is no listed insurer to observe. Everything else in this table is unusually dense — thirty-five themes reachable at Light against a target of fifty-five, in the historical sizing scheme; current coverage comes from the reviewed economic plan.

## Adverse flags

This market's regime issues these, and no other market's does. They cost the same as any
universal flag; what is market-specific is the vocabulary, not the price.

| Code | What it is |
|---|---|
| `administrative_issue` | 관리종목 — designated an administrative issue by KRX |
| `investment_alert` | Under an investment caution, warning or risk designation |
| `trading_halt_review` | Halted pending a listing eligibility review |

## Size

Research the leader/necessary-peer roster and declare four entity ceilings in `coverage_plan`.
Reference instruments are additional. Medium covers most reviewed leaders; Heavy protects the
full necessary backbone; Max adds at least 30% sourced Beta following that Heavy's distribution.
Starter theme levels/weights do not set current member quotas.

## Example

Open [KR Medium](../../examples/kr-medium/build-spec.json) and its
[research review](../../examples/kr-medium/research-review.json). Business review and reused
listing/price facts retain their separate dates; see [example limits](../../examples/README.md).

## Suggested live fields

Beyond the ones in equity-common.md:

- Administrative issue (관리종목) designation and the reason for it.
- Investment alert tier — 주의 / 경고 / 위험 are three different states, not one.
- Foreign ownership limit and current foreign holding, which caps the marginal buyer.

## Report language

English is always generated, with a Korean companion by default. Write researched names
and brief reasons in Korean, with authored `report_translations.en` for human content.
`--language` chooses the companion language without changing membership or facts.
