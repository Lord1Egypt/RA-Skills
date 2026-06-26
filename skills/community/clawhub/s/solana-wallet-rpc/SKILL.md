---
name: solana-wallet-rpc
description: Portable Solana wallet operations for agents. Use when an agent needs a Solana wallet for devnet or mainnet workflows such as creating a wallet, getting a wallet address, checking SOL balance, requesting a devnet airdrop, or signing Ed25519 messages and producing base58 signatures for ownership proofs like RockPaperClaw wallet linking. Default to devnet unless the user explicitly wants another network. Do not send funds or sign opaque payloads without explicit approval.
---

# Solana Wallet RPC

**Warning:** This skill creates and uses local Solana private key files. Treat all generated or configured keypair files as secrets. Default usage is intended for **devnet** testing unless the user explicitly asks for another network.

Use the bundled script in `scripts/solana_wallet.cjs` for wallet operations.

## Scope

This skill is intentionally narrow.

It can:

- create or load a local Solana wallet
- print the wallet address
- check SOL balance
- request a devnet SOL airdrop
- sign a text message and return base58 or base64 signatures
- verify a signature against the local wallet
- preview and, with explicit confirmation, optionally submit the RockPaperClaw deposit alias command

It cannot:

- send SPL token transfers
- submit arbitrary Anchor program instructions
- replace a full Solana transaction-capable wallet or MCP

## Safety rules

- Default to **devnet** unless the user explicitly asks for another network.
- Do not send funds or sign opaque payloads without explicit approval.
- Fund-moving commands default to preview mode and require both an explicit keypair and `--execute` before sending a transaction.
- Prefer printing structured JSON output so addresses, balances, and signatures are easy to reuse.
- Treat private keys and keypair files as secrets.
- `create-wallet` refuses to overwrite an existing keypair unless `SOLANA_WALLET_OVERWRITE=1` is set.

## Runtime requirements

This skill bundles a `package.json` with the runtime dependencies it needs, so the required packages are scoped to the skill directory rather than the whole project.

Install them from the skill directory before running the script:

```bash
cd skills/solana-wallet-rpc
npm install
```

Required packages:

- `@solana/spl-token`
- `@solana/web3.js`
- `tweetnacl`
- `bs58`

Why these are used:

- `@solana/spl-token` — associated token account derivation and token-program constants for the RockPaperClaw deposit flow
- `@solana/web3.js` — Solana-native keypair handling, RPC access, balance checks, and devnet airdrops
- `tweetnacl` — Ed25519 message signing compatible with Solana wallet key material
- `bs58` — base58 encoding/decoding for Solana addresses and wallet-link signatures

These are standard Solana/crypto runtime dependencies, not arbitrary network or eval helpers.

## Defaults and configuration

The script supports these env vars:

- `SOLANA_RPC_URL` — defaults to `https://api.devnet.solana.com`
- `SOLANA_WALLET_KEYPAIR` — path to a 64-byte Solana keypair JSON file
- `SOLANA_WALLET_OVERWRITE=1` — allows `create-wallet` to overwrite an existing keypair file

If `SOLANA_WALLET_KEYPAIR` is not set, the script tries common defaults such as:

- `~/.config/solana/id.json`
- `~/.solana/id.json`
- `~/.openclaw/wallets/solana-devnet.json`
- `~/.openclaw/wallets/solana.json`

When creating a new wallet without an explicit path, the script defaults to:

- `~/.openclaw/wallets/solana-<network>.json`

Override the env vars when using a different wallet or network. Auto-discovery is intended for wallet lookup and signing workflows; fund-moving commands should use an explicit `--keypair` or `SOLANA_WALLET_KEYPAIR`.

For RockPaperClaw deposits, the program ID and USDC mint are pinned to the canonical devnet values unless you pass explicit CLI flags.

These environment variables are local script settings for this wallet helper only. They are not required by the main `rockpaperclaw` skill.

## Commands

Run from the repo root unless there is a reason not to:

```bash
node skills/solana-wallet-rpc/scripts/solana_wallet.cjs create-wallet
node skills/solana-wallet-rpc/scripts/solana_wallet.cjs create-wallet /path/to/keypair.json
node skills/solana-wallet-rpc/scripts/solana_wallet.cjs address
node skills/solana-wallet-rpc/scripts/solana_wallet.cjs balance
node skills/solana-wallet-rpc/scripts/solana_wallet.cjs airdrop 1
node skills/solana-wallet-rpc/scripts/solana_wallet.cjs sign-message "your message here"
node skills/solana-wallet-rpc/scripts/solana_wallet.cjs verify-message "your message here" "<signature>"
node skills/solana-wallet-rpc/scripts/solana_wallet.cjs rockpaperclaw-deposit <agent-id> <amount-micro-usdc> --keypair /path/to/keypair.json
```

`verify-message` accepts either **base64** or **base58** signatures.

## Common workflows

### Create a wallet

```bash
node skills/solana-wallet-rpc/scripts/solana_wallet.cjs create-wallet
```

This generates a new keypair and stores it at a safe default path such as `~/.openclaw/wallets/solana-devnet.json`.

If you want a specific file path:

```bash
node skills/solana-wallet-rpc/scripts/solana_wallet.cjs create-wallet ~/.config/solana/id.json
```

### Get wallet address

```bash
node skills/solana-wallet-rpc/scripts/solana_wallet.cjs address
```

Use this when another tool or service needs the wallet public key.

### Check balance

```bash
node skills/solana-wallet-rpc/scripts/solana_wallet.cjs balance
```

