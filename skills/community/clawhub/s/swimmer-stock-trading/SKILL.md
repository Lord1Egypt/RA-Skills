---
name: swimmer-stock-trading
description: Discover Swimmer Finance Solana stock-token routes and balances, then submit a custodial order instruction by irreversibly transferring USDC or a trusted stock token to the fixed operator recipient with a public memo. Use for pool discovery, tradability checks, optional quotes, balance checks, market or limit order preparation, explicit risk confirmation, local signing, submission, and settlement-status checks. This is not an atomic on-chain swap and does not guarantee execution, consideration, cancellation, or refund.
metadata:
  openclaw:
    emoji: "📈"
    requires:
      bins: ["python3"]
    permissions:
      filesystem: true
      network: true
    capability_scope:
      filesystem_read: ["~/.config/swimmer-stock-trading/config.json"]
      network_connect: ["https://api.mainnet-beta.solana.com", "https://api.sharesdao.com:8443"]
---

# Swimmer custodial stock-order submission

Use this skill only for Swimmer-issued stock-token routes settled in canonical USDC on Solana mainnet. No registration, login, or service API key is required. The user funds a dedicated low-balance wallet with USDC and a small amount of SOL for network fees.

Submission is an irreversible SPL-token transfer to a fixed Swimmer custodial recipient plus a public memo. It is not an atomic swap. The Solana transaction cannot enforce order execution, delivery of the requested asset, cancellation, or refund. Read [references/custody-and-settlement.md](references/custody-and-settlement.md) before preparing an order.

## Mandatory security boundary

- Never ask for or display a seed phrase, private key, wallet export, or config contents. If a secret appears in chat or output, tell the user to treat it as compromised and move funds from a separate trusted device.
- The human creates `~/.config/swimmer-stock-trading/config.json` in a trusted local editor. Only the packaged signer reads it. The CLI has no config-path option and opens only that path without following symlinks.
- Use a new dedicated wallet with only the amount at risk. This hot-wallet setup is not as strong as a hardware wallet or isolated signer.
- Require exact directory mode `0700`, file mode `0600`, current-user ownership, an independently verified recipient acknowledgement, trusted ticker-to-mint mappings, and raw per-mint spending caps.
- Use only `https://api.mainnet-beta.solana.com` and `https://api.sharesdao.com:8443`. Do not ask the user for a base URL, RPC API key, or registration.
- Do not use EVM, devnet, testnet, native-SOL settlement, arbitrary tokens, legacy `.S` symbols, `/router/swap`, API-supplied calldata, or API-supplied transactions.
- Show the exact irreversible-transfer authorization and confirmation digest immediately before signing. Preparation, route discovery, quoting, and balance checks are not authorization.

The metadata declares filesystem and network access because those are the capabilities the runtime exposes. The signer further restricts secret reads to one fixed file, and these instructions restrict network destinations to the two fixed origins above.

## Workflow

1. For initial setup, follow [references/keypair-setup.md](references/keypair-setup.md). The user must independently verify the fixed custodial recipient and each stock mint before putting them in the protected config.
2. Discover pools and exact Solana USDC routes using [references/protocol.md](references/protocol.md). A route response is discovery data, not independent proof of mint ownership or settlement.
3. Check SOL, USDC, and the trusted stock-token balance with [references/balances.md](references/balances.md). Stop on insufficient offered-token balance or insufficient SOL.
4. Collect ticker, BUY/SELL, MARKET/LIMIT, raw offered amount, and raw requested amount. A LIMIT requires a positive exact request. A MARKET uses request `0` unless the user explicitly asks for an optional estimate.
5. Prepare only the eight public fields documented in [references/wallet-submission.md](references/wallet-submission.md). The recipient is not a plan field; the signer derives it internally.
6. Pipe the plan to `inspect`. Present every returned field, especially the full destination, safety cap, non-atomic settlement warning, and whether a MARKET order has no on-chain minimum receive.
7. Ask the user to authorize that exact irreversible transfer and digest. Do not soften this into “confirm trade.”
8. Only after explicit confirmation, pipe the identical plan to `send --confirm <digest>`. The signer fetches a fresh blockhash, constructs exactly one classic SPL transfer plus one memo, simulates with signature verification, and submits with preflight.
9. Report the signature as submitted only. Check on-chain confirmation and the service’s order status separately. Never auto-retry an uncertain submission.

## Stop conditions

Stop without signing if config checks fail; the recipient or stock mint has not been independently verified; the ticker/mint is absent from the protected allowlist; a spending cap is missing or exceeded; a route is not exact Solana USDC; the plan has extra fields; the user has not accepted the non-atomic custodial risk; the confirmation digest differs; simulation fails; or settlement/refund terms cannot be verified from an official source.
