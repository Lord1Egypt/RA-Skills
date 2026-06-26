---
name: thetanuts
description: Trade crypto options on Thetanuts Finance - orderbook fills, RFQ lifecycle, multi-strike structures, real-time WebSocket, wallet management, early settlement, referrer fees
homepage: https://github.com/Thetanuts-Finance/thetanuts-sdk
user-invocable: true
metadata: {"openclaw":{"emoji":"📈","install":[{"type":"node","package":"."}]}}
---

## First-Time Setup (Onboarding Flow)

### Startup Checks

On a new conversation the agent should:

```
Step 1: Check wallet status (read-only, safe to run automatically)
   └─> node scripts/wallet-discover.js

Step 2: Interpret the result:
   - configured: false → Enter ONBOARDING MODE
   - configured: true  → Greet user with their address, proceed normally
```

### Updates (User-Initiated Only)

The agent must NEVER run `update.sh` automatically. Updates change code that signs
transactions, so they require explicit user consent each time.

When the user asks to check for or apply updates:
- Run `bash scripts/update.sh` and surface the full output to the user.
- If a new version is available, summarize the diff/changelog and ask the user
  to confirm before applying.
- If already up to date, say so explicitly. Do not run code-changing commands
  silently.

### Onboarding Mode (No Wallet Detected)

When no wallet is configured, guide the user through setup in this order:

```
No wallet detected
      │
      ▼
┌─────────────────────────────────────────┐
│ "Welcome to Thetanuts Options Trading!  │
│  Let's get you set up in 3 steps."      │
└─────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────┐
│ Step 1: Create or import a wallet       │
│ • New user → wallet-create.js           │
│ • Have a seed? → wallet-import.js       │
│                                         │
│ WARN: Use a DEDICATED wallet.           │
│ Never reuse your primary wallet seed.   │
│ Custody stays LOCAL on your machine.    │
└─────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────┐
│ Step 2: Verify & fund the wallet        │
│ • Run wallet-discover.js → show address │
│ • Run wallet-balance.js --chain         │
│   base-mainnet                          │
│ • If zero balance: explain funding      │
│   - Need ETH on Base for gas fees       │
│   - Need USDC for PUT trades            │
│   - Need WETH for CALL trades           │
│   - Bridge via bridge.base.org          │
└─────────────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────────────┐
│ Step 3: Market overview & first trade   │
│ • Fetch prices: get-prices.ts           │
│ • WebSearch for market news             │
│ • Ask risk preference (LOW/MED/HIGH)    │
│ • Show first strategy recommendation    │
└─────────────────────────────────────────┘
```

### Welcome Message (After Onboarding or Returning User)

Once wallet is configured, the agent MUST automatically:
1. Show wallet address and balances (run `wallet-discover.js` + `wallet-balance.js`)
2. Fetch current market prices (run `get-prices.ts`)
3. Show a brief market snapshot with available option types

Present this without the user asking:

```
Welcome to Thetanuts Options Trading!

Your wallet: 0x...
Chain: Base Mainnet
Balances: X ETH (gas) | Y USDC | Z WETH

Live Market:
• ETH: $X,XXX (24h: +X.X%)
• BTC: $XX,XXX (24h: +X.X%)

Available options: PUT, CALL, spreads, butterflies, condors

What would you like to do?
• "Show me ETH puts"      → View available strikes and prices
• "Recommend a strategy"  → I'll check market news and suggest based on your risk preference
• "Check my positions"    → View open trades and P&L on expired ones

New to options? Just say "teach me about options"
```

### Security Reminders (shown during onboarding)

- **DEDICATED WALLET**: Use a dedicated wallet seed for this integration. Never reuse your primary wallet.
- **LOCAL CUSTODY**: Your seed phrase stays on your machine. The agent never sends it anywhere.
- **TRANSACTIONS**: Irreversible once broadcast. Always verify before sending.
- **APPROVALS**: Token approvals allow contracts to spend your tokens. Only approve trusted contracts.
- **GAS**: Ensure wallet has ETH on Base for gas fees.
- **RFQ KEYS**: Back up `.thetanuts-keys/` directory — lost keys cannot decrypt past offers.

---

# Thetanuts Options Trading

## What is TNUT Agent?

TNUT Agent is your AI-powered assistant for trading crypto options on Thetanuts Finance.

**What it does:**
- Manages local wallets safely (custody stays on your machine)
- Accesses market intelligence (prices, orderbook, MM quotes)
- Inspects options and positions
- Prepares and executes trades through the Thetanuts protocol

**Local-first design:**
- Wallet custody stays LOCAL - your seed phrase never leaves your machine
- Signing stays LOCAL - transactions are signed on your device
- Backend provides intelligence, data, and routing support only

**Capabilities:**
| Category | What You Can Do |
|----------|----------------|
| Wallet | Create, import, check balances |
| Market Data | Live prices, MM quotes, orderbook orders |
| Trading | Fill orderbook orders, submit RFQs, approve tokens |
| Positions | View open positions, calculate payoffs |

---

## Options 101

### What are Options?

Options are contracts that give you the right (but not obligation) to buy or sell an asset at a specific price by a specific date.

### PUT Options

A **PUT** gives the holder the right to SELL at the strike price.

| Action | You... | Profit When | Risk |
|--------|--------|-------------|------|
| **Buy PUT** | Pay premium upfront | Price drops below strike | Lose premium if price stays up |
| **Sell PUT** | Receive premium | Price stays above strike | Lose if price drops below strike |

**Example:**
- ETH is at $2000
- You BUY a $1900 PUT for $10 premium
- If ETH drops to $1800 → Your PUT is worth $100 (profit: $90)
- If ETH stays at $2000 → Your PUT expires worthless (loss: $10 premium)

### CALL Options

A **CALL** gives the holder the right to BUY at the strike price.

| Action | You... | Profit When | Risk |
|--------|--------|-------------|------|
| **Buy CALL** | Pay premium upfront | Price rises above strike | Lose premium if price stays down |
| **Sell CALL** | Receive premium | Price stays below strike | Lose if price rises above strike |

**Example:**
- ETH is at $2000
- You BUY a $2100 CALL for $15 premium
- If ETH rises to $2300 → Your CALL is worth $200 (profit: $185)
- If ETH stays at $2000 → Your CALL expires worthless (loss: $15 premium)

### Key Terms

| Term | Definition |
|------|------------|
| **Strike** | The price at which the option can be exercised |
| **Expiry** | When the option expires (settlement date, 8:00 UTC) |
| **Premium** | The price paid for the option |
| **Settlement** | Cash payment based on price difference at expiry |
| **Collateral** | Funds locked to back the option (for sellers) |

### Collateral Requirements by Option Type

**IMPORTANT:** Different option types require different collateral tokens:

| Option Type | Implementation | Collateral Required |
|-------------|----------------|---------------------|
| **PUT** | PUT | USDC (quote asset) |
| **CALL** | INVERSE_CALL | WETH (base asset) |

- **PUT options**: Collateral in USDC. Formula: `(collateral × 1e8) / strike`
- **CALL options**: Collateral in WETH. Formula: `collateral / 1e12` (1 WETH = 1 contract)

The `build-rfq.ts` script automatically selects the correct collateral based on option type.

---

## Multi-Strike Option Structures

Beyond vanilla PUT and CALL options, Thetanuts supports advanced multi-strike structures for sophisticated trading strategies.

### All Option Types

| Type | Strikes | Collateral | Description |
|------|---------|------------|-------------|
| **PUT** | 1 | USDC | Standard cash-settled put |
| **INVERSE_CALL** | 1 | WETH | Cash-settled call (base collateral) |
| **CALL_SPREAD** | 2 | USDC | Buy lower strike call, sell higher strike call |
| **PUT_SPREAD** | 2 | USDC | Buy higher strike put, sell lower strike put |
| **CALL_FLY** | 3 | USDC | Call butterfly - profit near middle strike |
| **PUT_FLY** | 3 | USDC | Put butterfly - profit near middle strike |
| **CALL_CONDOR** | 4 | USDC | Call condor - wider profit range |
| **PUT_CONDOR** | 4 | USDC | Put condor - wider profit range |
| **IRON_CONDOR** | 4 | USDC | Put spread + call spread (neutral) |
| **PHYSICAL_CALL** | 1 | WETH | Physically settled call |
| **PHYSICAL_PUT** | 1 | USDC | Physically settled put |

### Strike Ordering Rules

**CRITICAL:** Strikes must be ordered correctly or the RFQ will fail.

| Structure | Type | Strike Order | Example |
|-----------|------|--------------|---------|
| Vanilla | PUT/CALL | N/A (1 strike) | `--strike 1900` |
| Spread | PUT | Descending (high→low) | `--strikes 1900,1800` |
| Spread | CALL | Ascending (low→high) | `--strikes 2000,2100` |
| Butterfly | PUT | Descending | `--strikes 1900,1850,1800` |
| Butterfly | CALL | Ascending | `--strikes 2000,2050,2100` |
| Condor | ALL | Always ascending | `--strikes 1800,1900,2100,2200` |

### Collateral Formulas by Structure (Human-Readable)

These are simplified formulas for quick estimation. For exact on-chain values, use `previewFillOrder()` or `client.utils.calculateCollateral()`.

| Structure | Collateral | Simplified Formula | Example |
|-----------|-----------|-------------------|---------|
| **Vanilla PUT** | USDC | `collateral / strike` | $1900 USDC at $1900 strike = 1 contract |
| **INVERSE_CALL** | WETH | `collateral` (1:1) | 1 WETH = 1 contract |
| **CALL_SPREAD** | USDC | `collateral / (upper - lower)` | $100 USDC / $100 width = 1 contract |
| **PUT_SPREAD** | USDC | `collateral / (upper - lower)` | $100 USDC / $100 width = 1 contract |
| **Butterfly** | USDC | `collateral / (middle - lower)` | $50 USDC / $50 wing = 1 contract |
| **Condor** | USDC | `collateral / (strike2 - strike1)` | $100 USDC / $100 inner width = 1 contract |
| **IRON_CONDOR** | USDC | `collateral / max(K2-K1, K4-K3)` | Based on wider wing |
| **PHYSICAL_CALL** | WETH | Same as INVERSE_CALL | 1 WETH = 1 contract |
| **PHYSICAL_PUT** | USDC | Same as Vanilla PUT | collateral / strike |

