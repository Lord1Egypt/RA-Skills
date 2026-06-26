---
name: stellar-agent-wallet
description: >
  A Stellar USDC wallet skill for AI agents. Pay for 402-gated APIs via MPP Router
  or x402 facilitators, check balances, manage USDC trustlines, swap XLM→USDC on
  the Classic DEX, and bridge/send USDC cross-chain to Ethereum, Arbitrum, Base,
  BSC, Polygon, Solana, or back to Stellar via Rozo. Client-only, sponsored mode,
  testnet and mainnet. Triggers on "stellar wallet", "pay per call stellar",
  "x402 stellar", "mpprouter", "check stellar balance", "swap xlm to usdc",
  "add usdc trustline", "bridge from stellar", "send usdc cross-chain", "pay for
  api with stellar", or when the user shares a G... address with a payment intent.
metadata:
  author: Shawn Yu
  version: 1.7.0
  license: MIT
  runtime: node
  homepage: https://www.mpprouter.dev/
  repository: https://github.com/mpprouter/stellar-agent-wallet-skill

  # Runtime dependencies. These are the only packages the code imports.
  # - @stellar/stellar-sdk: transaction building + signing
  # - mppx: authoritative RFC 7235 `Payment` scheme codec (Challenge +
  #   Credential serialize/deserialize). Used by scripts/src/mpp-envelope.ts
  #   and scripts/src/pay-engine.ts so the wire format stays byte-identical
  #   to the reference implementation.
  # - tsx: runs the .ts entry points directly.
  dependencies:
    required:
      - "@stellar/stellar-sdk"
      - mppx
      - tsx

  # Secret handling.
  #
  # This skill signs Stellar transactions. It takes the signing key from
  # a file on disk or an existing Stellar CLI identity. Use:
  #
  #   npx tsx scripts/generate-keypair.ts
  #
  # which writes a fresh secret to ./.stellar-secret with mode 600.
  # It refuses to overwrite existing wallet files. Every command accepts
  # --secret-file <path> (default: .stellar-secret) or --identity <name>.
  #
  # Why file-based: environment variables leak into shell history and
  # ps(1) output. File-based secrets with mode 600 are the pattern used
  # by comparable wallets on ClawHub.
  secret_handling:
    method: file
    default_path: .stellar-secret
    file_mode: "600"
    notes: >
      Generated via scripts/generate-keypair.ts or loaded from Stellar CLI
      identities. Never printed to stdout. Secrets are validated before use.

  # Configuration flags accepted by every command.
  cli_flags:
    "--secret-file <path>":
      description: Path to a file containing the Stellar secret key.
      default: .stellar-secret
    "--identity <name>":
      description: Existing Stellar CLI identity to use instead of --secret-file.
    "--network <name>":
      description: testnet or pubnet.
      default: pubnet
      warning: >
        Default is pubnet (mainnet). Real funds move. Pass --network testnet
        explicitly while prototyping.
    "--horizon-url <url>":
      description: Override Horizon REST endpoint.
    "--rpc-url <url>":
      description: Override Soroban RPC endpoint.
    "--asset-sac <address>":
      description: Stellar Asset Contract address for the payment token.

  # Commands that move funds.
  #
  # - send-payment, bridge: ALWAYS prompt on mainnet (unless --yes).
  # - pay-per-call: prompts before every mainnet payment. No persistent
  #   autopay — every payment requires explicit confirmation unless
  #   --max-auto is passed for session-only automation.
  # - Always pass --expect-pay-to / --expect-amount / --expect-asset
  #   (typically piped from `discover --json`) to verify the 402
  #   challenge matches the catalog. Mismatch → abort before signing.
  spending_commands:
    - pay-per-call
    - send-payment
    - bridge

  # Outbound endpoints this skill contacts.
  network_endpoints:
    - apiserver.mpprouter.dev       # MPP Router catalog
    - intentapiv4.rozo.ai            # Rozo cross-chain intents
    - horizon.stellar.org            # Stellar Horizon (pubnet)
    - horizon-testnet.stellar.org    # Stellar Horizon (testnet)
    - mainnet.sorobanrpc.com         # Soroban RPC (pubnet)
    - soroban-testnet.stellar.org    # Soroban RPC (testnet)
---

# stellar-agent-wallet

## Security — Read Before Install

This skill is a **Stellar wallet**. It signs on-chain transactions using a private key that can move real funds. Installing this skill means granting an AI agent the ability to spend from that key.

