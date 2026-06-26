#!/usr/bin/env npx tsx
/**
 * Fill an orderbook order on Thetanuts Finance.
 * Seed is read from WDK_SEED env var (or --seed-file) — never from argv.
 *
 * Usage:
 *   WDK_SEED="..." npx tsx fill-order.ts --order-index <n> --collateral <amount> [--execute] [--wait]
 *
 * Without --execute, the script previews the fill without signing.
 */

import { ThetanutsClient } from '@thetanuts-finance/thetanuts-client';
import { JsonRpcProvider, Wallet, HDNodeWallet } from 'ethers';
import { loadSeed } from './lib/load-seed';

const RPC_URL = process.env.THETANUTS_RPC_URL || 'https://mainnet.base.org';
const CHAIN_ID = 8453;

// Known tokens for display
const KNOWN_TOKENS: Record<string, { symbol: string; decimals: number }> = {
  '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913': { symbol: 'USDC', decimals: 6 },
  '0x4200000000000000000000000000000000000006': { symbol: 'WETH', decimals: 18 },
  '0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf': { symbol: 'cbBTC', decimals: 8 },
};

interface FillParams {
  orderIndex: number;
  collateral: number;
  walletIndex: number;
  execute: boolean;
  wait: boolean;
  referrer?: string;
}

function parseArgs(args: string[]): FillParams | null {
  const params: Partial<FillParams> = {
    walletIndex: 0,
    execute: false,
    wait: false,
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--order-index':
        params.orderIndex = parseInt(args[++i]);
        break;
      case '--collateral':
        params.collateral = parseFloat(args[++i]);
        break;
      case '--index':
        params.walletIndex = parseInt(args[++i]) || 0;
        break;
      case '--execute':
        params.execute = true;
        break;
      case '--wait':
        params.wait = true;
        break;
      case '--referrer':
        params.referrer = args[++i];
        break;
    }
  }

  const missing: string[] = [];
  if (params.orderIndex === undefined || isNaN(params.orderIndex)) missing.push('--order-index');
  if (params.collateral === undefined || isNaN(params.collateral)) missing.push('--collateral');

  if (missing.length > 0) {
    console.error(JSON.stringify({
      error: true,
      message: 'Missing required parameters',
      missing,
      usage: 'WDK_SEED="..." npx tsx fill-order.ts --order-index <number> --collateral <amount> [--execute] [--wait]',
      example: 'WDK_SEED="word1 word2 ... word12" npx tsx fill-order.ts --order-index 0 --collateral 10 --execute --wait',
      help: {
        orderIndex: 'Index of order from fetch-orders.ts output (0-based)',
        collateral: 'Amount of collateral in token units (e.g., 10 for 10 USDC)',
        execute: 'Include to actually execute (without this, preview only)',
        wait: 'Wait for transaction confirmation',
      },
    }, null, 2));
    return null;
  }

  return params as FillParams;
}

function formatAmount(amount: bigint, decimals: number): string {
  const divisor = BigInt(10 ** decimals);
  const integerPart = amount / divisor;
  const fractionalPart = amount % divisor;
  const fractionalStr = fractionalPart.toString().padStart(decimals, '0');
  return `${integerPart}.${fractionalStr.slice(0, 4)}`;
}

