---
name: zyfai
description: Earn yield on any Ethereum wallet on Ethereum Mainnet, Base, and Arbitrum. Use when a user wants passive DeFi yield on their funds. The first deposit assigns a non-custodial pre-deployed subaccount (Safe) with a signed session key to their EOA — no separate deploy or session-key step. Supports USDC, WETH, and EURC, with automated yield optimization and deposit/withdraw anytime.
---

# Zyfai — Yield for Any Wallet

Turn any Ethereum wallet into a yield-generating account.

## What This Does

When a user wants to **earn yield** on their crypto, their first `depositFunds` call associates their EOA with a **pre-deployed Smart Account (Safe)** that already has a signed session key. Funds deposited into this subaccount are automatically optimized across DeFi protocols. The user stays in full control and can withdraw anytime. Their EOA is unchanged.

```
┌─────────────────┐      ┌──────────────────────┐
│   User's EOA    │ ───► │  Zyfai Subaccount    │
│  (their wallet) │      │  (Safe smart wallet) │
│                 │      │                      │
│  Owns & controls│      │  • Auto-rebalancing  │
│                 │      │  • Yield optimization│
│                 │      │  • Non-custodial     │
└─────────────────┘      └──────────────────────┘
```

**Key points:**
- The subaccount is **owned by the user's EOA** — only they can withdraw
- Session keys allow **automated rebalancing** but cannot withdraw to other addresses
- The **first deposit** assigns the Safe live on Ethereum Mainnet, Base, and Arbitrum at once
- **No separate deploy or session-key step** — `depositFunds` is the onboarding call

## The Flow

```
1. CONNECT   →  Authenticate the user's wallet
2. DEPOSIT   →  First deposit assigns pre-deployed Safe + session; starts earning
3. WITHDRAW  →  Pull funds back to wallet (anytime)
```

On the first deposit, Zyfai assigns a pre-deployed Safe with a signed session key to the EOA. The Safe is available immediately on Ethereum Mainnet, Base, and Arbitrum. This does not impact the EOA itself.

## Prerequisites

