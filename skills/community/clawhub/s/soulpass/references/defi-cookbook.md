# DeFi & Trading Cookbook

Operational wisdom for DeFi on Solana via SoulPass CLI. For command syntax and parameters, run `soulpass --help` or `soulpass schema`.

## Table of Contents

1. [Swap Strategy](#swap-strategy)
2. [Reading Lend Positions](#reading-lend-positions)
3. [Token Risk Assessment](#token-risk-assessment)
4. [Recipes — Common DeFi Patterns](#recipes)
5. [High-Frequency Daemon](#high-frequency-daemon)
6. [Pitfalls & Safety](#pitfalls)
7. [Trading Strategies](#trading-strategies) — Meme coin safety, copy trading, signal execution

---

## Swap Strategy

### Slippage — When to Set What

Default slippage is **50 BPS (0.5%)**. Maximum: **500 BPS (5%)**.

| Pair type | Recommended slippage | Why |
|-----------|---------------------|-----|
| Stablecoin ↔ Stablecoin (USDC/USDT) | 10 BPS (0.1%) | Deep liquidity, minimal price movement |
| Major pairs (SOL/USDC) | 50 BPS (default) | Usually fine, but set explicit during volatility |
| Low-liquidity / new tokens | 100-300 BPS | Thin orderbooks cause larger price impact |
| Meme tokens / micro-caps | 300-500 BPS | Extreme volatility, pool depth varies wildly |

If a swap fails with slippage errors, increase incrementally — don't jump straight to 500.

### Mint Address Mode — Watch the Decimals

When using mint addresses instead of symbols, `--amount` switches to **atomic units** (lamports), not human-readable:

```bash
# Symbol mode: human-readable (1.5 SOL)
soulpass swap --from SOL --to USDC --amount 1.5

# Mint mode: atomic units (1.5 SOL = 1,500,000,000 lamports)
soulpass swap --from So11...112 --to EPjF...t1v --amount 1500000000
```

This is the #1 source of "swapped way too much/too little" errors. Always use symbols when available.

---

## Reading Lend Positions

`soulpass lend balance` returns fields that are easy to misread:

```json
{
  "fTokenBalance": "100500000",
  "estimatedValue": "101200000",
  "exchangeRate": 1.006965
}
```

- **fTokenBalance** — pool share tokens you hold (NOT the underlying amount)
- **estimatedValue** — actual underlying token amount in atomic units. Divide by `10^decimals` for human-readable (USDC: divide by 1,000,000)
- **exchangeRate** — if >1.0, yield has accrued. The difference from 1.0 is your earnings percentage

**Common mistake:** checking `soulpass balance` and thinking you can withdraw from lend. Lend balance and wallet balance are separate pools. Always check `soulpass lend balance` before withdrawing.

Note: `--amount` and `--all` are mutually exclusive on `lend withdraw` — use one or the other.

---

## Token Risk Assessment

Before interacting with unknown tokens, use `soulpass price` to check risk signals:

```bash
soulpass price <token-or-mint>
```

Look at these fields in the response:
- **verified: false** — token is not verified by Jupiter. Proceed with extreme caution
- **liquidity** — low liquidity means high slippage and potential rug risk
- **marketCap** — very low market cap tokens are higher risk

Rule of thumb: if `verified: false` AND `liquidity < 100000`, think twice before swapping into it.

---

## Recipes

These are common DeFi patterns you'll encounter. Each is a goal-oriented workflow, not a command reference.

### DCA (Dollar-Cost Averaging)

Goal: Buy SOL regularly regardless of price, reducing timing risk.

```
1. soulpass price SOL                              # check current price (optional, for logging)
2. soulpass swap --from USDC --to SOL --amount 50  # buy $50 worth
3. Repeat on a schedule (hourly, daily, weekly)
```

For automated DCA, use the daemon in a loop. The agent decides the interval and amount — there's no built-in scheduler, so the agent or a cron-style tool drives the timing.

### Take-Profit / Stop-Loss

Goal: Sell when price hits a target, protect against drops.

```
1. soulpass price SOL                              # check price
2. If price >= target: soulpass swap --from SOL --to USDC --amount <sell-amount>
3. If price <= stop-loss: soulpass swap --from SOL --to USDC --amount <all>
4. Otherwise: wait and check again
```

The agent implements the logic; soulpass provides price checks and execution. Use the daemon for frequent polling to avoid startup overhead.

### Yield Parking

Goal: Earn yield on idle funds, pull out when you need to trade.

```
1. soulpass balance --token USDC                   # check idle funds
2. soulpass lend deposit --amount 100 --token USDC # park in Jupiter Lend
3. ... time passes, yield accrues ...
4. soulpass lend balance --token USDC              # check position + earnings
5. soulpass lend withdraw --token USDC --all       # pull out when ready
6. soulpass swap --from USDC --to SOL --amount ... # trade with withdrawn funds
```

Key: always check `lend balance` (not `balance`) before withdrawing. They are separate pools.

### Portfolio Rebalance

Goal: Maintain a target allocation (e.g., 60% SOL / 40% USDC).

```
1. soulpass balance                                # SOL balance
2. soulpass balance --token USDC --usd             # USDC balance in USD
3. Calculate current ratio vs target
4. If over-allocated to SOL: soulpass swap --from SOL --to USDC --amount <delta>
5. If over-allocated to USDC: soulpass swap --from USDC --to SOL --amount <delta>
```

### Monitor and Act (Signal-Driven Trading)

Goal: React to signals from another tool (Birdeye, DexScreener, custom logic).

```
1. Other tool provides signal (e.g., "new token listed", "price crossed MA")
2. soulpass price <token>                          # verify signal, check risk
3. If verified: false OR liquidity < 100000 → skip (see Token Risk Assessment)
4. soulpass swap --from USDC --to <token> --amount <size> --slippage 300
5. soulpass tx --hash <sig>                        # verify execution
```

For high-frequency signals, use the daemon: `soulpass serve` → POST swaps via JSON-RPC.

---

## High-Frequency Daemon

For trading bots, batch payments, or anything calling soulpass in a loop, use the daemon to eliminate ~600ms startup overhead per call.

```bash
soulpass serve    # starts on port 8402
```

All methods use JSON-RPC format: `POST http://127.0.0.1:8402` with `{"jsonrpc":"2.0","method":"...","params":{...},"id":1}`.

**Available methods:** `price`, `balance`, `tx_status`, `swap`, `pay`, `batch` (up to 20 parallel SOL transfers), `cache_invalidate`.

### When to Use Daemon vs CLI

| Scenario | Use |
|----------|-----|
| One-off payment or swap | CLI (`soulpass pay/swap ...`) |
| 10+ operations in a loop | Daemon |
| Trading bot polling prices every few seconds | Daemon |
| Interactive agent session with occasional operations | CLI (simpler) |

The daemon keeps warm caches — after the first `price` call, subsequent calls are significantly faster.

---

## Pitfalls

### Gas: Authority Pays, Not Wallet

After 30 free sponsored transactions per month, gas comes from your **Authority address**, not your Wallet/Vault. If Authority runs out of SOL, all transactions fail — even if Wallet has plenty of SOL.

Check: `soulpass balance --address <authority-address>`

### Verify After Every Swap

Always check the tx hash after submission: `soulpass tx --hash <sig>`. Don't assume success from the CLI response alone — network congestion can cause transactions to land late or fail.

### Don't Confuse the Three Balance Pools

This is repeated from SKILL.md because it's that important:

```
soulpass balance           → Wallet (Vault) — your funds
soulpass lend balance      → Lend position — deposited yield funds
Authority address          → Gas — keeps transactions flowing
```

Checking the wrong pool before an operation is the #1 source of "insufficient balance" errors.

---

## Trading Strategies

Real-world strategies you can build with SoulPass. These are patterns — adapt them to your risk tolerance and market conditions.

### Meme Coin Safety Checklist

99% of Pump.fun launches rug pull or die within 48 hours. Before buying ANY unknown token, run this checklist:

```bash
# Step 1: Check token risk signals
soulpass price <token-or-mint>
```

**Red flags — DO NOT buy if:**
- `verified: false` AND `liquidity < 100000` — likely scam or dead token
- Mint authority not revoked (check via Solscan or RugCheck) — project can dilute your holdings
- Top 5 wallets hold >50% of total supply — pump-and-dump setup
- Token created less than 24 hours ago with no community
- No locked liquidity — developer can pull the rug at any time

**Acceptable risk indicators:**
- `verified: true` on Jupiter — token has passed basic checks
- `liquidity > 500000` — enough depth for reasonable trades
- Active community and social presence
- Mint authority revoked
- Liquidity locked

**Safe entry pattern:**

```bash
# 1. Risk check
soulpass price BONK

# 2. Start small — never more than 2-5% of balance on meme coins
soulpass swap --from USDC --to BONK --amount 10 --slippage 300

# 3. Verify execution
soulpass tx --hash <signature>

# 4. Monitor position
soulpass balance --token BONK
soulpass price BONK    # check periodically

# 5. Take profit when target hit — don't get greedy
soulpass swap --from BONK --to USDC --amount <position> --slippage 300
```

**Slippage for meme coins:** Use 200-500 BPS. Thin orderbooks cause large price impact. If a swap fails with slippage error, increase by 50 BPS increments — don't jump to 500.

### Copy Trading Strategy (Solana Whales)

Mirror trades from profitable Solana wallets. Tools like GMGN.ai, SolSqueezer, and Nansen help identify wallets with strong track records.

**Criteria for selecting wallets to follow:**
- ROI above 100%
- Win rate above 60%
- Not too many trades per day (avoids gambling patterns)
- Consistent over 30+ days (not just one lucky trade)

**Copy trading workflow:**

```bash
# Whale bought a token — you evaluate and follow

# 1. ALWAYS check token risk first
soulpass price <token>

# 2. Check your available balance
soulpass balance --token USDC

# 3. If risk is acceptable, follow with proportional size (1-5% of balance)
soulpass swap --from USDC --to <token> --amount 20 --slippage 200

# 4. Monitor price — exit when target hit or whale exits
soulpass price <token>

# 5. Exit
soulpass swap --from <token> --to USDC --amount <position> --slippage 200
```

**Risk management rules:**
- **Never risk more than 2-5%** of your balance per copy trade
- **Always check token risk** before following — whales can afford losses you can't
- **Latency matters** — whale data has delay. Check `soulpass price` before placing your order
- **Don't stack correlated positions** — if the whale is buying 5 meme coins, that's one bet, not five
- **Exit discipline** — if you can't track the whale's exit, set a time-based exit (e.g., sell after 4 hours)

For speed-critical copy trading, use the daemon (`soulpass serve`) to avoid 600ms CLI startup per call.

### Signal → Execution Pipeline

Connect external signals (whale trackers, social media sentiment, AI analysis) directly to SoulPass execution:

```bash
# === Generic signal execution loop ===

# Signal arrives: "BUY token X, size $20, slippage 200"

# 1. Pre-flight: risk check
soulpass price <token>
# If verified: false AND liquidity < 100000 → SKIP

# 2. Pre-flight: balance check
soulpass balance --token USDC

# 3. Execute
soulpass swap --from USDC --to <token> --amount 20 --slippage 200

# 4. Verify execution
soulpass tx --hash <signature>

# 5. Set exit criteria and monitor
soulpass price <token>    # poll periodically
# When target hit: exit
soulpass swap --from <token> --to USDC --amount <position> --slippage 200
```

For bots that poll every few seconds, use the daemon:

```bash
soulpass serve    # start daemon

# Price poll (cached, fast)
curl -s http://127.0.0.1:8402 -d '{"jsonrpc":"2.0","method":"price","params":{"tokens":["BONK"]},"id":1}'

# Execute swap
curl -s http://127.0.0.1:8402 -d '{"jsonrpc":"2.0","method":"swap","params":{"from":"USDC","to":"BONK","amount":"20","slippage":200},"id":1}'
```

### DCA Automation (Dollar-Cost Averaging)

Reduce timing risk by buying regularly regardless of price. The agent or a cron tool drives the schedule:

```bash
# === Daily DCA: buy $50 of SOL ===

# 1. Check price (for logging)
soulpass price SOL

# 2. Execute purchase
soulpass swap --from USDC --to SOL --amount 50

# 3. Verify
soulpass tx --hash <signature>

# Repeat daily/weekly/hourly via cron or agent loop
```

For high-frequency DCA (hourly), use the daemon to avoid startup overhead.

### Yield + Trading Hybrid

Park idle funds in Jupiter Lend while waiting for trading opportunities:

```bash
# 1. Deposit idle USDC into Jupiter Lend (earns ~6-10% APY)
soulpass lend deposit --amount 500 --token USDC

# 2. Wait for trading opportunity...

# 3. When signal arrives: withdraw and trade
soulpass lend withdraw --token USDC --all
soulpass swap --from USDC --to <target-token> --amount 100 --slippage 200

# 4. After exiting the trade, re-deposit idle funds
soulpass lend deposit --amount 500 --token USDC
```

This way your capital earns yield even when you're not actively trading.