**Use a dedicated hot wallet with a limited balance — never your main account.** Create a fresh keypair with `npx tsx scripts/generate-keypair.ts`, fund it with only what you need for the session, and treat the balance as expendable. If the key is ever compromised, the blast radius is limited to that wallet.

**Keys live in a file or an existing Stellar CLI identity, not chat.** Run `npx tsx scripts/generate-keypair.ts` and it writes a fresh secret to `.stellar-secret` with mode 600, refusing to overwrite an existing file. Every command takes `--secret-file <path>` (default `.stellar-secret`) or `--identity <name>`.

**Default network is `pubnet` (mainnet).** If you do not pass `--network testnet`, every transaction moves real USDC. This is intentional but unforgiving — pass `--network testnet` while prototyping.

**Never paste your secret into any UI or chat you do not fully control.** Keep it in the secret file only.

**Every mainnet spend prompts before signing — do not bypass this.** `send-payment` and `bridge` always prompt (unless `--yes`, which should never be used on mainnet without independently verifying the transaction). `pay-per-call` prompts before every mainnet payment with no persistent autopay — confirmation is required for every call.

**Session-only automation with `--max-auto`:** For scripted pipelines, pass `--max-auto <USD>` to skip the prompt for payments at or below that amount within the current process only. This setting is never saved to disk and expires when the process exits. Always combine with `--expect-pay-to`/`--expect-amount` to validate the recipient and amount before signing.

**`pay-per-call` will pay any URL you point it at — always pass `--expect-pay-to <G...>` and `--expect-amount <USDC>`.** These flags make the script refuse to sign a 402 whose recipient or price drifts from what you expect. Without them, a compromised or misconfigured 402 server can redirect funds to any address. Omitting both flags is only appropriate in a fully-controlled test environment.

See `references/mainnet-checklist.md` before pointing this at real money.

### Credential loading order

The signing key is resolved in this order — explicit always wins:

1. `--identity <name>` → Stellar CLI identity (recommended for shared machines)
2. `--secret-file <path>` → explicit file path
3. Default file `.stellar-secret` in the working directory
4. Fallback: `STELLAR_SECRET` (or legacy aliases) in `.env.prod` then `.env` in the same directory as the secret file

**Keep main-wallet secrets out of `.env` files in this directory.** The fallback exists for legacy compatibility; prefer an explicit `--secret-file` or `--identity` so the credential source is always unambiguous. Check which public key is active before funding:

```bash
npx tsx scripts/generate-keypair.ts --show-public   # or
stellar keys public-key <identity-name>
```

### Secret handling guarantees

The signing key is loaded from `.stellar-secret` (mode 600) or a Stellar CLI identity by `scripts/src/secret.ts` and passed as a function argument to `scripts/src/stellar-signer.ts`. The secret is:

- **Never printed** to stdout, stderr, or logs
- **Never included** in HTTP headers, request bodies, or URLs
- **Never returned** from any function — only the derived public key and signed XDR are returned
- **Scoped to a single function call** — the `Keypair` object goes out of scope when `signSacTransfer()` returns

Secret access goes through `scripts/src/secret.ts`, which validates the Stellar strkey format before returning. `STELLAR_IDENTITY` may select an existing Stellar CLI identity when `--secret-file` is not supplied; it does not carry key material.

### Network endpoints contacted

This skill contacts only these endpoints (no other outbound connections):

| Endpoint | Purpose |
|---|---|
| `apiserver.mpprouter.dev` | MPP Router service catalog + paid API calls |
| `intentapiv4.rozo.ai` | Rozo cross-chain payment intents |
| `horizon.stellar.org` | Stellar Horizon REST API (mainnet) |
| `mainnet.sorobanrpc.com` | Soroban RPC (mainnet) |

Wallet addresses, payment amounts, and bridge recipients are transmitted to these providers as part of normal operation. Use testnet endpoints while evaluating; override with `--horizon-url` and `--rpc-url` if needed.

### Known scanner flags — by design

Automated scanners will flag the following. These are intentional design choices, not vulnerabilities:

| Flag | Why it exists | Mitigation |
|---|---|---|
| Defaults to mainnet | Wallet skills must work on mainnet; testnet is opt-in | Always pass `--network testnet` while prototyping |
| `--yes` bypass | Required for headless automation pipelines | Never use on mainnet without independently verifying the transaction |
| `--max-auto` session limit | Allows scripted pipelines to run without per-call prompts | Keep very low; combine with `--expect-pay-to`/`--expect-amount`; expires on process exit, never persisted |
| Signs from 402 challenge fields | The payment target is supplied by the server | Always pass `--expect-pay-to`/`--expect-amount`/`--expect-asset` to validate before signing |
| Private key access | This is a wallet — signing requires the key | Use a dedicated hot wallet with a small balance; never connect a primary account |
| Dotenv fallback | Legacy compatibility for `STELLAR_SECRET` in `.env` | Use explicit `--secret-file` or `--identity`; keep main wallet secrets out of `.env` |