- **API Key** — Get one programmatically (see below) or manually at [sma.zyf.ai](https://sma.zyf.ai)
- **Wallet Connection** — Either a wallet provider (browser) or secure key management (server)
- **Node.js 18+**

```bash
npm install @zyfai/sdk viem
```

> Latest version: `@zyfai/sdk@0.2.54`

### Programmatic API Key Creation (Agent-Native)

Agents can create their own API key without human intervention. You need the wallet address (public key) of the agent.

```bash
POST https://sma.zyf.ai/api/sdk-api-keys/create
Content-Type: application/json

{
  "clientName": "my-agent",
  "walletAddress": "0x...",
  "email": "agent@example.com"
}
```

**Response:**
```json
{
  "success": true,
  "message": "SDK API key created successfully. Store the apiKey securely - it cannot be retrieved later!",
  "data": {
    "id": "936...",
    "apiKey": "zyfai_361ad41d083c2fe.....",
    "keyPrefix": "zyfai_361ad4",
    "clientName": "my-agent",
    "ownerWalletAddress": "0x..."
  }
}
```

> **Important:** Store the `apiKey` securely — it cannot be retrieved later. The key is linked to the provided wallet address.

## Supported Chains

| Chain            | ID    | Assets            | Min. deposit                          |
|------------------|-------|-------------------|---------------------------------------|
| Ethereum Mainnet | 1     | USDC, WETH, EURC  | $10,000 (WETH: $10,000 worth of WETH) |
| Base             | 8453  | USDC, WETH, EURC  | $100 (WETH: $100 worth of WETH)       |
| Arbitrum         | 42161 | USDC, WETH        | $100 (WETH: $100 worth of WETH)       |

> **EURC** is available on **Ethereum Mainnet and Base only** (not Arbitrum).
>
> **Minimums** apply to the total Safe balance *after* the deposit — top-ups below the minimum are allowed if the Safe already holds enough. WETH minimums use the live ETH/USD price, so the wei threshold moves with the market.

## Important: Always Use EOA Address

When calling SDK methods, **always pass the EOA address** (the user's wallet address) as `userAddress` — never the subaccount/Safe address. The SDK resolves the assigned Safe address for that EOA automatically.

## Wallet Connection Options

The SDK supports multiple ways to connect a wallet. Choose based on your security requirements and deployment context.

### Option 1: Wallet Provider (Recommended for Browser/dApps)

Use an injected wallet provider like MetaMask. The private key never leaves the user's wallet.

```typescript
import { ZyfaiSDK } from "@zyfai/sdk";

const sdk = new ZyfaiSDK({ apiKey: "your-api-key", referralSource: "openclaw-skill" });

// Connect using injected wallet provider (MetaMask, WalletConnect, etc.)
await sdk.connectAccount(window.ethereum, 8453);
```

**Security:** The private key stays in the user's wallet. The SDK only requests signatures when needed.

### Option 2: Viem WalletClient (Recommended for Server Agents)

Use a pre-configured viem WalletClient. This is the recommended approach for server-side agents as it allows integration with secure key management solutions.

```typescript
import { ZyfaiSDK } from "@zyfai/sdk";
import { createWalletClient, http } from "viem";
import { base } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";

// Create wallet client with your preferred key management
// Option A: From environment variable (simple but requires secure env management)
const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);

// Option B: From KMS (AWS, GCP, etc.) - recommended for production
// const account = await getAccountFromKMS();

// Option C: From Wallet-as-a-Service (Turnkey, Privy, etc.)
// const account = await turnkeyClient.getAccount();

const walletClient = createWalletClient({
  account,
  chain: base,
  transport: http(),
});

const sdk = new ZyfaiSDK({ apiKey: "your-api-key", referralSource: "openclaw-skill" });

// Connect using the WalletClient
await sdk.connectAccount(walletClient, 8453);
```

**Security:** The WalletClient abstraction allows you to integrate with secure key management solutions like:
- **AWS KMS** / **GCP Cloud KMS** — Hardware-backed key storage
- **Turnkey** / **Privy** / **Dynamic** — Wallet-as-a-Service providers
- **Hardware wallets** — Via WalletConnect or similar

### Option 3: Private Key String (Development Only)

Direct private key usage.

```typescript
import { ZyfaiSDK } from "@zyfai/sdk";

const sdk = new ZyfaiSDK({ apiKey: "your-api-key", referralSource: "openclaw-skill" });

// WARNING: Only use for development. Never hardcode private keys in production.
await sdk.connectAccount(process.env.PRIVATE_KEY, 8453);
```

**Security Warning:** Raw private keys in environment variables are a security risk. For production autonomous agents, use Option 2 with a proper key management solution.

### Security Comparison

| Method | Security Level | Use Case |
|--------|---------------|----------|
| Wallet Provider | High | Browser dApps, user-facing apps |
| WalletClient + KMS | High | Production server agents |
| WalletClient + WaaS | High | Production server agents |
| Private Key String | Low | Development/testing only |

## Step-by-Step

### 1. Connect to Zyfai

`connectAccount` automatically authenticates the user via SIWE (Sign-In with Ethereum). No extra auth step is needed.

```typescript
import { ZyfaiSDK } from "@zyfai/sdk";
import { createWalletClient, http } from "viem";
import { base } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";

const sdk = new ZyfaiSDK({ apiKey: "your-api-key", referralSource: "openclaw-skill" });

// For browser: use wallet provider
await sdk.connectAccount(window.ethereum, 8453);

// For server: use WalletClient (see Wallet Connection Options above)
const walletClient = createWalletClient({
  account: privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`),
  chain: base,
  transport: http(),
});
await sdk.connectAccount(walletClient, 8453);
```

### 2. Deposit Funds

The first deposit **onboards** the user: it assigns a pre-deployed Safe with a signed session key on Ethereum Mainnet, Base, and Arbitrum — no separate deploy or session-key call. `asset` is **required**.

```typescript
const userAddress = "0x..."; // User's EOA (NOT the subaccount address!)
const chainId = 8453; // Base

// Deposit 10 USDC (6 decimals). Optional strategy applies on first deposit only.
await sdk.depositFunds(userAddress, chainId, "10000000", "USDC", "conservative");

