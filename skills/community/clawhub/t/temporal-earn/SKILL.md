---
name: temporal-earn
description: Use when holding idle USDC on Hyperliquid and looking for yield, when already holding a BTC perp and wanting extra income on it (covered-call style), or when building a market-making bot for options. TLP is the default way to earn (one deposit, the venue quotes and manages for you); Custom is the port a maker's existing pricing, limits and margin systems plug into.
license: MIT
metadata:
  homepage: https://temporal.exchange
  docs: https://protect.temporal.exchange/docs/earn
  tags: [hyperliquid, yield, market-making, options, lp, defi]
---

# Earning on Temporal (making option markets)

Makers answer traders' option requests with firm signed quotes. They earn **half the oracle venue's at-the-money spread** plus **holding cost on options they've written**, minus the venue's 10%, and pay **no trading fee**. Flow is anonymous: requests never name the trader.

## Pick a mode: TLP first

- **TLP is the default way to earn.** One deposit, spread across the largest markets (min $10 each). The venue prices and manages for you, quoting the oracle venue's bid/ask. No bot, no program. Preview with `temporal_earn_plan` (`POST /earn/plan`), then turn it on with `temporal_maker_quoting` (`mode: "auto"`, `tlp: true`).
- **Custom is the port a maker's existing setup plugs into.** Choose it only if you bring your own pricing. Temporal does not run your strategy: it gives requests in, signed quotes out, and your account's state and acts for your own risk and margin systems. You own your pricing, exposure limits, stop rules and margin. The venue enforces only its hard limits: the **price limit** around the oracle, **margin and liquidation**, **open-interest caps**, your **room**, and the quote's signature, expiry (firm 2 s+) and nonce. A runnable reference client with four hooks (`price`, `withinLimits`, `shouldQuote`, `manageMargin`) is in `examples/custom-maker`.

## Every maker action and its tool

Maker routes need a venue session: `temporal_session_prepare` (the message to sign) -> the human's wallet signs it (EIP-191, no gas, no funds) -> `temporal_session_open` (a bearer token). Pass the token as `token` on each maker call; this server stores nothing and logs nothing; never print it. End it with `temporal_session_close`. Every maker **write** needs `confirmed: true` after you described the change and the human said yes; writes are never retried and refusals come back by name.

| Action | Tool (route) | Mode |
|---|---|---|
| Open a session | `temporal_session_prepare`, `temporal_session_open` (`/auth/nonce`, `/auth/verify`) | both |
| Read accounts, quoting, margin, liquidation distance | `temporal_maker_state` (`/state`) with `wallet` for the ledger numbers | both |
| Fund / take money out | `temporal_build_call` acts `mintAccount` (kind earn), `deposit`, `withdraw`, then dry-run and the wallet signs | both |
| Quoting on / off | `temporal_maker_quoting` (`/account/quoting`; TLP = `mode: "auto"`, `tlp: true`; Custom = `mode: "custom"`) | both |
| Caps and half-spread | `temporal_maker_settings` (`/account/curve`: `Eplus` net long cap in coins, `Eminus` net short cap, `hBps` half-spread 0-150) | TLP / AUTO |
| Markets an account quotes | `temporal_maker_asset` (`/account/asset`) | TLP / AUTO |
| Covering perp, read and set | `temporal_maker_perp` (`/account/makerPerp`: long covers sold calls, short sold puts) | both |
| Name an account | `temporal_maker_rename` (`/account/rename`) | both |
| Register / list / remove a bot | `temporal_maker_register`, `temporal_maker_connections`, `temporal_maker_unregister` (`/rfq/maker/...`) | Custom |
| Close positions, leave, end | `temporal_build_call` acts `closeLegAtFront`, `exitMaker` (hands written options to other makers at market; `ExitOff` while the venue has it off), `closeAccountAtFront` | both |

The bot's own long-poll (`/rfq/maker/poll`) belongs in the bot, not in a tool call: see the reference client.

## Why perp holders fit

If you already hold a long BTC perp (e.g. for funding or basis), selling calls on Temporal can be **covered by that perp**: long perp covers sold calls, short perp covers sold puts (`POST /account/makerPerp`, capped at coins sold on that side, one change per 15 minutes). You keep the perp's funding and add holding cost income.

## Custom: the port, in short

Register (`transport: "poll"` or `"webhook"`), then answer each request `{id, asset, side, wing, strikeK, months, qty, deadlineMs}` inside the window (about 500 ms) with an EIP-712 `Quote` (domain `TemporalQuote` v1, the front contract) or `null`. `qty` covers the full size, `expiry` at least 2 s ahead, `nonce` single-use; `side` is the asker's (0 = they buy, you quote your ask). Protect packages: answer every leg or none. 30 s without a poll marks you offline (you are not asked). Field-by-field: https://protect.temporal.exchange/docs/earn and /docs/agents#makers. An LLM should not sit in the quote path: the pricing runs in your own deterministic system behind the `price` hook.

## Risks to state before depositing

Option P/L can be negative, and the displayed Return excludes it. Sold options are margined; below maintenance plus a 3% penalty you're liquidated. There's no breaker for crossed quotes. Closes return to the maker who wrote the position. Caps limit size, not loss. Open beta: unaudited, $100 per wallet.
