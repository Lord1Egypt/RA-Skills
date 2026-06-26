# QFC DeFi Operations Guide

## Overview

QFC supports standard EVM-compatible DeFi operations. All Solidity contracts deployed on Ethereum can run on QFC with minimal changes. Gas fees are extremely low (<$0.0001 per transaction).

## Staking

### Validator Staking

Validators secure the network through the Proof of Contribution (PoC) consensus.

| Parameter | Value |
|-----------|-------|
| Minimum stake | 10,000 QFC |
| Unstake delay | 7 days |
| Max active validators | 1,000 |
| Max single validator | 1% of total stake |
| Estimated APY | 8-18% |

```typescript
const staking = new QFCStaking('testnet');

// List validators
const validators = await staking.getValidators();

// Check stake for an address
const stake = await staking.getStake('0x1234...');

// Get contribution score (0-10000)
const score = await staking.getContributionScore('0x1234...');

// Detailed 7-dimension breakdown
const breakdown = await staking.getScoreBreakdown('0x1234...');
```

### Delegation

Delegate QFC to a validator without running a node.

| Parameter | Value |
|-----------|-------|
| Minimum delegation | 100 QFC |
| Commission range | 0-20% |
| Delegator reward | validator_share * (1 - commission) |

Delegates share in validator slashing risk.

## Token Swaps

QFC has a built-in SimpleSwap contract (constant product AMM, x*y=k).

```typescript
const contract = new QFCContract('testnet');

// Read pool reserves
const reserves = await contract.call(
  SWAP_ADDRESS,
  SWAP_ABI,
  'getReserves',
);

// Swap tokens (requires wallet)
await contract.send(
  SWAP_ADDRESS,
  SWAP_ABI,
  'swapExactTokensForTokens',
  [amountIn, amountOutMin, [tokenA, tokenB], deadline],
  wallet,
);
```

Swap fee: 0.3% per trade.

## Liquidity Provision

Provide liquidity to earn swap fees.

```typescript
// Add liquidity
await contract.send(
  SWAP_ADDRESS,
  SWAP_ABI,
  'addLiquidity',
  [tokenA, tokenB, amountA, amountB, minA, minB, deadline],
  wallet,
);

// Remove liquidity
await contract.send(
  SWAP_ADDRESS,
  SWAP_ABI,
  'removeLiquidity',
  [tokenA, tokenB, liquidity, minA, minB, deadline],
  wallet,
);
```

## Yield Vaults

QFC supports ERC-4626 style yield vaults.

```typescript
// Deposit into vault
await contract.send(VAULT_ADDRESS, VAULT_ABI, 'deposit', [amount, receiver], wallet);

// Check shares
const shares = await contract.call(VAULT_ADDRESS, VAULT_ABI, 'balanceOf', [address]);

// Withdraw
await contract.send(VAULT_ADDRESS, VAULT_ABI, 'withdraw', [amount, receiver, owner], wallet);
```

## Fee Structure

QFC uses EIP-1559 style dynamic gas pricing:

| Operation | Gas | Cost (1 Gwei base) |
|-----------|-----|---------------------|
| Simple transfer | 21,000 | 0.000021 QFC |
| ERC-20 transfer | ~65,000 | 0.000065 QFC |
| Swap | ~150,000 | 0.00015 QFC |
| Contract deploy | ~500,000 | 0.0005 QFC |
| NFT mint | ~100,000 | 0.0001 QFC |

Fee distribution: 50% block producer, 30% voters, 20% burned.

## Key Contract Addresses

Contract addresses are available via `qfc-contracts` repo. Use the QFC Explorer to verify addresses:
- Testnet: https://explorer.testnet.qfc.network/contracts
- Mainnet: https://explorer.qfc.network/contracts
