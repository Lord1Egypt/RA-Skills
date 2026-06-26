# Payment Tool Signatures

Known payment tools and how to detect their transactions in tool call results.

## agent-wallet-cli

- **Tool name pattern**: `agent-wallet-cli` or `wallet`
- **Payment indicator**: args contain `x402` subcommand
- **Amount extraction**: `--max-amount` from args; actual amount from response `amount` or `payment.amount`
- **Tx hash extraction**: response `tx_hash`, `transaction`, or `hash` field
- **Currency**: response `currency` field, defaults to USDC
- **Chain**: response `chain` or `network` field

## v402

- **Tool name pattern**: tool name or args contain `v402`
- **Payment indicator**: script name contains `pay` or `http`
- **Amount extraction**: response `amount` or `payment.amount` field
- **Tx hash extraction**: response `signature`, `tx_hash`, or `hash` field
- **Currency**: response `currency` field, defaults to USDC

## ClawRouter

- **Tool name pattern**: `clawrouter` (case-insensitive)
- **Payment indicator**: response contains `cost` or `price` field, or `X-PAYMENT-RESPONSE` header
- **Amount extraction**: response `cost` or `price` field
- **Tx hash extraction**: response `tx_hash` if available (may be aggregated billing with no per-call hash)
- **Note**: ClawRouter is specifically for LLM inference routing

## payment-skill (second-state)

- **Tool name pattern**: `payment-skill`, `payment_skill`, or `pay`
- **Payment indicator**: tool name matches
- **Amount extraction**: response `amount` or `payment.amount` field
- **Tx hash extraction**: response `tx_hash`, `hash`, or `signature` field

## Generic x402

- **Tool name pattern**: any tool
- **Payment indicator**: response body contains `X-PAYMENT-RESPONSE` header or `"x402"` string
- **Amount extraction**: response `amount` or `payment.amount` field
- **Tx hash extraction**: response `tx_hash` or `hash` field
- **Note**: This is the catch-all detector. It fires last, only if no specific detector matched.

---

## Adding New Detectors

To support a new payment tool:

1. Add a section above documenting the tool's name pattern, payment indicators, and field locations
2. Add a corresponding detector function in `server/detectors.js`
3. Register it in the `detectors` array (before the generic x402 catch-all)