// Deposit 0.5 WETH (18 decimals)
// IMPORTANT: User must have WETH, not ETH. Wrap ETH to WETH first if needed.
await sdk.depositFunds(userAddress, chainId, "500000000000000000", "WETH");

// Deposit 10 EURC (6 decimals) — Ethereum Mainnet / Base only
await sdk.depositFunds(userAddress, chainId, "10000000", "EURC");
```

Funds move from EOA → Subaccount and start earning yield immediately.

**Strategies (first deposit only):**
- `"conservative"` — Stable yield, lower risk (default)
- `"aggressive"` — Higher yield, higher risk

**Minimum portfolio balance** (checked against the total Safe balance *after* the deposit — top-ups below the minimum are allowed if the Safe already holds enough):

| Chain            | USDC     | WETH               | EURC        |
|------------------|----------|--------------------|-------------|
| Base / Arbitrum  | $100     | $100 worth of WETH | €5 (Base only) |
| Ethereum Mainnet | $10,000  | $10,000 worth of WETH | €10,000  |

WETH minimums use the live ETH/USD price from the Data API, so the wei threshold moves with the market.

**Returns:**

```typescript
interface DepositResponse {
  success: boolean;
  txHash: string;
  smartWallet: string;
  amount: string;
}
```

After depositing you can inspect the assigned Safe:

```typescript
const wallet = await sdk.getSmartWalletAddress(userAddress, chainId);
console.log(`Subaccount: ${wallet.address}`);
console.log(`Deployed: ${wallet.isDeployed}`);

const user = await sdk.getUserDetails();
console.log("Session key active:", user.hasActiveSessionKey);
```

#### Log External Deposit (Sponsored / Gasless Transactions)

If you execute the token transfer yourself (e.g. via Privy, Biconomy, or another sponsored/gasless provider), register it with Zyfai's backend using `logDeposit`:

```typescript
// 1. Execute the ERC-20 transfer to the Safe with your own wallet implementation
const txHash = await privyWallet.sendTransaction({ to: safeAddress, data: transferData });

// 2. Log the deposit so Zyfai tracks it and optimizes yield
const result = await sdk.logDeposit(8453, txHash, "100000000"); // 100 USDC
```

### 3. Withdraw Funds

```typescript
// Withdraw all USDC (default)
await sdk.withdrawFunds(userAddress, chainId);

// Partial USDC withdrawal (5 USDC)
await sdk.withdrawFunds(userAddress, chainId, "5000000");

// Withdraw all WETH
await sdk.withdrawFunds(userAddress, chainId, undefined, "WETH");

// Partial WETH withdrawal (0.1 WETH)
await sdk.withdrawFunds(userAddress, chainId, "100000000000000000", "WETH");

// Withdraw all EURC
await sdk.withdrawFunds(userAddress, chainId, undefined, "EURC");
```

Funds always return to the user's EOA (the Safe owner). Withdrawals are processed **asynchronously** by the backend, so `txHash` may not be immediately available — check `result.message` and use `getHistory()` to track it.

### 4. Disconnect

```typescript
await sdk.disconnectAccount();
```

## Complete Example

```typescript
import { ZyfaiSDK } from "@zyfai/sdk";
import { createWalletClient, http } from "viem";
import { base } from "viem/chains";
import { privateKeyToAccount } from "viem/accounts";

