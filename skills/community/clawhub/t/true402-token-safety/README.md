# true402-token-safety — OpenClaw skill

Rug-check any Base token before trading, from inside [OpenClaw](https://openclaw.ai): a **real buy/sell honeypot simulation** (proves the token is sellable, not just a static scan) plus liquidity and ownership checks, returning one `AVOID / CAUTION / OK` verdict.

Powered by [true402.dev](https://true402.dev) — pay-per-call over [x402](https://x402.org), no accounts, no API keys. The first few checks each day are **free, no wallet needed**.

## Install

```bash
openclaw skills install true402-token-safety
```

or copy this directory to `~/.openclaw/workspace/skills/true402-token-safety/`.

## Make it automatic

A skill is guidance the agent can forget. The [true402 swap guard](https://github.com/true402/openclaw-swap-guard) plugin runs the same check on **every** tool call that buys a token and blocks honeypots and rugs:

```bash
openclaw plugins install clawhub:@true402.dev/openclaw-swap-guard
```

## Use

Ask your agent things like:

> "Is 0x532f…42E4 safe to buy?"
> "Rug-check this token before you snipe it."

The agent runs `npx -y @true402.dev/rugcheck@1.3.4 0x…` and gates on the verdict (non-zero exit on AVOID or on a failed check).

## Optional: unlimited checks

Set `PAYER_PRIVATE_KEY` to a Base wallet holding a little USDC to pay ~$0.008 per check over x402 (gas sponsored — the wallet needs no ETH). The key signs locally and is never sent anywhere; the client refuses to sign any single charge above **$0.25**. Without a key, the free daily trial applies.

### Handling that key

A private key in an environment variable is reachable from shell history, process listings, crash
dumps, container introspection and any log that prints the environment. The design already limits
the damage — signing is local, and the client will not sign a charge above $0.25 — but the wallet is
still spendable by anything that can read the variable. So:

- **Use a dedicated wallet, funded with a few dollars.** Never a wallet holding anything you would
  mind losing, and never one that is also an identity or a treasury.
- **Keep it out of files that travel.** No `.env` in git, no plaintext in a Dockerfile or CI log.
  A secret manager or a local-only file with restricted permissions; export it in the shell that
  needs it, not in a global profile.
- **Top it up rather than pre-loading it.** The per-call cost is fractions of a cent, so a small
  float covers thousands of checks and bounds the worst case.
- **Rotate by moving on.** There is no revocation for a leaked key — generate a new wallet, move the
  remaining balance, and stop using the old one.
- **You do not need it to evaluate this.** The free daily trial returns the same real verdict with
  no wallet at all; add a key only when the volume needs it.

## Links

- Live in-browser check: https://true402.dev/check
- API reference: https://true402.dev/docs/api
- OpenAPI: https://true402.dev/openapi.json
- MCP server (all stalls as agent tools): `npx @true402.dev/mcp-server@1.3.2`

## License

MIT-0 (per ClawHub policy).
