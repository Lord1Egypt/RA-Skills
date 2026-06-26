#!/usr/bin/env node
/**
 * spandex_trade.mjs — spanDEX Meta-Aggregator trading script for Base chain
 * 
 * Usage:
 *   node spandex_trade.mjs quote    --sell TOKEN --buy TOKEN --amount 1.5 [--strategy bestPrice|fastest|estimatedGas|priority]
 *   node spandex_trade.mjs swap     --sell TOKEN --buy TOKEN --amount 1.5 [--slippage 300] [--strategy bestPrice] [--dry-run]
 *   node spandex_trade.mjs balance  [--token TOKEN]
 *   node spandex_trade.mjs providers                           # list configured providers
 *   node spandex_trade.mjs limit    --sell TOKEN --buy TOKEN --sell-amount 1.5 --buy-amount 5.0 [--expiry 14d]
 *   node spandex_trade.mjs orders   [--status active|filled|cancelled]
 *   node spandex_trade.mjs cancel-order --order-id 123
 * 
 * TOKEN can be: contract address, or alias (USDC, WETH, ETH)
 * Amounts are in human-readable form (1.5 = 1.5 tokens)
 * All output is JSON for easy parsing
 * 
 * Env vars:
 *   BASE_RPC_URL         — Alchemy/Infura RPC (default: Alchemy)
 *   SPANDEX_APP_ID       — Fabric app ID (default: moltino-trader)
 *   SPANDEX_STRATEGY     — default quote strategy (default: bestPrice)
 *   SPANDEX_PRIORITY_GWEI — priority fee floor in gwei (default: 0.03)
 *   SPANDEX_SKIP_LOCK    — skip anti-double-execution lock (1 = skip)
 */

import { createPublicClient, createWalletClient, http, formatUnits, parseUnits, parseGwei, erc20Abi } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { base } from 'viem/chains';
import {
  createConfig,
  fabric,
  kyberswap,
  odos,
  velora,
  lifi,
  relay,
  getQuotes,
  selectQuote,
  getPricing,
  buildCalls,
  netOutputs,
  sortQuotesByPerformance,
} from '@spandex/core';
import fs from 'fs';
import path from 'path';

// ─── Config ───────────────────────────────────────────────────────────────────

const KEY_PATH = process.env.SPANDEX_KEY_PATH || null;
const RPC_URL = process.env.BASE_RPC_URL;
if (!RPC_URL) die('BASE_RPC_URL env var required (e.g. Alchemy, Infura, or public RPC)');
const APP_ID = process.env.SPANDEX_APP_ID || 'spandex-trader-skill';
const DEFAULT_STRATEGY = process.env.SPANDEX_STRATEGY || 'bestPrice';

// Priority fee floor (gwei) — Base OP Stack sequencer orders by priority fee.
// 0.03 gwei = "instant" tier (~$0.02-0.05 per swap). Configurable via env.
const PRIORITY_FEE_GWEI = process.env.SPANDEX_PRIORITY_GWEI || '0.03';
const MIN_PRIORITY_FEE = parseGwei(PRIORITY_FEE_GWEI);

