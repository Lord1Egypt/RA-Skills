---
name: trenchytools
description: "Launch and trade memecoins through the TrenchyTools API (pump.fun, PumpSwap, pons on Robinhood Chain). Use when asked to launch a token, bundle-buy at launch, snipe an auto-buy, or give an agent trading with a single API key instead of an RPC node, Jito client and IPFS keys."
---

# TrenchyTools

One API key replaces the RPC node, the Jito client and the IPFS keys. The API builds
**unsigned** transactions; you sign locally with `@solana/web3.js` (Solana) or `viem`
(Robinhood Chain) and submit. Keys never leave the machine.

- Base URL: `https://api.trenchy.tools`
- Agent instructions: `https://api.trenchy.tools/AGENTS.md` (read this first)
- Spec: `https://trenchy.tools/openapi.json` · Live capabilities: `GET /api/chains`
- Only use paths that exist in the spec; never invent endpoints or fields.

## Auth: prefer the header

Send the key in the `x-api-key` header on every request. Prefer it over `?api-key=` because
a key in the URL ends up in server logs, referrers and shell history.

```bash
curl -H "x-api-key: ***" "https://api.trenchy.tools/api/me"
```

The query form (`?api-key=***`) still works and is the only option for the WebSocket
(`wss://api.trenchy.tools/api/sol/data?api-key=***`), which cannot send headers.

## Get a key

```bash
curl "https://api.trenchy.tools/api/create-api-key?label=my-agent"
# -> {"apiKey":"***"}  shown once; store it, then send it as the x-api-key header
```

## Rules (non-negotiable)

1. **Back up every wallet to disk before funding it** — a missing file answers `409 not_backed_up`.
2. `trade-local` returns an unsigned transaction: sign it yourself, then `send`.
3. **Simulate first**, start tiny (0.01 SOL / 0.001 ETH).
4. Branch on the error `code`; `429` carries `retry-after`; check `GET /tx/:id` before retrying a send
   (a landed retry is a second trade).
5. Never promise a profit or a landing; report what was built, simulated, sent and confirmed.

## The flows

- **Trade:** `POST /api/sol/trade-local` -> sign -> `POST /api/sol/send` -> `GET /api/sol/tx/:sig`
- **Launch:** `POST /api/ipfs` (image + metadata -> `metadataUri`) -> generate a mint keypair locally ->
  `POST /api/sol/trade-local` with `action:"create"`, `mint`, `tokenMetadata:{name,symbol,uri}`, `amount`
  -> sign with wallet + mint -> `send`
- **Bundle (create + buyers in one block):** array body to `trade-local` (create first, buys after; the first
  `priorityFee` is the Jito tip) -> sign each -> `POST /api/sol/bundle` -> `GET /api/sol/bundle/:id`.
  More than 4 buyers: call `POST /api/sol/lut` first.
- **Robinhood Chain (pons):** `POST /api/rh/trade-local` -> sign with `viem` -> `POST /api/rh/send` ->
  `GET /api/rh/tx/:hash`. Sells accept `"100%"` or `"NN%"`.
- **Stream:** `wss://api.trenchy.tools/api/sol/data?api-key=***` with `subscribeNewToken`,
  `subscribeTokenTrade`, `subscribeMigration`.

## Amounts

Solana: `amount` is SOL when `denominatedInSol:"true"`, tokens otherwise. Robinhood: ETH when
`denominatedInEth:"true"`. Slippage is a percent. `pool:"auto"` follows a coin curve -> AMM.

## Starters

- `github.com/Trenchy-Tools/pumpfun-starter` (Solana) · `github.com/Trenchy-Tools/pons-starter` (Robinhood Chain)
- `github.com/Trenchy-Tools/wallet-mover` (create/fund/split wallets; shares one wallet folder)
- Demos: `pumpfun.trenchy.tools` · `pons.trenchy.tools` · `mover.trenchy.tools`