Use this before attempting any onchain action.

### Request devnet SOL

```bash
node skills/solana-wallet-rpc/scripts/solana_wallet.cjs airdrop 0.25
```

Notes:
- Devnet faucets often rate-limit or run dry.
- If the faucet returns 429, report that clearly and stop retrying aggressively.

Important:
- This airdrop funds **SOL for fees only**.
- It does **not** fund the wallet with USDC for RockPaperClaw deposits.

### Get devnet USDC for RockPaperClaw

RockPaperClaw bankroll funding uses canonical devnet USDC, not SOL.

- Use this skill to get the wallet address and, if needed, some devnet SOL for fees.
- Then use the official **Circle faucet** at `https://faucet.circle.com/` to send canonical test USDC to that same wallet address when the faucet supports your target network.
- In the faucet UI, confirm the network selection matches the network you are using before submitting the request.
- Circle's faucet page indicates rate limits can apply per stablecoin and test network pairing.
- The canonical devnet USDC mint used by RockPaperClaw is `4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU`.
- After the wallet has both fee SOL and devnet USDC, continue with `get_deposit_info` and the RockPaperClaw deposit flow.

### Sign a message

```bash
node skills/solana-wallet-rpc/scripts/solana_wallet.cjs sign-message "wallet link for agent <agent-id>"
```

Return the JSON fields clearly:
- `address`
- `message`
- `signatureBase58`
- `signatureBase64`

### RockPaperClaw deposit alias

```bash
node skills/solana-wallet-rpc/scripts/solana_wallet.cjs rockpaperclaw-deposit <agent-id> <amount-micro-usdc> --keypair /path/to/keypair.json
```

Preview example:

```bash
node skills/solana-wallet-rpc/scripts/solana_wallet.cjs rockpaperclaw-deposit 87a28ffe-5870-4789-ac52-ba5f4c49b38a 1000000 --keypair ~/.config/solana/id.json
```

Execute example:

```bash
node skills/solana-wallet-rpc/scripts/solana_wallet.cjs rockpaperclaw-deposit 87a28ffe-5870-4789-ac52-ba5f4c49b38a 1000000 --keypair ~/.config/solana/id.json --execute
```

This is a convenience signer path for RockPaperClaw users who are already in the wallet skill. The canonical RockPaperClaw flow is: use the main `rockpaperclaw` skill for `get_profile` and `get_deposit_info`, then use a separate wallet tool such as this one for the actual signed transaction. Without `--execute`, this command only prints a preview.

## RockPaperClaw note

For RockPaperClaw, the likely sequence is:
1. Create or locate a wallet.
2. Get the wallet address.
3. Construct the exact message the service expects.
4. Sign that exact message.
5. Pass `wallet_address`, `message`, and the **base58** signature into `link_wallet`.
6. When funding chips, call `get_deposit_info` in the main `rockpaperclaw` skill to confirm the current program ID, vault, mint, and agent ID.
7. Use a separate wallet tool for the actual deposit signing step. This wallet helper can do that if you explicitly want a local script-based signer.

If a service rejects the signature, verify whether it expects base58, base64, or hex before changing anything else.

For deposits specifically, think of the RockPaperClaw flow as:

- `get_profile` to get `agent_id`
- `get_deposit_info` to confirm deposit metadata
- fund the wallet with canonical devnet USDC from the Circle faucet
- use `rockpaperclaw` to verify deposit metadata, then use a separate wallet tool to sign and send the Anchor deposit transaction

This wallet skill can perform the same deposit transaction through `rockpaperclaw-deposit`, but that command is a convenience path when you are already in this skill for wallet setup.

## RockPaperClaw example flows

### Wallet-link flow

1. In RockPaperClaw, call `get_profile` and copy the `agent_id`.
2. Run `node skills/solana-wallet-rpc/scripts/solana_wallet.cjs address` and copy `address`.
3. Build the exact message `RockPaperClaw wallet link: <agent-id>`.
4. Run `node skills/solana-wallet-rpc/scripts/solana_wallet.cjs sign-message "RockPaperClaw wallet link: <agent-id>"`.
5. Copy `signatureBase58` from the JSON output.
6. Call `link_wallet` in RockPaperClaw with the wallet address, exact message, and base58 signature.

### Deposit-prep flow

1. In RockPaperClaw, call `get_profile` and copy the `agent_id`.
2. In RockPaperClaw, call `get_deposit_info` and copy the program ID, mint, vault, and config PDA.
3. Run `node skills/solana-wallet-rpc/scripts/solana_wallet.cjs balance` to confirm SOL for fees.
4. If needed on devnet, run `node skills/solana-wallet-rpc/scripts/solana_wallet.cjs airdrop 0.25`.
5. Use the Circle faucet to fund that same wallet with canonical devnet USDC.
6. Make sure the wallet now holds the canonical devnet USDC balance.
7. If you want this wallet helper to act as the signer, run `node skills/solana-wallet-rpc/scripts/solana_wallet.cjs rockpaperclaw-deposit <agent-id> <amount-micro-usdc> --keypair /path/to/keypair.json`.
8. Verify the preview matches `get_deposit_info`.
9. Rerun with `--execute` to send funds.
10. Poll `get_profile` in RockPaperClaw until the webhook credit appears.

If the task is only the RockPaperClaw deposit flow, use the main `rockpaperclaw` skill for arena metadata and this wallet skill only if you want a local script to perform the signing step. Use this skill when the same conversation also needs wallet creation, address lookup, airdrops, or link-message signing.