async function main() {
  const args = process.argv.slice(2);
  const params = parseArgs(args);

  if (!params) {
    process.exit(1);
  }

  // Only load the seed when we actually need to sign — preview mode stays read-only.
  const seed = params.execute ? loadSeed(args).seed : undefined;

  const provider = new JsonRpcProvider(RPC_URL);

  let client: ThetanutsClient;
  let signer: Wallet | HDNodeWallet | undefined;

  if (params.execute) {
    signer = Wallet.fromPhrase(seed!, provider);
    client = new ThetanutsClient({
      chainId: CHAIN_ID,
      provider,
      signer,
      referrer: params.referrer,
    });
  } else {
    client = new ThetanutsClient({
      chainId: CHAIN_ID,
      provider,
    });
  }

  try {
    // Fetch all orders
    const orders = await client.api.fetchOrders();

    if (orders.length === 0) {
      console.log(JSON.stringify({
        error: true,
        message: 'No orders available in orderbook',
        timestamp: new Date().toISOString(),
      }, null, 2));
      process.exit(1);
    }

    // Find the order by index
    if (params.orderIndex < 0 || params.orderIndex >= orders.length) {
      console.log(JSON.stringify({
        error: true,
        message: `Order index ${params.orderIndex} out of range. Available: 0-${orders.length - 1}`,
        totalOrders: orders.length,
        timestamp: new Date().toISOString(),
      }, null, 2));
      process.exit(1);
    }

    const order = orders[params.orderIndex];

    // Extract order details
    const isCall = order.rawApiData?.isCall ?? true;
    const strikeRaw = order.order?.strikes?.[0] ?? order.order?.strikePrice;
    const strike = strikeRaw ? Number(strikeRaw) / 1e8 : 0;
    const expiry = order.order?.expiry ? Number(order.order.expiry) : 0;
    const price = order.order?.price ? Number(order.order.price) / 1e8 : 0;
    const isBuyer = order.order?.isBuyer ?? false;

    // Check if order is expired
    const now = Math.floor(Date.now() / 1000);
    if (expiry > 0 && expiry < now) {
      console.log(JSON.stringify({
        error: true,
        message: 'Order has expired',
        orderExpiry: new Date(expiry * 1000).toISOString(),
        currentTime: new Date().toISOString(),
        suggestion: 'Fetch fresh orders with: npx tsx fetch-orders.ts',
        timestamp: new Date().toISOString(),
      }, null, 2));
      process.exit(1);
    }

    // Determine collateral token and decimals
    const collateralTokenAddress = order.rawApiData?.collateral || order.order?.collateralToken || client.chainConfig.tokens.USDC.address;
    const tokenInfo = KNOWN_TOKENS[collateralTokenAddress] || { symbol: 'UNKNOWN', decimals: 18 };
    const collateralDecimals = tokenInfo.decimals;

    // Convert collateral to BigInt
    const collateralAmount = BigInt(Math.floor(params.collateral * (10 ** collateralDecimals)));

    // Preview the fill
    const preview = client.optionBook.previewFillOrder(order, collateralAmount);

    // Format ticker
    const expiryDate = new Date(expiry * 1000);
    const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
    const day = expiryDate.getUTCDate();
    const month = months[expiryDate.getUTCMonth()];
    const year = expiryDate.getUTCFullYear().toString().slice(-2);
    const ticker = `ETH-${day}${month}${year}-${strike}-${isCall ? 'C' : 'P'}`;

    const previewResult = {
      mode: params.execute ? 'EXECUTE' : 'PREVIEW',
      order: {
        index: params.orderIndex,
        ticker,
        type: isCall ? 'CALL' : 'PUT',
        strike,
        expiry,
        expiryDate: expiryDate.toISOString(),
        side: isBuyer ? 'BID' : 'ASK',
        pricePerContract: price,
        maker: order.makerAddress,
      },
      fill: {
        collateralAmount: params.collateral,
        collateralToken: tokenInfo.symbol,
        collateralTokenAddress,
        maxContracts: preview.maxContracts ? Number(preview.maxContracts) / 1e8 : 0,
        numContracts: preview.numContracts ? Number(preview.numContracts) / 1e8 : 0,
        pricePerContract: preview.pricePerContract ? Number(preview.pricePerContract) / 1e8 : 0,
        yourRole: isBuyer ? 'seller' : 'buyer',
        whatHappens: isBuyer
          ? `You SELL to this BID. You post ${params.collateral} ${tokenInfo.symbol} collateral and receive premium.`
          : `You BUY from this ASK. You pay ${params.collateral} ${tokenInfo.symbol} to buy the option.`,
      },
      timestamp: new Date().toISOString(),
    };

    if (!params.execute) {
      // Preview only mode
      console.log(JSON.stringify({
        ...previewResult,
        nextStep: 'Add --execute flag to fill this order',
        command: `WDK_SEED="..." npx tsx fill-order.ts --order-index ${params.orderIndex} --collateral ${params.collateral} --execute --wait`,
      }, null, 2));
      return;
    }

    // Execute mode - fill the order
    if (!signer) {
      throw new Error('Signer required for execution');
    }

    const walletAddress = await signer.getAddress();

    // Pre-check: ensure wallet has ETH for gas
    const ethBalance = await provider.getBalance(walletAddress);
    if (ethBalance === 0n) {
      console.log(JSON.stringify({
        error: true,
        message: 'Wallet has 0 ETH on Base. You need ETH for gas fees. Bridge ETH to Base via bridge.base.org.',
        address: walletAddress,
        timestamp: new Date().toISOString(),
      }, null, 2));
      process.exit(1);
    }

    // Pre-check: ensure wallet has enough collateral tokens
    const tokenBalance = await client.erc20.getBalance(collateralTokenAddress, walletAddress);
    if (tokenBalance < collateralAmount) {
      const needed = Number(collateralAmount - tokenBalance) / (10 ** tokenInfo.decimals);
      console.log(JSON.stringify({
        error: true,
        message: `Insufficient ${tokenInfo.symbol} balance. You need ${needed.toFixed(tokenInfo.decimals > 6 ? 6 : 2)} more ${tokenInfo.symbol}. Current balance is less than the required collateral.`,
        token: collateralTokenAddress,
        tokenSymbol: tokenInfo.symbol,
        address: walletAddress,
        timestamp: new Date().toISOString(),
      }, null, 2));
      process.exit(1);
    }

    // Check token allowance and approve if needed
    const optionBookAddress = client.chainConfig.contracts.optionBook;
    const currentAllowance = await client.erc20.getAllowance(
      collateralTokenAddress,
      walletAddress,
      optionBookAddress
    );

    let approvalTx: string | null = null;
    if (currentAllowance < collateralAmount) {
      console.error(JSON.stringify({
        status: 'approving',
        message: `Approving ${tokenInfo.symbol} for OptionBook...`,
      }));

      // SDK approve() waits internally and returns a receipt, not a tx response
      const approveReceipt = await client.erc20.approve(
        collateralTokenAddress,
        optionBookAddress,
        collateralAmount * 10n // Approve 10x for future fills
      );

      approvalTx = approveReceipt.hash;
    }

    // Fill the order
    console.error(JSON.stringify({
      status: 'filling',
      message: 'Executing order fill...',
    }));

    // SDK fillOrder() waits internally and returns a receipt, not a tx response
    const fillReceipt = await client.optionBook.fillOrder(order, collateralAmount, params.referrer);

    console.log(JSON.stringify({
      success: true,
      ...previewResult,
      execution: {
        walletAddress,
        approvalTx,
        fillTx: fillReceipt.hash,
        blockNumber: fillReceipt.blockNumber,
        gasUsed: fillReceipt.gasUsed?.toString(),
      },
      timestamp: new Date().toISOString(),
    }, null, 2));

  } catch (error) {
    console.error(JSON.stringify({
      error: true,
      message: error instanceof Error ? error.message : 'Unknown error',
      code: (error as any)?.code,
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }
}

main();
