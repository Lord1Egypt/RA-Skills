# User Flows

Use this file when the user is trying to do something on Zeko, not build infrastructure.

## Start here

- Wallet and network basics: `https://docs.zeko.io/users/getting-started`
- App connection flow: `https://docs.zeko.io/users/guides/dapp`
- Bridging flow: `https://docs.zeko.io/users/guides/zeko-bridge`
- Sending tokens: `https://docs.zeko.io/users/guides/sending-tokens`

## Agent interpretation

- For Ethereum bridging in a browser, MetaMask signs on L1 and the Zeko Snap manages the B62 L2 account. Other wallets such as Auro are supported only where the selected deployment exposes them.
- If the user asks for automation, prefer direct env vars, SDK calls, CLI calls, or `curl`.
- For Ethereum-backed Zeko, use the explorer linked by the selected deployment and its Ethereum transaction links. `https://zekoscan.io/testnet` and `https://zekoscan.io/mainnet` are legacy Zeko-M explorer references.
- If the user asks how to send native MINA from one address to another, route to `references/40-endpoints-and-curl.md` for the `sendPayment` flow and base-unit conversion.

## Quick routing

- Need faucet funding or JSON output: read `references/30-bridge-and-faucet.md`.
- Need endpoint values or explorer/API checks: read `references/40-endpoints-and-curl.md`.
