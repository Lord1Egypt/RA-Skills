---
name: x402card-agent
description: Discover, issue, top up, and manage an x402card wallet-owned virtual card through public Base-USDC x402 entrypoints, including exact-payment validation, payer ownership, idempotent recovery, asynchronous issuance or funding, owner authentication, balance, and secure credential reveal. Use when an owner wants a virtual card, wants to add funds to an active card, or needs the x402card card contract without exposing a private key.
---

# x402card agent

Install the public CLI with `curl -sSL https://x402card.org/install | sh`, or use the local runtime in `packages/agent` from a source checkout. Use the public MCP only for discovery because it has no wallet authority.

## Safe workflow

1. Read `https://api.x402card.org/api/card/discovery`, `https://api.x402card.org/api/agent`, and runtime config before a money action.
2. Obtain explicit approval for the fixed economics: the wallet pays 25 USDC on Base, the card starts at $25, the platform fee is $10, and the expected available balance is $15.
3. Generate one stable idempotency key. POST it to `https://api.x402card.org/api/card/purchase` without `PAYMENT-SIGNATURE`; this returns a 402 challenge and does not charge the wallet.
4. Validate x402 v2, scheme `exact`, Base `eip155:8453`, native Base USDC, amount `25000000`, the expected payee, and resource `/api/card/purchase`.
5. Submit the same body once with `PAYMENT-SIGNATURE`. The x402 payer becomes the card owner. Preserve `orderId` and treat issuance as pending until the provider reports the card active.
6. If the paid response is ambiguous, repeat only the same body and idempotency key. Require `replayed: true`; never create or sign a replacement payment.
7. Authenticate the payer wallet only for owner reads: card list, balance, status, and credential reveal. Credentials require a fresh owner signature and must stay out of MCP, chat, logs, stdout, files, and model context.

## Top-up workflow

1. Require an active card and read `https://api.x402card.org/api/card/topup/discovery` plus live runtime config.
2. Obtain explicit approval for the gross amount. Current limits are 25–250 USDC and the current load fee is 2%; verify both live before signing.
3. Generate one stable idempotency key. POST `{ "amountUsdCents": 5000, "idempotencyKey": "..." }` to `https://api.x402card.org/api/card/topup` without `PAYMENT-SIGNATURE`.
4. Validate x402 v2, exact Base USDC, expected payee, resource `/api/card/topup`, and atomic amount `amountUsdCents * 10000`.
5. Submit the same body once with `PAYMENT-SIGNATURE`. The payer must own the active card. Funding is asynchronous; settlement is not proof that the card was credited.
6. After an ambiguous response, repeat only the same body and key and require a verified replay. Never authorize a replacement payment.

The installed CLI remains a supported authenticated fallback: configure `X402CARD_SIGNER_COMMAND`, run `x402card-agent status`, then `x402card-agent issue` once or `x402card-agent topup <usd>` for an active card. Stable operation keys recover the same issue or funding order. To top up the same amount again after the prior operation is confirmed funded, use `x402card-agent topup <usd> --new`; it refuses to rotate an unresolved operation. Use `operation`, `cards`, and `balance` to read progress, and `reveal` only to the controlling TTY or explicit clipboard.

The local MCP command is `x402card-mcp`. It may use the signer for bounded owner and issue operations, but it intentionally exposes no generic signing tool and no credential-reveal tool.

Treat unknown settlement state as pending/operator review. Never generate a second payment or change an idempotency key to bypass a pending operation.