**Key rule:** Only INVERSE_CALL and PHYSICAL_CALL use WETH (base asset). **Everything else uses USDC** — including CALL_SPREAD, CALL_FLY, and CALL_CONDOR.

### When to Use Each Structure

| Structure | Market View | Risk Level | Risk/Reward | Best For |
|-----------|-------------|------------|-------------|----------|
| **PUT** | Bearish | HIGH | Large profit (up to strike - premium), lose premium | Strong downside conviction |
| **CALL** | Bullish | HIGH | Unlimited profit, lose premium | Strong upside conviction |
| **PUT_SPREAD** | Moderately bearish | MEDIUM | Capped profit/loss | Cheaper than vanilla put |
| **CALL_SPREAD** | Moderately bullish | MEDIUM | Capped profit/loss | Cheaper than vanilla call |
| **PUT_FLY** | Neutral/range-bound | LOW | High reward if pinned, tiny cost | Low cost, precise target |
| **CALL_FLY** | Neutral/range-bound | LOW | High reward if pinned, tiny cost | Low cost, precise target |
| **CONDOR** | Neutral/range-bound | MEDIUM | Lower reward, wider range | More forgiving than fly |
| **IRON_CONDOR** | Neutral | LOW | Collect premium both sides | Range-bound markets |
| **PHYSICAL_CALL** | Bullish (want delivery) | HIGH | Receive underlying asset | Physical settlement needed |
| **PHYSICAL_PUT** | Bearish (want delivery) | HIGH | Deliver underlying asset | Physical settlement needed |

### Risk-Categorized Strategy Recommendations

When a user asks for a strategy recommendation, **FIRST ask about their risk preference**, then match to appropriate strategies within that tier.

#### Step 1: Ask the User's Risk Level

Present these three options:

| Risk Level | What It Means | Max Loss | Profit Potential |
|------------|---------------|----------|-----------------|
| **LOW** | Defined max loss, premium collection, high probability of small wins | Capped & known upfront | Capped but consistent |
| **MEDIUM** | Spreads with balanced risk/reward, moderate probability | Capped at spread width | Capped at spread width |
| **HIGH** | Full directional exposure, low probability of large wins | Full premium (buyer) or very large (seller) | Unlimited (buyer) |

#### Step 2: Strategy Decision Tree by Risk Level

```
User wants a strategy recommendation
        │
        ▼
┌──────────────────────────────────┐
│ Step 1: Check market news        │
│ (WebSearch - see News section)   │
└──────────────────────────────────┘
        │
        ▼
┌──────────────────────────────────┐
│ Step 2: Ask risk level           │
│ LOW / MEDIUM / HIGH              │
└──────────────────────────────────┘
        │
        ├── LOW RISK
        │   │
        │   ├── Neutral view ──────► IRON_CONDOR (sell)
        │   │                        Collect premium both sides, profit if range-bound
        │   │                        Max loss: spread width - premium
        │   │                        Max gain: premium collected
        │   │                        Win prob: ~60-70% (price stays in range)
        │   │
        │   ├── Slightly bullish ──► PUT_FLY (buy) or Sell PUT via orderbook
        │   │                        Butterfly: tiny cost, big payout if pinned
        │   │                        Max loss: premium paid (very small)
        │   │                        Max gain: wing width - premium
        │   │
        │   ├── Slightly bearish ──► CALL_FLY (buy) or Sell CALL via orderbook
        │   │                        Same as above, opposite direction
        │   │
        │   └── Range-bound ───────► Butterfly (CALL_FLY / PUT_FLY)
        │                            Cheapest defined-risk play
        │                            Max loss: premium paid (~$3-5/contract)
        │                            Max gain: wing width (~$47-50/contract)
        │
        ├── MEDIUM RISK
        │   │
        │   ├── Bullish ──────────► CALL_SPREAD (buy)
        │   │                       Cheaper than vanilla call, capped both sides
        │   │                       Max loss: premium paid
        │   │                       Max gain: spread width - premium
        │   │                       Risk/Reward: typically 1:1 to 1:3
        │   │
        │   ├── Bearish ─────────► PUT_SPREAD (buy)
        │   │                       Cheaper than vanilla put, capped both sides
        │   │                       Max loss: premium paid
        │   │                       Max gain: spread width - premium
        │   │
        │   └── Range-bound ─────► CONDOR (CALL_CONDOR / PUT_CONDOR)
        │                          Wider profit range than butterfly
        │                          Max loss: wing width - premium collected
        │                          Max gain: premium collected (sell) or inner width (buy)
        │
        └── HIGH RISK
            │
            ├── Bullish ──────────► CALL (vanilla buy) / INVERSE_CALL
            │                       Unlimited profit potential if price rises
            │                       Max loss: full premium paid
            │                       Max gain: unlimited
            │
            ├── Bearish ─────────► PUT (vanilla buy)
            │                       Unlimited profit if price crashes
            │                       Max loss: full premium paid
            │                       Max gain: strike - premium (if price → 0)
            │
            └── Selling premium ──► Naked PUT sell or CALL sell
                                    Collect premium, very large risk if wrong
                                    Max loss: strike price (PUT) or unlimited (CALL)
                                    Max gain: premium collected
```

#### Risk Summary Card (Always Show When Recommending)

Every strategy recommendation MUST include this card:

```
┌────────────────────────────────────────────────────┐
│ Strategy:  [STRATEGY NAME]                         │
│ Risk:      [LOW / MEDIUM / HIGH]                   │
│ Direction: [BULLISH / BEARISH / NEUTRAL]           │
├────────────────────────────────────────────────────┤
│ Max Loss:  $[amount] ([description])               │
│ Max Gain:  $[amount] ([description])               │
│ Break-even: $[price]                               │
│ Win Zone:  Price between $[low] and $[high]        │
│ Collateral: [amount] [token]                       │
└────────────────────────────────────────────────────┘
```

#### Collateral Efficiency Comparison

Different structures give you different exposure per dollar of collateral:

| Structure | $100 Collateral Gets You | Relative Efficiency | Risk Level |
|-----------|-------------------------|---------------------|------------|
| **Vanilla PUT** (at $2000 strike) | ~0.05 contracts | 1x (baseline) | HIGH |
| **PUT_SPREAD** ($100 width) | 1 contract | **20x more** | MEDIUM |
| **Butterfly** ($50 wing width) | 2 contracts | **40x more** | LOW |
| **Condor** ($100 inner width) | 1 contract | **20x more** | MEDIUM |
| **Iron Condor** ($100 inner width) | 1 contract | **20x more** | LOW |

**Key Insight:** For users with small collateral (under $100), LOW and MEDIUM risk strategies (spreads, butterflies) provide significantly more market exposure than HIGH risk vanilla options.

#### Strategy Selection Inputs

When recommending a strategy, consider these inputs in order of priority:

| Priority | Input | How to Determine | Impact on Recommendation |
|----------|-------|-----------------|-------------------------|
| **1** | **Risk Level** | Ask user: low, medium, or high? | PRIMARY filter — determines available strategies |
| **2** | **Market View** | Ask user: bullish, bearish, or neutral? | Determines direction within risk tier |
| **3** | **News/Events** | WebSearch for recent market events | Informs conviction level and timing |
| **4** | **Collateral Size** | Check wallet balance | Small = prefer spreads/butterflies for efficiency |
| **5** | **Conviction Level** | Ask: strong view or moderate? | High conviction may justify higher risk tier |
| **6** | **Expiry Timeframe** | Check available expiries | Short-term neutral = butterfly, Longer = condor |

### News & Events Integration

**Before EVERY strategy recommendation, the agent MUST search for recent market-moving events.** This ensures context-aware recommendations, not purely technical ones.

#### How to Fetch Market News

Use WebSearch with these queries (run at least 2):

| Query | Purpose |
|-------|---------|
| `"crypto market news today"` | General market sentiment |
| `"ethereum price catalyst"` or `"bitcoin price catalyst"` | Asset-specific events |
| `"FOMC meeting crypto"` or `"CPI inflation crypto"` | Macro events affecting crypto |
| `"crypto options expiry this week"` | Options-specific events (pin risk, gamma squeeze) |
| `"ethereum upgrade"` or `"bitcoin ETF flows"` | Protocol/regulatory catalysts |

If WebSearch returns a relevant article, use **WebFetch** to get deeper details.

#### Translating News to Strategy

| Event Type | Expected Impact | Suggested Direction | Risk Note |
|------------|----------------|--------------------|--------------------|
| Rate cut / dovish Fed | Bullish | CALL-side strategies | MEDIUM — market may "sell the news" |
| Rate hike / hawkish Fed | Bearish | PUT-side strategies | MEDIUM — may already be priced in |
| Major exchange hack/exploit | Bearish (short-term) | PUT-side strategies | HIGH — volatility spike |
| ETF approval / large inflows | Bullish | CALL-side strategies | MEDIUM — catalyst may be priced in |
| Protocol upgrade (successful) | Bullish for that asset | CALL-side strategies | LOW-MEDIUM |
| Regulatory crackdown | Bearish | PUT-side or neutral | HIGH — uncertainty and fear |
| Large options expiry (high OI) | Neutral → pin risk | Butterflies / Condors (LOW risk) | LOW — defined risk |
| No significant news | Neutral / range-bound | Premium selling (Iron Condor) | LOW — collect theta decay |
| Conflicting signals | Uncertain | Neutral structures or wait | Reduce size, use LOW risk |

#### News-Informed Recommendation Template

When presenting a strategy recommendation, always include market context:

```
Market Context (from recent news):
• [Event 1]: [brief description] → [bullish/bearish/neutral]
• [Event 2]: [brief description] → [bullish/bearish/neutral]

Overall market bias: [BULLISH / BEARISH / NEUTRAL / UNCERTAIN]

Based on [RISK LEVEL] risk preference and current market conditions:
[Strategy recommendation with Risk Summary Card]
```

