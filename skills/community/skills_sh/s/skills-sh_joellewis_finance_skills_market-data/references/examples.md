# Market Data — Worked Examples

Cost figures below reflect 2024-2025 list pricing; verify current pricing with vendors and exchanges before budgeting.

## Contents

1. [Example 1: Market Data Infrastructure for a Mid-Size RIA](#example-1-market-data-infrastructure-for-a-mid-size-ria)
2. [Example 2: Market Data for an Electronic Trading Platform](#example-2-market-data-for-an-electronic-trading-platform)
3. [Example 3: Entitlement Management and Exchange Licensing Compliance](#example-3-entitlement-management-and-exchange-licensing-compliance)

### Example 1: Market Data Infrastructure for a Mid-Size RIA

**Scenario:** A $2B RIA with 3,000 client accounts needs: real-time quotes for 15 portfolio
managers/traders, delayed data for 40 client service associates, EOD data for portfolio
accounting and performance, historical data for research, and a client portal with current
market values.

**Data level assessment:** Level 1 is sufficient. The firm places client orders, not market
making or HFT. This significantly reduces cost and infrastructure complexity.

**Vendor evaluation:**

| Option | Est. Annual Cost | Key Trade-off |
|---|---|---|
| Bloomberg (15 Terminals + Data License) | $375K-$425K | Deep analytics but expensive per-terminal model |
| Refinitiv Eikon (15 seats) + DataScope | $200K-$275K | Lower cost but smaller user community |
| FactSet (15 seats) + EOD package | $150K-$225K | Flexible pricing, strong API, less real-time trading depth |

FactSet offers the best balance for this firm: real-time quotes and screening for portfolio
managers, historical data and factor tools for research, and API access for internal systems.

**Client portal data strategy:** Real-time redistribution would add $100K-$200K/year in
exchange fees for 3,000 non-professional users. The firm selects 15-minute delayed data,
eliminating redistribution fees and clearly labeling prices as delayed.

**Exchange licensing:** 15 professional users for real-time Level 1. 40 associates on delayed
data (no exchange license). Client portal on delayed data (no redistribution fees). One
administrator handles monthly subscriber reporting through the vendor.

**Analysis:** Total cost of approximately $175K-$250K vs $400K+ for Bloomberg-centric.
The architecture separates real-time (licensed professionals) from delayed (everyone else),
minimizing licensing complexity. Annual vendor reviews and usage audits ensure compliance.

### Example 2: Market Data for an Electronic Trading Platform

**Scenario:** A broker-dealer building an institutional equity platform with real-time
market data display, smart order routing, execution algorithms (TWAP, VWAP), and post-trade
TCA. Must balance latency, completeness, cost, and Reg NMS compliance.

**The firm needs both SIP and direct feeds:** SIP provides the authoritative NBBO for best
execution compliance. Direct feeds from major exchanges provide the per-exchange depth that
smart order routing and algorithms require.

**Feed selection:** Direct feeds from NYSE Arca, Nasdaq TotalView (ITCH), NYSE (Pillar),
Cboe BZX/EDGX (PITCH), and IEX DEEP — covering the majority of volume. Lower-volume
exchanges added later if routing analysis indicates missed liquidity.

**Ticker plant design:** (1) Feed handlers per exchange with kernel bypass networking,
(2) NBBO calculator comparing internal NBBO against SIP for validation, (3) Book builder
maintaining per-exchange and consolidated order books, (4) Pub-sub publishing layer with
full-rate feeds for algorithms and conflated feeds for client displays, (5) Historical
capture for TCA, regulatory records, and strategy research.

**Redistribution licensing:** Displaying real-time data to institutional clients requires
redistribution agreements with each exchange, monthly professional user reporting, and
per-user fees — or enterprise redistribution pricing if economical.

**Analysis:** Total market data cost is substantial: direct feeds ($300K-$500K/year),
SIP ($50K-$100K/year), ticker plant build ($200K-$400K initial), redistribution fees
($100K-$500K/year). Market data is one of the largest operating costs for an electronic
platform. Budget for annual exchange fee increases.

### Example 3: Entitlement Management and Exchange Licensing Compliance

**Scenario:** A 200-employee multi-strategy hedge fund (New York, London, Hong Kong)
receives an NYSE audit notification. Subscriber counts have been estimated rather than
tracked, and the fund is uncertain whether its risk system's use of NYSE pricing
constitutes non-display use.

**Data consumption inventory:** The fund catalogs all NYSE data consumers: (1) Display
users — every Bloomberg Terminal, Eikon desktop, and internal dashboard showing NYSE
real-time data. Result: 120 professional display users found vs 95 previously reported.
(2) Non-display applications — algorithmic trading, risk (VaR/Greeks), portfolio valuation,
OMS, pricing engines. Result: 8 unreported non-display applications identified.
(3) Derived data — a daily position file with NYSE closing prices sent to the prime broker
requires review against NYSE's derived data policy.

**Remediation:** File amended subscriber reports (expect back-billing). Register non-display
applications by category (A: trading, B: internal non-trading, C: derived/redistribution).
Deploy an entitlement management platform (Bloomberg SSEOMS, Refinitiv DACS, or dedicated
tools like TRG Screen). Establish provisioning/deprovisioning policies. Automate monthly
subscriber count generation and reconciliation.

**Financial exposure:**

| Gap | Estimated Back-Billing |
|---|---|
| Display under-reporting (25 users x 12 months) | $75K-$150K |
| Non-display applications (8, some Category A) | $200K-$500K |
| Potential redistribution (1 flow under review) | $0-$100K |
| **Total exposure** | **$275K-$750K** |

**Analysis:** Remediation cost ($100K-$200K for entitlement system + ongoing administration)
is modest vs audit exposure. Market data entitlement management must be a formal compliance
function. Conduct internal audits annually before exchanges audit externally.