async function startEarningYield(userAddress: string) {
  const sdk = new ZyfaiSDK({ apiKey: process.env.ZYFAI_API_KEY! });
  const chainId = 8453; // Base

  // Connect using WalletClient (recommended for server agents)
  const walletClient = createWalletClient({
    account: privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`),
    chain: base,
    transport: http(),
  });
  await sdk.connectAccount(walletClient, chainId);

  // First deposit assigns the pre-deployed Safe + session (pass EOA as userAddress)
  await sdk.depositFunds(userAddress, chainId, "100000000", "USDC", "conservative");
  console.log("Deposited! Now earning yield.");

  await sdk.disconnectAccount();
}

async function withdrawYield(userAddress: string, amount?: string) {
  const sdk = new ZyfaiSDK({ apiKey: process.env.ZYFAI_API_KEY! });
  const chainId = 8453; // Base

  // Connect using WalletClient
  const walletClient = createWalletClient({
    account: privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`),
    chain: base,
    transport: http(),
  });
  await sdk.connectAccount(walletClient, chainId);

  // Withdraw funds (pass EOA as userAddress)
  if (amount) {
    await sdk.withdrawFunds(userAddress, chainId, amount); // partial
    console.log(`Withdrawn ${amount} (6 decimals) to EOA`);
  } else {
    await sdk.withdrawFunds(userAddress, chainId); // full
    console.log("Withdrawn all funds to EOA");
  }

  await sdk.disconnectAccount();
}
```

## API Reference

| Method | Params | Description |
|--------|--------|-------------|
| `connectAccount` | `(walletClientOrProvider, chainId?)` | Authenticate with Zyfai (SIWE) |
| `getSmartWalletAddress` | `(userAddress, chainId)` | Get subaccount address & status |
| `depositFunds` | `(userAddress, chainId, amount, asset, strategy?)` | Deposit USDC/WETH/EURC (first deposit onboards) |
| `logDeposit` | `(chainId, txHash, amount, tokenAddress?)` | Log an externally-executed deposit |
| `withdrawFunds` | `(userAddress, chainId, amount?, assetType?)` | Withdraw USDC/WETH/EURC |
| `getPositions` | `(userAddress, chainId?)` | Get active DeFi positions |
| `getPortfolio` | `(userAddress)` | Portfolio with net-of-fee balances |
| `getAvailableProtocols` | `(chainId)` | Get available protocols & pools |
| `getAPYPerStrategy` | `(crossChain?, days?, strategy?, chainId?, tokenSymbol?)` | Get APY by strategy and token |
| `getUserDetails` | `(asset?)` | Get user details for USDC, WETH, or EURC |
| `getOnchainEarnings` | `(walletAddress)` | Get earnings data by token |
| `updateUserProfile` | `(params)` | Update strategy, protocols, splitting per asset |
| `pauseAgent` / `resumeAgent` | `()` | Pause / resume automated operations |
| `registerAgentOnIdentityRegistry` | `(smartWallet, chainId)` | Register agent on ERC-8004 Identity Registry |
| `disconnectAccount` | `()` | End session |

**Note:** All methods that take `userAddress` expect the **EOA address**, not the subaccount/Safe address.

> `deploySafe(userAddress, chainId, strategy?)` and `createSessionKey(userAddress, chainId)` remain available for legacy flows but are **deprecated** — prefer `depositFunds()` for onboarding.

## Data Methods

### getPositions

Get all active DeFi positions for a user across protocols. Optionally filter by chain.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| userAddress | string | Yes | User's EOA address |
| chainId | SupportedChainId | No | Optional: filter by specific chain ID |

```typescript
// Get all positions across all chains
const positions = await sdk.getPositions("0xUser...");

// Get positions on Arbitrum only
const arbPositions = await sdk.getPositions("0xUser...", 42161);

positions.positions.forEach((bundle) => {
  console.log(`Chain: ${bundle.chain}, Strategy: ${bundle.strategy}`);
  bundle.positions.forEach((slot) => {
    console.log(`Token: ${slot.token_symbol}, Pool: ${slot.pool}`);
    console.log(`Underlying Amount: ${slot.underlyingAmount}`);
  });
});
```

### getPortfolio

Returns the full wallet portfolio plus **net-of-pending-fee** fields. Pending fee is `current` onchain earnings × 10%; gross balances are unchanged.

```typescript
const { portfolio } = await sdk.getPortfolio(userAddress);

// Gross vs net (after pending Zyfi fee)
console.log(portfolio.portfolioByAssetType?.usdc?.balance);
console.log(portfolio.portfolioByAssetType?.usdc?.balanceWithFee);

portfolio.positions?.forEach((slot) => {
  console.log(slot.pool, slot.underlyingAmount, slot.underlyingAmountWithFee);
  console.log(slot.pool_apy, slot.pool_apy_withFee); // pool_apy_withFee = pool_apy × 0.9
});
```

### getAvailableProtocols

Get available DeFi protocols and pools for a specific chain with APY data.

```typescript
const protocols = await sdk.getAvailableProtocols(42161); // Arbitrum

