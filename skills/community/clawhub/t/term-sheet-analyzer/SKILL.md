---
name: term-sheet-analyzer
description: >
  Analyze startup financing term sheets: SAFEs, convertible notes, and priced equity rounds.
  Decode economic terms, flag founder-unfriendly clauses, model dilution impact, calculate
  effective pre/post-money valuations, and compare multiple competing term sheets side-by-side.
  Outputs plain-language risk summary plus structured dilution scenarios. Use when a founder,
  CFO, or investor receives a term sheet and needs to understand its real economic and control
  implications before signing.
  NOT for: legal advice or drafting legal documents (refer to counsel), cap table management
  (use cap-table-manager skill), token sale structures (use erc20-tokenomics-builder), or
  post-close equity administration.
version: 1.0.0
author: PrecisionLedger
tags:
  - finance
  - startups
  - term-sheets
  - fundraising
  - SAFEs
  - convertible-notes
  - venture
---

# Term Sheet Analyzer Skill

Decode the real economics and control implications of any startup financing term sheet. This skill guides Sam Ledger through parsing SAFEs, convertible notes, and priced rounds — translating legal language into numbers, identifying red flags, and producing a founder-ready risk summary.

---

## When to Use This Skill

**Trigger phrases:**
- "Analyze this term sheet"
- "What does this SAFE actually mean?"
- "Is this a good deal?"
- "How much dilution am I taking?"
- "Compare these two term sheets"
- "What's the post-money valuation cap?"
- "Explain these liquidation preferences"
- "Flag any founder-unfriendly terms"
- "Investor sent a convertible note, what should I know?"

**NOT for:**
- Drafting or redlining legal documents → engage startup counsel
- Post-close cap table management → use `cap-table-manager`
- Token sale / SAFT structures → use `erc20-tokenomics-builder`
- Public company securities analysis → different regulatory framework
- Personal investment advice → not a licensed advisor

---

## Instrument Types

### 1. SAFE (Simple Agreement for Future Equity)

YC's standard instrument. Four variants:

| SAFE Type | Valuation Cap | Discount | Notes |
|---|---|---|---|
| Cap Only | ✅ Yes | ❌ No | Most common at pre-seed |
| Discount Only | ❌ No | ✅ Yes (typically 15-20%) | Less common |
| Cap + Discount | ✅ Yes | ✅ Yes | Investor gets better of the two |
| MFN (Most Favored Nation) | ❌ No | ❌ No | Converts at best future SAFE terms |

**Key SAFE economics:**

```
Conversion Price (Cap-based):
  = Valuation Cap / (Fully Diluted Shares at Qualified Financing)

Conversion Price (Discount-based):
  = Priced Round Price × (1 - Discount Rate)

Investor uses whichever price is LOWER (better for investor)

Example:
  SAFE amount: $100,000
  Valuation cap: $5,000,000
  Priced round: Series A at $10M pre-money, $2.00/share
  
  Cap price: $5M / 5,000,000 shares = $1.00/share
  Discount price (20%): $2.00 × 0.80 = $1.60/share
  
  Investor converts at $1.00/share (cap wins)
  Shares received: $100,000 / $1.00 = 100,000 shares
```

**Post-Money SAFE (YC standard post-2018):**
- Cap is post-money (includes SAFE investment itself)
- Ownership % is locked: Investment ÷ Cap = ownership
- Example: $200k on $5M post-money cap = 4.0% ownership (guaranteed)

**Pre-Money SAFE (older, less common):**
- Cap is pre-money; actual dilution depends on total SAFE stack and option pool
- Riskier for founders: SAFE stack + option pool refresh can cause severe dilution

---

### 2. Convertible Note

Debt instrument that converts to equity. Key terms to extract:

