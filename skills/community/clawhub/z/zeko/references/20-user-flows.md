# User Flows

Use this file when the user is trying to do something on Zeko, not build infrastructure.

## Start here

- Wallet and network basics: `https://docs.zeko.io/users/guides/getting-started`
- App connection flow: `https://docs.zeko.io/users/guides/interacting-with-a-dapp`
- Bridging flow: `https://docs.zeko.io/users/guides/using-zeko-bridge`
- Sending tokens: `https://docs.zeko.io/users/guides/sending-tokens`

## Agent interpretation

- If the user asks for a wallet recommendation in a browser session, Auro Wallet is relevant.
- If the user asks for automation, prefer direct env vars, SDK calls, CLI calls, or `curl`.
- If the user asks where to inspect transactions, use `https://zekoscan.io/testnet` for testnet or `https://zekoscan.io/mainnet` for mainnet.
- If the user asks how to send native MINA from one address to another, route to `references/40-endpoints-and-curl.md` for the `sendPayment` flow and base-unit conversion.

## Quick routing

- Need faucet funding or JSON output: read `references/30-bridge-and-faucet.md`.
- Need endpoint values or explorer/API checks: read `references/40-endpoints-and-curl.md`.