protocols.protocols.forEach((protocol) => {
  console.log(`${protocol.name} (ID: ${protocol.id})`);
  protocol.pools?.forEach((pool) => {
    console.log(`  Pool: ${pool.name} - APY: ${pool.apy || "N/A"}%`);
  });
});
```

Returns:
```typescript
interface ProtocolsResponse {
  success: boolean;
  chainId: SupportedChainId;
  protocols: Protocol[];
}
```

### getUserDetails

Get the authenticated user's details including smart wallet, chains, protocols, and settings. Requires SIWE authentication (done automatically by `connectAccount`). Accepts an optional `asset` (`"USDC"` default, `"WETH"`, or `"EURC"`) — each asset has its own configuration.

```typescript
await sdk.connectAccount(walletClient, chainId);

const user = await sdk.getUserDetails();          // USDC settings (default)
const wethUser = await sdk.getUserDetails("WETH"); // WETH settings

console.log("Smart Wallet:", user.smartWallet);
console.log("Chains:", user.chains);
console.log("Strategy:", user.strategy);
console.log("Has Active Session:", user.hasActiveSessionKey);
```

Returns `UpdateUserProfileResponse` (same shape as `updateUserProfile`).

### updateUserProfile

Update the authenticated user's profile settings including strategy, protocols, splitting, and cross-chain options. Requires SIWE authentication.

**Parameters:**

```typescript
interface UpdateUserProfileRequest {
  /** Investment strategy: "conservative" or "aggressive" */
  strategy?: string;
  /** Array of protocol IDs to use */
  protocols?: string[];
  /** Enable auto-selection of protocols */
  autoSelectProtocols?: boolean;
  /** Enable omni-account for cross-chain operations */
  omniAccount?: boolean;
  /** Array of chain IDs to operate on */
  chains?: number[];
  /** Enable automatic compounding (default: true) */
  autocompounding?: boolean;
  /** Custom name for your agent */
  agentName?: string;
  /** Enable cross-chain strategy execution */
  crosschainStrategy?: boolean;
  /** Enable position splitting across multiple protocols */
  splitting?: boolean;
  /** Minimum number of splits (1-4) */
  minSplits?: number;
  /** Asset to update settings for: "USDC" (default), "WETH", or "EURC" */
  asset?: "USDC" | "WETH" | "EURC";
}
```

**Note on `asset`:** Each asset has its own configuration. Use `asset: "WETH"` or `asset: "EURC"` to update that asset separately from USDC.

**Returns:**

```typescript
interface UpdateUserProfileResponse {
  success: boolean;
  smartWallet?: string;
  chains?: number[];
  strategy?: string;
  protocols?: string[];
  autoSelectProtocols?: boolean;
  omniAccount?: boolean;
  autocompounding?: boolean;
  agentName?: string;
  crosschainStrategy?: boolean;
  executorProxy?: boolean;
  hasActiveSessionKey?: boolean;
  splitting?: boolean;
  minSplits?: number;
  customization?: Record<string, any>;
  asset?: "USDC" | "WETH" | "EURC";
}
```

**Examples:**

```typescript
// Update strategy from conservative to aggressive
await sdk.updateUserProfile({ strategy: "aggressive" });

// Configure specific protocols
const protocolsResponse = await sdk.getAvailableProtocols(8453);
const selectedProtocols = protocolsResponse.protocols
  .filter(p => ["Aave", "Compound", "Moonwell"].includes(p.name))
  .map(p => p.id);
await sdk.updateUserProfile({ protocols: selectedProtocols });

// Enable position splitting (distribute across multiple protocols)
await sdk.updateUserProfile({ splitting: true, minSplits: 3 });
```

> **Cross-chain strategies:** Only enable cross-chain when the user **explicitly requests** it. For cross-chain to work, **both** `crosschainStrategy` and `omniAccount` must be `true`. Never enable cross-chain settings by default.

```typescript
// Enable cross-chain ONLY when explicitly requested by the user
await sdk.updateUserProfile({ crosschainStrategy: true, omniAccount: true });
```

**Notes:**
- **Strategy:** Can be changed anytime. Subsequent rebalancing uses the new active strategy.
- **Protocols:** Use `getAvailableProtocols(chainId)` to get valid protocol IDs before updating.
- **Smart Splitting (minSplits = 1):** Default mode. Funds are distributed across multiple DeFi pools only when beneficial, based on current market conditions.
- **Forced Splitting (minSplits > 1):** Funds are always distributed across at least that many pools (up to 4) for risk diversification.
- **Cross-chain:** Requires **both** `crosschainStrategy: true` AND `omniAccount: true`.
- **Auto-compounding:** Enabled by default — yields are reinvested automatically.
- Smart wallet address, chains, and `executorProxy` cannot be updated via this method.

### pauseAgent / resumeAgent

Pause the agent by clearing all protocols (stops automated operations) across USDC, WETH, and EURC. Resume to restart.

```typescript
await sdk.pauseAgent();

