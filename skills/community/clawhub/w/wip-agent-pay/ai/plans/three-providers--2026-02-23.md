# Plan: Three Providers ... Coinbase CDP, Stripe, Privy

**Date:** 2026-02-23
**Author:** Claude Code (Opus 4.6)
**Status:** Planning

## The Big Picture

Agent Pay has one provider today (`providers/coinbase.js`) that mints one-time URLs via a Cloudflare Worker. That's Mode B ... "mint a token, hand it to the agent."

This plan adds two things: wallet providers (where the agent's money lives) and a funding on-ramp (how money gets into the wallet). All run inside Cloudflare Workers. No SDKs needed ... raw `fetch` to REST APIs. The interface layer (CLI, MCP, OpenClaw) doesn't change.

**Agent Pay is the money provider.** We are the payment rail.

```
    FUNDING (money in)              SPENDING (money out)
    ─────────────────               ───────────────────
    Stripe (Apple Pay / Face ID)    CDP wallet ──▶ x402 services
    Stripe (Apple Pay / Face ID)    Privy wallet ──▶ x402 services
    Manual (coinbase.com)           CDP wallet ──▶ x402 services
    Manual (direct transfer)        Privy wallet ──▶ x402 services
```

```
  ┌─────────────────────────────────────────────────┐
  │                  agent_pay                       │
  │               CLI / MCP / OC                     │
  └──────────┬────────────────────┬─────────────────┘
             │                    │
     ┌───────▼────────┐  ┌───────▼────────┐
     │  FUNDING       │  │  SPENDING      │
     │  (money in)    │  │  (money out)   │
     │                │  │                │
     │  Stripe        │  │  CDP (x402)    │
     │  Apple Pay     │  │  Privy (x402)  │
     │  Face ID       │  │                │
     └────────────────┘  └────────────────┘
```

**Funding: Stripe** ... Apple Pay on-ramp. User taps Face ID, money flows into their agent's CDP or Privy wallet. No crypto knowledge needed. No Coinbase account needed (for the buyer). Agent Pay receives fiat, converts to USDC, deposits into wallet.

**Spending: Coinbase CDP** ... x402 native. Signs EIP-3009 transferWithAuthorization via MPC. For crypto-native services (Morning Stew on Monad). Coinbase holds the keys.

**Spending: Privy** ... embedded server wallet. Smart contract wallet with spend policies. Broad chain support (11+ chains). For users who don't want Coinbase. Privy holds the keys.

**The seller (Morning Stew) doesn't need a Stripe account.** Morning Stew speaks x402. The agent pays Morning Stew with USDC from the funded wallet. Morning Stew doesn't know or care where the USDC came from.

## Architecture: Everything Is a Worker

The existing Worker (`pay-wip-computer.wipcomputer.workers.dev`) handles one-time URL mint/redeem. The new providers add routes to this same Worker OR deploy as separate Workers. Same KV namespace.

### Worker Routes (expanded)

```
POST /create              ... existing: mint one-time URL (Mode B)
GET  /{token}             ... existing: redeem one-time URL
GET  /                    ... existing: health check

POST /x402/pay            ... NEW: x402 flow (hit URL, sign, retry)
POST /stripe/checkout     ... NEW: create Stripe checkout session
POST /stripe/webhook      ... NEW: Stripe payment confirmation
GET  /stripe/success      ... NEW: post-payment redirect (returns token)
POST /privy/pay           ... NEW: Privy wallet send
```

All routes share the same KV namespace (`PAY_TOKENS`). After payment confirms (any provider), the Worker mints a one-time token in KV. Same self-destruct. Same 410 on second use. The token is the universal output.

## Provider 1: Coinbase CDP (x402)

### What It Does

Agent hits a paywalled URL. Gets 402 back with payment requirements. Agent calls `agent_pay pay <url>`. Worker handles the rest: parses the 402, signs EIP-3009 via CDP, retries with proof, returns content.

### Auth (Two JWTs, Ed25519)

CDP requires two JWTs per request:

1. **Bearer Token:** Signed with CDP API Key Secret (Ed25519). Fields: `sub` (key ID), `iss: "cdp"`, `aud: ["cdp_service"]`, `exp` (+120s), `uri` (method + host + path).
2. **X-Wallet-Auth:** Signed with Wallet Secret. Fields: `iat`, `nbf`, `jti`, `uris`, `reqHash` (SHA-256 of request body).

Both use Ed25519 which `crypto.subtle.sign("Ed25519")` supports natively in Workers. No SDK needed.

### The Flow

```
1. Agent: agent_pay pay https://morning-stew.../v1/issues/MS-3
2. Worker: fetch(url) ... gets 402 + payment requirements
3. Worker: parse 402 response (payTo, amount, network, USDC contract)
4. Worker: construct EIP-3009 transferWithAuthorization typed data
5. Worker: POST api.cdp.coinbase.com/platform/v2/evm/accounts/{addr}/sign-typed-data
           (Bearer JWT + X-Wallet-Auth JWT)
6. Worker: gets signature back
7. Worker: retry original URL with X-PAYMENT-SIGNATURE header
8. Worker: content returned
9. Worker: mint one-time token in KV with content
10. Agent: receives token URL
```

### Secrets (1Password)

| Entry | Vault | Fields |
|-------|-------|--------|
| `wip-agent-pay-coinbase-cdp` | Agent Secrets | `api-key-id`, `api-key-secret`, `wallet-secret`, `account-address` |

Parker creates the CDP wallet on portal.cdp.coinbase.com. Funds it by withdrawing USDC from his Coinbase portfolio to the CDP wallet address. Stores creds in 1Password.

### API Calls

**Create account (one-time, manual or script):**
```
POST https://api.cdp.coinbase.com/platform/v2/evm/accounts
Authorization: Bearer <jwt>
X-Wallet-Auth: <wallet-auth-jwt>
```

**Sign EIP-712 typed data:**
```
POST https://api.cdp.coinbase.com/platform/v2/evm/accounts/{address}/sign-typed-data
Authorization: Bearer <jwt>
X-Wallet-Auth: <wallet-auth-jwt>
Content-Type: application/json

{
  "typed_data": {
    "domain": {
      "name": "USD Coin",
      "version": "2",
      "chainId": "10143",        // Monad testnet (or mainnet ID)
      "verifyingContract": "0x..."  // USDC contract on Monad
    },
    "types": {
      "TransferWithAuthorization": [
        { "name": "from", "type": "address" },
        { "name": "to", "type": "address" },
        { "name": "value", "type": "uint256" },
        { "name": "validAfter", "type": "uint256" },
        { "name": "validBefore", "type": "uint256" },
        { "name": "nonce", "type": "bytes32" }
      ]
    },
    "primaryType": "TransferWithAuthorization",
    "message": {
      "from": "{our CDP wallet address}",
      "to": "{payTo from 402}",
      "value": "{amount in smallest unit}",
      "validAfter": "0",
      "validBefore": "{now + 300}",
      "nonce": "{random bytes32}"
    }
  }
}
```

### New Files

| File | What |
|------|------|
| `providers/x402.js` | Local provider: hit URL, call Worker /x402/pay, return result |
| Worker route: `/x402/pay` | Parse 402, sign via CDP, retry, mint token |
| `lib/cdp-auth.js` | Ed25519 JWT generation for Workers (crypto.subtle) |

### CLI Addition

```bash
wip-agent-pay pay <url>                    # x402 mode
wip-agent-pay pay <url> --provider=cdp     # explicit
```

### Open Questions

1. Does Monad mainnet have a chain ID assigned yet? Need to verify.
2. Does Morning Stew's 402 response include the USDC contract address, or do we need to know it per-chain?
3. CDP wallet creation ... can it be done from the Worker, or must it be done on portal.cdp.coinbase.com?

---

## Provider 2: Stripe (Apple Pay ... Funding On-Ramp)

### What It Does

User wants to fund their agent's wallet. Agent opens a Stripe Checkout page. User taps Face ID (Apple Pay). Money goes to Agent Pay (us) via Stripe. Agent Pay converts to USDC and deposits into the user's CDP or Privy wallet. Now the agent can spend.

**Stripe is how money gets IN. CDP/Privy is how money gets OUT.**

### Why This Is the Normie Path

- No Coinbase account needed (for the buyer)
- No crypto wallet setup needed
- No 1Password needed (for the buyer)
- Apple Pay just works in Stripe Checkout
- Google Pay also just works
- Card fallback for everyone else
- User doesn't need to know what USDC is

### Auth

One API key. `Authorization: Bearer sk_live_xxx`. That's it.

### The Flow

```
1. Agent: "Your wallet is empty. Want to add $10?"
2. User: "yes"
3. Agent: POST Worker /stripe/checkout { amount: 10, walletType: "cdp", walletAddress: "0x..." }
4. Worker: create Stripe Checkout session ($10)
5. Worker: return { checkoutUrl, pendingFundId }
6. Agent: opens checkoutUrl in user's browser
7. User: taps Face ID / enters card
8. Stripe: sends webhook to Worker /stripe/webhook
9. Worker: verifies signature, converts fiat to USDC, deposits to wallet address
10. Worker: marks pendingFundId as complete
11. Agent: wallet funded. Now spend via CDP or Privy x402 flow.
```

### Stripe Checkout in Workers (zero deps)

```javascript
// Inside Worker
async function createCheckout(amount, service, note, origin) {
  const resp = await fetch("https://api.stripe.com/v1/checkout/sessions", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${env.STRIPE_SECRET_KEY}`,
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: new URLSearchParams({
      "line_items[0][price_data][currency]": "usd",
      "line_items[0][price_data][product_data][name]": `${service}: ${note}`,
      "line_items[0][price_data][unit_amount]": String(Math.round(amount * 100)),
      "line_items[0][quantity]": "1",
      "mode": "payment",
      "success_url": `${origin}/stripe/success?session_id={CHECKOUT_SESSION_ID}`,
      "cancel_url": `${origin}/stripe/cancel`,
      "metadata[service]": service,
      "metadata[note]": note,
    }),
  });
  return resp.json();
}
```

Apple Pay appears automatically. No extra config.

### Webhook Verification in Workers

```javascript
// HMAC-SHA256 with crypto.subtle
async function verifyStripeWebhook(body, signature, secret) {
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey(
    "raw", encoder.encode(secret),
    { name: "HMAC", hash: "SHA-256" }, false, ["sign"]
  );
  // Parse Stripe signature header (t=timestamp,v1=hash)
  const parts = Object.fromEntries(signature.split(",").map(p => p.split("=")));
  const payload = `${parts.t}.${body}`;
  const expected = await crypto.subtle.sign("HMAC", key, encoder.encode(payload));
  const expectedHex = [...new Uint8Array(expected)].map(b => b.toString(16).padStart(2, "0")).join("");
  return expectedHex === parts.v1;
}
```

### Secrets (1Password + Cloudflare)

| Entry | Vault | Fields |
|-------|-------|--------|
| `wip-agent-pay-stripe` | Agent Secrets | `secret-key`, `webhook-secret`, `publishable-key` |

Worker env vars: `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`.

Parker creates a Stripe account at stripe.com. Gets API keys. Stores in 1Password. Sets Worker env vars on Cloudflare dashboard.

### Fiat-to-USDC Conversion

After Stripe payment confirms, the Worker needs to convert fiat to USDC and send it to the wallet. Options:
- **Coinbase Commerce / On-ramp API** ... fiat in, USDC out to an address
- **Stripe crypto payouts** ... Stripe can pay out in USDC on Polygon (US only)
- **Manual for v1** ... Parker manually tops up wallets, Stripe just tracks the balance owed

For v1: Stripe confirms payment, Worker credits the wallet balance in KV. The wallet is already funded manually by Parker. Stripe is the accounting layer. Real fiat-to-USDC conversion is v2.

### New Files

| File | What |
|------|------|
| `providers/stripe.js` | Local provider: call Worker /stripe/checkout, return checkoutUrl |
| Worker routes: `/stripe/*` | Checkout creation, webhook, success/cancel pages |

### CLI Addition

```bash
wip-agent-pay fund 10                         # fund wallet with $10 via Apple Pay
wip-agent-pay fund 10 --wallet=cdp            # specify wallet type
wip-agent-pay fund 10 --wallet=privy          # fund Privy wallet instead
```

---

## Provider 3: Privy (Embedded Wallet)

### What It Does

Server-side embedded wallet. No Coinbase. No user-facing setup. The app creates a wallet, funds it, agent spends from it. Smart contract wallet with spend policies (max amount, allowlisted recipients).

Privy was acquired by Stripe (June 2025). The two are converging.

### Auth

HTTP Basic Auth. `Authorization: Basic base64(app-id:app-secret)`. Plus `privy-app-id` header.

### The Flow

```
1. Setup (one-time): create Privy server wallet, fund it with USDC
2. Agent: agent_pay pay <url> --provider=privy
3. Local provider: POST Worker /privy/pay
4. Worker: hit paywalled URL, get 402, extract payment requirements
5. Worker: POST api.privy.io/v1/wallets/{id}/rpc
           method: eth_signTypedData_v4 (EIP-712 for EIP-3009)
6. Worker: gets signature
7. Worker: retry URL with payment proof
8. Worker: mint one-time token with content
9. Agent: receives token URL
```

### API Calls

**Create wallet (one-time):**
```
POST https://api.privy.io/v1/wallets
Authorization: Basic <base64(app-id:app-secret)>
privy-app-id: <app-id>

{ "chain_type": "ethereum" }
```

**Sign typed data:**
```
POST https://api.privy.io/v1/wallets/{wallet_id}/rpc
Authorization: Basic <base64(app-id:app-secret)>
privy-app-id: <app-id>

{
  "method": "eth_signTypedData_v4",
  "caip2": "eip155:10143",
  "params": {
    "typed_data": { ... EIP-712 domain/types/message ... }
  }
}
```

### Spend Policies

Privy has a policy engine:
- Max transfer per tx
- Allowlisted recipient addresses
- Allowlisted contract methods
- Rate limits

This maps directly to Agent Pay's security model: human sets limits, agent spends within them.

### Secrets (1Password)

| Entry | Vault | Fields |
|-------|-------|--------|
| `wip-agent-pay-privy` | Agent Secrets | `app-id`, `app-secret`, `wallet-id`, `wallet-address` |

Parker creates a Privy account at privy.io. Creates an app. Creates a server wallet. Funds it. Stores creds in 1Password.

### Supported Chains

Ethereum, Base, Polygon, Arbitrum, Optimism, Solana, Cosmos, Stellar, Sui, Aptos, and more. Any EVM chain via `eip155:{chainId}`.

### New Files

| File | What |
|------|------|
| `providers/privy.js` | Local provider: call Worker /privy/pay, return result |
| Worker route: `/privy/pay` | Sign via Privy API, handle 402 flow |

### CLI Addition

```bash
wip-agent-pay pay <url> --provider=privy
wip-agent-pay 0.10 morning-stew "MS-#8" --provider=privy
```

---

## Updated CLI

```bash
# FUND wallet (money in)
wip-agent-pay fund <amount>                    # Apple Pay via Stripe
wip-agent-pay fund <amount> --wallet=cdp       # fund CDP wallet
wip-agent-pay fund <amount> --wallet=privy     # fund Privy wallet

# PAY a service via x402 (money out)
wip-agent-pay pay <url>                        # auto-detect wallet
wip-agent-pay pay <url> --wallet=cdp           # use CDP wallet
wip-agent-pay pay <url> --wallet=privy         # use Privy wallet

# MINT one-time URL (existing Mode B)
wip-agent-pay <amount> <service> [note]        # existing flow, unchanged

# CHECK balance
wip-agent-pay balance                          # show wallet balance
wip-agent-pay balance --wallet=cdp
wip-agent-pay balance --wallet=privy
```

## Updated Worker Structure

```
Worker: pay-wip-computer.wipcomputer.workers.dev

Bindings:
  KV: PAY_TOKENS
  Secrets: WORKER_SECRET, STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET,
           CDP_API_KEY_ID, CDP_API_KEY_SECRET, CDP_WALLET_SECRET, CDP_ACCOUNT_ADDRESS,
           PRIVY_APP_ID, PRIVY_APP_SECRET, PRIVY_WALLET_ID

Routes:
  GET  /                    health check
  POST /create              mint one-time URL (existing, auth: WORKER_SECRET)
  GET  /{token}             redeem one-time URL (existing)
  POST /x402/pay            x402 flow via CDP (auth: WORKER_SECRET)
  POST /stripe/checkout     create Stripe checkout (auth: WORKER_SECRET)
  POST /stripe/webhook      Stripe webhook (auth: Stripe signature)
  GET  /stripe/success      post-checkout redirect
  POST /privy/pay           pay via Privy wallet (auth: WORKER_SECRET)
```

All routes that the agent calls require `Authorization: Bearer {WORKER_SECRET}`. The Worker secret is already in 1Password and wired.

## Updated File Structure

```
wip-agent-pay/
  cli.js                     updated: --provider flag, pay subcommand
  providers/
    coinbase.js              existing: one-time URL via Worker
    x402.js                  NEW: x402 via CDP (calls Worker /x402/pay)
    stripe.js                NEW: Apple Pay (calls Worker /stripe/checkout)
    privy.js                 NEW: embedded wallet (calls Worker /privy/pay)
    index.js                 NEW: provider router (--provider flag)
  lib/
    cdp-auth.js              NEW: Ed25519 JWT generation (for Worker)
    stripe-verify.js         NEW: webhook HMAC verification (for Worker)
  worker/
    index.js                 NEW: full Worker source (replaces inline deploy)
    wrangler.toml            NEW: Cloudflare config
  mcp-server.mjs             updated: url param, provider param
  openclaw.mjs               updated: url param, provider param
  ...
```

## Execution Order

### Phase 1: Coinbase CDP (x402)

1. Create `lib/cdp-auth.js` ... Ed25519 JWT generation using Web Crypto
2. Create `providers/x402.js` ... local provider that calls Worker
3. Add `/x402/pay` route to Worker
4. Update `cli.js` with `pay <url>` subcommand and `--provider` flag
5. Create `providers/index.js` ... provider router
6. Update `mcp-server.mjs` and `openclaw.mjs` with `url` + `provider` params
7. Parker: create CDP wallet on portal.cdp.coinbase.com
8. Parker: withdraw USDC from portfolio to CDP wallet address
9. Parker: store CDP creds in 1Password (`wip-agent-pay-coinbase-cdp`)
10. Parker: set CDP env vars on Cloudflare Worker
11. Test: `wip-agent-pay pay <morning-stew-free-endpoint>`
12. Test: `wip-agent-pay pay <morning-stew-paid-endpoint>`
13. PR + merge

### Phase 2: Stripe (Apple Pay Funding On-Ramp)

14. Add `/stripe/checkout` route to Worker (create checkout session)
15. Add `/stripe/webhook` route to Worker (HMAC verification, credit wallet)
16. Add `/stripe/success` + `/stripe/cancel` routes to Worker
17. Create `providers/stripe.js` ... local provider (calls Worker /stripe/checkout)
18. Update `cli.js` with `fund` subcommand
19. Parker: create Stripe account (Agent Pay / WIP.computer is the merchant)
20. Parker: store Stripe creds in 1Password (`wip-agent-pay-stripe`)
21. Parker: set Stripe env vars on Cloudflare Worker
22. Parker: configure Stripe webhook URL to Worker
23. Test: `wip-agent-pay fund 10` ... opens Apple Pay checkout
24. Test: Apple Pay in Safari, verify wallet credited
25. PR + merge

### Phase 3: Privy (Embedded Wallet)

25. Create `providers/privy.js` ... local provider
26. Add `/privy/pay` route to Worker
27. Parker: create Privy account + app + server wallet
28. Parker: fund Privy wallet with USDC
29. Parker: store Privy creds in 1Password (`wip-agent-pay-privy`)
30. Parker: set Privy env vars on Cloudflare Worker
31. Test: `wip-agent-pay pay <url> --provider=privy`
32. PR + merge

### Phase 4: Docs + Ship

33. Update SPEC.md (three providers, provider selection)
34. Update SETUP.md (three setup paths)
35. Update SKILL.md
36. Update README.md
37. Dev update
38. Tag release

## What Parker Does vs What Code Does

| Task | Who |
|------|-----|
| Create CDP wallet on portal.cdp.coinbase.com | Parker |
| Fund CDP wallet (withdraw USDC from portfolio) | Parker |
| Store CDP creds in 1Password | Parker |
| Create Stripe account | Parker |
| Store Stripe keys in 1Password | Parker |
| Set Cloudflare Worker env vars | Parker |
| Create Privy account + app + wallet | Parker |
| Fund Privy wallet | Parker |
| Store Privy creds in 1Password | Parker |
| Everything else (all code, all routes, all providers) | Code |

## Security Model (unchanged)

Human creates wallet. Human funds wallet. Human sets limits. Agent only spends. No exceptions.

Each provider enforces this differently:
- **CDP:** Isolated portfolio. API key scoped to one portfolio.
- **Stripe:** Checkout session created by Worker. Agent never sees Stripe key.
- **Privy:** Spend policies on the wallet. Max amount, allowlisted recipients.

The Worker secret gates all agent-facing routes. Agent can't call CDP/Stripe/Privy directly. Only through the Worker.

## Open Questions

1. **CDP portal access:** Does Parker have access to portal.cdp.coinbase.com? Need to check.
2. **Monad chain ID:** Verify Monad mainnet/testnet chain IDs for EIP-712 domain.
3. **Morning Stew 402 format:** What exactly does the 402 response body look like? Need to test against their endpoint.
4. **Fiat-to-USDC conversion:** For Stripe funding, how do we convert fiat to USDC automatically? Coinbase On-ramp API? Or manual for v1?
5. **Privy + Stripe convergence:** Since Stripe acquired Privy (June 2025), should we expect a unified API? Build now, converge later.
6. **Worker size limits:** Cloudflare Workers have a 1MB limit on free tier. With all routes, are we close? Probably fine.
7. **Stripe account:** Parker needs a Stripe account. Does he have one? Agent Pay (WIP.computer) is the merchant.