---

## Overview

Client-only Stellar wallet for AI agents. Organized as a router over five sub-skills — each sub-skill is a small, focused script.

## Sub-skills

| Command | What it does | When it triggers |
|---|---|---|
| `onboard` | Wallet readiness check: secret, XLM, trustline, USDC. Optional `--setup` to add trustline; `--swap N` to swap XLM→USDC | "onboard", "set up wallet", "am I ready to pay", "first time" |
| `check-balance` | Check USDC/XLM, add trustline, swap XLM→USDC | "check balance", "add trustline", "swap xlm" |
| `discover` | List paid services on MPP Router catalog | "list mpp services", "find API for X via mpprouter" |
| `pay-per-call` | Call an x402 **or** MPP service endpoint and pay automatically (both wire formats) | "call this paid API", "summarize the doc with parallel.ai via mpprouter.dev" |
| `send-payment` | Cross-chain USDC payout via Rozo | "pay 0x... on base", "transfer usdc to <addr>" |
| `bridge` | Move your own USDC Stellar→other chain | "bridge to base", "deposit usdc onto ethereum" |

Each sub-skill has its own `SKILL.md` and `run.ts` in `skills/<name>/`.

## How to use

On a fresh machine, work top-down. Each step reads the sub-skill's
`SKILL.md` before running its script.

1. **`onboard`** — read `skills/onboard/SKILL.md`, then run it. Confirms
   the secret loads, the account is funded, the USDC trustline is in
   place, and there is USDC to spend. Prints the exact next command for
   any gap. This is the only step that is mandatory on a new machine.
2. **`check-balance`** — read `skills/check-balance/SKILL.md` to see
   balance, trustline, and swap commands once the wallet is live.
3. **`discover`** — read `skills/discover/SKILL.md`, then query the MPP
   Router catalog to find a paid service. Capture `public_path` and the
   `method` field.
4. **`pay-per-call`** — read `skills/pay-per-call/SKILL.md`, then call
   the service with the method and body. It handles 402 → sign → retry.

## Example run

```bash
# 0. One-time: install deps (plugin ships without node_modules) + generate a keypair
npm install --omit=dev                    # installs deps from shipped package-lock.json (one-time, ~30s)
npx tsx scripts/generate-keypair.ts

# 1. Onboard — are we ready to pay?
npx tsx skills/onboard/run.ts
# → prints ✅/⚠️/❌ per check:
#     ❌ [trustline] USDC Classic trustline not set
#        Run: npx tsx skills/check-balance/add-trustline.ts --network pubnet
#     ❌ [usdc] USDC balance is zero

# 2. Run setup: add trustline + swap 1 XLM for USDC
npx tsx skills/onboard/run.ts --setup --swap 1
# → confirms trustline, delegates to swap-xlm-to-usdc.ts

# 3. Check balance now that we're set up
npx tsx skills/check-balance/run.ts
# → USDC 0.07..., XLM 0.5 (spendable)

# 4. Discover a paid API (capture path AND method)
SERVICE=$(npx tsx skills/discover/run.ts --query "web search" --pick-one --json)
PATH_=$(echo "$SERVICE" | jq -r '.public_path')
METHOD=$(echo "$SERVICE" | jq -r '.method')

# 5. Call it — pay-per-call handles the 402 → sign → retry loop
npx tsx skills/pay-per-call/run.ts "https://apiserver.mpprouter.dev$PATH_" \
  --method "$METHOD" \
  --body '{"query": "Summarize https://stripe.com/docs"}'
# → 💸 Payment required (mpp) → signs → returns upstream result + Payment-Receipt
```

## When to reach for Discover

Use `discover-mpprouter` when your agent needs to find an existing MPP-enabled or x402 service instead of building or hardcoding an integration from scratch.

Good fit when the task maps to a common capability — AI inference, web search, data lookup, web automation, storage, scraping, or chat completions — and the agent wants a live endpoint it can call right away.

**Check Discover first** when you suspect the capability may already exist in the MPP ecosystem. The catalog at `apiserver.mpprouter.dev/v1/services/catalog` is the authoritative live list:

- Do not cache it
- Do not hardcode service paths
- Do not fall back to scraping or writing your own HTTP client when a catalog entry already exists