// Token aliases (Base chain)
const TOKEN_ALIASES = {
  'USDC':  { address: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913', decimals: 6 },
  'USDT':  { address: '0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2', decimals: 6 },
  'DAI':   { address: '0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb', decimals: 18 },
  'WETH':  { address: '0x4200000000000000000000000000000000000006', decimals: 18 },
  'ETH':   { address: '0x4200000000000000000000000000000000000006', decimals: 18 },
};

// ─── Lockfile (anti-double-execution) ─────────────────────────────────────────

const LOCKDIR = '/tmp/spandex_locks';
const COOLDOWN_S = 120;

function checkLock(tokenAddress) {
  if (process.env.SPANDEX_SKIP_LOCK === '1') return;
  const lockFile = path.join(LOCKDIR, tokenAddress.toLowerCase());
  if (fs.existsSync(lockFile)) {
    const lockAge = Math.floor(Date.now() / 1000) - Math.floor(fs.statSync(lockFile).mtimeMs / 1000);
    if (lockAge < COOLDOWN_S) {
      die(`trade locked — previous trade ${lockAge}s ago (cooldown: ${COOLDOWN_S}s)`);
    }
  }
}

function setLock(tokenAddress) {
  fs.mkdirSync(LOCKDIR, { recursive: true });
  fs.writeFileSync(path.join(LOCKDIR, tokenAddress.toLowerCase()), new Date().toISOString());
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function loadPrivateKey() {
  // Priority: SPANDEX_PRIVATE_KEY (raw hex) > SPANDEX_KEY_PATH (file path)
  const rawKey = process.env.SPANDEX_PRIVATE_KEY;
  if (rawKey) return rawKey.startsWith('0x') ? rawKey : `0x${rawKey}`;
  if (KEY_PATH) {
    try {
      return fs.readFileSync(KEY_PATH, 'utf8').trim();
    } catch (e) {
      die(`Cannot read private key from ${KEY_PATH}: ${e.message}`);
    }
  }
  die('Set SPANDEX_PRIVATE_KEY (hex) or SPANDEX_KEY_PATH (file) env var');
}

function resolveToken(input) {
  if (!input) die('Token not specified');
  const upper = input.toUpperCase();
  if (TOKEN_ALIASES[upper]) return { ...TOKEN_ALIASES[upper], alias: upper };
  if (input.startsWith('0x') && input.length === 42) {
    return { address: input, decimals: null, alias: null };
  }
  die(`Unknown token: ${input}. Use a contract address or alias (USDC, WETH, ETH, DAI, USDT)`);
}

async function getTokenDecimals(client, address) {
  try {
    return Number(await client.readContract({ address, abi: erc20Abi, functionName: 'decimals' }));
  } catch (e) {
    die(`Cannot read decimals for ${address}: ${e.message}`);
  }
}

async function getTokenSymbol(client, address) {
  try {
    return await client.readContract({ address, abi: erc20Abi, functionName: 'symbol' });
  } catch {
    return 'UNKNOWN';
  }
}

async function getTokenBalance(client, tokenAddress, walletAddress) {
  if (tokenAddress.toLowerCase() === '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee') {
    return await client.getBalance({ address: walletAddress });
  }
  return await client.readContract({
    address: tokenAddress, abi: erc20Abi, functionName: 'balanceOf', args: [walletAddress],
  });
}

function getSlippageBps(args, sellAddress, buyAddress) {
  if (args.slippage) return parseInt(args.slippage);
  const majorTokens = Object.values(TOKEN_ALIASES).map(t => t.address.toLowerCase());
  const isMajorSell = majorTokens.includes(sellAddress.toLowerCase());
  const isMajorBuy = majorTokens.includes(buyAddress.toLowerCase());
  if (!isMajorSell && !isMajorBuy) return 500;    // 5% microcap↔microcap
  if (!isMajorSell || !isMajorBuy) return 300;    // 3% major↔microcap
  return 50;                                        // 0.5% major↔major
}

function parseArgs(argv) {
  const args = {};
  const positional = [];
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith('--')) {
      const key = argv[i].slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith('--')) { args[key] = next; i++; }
      else { args[key] = true; }
    } else {
      positional.push(argv[i]);
    }
  }
  return { action: positional[0], ...args };
}

function out(data) {
  console.log(JSON.stringify(data, (_, v) => typeof v === 'bigint' ? v.toString() : v, 2));
}

function die(msg) {
  console.error(JSON.stringify({ error: msg }));
  process.exit(1);
}

// ─── Gas pricing ──────────────────────────────────────────────────────────────

async function getGasParams(publicClient) {
  const block = await publicClient.getBlock({ blockTag: 'latest' });
  const baseFee = block.baseFeePerGas || 0n;
  const priorityFee = MIN_PRIORITY_FEE;
  return {
    maxFeePerGas: baseFee * 2n + priorityFee,
    maxPriorityFeePerGas: priorityFee,
  };
}