---

### Multi-Strike RFQ Examples

**2-Strike Spread (CALL_SPREAD):**
```bash
npx tsx scripts/build-rfq.ts \
  --underlying ETH \
  --type CALL \
  --strikes 2000,2100 \
  --expiry 1774684800 \
  --contracts 1 \
  --direction buy
```
*Buy $2000 call, sell $2100 call. Max profit = $100 - premium. Max loss = premium.*

**3-Strike Butterfly (PUT_FLY):**
```bash
npx tsx scripts/build-rfq.ts \
  --underlying ETH \
  --type PUT \
  --strikes 1900,1850,1800 \
  --expiry 1774684800 \
  --contracts 1 \
  --direction buy
```
*Profit maximized if ETH settles at $1850. Low cost, high reward if pinned.*

**4-Strike Condor (IRON_CONDOR):**
```bash
npx tsx scripts/build-rfq.ts \
  --underlying ETH \
  --type PUT \
  --strikes 1800,1900,2100,2200 \
  --expiry 1774684800 \
  --contracts 1 \
  --direction sell
```
*Sell iron condor. Collect premium if ETH stays between $1900-$2100.*

---

## OptionBook vs RFQ (Factory)

The SDK supports two trading systems. Choose based on your use case:

| | **OptionBook** | **RFQ (Factory)** |
|---|---|---|
| **What** | Fill existing market-maker orders | Create custom options via sealed-bid auction |
| **When to use** | Quick trades on listed options | Custom strikes, expiries, multi-leg structures |
| **Structures** | Vanilla only | Vanilla, spread, butterfly, condor, iron condor |
| **Key methods** | `fillOrder()`, `previewFillOrder()` | `buildRFQRequest()`, `requestForQuotation()` |
| **Pricing** | Order prices from `fetchOrders()` | MM pricing from `getAllPricing()` |
| **Data source** | Book indexer (`/api/v1/book/`) | Factory indexer (`/api/v1/factory/`) |
| **User data** | `getUserPositionsFromIndexer()` | `getUserRfqs()`, `getUserOptionsFromRfq()` |
| **Stats** | `getBookProtocolStats()`, `getBookDailyStats()` | `getFactoryProtocolStats()`, `getFactoryDailyStats()` |
| **Collateral** | Paid upfront by taker | `collateralAmount = 0` (held by factory) |
| **Settlement** | Cash only | Cash or physical |

### Orderbook Trading

**What it is:** Fill existing orders posted by market makers - instant execution.

```
You → Fill existing order → Instant trade
```

**Best for:**
- Standard strikes/expiries with existing liquidity
- Quick trades when you see a good price
- Smaller to medium sizes

**How it works:**
1. Fetch orderbook: `npx tsx scripts/fetch-orders.ts --type PUT`
2. See available BIDs (buyers) and ASKs (sellers)
3. Fill the order you want: `npx tsx scripts/fill-order.ts --order-index 0 --collateral 10 --execute` (reads `WDK_SEED` from `.env`)

### RFQ (Request for Quote)

**What it is:** Request a custom quote from market makers - they respond within 45 seconds.

```
You → Submit RFQ → MM sees it → MM sends encrypted offer → You settle (or accept early)
```

**Best for:**
- Custom strikes/expiries not on orderbook
- No existing liquidity at your terms
- Larger sizes (MMs may offer better pricing)
- Multi-leg structures (spreads, butterflies, condors)

**How it works:**
1. Build RFQ: `npx tsx scripts/build-rfq.ts --underlying ETH --type PUT --strike 1900 --expiry <timestamp> --contracts 0.1 --direction buy`
2. Send transaction with the returned `to` and `data`
3. Wait up to 45 seconds for MM response
4. Settle when offer received (or accept early - see Early Settlement)

### Decision Matrix

| Scenario | Use | Why |
|----------|-----|-----|
| "I see a good price on orderbook" | **Orderbook** | Instant execution |
| "Standard strike, liquidity exists" | **Orderbook** | Faster, simpler |
| "Custom strike not on orderbook" | **RFQ** | Only way to get it |
| "Large size trade" | **RFQ** | May get better pricing |
| "Need it filled NOW" | **Orderbook** | RFQ takes up to 6 min |
| "No orders at my strike" | **RFQ** | Request custom quote |
| "Multi-leg structure" | **RFQ** | Orderbook only supports vanilla |
| "Physical settlement" | **RFQ** | Orderbook is cash-only |

**Agent Decision Logic:**
1. First, check orderbook for liquidity at your strike
2. If liquidity exists → recommend Orderbook
3. If no liquidity → recommend RFQ and explain why

---

## Agent Decision Logic (Orderbook-First)

When a user wants to trade, the agent ALWAYS checks the orderbook first before recommending a trading method.

### Decision Flowchart

```
User wants to trade
        │
        ▼
┌─────────────────────────┐
│  check-orderbook.ts     │
│  Check for liquidity    │
└─────────────────────────┘
        │
        ▼
┌─────────────────────────┐
│ Exact strike match?     │
└─────────────────────────┘
    │           │
   Yes          No
    │           │
    ▼           ▼
┌─────────┐  ┌─────────────────┐
│Orderbook│  │Nearby strikes?  │
│  Fill   │  │(within ±5%)     │
└─────────┘  └─────────────────┘
                 │         │
                Yes        No
                 │         │
                 ▼         ▼
           ┌─────────┐  ┌─────┐
           │Show     │  │ RFQ │
           │options  │  │     │
           └─────────┘  └─────┘
```

### How to Use check-orderbook.ts

Before recommending orderbook or RFQ, run:
```bash
npx tsx scripts/check-orderbook.ts --underlying ETH --type PUT --strike 1900 --expiry 1774684800 --direction sell
```

The script returns:
- `recommendation`: "orderbook" or "rfq"
- `reason`: Explanation of why
- `orderbookOrders`: Matching orders with prices
- `nearbyStrikes`: Alternative strikes if exact not found
- `nextStep`: Command to run next

### Example Scenarios

**Scenario 1: Liquidity Found**
```
User: "Sell a PUT at $1900"
Agent: Runs check-orderbook.ts
Result: {
  "recommendation": "orderbook",
  "reason": "Found orderbook liquidity at strike $1900. Best bid: $8.08. Available: 75 contracts."
}
Agent: "Found a buyer at $8.08/contract. Use orderbook for instant execution."
```

**Scenario 2: No Exact Match, Nearby Available**
```
User: "Sell a PUT at $1850"
Agent: Runs check-orderbook.ts
Result: {
  "recommendation": "rfq",
  "reason": "No orderbook liquidity at $1850. Nearby strikes: $1900 (+2.7%), $1925 (+4.1%)"
}
Agent: "No orders at $1850, but $1900 is available (+2.7%). Would you like that, or submit RFQ for $1850?"
```

**Scenario 3: Partial Fill**
```
User: "Sell 100 contracts at $1900"
Agent: Runs check-orderbook.ts --size 100
Result: {
  "recommendation": "orderbook",
  "partialFillAvailable": true,
  "partialSize": 75,
  "reason": "Found 75 contracts (you requested 100). Partial fill available."
}
Agent: "Only 75 contracts available on orderbook. Fill partial now, or use RFQ for full 100?"
```

---

## Trading Workflows

### Workflow 1: Fill an Orderbook Order (Instant)

```
Step 1: Check wallet
   └─> node scripts/wallet-discover.js

Step 2: Check balance
   └─> node scripts/wallet-balance.js --chain base-mainnet --tokens 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913

Step 3: Fetch orderbook
   └─> npx tsx scripts/fetch-orders.ts --type PUT

Step 4: Preview fill (see what you'll get)
   └─> npx tsx scripts/fill-order.ts --order-index 0 --collateral 10

Step 5: Execute fill (reads WDK_SEED from .env — never pass seed on CLI)
   └─> npx tsx scripts/fill-order.ts --order-index 0 --collateral 10 --execute --wait
```

### Workflow 2: Submit an RFQ (Custom Terms)

```
Step 1: Check wallet & balance (same as above)

Step 2: Get MM pricing to see market levels
   └─> npx tsx scripts/get-mm-pricing.ts ETH --type PUT

Step 3: Build RFQ with your terms
   └─> npx tsx scripts/build-rfq.ts --underlying ETH --type PUT --strike 1900 --expiry 1774684800 --contracts 0.1 --direction buy

Step 4: Approve tokens (if selling/first time — prefer exact amount over --max)
   └─> npx tsx scripts/approve-token.ts --token 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 --spender 0x8118daD971dEbffB49B9280047659174128A8B94 --amount <exact> --wait
   (For unlimited approvals, add --max --confirm-max. Seed read from WDK_SEED env.)

Step 5: Send RFQ transaction (reads WDK_SEED from .env)
   └─> npx tsx scripts/send-transaction.ts --to <from step 3> --data <from step 3> --wait

Step 6: Wait for MM offer (up to 45 seconds)

Step 7: Verify RFQ fill
   └─> npx tsx scripts/check-rfq-fill.ts --address <wallet> --ticker <expected> --since <submission_timestamp>
   └─> If filled: Shows position details
   └─> If not filled: Shows suggestions for next steps
```

### Workflow 3: Check Positions

```
npx tsx scripts/get-positions.ts 0xYourWalletAddress
```

### Workflow 3b: Portfolio Performance & ROI Review

After trades expire, show the user their realized returns. This workflow uses existing scripts — no new tools needed.

#### How to Calculate ROI

```
Step 1: Fetch all positions
   └─> npx tsx scripts/get-positions.ts <wallet_address>

Step 2: Categorize by status
   - Settled/expired positions → REALIZED P&L
   - Active/open positions → UNREALIZED (show separately)

Step 3: For each expired position
   - Use the pnlUsd field from get-positions.ts (if available)
   - If pnlUsd is missing, calculate manually:
     └─> For PUT/CALL: npx tsx scripts/calculate-payout.ts --type <PUT|CALL> --strike <strike> --settlement <settlement_price> --contracts <amount> [--is-buyer]
     └─> For spreads/butterflies/condors: use client.option.calculatePayout(optionAddress, settlementPrice) on-chain
         (Note: calculate-payout.ts only supports vanilla PUT/CALL — multi-strike payouts need the SDK on-chain method)

Step 4: Aggregate and present using the template below
```