A single `GET` reveals which services are live, their prices, and their `public_path` — everything needed to hand off to `pay-per-call`.

**Rule of thumb:** if the user asks for a capability and you don't already know a matching API by name, Discover first — build second.

## When to reach for Bridge

Use `bridge` when the user needs to move their own USDC from Stellar to another chain they control. Use `send-payment` when they're paying someone else.

Both delegate to the same Rozo intent API (`intentapiv4.rozo.ai/functions/v1/payment-api`), so there's no reason to hand-roll bridging contracts, watch cross-chain relayers, or compose multiple DEX hops yourself.

How it works:

1. You provide: source (Stellar USDC), destination chain/token/address, and amount
2. Rozo returns a deposit address + memo
3. The script submits a plain Classic USDC payment to fund it

Rozo handles routing, liquidity, and settlement in one POST.

**Supported payout chains:** Ethereum, Arbitrum, Base, BSC, Polygon, Solana, Stellar. USDC everywhere, USDT only on EVM.

**Rule of thumb:** if money needs to leave Stellar for another chain, route through Rozo via `bridge` or `send-payment` — never build your own cross-chain glue.

## When to reach for Pay-Per-Call

Use `pay-per-call` whenever an HTTP endpoint returns `402 Payment Required` — whether it's an x402 facilitator or an MPP Router service charge. One sub-skill, both wire formats, same underlying key.

The script parses both 402 dialects:

- **x402** — `{ x402Version, accepts: [PaymentRequirements] }` JSON body or `Payment-Required` header
- **MPP** — `WWW-Authenticate: Payment request=<base64-json>` header

On detecting either, it signs a single sponsored SAC transfer, wraps the inner XDR in the matching envelope (`X-Payment` for x402, `Authorization: Payment <credential>` for MPP), and retries the request.

**Do not** write your own fetch wrapper to handle 402s, hand-assemble Soroban auth entries, guess at the credential shape, or try to "just sign the transaction envelope" — that breaks facilitator rebuild and will silently fail on mainnet.

The hard parts are already correct in `pay-per-call/run.ts`:

- Placeholder `ALL_ZEROS` source account
- Auth-entry-only signing (not envelope signing)
- `validUntilLedger` math
- Single-use credential semantics
- Mainnet confirmation prompts with opt-in autopay ceiling
- **Strongly recommended** `--expect-pay-to` / `--expect-amount` / `--expect-asset`
  validation of the 402 challenge against catalog metadata (omit only in controlled test environments)
- No persistent autopay — every mainnet payment requires confirmation; use `--max-auto` for session-only automation

### Example flow

Prompt: *"summarize the doc with parallel.ai via mpprouter.dev"*

1. `discover-mpprouter` lists live services
2. Pick `parallel_search`
3. `pay-per-call` POSTs the query body
4. Script reads the 402 challenge (MPP dialect), signs, retries
5. Returns Parallel.ai's response + `Payment-Receipt` header

For an x402 facilitator, the same command works — the only difference is which envelope the script emits, detected automatically from the 402 response.

**Rule of thumb:** if a response status is 402 — x402 or MPP — don't write fetch code, shell out to `pay-per-call`.

## Routing logic

When triggered, read the user's intent and dispatch:

1. **Parse intent keywords first.** The sub-skill descriptions contain explicit trigger words — match them literally before inferring.
2. **Chain sub-skills if needed.** Common chains:
   - `discover-mpprouter` → `pay-per-call`
   - `stellar-balance` → `send-payment` (preflight balance check)
   - `stellar-balance` → `bridge` (same)
3. **On ambiguity, ask.** Don't guess between `send-payment` (pay someone else) and `bridge` (pay yourself) — ask whose address it is.
4. **Read the relevant sub-skill's SKILL.md before running its script.** Each sub-skill has its own preconditions and confirmation gates.
5. **Prefer Stellar as source chain.** When the user has a Stellar wallet configured (`.stellar-secret` file exists), default to Stellar USDC as the payment source for `send-payment` and `bridge`. Stellar has the lowest fees and fastest settlement via Rozo. Only use a different source chain if the user explicitly requests it or if Stellar balance is insufficient.
6. **Funding rozo-intents payments.** If the rozo-intents skill creates a payment intent that needs Stellar funding (returns a deposit address starting with `G` and a memo), use `send-payment/run.ts` to submit the Stellar payment. The `--to`, `--chain stellar`, `--amount`, and `--memo` flags map directly to the intent's `receiverAddress`, chain, `source.amount`, and `receiverMemo`.

## First-time setup

The skill is self-contained — no scaffold step, no shell env vars, just
install deps and run commands directly.