// ─── Setup ────────────────────────────────────────────────────────────────────

function createSetup() {
  const pk = loadPrivateKey();
  const account = privateKeyToAccount(pk);

  const publicClient = createPublicClient({ chain: base, transport: http(RPC_URL) });
  const walletClient = createWalletClient({ chain: base, transport: http(RPC_URL), account });

  // spanDEX config: 6 free providers (no API keys needed)
  const spandexConfig = createConfig({
    providers: [
      fabric({ appId: APP_ID }),
      kyberswap({ clientId: APP_ID }),
      odos({}),
      velora({}),
      lifi({}),
      relay({}),
    ],
    options: {
      deadlineMs: 15_000,
      numRetries: 1,
    },
    clients: [publicClient],
    logging: process.env.SPANDEX_DEBUG ? { level: 'debug' } : undefined,
  });

  return { publicClient, walletClient, account, spandexConfig };
}

// ─── Resolve token info (decimals + symbol) ───────────────────────────────────

async function resolveTokenInfo(publicClient, input) {
  const info = resolveToken(input);
  if (!info.decimals) info.decimals = await getTokenDecimals(publicClient, info.address);
  info.symbol = info.alias || await getTokenSymbol(publicClient, info.address);
  return info;
}

// ─── Actions ──────────────────────────────────────────────────────────────────

async function actionQuote(args) {
  if (!args.sell || !args.buy || !args.amount) {
    die('Usage: quote --sell TOKEN --buy TOKEN --amount 1.5 [--strategy bestPrice|fastest|estimatedGas|priority]');
  }

  const { publicClient, account, spandexConfig } = createSetup();
  const sellInfo = await resolveTokenInfo(publicClient, args.sell);
  const buyInfo = await resolveTokenInfo(publicClient, args.buy);

  const inputAmount = parseUnits(args.amount, sellInfo.decimals);
  const slippageBps = getSlippageBps(args, sellInfo.address, buyInfo.address);
  const strategy = args.strategy || DEFAULT_STRATEGY;

  const swapParams = {
    chainId: 8453,
    inputToken: sellInfo.address,
    outputToken: buyInfo.address,
    mode: 'exactIn',
    inputAmount,
    slippageBps,
    swapperAccount: account.address,
  };

  // Single fetch: get all simulated quotes, then select winner from same set
  const quotePromises = await getQuotes({ config: spandexConfig, swap: swapParams });
  const allQuotes = await Promise.allSettled(quotePromises);

  const resolvedQuotes = allQuotes
    .filter(r => r.status === 'fulfilled' && r.value)
    .map(r => r.value);

  // Provider comparison
  const providerResults = resolvedQuotes.map(q => ({
    provider: q.provider,
    success: q.success,
    simulationSuccess: q.simulation?.success ?? false,
    outputAmount: q.success && q.simulation?.success
      ? formatUnits(q.simulation.outputAmount, buyInfo.decimals) : null,
    gasUsed: q.simulation?.gasUsed?.toString() ?? null,
    latencyMs: q.latency ? Math.round(q.latency) : null,
    error: !q.success ? (q.error?.message || 'quote failed') : null,
  }));

  // USD pricing from provider metadata
  const pricing = getPricing(resolvedQuotes);

  // Select winner using library's selectQuote (same data, no re-fetch)
  const successQuotes = resolvedQuotes.filter(q => q.success && q.simulation?.success);
  const winner = successQuotes.length > 0
    ? await selectQuote({ strategy, quotes: successQuotes.map(q => Promise.resolve(q)) })
    : null;

  out({
    action: 'quote',
    sellToken: sellInfo.address,
    sellSymbol: sellInfo.symbol,
    buyToken: buyInfo.address,
    buySymbol: buyInfo.symbol,
    inputAmount: args.amount,
    slippageBps,
    strategy,
    winner: winner ? {
      provider: winner.provider,
      outputAmount: formatUnits(winner.simulation.outputAmount, buyInfo.decimals),
      gasUsed: winner.simulation.gasUsed?.toString() ?? null,
    } : null,
    pricing: pricing.inputToken || pricing.outputToken ? {
      inputUsd: pricing.inputToken?.usdPrice ?? null,
      outputUsd: pricing.outputToken?.usdPrice ?? null,
    } : null,
    providers: providerResults,
    wallet: account.address,
  });
}

