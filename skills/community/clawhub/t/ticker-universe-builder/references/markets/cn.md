# CN overlay

Read [equity-common.md](equity-common.md) first: the universe boundary, the fund-versus-basket
redundancy test, the cash-management exclusion and the rule about regressing against the
theme rather than the index are the same in every equity market.

## Universe boundary

- Shanghai, Shenzhen and Beijing listings plus the indices and ETFs needed as gauges, all
  expressible in TradingView.
- A common share must have a confirmed six-digit code, the correct venue and a normal, tradable
  listing state.
- ST and \*ST names, delisting-transition names, long-halted names, names whose identity cannot be
  confirmed, and names without recent effective turnover are excluded by default.
- The venue is part of CN identity: `SSE:000001` and `SZSE:000001` are different instruments, so
  the default `asset_id` keeps the venue prefix.
- ETFs and single names are compared separately. ETFs carry structural gauges; single names carry
  company and supply-chain information.
- The report is written in Simplified Chinese, so write the snapshot in Simplified Chinese:
  `name` is the listed short name (`贵州茅台`, not `Kweichow Moutai`), and `l1_name`, `reason`
  and every `measurement.method` are Chinese prose. Theme codes and `theme_name` stay ASCII —
  they are identifiers that have to survive a TradingView import.

## Build focus

- Light is leader-only; Medium covers most reviewed leaders; Heavy completes all necessary
  leaders and differentiated peers before a small measured satellite tail. Max adds only
  qualified satellites to the same Heavy. Use the shared [coverage contract](../coverage-plan.md).
- Compare at the old Core's observation budget, and reconcile every original instrument.
  Recent heat, display-theme count and market-cap rank alone cannot define representation.
- Review nationwide/shareholding/regional banking, insurance types, power-generation business
  models, food/drink/retail branches and agriculture before optional semiconductor depth.
  Separate fibre/optical communications from grid equipment; multiple business lines need
  evidence for the chosen primary branch, not a keyword match.

## CN economic map

The starter preserves the legacy fine driver map: optical modules, servers/PCB, IDC, cooling and
power; equipment, materials, fabrication, packaging and chip functions; battery materials,
cells, equipment and storage; grid equipment versus power operations. Do not append a parallel
provider-industry taxonomy around these existing duties. Unmapped names require business
research into the same map, or an explicitly justified new durable theme.

Check mixed businesses before inheriting a section. The October 2026 review separates optical
fibre/network construction (`10_F`) from modules/components (`10_A`) and grid equipment
(`17_A`); EDA/IP (`11_I`) from enterprise software; and oilfield services (`21_D`) from
shipbuilding. Hengtong and Zhongtian can serve the fibre observation, but their substantial
power and submarine-cable businesses must remain disclosed. A chosen observation function is
not a claim about the largest revenue segment. Hengtong's
[2025 financial table](https://static.cninfo.com.cn/finalpage/2026-05-16/1225310932.PDF)
reports larger smart-grid than optical-communication revenue.

Other reviewed boundaries: [Yealink](https://static.cninfo.com.cn/finalpage/2026-04-22/1225142083.PDF)
supplies communication terminals, not general enterprise software;
[Empyrean](https://static.cninfo.com.cn/finalpage/2026-04-28/1225217315.PDF) supplies EDA;
[COSL](https://static.cninfo.com.cn/finalpage/2026-03-25/1225028515.PDF) supplies oilfield services.
These are dated research examples, not permanent ticker overrides in the selector.

Keep broad/style, sector and gold/duration gauges distinct from their stocks. A listed ETF may
stand in for an index observation only with a disclosed proxy reason. Quote activity and a clean
name string do not complete ST, halt, inquiry or issuer-quality checks. Policy news changes
research priority, not permanent membership without a durable industrial link.

## A size and turnover floor comes before any other judgement

Below a minimum fund size and daily turnover, the instrument's own price series is too noisy to
read a signal from — the spread alone moves the daily bar. Such a name is not "slightly worse
coverage", it is a **false sector anchor**: it will be quoted as if it represented its sector.

The only defensible exception is a theme's sole pure-play leader, and that exception is recorded
with its reason.

## Cash-management instruments

Short-term financing bond ETFs and money-market funds are excluded by instrument type. They post
the largest turnover in the entire ETF market, the tightest spreads and the best tracking, so every
quality ranking puts them first — which is exactly why the exclusion has to be written down rather
than left to whoever happens to be reviewing.

## Example

[`examples/cn-medium/`](../../examples/cn-medium/) contains a current coverage-first Medium
research snapshot, measured statistics, dated listing evidence, reports and script-generated watchlist.
Read [the scope and limitations](../../examples/README.md) before reusing it.

## Suggested live fields

- Listing, risk-warning and halt status.
- 20-day and 60-day turnover percentiles.
- 63 / 126 / 252-day beta, R² and downside beta against the theme's own ETF or theme leader.
- Relative return, max drawdown and residual volatility.
- The update time of sector, core-business and theme evidence.
