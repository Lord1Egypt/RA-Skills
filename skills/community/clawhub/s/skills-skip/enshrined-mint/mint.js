#!/usr/bin/env node
/**
 * Enshrined Exchange - Mint/Swap/Check Balance (Tempo DEX)
 *
 * Network:  Tempo (Chain 4217)
 * RPC:      https://rpc.moderato.tempo.xyz
 * Explorer: https://explorer.tempo.xyz
 *
 * Key Contracts:
 *   Stablecoin DEX:  0xdec0000000000000000000000000000000000000
 *   pathUSD:         0x20c0000000000000000000000000000000000000
 *   ENSH:            0x20c00000000000000000000031d99efa5dbd3713
 *   ENSH Mint:       0x3ba0a6d270f7dd69964f67219288f8cedfab54bc
 *
 * Usage:
 *   PRIVATE_KEY=0x... node mint.js --action swap --amount 3600 --from pathUSD --to ENSH
 *   PRIVATE_KEY=0x... node mint.js --action balance
 *   PRIVATE_KEY=0x... node mint.js --action mint-ensh --amount 100 --source pathUSD
 *
 * Docs: https://docs.tempo.xyz/protocol/exchange/spec
 */

const { ethers } = require('ethers');
const args = require('minimist')(process.argv.slice(2));

const RPC = 'https://rpc.moderato.tempo.xyz';

// Contracts
const DEX = '0xdec0000000000000000000000000000000000000';
const ENSH_MINT = '0x3ba0a6d270f7dd69964f67219288f8cedfab54bc';

const TOKENS = {
  pathUSD: '0x20c0000000000000000000000000000000000000',
  ENSH:    '0x20c00000000000000000031d99efa5dbd3713',
};

const DECIMALS = { pathUSD: 6, ENSH: 18 };
const EXPLORER = 'https://explorer.tempo.xyz/tx';

// ─── Stablecoin DEX ABI (from docs.tempo.xyz) ─────────────────────────────────
const DEX_ABI = [
  // Constants
  'function PRICE_SCALE() external view returns (uint32)',
  'function TICK_SPACING() external view returns (int16)',
  'function MIN_TICK() external view returns (int16)',
  'function MAX_TICK() external view returns (int16)',
  // Balances
  'function balanceOf(address user, address token) external view returns (uint128)',
  'function withdraw(address token, uint128 amount) external',
  // Swaps
  'function swapExactAmountIn(address tokenIn, address tokenOut, uint128 amountIn, uint128 minAmountOut) external returns (uint128 amountOut)',
  'function swapExactAmountOut(address tokenIn, address tokenOut, uint128 amountOut, uint128 maxAmountIn) external returns (uint128 amountIn)',
  'function quoteSwapExactAmountIn(address tokenIn, address tokenOut, uint128 amountIn) external view returns (uint128 amountOut)',
  'function quoteSwapExactAmountOut(address tokenIn, address tokenOut, uint128 amountOut) external view returns (uint128 amountIn)',
  // Orders
  'function place(address token, uint128 amount, bool isBid, int16 tick) external returns (uint128 orderId)',
  'function cancel(uint128 orderId) external',
  // Books
  'function pairKey(address tokenA, address tokenB) external pure returns (bytes32 key)',
  'function books(bytes32 pairKey) external view returns (address base, address quote, int16 bestBidTick, int16 bestAskTick)',
];

// ERC-20 ABI
const ERC20_ABI = [
  'function balanceOf(address) view returns (uint256)',
  'function decimals() view returns (uint8)',
  'function symbol() view returns (string)',
  'function approve(address spender, uint256 amount) returns (bool)',
  'function allowance(address owner, address spender) view returns (uint256)',
  'function transfer(address to, uint256 amount) returns (bool)',
  'function transferFrom(address from, address to, uint256 amount) returns (bool)',
];

// ENSH Mint contract ABI (unknown - probing)
const MINT_ABI = [
  'function mint(address to, uint256 amount)',
  'function deposit(uint256 amount)',
  'function swap(uint256 amount)',
  'function enter(address token, uint256 amount)',
  'function buy(address token, uint256 amount)',
];

function parseAmount(amount, symbol) {
  const dec = DECIMALS[symbol] || 18;
  return ethers.parseUnits(amount.toString(), dec);
}

function formatAmount(amount, symbol) {
  const dec = DECIMALS[symbol] || 18;
  return ethers.formatUnits(amount, dec);
}

async function getBalance(contract, address) {
  try {
    return await contract.balanceOf(address);
  } catch { return 0n; }
}