async function actionSwap(args) {
  if (!args.sell || !args.buy || !args.amount) {
    die('Usage: swap --sell TOKEN --buy TOKEN --amount 1.5 [--slippage 300] [--strategy bestPrice] [--dry-run]');
  }

  const { publicClient, walletClient, account, spandexConfig } = createSetup();
  const sellInfo = await resolveTokenInfo(publicClient, args.sell);
  const buyInfo = await resolveTokenInfo(publicClient, args.buy);

  // Anti-double-execution lock
  const majorTokens = Object.values(TOKEN_ALIASES).map(t => t.address.toLowerCase());
  const tradedToken = !majorTokens.includes(sellInfo.address.toLowerCase()) ? sellInfo.address
    : !majorTokens.includes(buyInfo.address.toLowerCase()) ? buyInfo.address : null;
  if (tradedToken) checkLock(tradedToken);

  const inputAmount = parseUnits(args.amount, sellInfo.decimals);
  const slippageBps = getSlippageBps(args, sellInfo.address, buyInfo.address);
  const strategy = args.strategy || DEFAULT_STRATEGY;

  // Check balance
  const balance = await getTokenBalance(publicClient, sellInfo.address, account.address);
  if (balance < inputAmount) {
    die(`Insufficient balance: have ${formatUnits(balance, sellInfo.decimals)} ${sellInfo.symbol}, need ${args.amount}`);
  }

  const swapParams = {
    chainId: 8453,
    inputToken: sellInfo.address,
    outputToken: buyInfo.address,
    mode: 'exactIn',
    inputAmount,
    slippageBps,
    swapperAccount: account.address,
  };

  out({ status: 'quoting', sell: `${args.amount} ${sellInfo.symbol}`, buy: buyInfo.symbol, slippageBps, strategy });

  // Fetch all simulated quotes
  const quotePromises = await getQuotes({ config: spandexConfig, swap: swapParams });
  const allQuotes = await Promise.allSettled(quotePromises);
  const validQuotes = allQuotes
    .filter(r => r.status === 'fulfilled' && r.value?.success && r.value?.simulation?.success)
    .map(r => r.value);

  if (validQuotes.length === 0) {
    die('No provider returned a successful quote. All aggregators failed or timed out.');
  }

  // Sort by simulated output (best price first) using library
  const sorted = sortQuotesByPerformance({ quotes: validQuotes, metric: 'outputAmount', ascending: false });
  const topQuote = sorted[0];
  const outputFormatted = formatUnits(topQuote.simulation.outputAmount, buyInfo.decimals);

  out({
    status: 'quoted',
    provider: topQuote.provider,
    outputAmount: outputFormatted,
    gasUsed: topQuote.simulation.gasUsed?.toString() ?? null,
    fallbackProviders: sorted.slice(1).map(q => q.provider),
  });

  // Dry run
  if (args['dry-run']) {
    out({
      action: 'swap', status: 'dry-run', provider: topQuote.provider,
      sellToken: sellInfo.address, sellSymbol: sellInfo.symbol,
      buyToken: buyInfo.address, buySymbol: buyInfo.symbol,
      inputAmount: args.amount, outputAmount: outputFormatted,
      slippageBps, wallet: account.address,
    });
    return;
  }

  // Set lock before execution
  if (tradedToken) setLock(tradedToken);

  // ── Execute with fallback ──
  // Try each provider in order of best price. Uses spanDEX buildCalls for proper
  // V4/Clanker/DERC20 compatibility (walletClient handles account context correctly).

  let result = null;
  const gasParams = await getGasParams(publicClient);

  for (const quote of sorted) {
    try {
      // Build calls via library — handles approval + swap for all pool types
      const calls = await buildCalls({
        quote, swap: swapParams, config: spandexConfig, publicClient,
        allowanceMode: 'unlimited',
      });

      out({ status: 'executing', provider: quote.provider, priorityFeeGwei: PRIORITY_FEE_GWEI, calls: calls.length });

      // Execute each call (approval if needed, then swap)
      let swapReceipt = null;
      for (const call of calls) {
        if (call.type === 'approval') {
          out({ status: 'approving', token: sellInfo.address, spender: call.txn.to });
        }
        const hash = await walletClient.sendTransaction({ ...call.txn, ...gasParams });
        const receipt = await publicClient.waitForTransactionReceipt({ hash });
        if (receipt.status !== 'success') {
          throw new Error(`${call.type} reverted: ${hash}`);
        }
        if (call.type === 'approval') {
          out({ status: 'approved', txHash: hash });
        }
        if (call.type === 'swap') {
          swapReceipt = receipt;
        }
      }

      result = {
        transactionHash: swapReceipt.transactionHash,
        provider: quote.provider,
        outputFormatted: formatUnits(quote.simulation.outputAmount, buyInfo.decimals),
        receipt: swapReceipt,
      };
      break;

    } catch (e) {
      out({
        status: 'fallback',
        failedProvider: quote.provider,
        reason: e.message?.slice(0, 120) || 'unknown error',
        tryingNext: sorted.indexOf(quote) < sorted.length - 1,
      });
      continue;
    }
  }

  if (!result) {
    die('All providers failed execution. Check token compatibility and slippage.');
  }

  // Post-execution: extract actual output from TX logs via netOutputs
  let actualOutput = result.outputFormatted;  // fallback to simulated
  try {
    const allocations = netOutputs({ swap: swapParams, logs: result.receipt.logs });
    const outputMap = allocations.outputToken;
    const swapperOutput = outputMap.get(account.address.toLowerCase());
    if (swapperOutput && swapperOutput > 0n) {
      actualOutput = formatUnits(swapperOutput, buyInfo.decimals);
    }
  } catch {
    // netOutputs is experimental — fall back to simulated amount silently
  }

  // Also read final balance for verification
  const newBalance = await getTokenBalance(publicClient, buyInfo.address, account.address);

  out({
    action: 'swap',
    status: 'executed',
    provider: result.provider,
    transactionHash: result.transactionHash,
    sellToken: sellInfo.address,
    sellSymbol: sellInfo.symbol,
    buyToken: buyInfo.address,
    buySymbol: buyInfo.symbol,
    inputAmount: args.amount,
    outputAmount: actualOutput,
    simulatedOutput: result.outputFormatted,
    newBuyBalance: formatUnits(newBalance, buyInfo.decimals),
    slippageBps,
    strategy,
    wallet: account.address,
    explorer: `https://basescan.org/tx/${result.transactionHash}`,
  });
}

