# Margin Operations — Worked Examples

## Contents

1. Example 1: Calculating margin requirements and buying power for a diversified brokerage account
2. Example 2: Managing a margin call sequence from generation through resolution
3. Example 3: Evaluating portfolio margin benefits for an active options trader

### Example 1: Calculating margin requirements and buying power for a diversified brokerage account

**Given:** A client opens a new margin account and deposits $150,000 in cash. The client wants to build a diversified portfolio.

**Step 1 — Determine Reg T buying power:**
- Cash deposit: $150,000
- SMA: $150,000 (initial cash deposit establishes the SMA)
- Reg T buying power: $150,000 x 2 = **$300,000**

**Step 2 — Client purchases a diversified portfolio:**
- $120,000 in large-cap equity ETF (VTI)
- $60,000 in international equity ETF (VXUS)
- $40,000 in investment-grade bond ETF (BND)
- $30,000 in REIT ETF (VNQ)
- Total purchases: $250,000

**Step 3 — Post-purchase account status:**
- Market value: $250,000
- Debit balance: $250,000 - $150,000 = $100,000
- Account equity: $250,000 - $100,000 = $150,000
- Equity percentage: $150,000 / $250,000 = **60%** (above 50% Reg T requirement)
- Remaining SMA: $150,000 - ($250,000 x 50%) = $150,000 - $125,000 = $25,000
- Remaining buying power: $25,000 x 2 = **$50,000**

**Step 4 — Determine maintenance call trigger (assuming 30% house requirement):**
- House maintenance: 30%
- Call triggered when: equity / market value < 30%
- Equivalently: market value falls to debit balance / (1 - 0.30) = $100,000 / 0.70 = **$142,857**
- This represents a decline of ($250,000 - $142,857) / $250,000 = **42.9%** from current value

**Step 5 — Margin interest cost estimate:**
- Debit balance: $100,000
- Assume margin rate: broker call rate (6.50%, illustrative — actual rates vary with the rate environment) + 0.75% = 7.25%
- Annual interest: $100,000 x 7.25% = $7,250
- Monthly interest: approximately $604
- This cost must be offset by portfolio returns exceeding 7.25% (on the borrowed portion) to add value through leverage

**Step 6 — Impact of a 15% market decline:**
- New market value: $250,000 x 0.85 = $212,500
- Debit balance unchanged: $100,000
- New equity: $212,500 - $100,000 = $112,500
- Equity percentage: $112,500 / $212,500 = **52.9%** (still above 30% house requirement; no margin call)
- New SMA: remains at $25,000 (SMA is a high-water mark; does not decrease with market decline)

### Example 2: Managing a margin call sequence from generation through resolution

**Given:** An existing margin account with the following position prior to market decline:
- Market value: $400,000 (80% equities, 20% bonds)
- Debit balance: $160,000
- Equity: $240,000 (60%)
- House maintenance requirement: 35%

**Days 1-12 — progressive decline, no call:** Equities fall in stages (down 18%, 28%, 35%, then 45% cumulatively from the original $320,000; bonds drift down 5%), taking the equity percentage from 60% to 53.3%, 48.5%, 44.0%, and finally 36.5% on Day 12 — approaching but never breaching the 35% house requirement.

**Day 14 — Call triggered:**
- Equities down 48% total; bonds down 5%
- New equity market value: $320,000 x 0.52 = $166,400
- New bond market value: $76,000
- New total market value: $166,400 + $76,000 = $242,400
- Debit balance: $160,000
- New equity: $242,400 - $160,000 = $82,400
- Equity percentage: $82,400 / $242,400 = **34.0%** — **below 35% house requirement**
- **House margin call generated** at end of day

**Margin call amount calculation:**
- Required equity: 35% x $242,400 = $84,840
- Current equity: $82,400
- **Call amount: $84,840 - $82,400 = $2,440**

**Day 14 — Notification and communication:**
- Automated margin call alert sent via system notification and email
- Margin department places phone call to client
- Notification states: $2,440 due by Day 19 (T+5 business days)
- Options presented: deposit cash, deposit marginable securities (at loan value), or liquidate positions

