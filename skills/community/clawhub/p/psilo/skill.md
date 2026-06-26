---
name: psilo
version: 1.0.1
description: >
  Use this skill when an agent needs to: (1) create on-chain escrow contracts via EscrowFactory,
  (2) release escrowed funds via arbiter-signed transactions, and (3) interact with the Pakt Escrow
  service using the @pakt/psilo SDK. Authentication and wallet: choose SIWA or Evalanche.
---

# Pakt Escrow API Skill

This skill provides **on-chain escrow contract management** for AI agents. Use the **@pakt/psilo** SDK for all escrow operations: create contracts, query status, prepare seller/buyer transactions, and trigger release. Release requires the seller and buyer to each sign an on-chain confirmation transaction, after which the system arbiter executes the final release.

**Primary interface:** Install `@pakt/psilo` and use `PsiloSDK.init({ baseUrl })`. All operations go through `sdk.escrow`: `getChains()`, `getAssets(chainId)`, `create(dto)`, `getStatus(chainId, escrowAddress)`, `updateStatus(escrowAddress, { chainId, address })`, `release(escrowAddress, { recipient? })`.
---

## Authentication Flow (Read this first)

Authenticate before calling protected escrow endpoints.

### Public auth and registration endpoints

- `POST /api/auth/register`
- `POST /api/auth/nonce`
- `POST /api/auth/verify`

All other endpoints require `Authorization: Bearer <accessToken>`.

### SIWA auth flow

1. **Broadcast on-chain register tx** from the agent wallet and obtain `agentId` from the `Registered` event.
2. **Register/update on platform** with `POST /api/auth/register` so SIWA sign-in can issue JWTs.
3. **Request nonce** with `POST /api/auth/nonce` using `{ address, agentId, agentRegistry? }`.
4. **Sign SIWA message** with the agent wallet/keyring.
5. **Verify signature** with `POST /api/auth/verify` using `{ message, signature }`.
6. **Use returned `accessToken`** in `Authorization: Bearer <token>` for protected endpoints.

If `401` is returned, request a new nonce and verify again to refresh authentication.

---

## Security and Transparency Checklist

This section is intentionally explicit to reduce security-review ambiguity for skill registries and automated scanners.

### Capability scope (what this skill is allowed to do)

- Create escrow contracts through `@pakt/psilo` / escrow API
- Read escrow-related metadata (chains, assets, status)
- Prepare seller/buyer release-readiness transactions
- Trigger release endpoint only when policy allows (arbiter/system flow)

### Out-of-scope behavior (what this skill must NOT do)

- Must not exfiltrate secrets, mnemonics, or private keys
- Must not run unrelated shell commands, package installs, or background services
- Must not access unrelated files outside the escrow workflow
- Must not perform autonomous fund transfers outside explicit escrow operations requested by the user

### Required credentials and env vars

Minimum expected inputs:

- `ESCROW_API_URL` (or use default in docs examples)
- `Authorization: Bearer <accessToken>` for protected endpoints
- Optional system-side release secret (`X-Release-Secret`) for release endpoints

For Hugging Face / model / unrelated infrastructure keys: out of scope for this skill.

### Data handling and storage

- This skill is documentation-driven and does not require writing local files by default
- If an integrator chooses to persist logs/receipts, they should avoid storing raw private keys and redact bearer tokens
- Never commit credentials, JWTs, release secrets, or wallet secrets into repository files

### Network access

Expected network destinations only:

- Escrow API base URL (for example `https://escrowapi.psiloai.com`)
- Chain RPC endpoints required to submit on-chain transactions

Any additional destination should be treated as suspicious and reviewed before use.

### Autonomous-use safeguards

If this skill is used by an autonomous agent:

- Require explicit user confirmation before create/release actions
- Enforce allowlists for chain IDs and token contracts
- Apply spend limits and per-transaction policy checks
- Prefer testnet wallets for validation before production funds

---

## IMPORTANT: Prerequisites

**Before using this skill, you MUST:**

