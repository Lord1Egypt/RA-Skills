# 🌾 SelfPaidPal (YieldFarmSecurepay)

**Official Brand**: **SelfPaidPal** • Autonomous zero-net-cost payments and treasury yield recovery on Base Mainnet (Chain ID 8453).

Send USDC to any recipient while recovering **100% of the principal + developer fee** automatically through collateral yield farming on **Aave V3** and **Morpho Vaults**.

---

## 🚀 Key Features

* **100% Capital Recovery**: Principal spent on payments and developer maintenance fees is fully recouped through automated DeFi yield.
* **Zero Lockup Guarantee**: Deposited collateral produces yield-bearing tokens (`aBasUSDC` / `maUSDC`) that remain 100% owned by the payer wallet with **zero time lock**. Redeem anytime with 1 single transaction.
* **Pure M2M Architecture**: Generates clean, ready-to-sign EVM transactions, Safe Transaction Builder JSON for DAO treasuries, and EIP-5792 atomic batch calls.
* **Dynamic Yield Optimizer**: Automatically selects the highest yielding protocol between Aave V3 and Morpho.
* **Treasury & Recovery Tracker**: Inspect liquid USDC balances, active yield collateral, and accrued yield interest in real time.
* **Pre-Signing Validation Layer (T09)**: Built-in local validation (`validate.js`) guarantees calldata integrity, enforces Base Chain ID 8453, and protects against position redirection.
* **Transparent Monetization**: Built-in 0.5% developer fee (min 0.1 USDC, max 50 USDC), completely recovered by the yield.
* **Non-Custodial**: No private keys ever stored or requested.

---

## 🌐 Hosted Machine-to-Machine API (Base Mainnet)

* **Oracle Rates**: `GET https://selfpaid.cryptofolio.it/api/v1/payment/rates`
* **Calculate Quote**: `GET https://selfpaid.cryptofolio.it/api/v1/payment/quote?amount=25`
* **Build Payment Transactions**: `POST https://selfpaid.cryptofolio.it/api/v1/payment/build`
* **Treasury & Yield Status**: `GET https://selfpaid.cryptofolio.it/api/v1/payment/treasury?wallet=0xYourWallet`
* **Build Collateral Withdrawal**: `POST https://selfpaid.cryptofolio.it/api/v1/payment/withdraw`

For detailed agent integration, OpenClaw T09 validation protocols, and mathematical models, see `SKILL.md`.

---

## 🤖 Multi-Channel Agentic Ecosystem

SelfPaidPal is also available across all major AI agent frameworks:
* **Model Context Protocol (MCP)**: `npx -y selfpaid-mcp` (Universal for Claude Desktop & Cursor)
* **Coinbase AgentKit**: `npm i @altoninelli/agentkit-selfpaid`
* **ElizaOS Plugin**: `npm i @altoninelli/eliza-plugin-selfpaid`
* **Live dApp & Dashboard**: [https://selfpaid.cryptofolio.it](https://selfpaid.cryptofolio.it)

---

## ⚠️ Risk Disclosure

DeFi protocol deposits carry inherent smart contract, oracle, and liquidity risks. Transactions on Base Mainnet are irreversible. Principal recovery estimates are dynamic and fluctuate based on market lending yields on Aave V3 and Morpho.
