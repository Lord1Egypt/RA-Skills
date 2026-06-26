# A-share Tape V1.1

Goal: build a Stan-style A-share tape using mostly free and reasonably stable data.

Principles:
- Keep the daily tape focused on what changes the regime read.
- Separate hard anchors from noisy confirmation signals.
- Prefer data that is free, repeatable, and can survive source changes with fallback.

## Tiering
- Core = should be in the V1 daily tape
- Confirm = useful confirmation layer
- Optional = helpful but noisy or fragile
- Avoid as core = do not let this drive the main thesis in V1

---

## 1) Internal Structure (Most Important)

| Indicator | Tier | Why it matters in Stan terms | Free source feasibility | Recommended sources | Notes |
|---|---|---|---|---|---|
| CSI300 vs CSI1000 | Core | China version of IWM/SPY; large vs small cap risk appetite | High | Tencent / Eastmoney / Yahoo proxies | Core breadth / risk-expansion read |
| ChiNext vs CSI300 | Core | Growth vs core-beta proxy | High | Tencent / Eastmoney / Yahoo | Use for duration / growth appetite |
| STAR50 vs CSI300 | Confirm | Higher-beta innovation-board confirmation | Medium | Eastmoney / Tencent / AkShare proxies | Useful, not strictly required in V1 |
| Up/down stocks count | Core | Most direct breadth signal | Medium-High | Eastmoney / AkShare market breadth pages | Critical for diagnosing “index up but tape weak” |
| Total turnover (Shanghai + Shenzhen combined turnover) | Core | Shows whether repair has real participation | High | Eastmoney / Tencent / AkShare | Pair with breadth, not alone |
| Limit-up / limit-down counts | Optional | A-share emotion extreme gauge | Medium | Eastmoney / AkShare | Emotion layer only |

---

## 2) Flow / Who Is Buying

| Indicator | Tier | Why it matters | Free source feasibility | Recommended sources | Notes |
|---|---|---|---|---|---|
| Northbound net flow (single day) | Core | Best free foreign-flow proxy | High | Eastmoney / AkShare HSGT endpoints | Must be read with continuity, not as a single print |
| Northbound 3-day / 5-day continuity | Core | More Stan-like than one-day flow | High | Derived from the same northbound source | Prefer over raw daily number |
| Northbound sector destination | Confirm | Shows whether foreign money is buying banks / consumer / tech | Medium | Eastmoney / AkShare summaries | Great when available, not mandatory |
| Margin financing balance change | Confirm | Retail leverage temperature | Medium | Eastmoney / AkShare | Better as weekly / daily confirmation, not thesis anchor |
| Credit-risk proxy basket (property developers / brokers / small-cap beta) | Confirm | A-share substitute for weak-credit tape; shows whether risk capital is willing to own fragile balance sheets | Medium | Eastmoney sector quotes + selected names | Prefer basket or spread-style read over one stock |
| ETF subscriptions / redemptions | Confirm | Institutional demand for style buckets | Medium-Low | Fund issuer pages / Eastmoney | Good to add later |
| Main-force net inflow | Optional | Can help with sector heat | Medium-Low | Eastmoney / web scrape | High noise, not a core anchor |

---

## 3) Sector / Single-name Leaders

| Indicator | Tier | Why it matters | Free source feasibility | Recommended sources | Notes |
|---|---|---|---|---|---|
| Property leaders (Vanke / Poly / CMSK) | Core | China credit-transmission proxy | High | Tencent / Eastmoney quotes | Use as a group, not a single-stock story |
| Banks: joint-stock vs big state banks | Core | Asset-quality / credit-belief proxy | High | Tencent / Eastmoney quotes | Stronger than only watching the bank index |
| Brokers (Eastmoney / CITIC / sector index) | Confirm | A-share sentiment amplifier | High | Tencent / Eastmoney quotes | Must confirm with turnover + breadth |
| Construction machinery / cyclicals | Confirm | Real-demand / infrastructure lead indicator | High | Tencent / Eastmoney quotes | Good second-layer confirmation |
| Transport / logistics / ports / highways | Confirm | China version of transport tape; shows whether goods flow and industrial demand are broadening | High | Eastmoney sector quotes / Tencent quotes | Prefer basket read over one name |
| Commercial vehicles / heavy-truck proxy | Confirm | Best public proxy for truck tape in A-share style | Medium | Eastmoney / Tencent quotes on truck and auto-parts names | Use as a demand / credit proxy, not in isolation |
| Moutai vs broad consumer | Confirm | Premium demand vs mass demand split | High | Tencent / Eastmoney quotes | Helps identify demand stratification |
| Optional vs staple consumer split | Confirm | Tells whether the market is paying for discretionary recovery or hiding in defensive demand | High | Eastmoney consumer sector quotes / ETF proxies | Useful when consumer is central to the thesis |

---

## 4) China Liquidity / Policy Layer