1. **Ensure the agent has a wallet and (optionally) auth for agent endpoints** — Choose one of the following.

   ### Option A: SIWA (Sign-In With Agent)

   Use [SIWA](https://siwa.id/skill.md) when you need **agent-only API endpoints** (e.g. `POST /api/escrows/agent`) and ERC-8128 receipt-based authentication.

   - **If the agent does not yet have a wallet:** Follow the [SIWA skill documentation](https://siwa.id/skill.md) to:
     - Install and configure SIWA using the `@buildersgarden/siwa` package
     - Choose and set up an agent-side wallet (e.g. [Private Key](https://siwa.id/skills/private-key/skill.md), [Keyring Proxy](https://siwa.id/skills/keyring-proxy/skill.md), or another [wallet skill](https://siwa.id/skill.md#skills) listed there)
     - **Register the agent on the ERC-8004 Identity Registry** (see [siwa.id/skill.md](https://siwa.id/skill.md) and the `@buildersgarden/siwa/registry` module)
     - Authenticate via SIWA to obtain a receipt for agent endpoints
   - **If the agent already has a wallet:** Ensure it is registered on ERC-8004 and that you can authenticate via SIWA to get a receipt when calling agent-only endpoints.

   ### Option B: Evalanche

   Use [Evalanche](https://www.npmjs.com/package/evalanche) when you want a **multi-EVM agent wallet** with minimal setup: non-custodial keys, many chains, and optional onchain identity (ERC-8004). No browser or popups.

   ```bash
   npm install evalanche
   ```

   ```typescript
   import { Evalanche } from 'evalanche';

   // Non-custodial: first run creates wallet at ~/.evalanche/keys/agent.json
   const { agent } = await Evalanche.boot({ network: 'base' });
   console.log(agent.address);  // use as buyer/seller in sdk.escrow.create()
   ```

   - Use `agent.address` as buyer or seller in `sdk.escrow.create()`. Sign and send deposit/update transactions with the same agent (e.g. via Evalanche’s signing APIs).
   - For **agent-only endpoints** that require a receipt (e.g. `POST /api/escrows/agent`), use SIWA (Option A) for that flow; Evalanche provides the wallet and chain operations, not the ERC-8128 receipt.

   **Summary:** Use **SIWA** for full agent-auth (receipt + agent-only endpoints). Use **Evalanche** for a simple multi-EVM wallet and standard `sdk.escrow.create()` with your agent address.

2. **Install the Psilo SDK** — Primary interface for escrow operations:
   ```bash
   npm install @pakt/psilo
   ```

3. **Know the API base URL** — The escrow API endpoint (e.g., `https://escrowapi.psiloai.com`)

---

## What You Can Do (SDK)

Use **@pakt/psilo** for all escrow operations. Initialize once, then call methods on `sdk.escrow`:

| Operation | SDK method | Description |
|-----------|------------|-------------|
| **Get chains** | `sdk.escrow.getChains()` | List supported escrow chains |
| **Get assets** | `sdk.escrow.getAssets(chainId)` | List supported assets for a chain |
| **Get escrow status** | `sdk.escrow.getStatus(chainId, escrowAddress)` | On-chain status: buyer, seller, arbiter, deposited, released, readyForRelease, buyerReleaseReady, balance |
| **Create escrow** | `sdk.escrow.create(dto)` | Deploy EscrowWallet via server-signed EscrowFactory; returns escrow address and deposit/approve payloads |
| **Prepare update (seller/buyer)** | `sdk.escrow.updateStatus(escrowAddress, { chainId, address })` | Get tx for markReady (seller) or markBuyerEscrowReleaseReady (buyer) |
| **Release escrow** | `sdk.escrow.release(escrowAddress, { recipient? })` | System-only; arbiter signs release (seller + buyer must have marked ready) |

---

## Using the Psilo SDK

### Installation and initialization

```bash
npm install @pakt/psilo
```

```typescript
import { PsiloSDK } from "@pakt/psilo";
const ESCROW_API_URL = process.env.ESCROW_API_URL || "https://escrowapi.psiloai.com";

const sdk = await PsiloSDK.init({
  baseUrl: ESCROW_API_URL
});
```

All examples below use `sdk.escrow`. Responses follow the standard envelope `{ status, message, data }`; use `result.data` for the payload. On failure the SDK throws; use try/catch for error handling.

### Get supported chains and assets

```typescript
const { data } = await sdk.escrow.getChains();
// data.chains: Array<{ chainId, name, network, nativeCurrency }>

const { data: assetsData } = await sdk.escrow.getAssets("43113");
// assetsData.assets: Array<{ address, symbol, name, decimals, isNative }>
```

### Create escrow

```typescript
import type { CreateEscrowDto } from "@pakt/psilo";

const { data } = await sdk.escrow.create({
  chainId: "43113",
  buyer: "0xBuyerAddress...",
  seller: "0xSellerAddress...",
  title: "Payment for development work",
  description: "Full-stack development services",  // optional
  amount: "1000",
  asset: "0xUSDCTokenAddress...",  // token contract; server may use ESCROW_ASSET_ADDRESS
  // expiration: "1740000000",   // optional unix timestamp
  // releaseType: "0",           // optional
} satisfies CreateEscrowDto);

const { onChain, buyerWallet, sellerWallet, arbiterWallet } = data;
// onChain.escrowAddress, onChain.txHash, onChain.deposit, onChain.approve (or null for native)
```

### Get escrow status

```typescript
const { data } = await sdk.escrow.getStatus("43113", "0xEscrowAddress...");
// data: { chainId, escrow, buyer, seller, arbiter, deposited, released, readyForRelease, buyerReleaseReady, balance }
```

### Mark ready (seller and buyer)

```typescript
// Seller or buyer: pass their address; server returns the correct tx (markReady vs markBuyerEscrowReleaseReady)
const { data: tx } = await sdk.escrow.updateStatus("0xEscrowAddress...", {
  chainId: "43113",
  address: "0xSellerOrBuyerAddress...",
});
// tx: { to, data, value, chainId, gas, maxFeePerGas, maxPriorityFeePerGas, type, instructions }
// Sign and broadcast tx with the wallet
```

### Release escrow (arbiter only)
**⚠️ Note:** This endpoint is ONLY used by the arbiter to release escrowed funds. It is not used by the buyer or seller.

```typescript
const { data } = await sdk.escrow.release("0xEscrowAddress...", {
  recipient: "0xSellerAddress...",  // optional; defaults to seller
});
// data: { success, txHash, escrowAddress, arbiter }
```

Release requires the server to be configured with `X-Release-Secret` (e.g. `RELEASE_SYSTEM_SECRET`). Call only after both seller and buyer have marked ready.

### Response envelope and errors

All SDK methods return a `ResponseDto<T>` with `status`, `message`, and `data`. On HTTP or API errors the SDK throws; use try/catch.

```typescript
try {
  const result = await sdk.escrow.getStatus("43113", escrowAddress);
  console.log(result.data);
} catch (error) {
  console.error("Escrow operation failed:", error.message);
}
```

---

## Global Response Format

SDK responses use the same envelope:

```json
{
  "status": "success" | "error",
  "message": "Human-readable status message",
  "data": { /* endpoint-specific payload or null on error */ }
}
```

Unless otherwise noted, examples show the **`data`** portion (`result.data` in code).

---
## Creating an Escrow

**IMPORTANT — Before creating an escrow:**

1. **Confirm buyer and seller addresses** — Verify both wallet addresses are correct
2. **Confirm amount** — Ensure the escrow amount matches the agreement
3. **Check wallet balance** — The buyer must have sufficient funds for gas and the escrow amount

### Example: Create escrow with SDK

```typescript
import { PsiloSDK } from "@pakt/psilo";
import type { CreateEscrowDto } from "@pakt/psilo";
const ESCROW_API_URL = process.env.ESCROW_API_URL || "https://escrowapi.psiloai.com";

const sdk = await PsiloSDK.init({
  baseUrl: ESCROW_API_URL,
});

const { data } = await sdk.escrow.create({
  chainId: "43113",
  buyer: "0xBuyerAddress...",
  seller: "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
  title: "Payment for development work",
  description: "Full-stack development services",
  amount: "1000",
  asset: "0xUSDCTokenAddress...",  // or use server default via ESCROW_ASSET_ADDRESS
} satisfies CreateEscrowDto);

console.log("Escrow created!");
console.log("Escrow Address:", data.onChain.escrowAddress);
console.log("Transaction:", `https://basescan.org/tx/${data.onChain.txHash}`);
// data.onChain.deposit → sign and send to fund the escrow
// data.onChain.approve → sign first if ERC-20, else null for native token
```

**Response structure (`data`):** `buyerWallet`, `sellerWallet`, `arbiterWallet`, `title`, `description`, `amount`, `expiration`, `releaseType`, `metadataHash`, `chainId`, and `onChain`: `{ txHash, escrowAddress, approve, deposit }`. Use `deposit` (and `approve` when present) to fund the escrow from the buyer's wallet.

### Agent-authenticated create (SIWA only)

When the agent is the buyer and you only have `receiverWallet`, `title`, `amount`, and `currency`, use the **SIWA** flow with `POST /api/escrows/agent` (see SIWA skill for authentication flow). The SDK does not wrap this endpoint; use `signAuthenticatedRequest` from `@buildersgarden/siwa/erc8128` with the receipt and the same body shape. **Evalanche** users: use standard `sdk.escrow.create()` with your `agent.address` as buyer.

---

## Depositing Funds to Escrow

After creating an escrow, funds must be deposited to the `escrowAddress`. The creator (sender) deposits funds by calling `EscrowWallet.deposit()`.

### Example: Deposit ETH to Escrow

```typescript
import { signTransaction, getAddress } from "@buildersgarden/siwa/keystore";
import { createPublicClient, http, parseEther } from "viem";
import { baseSepolia } from "viem/chains";

const ESCROW_WALLET_ABI = [
  "function deposit() external payable",
  "function getStatus() external view returns (bool _deposited, bool _released, uint256 _balance)",
] as const;

async function depositToEscrow(
  escrowAddress: string,
  amountInEth: string
) {
  const client = createPublicClient({
    chain: baseSepolia,
    transport: http(process.env.RPC_URL),
  });

  const address = await getAddress();
  const nonce = await client.getTransactionCount({ address });
  const { maxFeePerGas, maxPriorityFeePerGas } = await client.estimateFeesPerGas();

  // Encode the deposit call
  const data = "0xd0e30db0"; // deposit() function selector

  const tx = {
    to: escrowAddress,
    value: parseEther(amountInEth),
    data,
    nonce,
    chainId: baseSepolia.id,
    type: 2,
    maxFeePerGas,
    maxPriorityFeePerGas,
    gas: 100000n,
  };

  const { signedTx } = await signTransaction(tx);
  const txHash = await client.sendRawTransaction({ serializedTransaction: signedTx });

  console.log(`Deposited ${amountInEth} ETH to escrow ${escrowAddress}`);
  console.log(`Transaction: https://sepolia.basescan.org/tx/${txHash}`);

  return txHash;
}
```

### Example: Deposit ERC20 Tokens to Escrow

```typescript
import { signTransaction, getAddress } from "@buildersgarden/siwa/keystore";
import { createPublicClient, http, encodeFunctionData, parseUnits } from "viem";
import { baseSepolia } from "viem/chains";

const ERC20_ABI = [
  {
    name: "transfer",
    type: "function",
    inputs: [
      { name: "to", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [{ name: "", type: "bool" }],
  },
] as const;

const ESCROW_WALLET_ABI = [
  "function deposit() external",
] as const;

async function depositERC20ToEscrow(
  escrowAddress: string,
  tokenAddress: string,
  amount: string,
  decimals: number = 18
) {
  const client = createPublicClient({
    chain: baseSepolia,
    transport: http(process.env.RPC_URL),
  });

  const address = await getAddress();

  // First, approve the escrow to spend tokens
  const approveData = encodeFunctionData({
    abi: ERC20_ABI,
    functionName: "transfer",
    args: [escrowAddress, parseUnits(amount, decimals)],
  });

  const nonce = await client.getTransactionCount({ address });
  const { maxFeePerGas, maxPriorityFeePerGas } = await client.estimateFeesPerGas();

  const approveTx = {
    to: tokenAddress,
    data: approveData,
    nonce,
    chainId: baseSepolia.id,
    type: 2,
    maxFeePerGas,
    maxPriorityFeePerGas,
    gas: 100000n,
  };

  const { signedTx: approveSignedTx } = await signTransaction(approveTx);
  await client.sendRawTransaction({ serializedTransaction: approveSignedTx });

  // Then call deposit() on the escrow wallet
  const depositData = encodeFunctionData({
    abi: ESCROW_WALLET_ABI,
    functionName: "deposit",
  });

  const depositTx = {
    to: escrowAddress,
    data: depositData,
    nonce: nonce + 1n,
    chainId: baseSepolia.id,
    type: 2,
    maxFeePerGas,
    maxPriorityFeePerGas,
    gas: 200000n,
  };

  const { signedTx: depositSignedTx } = await signTransaction(depositTx);
  const txHash = await client.sendRawTransaction({ serializedTransaction: depositSignedTx });

  console.log(`Deposited ${amount} tokens to escrow ${escrowAddress}`);
  return txHash;
}
```

---

## Releasing Escrow Funds

Release requires **three ordered steps** — each party signs their own on-chain transaction, then the system triggers the final release.

| Step | Who | Action | SDK / API |
|------|-----|--------|-----------|
| 1 | **Seller** | Signs `markReady()` — signals work is done | `sdk.escrow.updateStatus(escrowAddress, { chainId, address })` |
| 2 | **Buyer** | Signs `markBuyerEscrowReleaseReady()` — confirms release | `sdk.escrow.updateStatus(escrowAddress, { chainId, address })` |

> Steps 1 and 2 can be done in any order. Step 3 is blocked until both are complete.

### Step 1 & 2: Seller and Buyer Mark Ready

Use the SDK to get the transaction payload for the seller or buyer. The server returns the correct tx (markReady vs markBuyerEscrowReleaseReady) based on `address`.

```typescript
// Seller: get markReady tx
const { data: sellerTx } = await sdk.escrow.updateStatus("0xEscrowAddress...", {
  chainId: CHAIN_ID,
  address: sellerWalletAddress,
});
// Sign and broadcast sellerTx with the seller's wallet

// Buyer: get markBuyerEscrowReleaseReady tx
const { data: buyerTx } = await sdk.escrow.updateStatus("0xEscrowAddress...", {
  chainId: CHAIN_ID,
  address: buyerWalletAddress,
});

**Response Structure:**
```typescript
{
  success: true,
  txHash: "0x...",              // Release transaction hash
  escrowAddress: "0x...",       // Escrow wallet address
  arbiter: "0x..."              // Arbiter address that signed the release
}
```

---

## Complete Workflow Example

End-to-end: initialize SDK → create escrow → deposit funds → seller and buyer mark ready → release.

```typescript
import { PsiloSDK } from "@pakt/psilo";
import type { CreateEscrowDto } from "@pakt/psilo";
import { signTransaction, getAddress } from "@buildersgarden/siwa/keystore";
import { createPublicClient, http, parseEther } from "viem";
import { baseSepolia } from "viem/chains";

const ESCROW_API_URL = process.env.ESCROW_API_URL || "https://escrowapi.psiloai.com";

const sdk = await PsiloSDK.init({
  baseUrl: ESCROW_API_URL,
});

const client = createPublicClient({
  chain: baseSepolia,
  transport: http(process.env.RPC_URL),
});
const chainId = String(baseSepolia.id);

// 1. Create escrow
const { data: escrow } = await sdk.escrow.create({
  chainId,
  buyer: "0xBuyerAddress...",
  seller: "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
  title: "Payment for services",
  amount: "1.0",
  asset: "0x...",  // or omit if server uses default
} satisfies CreateEscrowDto);
const escrowAddress = escrow.onChain.escrowAddress;
console.log("Escrow created:", escrowAddress);

// 2. Deposit funds (buyer signs and sends deposit tx)
const address = await getAddress();
const nonce = await client.getTransactionCount({ address });
const { maxFeePerGas, maxPriorityFeePerGas } = await client.estimateFeesPerGas();
const depositTx = {
  to: escrowAddress,
  value: parseEther("1.0"),
  data: "0xd0e30db0",
  nonce,
  chainId: baseSepolia.id,
  type: 2,
  maxFeePerGas,
  maxPriorityFeePerGas,
  gas: 100000n,
};
const { signedTx } = await signTransaction(depositTx);
const depositHash = await client.sendRawTransaction({ serializedTransaction: signedTx });
await client.waitForTransactionReceipt({ hash: depositHash });
console.log("Deposited:", depositHash);

// 3. Seller and buyer mark ready (each signs their tx from updateStatus)
const { data: sellerTx } = await sdk.escrow.updateStatus(escrowAddress, {
  chainId,
  address: escrow.sellerWallet,
});
const { data: buyerTx } = await sdk.escrow.updateStatus(escrowAddress, {
  chainId,
  address: escrow.buyerWallet,
});
// Sign and broadcast sellerTx and buyerTx with respective wallets ...

// 4. System triggers release
const { data: releaseResult } = await sdk.escrow.release(escrowAddress);
console.log("Escrow released:", releaseResult.txHash);
```

---

## Security Model

### Onchain Security

- Escrow contracts are deployed via `EscrowFactory` using CREATE2 (deterministic addresses)
- Funds are held in single-use `EscrowWallet` contracts
- Fee logic is enforced on-chain in `EscrowWallet`; PAKT reward distribution is currently disabled in the live contracts

---

## Error Handling

### Common Errors

**401 Unauthorized**
- Receipt expired or invalid
- ERC-8128 signature verification failed
- Agent not registered on ERC-8004

**403 Forbidden**
- Agent address doesn't match escrow sender/receiver
- Escrow not in a valid state for release
- For `sdk.escrow.updateStatus`: address is neither buyer nor seller

**400 Bad Request**
- Invalid request body format
- Missing required fields

**404 Not Found**
- For `sdk.escrow.getStatus`: address is not a valid escrow contract

**500 Internal Server Error**
- Onchain configuration missing (RPC URL, factory address, private key)
- Blockchain transaction failed

### Example Error Handling (SDK)

The SDK throws on failure. Use try/catch and re-authenticate or handle as needed.

```typescript
try {
  const result = await sdk.escrow.getStatus(chainId, escrowAddress);
  return result.data;
} catch (error) {
  // Re-authenticate on 401, check message for 403/404/500
  console.error("Escrow operation failed:", error.message);
  throw error;
}
```

---

## Troubleshooting

**"Invalid agent authentication"**
- Check that receipt hasn't expired (default TTL: 30 minutes)
- Verify ERC-8128 signature headers are correctly formatted
- Ensure agent is registered on ERC-8004 registry

**"Agent address does not match escrow sender or receiver"**
- Verify you're using the correct agent wallet address
- Check that the escrow was created with your agent's address as sender

**"Address is neither the escrow buyer nor seller"** (`sdk.escrow.updateStatus`)
- Ensure the `address` you pass is the connected wallet of the seller (for markReady) or buyer (for markBuyerEscrowReleaseReady)
- Address is compared on-chain to the escrow contract's buyer and seller

**"Escrow has not been deposited yet"**
- Funds must be deposited before release
- Call `EscrowWallet.deposit()` first

**"Escrow has already been released"**
- Each escrow can only be released once
- Check escrow status via `sdk.escrow.getStatus(chainId, escrowAddress)` before attempting release

---

## Supported Chains

The escrow API works with any EVM chain where `EscrowFactory` is deployed.

| Chain | Chain ID | Testnet Chain ID |
|-------|----------|------------------|
| Base | 8453 | 84532 (Base Sepolia) |
| Ethereum | 1 | 11155111 (Sepolia) |
| Avalanche | 43114 | 43113 (Fuji) |
| Polygon | 137 | 80002 (Amoy) |

Configure the chain via `ESCROW_CHAIN_ID` environment variable on the API server.

---

## Reference
- [@pakt/psilo](https://www.npmjs.com/package/@pakt/psilo) — TypeScript SDK for all escrow operations
- [SIWA (siwa.id/skill.md)](https://siwa.id/skill.md) — Agent auth and receipt-based agent endpoints; wallet + ERC-8004 registration
- [Evalanche](https://www.npmjs.com/package/evalanche) — Multi-EVM agent wallet; use with standard escrow create/deposit/update
- [SIWA Protocol Spec](https://siwa.id/docs) — SIWA authentication specification
