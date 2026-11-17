---
name: xh-agents-x402
description: Pay-per-call x402 data for AI agents on Base. It does two different things: (1) free discovery - list and price 42 paid routes (endpoint trust scoring, token safety, wallet/market intel, document extraction, knowledge-base answers); (2) paid execution - sign and send real USDC payments for those routes using a private payer key the skill reads locally from the XH_PAYER_KEY environment variable or from the file named by XH_PAYER_KEY_FILE. Use when an agent must vet another x402 endpoint before paying it, screen a Base token, or buy per-call on-chain data with its own wallet. Install only where a skill reading a funded wallet key and moving USDC is acceptable.
---

# XH Agents - paid x402 data, one call at a time

42 paid x402 routes on Base, USDC per call, no API key, no signup. Everything is paid with a wallet
you already control; nothing here needs an account with us.

This skill contains a payer, not just a client. Read the next two sections before installing it in
an environment where a wallet key lives.

## What this skill can do to your machine

- **Moves money.** `pay` signs an EIP-3009 USDC authorization and sends it to the seller's
  facilitator. Real USDC leaves the wallet whose key you provided. No other action moves funds.
- **Reads a private key.** Only from `XH_PAYER_KEY` (env) or the file named by `XH_PAYER_KEY_FILE`.
  The key stays in the process: never printed, never logged, never written to disk, never sent to
  any host other than as a signature over the payment authorization.
- **Network access.** HTTPS to `xhagents.xyz` (catalogue and product calls), to public Base
  JSON-RPC endpoints (`1rpc.io`, `base.drpc.org`, `mainnet.base.org`) for the balance read, and
  through the official `x402` SDK to the seller's facilitator.
- **No writes, no shell.** No filesystem writes, no subprocess, no `exec`/`eval`, no dynamic
  imports, no environment mutation.

## Declared permissions

| Capability | Scope | Used for |
|---|---|---|
| network (HTTPS) | `xhagents.xyz`, public Base RPC hosts, facilitator hosts reached by the `x402` SDK | catalogue, price quotes, balance, settlement |
| env read | `XH_PAYER_KEY`, `XH_PAYER_KEY_FILE`, `XH_MAX_PRICE_USDC` | locate the payer key, set the ceiling |
| file read | only the single path given in `XH_PAYER_KEY_FILE` (expected mode 600) | payer key |
| file write | none | - |
| process exec | none | - |

Consent gate: none of this happens unless someone deliberately exports a funded key for this skill.
The free modes (`catalogue`, `quote`) never read the key at all, and `whoami` reads it only to print
your own address and balance.

## Discover before you buy (free, no key)

```bash
python3 scripts/xh_pay.py catalogue                                  # every paid route + summary
python3 scripts/xh_pay.py quote https://xhagents.xyz/api/x402-trust --method POST  # price first
```

Discovery documents: `https://xhagents.xyz/openapi.json`, `https://xhagents.xyz/.well-known/x402`,
`https://xhagents.xyz/llms.txt`. Human-readable catalogue: `https://xhagents.xyz/`. Our own
published numbers (settled calls, USDC received, treasury balance) are on
`https://xhagents.xyz/trust/` - we disclose our traffic rather than inflate it.

## Pay (this spends USDC)

```bash
export XH_PAYER_KEY_FILE=~/.xh-payer.key    # mode 600, plain hex key of a funded Base wallet
python3 scripts/xh_pay.py whoami            # address + balance, so nothing is paid blind
python3 scripts/xh_pay.py pay https://xhagents.xyz/api/x402-trust \
    --method POST --body '{"url":"https://the-endpoint-you-are-checking.com/api/thing"}' --max 0.10
```

`pay` reads the 402 challenge, refuses it when any guard below fails, signs an EIP-3009
authorization, retries with the payment header, and prints the product plus the decoded
`PAYMENT-RESPONSE` settlement proof. Under the hood it is the official `x402` Python client
(`x402ClientSync` + `ExactEvmClientScheme` on `eip155:8453`); no gas is needed because the
facilitator pays it. `--pay-to <addr>` (repeatable) restricts the destination to an allowlist.

If you prefer tools over shell: the same engine is exposed as an MCP server
(`mcp_server.py`: `xh_catalogue`, `xh_quote`, `xh_provenance`, `xh_trust_score`, `xh_token_safety`,
`xh_call`).

## Guards enforced in code (not by convention)

1. **Quote before paying.** The live 402 challenge is authoritative; never sign a cached price.
2. **Price ceiling.** `--max` defaults to $0.10. A challenge above it is refused before signing.
3. **Asset allowlist.** Only canonical USDC on Base
   (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`, name `USD Coin`) can be signed for. A ceiling
   alone is bypassable: a hostile seller can quote a small amount in a different token, or in the
   same token with different decimals.
4. **Network locked.** Only `eip155:8453` - with the documented x402 v1 shorthand `base` accepted
   as an alias for it (the authorization is always built for `eip155:8453`). Anything else is refused.
5. **Destination shown and optionally restricted.** `quote` prints `payTo`; `--pay-to` allowlists it.
6. **Keep the settlement proof.** `pay` prints the decoded `PAYMENT-RESPONSE` - store it with the
   result, it is your receipt.
7. **A 402 is not an error** - it is the price tag. Only a paid retry should return 200.

## The calls agents actually use

| Route | Price | What you get |
|---|---|---|
| `POST /api/x402-trust` | $0.05 | 0-100 trust score for any x402 endpoint: gate behaviour, challenge conformance, discovery docs, payTo reputation, price sanity, with the penalties named |
| `POST /api/token-safety` | $0.05 | 0-100 Base token safety score with the components that lost points |
| `POST /api/wallet-profile`, `/api/whale-watch`, `/api/gas-tracker` | $0.10 | wallet profile, whale moves, Base gas |
| `POST /api/arkham-intel/*` | $0.10 | portfolio, counterparties, pool flow, fund trace (6 routes) |
| `POST /api/trust-leaderboard` | $0.05 | x402 sellers ranked by trust (free method page: `/api/trust-leaderboard/method`) |
| `POST /api/document-extract` | $0.05 | PDF/scan to text with OCR, sha256 of the bytes |
| `POST /api/domain-audit` | $0.05 | domain + email deliverability audit |
| `POST /api/kb/ask`, `POST /api/chat` | $0.30 | knowledge-base answer / market question |
| `GET,POST /api/compute/xh-bundle` | $0.91 | 13 production playbooks on shipping a paid x402 API (GET returns the free index) |

Full list with live prices: `python3 scripts/xh_pay.py catalogue` (do not trust a price table in a
document, including this one - quote the route). `references/routes.md` is generated from live
challenges.

## Requirements

Python 3.10+, `pip install x402 eth_account`. A funded Base wallet for paid calls (USDC only; no ETH
needed - the facilitator sponsors gas). Free calls (`catalogue`, `quote`) need nothing.
