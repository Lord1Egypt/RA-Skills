# Exchange Connectivity — Worked Examples

## Contents

1. Example 1: Designing FIX Connectivity to Multiple Execution Venues for a Broker-Dealer
2. Example 2: Building a Market Data Infrastructure with Consolidated and Direct Feeds
3. Example 3: Implementing Trading Halt Handling Across Order Management and Market Data Systems

### Example 1: Designing FIX Connectivity to Multiple Execution Venues for a Broker-Dealer

**Scenario:** A broker-dealer is building an order routing system to connect to five U.S. equity execution venues: NYSE, Nasdaq, Cboe BZX, Cboe EDGX, and IEX. The firm needs to support smart order routing across these venues and must comply with SEC Rule 15c3-5 market access requirements.

**Connectivity Architecture Decisions:**

The firm must decide between FIX and proprietary protocols for each venue. For an initial build, FIX is the pragmatic choice across all five venues — it provides a uniform interface, simplifies development, and reduces the number of protocol implementations to maintain. If the firm later requires sub-millisecond latency, it can add proprietary protocol gateways (OUCH for Nasdaq, BOE for Cboe, Pillar binary for NYSE) for latency-sensitive flow while keeping FIX for less time-sensitive order types.

**Session Layout:**
- Two FIX sessions per venue (primary and backup) — 10 sessions total. Primary sessions route through one extranet (e.g., TNS); backup sessions route through a second (e.g., IPC).
- Separate SenderCompIDs for each session. The firm applies for market participant identifiers and FIX credentials with each exchange.
- Heartbeat interval: 30 seconds for all order sessions.
- Sequence number persistence: sequence numbers stored to disk (using a journaling database or flat file with fsync), enabling session recovery without resetting after an application restart.

**Pre-Trade Risk Controls (Rule 15c3-5):**
The firm implements a risk gateway between the smart order router and the exchange FIX sessions. Every order passes through the risk gateway before reaching the exchange. Controls include:
- **Price collar:** Reject orders with a limit price more than 10% away from the NBBO for liquid securities (Tier 1) or 20% for less liquid securities (Tier 2).
- **Order size limit:** Reject single orders exceeding a configurable maximum (e.g., 50,000 shares for most equities). The maximum is adjustable by security based on average daily volume.
- **Position/capital exposure limit:** Track net exposure per symbol and in aggregate. Reject orders that would breach the per-symbol or aggregate capital limit.
- **Duplicative order detection:** Flag and reject orders that match a recently submitted order on symbol, side, quantity, and price within a configurable time window (e.g., 1 second).
- **Kill switch:** A firm-wide kill switch that cancels all open orders across all venues and prevents new order submission. Triggered manually by risk management or automatically when aggregate exposure exceeds an emergency threshold.
- **Restricted security list:** Halt-restricted and firm-restricted securities are blocked before reaching the exchange.

**Operational Procedures:**
- **Morning startup:** FIX sessions are connected at 7:00 AM ET. Sequence numbers are synchronized via ResendRequest if there is a gap from the prior session. The risk gateway is initialized with current position data from the overnight batch. Pre-market orders are accepted starting at 7:30 AM ET.
- **Intraday monitoring:** Operations staff monitors FIX session status, heartbeat health, and latency metrics on a real-time dashboard. Alerts fire if a session disconnects, if latency exceeds 5 ms, or if the backup session has not been tested in the last 30 days.
- **End of day:** After post-market order entry closes (5:00 PM ET), the firm reconciles all fills across venues against the internal blotter. Sequence numbers are persisted. Drop-copy sessions (separate read-only FIX sessions that receive a copy of all execution reports) are used to cross-check that no fills were missed on the primary sessions.

### Example 2: Building a Market Data Infrastructure with Consolidated and Direct Feeds

**Scenario:** An institutional broker-dealer is building market data infrastructure to support its algorithmic trading desk and its best execution analysis function. The algorithmic desk requires the lowest available latency for real-time trading decisions. The best execution team requires a consolidated view for transaction cost analysis. The firm trades U.S. equities listed on NYSE and Nasdaq.

**Feed Architecture:**

For the algorithmic desk, the firm subscribes to direct feeds from each exchange:
- Nasdaq TotalView-ITCH (Level 3, order-by-order) — provides the full Nasdaq order book.
- NYSE Integrated Feed via Pillar — provides depth-of-book data for NYSE-listed securities.
- Cboe PITCH feeds for BZX, BYX, EDGX, EDGA — provides order-by-order data for Cboe venues.
- IEX DEEP — provides price-level aggregated depth for IEX.

These direct feeds are received at the firm's co-location presence in both the Nasdaq/Carteret data center and the NYSE/Mahwah data center. The firm runs a feed handler process for each exchange protocol that decodes the binary messages and publishes normalized market data events to an internal messaging bus.

For the best execution team, the firm subscribes to the SIP consolidated feeds:
- CTA/CQS (for NYSE-listed securities) — provides consolidated NBBO and last sale.
- UTP (for Nasdaq-listed securities) — provides consolidated NBBO and last sale.

The SIP feeds serve as the regulatory reference for NBBO and are used in transaction cost analysis to measure execution quality against the prevailing NBBO at the time of each order.