#### ROI Calculation Logic

**For BUYERS (paid premium):**
- Cost basis = premium paid (collateral committed)
- Return = pnlUsd or calculated payout
- ROI = (return / cost_basis) × 100%
- Expired worthless → ROI = **-100%**
- Example: Paid $10 premium, option settled for $25 payout → ROI = +150%

**For SELLERS (received premium):**
- Credit received = premium collected
- Settlement cost = pnlUsd (negative = you paid out)
- ROI = (net_pnl / collateral_locked) × 100%
- Expired worthless for buyer (good for seller) → ROI = +(premium / collateral) × 100%
- Example: Collected $8 premium on $100 collateral, expired OTM → ROI = +8%

#### Portfolio Performance Summary Template

Present results in this format:

```
Portfolio Performance Summary
══════════════════════════════════════════════════════════
Wallet: 0x...
Period: [earliest expired trade] to [latest expired trade]

REALIZED P&L (Expired Positions)
┌──────────────────────┬──────┬─────────┬─────────┐
│ Trade                │ Side │ P&L     │ ROI     │
├──────────────────────┼──────┼─────────┼─────────┤
│ ETH-28MAR-2000-P     │ SELL │ +$12.50 │ +6.25%  │
│ ETH-28MAR-2100-C     │ BUY  │ -$8.00  │ -100%   │
│ ETH-04APR-1900/1800  │ BUY  │ +$45.00 │ +150%   │
├──────────────────────┼──────┼─────────┼─────────┤
│ TOTAL                │      │ +$49.50 │         │
└──────────────────────┴──────┴─────────┴─────────┘

Win rate: 2/3 (66.7%)
Average P&L per trade: +$16.50
Best trade:  ETH PUT_SPREAD (+$45.00, +150%)
Worst trade: ETH CALL (-$8.00, expired worthless)

OPEN POSITIONS
┌──────────────────────┬──────┬───────────┬──────────┬────────┐
│ Trade                │ Side │ Contracts │ Expiry   │ Status │
├──────────────────────┼──────┼───────────┼──────────┼────────┤
│ ETH-18APR-2000-P     │ BUY  │ 0.5       │ Apr 18   │ Active │
└──────────────────────┴──────┴───────────┴──────────┴────────┘
```

#### When to Show Performance

- User asks "how are my trades doing?", "show my P&L", "what's my ROI?"
- User asks "check my positions" AND has expired positions → include ROI for expired ones
- Proactively mention performance when user has recently expired positions they haven't reviewed
- After any trade settles, offer to show the outcome: "Your ETH PUT just expired. Want to see how it did?"

---

### Workflow 4: Early Settlement (Accept MM Offer Before Deadline)

After a market maker submits an encrypted offer to your RFQ, you can decrypt and accept it early — no need to wait for the full deadline.

```
Step 1: Submit RFQ (Workflow 2, Steps 1-5)

Step 2: MM sends encrypted offer (within 45 seconds)

Step 3: Decrypt the offer using your ECDH keypair
   └─> Uses client.rfqKeys.decryptOffer()

Step 4: Accept the offer early
   └─> Uses client.optionFactory.encodeSettleQuotationEarly(quotationId, offerAmount, nonce, offeror)
   └─> Send transaction with returned {to, data}
```

**Real examples:**
- RFQ 784 (PUT BUTTERFLY $1700/$1800/$1900): MM offered at 04:05:45 UTC, early settle at 04:07:09 UTC (3 min before deadline)
  - TX: `0x105f75cdfb64a3796100f6d667bc4f7fec3836d2b5aa5c43b66073a1b40964ee`
- RFQ 785 (PUT CONDOR $1600/$1700/$1800/$1900): MM offered 0.003248 USDC, early settle at 04:15:00 UTC
  - TX: `0xa89fb6dbad43b430399bbdec878927185e602b7df9b5390f71d2d11c33e4d850`

### Workflow 5: Cancel RFQ & Claim Refund

If a user wants to cancel an active RFQ before it settles, or if no MM responded:

```
┌─────────────────────────────────────────────────────┐
│ RFQ submitted                                       │
│         │                                           │
│         ▼                                           │
│ ┌─────────────────────┐                             │
│ │ MM responded?       │                             │
│ └─────────────────────┘                             │
│     │           │                                   │
│    Yes          No                                  │
│     │           │                                   │
│     ▼           ▼                                   │
│ ┌─────────┐  ┌──────────────────────────────┐       │
│ │ Accept  │  │ RFQ expires with no offers   │       │
│ │ or      │  │ → No collateral was locked   │       │
│ │ Cancel? │  │ → Nothing to refund          │       │
│ └─────────┘  └──────────────────────────────┘       │
│   │     │                                           │
│  Accept Cancel                                      │
│   │     │                                           │
│   ▼     ▼                                           │
│ Settle  Cancel RFQ                                  │
│         └─> cancelQuotation(quotationId)            │
│         └─> Collateral returned to wallet           │
└─────────────────────────────────────────────────────┘
```

#### Cancel an Active RFQ

```typescript
// Cancel before settlement — requester only
const { to, data } = client.optionFactory.encodeCancelQuotation(quotationId);
// Send transaction with {to, data} via send-transaction.ts
```

#### Cancel an Offer (Market Maker Side)

```typescript
// MM cancels their offer before settlement
const { to, data } = client.optionFactory.encodeCancelOfferForQuotation(quotationId);
```

#### Check RFQ Status

```typescript
// Query current state of an RFQ
const quotation = await client.optionFactory.getQuotation(quotationId);
// quotation status: 'active' | 'settled' | 'cancelled'
// quotation.isActive — whether RFQ is still open
// quotation.currentWinner — winning offeror's address
```

#### Refund Rules

| Scenario | Collateral | What Happens |
|----------|-----------|-------------|
| **Buy RFQ, no MM responds** | No collateral locked by buyer | Nothing to refund — buyer only pays premium if settled |
| **Buy RFQ, user cancels before settlement** | No collateral locked | RFQ cancelled, no action needed |
| **Sell RFQ, no MM responds** | Collateral held by factory | RFQ expires, collateral returned automatically |
| **Sell RFQ, user cancels before settlement** | Collateral held by factory | `cancelQuotation()` releases collateral back to wallet |
| **Sell RFQ, settled** | Collateral locked in option | Collateral backs the option until expiry/settlement |
| **Orderbook fill (buy or sell)** | Collateral paid/locked at fill | Irreversible — no cancellation for orderbook fills |

**IMPORTANT:** Orderbook fills are INSTANT and IRREVERSIBLE. Only RFQs can be cancelled (before settlement).

---

### Buy vs Sell Order: Collateral & Token Flow

**No ETH is sent as transaction value for option trades.** All collateral flows happen via ERC-20 token transfers (USDC, WETH). ETH is only used for gas fees.

#### When BUYING Options

```
Buyer Flow:
1. Premium is paid in collateral tokens (USDC for PUTs, WETH for CALLs)
2. Token approval needed: approve-token.ts (one-time per token/spender)
3. Collateral is transferred to the contract when the trade executes
4. If RFQ: collateralAmount = 0 in the request (factory holds it)
5. If Orderbook: collateral deducted at fill time

What you PAY:   Premium (in USDC or WETH) + gas (in ETH)
What you GET:   Option position (right to profit if price moves your way)
At expiry:      Payout if in-the-money, or nothing if out-of-the-money
```

#### When SELLING Options

```
Seller Flow:
1. Collateral is LOCKED to back the option (USDC for PUTs, WETH for CALLs)
2. Token approval needed: approve-token.ts (one-time per token/spender)
3. Collateral transferred to contract and held until expiry
4. Premium is received from buyer

What you PAY:   Collateral lock (USDC or WETH) + gas (in ETH)
What you GET:   Premium received upfront
At expiry:      Keep premium if OTM, or payout difference if ITM
                Remaining collateral returned after settlement
```

#### Token Requirements Summary

| Action | Collateral Token | Gas Token | Approval Needed |
|--------|-----------------|-----------|-----------------|
| **Buy PUT** | USDC (premium) | ETH | USDC → OptionFactory/OptionBook |
| **Buy CALL** | WETH (premium) | ETH | WETH → OptionFactory/OptionBook |
| **Sell PUT** | USDC (collateral lock) | ETH | USDC → OptionFactory/OptionBook |
| **Sell CALL** | WETH (collateral lock) | ETH | WETH → OptionFactory/OptionBook |

**Always check balance BEFORE trading:**
```bash
# Check USDC balance (for PUTs)
node scripts/wallet-balance.js --chain base-mainnet --tokens 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913

# Check WETH balance (for CALLs)
node scripts/wallet-balance.js --chain base-mainnet --tokens 0x4200000000000000000000000000000000000006

# Check ETH balance (for gas)
node scripts/wallet-balance.js --chain base-mainnet
```

### Winner Selection & Payout by Option Type

The **winner** (`winningOfferor`) in an RFQ is always the market maker with the best offer price. Winner selection works the **same way for ALL option types** — PUT, CALL, spreads, butterflies, condors, iron condors, and physical options.

#### Winner Fields in SDK

The winner address appears in three places depending on context:

| Context | Field | When to Use |
|---------|-------|-------------|
| **On-chain state** | `QuotationState.currentWinner` | During active RFQ — the current best offeror |
| **State API** | `StateRfq.winner` | After settlement — the final winning MM |
| **Settlement event** | `QuotationSettledEvent.winningOfferor` | Emitted when RFQ settles |

#### Payout Formulas by Option Type