async function actionBalance(args) {
  const { publicClient, account } = createSetup();

  if (args.token) {
    const tokenInfo = await resolveTokenInfo(publicClient, args.token);
    const balance = await getTokenBalance(publicClient, tokenInfo.address, account.address);
    out({
      action: 'balance', wallet: account.address,
      token: tokenInfo.address, symbol: tokenInfo.symbol,
      balance: formatUnits(balance, tokenInfo.decimals),
      balanceRaw: balance.toString(),
    });
  } else {
    const ethBalance = await publicClient.getBalance({ address: account.address });
    const balances = [{
      symbol: 'ETH (native)', address: 'native',
      balance: formatUnits(ethBalance, 18),
    }];
    for (const [name, info] of Object.entries(TOKEN_ALIASES)) {
      if (name === 'ETH' || name === 'DAI' || name === 'USDT') continue;
      const bal = await getTokenBalance(publicClient, info.address, account.address);
      balances.push({ symbol: name, address: info.address, balance: formatUnits(bal, info.decimals) });
    }
    out({ action: 'balance', wallet: account.address, balances });
  }
}

async function actionProviders() {
  const providers = [
    { name: 'Fabric', factory: 'fabric', apiKey: false, fee: '0-0.1%', notes: 'Built by spanDEX team' },
    { name: 'KyberSwap', factory: 'kyberswap', apiKey: false, fee: '0%', notes: 'Uniswap V4 support' },
    { name: 'Odos', factory: 'odos', apiKey: false, fee: '0.03%', notes: 'Multi-hop routing' },
    { name: 'Velora', factory: 'velora', apiKey: false, fee: '15% of integrator fee', notes: 'MEV protection' },
    { name: 'LI.FI', factory: 'lifi', apiKey: false, fee: '0.25%', notes: 'Cross-chain capable' },
    { name: 'Relay', factory: 'relay', apiKey: false, fee: 'varies', notes: 'Cross-chain, intent-based' },
  ];
  out({ action: 'providers', count: providers.length, providers });
}

