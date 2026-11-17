# Source Policy

This policy defines which sources can enter numeric consensus and how they are counted.

## Tiers

| Tier | Source type | Use |
| --- | --- | --- |
| A | Exchange or high-liquidity reference bookmaker with timestamped prices | Full numeric input |
| B | Mainstream sportsbook with timestamped prices | Full numeric input |
| C | Odds aggregator that exposes the underlying bookmaker and update time | Numeric input only after dedupe |
| D | Tip site, preview, social post, unattributed odds, or commentary | Context only; never numeric consensus |

Tip sites are excluded from consensus because they are not prices and do not provide independent market truth.

## Deduplication

- Count the underlying bookmaker, not the page that displays it.
- If the same bookmaker appears on multiple aggregators, count it once.
- Deduplicate by bookmaker, market, line, selection, and time bucket.
- Do not treat mirrored feeds, affiliate mirrors, or copied tables as new books.

## Freshness

- Use recency weight `1.0` for quotes under 15 minutes old, `0.9` for 15-60 minutes, `0.7` for 60-180 minutes, and `0.4` for older non-opening quotes.
- Quote freshness must always be shown with an explicit timestamp.
- Opening lines remain a separate snapshot and are never silently mixed into the current consensus.
- Stale quotes may be reported, but their age must be stated and their weight reduced.
- Near kickoff, a forecast with no usable quote inside 60 minutes must abstain.

## Source Counts

- Minimum usable independent bookmakers: three.
- Preferred independent bookmakers: five or more.
- If fewer than three independent books remain after dedupe, abstain from a market edge. A diagnostic or tactical summary may still be given if it is clearly labeled non-betting analysis.
- Report both raw source count and deduped bookmaker count.

## Starting Weights

- Tier A: `1.25`.
- Tier B: `1.0`.
- Tier C: `0.75` after underlying-bookmaker deduplication.
- Tier D: `0.0` for numeric consensus.
- A complete de-vigged market receives full completeness weight. An incomplete market receives at most half weight and cannot anchor the forecast.

These are transparent starting assumptions, not permanent claims about bookmaker quality. Change them only after at least 100 completed forecasts overall and 30 in the affected competition/market bucket.

## Unavailable Data

- Never invent missing prices or timestamps.
- If a book, market, or checkpoint is unavailable, say it is unavailable.
- If a requested checkpoint has no quote, do not relabel a nearby quote as that checkpoint.
- If only one market family is available, state that the forecast is partial.

## Current Consensus Inputs

Only these sources can move the numeric consensus:

- current bookmaker prices;
- underlying bookmaker prices reached through an aggregator;
- exchange/reference prices with timestamps.

Everything else is diagnostic or narrative support.

## Minimum Reporting Fields

Every usable quote should carry:

- source name;
- underlying bookmaker;
- market type;
- selection and line;
- odds format;
- quoted odds;
- timestamp with timezone;
- whether it belongs to opening or one of the comparison checkpoints.
