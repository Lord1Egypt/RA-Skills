---
name: vaultline
description: Use when an agent needs to store, retrieve, list, inspect, or delete files through Vaultline, or when it needs to choose between open and private storage tiers, construct the required wallet-auth headers for private objects, or follow the x402 pay-and-retry flow for uploads and downloads. Also use when explaining that encrypted storage is coming soon but not live.
version: 0.1.2
metadata:
  openclaw:
    homepage: https://github.com/BuiltByEcho/vaultline
    requires:
      bins:
        - node
        - npm
    install:
      - id: vaultline-sdk
        kind: node
        package: "@builtbyecho/vaultline-sdk"
        bins: []
        label: Install Vaultline SDK from npm
---

# Vaultline

Use this skill to work with the Vaultline API correctly and consistently.

## Quick workflow

1. Decide the storage tier.
2. Build the exact file path/key.
3. Upload, read, head, list, or delete with the correct headers.
4. For paid operations, follow the x402 pay-and-retry flow.
5. For private objects, require wallet-auth headers before access.
6. Treat encrypted storage as coming soon, not live.

## Tier decision

- Use `open` for shared/public-by-key files.
- Use `private` for wallet-restricted files.
- Do not use `encrypted` as a live tier yet.

Read `references/pricing-and-tier-selection.md` when you need pricing, tradeoffs, or help choosing a tier.

## Core rules

- Default to `open` if no tier is specified.
- Require `x-storage-tier: private` for private uploads.
- Require wallet-auth headers for private upload, read, head, delete, and any list call that should reveal private objects.
- Treat open files as readable by anyone who knows the path and satisfies any payment requirement.
- Keep the original request intact when retrying after `402` payment negotiation.
- Preserve `content-type` and `content-length` on uploads.
- Do not claim encrypted/ciphertext storage exists yet.

## Private auth rules

For private operations, send:
- `x-auth-wallet`
- `x-auth-timestamp`
- `x-auth-signature`

The signature must cover:
- HTTP method
- request path
- wallet
- timestamp

Read `references/api-examples.md` for the exact auth message format and request examples.

## Pay-and-retry rules

For paid uploads or large paid reads:
1. Send the request normally.
2. If the server returns `402`, parse the `payment-required` header.
3. Create/sign the x402 payment payload.
4. Retry the same request with the payment header.
5. Expect the normal route response.

## Current Bankr endpoints

Primary public Bankr x402 endpoints are owned by `builtbyecho@agentmail.to` / `0x2a16625fad3b0d840ac02c7c59edea3781e340ae`:

- `https://x402.bankr.bot/0x2a16625fad3b0d840ac02c7c59edea3781e340ae/vaultline-upload`
- `https://x402.bankr.bot/0x2a16625fad3b0d840ac02c7c59edea3781e340ae/vaultline-download`
- `https://x402.bankr.bot/0x2a16625fad3b0d840ac02c7c59edea3781e340ae/vaultline-list`

## Task patterns

### Upload a shared file
- Use `open`.
- Upload normally.
- If the server returns `402`, pay and retry.

### Upload a private file
- Use `private`.
- Attach wallet-auth headers.
- Optionally attach `x-owner-wallet` and `x-allowed-wallets`.
- If the server returns `402`, pay and retry.

### Read a private file
- Always attach wallet-auth headers first.
- Expect `401` when auth headers are missing or invalid.
- Expect `403` when the wallet is authenticated but not authorized.
- If authorized and the read is billable, pay and retry after `402`.

### Explain the product tiers
- Say `open` is live.
- Say `private` is live.
- Say `encrypted` is coming soon.
- Frame them as: sharing -> ownership -> maximum privacy.
