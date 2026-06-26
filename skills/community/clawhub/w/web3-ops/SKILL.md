---
name: web3-ops
description: Perform EVM Web3 on-chain operations: check addresses, scan portfolios, transfer assets, swap/bridge tokens, mint NFTs, custom raw tx, PnL tracking, Cutloss/Takeprofit monitor, RSI/EMA trading signals, GoPlus contract security audits, whale tracking, anti-MEV route routing, and wallet creation.

env:
  - PRIVATE_KEY

requirements:
  bins:
    - node
---
# Secure AI-Native Web3 Operational Skill

This skill allows the OpenClaw AI agent to interface with EVM blockchains (Ethereum, Arbitrum, Base, Optimism, Polygon, BNB Chain, Sonic, Sepolia, etc.) using a local Node.js CLI utility under a strict Human-in-the-Loop safety model.


## Global Options

These flags can be appended to any command:
*   `--json`: Silences human logs and outputs strictly JSON to `stdout` (highly recommended for AI agent parsing).
*   `--rpc <url>`: Overrides default node RPC with a custom RPC endpoint (useful for testnets or private nodes).
*   `--simulate`: Simulates the transaction (dry run) using gas estimation and call simulation. Prevents sending failing transactions and calculates gas fees.

## CLI Commands & Arguments

All commands are run using Node.js inside the skill directory:
`node skills/web3-ops/index.js <command> [arguments]`

### 1. Get Wallet Address
Get your configured wallet address.
*   **Usage:** `node skills/web3-ops/index.js address [--json]`

### 2. Check Specific Balance
Check native coin (ETH, MATIC, BNB, S) or a specific ERC-20 token balance using symbol or contract address.
*   **Native Coin:** `node skills/web3-ops/index.js balance --chain <chain> [--json]`
*   **ERC-20 Token:** `node skills/web3-ops/index.js balance --chain <chain> --token <symbol_or_address> [--json]`
*   *Example:* `node skills/web3-ops/index.js balance --chain base --token AERO`

### 3. Scan Portfolio (New)
Scan and list all tokens with a positive balance in your wallet. If no chain is specified, it will scan all supported networks in parallel. Automatically detects "degen/micin" tokens using block explorer transaction history.
*   **Usage (All Chains):** `node skills/web3-ops/index.js portfolio [--json]`
*   **Usage (Single Chain):** `node skills/web3-ops/index.js portfolio --chain <chain> [--json]`

### 4. Transfer Coins or Tokens
Send native coins or ERC-20 tokens to another address.
*   **Native Coin:** `node skills/web3-ops/index.js transfer --chain <chain> --to <recipient_address> --amount <amount> [--json] [--simulate]`
*   **ERC-20 Token:** `node skills/web3-ops/index.js transfer --chain <chain> --to <recipient_address> --amount <amount> --token <symbol_or_address> [--json] [--simulate]`

### 5. Swap Tokens (Same-Chain)
Swap tokens on the same blockchain network. Supports auto-routing and manual routers.
*   **Auto Mode (Li.Fi Aggregator):**
    `node skills/web3-ops/index.js swap --chain <chain> --fromToken <symbol_or_address> --toToken <symbol_or_address> --amount <amount> --mode auto [--json] [--simulate]`
*   **Manual Mode (Uniswap/PancakeSwap/Relay/Li.Fi):**
    `node skills/web3-ops/index.js swap --chain <chain> --fromToken <symbol_or_address> --toToken <symbol_or_address> --amount <amount> --mode manual --provider <lifi|relay|uniswap|pancakeswap> [--json] [--simulate]`
*   **Slippage Tolerance:** Add `--slippage <percent>` (default is 0.5)

### 6. Bridge Tokens (Cross-Chain)
Bridge and swap assets from one blockchain to another.
*   **Auto Mode (Li.Fi Aggregator):**
    `node skills/web3-ops/index.js bridge --fromChain <source_chain> --toChain <target_chain> --fromToken <symbol_or_address> --toToken <symbol_or_address> --amount <amount> --mode auto [--json] [--simulate]`
*   **Manual Mode (Relay/Li.Fi):**
    `node skills/web3-ops/index.js bridge --fromChain <source_chain> --toChain <target_chain> --fromToken <symbol_or_address> --toToken <symbol_or_address> --amount <amount> --mode manual --provider <lifi|relay> [--json] [--simulate]`

### 7. Mint NFT
Mint or claim NFTs on a smart contract.
*   **Usage:** `node skills/web3-ops/index.js mint --chain <chain> --contract <nft_contract_address_or_url> [--function <signature>] [--args <json_array_arguments>] [--value <native_fee_to_send>] [--json] [--simulate]`
*   *Note:* `--function`, `--args`, and `--value` are optional. If omitted, the skill will fetch the verified contract ABI from the explorer, auto-detect the mint function (e.g., `mint`, `claim`), and infer the arguments automatically.
*   *Example:* `node skills/web3-ops/index.js mint --chain base --contract 0x123...`