// Verify
const details = await sdk.getUserDetails();
console.log("Active protocols:", details.protocols?.length); // 0 when paused

await sdk.resumeAgent();
```

### getAPYPerStrategy

Get global APY by strategy type, time period, chain, and token. Use this to compare expected returns before depositing. Prefer `average_apy_withFee` / `average_apy_with_rzfi_withFee` (gross × 0.9) for user-facing display (renamed from `*_with_fee` in `@zyfai/sdk` 0.2.51).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| crossChain | boolean | No | If `true`, cross-chain strategies; else single-chain (default: `false`) |
| days | number | No | Period: `7`, `15`, `30`, `60` (default: `7`) |
| strategy | string | No | `"conservative"` (default) or `"aggressive"` |
| chainId | number | No | Filter by chain ID (e.g. `8453`) |
| tokenSymbol | string | No | Filter by token: `"USDC"`, `"WETH"`, or `"EURC"` |

```typescript
// 7-day APY for USDC conservative
const usdcApy = await sdk.getAPYPerStrategy(false, 7, "conservative", undefined, "USDC");

// Compare strategies (30d)
const conservative = await sdk.getAPYPerStrategy(false, 30, "conservative");
const aggressive = await sdk.getAPYPerStrategy(false, 30, "aggressive");
console.log(`Conservative 30d APY: ${conservative.data[0]?.average_apy_withFee}%`);
console.log(`Aggressive 30d APY: ${aggressive.data[0]?.average_apy_withFee}%`);
```

Returns:
```typescript
interface APYPerStrategyResponse {
  success: boolean;
  count: number;
  data: APYPerStrategy[];
}

interface APYPerStrategy {
  id: string;
  timestamp: string;
  amount: number;
  fee_threshold: number;
  days: number;
  chain_id: number;
  is_cross_chain: boolean;
  average_apy: number;
  average_apy_with_rzfi: number;
  total_rebalances: number;
  created_at: string;
  strategy: string;
  token_symbol?: string;
  average_apy_withFee: number;
  average_apy_with_rzfi_withFee: number;
  events_average_apy?: Record<string, number>;
  events_average_apy_withFee?: Record<string, number>;
  events_average_apy_with_rzfi_withFee?: Record<string, number>;
}
```

### getOnchainEarnings

Get onchain earnings for a wallet with per-token totals (multi-asset).

```typescript
const earnings = await sdk.getOnchainEarnings(smartWalletAddress);

console.log("Total by token:", earnings.data.totalEarningsByToken);
// { "USDC": 150.50, "WETH": 0.05 }

// Net totals (after fee): lifetime + unrealized + current × 0.9
console.log("Net by token:", earnings.data.totalEarningsByTokenWithFee);
```

Returns:
```typescript
type TokenEarnings = Record<string, number>;                  // { "USDC": 100.5, "WETH": 0.025 }
type ChainTokenEarnings = Record<string, TokenEarnings>;      // { "8453": { "USDC": 100.5 } }

interface OnchainEarnings {
  walletAddress: string;
  totalEarningsByToken: TokenEarnings;
  totalEarningsByChain?: ChainTokenEarnings;
  totalEarningsByTokenWithFee: TokenEarnings; // lifetime + unrealized + current × 0.9
  totalEarningsByChainWithFee?: ChainTokenEarnings;
  lastCheckTimestamp?: string;
  lastLogDate?: Record<string, string | null>;
}