async function actionBalance(wallet, tokenSymbol) {
  const tokenAddr = TOKENS[tokenSymbol];
  if (!tokenAddr) throw new Error(`Unknown token: ${tokenSymbol}`);

  // ERC20 wallet balance
  const token = new ethers.Contract(tokenAddr, ERC20_ABI, wallet);
  const bal = await getBalance(token, wallet.address);
  console.log(`  ${tokenSymbol} (wallet): ${formatAmount(bal, tokenSymbol)}`);

  // DEX internal balance
  const dex = new ethers.Contract(DEX, DEX_ABI, wallet);
  try {
    const dexBal = await dex.balanceOf(wallet.address, tokenAddr);
    console.log(`  ${tokenSymbol} (DEX):   ${formatAmount(dexBal, tokenSymbol)}`);
  } catch { /* skip */ }
}

async function actionSwap(wallet, amount, fromToken, toToken) {
  const src = fromToken.toUpperCase();
  const dst = toToken.toUpperCase();
  const srcAddr = TOKENS[fromToken];
  const dstAddr = TOKENS[toToken];

  if (!srcAddr) throw new Error(`Unknown token: ${fromToken}`);
  if (!dstAddr) throw new Error(`Unknown token: ${toToken}`);
  if (src === dst) throw new Error('From and To cannot be the same');

  const amountIn = parseAmount(amount, fromToken);
  const dex = new ethers.Contract(DEX, DEX_ABI, wallet);
  const token = new ethers.Contract(srcAddr, ERC20_ABI, wallet);

  // Step 1: Check wallet balance
  console.log(`\n📋 Step 1: Check ${fromToken} balance`);
  const walletBal = await getBalance(token, wallet.address);
  console.log(`  Wallet: ${formatAmount(walletBal, fromToken)}`);
  if (walletBal < amountIn) throw new Error(`Insufficient ${fromToken} balance`);

  // Step 2: Check DEX internal balance
  console.log(`\n📋 Step 2: Check DEX internal balance`);
  try {
    const dexBal = await dex.balanceOf(wallet.address, srcAddr);
    console.log(`  DEX internal: ${formatAmount(dexBal, fromToken)}`);
    console.log(`  Note: DEX uses internal balances — use withdraw() to pull funds out`);
  } catch { /* skip */ }

  // Step 3: Approve DEX to spend token
  console.log(`\n📋 Step 3: Approve DEX to spend ${fromToken}`);
  const currentAllow = await token.allowance(wallet.address, DEX).catch(() => 0n);
  if (currentAllow < amountIn) {
    const approveTx = await token.approve(DEX, ethers.MaxUint256);
    await approveTx.wait();
    console.log('  ✅ Approved');
  } else {
    console.log('  ✅ Already approved');
  }

  // Step 4: Get a quote first
  console.log(`\n📋 Step 4: Quote`);
  try {
    const quote = await dex.quoteSwapExactAmountIn(srcAddr, dstAddr, amountIn);
    console.log(`  Expected output: ${formatAmount(quote, toToken)} ${toToken}`);
  } catch(e) {
    console.log(`  ⚠️  Quote failed: ${e.message.slice(0,80)}`);
  }

  // Step 5: Execute swap
  console.log(`\n📋 Step 5: Swap ${amount} ${fromToken} → ${toToken}`);
  try {
    const swapTx = await dex.swapExactAmountIn(srcAddr, dstAddr, amountIn, 0n);
    const receipt = await swapTx.wait();
    console.log(`\n✅ SWAP SUCCESSFUL`);
    console.log(`  TX: ${EXPLORER}/${swapTx.hash}`);
    console.log(`  Gas used: ${receipt.gasUsed.toString()}`);
  } catch(e) {
    // Try swapExactAmountOut as fallback
    console.log(`  swapExactAmountIn failed, trying swapExactAmountOut...`);
    const swapTx = await dex.swapExactAmountOut(srcAddr, dstAddr, amountIn, ethers.MaxUint256);
    const receipt = await swapTx.wait();
    console.log(`\n✅ SWAP SUCCESSFUL`);
    console.log(`  TX: ${EXPLORER}/${swapTx.hash}`);
  }

  // Final balances
  const finalSrc = await getBalance(token, wallet.address);
  const dexDst = await dex.balanceOf(wallet.address, dstAddr).catch(() => 0n);
  console.log(`\n📊 Final`);
  console.log(`  ${fromToken} (wallet): ${formatAmount(finalSrc, fromToken)}`);
  console.log(`  ${toToken} (DEX):     ${formatAmount(dexDst, toToken)}`);
}