### 8. Custom Transaction (Raw Transaction)
Broadcast a custom raw transaction with hex data payload.
*   **Usage:** `node skills/web3-ops/index.js custom --chain <chain> --to <target_address> --data <hex_calldata> --value <native_amount> [--json] [--simulate]`

### 9. Profit & Loss Tracker (PnL)
Calculate the average buy price and current profit/loss of a token.
*   **Usage:** `node skills/web3-ops/index.js pnl --chain <chain> --token <symbol_or_address> [--buyPrice <manual_usd_price>] [--json]`

### 10. Cutloss & Takeprofit Monitor
Monitor token price in real-time and execute a pre-authorized safety swap to USDC if limits are reached.
*   **Usage:** `node skills/web3-ops/index.js monitor --chain <chain> --token <symbol_or_address> --amount <sell_amount> --cutloss <percent_or_price> --takeprofit <percent_or_price> [--max-checks <count>] [--interval <seconds>] [--alert] [--json]`

### 11. Trading Signals
Fetch daily candles and analyze RSI (14) & EMA (20/50) indicators to generate Buy/Sell recommendations.
*   **Usage:** `node skills/web3-ops/index.js signal --chain <chain> --token <symbol_or_address> [--alert] [--json]`

### 12. Smart Contract Auditor
Perform a GoPlus security audit to detect honey pots, taxes, and code privileges.
*   **Usage:** `node skills/web3-ops/index.js analyze --chain <chain> --token <symbol_or_address> [--json]`

### 13. Whale Tracker
Scan block explorer transfers for large transaction amounts exceeding a threshold.
*   **Usage:** `node skills/web3-ops/index.js whales --chain <chain> --token <symbol_or_address> [--min-usd <value>] [--alert] [--json]`

### 14. Create EVM Wallet
Generate a random EVM wallet and automatically write its credentials to `.env`.
*   **Usage:** `node skills/web3-ops/index.js create-wallet [--force] [--json]`
*   *Security Warning:* Run this command only locally in the CLI terminal. Do not let AI agents trigger it remotely over chat interfaces.

---


## Agent Behavior & Telegram Prompt Guidelines

When interacting with the user regarding blockchain transactions:
1.  **Translate Intent to CLI:** Convert the user's natural language requests (e.g., "Check my Base portfolio", "Swap 10 USDC to ETH on Base", "Send 0.01 Sepolia ETH to 0x...") into the corresponding CLI command. Always append `--json` for programmatic parsing.
2.  **No Raw JSON Outputs (CRITICAL):** Never output raw JSON (such as `{ "success": true, ... }`) directly to the user. Always parse the command's JSON output and translate it into a natural, friendly, and engaging human-readable response.
3.  **Utilize Simulation Mode:** If the user is unsure, asks "will this transaction work?", or is making a high-value transfer, suggest simulating it first using `--simulate`.
4.  **Display Copyable Addresses (CAs):** When printing token balances, portfolios, or transaction confirmations, format all contract addresses (CA) inside Telegram monospace code blocks (e.g. `` `0x940181a94A35A4569E4529A3CDfB74e38FD98631` ``) so users can tap to copy them instantly.
5.  **Support Testnets & Custom RPCs:** If the user specifies a testnet (e.g., Sepolia) or requests a private RPC, append the `--rpc` flag to the command.
6.  **Explorer Links:** Always extract the `explorer` link from the output JSON and present it to the user so they can track block confirmation status.
7.  **Security Notice:** Never request seed phrases, mnemonics, or private keys. The wallet configuration is loaded securely from the local server's `.env` file.
8.  **Casual & Friendly Tone:** Explain transaction results, balances, or confirmations in a natural, casual, and friendly everyday chat style (e.g., like a helpful Web3 degen companion). Avoid robotic or overly dry responses, but always keep technical fields (like contract addresses and transaction hashes) accurate and formatted for easy copying.
9.  **Format PnL Reports:** Summarize PnL reports into friendly bullets. E.g., mention the current balance, average buy price, current market price, and the overall gain/loss in USD and ROI percentage.
10. **Format Security Audits:** Highlight whether the contract is safe or a honeypot, buying/selling taxes, and list any risk findings with appropriate alert emojis (e.g., 🚨, ⚠️, ℹ️).
11. **Format Trading Signals:** Present the overall signal recommendation (e.g., "STRONG BUY" in bold) along with the RSI (14) value and the EMA trend.
12. **Format Whale Alerts:** Summarize detected whale transactions by showing the USD value, the amount of tokens, sender/receiver addresses, and a link to the transaction hash.
13. **NFT Mint Autodetection:** If the user asks to mint an NFT by providing a contract address or marketplace/explorer link without specifying the function signature or arguments, run the `mint` command and omit the `--function`, `--args`, and `--value` parameters. The skill will automatically fetch the verified contract ABI, detect the mint function, and infer the arguments. Always suggest simulation using `--simulate` first to verify correctness.

