---
name: turbos
description: Integrate the Turbos Finance CLMM SDK on Sui for pools, swaps, positions, fees, and liquidity workflows. Use when building or analyzing apps that interact with Turbos Finance concentrated liquidity pools.
version: 0.1.0
metadata:
  openclaw:
    homepage: https://github.com/turbos-finance/turbos-skills
---

# Turbos Finance CLMM SDK - Integration Guide

Turbos Finance is a Concentrated Liquidity Market Maker (CLMM) DEX on Sui. This guide covers the `turbos-clmm-sdk` package for building DeFi applications.

- **Repository**: https://github.com/turbos-finance/turbos-clmm-sdk
- **npm**: `turbos-clmm-sdk`

---

## Table of Contents

1. [Installation](#installation)
2. [SDK Initialization](#sdk-initialization)
3. [Module: Contract](#module-contract)
4. [Module: Pool](#module-pool)
5. [Module: Trade](#module-trade)
6. [Module: Position](#module-position)
7. [Module: Account](#module-account)
8. [Module: Math](#module-math)
9. [Key Types Reference](#key-types-reference)

---

## Installation

```bash
pnpm add turbos-clmm-sdk @mysten/sui
```

---

## SDK Initialization

```typescript
import { Network, TurbosSdk } from 'turbos-clmm-sdk';
import { SuiClient } from '@mysten/sui/client';

// Mainnet (default fullnode RPC)
const sdk = new TurbosSdk(Network.mainnet);

// Testnet
const sdk = new TurbosSdk(Network.testnet);

// Custom SuiClient
const client = new SuiClient({ url: 'YOUR_RPC_URL' });
const sdk = new TurbosSdk(Network.mainnet, client);

// Custom SuiClientOptions
const sdk = new TurbosSdk(Network.mainnet, { url: 'YOUR_RPC_URL' });
```

### SDK Structure

The `TurbosSdk` instance exposes the following modules:

| Property | Type | Description |
|----------|------|-------------|
| `sdk.pool` | `Pool` | Pool creation, liquidity operations |
| `sdk.contract` | `Contract` | Protocol configuration & fee tiers |
| `sdk.trade` | `Trade` | Swap operations |
| `sdk.position` | `Position` | Position/NFT queries (replaces `sdk.nft`) |
| `sdk.math` | `MathUtil` | Tick/price/sqrt math utilities |
| `sdk.account` | `Account` | Keypair & mnemonic helpers |
| `sdk.coin` | `Coin` | Coin metadata & selection |
| `sdk.provider` | `SuiClient` | Underlying Sui RPC client |

---

## Module: Contract

Protocol configuration and fee tier management.

### getConfig

```typescript
import type { Contract } from 'turbos-clmm-sdk';

const config: Contract.Config = await sdk.contract.getConfig();
// Returns: { PackageId, PackageIdOriginal, PoolConfig, Positions, Versioned, PoolTableId, ... }
```

### getFees

```typescript
const fees: Contract.Fee[] = await sdk.contract.getFees();
// Each fee: { fee: number, objectId: string, type: string, tickSpacing: number }
```

### getFee

```typescript
// Get fee tier by tick spacing
const fee: Contract.Fee = await sdk.contract.getFee(60);
```

### Contract.Config Interface

```typescript
interface Config {
  PackageId: string;
  PackageIdOriginal: string;
  PoolConfig: string;
  Positions: string;
  PoolFactoryAdminCap: string;
  Versioned: string;
  PoolTableId: string;
  VaultOriginPackageId: string;
  VaultPackageId: string;
  VaultGlobalConfig: string;
  VaultRewarderManager: string;
  VaultUserTierConfig: string;
  AclConfig: string;
}
```

---

## Module: Pool

Core pool operations: create, add/remove liquidity, collect fees/rewards.

### getPools

```typescript
// Get all unlocked pools
const pools: Pool.Pool[] = await sdk.pool.getPools();

// Include locked pools
const allPools: Pool.Pool[] = await sdk.pool.getPools(true);
```

### getPool

```typescript
const pool: Pool.Pool = await sdk.pool.getPool(poolId);
```

### createPool

```typescript
const fee = await sdk.contract.getFee(60); // or other tick spacing

const txb = await sdk.pool.createPool({
  fee,                          // Fee object from sdk.contract.getFees()
  coinTypeA: '0x2::sui::SUI',
  coinTypeB: '0x...::usdc::USDC',
  sqrtPrice: '79226673515401279992447579055',  // Initial sqrt price (X64)
  address: 'YOUR_SUI_ADDRESS',
  amountA: '1000000000',        // Amount of coin A (raw units)
  amountB: '1000000',           // Amount of coin B (raw units)
  tickLower: -100,
  tickUpper: 100,
  slippage: '5',                // Percentage [0, 100)
  deadline: 60000,              // Optional, default 60s
});
```

### addLiquidity (Open New Position)

```typescript
const txb = await sdk.pool.addLiquidity({
  pool: poolId,
  address: 'YOUR_SUI_ADDRESS',
  amountA: '1000000000',
  amountB: '1000000',
  tickLower: -100,
  tickUpper: 100,
  slippage: '5',                // Percentage [0, 100)
  deadline: 60000,              // Optional
  txb: existingTxb,             // Optional, append to existing transaction
});
```

### increaseLiquidity (Add to Existing Position)

```typescript
const txb = await sdk.pool.increaseLiquidity({
  pool: poolId,
  nft: positionNftId,           // Existing position NFT ID
  address: 'YOUR_SUI_ADDRESS',
  amountA: '500000000',
  amountB: '500000',
  slippage: '5',
  deadline: 60000,
});
```

### decreaseLiquidity

```typescript
const txb = await sdk.pool.decreaseLiquidity({
  pool: poolId,
  nft: positionNftId,
  address: 'YOUR_SUI_ADDRESS',
  amountA: '500000000',         // Expected amount A to receive
  amountB: '500000',            // Expected amount B to receive
  decreaseLiquidity: '1000000', // Liquidity units to remove
  slippage: '5',
});
```

### decreaseLiquidityWithReturn

Returns coin objects instead of transferring, for composability in PTBs:

```typescript
const { txb, coinA, coinB } = await sdk.pool.decreaseLiquidityWithReturn({
  pool: poolId,
  nft: positionNftId,
  address: 'YOUR_SUI_ADDRESS',
  amountA: '500000000',
  amountB: '500000',
  decreaseLiquidity: '1000000',
  slippage: '5',
});
// coinA, coinB are TransactionObjectArguments for further PTB composition
```

### removeLiquidity (Full Removal + Collect + Burn)

Combines `decreaseLiquidity` + `collectFee` + `collectReward` + `burn`:

```typescript
const txb = await sdk.pool.removeLiquidity({
  pool: poolId,
  nft: positionNftId,
  address: 'YOUR_SUI_ADDRESS',
  amountA: '500000000',
  amountB: '500000',
  decreaseLiquidity: '1000000',
  slippage: '5',
  collectAmountA: '1000',       // Fee amount A to collect
  collectAmountB: '1000',       // Fee amount B to collect
  rewardAmounts: ['500', '0', '0'],
});
```

### collectFee

```typescript
const txb = await sdk.pool.collectFee({
  pool: poolId,
  nft: positionNftId,
  address: 'YOUR_SUI_ADDRESS',
  collectAmountA: '1000',
  collectAmountB: '1000',
});
```

### collectReward

```typescript
const txb = await sdk.pool.collectReward({
  pool: poolId,
  nft: positionNftId,
  address: 'YOUR_SUI_ADDRESS',
  rewardAmounts: ['500', '0', '0'],  // Amount per reward slot
});
```

### estimateAmountsFromOneAmount

Estimate the required token pair amounts given a single token amount:

```typescript
const [amountA, amountB] = sdk.pool.estimateAmountsFromOneAmount({
  sqrtPrice: pool.sqrt_price,
  tickLower: -100,
  tickUpper: 100,
  amount: '1000000000',
  isAmountA: true,
});
```

### getTokenAmountsFromLiquidity

Calculate token amounts from a liquidity value:

```typescript
import BN from 'bn.js';

const [amountA, amountB] = sdk.pool.getTokenAmountsFromLiquidity({
  currentSqrtPrice: new BN(pool.sqrt_price),
  lowerSqrtPrice: sdk.math.tickIndexToSqrtPriceX64(tickLower),
  upperSqrtPrice: sdk.math.tickIndexToSqrtPriceX64(tickUpper),
  liquidity: new BN(position.liquidity),
  ceil: true,  // Optional, defaults true
});
```

### getPoolTypeArguments

```typescript
// Returns [coinTypeA, coinTypeB, feeType]
const types: Pool.Types = await sdk.pool.getPoolTypeArguments(poolId);
```

### fetchTicks

Fetch all initialized ticks for a pool:

```typescript
const ticks = await sdk.pool.fetchTicks(poolId);
// Each tick: { id, tick_index, liquidity_gross, liquidity_net, fee_growth_outside_a/b, ... }
```

---

## Module: Trade

Swap operations with single-hop and multi-hop routing.

### computeSwapResult

Simulate a swap to get expected output (single amount for all pools):

```typescript
import type { Trade } from 'turbos-clmm-sdk';

const results: Trade.ComputedSwapResult[] = await sdk.trade.computeSwapResult({
  pools: [{ pool: poolId, a2b: true }],
  address: 'YOUR_SUI_ADDRESS',
  amountSpecified: '1000000000',
  amountSpecifiedIsInput: true,
  tickStep: 100,   // Optional, default 100
});

// Result fields: { a_to_b, amount_a, amount_b, fee_amount, protocol_fee,
//   sqrt_price, tick_current_index, tick_pre_index, pool, ... }
```

### computeSwapResultV2

Simulate a swap with per-pool amounts (useful for multi-hop with different amounts):

```typescript
const results = await sdk.trade.computeSwapResultV2({
  pools: [
    { pool: poolId1, a2b: true, amountSpecified: '500000000' },
    { pool: poolId2, a2b: false, amountSpecified: '500000000' },
  ],
  address: 'YOUR_SUI_ADDRESS',
  amountSpecifiedIsInput: true,
});
```

### swap

Execute a swap (supports up to 2-hop routing):

```typescript
const swapResult = await sdk.trade.computeSwapResult({ ... });

const txb = await sdk.trade.swap({
  routes: [{
    pool: poolId,
    a2b: true,
    nextTickIndex: sdk.math.bitsToNumber(swapResult[0].tick_current_index.bits),
  }],
  coinTypeA: '0x2::sui::SUI',
  coinTypeB: '0x...::usdc::USDC',
  address: 'YOUR_SUI_ADDRESS',
  amountA: swapResult[0].amount_a,
  amountB: swapResult[0].amount_b,
  amountSpecifiedIsInput: true,
  slippage: '1',   // Percentage
});
```

### swapWithReturn

Swap and return coin objects for PTB composability:

```typescript
const { txb, coinVecA, coinVecB } = await sdk.trade.swapWithReturn({
  poolId,
  coinType: coinTypeA,
  amountA: '1000000000',
  amountB: '500000',
  swapAmount: '1000000000',
  nextTickIndex: tickIndex,
  slippage: '1',
  amountSpecifiedIsInput: true,
  a2b: true,
  address: 'YOUR_SUI_ADDRESS',
});
```

### swapWithPartner

Swap with a partner fee split:

```typescript
const txb = await sdk.trade.swapWithPartner({
  poolId,
  swapAmount: '1000000000',
  amountSpecifiedIsInput: true,
  slippage: '1',
  a2b: true,
  address: 'YOUR_SUI_ADDRESS',
  partner: 'PARTNER_OBJECT_ID',
});
```

---

## Module: Position

Position (NFT) management and analytics. `sdk.position` replaces the deprecated `sdk.nft`.

### getPositionsByOwner (via SuiClient)

The SDK does not provide a built-in method to list all positions by owner address. Instead, use `sdk.provider.getOwnedObjects` to query `TurbosPositionNFT` objects, then batch-fetch position details. This is the pattern used by Turbos' own frontend:

```typescript
import { unstable_getObjectFields, unstable_getObjectId, type NFT } from 'turbos-clmm-sdk';
import type { PaginatedObjectsResponse } from '@mysten/sui/client';

interface PositionInfo extends NFT.PositionField {
  nftId: string;
  positionId: string;
  poolId: string;
  tickLower: number;
  tickUpper: number;
  objectId: string;
}

async function getPositionsByOwner(
  sdk: TurbosSdk,
  ownerAddress: string,
): Promise<PositionInfo[]> {
  const contract = await sdk.contract.getConfig();

  // Step 1: Paginate through all TurbosPositionNFT objects owned by the address
  const nfts: { nftId: string; positionId: string; poolId: string }[] = [];
  let cursor: string | null | undefined;
  let page: PaginatedObjectsResponse;
  do {
    page = await sdk.provider.getOwnedObjects({
      owner: ownerAddress,
      options: { showContent: true, showOwner: true },
      cursor,
      filter: {
        StructType: `${contract.PackageIdOriginal}::position_nft::TurbosPositionNFT`,
      },
    });
    page.data.forEach((item) => {
      const nftId = unstable_getObjectId(item);
      const fields = unstable_getObjectFields(item) as {
        position_id: string;
        pool_id: string;
      };
      if (fields.position_id && fields.pool_id) {
        nfts.push({ nftId, positionId: fields.position_id, poolId: fields.pool_id });
      }
    });
    cursor = page.nextCursor;
  } while (page.hasNextPage);

  if (nfts.length === 0) return [];

  // Step 2: Batch fetch position details (max 50 per call)
  const batchSize = 50;
  const batches: Promise<any[]>[] = [];
  for (let i = 0; i < nfts.length; i += batchSize) {
    batches.push(
      sdk.provider.multiGetObjects({
        ids: nfts.slice(i, i + batchSize).map((n) => n.positionId),
        options: { showContent: true },
      }),
    );
  }

  const allResults = (await Promise.all(batches)).flat();

  // Step 3: Parse position fields
  return allResults.map((obj): PositionInfo => {
    const objectId = unstable_getObjectId(obj);
    const fields = unstable_getObjectFields(obj) as unknown as NFT.PositionField;
    const nft = nfts.find((n) => n.positionId === objectId)!;
    return {
      ...fields,
      ...nft,
      objectId,
      tickLower: sdk.math.bitsToNumber(fields.tick_lower_index.fields.bits),
      tickUpper: sdk.math.bitsToNumber(fields.tick_upper_index.fields.bits),
    };
  });
}
```

**Key details:**
- NFT struct type filter: `{PackageIdOriginal}::position_nft::TurbosPositionNFT`
- Each NFT has `position_id` and `pool_id` fields linking to the actual position data
- Burned/locked positions use a different struct: `{PackageId}::position_manager::TurbosPositionBurnNFT`, with pool ID nested at `position_nft.fields.pool_id`
- Use `sdk.math.bitsToNumber(tick_index.fields.bits)` to convert tick index from on-chain I32 format

### getFields

```typescript
const fields = await sdk.position.getFields(nftId);
// Returns: { description, id, img_url, name, pool_id, position_id }
```

### getPositionFields

```typescript
const position = await sdk.position.getPositionFields(nftId);
// Returns: { liquidity, tick_lower_index, tick_upper_index,
//   fee_growth_inside_a/b, tokens_owed_a/b, reward_infos }
```

### getPositionFieldsByPositionId

```typescript
const position = await sdk.position.getPositionFieldsByPositionId(positionId);
```

### getPositionTick

```typescript
const tick = await sdk.position.getPositionTick(poolId, position.tick_lower_index);
// Returns: { tickIndex, initialized, liquidityNet, liquidityGross,
//   feeGrowthOutsideA, feeGrowthOutsideB, rewardGrowthsOutside }
```

### getPositionLiquidityUSD

```typescript
const usdValue = await sdk.position.getPositionLiquidityUSD({
  poolId,
  position,                   // PositionField
  priceA: '1.00',            // USD price of coin A
  priceB: '50000',           // USD price of coin B
});
```

### getUnclaimedFeesAndRewards

```typescript
const result = await sdk.position.getUnclaimedFeesAndRewards({
  poolId,
  position,
  getPrice: async (coinType) => getPriceForCoin(coinType),
});
// Returns: { fees, rewards, total, fields: { feeOwedA, feeOwedB, collectRewards, ... } }
```

### getUnclaimedFees

```typescript
const fees = await sdk.position.getUnclaimedFees({
  pool,
  position,
  tickLowerDetail,
  tickUpperDetail,
  getPrice: async (coinType) => getPriceForCoin(coinType),
});
// Returns: { feeOwedA, feeOwedB, unclaimedFees, scaledFeeOwedA, scaledFeeOwedB }
```

### getUnclaimedRewards

```typescript
const rewards = await sdk.position.getUnclaimedRewards({
  pool,
  position,
  tickLowerDetail,
  tickUpperDetail,
  getPrice: async (coinType) => getPriceForCoin(coinType),
});
// Returns: { unclaimedRewards, collectRewards, scaledCollectRewards }
```

### getPositionAPR

```typescript
const apr = await sdk.position.getPositionAPR({
  poolId,
  tickLower: -100,
  tickUpper: 100,
  fees24h: '1000',
  getPrice: async (coinType) => getPriceForCoin(coinType),
  liquidity: '1000000',  // Optional, defaults to pool liquidity
});
// Returns: { fees: string, rewards: string, total: string }
```

### burn

Burn a position NFT (must have 0 liquidity):

```typescript
const txb = await sdk.position.burn({
  pool: poolId,
  nft: positionNftId,
});
```

---

## Module: Account

Keypair and mnemonic utilities.

### generateMnemonic

```typescript
const mnemonic24 = sdk.account.generateMnemonic(24);   // 24 words (default)
const mnemonic12 = sdk.account.generateMnemonic(12);   // 12 words
```

### getKeypairFromMnemonics

```typescript
const keypair = sdk.account.getKeypairFromMnemonics(mnemonic, {
  accountIndex: 0,  // Optional, default 0
  isExternal: false, // Optional, default false
  addressIndex: 0,   // Optional, default 0
});
// Derive path: m/44'/784'/{accountIndex}'/{isExternal ? 1 : 0}'/{addressIndex}'
```

---

## Module: Math

Tick, price, and sqrt math utilities accessed via `sdk.math`.

### Key Methods

```typescript
// Tick ↔ SqrtPrice
const sqrtPriceX64: BN = sdk.math.tickIndexToSqrtPriceX64(tickIndex);
const tickIndex: number = sdk.math.sqrtPriceX64ToTickIndex(sqrtPriceX64);

// Tick ↔ Price (human-readable)
const price: Decimal = sdk.math.tickIndexToPrice(tickIndex, decimalsA, decimalsB);
const sqrtPriceX64: BN = sdk.math.priceToSqrtPriceX64(price, decimalsA, decimalsB);

// Bits (I32/I128) ↔ Number
const num: number = sdk.math.bitsToNumber(bits);           // I32
const num: number = sdk.math.bitsToNumber(bits, 128);      // I128

// Scale conversions
const scaled: string = sdk.math.scaleDown(amount, decimals);

// X64 fixed-point conversions
const x64: Decimal = sdk.math.toX64_Decimal(value);
const fromX64: Decimal = sdk.math.fromX64_Decimal(value);
```

---

## Key Types Reference

### Pool.Pool

```typescript
interface Pool {
  objectId: string;
  type: string;
  types: [coinTypeA: string, coinTypeB: string, feeType: string];
  coin_a: string;
  coin_b: string;
  fee: number;
  fee_protocol: number;
  liquidity: string;
  sqrt_price: string;
  tick_current_index: { type: string; fields: { bits: number } };
  tick_spacing: number;
  unlocked: boolean;
  max_liquidity_per_tick: string;
  fee_growth_global_a: string;
  fee_growth_global_b: string;
  protocol_fees_a: string;
  protocol_fees_b: string;
  reward_infos: {
    type: string;
    fields: {
      emissions_per_second: string;
      growth_global: string;
      manager: string;
      vault: string;
      vault_coin_type: string;
    };
  }[];
  deploy_time_ms: string;
  reward_last_updated_time_ms: string;
  tick_map: { type: string; fields: { id: { id: string }; size: string } };
}
```

### Trade.ComputedSwapResult

```typescript
interface ComputedSwapResult {
  a_to_b: boolean;
  amount_a: string;
  amount_b: string;
  fee_amount: string;
  is_exact_in: boolean;
  liquidity: string;
  pool: string;
  protocol_fee: string;
  recipient: string;
  sqrt_price: string;
  tick_current_index: { bits: number };
  tick_pre_index: { bits: number };
}
```

### Network Enum

```typescript
enum Network {
  mainnet = 'mainnet',
  testnet = 'testnet',
}
```

---

## Common Patterns

### Typical Swap Flow

```typescript
import { Network, TurbosSdk } from 'turbos-clmm-sdk';

const sdk = new TurbosSdk(Network.mainnet);

// 1. Compute swap result
const swapResults = await sdk.trade.computeSwapResult({
  pools: [{ pool: poolId, a2b: true }],
  address: walletAddress,
  amountSpecified: '1000000000',
  amountSpecifiedIsInput: true,
});

// 2. Build swap transaction
const txb = await sdk.trade.swap({
  routes: [{
    pool: poolId,
    a2b: true,
    nextTickIndex: sdk.math.bitsToNumber(swapResults[0].tick_current_index.bits),
  }],
  coinTypeA,
  coinTypeB,
  address: walletAddress,
  amountA: swapResults[0].amount_a,
  amountB: swapResults[0].amount_b,
  amountSpecifiedIsInput: true,
  slippage: '1',
});

// 3. Sign and execute
await suiClient.signAndExecuteTransaction({ transaction: txb, signer: keypair });
```

### Typical Liquidity Addition Flow

```typescript
// 1. Get fee tier
const fee = await sdk.contract.getFee(60);

// 2. Estimate amounts from one side
const [amountA, amountB] = sdk.pool.estimateAmountsFromOneAmount({
  sqrtPrice: pool.sqrt_price,
  tickLower,
  tickUpper,
  amount: '1000000000',
  isAmountA: true,
});

// 3. Add liquidity (opens new position)
const txb = await sdk.pool.addLiquidity({
  pool: poolId,
  address: walletAddress,
  amountA,
  amountB,
  tickLower,
  tickUpper,
  slippage: '5',
});

// 4. Sign and execute
await suiClient.signAndExecuteTransaction({ transaction: txb, signer: keypair });
```

---

## Package Reference

| Package | npm | Purpose |
|---------|-----|---------|
| CLMM SDK | `turbos-clmm-sdk` | Concentrated liquidity AMM (pools, positions, swaps) |
| Peer Dep | `@mysten/sui` | Sui blockchain client |