interface OnchainEarningsResponse {
  success: boolean;
  data: OnchainEarnings;
}
```

> **Fee formula:** pending fee = `current × 0.1` (unrealised yield only). Do **not** apply `× 0.9` to lifetime or unrealized earnings.

### registerAgentOnIdentityRegistry (ERC-8004)

Register your Zyfai deployed agent on the Identity Registry following the ERC-8004 standard (used for OpenClaw agent registration). The method fetches a `tokenUri` with the agent's metadata (stored on IPFS), then registers it on-chain.

**Supported Chains:** Base (8453), Arbitrum (42161)

```typescript
const sdk = new ZyfaiSDK({ apiKey: "your-api-key" });
await sdk.connectAccount(walletClient, 8453);

const walletInfo = await sdk.getSmartWalletAddress(userAddress, 8453);
const result = await sdk.registerAgentOnIdentityRegistry(walletInfo.address, 8453);

console.log("Tx Hash:", result.txHash);
console.log("Chain ID:", result.chainId);
console.log("Smart Wallet:", result.smartWallet);
```

Returns:
```typescript
interface RegisterAgentResponse {
  success: boolean;
  txHash: string;
  chainId: number;
  smartWallet: string;
}
```

## Security

- **Non-custodial** — User's EOA owns the subaccount
- **Session keys are limited** — Can rebalance, cannot withdraw elsewhere
- **Deterministic** — Same EOA = same subaccount address across Mainnet, Base, and Arbitrum
- **Flexible key management** — Use wallet providers, WalletClients, or KMS integrations

### Key Management Best Practices

For **production autonomous agents**, we recommend:

1. **Use a WalletClient** with a secure key source (not raw private keys)
2. **Integrate with KMS** (AWS KMS, GCP Cloud KMS) for hardware-backed key storage
3. **Consider Wallet-as-a-Service** providers like Turnkey, Privy, or Dynamic
4. **Never hardcode** private keys in source code
5. **Rotate keys** periodically and implement key revocation procedures

## Troubleshooting

### "No account connected" error

Call `connectAccount()` before methods that require **signing or SIWE authentication** (e.g. `depositFunds`, `withdrawFunds`, `updateUserProfile`). Read-only data methods (e.g. `getPositions`, `getHistory`, `getOnchainEarnings`) do not require a connected wallet.

### "Safe not available" / deposit failed on first use

The Safe is assigned on the first successful `depositFunds` call. If deposit fails:
1. Confirm the EOA is connected via `connectAccount`
2. Confirm the chain and asset are supported (EURC: Mainnet/Base only)
3. Retry `depositFunds` — do **not** call any separate deploy or session-key method

### Subaccount address mismatch across chains

After the first deposit, the assigned Safe address should be **identical** across Mainnet, Base, and Arbitrum for the same EOA:

```typescript
const baseWallet = await sdk.getSmartWalletAddress(userAddress, 8453);
const arbWallet = await sdk.getSmartWalletAddress(userAddress, 42161);

if (baseWallet.address !== arbWallet.address) {
  console.error("Address mismatch! Contact support.");
}
```

If addresses don't match, contact support on Telegram: [@paul_zyfai](https://t.me/paul_zyfai)

### "Invalid signature" error

This typically means:
- The wallet/signer doesn't match the EOA you're passing
- The Safe address on-chain doesn't match what the SDK expects

Verify you're using the correct wallet for the EOA.

### Withdrawal transaction hash not available

Withdrawals are processed asynchronously by the backend. If `withdrawFunds` returns without a `txHash`:
1. Check the `message` field for status
2. Use `getHistory()` to track when the withdrawal transaction is processed

## Resources

- **Get API Key:** [sma.zyf.ai](https://sma.zyf.ai) or programmatically via `POST /api/sdk-api-keys/create`
- **Docs:** [docs.zyf.ai](https://docs.zyf.ai)
- **Demo:** [github.com/ondefy/zyfai-sdk-demo](https://github.com/ondefy/zyfai-sdk-demo)
- **MCP Server:** [mcp.zyf.ai](https://mcp.zyf.ai/mcp) — Use with Claude or other MCP-compatible agents
- **Agent Registration:** [zyf.ai/.well-known/agent-registration.json](https://www.zyf.ai/.well-known/agent-registration.json)

## License

MIT License

Copyright (c) 2024 Zyfai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