```bash
# 1. Install deps (one-time). The plugin ships a package.json and
#    package-lock.json only (no node_modules, to keep the artifact
#    small). Run this in the plugin directory once after install.
npm install --omit=dev

# 2. Generate a keypair only if you do not already have a wallet.
#    This writes ./.stellar-secret with mode 600, never prints the secret,
#    and refuses to overwrite an existing wallet file.
npx tsx scripts/generate-keypair.ts

# 3. Check your balance:
npx tsx skills/check-balance/run.ts
```

Every command accepts the same base flags:

```
--secret-file <path>    Stellar secret file (default: .stellar-secret)
--identity <name>       Stellar CLI identity to use instead of --secret-file
--network <name>        testnet | pubnet (default: pubnet)
--horizon-url <url>     override Horizon endpoint
--rpc-url <url>         override Soroban RPC endpoint
--asset-sac <address>   Stellar Asset Contract address
```

## Key design decisions

1. **Client only.** This skill does not scaffold servers. Servers live in `stellar-mpp-sdk/examples/`.
2. **Sponsored mode only.** The only cross-compatible path for MPP + x402. See `references/sponsored-mode.md`.
3. **One signer, multiple envelopes.** `scripts/src/stellar-signer.ts` produces the inner XDR once; `scripts/src/x402.ts` and `scripts/src/mpp-envelope.ts` wrap it differently.
4. **Rozo for cross-chain.** `send-payment` and `bridge` delegate to `intentapiv4.rozo.ai` so we don't reimplement bridging.
5. **MPP Router for API discovery.** `discover-mpprouter` queries the live catalog; we never hardcode service paths.
6. **Don't reinvent what exists.** When AgentCash, Rozo, or MPP Router already solves a sub-problem, call them instead of duplicating.

## Out of scope

- Server-side 402 handlers (use `@stellar/mpp/charge/server`)
- Channel-mode payments (off-chain commitments — use `@stellar/mpp/channel/client` directly if you need them)
- Non-Stellar payment origination (if paying FROM EVM, use a different skill)
- Key management beyond `.env` files (for production-grade, bring your own KMS)
- Channel / trustline destruction (do that by hand — destructive ops not automated)

## References

- `references/x402-exact-spec.md` — x402 Stellar exact scheme wire format
- `references/mpp-charge-spec.md` — @stellar/mpp charge mode wire format
- `references/sponsored-mode.md` — why sponsored is the only cross-compat path
- `references/sdk-api-cheatsheet.md` — common imports and constants
- `references/mainnet-checklist.md` — before going to pubnet

## Files in this skill

```
stellar-agent-wallet/
├── SKILL.md                          ← you are here
├── references/                       ← on-demand context
│   ├── x402-exact-spec.md
│   ├── mpp-charge-spec.md
│   ├── sponsored-mode.md
│   ├── sdk-api-cheatsheet.md
│   └── mainnet-checklist.md
├── scripts/
│   ├── generate-keypair.ts           ← writes .stellar-secret with mode 600
│   └── src/                          ← shared library code
│       ├── secret.ts                 ← file-based secret loader + redactor
│       ├── cli-config.ts             ← shared command-line flag parser
│       ├── stellar-signer.ts         ← sign SAC transfers
│       ├── rozo-client.ts            ← Rozo intent API client
│       ├── mpprouter-client.ts       ← MPP Router catalog client
│       ├── pay-engine.ts             ← 402 parse + retry orchestrator
│       ├── x402.ts                   ← x402 envelope encoder
│       ├── mpp-envelope.ts           ← MPP charge envelope encoder
│       └── balance.ts                ← shared balance reader (onboard + check-balance)
└── skills/                         ← sub-skills (run directly)
    ├── onboard/
    │   ├── SKILL.md
    │   └── run.ts                    ← readiness check + guided setup
    ├── check-balance/
    │   ├── SKILL.md
    │   ├── run.ts                    ← balance check
    │   ├── add-trustline.ts          ← enable Classic USDC
    │   └── swap-xlm-to-usdc.ts       ← DEX path payment
    ├── discover/
    │   ├── SKILL.md
    │   └── run.ts                    ← MPP Router catalog
    ├── pay-per-call/
    │   ├── SKILL.md
    │   └── run.ts                    ← 402 → pay → retry
    ├── send-payment/
    │   ├── SKILL.md
    │   ├── run.ts                    ← cross-chain via Rozo
    │   └── status.ts                 ← poll payment status
    └── bridge/
        ├── SKILL.md
        └── run.ts                    ← thin wrapper over send-payment
```