**Day 16 — Client responds:**
- Client deposits $5,000 cash (exceeds call amount to provide buffer)
- New debit balance: $160,000 - $5,000 = $155,000
- Assuming market unchanged: equity = $242,400 - $155,000 = $87,400
- Equity percentage: $87,400 / $242,400 = **36.1%** (above 35%)
- **Margin call satisfied**

**Alternative resolution — Partial liquidation:**
- If client cannot deposit, sell $7,000 of bond ETF
- Proceeds reduce debit balance: $160,000 - $7,000 = $153,000
- New market value: $242,400 - $7,000 = $235,400
- New equity: $235,400 - $153,000 = $82,400
- Equity percentage: $82,400 / $235,400 = **35.0%** (at the requirement; call met but no buffer)
- Better approach: sell more to create a buffer above the requirement

### Example 3: Evaluating portfolio margin benefits for an active options trader

**Given:** An experienced options trader maintains the following portfolio:
- Account equity: $500,000
- Long 2,000 shares SPY at $450 = $900,000
- Long 20 SPY 420 puts (protective puts, 3-month expiry), premium paid $8 per contract = $16,000
- Short 20 SPY 480 calls (covered calls, 3-month expiry), premium received $5 per contract = $10,000
- Net portfolio delta: reduced from 2,000 to approximately 1,400 (hedged)

**Step 1 — Calculate Reg T margin requirement:**
Under Reg T, margin is calculated position-by-position:
- Long 2,000 shares SPY at $450: 50% initial margin = $450,000
- Long 20 SPY 420 puts: fully paid (no margin required; cost $16,000 already paid)
- Short 20 SPY 480 calls: covered by long shares (no additional margin required)
- **Total Reg T margin requirement: $450,000**
- Account equity: $500,000
- Excess equity: $500,000 - $450,000 = $50,000
- The protective puts and covered calls provide risk reduction, but Reg T does not recognize the hedge

**Step 2 — Calculate portfolio margin requirement:**
Under portfolio margin (OCC TIMS), the entire position is evaluated as a unit under stress scenarios:
- The key stress scenario is SPY -15% (worst case for this long-biased portfolio):
  - SPY drops from $450 to $382.50
  - Long stock loss: 2,000 x ($450 - $382.50) = -$135,000
  - Long 420 puts gain: puts move deep in-the-money; approximate gain: 20 x 100 x ($420 - $382.50 - $8) = +$59,000
  - Short 480 calls gain: calls expire worthless; gain: 20 x 100 x $5 = +$10,000
  - **Net portfolio loss under -15% stress: -$135,000 + $59,000 + $10,000 = -$66,000**
- Additional stress scenarios (+15%, +/-5%, +/-10%) produce smaller losses for this position
- **Portfolio margin requirement: approximately $66,000** (the largest loss across all scenarios)

**Step 3 — Compare Reg T vs portfolio margin:**

| Metric | Reg T | Portfolio Margin |
|--------|-------|-----------------|
| Margin requirement | $450,000 | $66,000 |
| Equity required | $450,000 | $66,000 |
| Excess equity | $50,000 | $434,000 |
| Additional buying power | $100,000 | $868,000 |
| Margin as % of market value | 50% | 7.3% |
| Leverage ratio | 1.8x | 13.6x (available, not necessarily used) |

**Step 4 — Assess the implications:**
- Portfolio margin reduces the requirement by **85%** because it recognizes the protective puts and covered calls as risk-reducing hedges
- The trader can deploy excess capital to additional strategies or maintain a larger cash buffer
- **Risk consideration:** The 13.6x available leverage is dangerous if fully utilized. The trader should maintain a self-imposed margin buffer well above the minimum — targeting no more than 50-60% utilization of portfolio margin capacity
- **Stress test beyond the model:** If SPY gaps down 25% overnight (beyond the 15% stress scenario), the portfolio loss would be approximately $100,000 — still within the $500,000 equity but illustrating that the OCC TIMS scenarios do not capture tail risk. The trader should run their own stress tests at more extreme levels
- **Qualification check:** The account meets the $100,000 minimum equity requirement. The trader must have appropriate options approval and complete the firm's portfolio margin agreement
