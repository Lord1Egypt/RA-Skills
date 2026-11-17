# UK equities overlay

Read [equity-common.md](equity-common.md) first. The universe boundary, the fund-versus-basket
redundancy test, the cash-management exclusion and the rule about regressing against the theme
rather than the index are the same in every equity market. What follows is what is true here and
is not true elsewhere.

## Identity

- One venue, `LSE`. Symbols are two to six characters and may carry a dot.
- Prices quote in pence for most lines and in pounds for a few. Whatever you use, say which in `measurement.method` — a turnover figure that is silently 100x wrong ranks the whole universe wrong.
- Verify each current listing before binding a dual-listed company. Build the requested market's
  verified line; an old venue code is not evidence that it still trades.

## What this market is

The starter table emphasizes pharma, oil majors, miners and staples. Many London-listed
businesses earn internationally; research their actual operations rather than treating listing
country as revenue geography. Current economic-plan weights are separate from display defaults.

There is no megacap platform theme and no AI infrastructure. They are dropped, not weighted down.

Closed-end investment trusts are their own group. They are a large, liquid part of this market with no equivalent anywhere else in the table, and they are gauges rather than operating companies.

Semiconductors are weighted to what London actually lists rather than to what the sector is worth globally — Arm is in New York, and pretending otherwise would hand a heavy weight to a theme with one mid-cap in it. Managed care leaves Light: the NHS is not a listed sector.

## Adverse flags

This market's regime issues these, and no other market's does. They cost the same as any
universal flag; what is market-specific is the vocabulary, not the price.

| Code | What it is |
|---|---|
| `cancellation_notice` | Has given notice of cancellation of its listing |
| `listing_category_transfer` | Transferring between listing categories |
| `offer_period` | In an offer period under the Takeover Code |

## Size

Research the leader/necessary-peer roster and declare four entity ceilings in `coverage_plan`.
Reference instruments are additional. Medium covers most reviewed leaders; Heavy protects the
full necessary backbone; Max adds at least 30% sourced Beta following that Heavy's distribution.
Starter theme levels/weights do not set current member quotas.

## Example

Open [UK Medium](../../examples/uk-medium/build-spec.json) and its
[research review](../../examples/uk-medium/research-review.json). The dated snapshot includes
reviewed operating representatives, GBP-normalized turnover and separate ETF references;
its declared scope is not an exhaustive leadership census or a Beta bench.

## Suggested live fields

Beyond the ones in equity-common.md:

- Takeover Code offer period status — a published, dated state, not a rumour.
- Listing category (Equity Shares Commercial Companies and its transitions).
- Investment trust discount or premium to NAV, where the member is a trust.

## Report language

The report is written in English by default, so write the snapshot in English
too — names, `l1_name`, reasons and measurement methods. `--language en` overrides the report
and changes nothing else about the build.
