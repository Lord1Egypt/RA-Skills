# ERC-20 Token Deployment on QFC

## Quick Start

Deploy a token in 3 steps:

1. **Create & fund a wallet**
2. **Deploy the token**
3. **(Optional) Verify on explorer**

```typescript
import { QFCWallet, QFCToken } from '@qfc/openclaw-skill';

// 1. Create wallet & fund via faucet
const wallet = new QFCWallet('testnet');
const { address, privateKey } = wallet.create();
// Fund via faucet or transfer QFC to this address

// 2. Deploy token
const token = new QFCToken('testnet');
const result = await token.deploy(
  'My Token',     // name
  'MTK',          // symbol
  '1000000',      // initial supply (1M tokens, 18 decimals)
  signer,         // ethers.Wallet instance
);

console.log('Contract:', result.contractAddress);
console.log('Explorer:', result.explorerUrl);
```

## Constructor Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | string | Full token name (e.g. "QFC Rewards Token") |
| `symbol` | string | Short ticker symbol (e.g. "QREW"), typically 3-5 chars |
| `initialSupply` | string | Human-readable amount (e.g. "1000000" = 1M tokens). All tokens have 18 decimals. Entire supply is minted to the deployer. |

## Token Contract Details

The pre-compiled contract is a standard ERC-20 with:

- **Solidity version**: 0.8.34
- **EVM target**: Paris (no PUSH0 opcode — required for QFC compatibility)
- **Optimizer**: enabled, 200 runs
- **Decimals**: 18 (hardcoded)
- **Functions**: `transfer`, `approve`, `transferFrom`, `balanceOf`, `allowance`, `name`, `symbol`, `decimals`, `totalSupply`
- **Events**: `Transfer`, `Approval`

The contract is **not mintable** — the total supply is fixed at deployment. There is no owner/admin role.

## Gas Costs

| Operation | Estimated Gas | Approximate Cost (1 gwei gas price) |
|-----------|--------------|--------------------------------------|
| Deploy token | ~540,000 | ~0.00054 QFC |
| Transfer | ~52,000 | ~0.000052 QFC |
| Approve | ~46,000 | ~0.000046 QFC |
| TransferFrom | ~63,000 | ~0.000063 QFC |

Gas limit is set to 800,000 for deployment to provide margin.

## After Deployment

### Verify Token Info

Token info can be read via `eth_getStorageAt` (recommended on QFC) or via `QFCToken.getTokenInfo()`:

```typescript
// Read via storage slots (works reliably on QFC)
// Slot 0: name (short string)
// Slot 1: symbol (short string)
// Slot 2: totalSupply (uint256)
// Slot 3[address]: balanceOf mapping

// Or via the QFCToken class:
const info = await token.getTokenInfo(result.contractAddress);
```

### Verify on Explorer

Submit the source code to the QFC explorer for public verification:

```
POST https://explorer.testnet.qfc.network/api/contracts/verify
{
  "address": "0x...",
  "sourceCode": "<solidity source>",
  "compilerVersion": "v0.8.28",
  "evmVersion": "paris",
  "optimizationRuns": 200
}
```

The source code is available as `ERC20_SOURCE_CODE` export:

```typescript
import { ERC20_SOURCE_CODE } from '@qfc/openclaw-skill';
```

### Transfer Tokens

```typescript
await token.transfer(
  contractAddress,
  '0xRecipient...',
  '100',        // 100 tokens
  signer,
);
```

### Approve & TransferFrom

```typescript
// Approve a spender
await token.approve(contractAddress, spenderAddress, '500', signer);

// Check allowance
const allowance = await token.getAllowance(contractAddress, ownerAddress, spenderAddress);
```

## Testnet vs Mainnet

| | Testnet | Mainnet |
|---|---------|---------|
| Chain ID | 9000 | 9001 |
| RPC | `https://rpc.testnet.qfc.network` | `https://rpc.qfc.network` |
| Explorer | `https://explorer.testnet.qfc.network` | `https://explorer.qfc.network` |
| Free QFC | Faucet available | No faucet |
| Recommended for | Testing, development | Production tokens |

Always test on testnet first before deploying to mainnet.

## Known QFC EVM Quirks

1. **PUSH0 not supported** — Contracts must be compiled with `evmVersion: "paris"` or earlier. The pre-compiled bytecode already handles this.

2. **eth_call may return empty** — View function calls via `eth_call` can return `0x` on QFC testnet. Use `eth_getStorageAt` as a workaround to read contract state directly.

3. **Log fields may be null** — Transaction receipts from QFC may have `null` values for `transactionIndex`, `blockNumber`, etc. in log entries. The `deploy()` method uses raw RPC polling to avoid ethers.js parsing errors.

4. **Gas estimation can overshoot** — ethers.js gas estimation may exceed the block gas limit (30M). The deploy method sets an explicit `gasLimit: 800000`.

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| `INSUFFICIENT_FUNDS` | Not enough QFC for gas | Fund wallet via faucet or transfer |
| `Transaction not confirmed after 120s` | Network congestion or RPC issue | Check tx hash on explorer, retry |
| `Deploy transaction reverted` | Invalid constructor args or bytecode issue | Check parameters, try with more gas |
| `NONCE_TOO_LOW` | Previous tx still pending | Wait for pending tx to confirm |