```
Principal Amount:     $[X]
Interest Rate:        [Y]% per annum (simple or compound)
Maturity Date:        [Z months] from issuance
Conversion Discount:  [D]% off priced round price
Valuation Cap:        $[C] (pre-money or post-money — MUST clarify)
Conversion Trigger:   Qualified Financing ≥ $[threshold]
Repayment:            At maturity if no conversion (cash or equity)
```

**Interest accrual impact on dilution:**

```
Example:
  Principal: $500,000
  Rate: 6% simple
  Issued: Jan 2025, Converts: Jan 2026 (12 months)
  
  Accrued interest: $500,000 × 6% = $30,000
  Principal + Interest at conversion: $530,000
  
  Converting at $1.00/share → 530,000 shares (not 500,000)
  Extra dilution from interest: 30,000 shares
```

**Note vs SAFE comparison:**

| Factor | SAFE | Convertible Note |
|---|---|---|
| Debt on balance sheet | ❌ No | ✅ Yes |
| Interest accrual | ❌ No | ✅ Yes |
| Maturity / repayment risk | ❌ No | ✅ Yes |
| Complexity | Lower | Higher |
| Investor preference | Simpler rounds | Bridge rounds |

---

### 3. Priced Equity Round

Most complex. Key terms to extract and analyze:

```
Pre-Money Valuation:     $[X]
Investment Amount:       $[Y]
Post-Money Valuation:    $[X + Y]
Price Per Share:         $[P] = Pre-Money / Pre-Round Fully Diluted Shares
Share Class:             Series [A/B/C] Preferred
Liquidation Preference:  [1x / 2x] [participating / non-participating]
Anti-Dilution:           [broad-based weighted average / narrow-based / full ratchet]
Pro-Rata Rights:         [Yes / No] — right to invest in future rounds
Board Seats:             [Lead investor gets X seats]
Option Pool:             [%] — pre-money or post-money?
Drag-Along:              [threshold %]
Information Rights:      [quarterly/annual financials]
```

---

## Red Flag Checklist

Run every term sheet through this checklist:

### 🔴 High Risk — Negotiate Hard
- [ ] **Full ratchet anti-dilution** — investor gets repriced to lowest future price; massively penalizes founders in a down round
- [ ] **Participating preferred with no cap** — investor gets liquidation preference PLUS pro-rata equity proceeds (double-dipping forever)
- [ ] **2x+ liquidation preference** — investor gets 2× their money before anyone else
- [ ] **Option pool pre-money and large (>20%)** — effective valuation is lower than stated; dilutes founders only
- [ ] **Pay-to-play without notice** — converts investors to common if they don't follow-on; can be weaponized
- [ ] **Exclusivity >30 days** — locks founder out of talking to other investors too long
- [ ] **No-shop clause with damages** — creates liability if founder walks away

### 🟡 Medium Risk — Understand the Implications
- [ ] **Broad-based weighted average anti-dilution** — standard but still dilutes founders in down rounds
- [ ] **Non-participating preferred** — investor converts to common at IPO/acquisition; usually acceptable
- [ ] **1x liquidation preference non-participating** — standard, fine
- [ ] **Pro-rata rights (major investor)** — investor can maintain ownership %; usually reasonable
- [ ] **Information rights (quarterly)** — standard; just operationally overhead
- [ ] **ROFR on secondary sales** — company/investors get first right to buy shares; limits founder liquidity
- [ ] **Drag-along at low threshold (<50%)** — can force sale without founder approval

### 🟢 Standard / Founder-Friendly
- [ ] 1x liquidation preference non-participating
- [ ] Broad-based weighted average anti-dilution
- [ ] Post-money SAFE with reasonable cap
- [ ] Board composition: 2 founders, 1 investor, 2 independents
- [ ] Option pool created post-money
- [ ] Pro-rata rights for major investors only (≥ $X invested)
- [ ] 12-month exclusivity max

---

## Dilution Modeling

### SAFE Dilution Scenario

