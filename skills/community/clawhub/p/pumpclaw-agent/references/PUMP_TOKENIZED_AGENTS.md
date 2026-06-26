# Pump Tokenized Agents (agent-payments-sdk) — Integration Notes

This skill templates a Telegram (polling) + web server project and highlights how to integrate Pump Tokenized Agent payments using `@pump-fun/agent-payments-sdk`.

Core ideas:

- Build accept-payment instructions via `buildAcceptPaymentInstructions`.
- User signs client-side; server verifies payment server-side via `validateInvoicePayment`.
- Never handle or log private keys.

Primary reference skill:
- https://raw.githubusercontent.com/pump-fun/pump-fun-skills/refs/heads/main/tokenized-agents/SKILL.md

Env vars commonly required:
- `SOLANA_RPC_URL`
- `AGENT_TOKEN_MINT_ADDRESS`
- `CURRENCY_MINT`

CURRENCY_MINT defaults:
- USDC: `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`
- wSOL: `So11111111111111111111111111111111111111112`