async function actionMintENSH(wallet, amount, sourceToken) {
  const src = sourceToken.toUpperCase();
  const srcAddr = TOKENS[sourceToken];
  if (!srcAddr) throw new Error(`Unknown token: ${sourceToken}`);
  if (src === 'ENSH') throw new Error('Source must be a stablecoin for minting');

  const amountIn = parseAmount(amount, sourceToken);
  const token = new ethers.Contract(srcAddr, ERC20_ABI, wallet);
  const mint = new ethers.Contract(ENSH_MINT, MINT_ABI, wallet);

  // Check balance
  console.log(`\n📋 Step 1: Check ${sourceToken} balance`);
  const bal = await getBalance(token, wallet.address);
  console.log(`  Balance: ${formatAmount(bal, sourceToken)}`);
  if (bal < amountIn) throw new Error(`Insufficient ${sourceToken}`);

  // Approve mint contract
  console.log(`\n📋 Step 2: Approve mint contract`);
  const currentAllow = await token.allowance(wallet.address, ENSH_MINT).catch(() => 0n);
  if (currentAllow < amountIn) {
    const approveTx = await token.approve(ENSH_MINT, ethers.MaxUint256);
    await approveTx.wait();
    console.log('  ✅ Approved');
  } else {
    console.log('  ✅ Already approved');
  }

  // Try mint functions
  console.log(`\n📋 Step 3: Mint ENSH`);

  // Try each mint function
  const mintFns = [
    { name: 'mint(address,uint256)', fn: 'mint', args: [wallet.address, amountIn] },
    { name: 'swap(uint256)', fn: 'swap', args: [amountIn] },
    { name: 'enter(address,uint256)', fn: 'enter', args: [srcAddr, amountIn] },
    { name: 'buy(address,uint256)', fn: 'buy', args: [srcAddr, amountIn] },
    { name: 'deposit(uint256)', fn: 'deposit', args: [amountIn] },
  ];

  let success = false;
  for (const mintFn of mintFns) {
    try {
      console.log(`  Trying ${mintFn.name}...`);
      const tx = await mint[mintFn.fn](...mintFn.args);
      const receipt = await tx.wait();
      console.log(`\n✅ MINT SUCCESSFUL (${mintFn.name})`);
      console.log(`  TX: ${EXPLORER}/${tx.hash}`);
      success = true;
      break;
    } catch(e) {
      if (e.message.includes('execution reverted')) {
        console.log(`    ✗ ${mintFn.name} reverted`);
      } else {
        console.log(`    ✗ ${mintFn.name} error: ${e.message.slice(0,60)}`);
      }
    }
  }

  if (!success) {
    console.log('\n⚠️  Mint functions not confirmed. Check explorer for correct ABI.');
  }
}

async function main() {
  const privateKey = process.env.PRIVATE_KEY;
  const action = (args.action || 'balance').toLowerCase();
  const amount = parseFloat(args.amount) || 0;
  const fromToken = args.from || 'pathUSD';
  const toToken = args.to || 'ENSH';
  const sourceToken = args.source || 'pathUSD';

  if (!privateKey) {
    console.error('❌ PRIVATE_KEY not set\n');
    console.error('Usage:');
    console.error('  Swap:    PRIVATE_KEY=0x... node mint.js --action swap --amount 3600 --from pathUSD --to ENSH');
    console.error('  Balance: PRIVATE_KEY=0x... node mint.js --action balance');
    console.error('  Mint:    PRIVATE_KEY=0x... node mint.js --action mint-ensh --amount 100 --source pathUSD');
    console.error('\nTokens: pathUSD, ENSH');
    process.exit(1);
  }

  const provider = new ethers.JsonRpcProvider(RPC);
  const wallet = new ethers.Wallet(privateKey, provider);

  console.log('');
  console.log('🔷 ENSHRIINED.EXCHANGE');
  console.log('═══════════════════════════════════════════════');
  console.log(`  Network:  Tempo (Chain 4217)`);
  console.log(`  RPC:      ${RPC}`);
  console.log(`  Wallet:   ${wallet.address}`);
  console.log(`  Action:   ${action}`);

  try {
    if (action === 'balance') {
      console.log('\n📊 Token Balances');
      for (const t of Object.keys(TOKENS)) {
        await actionBalance(wallet, t);
      }
    } else if (action === 'swap') {
      if (!amount) throw new Error('--amount required');
      await actionSwap(wallet, amount, fromToken, toToken);
    } else if (action === 'mint-ensh') {
      if (!amount) throw new Error('--amount required');
      await actionMintENSH(wallet, amount, sourceToken);
    } else {
      throw new Error(`Unknown action: ${action}`);
    }
  } catch (err) {
    console.error(`\n❌ Error: ${err.message || err}`);
    process.exit(1);
  }
}

main();