| Indicator | Tier | Why it matters | Free source feasibility | Recommended sources | Notes |
|---|---|---|---|---|---|
| DR007 | Core | China equivalent of daily funding stress / ease | Medium | AkShare / interbank sources | Critical when a stable source exists |
| Shibor 1W | Core | Simple local funding anchor | High | Shibor official / AkShare / web sources | Good free substitute if DR007 lags |
| China 10Y yield | Core | Local duration / macro-pricing anchor | Medium-High | ChinaBond / AkShare / public yield sources | Daily or latest usable |
| China 10Y-1Y curve slope | Core | Recovery pricing vs disbelief | Medium | Derived from China yields | Strong macro-weather anchor |
| OMO net injection | Confirm | Shows whether PBoC is actively smoothing | Medium | PBoC site / summaries | Good desk-color input |
| MLF / LPR changes | Confirm | Important policy-shift markers | High | Official releases | Event-driven, not daily necessity |

---

## 5) External Constraint Layer

| Indicator | Tier | Why it matters | Free source feasibility | Recommended sources | Notes |
|---|---|---|---|---|---|
| USDCNY / USDCNH | Core | Most important external valuation constraint | High | Yahoo / Tencent FX / Stooq proxy | Must be in V1 |
| CN-US 10Y spread | Confirm | External capital-pressure / FX-pressure read | Medium | Derived from China 10Y + UST 10Y | Strong if stable China yield feed exists |
| HK China assets (HSCEI / FXI / KWEB) | Core | External confirmation of China beta | High | Yahoo / Tencent / Eastmoney / Stooq | Confirmation, not thesis by itself |
| Copper vs property chain | Confirm | Real-demand validity test | Medium | SHFE copper / proxies + property leaders | Helps filter fake reflation |
| VIX / iVIX | Confirm | Global panic vs local panic split | Medium | VIX free; iVIX availability varies | Optional in V1 if the local source is unstable |

---

## Recommended V1 A-share Daily Tape

### Core anchors (must have)
1. CSI300 vs CSI1000
2. ChiNext vs CSI300
3. Up/down counts
4. Total turnover
5. Northbound flow (day + 3d/5d continuity)
6. USDCNY / USDCNH
7. DR007 or Shibor 1W
8. China 10Y and 10Y-1Y slope
9. Property leader basket
10. Joint-stock banks vs big state banks
11. HK China assets confirmation (FXI / KWEB / HSCEI)

### Confirmation layer
12. Brokers + turnover confirmation
13. Construction machinery / cyclicals
14. Transport / logistics / heavy-truck proxy basket
15. Moutai vs broad consumer
16. Optional vs staple consumer split
17. Credit-risk proxy basket (property / brokers / fragile beta)
18. OMO / MLF / LPR event markers
19. Margin financing balance change
20. Copper vs property chain

### Optional / emotion layer
21. Limit-up / limit-down counts
22. Main-force net inflow
23. ETF subscriptions / redemptions

---

## Preferred A-share Second-order Chains

Use at least one explicit transmission chain in every A-share morning brief.

### Template A: FX constraint chain
Stronger dollar / USDCNY staying elevated
-> lower threshold for foreign capital to stay cautious
-> weaker northbound continuity
-> broad-beta and small-cap growth fail to get incremental confirmation
-> the market falls back to “certainty first,” where Moutai and offshore China leaders tend to outperform CSI1000-style beta.

### Template B: Local liquidity chain
Shibor / FR007 declines
-> local funding becomes cheaper
-> growth valuations repair first
-> if turnover and breadth do not confirm
-> it is only structural repair, not broad market diffusion.

### Template C: Credit transmission chain
Policy support / pro-property messaging appears
-> first check property stocks and banks
-> then check property sales, development investment, and credit structure
-> if bonds and credit do not confirm
-> equities are only trading expectation, not genuine expansion.

---

## How to Read It in Stan Style

### If these align, upgrade toward “diffusion repair”
- USDCNY stable to stronger CNY
- Northbound flow positive and persistent
- CSI1000 and ChiNext outperform CSI300
- Breadth improves together with turnover
- Joint-stock banks and property leaders stabilize together

### If these align, stay in “structural divergence”
- Index is stable but breadth is weak
- Large caps hold while small caps lag
- Northbound is inconsistent
- HK China confirms only partially
- Local funding is stable but credit-sensitive sectors do not follow
- Property / transport / mass-consumer / weak-credit proxies fail to confirm the headline move

### If these align, downgrade toward “defense / contraction”
- USDCNY weakens sharply
- Northbound turns persistently negative
- CSI1000 / ChiNext lose leadership
- Breadth deteriorates despite index resilience
- Joint-stock banks and property leaders underperform again

---

## Honest V1 Boundary

Even with a stronger A-share tape, this workflow still does not replace:
- intraday tape feel in specific leaders
- transcript nuance and company-guidance interpretation
- execution decisions: exact name, exact level, exact size

Use this tape to standardize first-layer environment judgment.
Leave second-layer execution to the human.
