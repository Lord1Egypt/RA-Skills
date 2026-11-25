# Macro scan checklist

Walk every section, in this order, before naming any ticker. Each line is a
short dated fact with a source. "Nothing new" is a valid entry. Target: one
screen of facts, not an essay.

## 1. Central banks and rates
- Policy rates and the next meeting dates (Fed, ECB, BoJ, BoE, PBoC, plus the
  user's home central bank from `sources.toml`)
- Market-implied path (futures / OIS) vs. guidance; any change this week
- 2y and 10y yields, curve shape, real yields

## 2. Inflation, growth, labour
- Latest CPI/PCE, PMIs, jobs data, GDP nowcasts; surprise vs. consensus
- Upcoming releases inside the next 2 weeks (date + time in user timezone)

## 3. Credit and liquidity
- IG/HY spreads, funding stress signals, bank lending, central bank balance sheets
- Dollar index and the user's base currency vs. USD

## 4. Market structure and positioning
- Index breadth, concentration (top-10 weight), equal-weight vs. cap-weight
- Volatility (VIX/MOVE), skew, put/call
- Positioning / flows if available (CFTC, fund flows, retail activity)
- Valuation ranges for the main indices and sectors

## 5. Earnings and sectors
- Earnings season stage, revisions trend, sector leadership over 1w / 1m / 3m

## 6. China and other large economies
- Growth data, policy measures, property, credit impulse, currency
- Any region configured in `sources.toml` (`[scan].extra_regions`)

## 7. Commodities
- Oil, gas, metals, agriculture: price, curve, inventories, supply events

## 8. Geopolitics and policy
- Conflicts, sanctions, tariffs, elections, fiscal deadlines
- For each: what the market already prices, and the next decision point

## 9. User-configured sources
- Read each source in `sources.toml` `[[sources]]` (newsletters, channels,
  broker research). Summarise, do not quote at length. Note the author's bias
  if known (a broker's research desk sells products; a channel may have a
  house view).

## 10. Calendar
- Merge all dated events from sections 1 to 9 into one list for the next
  2 weeks, in the user's timezone.

## Output of the scan
A dated list grouped by section, then a calendar, then **one line**: "What the
loudest story of the week is, and how much space it got in this scan."
