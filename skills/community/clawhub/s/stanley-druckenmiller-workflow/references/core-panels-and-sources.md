# Core Panels and Sources

Purpose: keep one compact reference for the V1/VNext panel hierarchy, key indicators, and practical source mapping.

Use this file when maintaining the skill, refining the data layer, or checking whether a panel belongs in the daily engine, weekly engine, or monthly background layer.

## 1) Product scope

This workflow is a first-layer macro environment engine.
It helps with:
- liquidity
- rates
- credit
- FX
- breadth / internal structure
- A-share transmission
- U.S. and China macro-to-execution translation

It does not replace second-layer execution judgment:
- exact asset
- exact level
- exact size
- discretionary trading nuance

## 2) Daily engine: required layers

### U.S. core
Use these as the default P0 daily stack:
- Fed net liquidity
- ON RRP balance
- 2s10s
- 3m10y
- 10Y TIPS real yield
- HY OAS
- DXY / dollar proxy
- USDJPY
- WTI
- VIX
- 10Y nominal yield
- IWM / SPY
- RSP / SPY
- KRE / SPY
- SPHB / SPLV

### A-share core
Use these as the default P0 daily stack:
- USDCNY or USDCNH
- northbound flow or valid proxy
- CSI300 vs CSI1000
- ChiNext vs CSI300
- breadth and turnover
- China liquidity anchor (DR007 or Shibor)
- China rates curve proxy
- property leader basket
- joint-stock banks vs big state banks
- HK / offshore China confirmation

## 3) Weekly / monthly extensions

### Weekly U.S.
Useful confirmation layer:
- initial jobless claims
- 5Y5Y or breakeven inflation
- EPS revision momentum
- broader breadth metrics
- housing / consumer high-frequency set
- thematic ETF flow proxies
- IG / CCC / EMB stress proxies

### Weekly China
Useful confirmation layer:
- DR007 / Shibor persistence
- China 10Y-1Y curve proxy
- credit impulse proxy
- property high-frequency sales
- HK China assets confirmation

### Monthly background
Use for slower regime calibration:
- QT progress
- financial conditions index
- ISM / PMI decomposition
- NFIB / business confidence
- China monthly credit impulse
- China property investment and sales
- global PMI split
- SLOOS

## 4) A-share transmission additions

### Internal structure
Most important A-share daily reads:
- CSI300 vs CSI1000
- ChiNext vs CSI300
- breadth
- turnover
- northbound continuity

### Flow / who is buying
Prefer:
- northbound day + continuity
- margin financing change
- style / sector destination when available
- ETF style flow as confirm, not thesis anchor

Daily stabilization rule:
- if northbound truth is unavailable or upstream values are clearly invalid, replace it with a northbound proxy built from Stock Connect breadth, style relative strength, and offshore China-beta confirmation
- do not keep northbound truth as a routine daily hard gap if the proxy is available

### Sector / single-name baskets
Use baskets, not isolated names:
- property
- joint-stock banks vs big state banks
- brokers
- machinery
- transport / logistics
- heavy-truck proxy
- premium consumer vs mass consumer
- credit-sensitive basket

Daily proxy policy:
- use these baskets to build both credit-risk proxy and industry-expression proxy when direct truth series are unstable
- do not block the daily memo waiting for exact industry net-flow truth
- treat true daily industry net-flow as enhancement, not hard dependency

### Preferred A-share second-order chains
Always try to include at least one explicit chain, for example:
- external FX constraint
  -> threshold for foreign capital to return changes
  -> northbound continuity changes
  -> broad-beta / small-cap / growth relative strength shifts
  -> sector expression rotates

- local liquidity change
  -> funding price changes
  -> valuation repair or only structural repair
  -> turnover and breadth either confirm or fail to confirm

- credit transmission change
  -> property / banks / credit-sensitive assets either confirm or fail to confirm
  -> cyclical leadership either becomes viable or does not

## 5) Domestic Demand / Real Economy Nowcast

### A-share / China side
Use a compressed daily format by default.

Default daily format:
- Housing: weak / stabilizing / improving
- Consumption: weak / mixed / improving
- Logistics / Trade: weak / mixed / improving
- Industrial Activity: weak / mixed / improving
- Composite Read: one sentence only

Expand the sub-blocks only when:
1. the underlying data has just updated,
2. the update changes the day’s thesis,
3. the market is explicitly trading this layer.

Preferred fields behind the compressed read:
- Housing: core-city second-hand viewings / listings, 30-city new home weekly sales area, land purchase / premium rate or construction proxy
- Consumption: CPCA passenger car sales, dealer inventory coefficient or premium consumption proxy, express delivery activity
- Logistics / Trade: SCFI, port throughput, freight / external demand proxy
- Industrial Activity: Daqin railway throughput, electricity usage, excavator domestic sales, steel production / steel price when available

Always end with:
- Domestic Demand Status: improving / mixed / weak
- implication for A-shares

### U.S. side
Use the same compact logic with local equivalents.
Do not require all blocks to be true daily-frequency series; stable latest-official weekly/monthly public series are acceptable if they can be fetched reliably on each daily run.

#### Housing
Default stable public core:
- 30Y mortgage rate (`MORTGAGE30US`)
- housing starts (`HOUST`)
- building permits (`PERMIT`)

Optional add-ons:
- mortgage applications
- new / existing home sales
- homebuilder sentiment