// ─── KyberSwap Limit Order API ────────────────────────────────────────────────

const KYBER_LO_DOMAIN = 'https://limit-order.kyberswap.com';
const KYBER_LO_CONTRACT = '0xcab2FA2eeab7065B45CBcF6E3936dDE2506b4f6C'; // Base

function parseExpiry(expiryStr) {
  if (!expiryStr) return Math.floor(Date.now() / 1000) + 86400 * 14;
  const match = expiryStr.match(/^(\d+)(m|h|d)$/);
  if (!match) die(`Invalid expiry format: ${expiryStr}. Use: 30m, 24h, 7d`);
  const [, num, unit] = match;
  const multiplier = { m: 60, h: 3600, d: 86400 }[unit];
  return Math.floor(Date.now() / 1000) + parseInt(num) * multiplier;
}

async function actionLimit(args) {
  if (!args.sell || !args.buy || !args['sell-amount'] || !args['buy-amount']) {
    die('Usage: limit --sell TOKEN --buy TOKEN --sell-amount 1.5 --buy-amount 5.0 [--expiry 14d]');
  }

  const { publicClient, walletClient, account } = createSetup();
  const sellInfo = await resolveTokenInfo(publicClient, args.sell);
  const buyInfo = await resolveTokenInfo(publicClient, args.buy);

  const makingAmount = parseUnits(args['sell-amount'], sellInfo.decimals).toString();
  const takingAmount = parseUnits(args['buy-amount'], buyInfo.decimals).toString();
  const expiredAt = parseExpiry(args.expiry);
  const gasParams = await getGasParams(publicClient);

  // Check + handle approval to KyberSwap LO contract
  const maxUint = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFn;
  const activeMakingRes = await fetch(
    `${KYBER_LO_DOMAIN}/read-ks/api/v1/orders/active-making-amount?chainId=8453&makerAsset=${sellInfo.address}&maker=${account.address}`
  ).then(r => r.json());
  const currentMakingAmount = BigInt(activeMakingRes?.data?.activeMakingAmount || '0');
  const totalNeeded = currentMakingAmount + BigInt(makingAmount);

  const allowance = await publicClient.readContract({
    address: sellInfo.address, abi: erc20Abi, functionName: 'allowance',
    args: [account.address, KYBER_LO_CONTRACT],
  });

  if (allowance < totalNeeded) {
    out({ status: 'approving', token: sellInfo.address, spender: KYBER_LO_CONTRACT });
    const approveHash = await walletClient.writeContract({
      address: sellInfo.address, abi: erc20Abi, functionName: 'approve',
      args: [KYBER_LO_CONTRACT, maxUint], ...gasParams,
    });
    await publicClient.waitForTransactionReceipt({ hash: approveHash });
    out({ status: 'approved', txHash: approveHash });
  }

  // Get unsigned EIP712 message
  const unsignedBody = {
    chainId: '8453', makerAsset: sellInfo.address, takerAsset: buyInfo.address,
    maker: account.address, makingAmount, takingAmount, expiredAt,
  };

  const signMsgRes = await fetch(`${KYBER_LO_DOMAIN}/write/api/v1/orders/sign-message`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(unsignedBody),
  }).then(r => r.json());

  if (signMsgRes.code !== 0) die(`KyberSwap sign-message failed: ${signMsgRes.message}`);
  const eip712Data = signMsgRes.data;

  // Sign + submit
  const signature = await walletClient.signTypedData({
    domain: { ...eip712Data.domain, chainId: parseInt(eip712Data.domain.chainId) },
    types: { Order: eip712Data.types.Order },
    primaryType: 'Order',
    message: eip712Data.message,
  });

  const createRes = await fetch(`${KYBER_LO_DOMAIN}/write/api/v1/orders`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...unsignedBody, salt: eip712Data.message.salt, signature }),
  }).then(r => r.json());

  if (createRes.code !== 0) die(`KyberSwap create order failed: ${createRes.message}`);

  out({
    action: 'limit', status: 'created', orderId: createRes.data?.id, provider: 'kyberswap',
    sellToken: sellInfo.address, sellSymbol: sellInfo.symbol,
    buyToken: buyInfo.address, buySymbol: buyInfo.symbol,
    sellAmount: args['sell-amount'], buyAmount: args['buy-amount'],
    expiresAt: new Date(expiredAt * 1000).toISOString(), wallet: account.address,
  });
}

