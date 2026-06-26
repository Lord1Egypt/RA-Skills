# Mainnet (pubnet) checklist

**Mainnet uses real money. Read this before flipping the network.**

## Network constants

```ts
// Passphrase
const PUBNET_PASSPHRASE = "Public Global Stellar Network ; September 2015";

// USDC SAC contract (pubnet)
const PUBNET_USDC_SAC = "CCW67TSZV3SSS2HXMBQ5JFGCKJNXKZM7UQUWUZPUTHXSTZLEO7SJMI75";

// XLM native SAC (pubnet) — only needed if paying in XLM
const PUBNET_XLM_SAC = "CAS3J7GYLGXMF6TDJBBYYSE3HQ6BBSMLNUQ34T6TZMYMW2EVH34XOWMA";

// CAIP-2
const PUBNET_CAIP2 = "stellar:pubnet";
```

## RPC providers (you need one — public RPCs rate-limit hard)

Public Soroban RPCs on mainnet are unreliable for production. Pick a paid provider:

| Provider | URL pattern | Notes |
|---|---|---|
| **Validation Cloud** | `https://mainnet.sorobanrpc.com` | Official SDF-curated; generous free tier |
| **Blockdaemon** | Custom URL after signup | Enterprise SLA |
| **QuickNode** | Custom URL after signup | Per-request pricing |
| **Nodies** | `https://stellar-mainnet.nodies.app` | Free-tier friendly |
| **Self-hosted** | `https://<your-rpc>` | Run `stellar-rpc` binary |

**Do not use testnet RPCs on mainnet or vice versa** — simulation will silently return junk.

## Preflight checklist before first mainnet run

- [ ] `--network pubnet` (this is the default, so omitting the flag is fine)
- [ ] `--rpc-url <provider>` set to a paid/reliable provider
- [ ] `--asset-sac CCW67TSZV3SSS2HXMBQ5JFGCKJNXKZM7UQUWUZPUTHXSTZLEO7SJMI75` (mainnet USDC) — **not the testnet one**
- [ ] Stellar account funded with **at least 2 XLM reserve** (minimum balance + trustline reserves)
- [ ] Trustline to mainnet USDC issuer (`GA5ZSEJYB37JRC5AVCIA5MOP4RHTM335X2KGX3IHOJAPP5RE34K4KZVN`) established — Classic Asset, not SAC.
- [ ] Funded with the USDC amount you plan to spend + headroom for fees
- [ ] Tested the exact same flow on testnet first — **never go straight to mainnet**
- [ ] `.stellar-secret` file has mode 600 and is NOT committed to git
- [ ] You have a hot wallet with limited funds, not your treasury account

## Fee budgeting

A sponsored SAC transfer on mainnet costs roughly:

- Base fee: 100 stroops (0.00001 XLM)
- Soroban resource fee: ~0.05–0.15 XLM per transfer (varies with instruction count)
- Total: budget **~0.2 XLM per payment** to be safe

For MPP sponsored mode and x402 `areFeesSponsored=true`, **the facilitator/server pays the fee**, not you. Your wallet only needs the reserve + the USDC amount.

## Mainnet-specific gotchas

- **Ledger close time**: ~5 seconds on pubnet, same as testnet. The `validUntilLedger = latestLedger + ceil(maxTimeout/5)` formula works unchanged.
- **Trustlines are required for Classic USDC** but **NOT required for SAC USDC** — if you're only ever paying via SAC, you don't need a trustline. But if you want to receive USDC via Classic payment ops, you do.
- **Rate limits**: public RPCs throttle at ~60 req/min. Your payment client retries on simulation failure — if you hit 429, back off exponentially.
- **Do not log secret keys**. Ever. Even in error paths.
- **mppx + @stellar/mpp version drift**: lock to exact versions in `package.json` on mainnet (`"@stellar/mpp": "0.4.0"`, not `"^0.4.0"`). Minor bumps have historically changed credential wire format.

## If something goes wrong

- **Simulation failed** → check RPC URL + network match. A testnet RPC with pubnet passphrase silently returns garbage.
- **Auth entry expired** → `validUntilLedger` was too close. Increase `maxTimeoutSeconds` to 120+.
- **Insufficient balance** → query via `Horizon.Server.loadAccount(pubkey)` or use the `check-balance` sub-skill.
- **Fee exceeded** → you're probably not in sponsored mode. Verify `feePayer: true` / `areFeesSponsored: true`.