#### Consumption
Default stable public core:
- retail sales (`RSAFS`)
- total vehicle sales / SAAR (`TOTALSA`)
- real personal consumption expenditure (`PCEC96`) when available

Optional add-ons:
- card / restaurant / travel proxies

#### Logistics / Trade
Default stable public core:
- freight transportation services index (`TSIFRGHT`)

Optional add-ons:
- rail / truck / freight / shipping proxies

#### Industrial Activity
Default stable public core:
- industrial production (`INDPRO`)
- capacity utilization (`TCU`)
- durable goods new orders (`DGORDER`) when available

Optional add-ons:
- ISM new orders
- capex / machinery / energy demand proxies

#### Fundamental Validation
Default stable public core:
- corporate profits after tax (`CP`)
- unit labor costs (`ULCNFB`)
- labor productivity (`OPHNFB`)
- valuation compatibility versus rates / real yields

Optional enhanced layer:
- public earnings season surprise summary
- public guidance / revisions summary when reliably accessible

Use this layer to answer:
- is the profitability backdrop improving, flat, or deteriorating?
- are margins under pressure?
- is productivity offsetting that pressure?
- is the move earnings-backed or just multiple expansion?

Always end with:
- Domestic Demand Status: improving / mixed / weak
- implication for U.S. equities

## 6) Practical source mapping

### U.S. / global
Use the best available mix of:
- FRED
- Yahoo or Stooq style market proxies
- official or widely used public sources

Key examples:
- Fed liquidity / rates / HY OAS / VIX / DXY: FRED preferred where possible
- index / ETF / FX / commodity proxies: Yahoo / Stooq fallback mix
- MOVE fallback: 10Y Treasury realized-volatility proxy from daily yield changes
- JPY vol fallback: USDJPY 20-day realized volatility
- earnings-revision breadth fallback: corporate profits + unit labor costs + productivity + sector relative-strength proxy

### A-shares / China
For now, it is acceptable to document the primary operational source simply as:
- akshare

When some fields are unavailable, acceptable fallbacks are:
- official webpages
- public reports / PDFs
- stable proxy indicators

### General rule
Do not hardcode data values in the skill.
The skill should define:
- what to fetch
- from where
- update cadence
- fallback or proxy
- downgrade behavior when unavailable

## 7) Data quality and downgrade rules

If data is incomplete:
- keep the memo alive
- explicitly name missing panels only when they are truly core and unfillable
- reduce confidence
- avoid fake precision
- use a proxy when the proxy preserves the transmission logic

Field status labels:
- ok
- stale
- proxy
- evidence insufficient

### Daily A-share stabilization rule
The daily A-share brief should not repeatedly surface the same structural missing items as hard gaps if stable proxies exist.

Apply these defaults:
- northbound net-buy truth -> northbound proxy
- property / LGFV spread truth -> credit-risk proxy in daily mode, true spread in weekly/monthly enhancement
- direct industry net-flow truth -> industry-expression proxy

Only report `Evidence Gaps` for missing P0 fields that do not have an acceptable stable proxy.
Do not report optional enhancement fields as daily gaps.

### Daily U.S. stabilization rule
The daily U.S. brief should not repeatedly surface the same structural missing items as hard gaps if stable proxies exist.

Apply these defaults:
- Europe breadth panel -> Europe breadth proxy
- MOVE -> Treasury realized-volatility proxy
- JPY 1M vol -> USDJPY 20d realized-volatility proxy
- daily sell-side revisions breadth -> downgrade to weekly/monthly enhancement and replace in daily mode with a public fundamental-validation proxy

Only report `Evidence Gaps` for missing P0 fields that do not have an acceptable stable proxy.
Do not report optional enhancement fields as daily gaps.

## 8) News validation

Use news validation as a verification layer, not as the regime engine.

Rules:
- build regime from transmission and market evidence first
- use news only to confirm, challenge, or explain the current thesis
- include 2-4 headlines max
- for each headline, state source, Supports / Conflicts / Noise, and one-line implication

### A-share source priority
1. Official / policy anchors
   - State Council / China gov portal / PBOC / CSRC / NDRC / NBS / MOF / MIIT / MOFCOM / Customs / NEA / exchanges
2. Market wires
   - CLS / Shanghai Securities News / China Securities Journal / Securities Times / Yicai
3. Sector verification
   - CRIC / Cih-index / Beike Research / CPCA / Shanghai Shipping Exchange / State Post Bureau / NEA / industry associations

### U.S. source priority
1. Core market / macro press
   - Bloomberg / Reuters / WSJ / FT / CNBC
2. Official / policy
   - Federal Reserve / Treasury / BLS / BEA / Census / CBOE
3. Broader narrative context
   - NYT / WaPo / AP / major sector press

Do not let a single headline override the transmission framework.

## 9) Output discipline

All final memos should preserve:
- conclusion first
- thesis before tape
- compact panels, then integrated read
- evidence anchors after the main memo
- explicit falsification
- no explicit trade orders

Use three reading layers:
1. decision layer
2. reasoning layer
3. evidence layer

## 10) Language resolution

Resolve language in this order:
1. explicit user instruction
2. account-level preference
3. current-session language habit
4. platform locale / Accept-Language
5. message-language detection

Rules:
- explicit instruction overrides everything
- session habit should not silently overwrite account-level preference
- if account preference and session habit conflict repeatedly, ask once and persist
- if ambiguity remains, default to the latest user message language
- keep analytical depth equivalent across languages