```
Inputs:
  Pre-round shares outstanding: 8,000,000
  Option pool pre-round: 1,000,000 (reserved)
  Fully diluted pre-round: 9,000,000
  
  SAFE 1: $250,000 at $4M post-money cap → ownership = 250k/4M = 6.25%
  SAFE 2: $150,000 at $6M post-money cap → ownership = 150k/6M = 2.5%
  
  Total SAFE dilution: 8.75% of post-SAFE, post-financing cap

Series A comes in at $10M pre-money, $4M raise:
  Post-money: $14M
  New option pool: 1,500,000 shares (10% post-money, created pre-money = dilutes founders)
  
  SAFE 1 converts at $4M cap:
    Shares = 6.25% × total post-money shares
  SAFE 2 converts at $6M cap:
    Shares = 2.5% × total post-money shares
  Series A investors: $4M / Series A price per share
  
Output cap table:
  Founders: [X]%
  SAFE 1 investor: 6.25%
  SAFE 2 investor: 2.5%
  Series A investors: [Y]%
  Option pool: 10%
  Total: 100%
```

### Effective Valuation Check

When a pre-money option pool shuffle is present:

```
Stated pre-money: $8,000,000
Option pool to create (pre-money): 1,500,000 shares at Series A price
Series A price: $8M / 8,000,000 pre-round shares = $1.00/share

Option pool cost: 1,500,000 × $1.00 = $1,500,000 (borne by founders)
Effective pre-money valuation founders receive: $8M - $1.5M = $6.5M

⚠️ Always model the "founder effective valuation" — it's often 15-25% lower than stated.
```

---

## Competing Term Sheet Comparison

When multiple term sheets are provided, produce a side-by-side comparison:

```
                        Term Sheet A        Term Sheet B
Investor:               Acme Ventures       Beta Capital
Pre-Money Valuation:    $8,000,000          $10,000,000
Investment:             $2,000,000          $2,500,000
Post-Money:             $10,000,000         $12,500,000
Founder ownership post: 68.2%               72.1%
Liquidation Pref:       1x non-part.        1x participating (cap 3x)
Anti-Dilution:          Broad WA            Full ratchet ⚠️
Option Pool:            10% post-money      15% pre-money ⚠️
Board:                  2F / 1I / 2I        2F / 2I / 1I
Pro-Rata:               Yes (major)         Yes (all)
Exclusivity:            30 days             45 days ⚠️
---
Red Flags:              0                   3 ⚠️
Recommended:            ✅ Term Sheet A     ❌ Proceed with caution
```

**Economic comparison at exit:**

```
Exit at $50M (acquisition):

Term Sheet A (1x non-participating):
  Investor: $2M preference, then converts to equity
  At $50M: investor converts (equity > preference)
  Investor share: 20% × $50M = $10M
  Founders + team: $40M

Term Sheet B (1x participating, 3x cap):
  Investor takes $2.5M preference first
  Remaining: $47.5M split pro-rata
  Investor: $2.5M + (20% × $47.5M) = $2.5M + $9.5M = $12M
  Founders + team: $38M

Difference: $2M less to founders at $50M exit from participating preferred.
At 2x cap ($5M), participating preference triggers cap and converts. Above cap, behaves like non-participating.
```

---

## Plain Language Translation Examples

**Legal text:** *"The Company shall maintain a fully diluted option pool of no less than 20% of the outstanding capital stock of the Company calculated on a post-financing basis, which pool shall be created prior to the closing of the financing."*

**Translation:** You must create a 20% option pool *before* this round closes. That means it comes out of your pre-money valuation, not the investor's. If your pre-money is $8M with 8M shares, you'll need to add ~2M new shares for the pool at closing, reducing your effective per-share pre-money valuation. Your founders' ownership % drops immediately. **This is the option pool shuffle — negotiate to have the pool created post-money instead.**

---

**Legal text:** *"In the event of a Liquidation Event, the holders of Series A Preferred Stock shall be entitled to receive, prior and in preference to any distribution to the holders of Common Stock, an amount per share equal to two times (2x) the Original Issue Price plus all accrued and unpaid dividends."*

