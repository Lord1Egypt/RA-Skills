---
name: rugcheck
description: >
  Analyze Solana tokens for rug pull risks using the RugCheck API (rugcheck.xyz).
  Use when asked to check a Solana token safety, risk score, liquidity, holder
  distribution, metadata mutability, or insider trading patterns. Also use for
  discovering trending, new, or recently verified Solana tokens. Triggers on
  token check, rug check, token safety, Solana token analysis, is this token safe,
  token risk score, LP locked, holder concentration.
---

# RugCheck — Solana Token Risk Analysis

Analyze any Solana token by mint address using the free RugCheck API. No API key required for read endpoints.

## Quick Start

```bash
# Get risk summary (score + flags)
bash scripts/rugcheck.sh summary <MINT_ADDRESS>

# Get full detailed report (holders, markets, metadata, LP)
bash scripts/rugcheck.sh report <MINT_ADDRESS>
```

## Script Reference

Run `bash scripts/rugcheck.sh help` for all commands:

| Command | Description |
|---------|-------------|
| `summary <mint>` | Risk score (0-100 normalized), risk flags, LP lock % |
| `report <mint>` | Full report: metadata, holders, markets, creator info |
| `insiders <mint>` | Insider/connected wallet graph |
| `lockers <mint>` | LP vault/locker info (locked liquidity details) |
| `votes <mint>` | Community votes on the token |
| `leaderboard` | Top voters/analysts on the platform |
| `domains` | Registered Solana domains |
| `trending` | Most voted tokens in past 24h |
| `new` | Recently detected tokens |
| `recent` | Most viewed tokens in past 24h |
| `verified` | Recently verified tokens |

## Interpreting Results

### Summary Response

Key fields from `/v1/tokens/{mint}/report/summary`:

- **`score_normalised`** — Risk score 0-100. Higher = riskier. Below 1000 raw score ≈ "Good".
  - 0-30: Low risk (Good)
  - 30-60: Medium risk (caution)
  - 60-100: High risk (danger)
- **`risks[]`** — Array of risk flags, each with:
  - `name`: Risk type (e.g. "Mutable metadata", "Low Liquidity", "Single holder ownership")
  - `level`: `"warn"` or `"danger"`
  - `value`: Human-readable detail (e.g. "$102.55", "40.00%")
  - `description`: Explanation
  - `score`: Raw risk contribution
- **`lpLockedPct`** — Percentage of LP tokens locked (0 = none locked, very risky)
- **`tokenProgram`** — SPL token program used
- **`tokenType`** — Token type classification

### Full Report Response

Additional fields from `/v1/tokens/{mint}/report`:

- **`tokenMeta`** — Name, symbol, URI, `mutable` flag, `updateAuthority`
- **`token`** — Supply, decimals, `mintAuthority`, `freezeAuthority`
- **`creator`** / `creatorBalance` — Token creator wallet and their current balance
- **`topHolders[]`** — Top holders with `address`, `owner`, `pct` (percentage), `uiAmount`
- **`markets[]`** — DEX markets/pools with liquidity data
- **`insiderNetworks`** — Connected insider wallet clusters

## Red Flag Checklist

When analyzing a token, flag these risks to the user:

1. **Mutable metadata** (`tokenMeta.mutable == true`) — Creator can change token name/image
2. **Low liquidity** (risk with `"Low Liquidity"` or check market data) — Easy to manipulate price
3. **High holder concentration** — Top 10 holders > 50% supply
4. **Single holder dominance** — One wallet holds >20% supply
5. **LP not locked** (`lpLockedPct == 0`) — Creator can pull liquidity anytime
6. **Mint authority exists** (`token.mintAuthority != null`) — Can mint infinite tokens
7. **Freeze authority exists** (`token.freezeAuthority != null`) — Can freeze wallets
8. **Few LP providers** — Only 1-2 wallets providing liquidity
9. **Low/zero trade volume** — No real market activity
10. **Creator holds large balance** — Creator still sitting on supply

## Presenting Results

Format findings clearly for the user. Example:

```
🔍 RugCheck Analysis: CLWDN (ClawdNation)
Mint: 3zvSRWfjPvcnt8wfTrKhgCtQVwVSrYfBY6g1jPwzfHJG

⚠️ Risk Score: 59/100 (Medium-High Risk)

🚩 Risk Flags:
  🔴 Low Liquidity — $102.55
  ⚠️ Single holder ownership — 40.00%
  ⚠️ High holder concentration — Top 10 hold >50%
  ⚠️ Low amount of holders
  ⚠️ Low LP providers
  ⚠️ Mutable metadata

🔓 LP Locked: 0% (NOT LOCKED)

📊 Top Holders:
  1. 40.0% — 3Y3g...p7rk
  2. 15.0% — 5bNH...4VGj
  3. 15.0% — 4dkX...Ncg6
  4. 10.0% — 8yY2...CKn8
  5. 10.0% — 2MT5...eB3h

Verdict: HIGH RISK — Multiple red flags. No locked liquidity,
concentrated holdings, mutable metadata. Exercise extreme caution.
```

## API Details

- **Base URL:** `https://api.rugcheck.xyz`
- **Auth:** None required for read endpoints
- **Rate limits:** Respect 429 responses; add 2-3 second delays between bulk queries
- **RugCheck web:** `https://rugcheck.xyz/tokens/<mint>` (link for users)

## Bulk Queries (requires auth)

These endpoints need a JWT from Solana wallet auth — not available for most agents:

- `POST /v1/bulk/tokens/summary` — Check multiple tokens at once
- `POST /v1/bulk/tokens/report` — Full reports for multiple tokens
