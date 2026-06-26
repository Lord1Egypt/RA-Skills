---
name: ditto-workflow
description: Creates, configures, and deploys on-chain automation workflows using the Ditto Network SDK. Use when the user asks to "create a workflow", "automate on-chain", "schedule transactions", "deploy a workflow", "set up recurring transfers", "swap tokens on a schedule", "automate DeFi", "create a cron job on-chain", "trigger on event", or mentions "Ditto Network". Handles workflow building, IPFS upload, on-chain registration, simulation, and cancellation. Do NOT use for general smart contract development unrelated to Ditto workflows.
license: MIT
metadata:
  author: Ditto Network
  version: 1.0.0
  category: web3-automation
  tags: [blockchain, defi, automation, workflows, smart-accounts]
---

# Ditto Workflow SDK Skill

Build and deploy declarative on-chain automation workflows using `@ditto/workflow-sdk`. Workflows define triggers (cron, event, onchain state) and jobs (batched contract calls) that execute via ZeroDev smart accounts with session keys.

**SDK source:** [github.com/dittonetwork/ditto-workflow-sdk](https://github.com/dittonetwork/ditto-workflow-sdk) (branch: `master`)

IMPORTANT: This skill file is the single source of truth for creating workflows. Do NOT read the SDK's `examples/`, `.env.example`, or `README.md` for guidance — they contain advanced operator patterns not intended for consumer workflow creation. Everything you need is in this file.

## Architecture: Owner vs Executor

Understanding these two roles is critical:

- **Owner** (the client/user): Holds a private key, creates and signs workflows. This is the only key the user provides.
- **Executor** (Ditto Network): A decentralized network of operators that runs workflows. The sdk provides the executor's public address to issue session permissions.

`submitWorkflow` takes `executorAddress` (a public `0x...` address). The session key system grants scoped permissions to this address so the network can execute on behalf of the owner's smart account.

## Critical: Before You Start

BEFORE writing any workflow code, verify the project setup:

1. Check that `@ditto/workflow-sdk` is installed: look for it in `package.json`
2. Check that a `.env` file exists with required keys (see Environment Setup below)
3. If the SDK is not installed, run: `npm install @ditto/workflow-sdk`

## Environment Setup

Create a `.env` file with exactly these two variables:

```
PRIVATE_KEY=0x...          # Owner's private key (the user's wallet — used to sign and deploy)
IPFS_SERVICE_URL=https://ipfs-service.dittonetwork.io
```

The `IPFS_SERVICE_URL` MUST be exactly `https://ipfs-service.dittonetwork.io`. No other URL works. Do not use `api.ditto.network`, localhost URLs, or any other endpoint.

The executor address is embedded in the SDK — use `getDittoExecutorAddress()` from `@ditto/workflow-sdk`.

CRITICAL:
- Never hardcode the owner's private key in source files. Always load from `.env` via `dotenv`.
- Always use `getDittoExecutorAddress()` for the executor address. Never derive it from a private key.

## Instructions

### Step 1: Gather Requirements

Ask the user for:
- **What action?** (transfer ETH, swap tokens, call a contract function)
- **On which chain?** (see Supported Chains below)
- **When/how often?** (cron schedule, on event, or when a condition is met)
- **How many times?** (execution limit)
- **Target contract address and function signature** (if calling a contract)

If the user is vague, suggest a concrete workflow and confirm before proceeding.

### Step 2: Write the Workflow Script

Create a TypeScript file that:
1. Loads environment variables with `dotenv`
2. Creates the owner account with `privateKeyToAccount`
3. Builds the workflow using `WorkflowBuilder` and `JobBuilder`
4. Submits with `submitWorkflow`, passing ALL required parameters

**Key pattern:** `WorkflowBuilder.create()` takes an `Account` (address only, no signing capability). Use `addressToEmptyAccount(owner.address)` for this. The actual `Signer` (full private key account from `privateKeyToAccount`) is passed separately to `submitWorkflow` for signing session keys and transactions.

CRITICAL — `value` must be `BigInt`:
- CORRECT: `value: BigInt(1000000000000000)` or `value: 1000000000000000n`
- WRONG: `value: 1` or `value: "1"` — plain numbers or strings cause session permissions to be generated incorrectly, resulting in failed workflow execution.

### Step 3: Fund the Smart Account

IMPORTANT: The Ditto SDK uses ZeroDev smart accounts (account abstraction). The smart account address is **different from the owner's EOA wallet address**. It is deterministically derived from the owner's private key by the ZeroDev kernel.

When `submitWorkflow` runs, it registers the workflow on-chain from this smart account. The smart account must have ETH on the target chain to pay for gas.

**How to find the smart account address:** Run the workflow script — if underfunded, the error message will include the smart account address (e.g., `AA21 didn't pay prefund`). Alternatively, add this before `submitWorkflow`:

```typescript
import { signerToEcdsaValidator } from '@zerodev/ecdsa-validator';
import { createKernelAccount } from '@zerodev/sdk';
import { createPublicClient, http } from 'viem';
import { getChainConfig } from '@ditto/workflow-sdk';

const chainConfig = getChainConfig(process.env.IPFS_SERVICE_URL!);
const chain = chainConfig[ChainId.BASE_SEPOLIA]; // use your target chain
const publicClient = createPublicClient({ chain: chain.chain, transport: http(chain.rpcUrl) });
const ecdsaValidator = await signerToEcdsaValidator(publicClient, { signer: owner, entryPoint: { address: '0x0000000071727De22E5E9d8BAf0edAc6f37da032', version: '0.7' } });
const kernelAccount = await createKernelAccount(publicClient, { plugins: { sudo: ecdsaValidator }, entryPoint: { address: '0x0000000071727De22E5E9d8BAf0edAc6f37da032', version: '0.7' } });
console.log('Smart account address (fund this):', kernelAccount.address);
```

**Funding:**
- **Testnet:** Use a faucet (e.g., Sepolia faucet, Base Sepolia faucet) to send test ETH to the smart account address
- **Production:** Send real ETH (0.005–0.01 ETH is typically enough for gas) to the smart account address on the target chain

CRITICAL: Always recommend testnet first. Only proceed to production chains after the user has verified the workflow works on testnet.

### Step 4: Run and Verify

```bash
npx ts-node your-workflow-script.ts
```

Expected output: IPFS hash and transaction receipt(s). The Ditto Network will now automatically execute this workflow according to the triggers. If submission fails, check the Troubleshooting section.

## Supported Chains

**Testnet (use for development):**

| Chain | ChainId Enum | ID |
|-------|-------------|-----|
| Ethereum Sepolia | `ChainId.SEPOLIA` | 11155111 |
| Base Sepolia | `ChainId.BASE_SEPOLIA` | 84532 |

**Production:**

| Chain | ChainId Enum | ID |
|-------|-------------|-----|
| Base | `ChainId.BASE` | 8453 |
| Arbitrum | `ChainId.ARBITRUM` | 42161 |
| Polygon | `ChainId.POLYGON` | 137 |
| Optimism | `ChainId.OPTIMISM` | 10 |
| Ethereum Mainnet | `ChainId.MAINNET` | 1 |

CRITICAL: NEVER deploy to production chains (Base, Arbitrum, Polygon, Optimism, Mainnet) without explicit user confirmation. Always default to testnet. When deploying to production, set `prodContract: true` in `submitWorkflow`.

## Trigger Types

### Cron Trigger (time-based)
```typescript
.addCronTrigger('*/5 * * * *')  // Every 5 minutes (UTC)
```

### Event Trigger (log-based)
```typescript
.addEventTrigger({
  chainId: ChainId.SEPOLIA,
  contractAddress: '0xTokenAddress',
  signature: 'Transfer(address,address,uint256)',
  filter: { from: '0xSpecificSender' }  // Optional: filter indexed params
})
```

### Onchain Trigger (state-based)
```typescript
import { OnchainConditionOperator } from '@ditto/workflow-sdk';

.addOnchainTrigger({
  chainId: ChainId.BASE,
  target: '0xOracleAddress',
  abi: 'latestAnswer() view returns (int256)',
  args: [],
  onchainCondition: {
    condition: OnchainConditionOperator.GREATER_THAN,
    value: 200000000000n  // e.g., ETH > $2000 (8 decimals)
  }
})
```

Multiple triggers are AND-ed: all must be satisfied for execution.

**OnchainConditionOperator values:** `EQUAL` (0), `GREATER_THAN` (1), `LESS_THAN` (2), `GREATER_THAN_OR_EQUAL` (3), `LESS_THAN_OR_EQUAL` (4), `NOT_EQUAL` (5), `ONE_OF` (6).

## Key Operations

### Simulate (dry run)

The SDK supports local dry-run simulation. You can issue a session to any address (not just the Ditto executor) by passing a custom address during workflow submission, then call `executeFromIpfs` with `simulate: true`. This performs gas estimation without sending transactions — useful for debugging workflows before deploying to the network.

### Cancel a Workflow

To cancel a deployed workflow, you need the IPFS hash from `submitWorkflow` and the registry address for the environment (prod or testnet):

```typescript
import { WorkflowContract, getDittoWFRegistryAddress } from '@ditto/workflow-sdk';

const registryAddress = getDittoWFRegistryAddress(false); // false = testnet, true = production
const wfContract = new WorkflowContract(registryAddress);
await wfContract.cancelWorkflow(ipfsHash, ownerAccount, chainId, process.env.IPFS_SERVICE_URL!);
```

### Check Workflow Status & Execution History

Use the Ditto Network API (base URL: `https://ipfs-service.dittonetwork.io`) to monitor deployed workflows. All endpoints use the IPFS hash returned by `submitWorkflow`. No authentication required.

**1. Workflow status** — check if the workflow is active, paused, or cancelled:
```typescript
const ipfsHash = 'QmYourWorkflowHash';
const res = await fetch(`https://ipfs-service.dittonetwork.io/workflow/status/${ipfsHash}`);
const status = await res.json();
console.log('Workflow status:', status);
```

**2. Execution logs (USE THIS to check last executions)** — returns the actual execution history with results, timestamps, and transaction details:
```typescript
const res = await fetch(`https://ipfs-service.dittonetwork.io/workflow/logs/${ipfsHash}?limit=20`);
const logs = await res.json();
console.log('Execution logs:', logs);
```
This is the primary endpoint for checking whether a workflow has run, when it ran, and whether executions succeeded or failed.

**3. Execution reports (advanced — NOT for checking execution history)** — these are internal simulation reports sent by all network operator nodes participating in the workflow. Each operator independently simulates the workflow, so you'll see multiple reports per execution (one per node). This is useful for debugging network-level issues but NOT for checking whether your workflow actually executed:
```typescript
const res = await fetch(`https://ipfs-service.dittonetwork.io/get-reports?ipfsHash=${ipfsHash}&page=1&limit=100`);
const reports = await res.json();
console.log('Node simulation reports:', reports);
```

IMPORTANT: When the user asks to "check last executions" or "see execution history", always use the **execution logs** endpoint (`/workflow/logs/`), NOT the reports endpoint. Reports show per-node simulation data, not actual execution outcomes.

### Data References (read contract state at execution time)
```typescript
import { dataRef } from '@ditto/workflow-sdk';

const ethPrice = dataRef({
  target: '0xChainlinkOracleAddress',
  abi: 'latestRoundData() returns (uint80, int256, uint256, uint256, uint80)',
  chainId: ChainId.SEPOLIA,
  resultIndex: 1,  // int256 price is the 2nd return value
});

// Use in a step arg - resolved dynamically at execution time by the network
.addStep({
  target: '0xSwapRouter',
  abi: 'swap(uint256)',
  args: [ethPrice],
})
```

## Workflow Limits

| Method | Purpose | Example |
|--------|---------|---------|
| `.setCount(n)` | Max total executions | `.setCount(100)` |
| `.setInterval(sec)` | Min seconds between runs | `.setInterval(300)` |
| `.setValidAfter(date)` | Start time (Date or ms) | `.setValidAfter(Date.now())` |
| `.setValidUntil(date)` | Expiration (Date or ms) | `.setValidUntil(Date.now() + 86400000)` |

## Step Interface

```typescript
interface Step {
  target: string;              // Contract address (0x-prefixed)
  abi: string;                 // Function signature, e.g. "transfer(address,uint256)"
                               // Empty string "" for raw ETH transfer
  args: readonly any[];        // Function arguments (can include dataRef strings)
  value?: bigint;              // ETH value in wei — MUST be BigInt
}
```

CRITICAL: The `value` field MUST use `BigInt()`. Using a plain number (e.g., `value: 1`) or string (e.g., `value: "1"`) instead of `BigInt(1)` will cause session permissions to be generated incorrectly, and the workflow will fail at execution time.

## Key Function Signatures

### submitWorkflow
```typescript
async function submitWorkflow(
  workflow: Workflow,
  executorAddress: `0x${string}`, // Use getDittoExecutorAddress()
  storage: IWorkflowStorage,
  owner: Signer,                  // Owner signs (from privateKeyToAccount)
  prodContract: boolean,          // true = mainnet registry, false = testnet
  ipfsServiceUrl: string,         // process.env.IPFS_SERVICE_URL
  usePaymaster?: boolean,         // Default: false
  switchChain?: (chainId: number) => Promise<void>,
  accessToken?: string,
): Promise<{ ipfsHash: string; userOpHashes: UserOperationReceipt[] }>;
```

IMPORTANT: `prodContract` and `ipfsServiceUrl` are REQUIRED parameters with no defaults. Always pass them explicitly.

## Complete Recipes

### Recipe 1: Recurring ETH Transfer (Testnet)

Sends 0.001 ETH to a recipient every 6 hours on Base Sepolia, up to 10 times.

```typescript
import {
  WorkflowBuilder, JobBuilder, ChainId,
  submitWorkflow, IpfsStorage, getDittoExecutorAddress
} from '@ditto/workflow-sdk';
import { privateKeyToAccount } from 'viem/accounts';
import { addressToEmptyAccount } from '@zerodev/sdk';
import * as dotenv from 'dotenv';

dotenv.config();

async function main() {
  const owner = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
  const executorAddress = getDittoExecutorAddress();
  const storage = new IpfsStorage(process.env.IPFS_SERVICE_URL!);

  const workflow = WorkflowBuilder.create(addressToEmptyAccount(owner.address))
    .addCronTrigger('0 */6 * * *')
    .setCount(10)
    .setValidUntil(Date.now() + 30 * 24 * 60 * 60 * 1000)
    .addJob(
      JobBuilder.create('eth-transfer')
        .setChainId(ChainId.BASE_SEPOLIA)
        .addStep({
          target: '0xRecipientAddressHere',
          abi: '',
          args: [],
          value: BigInt('1000000000000000') // 0.001 ETH in wei
        })
        .build()
    )
    .build();

  const { ipfsHash, userOpHashes } = await submitWorkflow(
    workflow,
    executorAddress,
    storage,
    owner,
    false,                         // testnet
    process.env.IPFS_SERVICE_URL!,
  );

  console.log('Deployed! IPFS hash:', ipfsHash);
  console.log('UserOp receipts:', userOpHashes.map(r => r.receipt?.transactionHash));
}

main().catch(console.error);
```

### Recipe 2: ERC-20 Approve + Swap (Production)

Approves a token and swaps it on a DEX every week on Base. Steps within a single job execute atomically.

```typescript
import {
  WorkflowBuilder, JobBuilder, ChainId,
  submitWorkflow, IpfsStorage, getDittoExecutorAddress
} from '@ditto/workflow-sdk';
import { privateKeyToAccount } from 'viem/accounts';
import { addressToEmptyAccount } from '@zerodev/sdk';
import * as dotenv from 'dotenv';

dotenv.config();

async function main() {
  const owner = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
  const executorAddress = getDittoExecutorAddress();
  const storage = new IpfsStorage(process.env.IPFS_SERVICE_URL!);

  const tokenAddress = '0xYourTokenAddress';
  const routerAddress = '0xDEXRouterAddress';
  const wethAddress = '0xWETHAddress';
  const swapAmount = BigInt('1000000000000000000'); // 1 token (18 decimals)

  const workflow = WorkflowBuilder.create(addressToEmptyAccount(owner.address))
    .addCronTrigger('0 0 * * 1')  // Every Monday at midnight UTC
    .setCount(52)                  // Up to 52 weeks
    .setValidUntil(Date.now() + 365 * 24 * 60 * 60 * 1000)
    .addJob(
      JobBuilder.create('weekly-dca')
        .setChainId(ChainId.BASE)
        .addStep({
          target: tokenAddress,
          abi: 'approve(address,uint256)',
          args: [routerAddress, swapAmount],
          value: BigInt(0),
        })
        .addStep({
          target: routerAddress,
          abi: 'swapExactTokensForETH(uint256,uint256,address[],address,uint256)',
          args: [
            swapAmount,
            BigInt(0),                    // minAmountOut (0 for simplicity — use dataRef for production)
            [tokenAddress, wethAddress],
            owner.address,
            BigInt(Math.floor(Date.now() / 1000) + 365 * 24 * 60 * 60), // 1 year deadline
          ],
          value: BigInt(0),
        })
        .build()
    )
    .build();

  const { ipfsHash, userOpHashes } = await submitWorkflow(
    workflow,
    executorAddress,
    storage,
    owner,
    true,                          // PRODUCTION
    process.env.IPFS_SERVICE_URL!,
  );

  console.log('Deployed! IPFS hash:', ipfsHash);
  console.log('UserOp receipts:', userOpHashes.map(r => r.receipt?.transactionHash));
}

main().catch(console.error);
```

Note: Time-dependent args like `deadline` are computed at script build time, not execution time. For workflows that may execute far in the future, use generous deadlines or `dataRef` for on-chain timestamps.

### Recipe 3: Call a Custom Contract on Event

Listens for a `Transfer` event on a token contract and calls a custom contract function when it fires. This pattern works for any contract and any event.

```typescript
import {
  WorkflowBuilder, JobBuilder, ChainId,
  submitWorkflow, IpfsStorage, getDittoExecutorAddress
} from '@ditto/workflow-sdk';
import { privateKeyToAccount } from 'viem/accounts';
import { addressToEmptyAccount } from '@zerodev/sdk';
import * as dotenv from 'dotenv';

dotenv.config();

async function main() {
  const owner = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
  const executorAddress = getDittoExecutorAddress();
  const storage = new IpfsStorage(process.env.IPFS_SERVICE_URL!);

  const workflow = WorkflowBuilder.create(addressToEmptyAccount(owner.address))
    // Trigger: fire when a Transfer event is emitted by the token contract
    .addEventTrigger({
      chainId: ChainId.SEPOLIA,
      contractAddress: '0xTokenContractAddress',
      signature: 'Transfer(address,address,uint256)',
      filter: { to: owner.address },  // Optional: only when tokens are sent TO the owner
    })
    .setCount(5)
    .setValidUntil(Date.now() + 30 * 24 * 60 * 60 * 1000)
    .addJob(
      JobBuilder.create('custom-action')
        .setChainId(ChainId.SEPOLIA)
        .addStep({
          target: '0xYourCustomContractAddress',
          abi: 'processDeposit(address,uint256,bool)',
          args: [
            '0xSomeAddress',
            BigInt('500000000000000000'), // 0.5 (18 decimals)
            true,
          ],
          value: BigInt(0),
        })
        .build()
    )
    .build();

  const { ipfsHash, userOpHashes } = await submitWorkflow(
    workflow,
    executorAddress,
    storage,
    owner,
    false,                         // testnet
    process.env.IPFS_SERVICE_URL!,
  );

  console.log('Deployed! IPFS hash:', ipfsHash);
  console.log('UserOp receipts:', userOpHashes.map(r => r.receipt?.transactionHash));
}

main().catch(console.error);
```

To adapt this recipe: replace the `signature` with any event your contract emits (e.g., `OrderPlaced(uint256,address)`), adjust the `filter` for indexed parameters, and replace the step's `target`/`abi`/`args` with your contract's function.

### Recipe 4: Price-Triggered Swap with Data Reference (Advanced)

Monitors a Chainlink oracle and swaps tokens when ETH drops below $2000, using the live price as a swap argument.

```typescript
import {
  WorkflowBuilder, JobBuilder, ChainId,
  submitWorkflow, IpfsStorage, getDittoExecutorAddress,
  dataRef, OnchainConditionOperator
} from '@ditto/workflow-sdk';
import { privateKeyToAccount } from 'viem/accounts';
import { addressToEmptyAccount } from '@zerodev/sdk';
import * as dotenv from 'dotenv';

dotenv.config();

async function main() {
  const owner = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
  const executorAddress = getDittoExecutorAddress();
  const storage = new IpfsStorage(process.env.IPFS_SERVICE_URL!);

  // Data reference: read live ETH/USD price at execution time
  const ethPrice = dataRef({
    target: '0x694AA1769357215DE4FAC081bf1f309aDC325306', // Chainlink ETH/USD on Sepolia
    abi: 'latestRoundData() returns (uint80, int256, uint256, uint256, uint80)',
    chainId: ChainId.SEPOLIA,
    resultIndex: 1, // int256 price (2nd return value)
  });

  const workflow = WorkflowBuilder.create(addressToEmptyAccount(owner.address))
    // Trigger: check price every 5 minutes, fire when ETH < $2000
    .addCronTrigger('*/5 * * * *')
    .addOnchainTrigger({
      chainId: ChainId.SEPOLIA,
      target: '0x694AA1769357215DE4FAC081bf1f309aDC325306',
      abi: 'latestAnswer() view returns (int256)',
      args: [],
      onchainCondition: {
        condition: OnchainConditionOperator.LESS_THAN,
        value: BigInt('200000000000'), // $2000 with 8 decimals
      },
    })
    .setCount(3)
    .setValidUntil(Date.now() + 7 * 24 * 60 * 60 * 1000)
    .addJob(
      JobBuilder.create('price-swap')
        .setChainId(ChainId.SEPOLIA)
        .addStep({
          target: '0xSwapRouterAddress',
          abi: 'swap(uint256)',
          args: [ethPrice], // Resolved dynamically at execution time
          value: BigInt(0),
        })
        .build()
    )
    .build();

  const { ipfsHash, userOpHashes } = await submitWorkflow(
    workflow,
    executorAddress,
    storage,
    owner,
    false,                         // testnet
    process.env.IPFS_SERVICE_URL!,
  );

  console.log('Deployed! IPFS hash:', ipfsHash);
  console.log('UserOp receipts:', userOpHashes.map(r => r.receipt?.transactionHash));
}

main().catch(console.error);
```

### Recipe 5: Multi-Chain Workflow

Deploys a workflow with jobs on two different chains. Each job gets its own session key and on-chain registration.

```typescript
import {
  WorkflowBuilder, JobBuilder, ChainId,
  submitWorkflow, IpfsStorage, getDittoExecutorAddress
} from '@ditto/workflow-sdk';
import { privateKeyToAccount } from 'viem/accounts';
import { addressToEmptyAccount } from '@zerodev/sdk';
import * as dotenv from 'dotenv';

dotenv.config();

async function main() {
  const owner = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
  const executorAddress = getDittoExecutorAddress();
  const storage = new IpfsStorage(process.env.IPFS_SERVICE_URL!);

  const workflow = WorkflowBuilder.create(addressToEmptyAccount(owner.address))
    .addCronTrigger('0 */12 * * *') // Every 12 hours
    .setCount(20)
    .setValidUntil(Date.now() + 30 * 24 * 60 * 60 * 1000)
    .addJob(
      JobBuilder.create('sepolia-transfer')
        .setChainId(ChainId.SEPOLIA)
        .addStep({
          target: '0xRecipientOnSepolia',
          abi: '',
          args: [],
          value: BigInt('100000000000000') // 0.0001 ETH
        })
        .build()
    )
    .addJob(
      JobBuilder.create('base-sepolia-transfer')
        .setChainId(ChainId.BASE_SEPOLIA)
        .addStep({
          target: '0xRecipientOnBaseSepolia',
          abi: '',
          args: [],
          value: BigInt('100000000000000') // 0.0001 ETH
        })
        .build()
    )
    .build();

  const { ipfsHash, userOpHashes } = await submitWorkflow(
    workflow,
    executorAddress,
    storage,
    owner,
    false,
    process.env.IPFS_SERVICE_URL!,
  );

  console.log('Deployed! IPFS hash:', ipfsHash);
  console.log('UserOp receipts:', userOpHashes.map(r => r.receipt?.transactionHash));
}

main().catch(console.error);
```

Note: The smart account must be funded on BOTH chains for multi-chain workflows.

### Recipe 6: Cancel a Workflow

Cancels a previously deployed workflow using its IPFS hash.

```typescript
import {
  WorkflowContract, getDittoWFRegistryAddress, ChainId
} from '@ditto/workflow-sdk';
import { privateKeyToAccount } from 'viem/accounts';
import * as dotenv from 'dotenv';

dotenv.config();

async function main() {
  const owner = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
  const ipfsHash = 'QmYourWorkflowIpfsHash'; // From submitWorkflow output

  const registryAddress = getDittoWFRegistryAddress(false); // false = testnet
  const wfContract = new WorkflowContract(registryAddress);

  const receipt = await wfContract.cancelWorkflow(
    ipfsHash,
    owner,
    ChainId.BASE_SEPOLIA,          // The chain the job was registered on
    process.env.IPFS_SERVICE_URL!,
  );

  console.log('Workflow cancelled! Tx:', receipt.receipt?.transactionHash);
}

main().catch(console.error);
```

Note: You must cancel on each chain the workflow has jobs on. For multi-chain workflows, call `cancelWorkflow` once per chain.

## Validation Checklist

BEFORE calling `submitWorkflow`, verify:
- Every step has a valid `target` address (0x-prefixed, 42 chars)
- `abi` is a valid Solidity function signature or empty string for raw ETH transfer
- All `value` fields use `BigInt()` — never plain numbers or strings
- `chainId` is from the supported chains list
- At least one trigger is defined
- `count` is > 0 if set
- `validUntil` is in the future
- `.env` has `PRIVATE_KEY` and `IPFS_SERVICE_URL`
- `prodContract` and `ipfsServiceUrl` are passed explicitly to `submitWorkflow`

## Troubleshooting

### Error: "Missing required environment variables"
Cause: `.env` file missing or incomplete.
Solution: Ensure `PRIVATE_KEY` and `IPFS_SERVICE_URL` are set. The IPFS URL must be exactly `https://ipfs-service.dittonetwork.io`. The executor address is provided by the SDK via `getDittoExecutorAddress()` — do NOT add it to `.env`.

### Error: "Chain ID must be greater than 0"
Cause: `setChainId()` not called on JobBuilder.
Solution: Add `.setChainId(ChainId.BASE_SEPOLIA)` before `.build()`.

### Error: "Job must have at least one step"
Cause: No steps added to a job.
Solution: Add at least one `.addStep({...})` call.

### Error: "Expiration time must be in the future"
Cause: `setValidUntil` was given a past timestamp.
Solution: Use `Date.now() + duration_in_ms`.

### Error: "AA21 didn't pay prefund"
Cause: The ZeroDev smart account doesn't have enough ETH to pay for gas. The smart account address is different from the owner's EOA — it's derived deterministically from the owner's private key.
Solution: Send ETH to the smart account address shown in the error on the target chain. See "Step 3: Fund the Smart Account" above. For testnet, use a faucet. For production, 0.005–0.01 ETH is typically enough.

### Transaction fails / reverts
Causes:
- Smart account has insufficient ETH for the step values
- Target contract function reverts (wrong args, permissions)
- Session key expired or misconfigured
- `value` was not passed as `BigInt` (causes empty session permissions)

Solution: Ensure the owner's smart account is funded on the target chain. Verify contract args are correct. Verify all `value` fields use `BigInt()`.

### IPFS upload fails
Cause: `IPFS_SERVICE_URL` unreachable or invalid.
Solution: The URL must be exactly `https://ipfs-service.dittonetwork.io`. No other URL works.

### Workflow deploys but never executes
Causes:
- Smart account not funded on the target chain
- Trigger conditions never met (e.g., cron in the past, price threshold never reached)
- `validUntil` already expired
- `count` already exhausted from prior runs

Solution: Check execution logs via `https://ipfs-service.dittonetwork.io/workflow/logs/{ipfsHash}` to see if execution was attempted. Check reports via `https://ipfs-service.dittonetwork.io/get-reports?ipfsHash={ipfsHash}` to see if nodes are simulating it.