async function actionOrders(args) {
  const { account } = createSetup();
  const params = new URLSearchParams({ chainId: '8453', maker: account.address, status: args.status || 'active' });
  const res = await fetch(`${KYBER_LO_DOMAIN}/read-ks/api/v1/orders?${params}`).then(r => r.json());
  if (res.code !== 0) die(`KyberSwap query orders failed: ${res.message}`);

  const orders = (res.data?.orders || []).map(o => ({
    id: o.id, makerAsset: o.makerAsset, takerAsset: o.takerAsset,
    makingAmount: o.makingAmount, takingAmount: o.takingAmount,
    filledMakingAmount: o.filledMakingAmount, filledTakingAmount: o.filledTakingAmount,
    status: o.status,
    expiredAt: o.expiredAt ? new Date(o.expiredAt * 1000).toISOString() : null,
    createdAt: o.createdAt,
  }));
  out({ action: 'orders', count: orders.length, wallet: account.address, orders });
}

async function actionCancelOrder(args) {
  if (!args['order-id']) die('Usage: cancel-order --order-id 123');

  const { walletClient, account } = createSetup();
  const cancelSignRes = await fetch(`${KYBER_LO_DOMAIN}/write/api/v1/orders/cancel-sign`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chainId: '8453', maker: account.address, orderIds: [parseInt(args['order-id'])] }),
  }).then(r => r.json());

  if (cancelSignRes.code !== 0) die(`KyberSwap cancel-sign failed: ${cancelSignRes.message}`);
  const eip712Data = cancelSignRes.data;

  const signature = await walletClient.signTypedData({
    domain: { ...eip712Data.domain, chainId: parseInt(eip712Data.domain.chainId) },
    types: { CancelOrder: eip712Data.types.CancelOrder },
    primaryType: 'CancelOrder',
    message: eip712Data.message,
  });

  const cancelRes = await fetch(`${KYBER_LO_DOMAIN}/write/api/v1/orders/cancel`, {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chainId: '8453', maker: account.address, orderIds: [parseInt(args['order-id'])], signature }),
  }).then(r => r.json());

  if (cancelRes.code !== 0) die(`KyberSwap cancel failed: ${cancelRes.message}`);
  out({ action: 'cancel-order', orderId: args['order-id'], status: 'cancelled' });
}

// ─── Main ─────────────────────────────────────────────────────────────────────

const args = parseArgs(process.argv.slice(2));

const actions = {
  quote: actionQuote, swap: actionSwap, balance: actionBalance, providers: actionProviders,
  limit: actionLimit, orders: actionOrders, 'cancel-order': actionCancelOrder,
};

if (!args.action || !actions[args.action]) {
  die(`Unknown action: ${args.action || '(none)'}. Available: ${Object.keys(actions).join(', ')}`);
}

actions[args.action](args).catch(e => die(`${args.action} failed: ${e.message}`));