**Normalization Layer:**
A market data normalization service consumes the output of all feed handlers and produces a unified internal representation:
- Each security is identified by the firm's internal security ID (mapped from exchange-specific symbology via the security master).
- All prices are represented in decimal format with a common precision.
- Timestamps are normalized to nanosecond UTC, preserving the original exchange timestamp and adding the firm's receipt timestamp.
- The normalization service constructs a "direct NBBO" by comparing the top-of-book from each direct feed, providing a synthetic NBBO that is typically available several hundred microseconds before the SIP NBBO.
- Book state is maintained for each venue, and an aggregated book across venues is available for algorithms that need full market depth.

**Redundancy:**
- Each direct feed has a primary and backup line (exchanges offer "A" and "B" feed instances with identical content sent over separate network paths). The feed handler arbitrates between the two lines, using the first-arriving copy of each message and filling gaps from the other.
- The SIP feeds are similarly dual-redundant.
- If a direct feed is lost entirely (both A and B lines), the system falls back to the SIP for that venue's contribution to the NBBO, and the algorithmic desk is alerted that venue-specific depth is unavailable.

**Performance Monitoring:**
- Feed handler latency is measured as the time between the exchange-timestamped event and the firm's internal publish timestamp. Target: under 10 microseconds from feed receipt to internal publish for co-located feed handlers.
- Gap detection: each feed handler tracks sequence numbers and alerts on gaps. Gaps on market data feeds (unlike FIX order sessions) typically cannot be recovered in real time — the data is simply missed and the book must be reconstructed from the next snapshot or full book refresh.
- Throughput monitoring: during peak message rates (e.g., market open, high-volatility events), the system monitors queue depths and processing backlogs to detect capacity issues before they cause data loss.

### Example 3: Implementing Trading Halt Handling Across Order Management and Market Data Systems

**Scenario:** A broker-dealer's technology team is implementing comprehensive halt handling across its order management system (OMS), smart order router (SOR), and market data platform. The firm must correctly handle market-wide circuit breakers, LULD trading pauses, and regulatory halts for individual securities.

**Detection Layer:**
Halt events are detected from multiple sources:
- **SIP administrative messages:** The SIP disseminates trading halt and resume messages (UTP and CTA halt/resume indicators). These are the authoritative source for regulatory halts and LULD trading pauses.
- **Direct exchange feeds:** Each exchange's proprietary feed includes halt and resume indicators specific to that venue.
- **LULD price band messages:** The SIP publishes LULD price bands (upper and lower limit prices) for each security. The market data platform consumes these bands and tracks limit state transitions.

The market data platform publishes halt events to the internal messaging bus with the following information: security identifier, halt type (MWCB Level 1/2/3, LULD pause, regulatory halt T1, regulatory halt T2, SEC suspension, exchange-specific), halt start time, affected venue(s) (all venues for MWCB and regulatory halts; specific venue for exchange-specific halts), and expected resume mechanism (auction, time-based, discretionary).

**OMS Halt Handling:**
When the OMS receives a halt event:
1. **Order acceptance:** New orders for the halted security are flagged. For regulatory halts and MWCB, new orders are rejected with a descriptive reason code ("Security halted — regulatory"). For LULD pauses, the firm may choose to queue orders for release when trading resumes or to reject them — the decision depends on the firm's policies and the order type.
2. **Open order management:** The OMS queries all open orders for the halted security across all venues. Depending on the halt type: some halts cause exchanges to cancel all resting orders (e.g., certain regulatory halts), some halts leave resting orders on the book (e.g., LULD pauses on some venues), and for halts that cancel resting orders, the OMS must update order status to "Canceled — halt" and notify the trader.
3. **Trader notification:** The OMS pushes halt alerts to trader workstations and the trading desk blotter, indicating the security, halt type, and estimated resume time (if available).
4. **Resume handling:** When a trading resume message is received, the OMS: releases any queued orders (if the firm's policy is to queue during halts), re-enables new order acceptance for the security, and alerts traders that trading has resumed.

**SOR Halt Handling:**
The smart order router maintains a real-time halt state table:
- Before routing any child order to a venue, the SOR checks the halt state table. If the security is halted at the target venue, the order is not sent.
- For LULD, the SOR checks the current price bands and rejects or adjusts orders with limit prices outside the bands.
- When trading resumes with a re-opening auction, the SOR may route auction-eligible orders (e.g., LOC or MOC orders) to the primary listing exchange for the reopening cross.

**Market-Wide Circuit Breaker Handling:**
A MWCB event is the most severe halt type. When a Level 1 or Level 2 MWCB triggers:
1. The market data platform detects the halt (via SIP or exchange messages) and publishes an all-securities halt event.
2. The OMS immediately suspends all order entry and flags all open orders. Exchanges will cancel resting orders.
3. The SOR stops routing. A firm-wide trading suspension is enforced.
4. The system starts a 15-minute countdown timer. Traders are shown the countdown on their workstations.
5. At resumption, exchanges conduct re-opening auctions. The OMS lifts the suspension and the SOR resumes routing.

For a Level 3 MWCB (20% decline), trading halts for the remainder of the day. The system marks the entire session as halted and prevents any further order activity.

**Testing and Validation:**
- The firm conducts quarterly halt-handling tests using simulated halt messages injected into the market data platform. Tests cover: single-security regulatory halt, LULD pause with re-opening auction, MWCB Level 1 with 15-minute pause, and MWCB Level 3 with end-of-day halt.
- Each test validates that: new orders are rejected or queued as expected, open orders are correctly managed, trader notifications are delivered, resume handling correctly re-enables trading, and all halt events are logged for CAT reporting.