| Type | Buyer Payout Formula | Max Payout | Settlement |
|------|---------------------|------------|------------|
| **PUT** | `max(strike - price, 0) × contracts` | strike × contracts | Cash (USDC) |
| **INVERSE_CALL** | `max(price - strike, 0) × contracts` | Unlimited | Cash (WETH) |
| **CALL_SPREAD** | `min(max(price - K1, 0), K2 - K1) × contracts` | (K2 - K1) × contracts | Cash (USDC) |
| **PUT_SPREAD** | `min(max(K1 - price, 0), K1 - K2) × contracts` | (K1 - K2) × contracts | Cash (USDC) |
| **CALL_FLY** | Peaks at middle strike, 0 at wings | wing width × contracts | Cash (USDC) |
| **PUT_FLY** | Peaks at middle strike, 0 at wings | wing width × contracts | Cash (USDC) |
| **CALL_CONDOR** | Flat max between K2-K3, tapers at wings | inner width × contracts | Cash (USDC) |
| **PUT_CONDOR** | Flat max between K2-K3, tapers at wings | inner width × contracts | Cash (USDC) |
| **IRON_CONDOR** | Profit if price between K2-K3 | premium collected | Cash (USDC) |
| **PHYSICAL_CALL** | Buyer receives underlying asset | N/A (delivery) | Physical |
| **PHYSICAL_PUT** | Buyer delivers underlying, receives USDC | N/A (delivery) | Physical |

#### SDK Payout Calculation Support

The SDK utility `client.utils.calculatePayout()` supports these types:

```typescript
type PayoutType = 'call' | 'put' | 'call_spread' | 'put_spread';
```

**For butterflies, condors, and iron condors**: use `client.option.calculatePayout(optionAddress, settlementPrice)` which calculates on-chain for any option type, or use `client.option.simulatePayout()` for simulation.

```typescript
// For vanilla and spreads — use utility function
const payout = client.utils.calculatePayout({
  type: 'call_spread',
  strikes: [2000n * 10n**8n, 2100n * 10n**8n],
  settlementPrice: 2050n * 10n**8n,
  numContracts: 1n * 10n**18n,
});

// For butterflies, condors, iron condors — use on-chain calculation
const payout = await client.option.calculatePayout(optionAddress, settlementPrice);
```

#### Settlement Events

When an option settles at expiry, these events are emitted:

| Event | Fields | Description |
|-------|--------|-------------|
| `OptionExpiredEvent` | settlementPrice | Oracle records the final price |
| `OptionPayoutEvent` | buyer, amountPaidOut | Buyer receives payout (if ITM) |
| `CollateralReturnedEvent` | seller, amountReturned | Seller gets remaining collateral back |

> **r12 settlement is automatic.** On the Base_r12 deployment, options no longer expose a zero-arg `payout()` write entrypoint — settlement fires from the factory's `notifyTradeSettled` callback once the oracle records the final price. SDK ≥ 0.2.4 throws `INVALID_PARAMS` on any legacy `payout()` call; check status with `client.option.getOptionInfo(optionAddress).settled` and read amounts with the view methods above. Reclaiming collateral after settlement uses `client.option.reclaimCollateral(optionAddress, ownedOption)` — the SDK auto-forwards `getReclaimFee()` as `msg.value`.

#### Physical Settlement (PHYSICAL_CALL / PHYSICAL_PUT)

Physical options involve actual asset delivery instead of cash settlement:

| Type | Buyer Pays | Buyer Receives | Seller Provides |
|------|-----------|----------------|-----------------|
| **PHYSICAL_CALL** | strike × contracts (USDC) | contracts of underlying (WETH) | WETH collateral |
| **PHYSICAL_PUT** | contracts of underlying (WETH) | strike × contracts (USDC) | USDC collateral |

The SDK has dedicated builders for physical options:
- `client.optionFactory.buildPhysicalRFQ()`
- `client.optionFactory.buildPhysicalSpreadRFQ()`
- `client.optionFactory.buildPhysicalButterflyRFQ()`
- `client.optionFactory.buildPhysicalCondorRFQ()`

---

## Understanding Collateral vs Contracts

When viewing orders, `availableAmount` represents the **maker's collateral budget**, not the number of contracts. The actual number of purchasable contracts depends on the option type and collateral requirements.

### Collateral Formulas by Option Type (On-Chain)

These are the on-chain formulas using raw decimal values. For practical use, prefer `previewFillOrder()` which handles all conversions automatically.

| Option Type | # Strikes | Collateral | On-Chain Formula | Example |
|-------------|-----------|-----------|-----------------|---------|
| **Vanilla PUT** | 1 | USDC | `(collateral × 1e8) / strike` | 10,000 USDC at $95k = 0.105 contracts |
| **INVERSE_CALL** | 1 | WETH | `collateral / 1e12` | 1 WETH = 1 contract |
| **CALL_SPREAD** | 2 | USDC | `(collateral × 1e8) / spreadWidth` | 10,000 USDC / $10k = 1 contract |
| **PUT_SPREAD** | 2 | USDC | `(collateral × 1e8) / spreadWidth` | 10,000 USDC / $10k = 1 contract |
| **BUTTERFLY** | 3 | USDC | `(collateral × 1e8) / maxSpread` | Based on widest strike range |
| **CONDOR** | 4 | USDC | `(collateral × 1e8) / maxSpread` | Based on widest strike range |
| **PHYSICAL_CALL** | 1 | WETH | Same as INVERSE_CALL | 1 WETH = 1 contract |
| **PHYSICAL_PUT** | 1 | USDC | Same as Vanilla PUT | Same formula |

**IMPORTANT: Only single-strike CALL options (INVERSE_CALL, PHYSICAL_CALL) use WETH collateral. ALL multi-strike structures use USDC, even CALL_SPREAD, CALL_FLY, and CALL_CONDOR.**

### Using previewFillOrder

Always use `previewFillOrder()` to see the actual contract count before filling:

```typescript
const order = orders[0];

// Preview shows calculated max contracts based on collateral requirements
const preview = client.optionBook.previewFillOrder(order);
console.log(`Max contracts: ${preview.maxContracts}`);
console.log(`Collateral token: ${preview.collateralToken}`);
console.log(`Price per contract: ${preview.pricePerContract}`);

// Preview with specific premium amount
const preview10 = client.optionBook.previewFillOrder(order, 10_000000n); // 10 USDC premium
console.log(`Contracts for 10 USDC: ${preview10.numContracts}`);
```

### Why This Matters

For a PUT option with a $95,000 strike:
- **Maker provides**: 10,000 USDC collateral
- **Max contracts**: 10,000 / 95,000 ≈ **0.105 contracts** (not 10,000!)

The `previewFillOrder()` method handles these calculations automatically for all option types.

---

## SDK Modules Reference

| Module | Purpose | Requires Signer |
|--------|---------|-----------------|
| `client.erc20` | Token approvals, balances, transfers | Write ops only |
| `client.optionBook` | Fill/cancel orders, get fees, preview fills | Write ops only |
| `client.api` | Fetch orders, positions, stats | No |
| `client.optionFactory` | RFQ lifecycle management | Write ops only |
| `client.option` | Position management, payouts | Write ops only |
| `client.events` | Query blockchain events (OfferMade, QuotationRequested) | No |
| `client.ws` | Real-time WebSocket subscriptions | No |
| `client.pricing` | Option pricing, Greeks | No |
| `client.mmPricing` | Market maker pricing with fee adjustments | No |
| `client.rfqKeys` | ECDH keypair management for sealed-bid RFQ encryption | No |
| `client.collar` | Collar loans (capped-upside, zero-interest). Pricing/estimation works today; write methods throw `NETWORK_UNSUPPORTED` until `CollarLoanCoordinator` is deployed on Base. | Write ops only |
| `client.utils` | Decimal conversions, payoffs | No |

---

## Referrer Fee Sharing

The SDK supports a **referrer address** for fee sharing on order fills. When a referrer is set, a portion of the trading fees is allocated to the referrer.

```typescript
// Option 1: Set referrer at client initialization (applies to all fills)
const client = new ThetanutsClient({
  chainId: 8453,
  provider,
  signer,
  referrer: '0x92b8ac05b63472d1D84b32bDFBBf3e1887331567',
});

// All fillOrder calls will use this referrer automatically
await client.optionBook.fillOrder(order);

// Option 2: Pass referrer per fill call (overrides client default)
await client.optionBook.fillOrder(order, undefined, '0xYourReferrerAddress');

// Option 3: Use encode methods (for viem/wagmi/AA wallets)
const { to, data } = client.optionBook.encodeFillOrder(
  order,
  collateralAmount,
  '0x92b8ac05b63472d1D84b32bDFBBf3e1887331567'
);
const hash = await walletClient.sendTransaction({ to, data });

// Query referrer fee split
const feeBps = await client.optionBook.getReferrerFeeSplit('0x...');
console.log(`Referrer fee: ${feeBps} bps`);

// Query accumulated fees
const fees = await client.optionBook.getFees(usdcAddress, '0x...');
console.log(`Accumulated fees: ${fees}`);
```

If no referrer is provided, the zero address (`0x000...`) is used (no fee sharing).

---

## RFQ Key Management

The SDK uses ECDH (Elliptic Curve Diffie-Hellman) key pairs for encrypted offers in the RFQ system. Keys are automatically persisted based on your environment:

| Environment | Default Storage | Persistence |
|-------------|-----------------|-------------|
| **Node.js** | `FileStorageProvider` | Keys saved to `.thetanuts-keys/` directory |
| **Browser** | `LocalStorageProvider` | Keys saved to localStorage |

### Automatic Key Management

```typescript
// Keys are automatically persisted - no configuration needed
const keyPair = await client.rfqKeys.getOrCreateKeyPair();
console.log('Public Key:', keyPair.compressedPublicKey);
// Keys are saved automatically and survive process restarts
```

### Key Backup Warning

> **IMPORTANT**: Back up your RFQ private keys! Keys are stored in `.thetanuts-keys/` with secure permissions. If lost, you cannot decrypt offers made to your public key. There is no recovery mechanism.

---

## Real-Time WebSocket Subscriptions

Subscribe to live updates for orders and prices:

```typescript
const client = new ThetanutsClient({ chainId: 8453, provider });

// 1. Connect
await client.ws.connect();

// 2. Subscribe to order updates
const unsubOrders = client.ws.subscribeOrders((update) => {
  console.log(`Order ${update.event}:`, update);
});

// 3. Subscribe to price updates for ETH
const unsubPrices = client.ws.subscribePrices((update) => {
  console.log(`ETH price: $${update.price}`);
}, 'ETH');

// 4. Handle connection state changes
const unsubState = client.ws.onStateChange((state) => {
  console.log(`WebSocket state: ${state}`);
});

// 5. Disconnect when done
// unsubOrders(); unsubPrices(); unsubState();
// client.ws.disconnect();
```

The WebSocket module auto-reconnects by default (up to 10 attempts).

---

## Error Handling

All SDK methods throw `ThetanutsError` with typed error codes:

```typescript
import { isThetanutsError, OrderExpiredError, InsufficientAllowanceError } from '@thetanuts-finance/thetanuts-client';

try {
  await client.optionBook.fillOrder(order, 10_000000n);
} catch (error) {
  if (error instanceof OrderExpiredError) {
    console.log('Order expired, fetching fresh orders...');
    const freshOrders = await client.api.fetchOrders();
  } else if (error instanceof InsufficientAllowanceError) {
    console.log('Approving tokens first...');
    await client.erc20.ensureAllowance(usdcAddress, optionBookAddress, amount);
  } else if (isThetanutsError(error)) {
    switch (error.code) {
      case 'SLIPPAGE_EXCEEDED': console.log('Price moved too much'); break;
      case 'INSUFFICIENT_BALANCE': console.log('Not enough tokens'); break;
      case 'SIGNER_REQUIRED': console.log('Signer required'); break;
      case 'CONTRACT_REVERT': console.log('Contract call failed'); break;
    }
  }
}
```

### Error Codes

| Code | Description |
|------|-------------|
| `ORDER_EXPIRED` | Order has expired or will expire soon |
| `SLIPPAGE_EXCEEDED` | Price moved beyond tolerance |
| `INSUFFICIENT_ALLOWANCE` | Token approval needed |
| `INSUFFICIENT_BALANCE` | Not enough tokens |
| `NETWORK_UNSUPPORTED` | Network not supported |
| `HTTP_ERROR` | API request failed |
| `CONTRACT_REVERT` | Smart contract call failed |
| `INVALID_PARAMS` | Invalid parameters provided |
| `ORDER_NOT_FOUND` | Order not found |
| `SIZE_EXCEEDED` | Fill size exceeds available |
| `SIGNER_REQUIRED` | Signer needed for transaction |
| `WEBSOCKET_ERROR` | WebSocket connection error |

---

## SDK Configuration Options

```typescript
interface ThetanutsClientConfig {
  chainId: 8453;                    // Required: Chain ID
  provider: Provider;               // Required: ethers.js provider
  signer?: Signer;                  // Optional: For transactions
  referrer?: string;                // Optional: Referrer address for fees
  apiBaseUrl?: string;              // Optional: Override API URL
  indexerApiUrl?: string;           // Optional: Override indexer URL
  pricingApiUrl?: string;           // Optional: Override pricing URL
  wsUrl?: string;                   // Optional: Override WebSocket URL
  env?: 'dev' | 'prod';             // Optional: Environment (default: prod)
  logger?: ThetanutsLogger;         // Optional: Custom logger
  keyStorageProvider?: StorageProvider; // Optional: Custom RFQ key storage
}
```

### Custom Logger

```typescript
const client = new ThetanutsClient({
  chainId: 8453,
  provider,
  logger: {
    debug: (msg, meta) => myLogger.debug(msg, meta),
    info: (msg, meta) => myLogger.info(msg, meta),
    warn: (msg, meta) => myLogger.warn(msg, meta),
    error: (msg, meta) => myLogger.error(msg, meta),
  },
});
```

---

## Production Checklist

Before deploying to production, verify the following:

- **RPC Provider**: Use a reliable provider (Alchemy, Infura, QuikNode) instead of public `https://mainnet.base.org` which has strict rate limits
- **Referrer Configuration**: Set the `referrer` address to earn fee-sharing revenue on fills
- **Error Logging**: Pass a custom `logger` to capture errors in Sentry/Datadog
- **Gas Buffer**: SDK adds 20% gas buffer for Account Abstraction wallets (Coinbase Smart Wallet, Safe)
- **Collateral Approval Flow**: Always call `client.erc20.ensureAllowance()` before `fillOrder()`
- **WebSocket Reconnection**: Auto-reconnects up to 10 attempts by default
- **Order Expiry Checks**: Check `order.expiry` before filling to avoid wasted gas estimates
- **RFQ Key Backup**: Back up `.thetanuts-keys/` directory — lost keys cannot decrypt past offers

---

## Decimal Handling

The SDK provides utilities for safe decimal conversions:

| Type | Decimals | Example |
|------|----------|---------|
| USDC | 6 | `1000000` = 1 USDC |
| WETH | 18 | `1000000000000000000` = 1 WETH |
| cbBTC | 8 | `100000000` = 1 cbBTC |
| Strike/Price | 8 | `185000000000` = $1850 |

```typescript
// Convert to on-chain values
const usdc = client.utils.toBigInt('100.5', 6);   // 100500000n
const strike = client.utils.strikeToChain(1850);  // 185000000000n

// Convert from on-chain values
const display = client.utils.fromBigInt(100500000n, 6);  // '100.5'
const price = client.utils.strikeFromChain(185000000000n); // 1850
```

---

## Example Conversations

### "I just installed this, what do I do?"

**Agent:** [Triggers onboarding flow]
1. Runs `wallet-discover.js` → no wallet found
2. Enters onboarding mode
3. Guides through wallet creation
4. Shows balance and funding instructions
5. Fetches market news via WebSearch
6. Asks risk preference
7. Makes first strategy suggestion

```
Agent: Welcome to Thetanuts Options Trading! Let's get you set up.

I see you don't have a wallet configured yet.
Would you like to create a new wallet or import an existing one?

[After wallet creation...]

Your wallet: 0x7a3F...9e2B
Chain: Base Mainnet
Balance: 0 ETH | 0 USDC | 0 WETH

To start trading, you'll need to fund your wallet:
• ETH on Base for gas fees (bridge via bridge.base.org)
• USDC for PUT options | WETH for CALL options

Once funded, tell me:
1. What's your risk preference? (Low / Medium / High)
2. Are you bullish, bearish, or neutral on ETH?

I'll check the latest market news and recommend a strategy!
```

### "What's happening in crypto that I should trade?"

**Agent:**
1. Uses WebSearch: `"crypto market news today"`
2. Uses WebSearch: `"ethereum bitcoin price catalyst this week"`
3. Summarizes findings and maps to strategy
4. Asks risk preference
5. Recommends with Risk Summary Card

```
Agent: Let me check the latest market news...

Market Context:
• Fed meeting tomorrow — markets expect rate hold, dovish tone → BULLISH
• Large BTC options expiry ($2.3B) on Friday → potential pin risk → NEUTRAL
• ETH Layer-2 TVL hitting ATH → positive sentiment → BULLISH

Overall bias: MODERATELY BULLISH with near-term volatility expected

What risk level are you comfortable with?

LOW:  Iron Condor — collect premium, profit if ETH stays in range
      Good for the expected range-bound action before Fed meeting
MEDIUM: Call Spread — capped upside play on the bullish bias
      Benefit from dovish Fed without unlimited downside
HIGH: Vanilla Call — unlimited upside if Fed sparks a rally
      Lose full premium if market sells the news
```

### "Show me LOW risk strategies"

**Agent:**
1. Fetches current prices and MM pricing
2. Filters for LOW risk structures
3. Shows Risk Summary Cards for each

```
Agent: Here are the LOW RISK strategies available right now:

┌────────────────────────────────────────────────────┐
│ Strategy:  Iron Condor (ETH)                       │
│ Risk:      LOW                                     │
│ Direction: NEUTRAL                                 │
├────────────────────────────────────────────────────┤
│ Strikes:   $1800 / $1900 / $2100 / $2200           │
│ Max Loss:  $85/contract                            │
│ Max Gain:  $15/contract (premium collected)        │
│ Win Zone:  ETH stays between $1900-$2100           │
│ Current:   ETH $2,050 (right in the sweet spot!)   │
│ Collateral: ~$100 USDC per contract                │
└────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────┐
│ Strategy:  Put Butterfly (ETH)                     │
│ Risk:      LOW                                     │
│ Direction: NEUTRAL (target $2,000)                 │
├────────────────────────────────────────────────────┤
│ Strikes:   $1950 / $2000 / $2050                   │
│ Max Loss:  ~$3/contract (premium paid)             │
│ Max Gain:  ~$47/contract (if pinned at $2,000)     │
│ Win Zone:  ETH settles near $2,000                 │
│ Collateral: ~$50 USDC per contract                 │
└────────────────────────────────────────────────────┘

Which strategy interests you? Or want to see MEDIUM or HIGH risk options?
```

### "How did my trades do?"

**Agent:**
1. Runs `get-positions.ts` with user's wallet address
2. Separates expired from active positions
3. Computes ROI for each expired position
4. Presents portfolio performance summary

```
Agent: Let me check your trading performance...

Portfolio Performance Summary
══════════════════════════════════════════════════════════
Wallet: 0x7a3F...9e2B
Period: Mar 14, 2026 to Apr 11, 2026

REALIZED P&L (Expired Positions)
┌───────────────────────┬──────┬──────────┬─────────┐
│ Trade                 │ Side │ P&L      │ ROI     │
├───────────────────────┼──────┼──────────┼─────────┤
│ ETH-28MAR-2000-P      │ SELL │ +$12.50  │ +6.25%  │
│ ETH-28MAR-2100-C      │ BUY  │ -$8.00   │ -100%   │
│ ETH-04APR-1900/1800-PS│ BUY  │ +$45.00  │ +150%   │
├───────────────────────┼──────┼──────────┼─────────┤
│ TOTAL                 │      │ +$49.50  │         │
└───────────────────────┴──────┴──────────┴─────────┘

Win rate: 2/3 (66.7%)
Average P&L per trade: +$16.50
Best trade:  ETH PUT_SPREAD (+$45.00, +150% ROI)
Worst trade: ETH CALL (-$8.00, expired worthless)

Insight: Your MEDIUM risk spread trades outperformed the HIGH risk
vanilla call. Consider focusing on spreads for better risk-adjusted returns.

OPEN POSITIONS
┌───────────────────────┬──────┬───────────┬──────────┐
│ Trade                 │ Side │ Contracts │ Expiry   │
├───────────────────────┼──────┼───────────┼──────────┤
│ ETH-18APR-2000-P      │ BUY  │ 0.5       │ Apr 18   │
└───────────────────────┴──────┴───────────┴──────────┘

Want me to analyze what your open position might settle at?
```