**Translation:** If the company is sold, investors get 2× their money back before you see a dollar. On a $2M investment, that's $4M off the top. If the exit is $5M, investors get $4M, founders split $1M. **This is a 2× liquidation preference — above market and founder-unfriendly. Standard is 1×.**

---

## Step-by-Step Workflow

### Step 1: Extract Key Terms
If a document is provided (PDF/text), parse out all economic and control terms using the term checklists above. If missing, ask:
- What instrument type? (SAFE, note, priced round)
- What are the economic terms? (amount, cap, discount, preference)
- What are the control terms? (board seats, pro-rata, drag-along)

### Step 2: Run Red Flag Checklist
Flag every term against the 🔴/🟡/🟢 checklist. Assign risk level.

### Step 3: Model Dilution
Calculate founder ownership % post-transaction and at key exit scenarios ($10M, $25M, $50M, $100M).

### Step 4: Produce Plain-Language Summary
One page max:
- What is this deal at a glance?
- What are the 3 most important things to understand?
- What should be negotiated?
- What's the recommendation?

### Step 5: Compare (if multiple sheets)
Side-by-side table + economic comparison at exit scenarios.

---

## Output Templates

### Quick Summary (1-pager)

```
TERM SHEET ANALYSIS
Company: [Name] | Date: [Date] | Analyst: Sam Ledger

DEAL SUMMARY
  Instrument: Post-Money SAFE
  Amount: $250,000
  Valuation Cap: $4,000,000 (post-money)
  Your implied ownership: 6.25%

RED FLAGS: 0 (clean term sheet)
YELLOW FLAGS: 1 — pro-rata rights for investor

KEY TERMS
  ✅ Post-money cap (ownership locked)
  ✅ No discount clause
  ✅ Standard YC MFN provision: No
  🟡 Pro-rata rights: Yes (investor can follow-on)

DILUTION AT SERIES A ($10M pre, $2M raise):
  Your ownership: ~52% (assuming 15% option pool, $750k total SAFEs)
  SAFE investor: ~6.0% (post-money cap math)
  Series A: ~16.7%
  Option pool: 15%

RECOMMENDATION:
  This is a standard, founder-friendly SAFE. No material changes needed.
  Confirm: post-money cap (not pre). Check MFN if issuing multiple SAFEs.
```

---

## Integration Points

- **`cap-table-manager`** — build full cap table post-conversion
- **`startup-financial-model`** — model how new funding extends runway
- **`investor-memo-generator`** — produce the investor memo that accompanies this raise
- **`due-diligence-dataroom`** — organize diligence materials investors request at term sheet stage
- **`crypto-tax-agent`** — tax implications of SAFE/equity conversion events

---

## Reference: Key Terms Glossary

```
Pre-money valuation:    Company value BEFORE new investment
Post-money valuation:   Pre-money + investment amount
Fully diluted shares:   All shares including options, warrants, convertibles
Liquidation preference: Amount investors get before common stockholders at exit
Participating preferred: Investors get preference AND pro-rata equity (double-dip)
Anti-dilution:          Adjusts investor price if future round is lower (down round)
Full ratchet:           Investor price drops to lowest future round price (harsh)
Broad-based WA:         Weighted average adjustment — more founder-friendly
Option pool shuffle:    Creating option pool pre-money to inflate stated valuation
Pro-rata rights:        Right to invest in future rounds to maintain ownership %
Drag-along:             Majority can force all shareholders to approve a sale
ROFR:                   Right of First Refusal — company/investors buy shares first
SAFE:                   Simple Agreement for Future Equity (YC standard instrument)
Qualified financing:    The trigger event that converts SAFEs/notes (typically ≥$1M raise)
MFN SAFE:               Most Favored Nation — converts at best terms of future SAFEs issued
```