---

### "Show me ETH puts"

**User:** Show me ETH puts

**Agent:**
1. Fetches MM pricing: `npx tsx scripts/get-mm-pricing.ts ETH --type PUT`
2. Shows available strikes, expiries, bid/ask prices
3. Asks which one interests you

### "I want to sell a put at $1900 with 10 USDC"

**Agent's Decision Process:**
1. Check orderbook for $1900 PUT bids
2. Found liquidity? → "Use Orderbook - there's a BID at $1900"
3. No liquidity? → "Use RFQ - I'll request a quote for you"

**If Orderbook:**
```
Agent: There's a BID at $1900. Let me fill it for you.
1. Previews: "You'll sell ~0.005 contracts, receive ~$X premium"
2. Asks: "Proceed?"
3. Executes fill
```

**If RFQ:**
```
Agent: No orderbook liquidity at $1900. I'll submit an RFQ.
1. Builds RFQ for ETH-1900-PUT sell
2. Approves USDC if needed
3. Submits RFQ
4. "RFQ submitted. MMs have 45 seconds to respond."
```

### "Check my positions"

**Agent:**
1. Gets wallet address from discover
2. Runs: `npx tsx scripts/get-positions.ts 0xYourAddress`
3. Shows open positions with current P&L

### "I have $50 and I'm bearish on ETH, recommend a strategy"

**Agent's Decision Process:**
1. WebSearch for market news → confirms bearish sentiment
2. User has small collateral ($50) → Consider spreads for efficiency
3. User is bearish → PUT direction
4. Ask risk level → user says "medium"
5. Recommendation: **PUT_SPREAD** (MEDIUM RISK)

**Agent:**
```
Market Context:
• ETH down 3% on regulatory concerns → BEARISH
• Overall market sentiment weak → confirms bearish view

With $50 and a bearish view at MEDIUM risk, I recommend a PUT SPREAD:

┌────────────────────────────────────────────────────┐
│ Strategy:  PUT_SPREAD                              │
│ Risk:      MEDIUM                                  │
│ Direction: BEARISH                                 │
├────────────────────────────────────────────────────┤
│ Max Loss:  $50 (your full collateral)              │
│ Max Gain:  $50 (spread width - premium)            │
│ Break-even: ~$1892                                 │
│ Win Zone:  ETH below $1900 at expiry               │
│ Collateral: $50 USDC -> 0.5 contracts              │
│             (20x more than vanilla PUT at 0.026)   │
└────────────────────────────────────────────────────┘

Available strikes for tomorrow's expiry:
• PUT_SPREAD $1950/$1850 - Bid: $12/contract
• PUT_SPREAD $1900/$1800 - Bid: $8/contract

Which spread would you like?

Want HIGH risk instead? Vanilla PUT gives unlimited profit but only 0.026 contracts.
Want LOW risk instead? Put Butterfly costs ~$3 with $47 max gain.
```

### "I think ETH will stay around $2000 this week"

**Agent's Decision Process:**
1. WebSearch for news → no major catalysts, range-bound expected
2. User expects neutral/range-bound market
3. Ask risk level → user says "low"
4. Check collateral: $30 → butterfly is most efficient
5. Recommendation: **CALL_FLY** (LOW RISK)

**Agent:**
```
Market Context:
• No major catalysts this week → NEUTRAL
• Options expiry Friday with large OI at $2000 → pin risk → NEUTRAL

With $30 and a neutral view, here's my LOW RISK recommendation:

┌────────────────────────────────────────────────────┐
│ Strategy:  CALL_FLY (Butterfly)                    │
│ Risk:      LOW                                     │
│ Direction: NEUTRAL (target $2,050)                 │
├────────────────────────────────────────────────────┤
│ Strikes:   2000 / 2050 / 2100                      │
│ Max Loss:  ~$5/contract (premium paid)             │
│ Max Gain:  ~$45/contract (at exactly $2050)        │
│ Break-even: $2005 - $2095                          │
│ Collateral: $30 -> ~6 contracts                    │
└────────────────────────────────────────────────────┘

Why butterfly (LOW risk)?
• Cheapest way to play range-bound (more contracts per dollar)
• Max loss is tiny (~$5/contract)
• If ETH pins near $2050, each contract pays ~$45

Want MEDIUM risk? A Condor ($100+) gives a wider profit zone.

Build this RFQ? (y/n)
```

### "I want to sell premium and collect income"

**Agent's Decision Process:**
1. WebSearch for news → range-bound market expected
2. User wants to sell premium → Income strategy
3. Risk level: LOW (income/premium selling = defined risk)
4. If neutral → **IRON_CONDOR**

**Agent:**
```
Market Context:
• Market consolidating after rally → NEUTRAL
• No major events this week → supports range-bound play

For premium selling, I recommend an IRON CONDOR (LOW RISK):

┌────────────────────────────────────────────────────┐
│ Strategy:  IRON_CONDOR (sell)                      │
│ Risk:      LOW                                     │
│ Direction: NEUTRAL (profit if range-bound)         │
├────────────────────────────────────────────────────┤
│ Strikes:   $1800 / $1900 / $2100 / $2200           │
│ Max Loss:  $85/contract (if ETH exits range)       │
│ Max Gain:  $15/contract (premium collected)        │
│ Win Zone:  ETH stays between $1900-$2100           │
│ Current:   ETH $2,000 (right in the middle!)       │
│ Collateral: ~$100 USDC per contract                │
└────────────────────────────────────────────────────┘

This strategy profits ~60-70% of the time in range-bound markets.
You collect $15 premium and risk $85 if wrong.

Is ETH likely to stay between $1900-$2100? Let me build this RFQ.
```

---

## Output Formatting & UX Guidelines

### Progressive Disclosure

Tailor detail level to the user's experience:

| User Type | How to Detect | What to Show |
|-----------|---------------|-------------|
| **New user** | First session, no wallet, asks basic questions | Simplified info, no SDK details, guide step-by-step |
| **Returning user** | Has wallet, has traded before | Relevant data for their question, skip basics |
| **Advanced user** | Asks about multi-strike, SDK, specific params | Full technical detail, contract addresses, raw data |

### Formatting Standards

**ASCII Table Alignment Rules (CRITICAL):**
- The `┌───┐` top border, `├───┤` divider, and `└───┘` bottom border MUST all be the **exact same width**
- Every content line `│ ... │` MUST have the right `│` aligned exactly under the `┐` corner
- Count characters carefully: if the border is 54 `─` chars wide (56 total with `┌┐`), every content line must be exactly 54 chars between the `│` borders
- Pad content lines with spaces on the right so the closing `│` always aligns
- If content is too long for the box, shorten it or wrap to a new line (indented, still inside the `│` borders)
- Use light box-drawing only: `┌ ┐ └ ┘ ─ │ ├ ┤ ┼ ┬ ┴` (never heavy/double: `═ ║ ╔`)

**For strategy recommendations** — Always include the Risk Summary Card (see "Risk-Categorized Strategy Recommendations" section for the full template with all fields: Strategy, Risk Level, Direction, Max Loss, Max Gain, Break-even, Win Zone, Collateral).

**For price/market data** — Use compact tables:
```
ETH Options (PUT) — Current Price: $2,050
┌────────────┬─────────┬────────┬────────┐
│ Strike     │ Expiry  │ Bid    │ Ask    │
├────────────┼─────────┼────────┼────────┤
│ $1,900     │ Apr 25  │ $8.50  │ $12.00 │
│ $2,000     │ Apr 25  │ $25.00 │ $30.00 │
└────────────┴─────────┴────────┴────────┘
```

**For trade confirmations** — Clear summary before execution:
```
Trade Summary
═════════════
Action: Buy PUT_SPREAD
Risk Level: MEDIUM
Strikes: $1900 / $1800
Expiry: Apr 25, 2026
Contracts: 1.0
Cost: ~$15 USDC
Max Loss: $15 | Max Gain: $85

Confirm? (yes/no)
```

**For errors** — Never show raw JSON to the user:
- Translate error codes to plain English
- Always suggest a corrective action
- Example: Instead of `{"error": "INSUFFICIENT_ALLOWANCE"}` → "You need to approve USDC spending first. Want me to do that?"

### MCP Tool Usage for Enhanced UX

| Tool | When to Use | Example |
|------|------------|---------|
| **WebSearch** | Before every strategy recommendation (fetch market news) | `"crypto market news today"` |
| **WebFetch** | Drill into a specific article or data source from WebSearch results | Fetch full article content |
| **context7** | When user asks about SDK features or encounters an unfamiliar error | Resolve `thetanuts-finance/thetanuts-client`, then query docs |

### Context7 for SDK Documentation

When a user asks a technical question about the Thetanuts SDK:
1. Use context7 `resolve-library-id` to find `thetanuts-finance/thetanuts-client`
2. Use context7 `query-docs` with the specific topic (e.g., "fillOrder", "WebSocket", "error handling")
3. Provide accurate, up-to-date answers from official documentation

---

## Commands Reference

### Wallet Commands

| Command | Description |
|---------|-------------|
| `node scripts/wallet-discover.js` | Check if wallet configured, show addresses |
| `node scripts/wallet-create.js` | Generate new wallet |
| `node scripts/wallet-import.js --seed-file /path` | Import existing seed |
| `node scripts/wallet-balance.js --chain base-mainnet` | Check balance |
| `node scripts/wallet-select.js --family evm --chain base-mainnet` | Set active chain |

### Market Data Commands

| Command | Description |
|---------|-------------|
| `npx tsx scripts/get-prices.ts` | Get BTC/ETH prices |
| `npx tsx scripts/get-mm-pricing.ts ETH --type PUT` | Get MM option quotes |
| `npx tsx scripts/fetch-orders.ts --type PUT` | Fetch orderbook |
| `npx tsx scripts/check-orderbook.ts --underlying ETH --type PUT --strike 1900 --expiry <ts> --direction sell` | Check orderbook liquidity (run FIRST before trading) |

### Trading Commands

| Command | Description |
|---------|-------------|
| `npx tsx scripts/fill-order.ts --order-index 0 --collateral 10 --execute` | Fill orderbook order (reads `WDK_SEED` env) |
| `npx tsx scripts/build-rfq.ts --underlying ETH --type PUT --strike 1900 --expiry <ts> --contracts 0.1 --direction buy` | Build vanilla RFQ (45s deadline) |
| `npx tsx scripts/build-rfq.ts --underlying ETH --type CALL --strikes 2000,2100 --expiry <ts> --contracts 1 --direction buy` | Build multi-strike RFQ (spread/fly/condor) |
| `npx tsx scripts/approve-token.ts --token <addr> --spender <addr> --amount <n>` | Approve tokens (exact amount; add `--max --confirm-max` for unlimited) |
| `npx tsx scripts/send-transaction.ts --to <addr> --data <hex>` | Send transaction (reads `WDK_SEED` env) |
| `npx tsx scripts/check-rfq-fill.ts --address <wallet> --ticker <expected> --since <ts>` | Verify RFQ fill status |

### Position Commands

| Command | Description |
|---------|-------------|
| `npx tsx scripts/get-positions.ts <address>` | Get open positions |
| `npx tsx scripts/calculate-payout.ts --type PUT --strike 1900 --settlement 1800 --contracts 1` | Calculate payoff |

---

## Contract Addresses (Base Mainnet, chain 8453)

> **Source of truth:** these mirror `@thetanuts-finance/thetanuts-client@^0.2.4` `CHAIN_CONFIGS_BY_ID[8453]`. Do not hard-code addresses in scripts — read them from `client.chainConfig` so future SDK upgrades stay in sync. If you ever see a mismatch, the SDK wins.

### Core Contracts — Base_r12 (deployed 2026-05-05, block 45601440)

| Contract | Address |
|----------|---------|
| **OptionBook** | `0x1bDff855d6811728acaDC00989e79143a2bdfDed` |
| **OptionFactory** | `0x8118daD971dEbffB49B9280047659174128A8B94` |
| **TWAP Consumer** | `0xE909fb38767e0ac5F7a347DF9Dd4222217E10816` |

### Tokens

| Token | Address | Decimals |
|-------|---------|----------|
| USDC | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` | 6 |
| WETH | `0x4200000000000000000000000000000000000006` | 18 |
| cbBTC | `0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf` | 8 |
| cbDOGE | `0x73c7A9C372F31c1b1C7f8E5A7D12B8735c817C79` | 8 |
| cbXRP | `0x7B2Cd9EA5566c345C9cdbcF58f5E211a0dB47444` | 6 |
| aBasWETH | `0xD4a0e0b9149BCee3C920d2E00b5dE09138fd8bb7` | 18 |
| aBascbBTC | `0xBdb9300b7CDE636d9cD4AFF00f6F009fFBBc8EE6` | 8 |
| aBasUSDC | `0x4e65fE4DbA92790696d040ac24Aa414708F5c0AB` | 6 |

### Option Implementations (Base_r12)

| Type | Address |
|------|---------|
| PUT | `0x7355EB92dfb0503DB558a70c10843618932ab290` |
| INVERSE_CALL | `0xE6c5756b0289e3f0994CB12eb8aB71Cd903Ed0Ea` |
| LINEAR_CALL | `0x051791df68223AE173Fade5217C48875e36eef61` |
| CALL_SPREAD | `0xfaeD63f7040E65b79cF0Ae29706fDc423eE249A9` |
| PUT_SPREAD | `0x02Fe0d9635e0139DBB3768a5d5Db404Fd84d9134` |
| INVERSE_CALL_SPREAD | `0x7Be48100b1B0349528A96D64953295Cd0Bbe4B70` |
| CALL_FLY | `0xa1d5f6b16A2e7f298F8d2cDF78F7779B4A20C4C2` |
| PUT_FLY | `0x4fd2C6D271cC6FF3EbD2027da9815a0608d03AA3` |
| CALL_CONDOR | `0x14476CF2ea9F7C448100F061670E390f17c78817` |
| PUT_CONDOR | `0xC742E422c7BB43A7FDe1CEF47997bC9D5b543cDD` |
| IRON_CONDOR | `0x9ebd7E23AfD52a48F557523019285EfEF2170D59` |
| RANGER | `0x9980ec85bc6fE07340adb36c76FA093bb6D4FcBc` |
| CALL_LOAN | `0x7c444A2375275DaB925b32493B64a407eE955DEd` |
| PHYSICAL_CALL | `0x8c56100caE246f7daa4BC1EC4d1477d71178c563` |
| PHYSICAL_PUT | `0x6aD53DD058bea004829cCf58a282C21a7Df02DcA` |

Physical multi-leg variants (`PHYSICAL_CALL_SPREAD`, `PHYSICAL_PUT_SPREAD`, `PHYSICAL_*_FLY`, `PHYSICAL_*_CONDOR`, `PHYSICAL_IRON_CONDOR`) are placeholders — the SDK throws if a quote routes through them.

### Legacy Option Implementations (recognized for existing positions)

The SDK's `optionImplementations` map still resolves these for parsing pre-r12 positions/events. Do **not** route new RFQs through them — quotes will reach a deprecated contract.

| Type | 8453_v6 (legacy) | Base_r10 (legacy) |
|------|------------------|-------------------|
| PUT | `0xF480F636301d50Ed570D026254dC5728b746A90F` | `0x64b4b21bf0845c79661f60ed48aa24d54bf74bb5` |
| INVERSE_CALL | `0x3CeB524cBA83D2D4579F5a9F8C0D1f5701dd16FE` | `0x1fdec69e5ac4fa9cb7092f381c2dd5688759d43c` |
| CALL_SPREAD | `0x4D75654bC616F64F6010d512C3B277891FB52540` | `0x2db5afa04aee616157beb53b96612947b3d13ee3` |
| PUT_SPREAD | `0xC9767F9a2f1eADC7Fdcb7f0057E829D9d760E086` | `0x571471b2f823cc6b5683fc99ac6781209bc85f55` |
| CALL_FLY | `0xD8EA785ab2A63a8a94C38f42932a54A3E45501c3` | `0xb727690fdd4bb0ff74f2f0cc3e68297850a634c5` |
| PUT_FLY | `0x1fE24872Ab7c83BbA26Dc761ce2EA735c9b96175` | `0x78b02119007f9efc2297a9738b9a47a3bc3c2777` |
| CALL_CONDOR | `0xbb5d2EB2D354D930899DaBad01e032C76CC3c28f` | `0x7d3c622852d71b932d0903f973caff45bcdba4f1` |
| PUT_CONDOR | `0xbdAcC00Dc3F6e1928D9380c17684344e947aa3Ec` | `0x5cc960b56049b6f850730facb4f3eb45417c7679` |
| IRON_CONDOR | `0x494Cd61b866D076c45564e236D6Cb9e011a72978` | `0xb200253b68fbf18f31d813aecef97be3a6246b79` |
| PHYSICAL_CALL | `0x07032ffb1df85eC006Be7c76249B9e6f39b60F32` | `0x025a8ef95f8939ffdba6a45973a28695846e9e45` |
| PHYSICAL_PUT | `0xAC5eCA7129909dE8c12e1a41102414B5a5f340AA` | `0x2d283d7ade2896d98331496ee761f15ed1d6a699` |

### Price Feeds (Chainlink)

| Asset | Address |
|-------|---------|
| ETH | `0x71041dddad3595F9CEd3DcCFBe3D1F4b0a16Bb70` |
| BTC | `0x64c911996D3c6aC71f9b455B1E8E7266BcbD848F` |
| SOL | `0x975043adBb80fc32276CbF9Bbcfd4A601a12462D` |
| DOGE | `0x8422f3d3CAFf15Ca682939310d6A5e619AE08e57` |
| XRP | `0x9f0C1dD78C4CBdF5b9cf923a549A201EdC676D34` |
| BNB | `0x4b7836916781CAAfbb7Bd1E5FDd20ED544B453b1` |
| PAXG | `0x5213eBB69743b85644dbB6E25cdF994aFBb8cF31` |
| AVAX | `0xE70f2D34Fd04046aaEC26a198A35dD8F2dF5cd92` |

---

## Updates

Updates are **user-initiated only** — the agent must never run `update.sh`
automatically. Updates change code that signs transactions, so they require
explicit consent each time.

To check for or apply an update:

```bash
bash scripts/update.sh
```

The agent should surface the script's full output, summarize any version
change, and ask the user to confirm before any code-changing step runs.

Optional flags:
- `REFRESH_WDK_DEPS=1` - Refresh dependencies from lockfile
- `UPGRADE_WDK_DEPS=1` - Upgrade dependency versions
- `RESTART_WDK_RUNTIME=1` - Best-effort restart of WDK runtime

Updates NEVER modify wallet secrets (`.env`, `WDK_SEED`).

---

## Ticker Format

Options use: `{UNDERLYING}-{EXPIRY}-{STRIKE}-{TYPE}`

Examples:
- `ETH-28MAR26-2500-P` = ETH Put, $2500 strike, March 28 2026 expiry
- `BTC-28MAR26-95000-C` = BTC Call, $95000 strike, March 28 2026 expiry

---

## Network

- **Chain**: Base Mainnet (Chain ID 8453)
- **Collateral**: USDC (6 decimals), WETH (18 decimals), cbBTC (8 decimals)
- **Strikes**: 8 decimals internally
- **Expiry**: 8:00 UTC on expiry date
