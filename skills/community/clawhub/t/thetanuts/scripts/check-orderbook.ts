#!/usr/bin/env npx tsx
/**
 * Check orderbook for available liquidity before trading
 * Usage: npx tsx check-orderbook.ts --underlying <ETH|BTC> --type <PUT|CALL> --strike <price> --expiry <timestamp> --direction <buy|sell> [--size <contracts>]
 *
 * Examples:
 *   npx tsx check-orderbook.ts --underlying ETH --type PUT --strike 1900 --expiry 1774684800 --direction sell
 *   npx tsx check-orderbook.ts --underlying ETH --type PUT --strike 1900 --expiry 1774684800 --direction buy --size 0.1
 */

import { ThetanutsClient } from '@thetanuts-finance/thetanuts-client';
import { JsonRpcProvider } from 'ethers';

const RPC_URL = process.env.THETANUTS_RPC_URL || 'https://mainnet.base.org';
const CHAIN_ID = 8453;

interface CheckParams {
  underlying: 'ETH' | 'BTC';
  type: 'PUT' | 'CALL';
  strike: number;
  expiry: number;
  direction: 'buy' | 'sell';
  size?: number;
}

interface MatchingOrder {
  index: number;
  ticker: string;
  type: 'PUT' | 'CALL';
  strike: number;
  expiry: number;
  expiryDate: string;
  side: 'BID' | 'ASK';
  price: number;
  availableContracts: number;
  maker: string;
}

interface NearbyStrike {
  strike: number;
  priceDiff: string;
  bestPrice: number;
  availableContracts: number;
  orderIndex: number;
}

interface CheckResult {
  recommendation: 'orderbook' | 'rfq';
  reason: string;
  params: CheckParams;
  orderbookOrders: MatchingOrder[];
  bestPrice: number | null;
  availableSize: number | null;
  partialFillAvailable: boolean;
  partialSize: number | null;
  nearbyStrikes: NearbyStrike[];
  nextStep: string;
  timestamp: string;
}

function parseArgs(args: string[]): CheckParams | null {
  const params: Partial<CheckParams> = {};

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--underlying':
        params.underlying = args[++i]?.toUpperCase() as 'ETH' | 'BTC';
        break;
      case '--type':
        params.type = args[++i]?.toUpperCase() as 'PUT' | 'CALL';
        break;
      case '--strike':
        params.strike = parseFloat(args[++i]);
        break;
      case '--expiry':
        params.expiry = parseInt(args[++i]);
        break;
      case '--direction':
        params.direction = args[++i]?.toLowerCase() as 'buy' | 'sell';
        break;
      case '--size':
        params.size = parseFloat(args[++i]);
        break;
    }
  }

  // Validate required params
  const missing: string[] = [];
  if (!params.underlying || !['ETH', 'BTC'].includes(params.underlying)) missing.push('--underlying (ETH|BTC)');
  if (!params.type || !['PUT', 'CALL'].includes(params.type)) missing.push('--type (PUT|CALL)');
  if (!params.strike || isNaN(params.strike)) missing.push('--strike (price)');
  if (!params.expiry || isNaN(params.expiry)) missing.push('--expiry (unix timestamp)');
  if (!params.direction || !['buy', 'sell'].includes(params.direction)) missing.push('--direction (buy|sell)');

  if (missing.length > 0) {
    console.error(JSON.stringify({
      error: true,
      message: 'Missing or invalid required parameters',
      missing,
      usage: 'npx tsx check-orderbook.ts --underlying <ETH|BTC> --type <PUT|CALL> --strike <price> --expiry <timestamp> --direction <buy|sell> [--size <contracts>]',
      example: 'npx tsx check-orderbook.ts --underlying ETH --type PUT --strike 1900 --expiry 1774684800 --direction sell',
      help: {
        underlying: 'Asset to trade (ETH or BTC)',
        type: 'Option type (PUT or CALL)',
        strike: 'Target strike price in USD',
        expiry: 'Unix timestamp for expiry (8:00 UTC on expiry date)',
        direction: 'buy = you buy the option, sell = you sell the option',
        size: 'Optional: desired contract size (if omitted, shows all available)',
      },
    }, null, 2));
    return null;
  }

  return params as CheckParams;
}

function formatTicker(underlying: string, expiry: number, strike: number, type: string): string {
  const expiryDate = new Date(expiry * 1000);
  const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
  const day = expiryDate.getUTCDate();
  const month = months[expiryDate.getUTCMonth()];
  const year = expiryDate.getUTCFullYear().toString().slice(-2);
  return `${underlying}-${day}${month}${year}-${strike}-${type === 'PUT' ? 'P' : 'C'}`;
}

async function main() {
  const args = process.argv.slice(2);
  const params = parseArgs(args);

  if (!params) {
    process.exit(1);
  }

  const provider = new JsonRpcProvider(RPC_URL);
  const client = new ThetanutsClient({
    chainId: CHAIN_ID,
    provider,
  });

  try {
    const now = Math.floor(Date.now() / 1000);

    // Fetch all orders
    const orders = await client.api.fetchOrders();

    // Extract order data helper
    const extractOrderData = (o: any, index: number): MatchingOrder | null => {
      const isCall = o.rawApiData?.isCall ?? true;
      const strike = o.order?.strikePrice ? Number(o.order.strikePrice) / 1e8 : 0;
      const expiry = o.order?.expiry ? Number(o.order.expiry) : 0;
      const price = o.order?.price ? Number(o.order.price) / 1e8 : 0;
      const availableAmount = o.availableAmount ? Number(o.availableAmount) / 1e8 : 0;
      const isBuyer = o.order?.isBuyer ?? false;
      const orderExpiry = o.rawApiData?.orderExpiryTimestamp || 0;

      // Skip expired orders
      if (orderExpiry > 0 && orderExpiry < now) {
        return null;
      }

      const optionType = isCall ? 'CALL' : 'PUT';

      return {
        index,
        ticker: formatTicker('ETH', expiry, strike, optionType),
        type: optionType,
        strike,
        expiry,
        expiryDate: new Date(expiry * 1000).toISOString(),
        side: isBuyer ? 'BID' : 'ASK',
        price,
        availableContracts: availableAmount,
        maker: o.makerAddress,
      };
    };

    // Filter orders by type and expiry
    const filteredOrders: MatchingOrder[] = [];
    const allValidOrders: MatchingOrder[] = [];

    orders.forEach((o: any, index: number) => {
      const orderData = extractOrderData(o, index);
      if (!orderData) return;

      // Must match option type
      if (orderData.type !== params.type) return;

      // Must match expiry
      if (orderData.expiry !== params.expiry) return;

      allValidOrders.push(orderData);

      // Check direction match:
      // - User wants to BUY -> need ASK orders (sellers)
      // - User wants to SELL -> need BID orders (buyers)
      const matchesSide = params.direction === 'buy'
        ? orderData.side === 'ASK'
        : orderData.side === 'BID';

      if (!matchesSide) return;

      filteredOrders.push(orderData);
    });

    // Find exact strike matches
    const exactMatches = filteredOrders.filter(o => o.strike === params.strike);

    // Find nearby strikes (within 5% range)
    const strikeTolerance = params.strike * 0.05;
    const nearbyMatches = filteredOrders.filter(o =>
      o.strike !== params.strike &&
      Math.abs(o.strike - params.strike) <= strikeTolerance
    );

    // Calculate nearby strikes summary
    const nearbyStrikes: NearbyStrike[] = [];
    const strikeMap = new Map<number, MatchingOrder[]>();

    nearbyMatches.forEach(o => {
      if (!strikeMap.has(o.strike)) {
        strikeMap.set(o.strike, []);
      }
      strikeMap.get(o.strike)!.push(o);
    });

    strikeMap.forEach((orders, strike) => {
      const bestOrder = orders.reduce((best, curr) =>
        params.direction === 'buy'
          ? (curr.price < best.price ? curr : best)  // Lowest price for buying
          : (curr.price > best.price ? curr : best), // Highest price for selling
        orders[0]
      );
      const totalContracts = orders.reduce((sum, o) => sum + o.availableContracts, 0);
      const priceDiff = ((strike - params.strike) / params.strike * 100).toFixed(1);

      nearbyStrikes.push({
        strike,
        priceDiff: `${parseFloat(priceDiff) >= 0 ? '+' : ''}${priceDiff}%`,
        bestPrice: bestOrder.price,
        availableContracts: totalContracts,
        orderIndex: bestOrder.index,
      });
    });

    // Sort nearby strikes by proximity to target
    nearbyStrikes.sort((a, b) =>
      Math.abs(a.strike - params.strike) - Math.abs(b.strike - params.strike)
    );

    // Calculate totals for exact matches
    const totalAvailable = exactMatches.reduce((sum, o) => sum + o.availableContracts, 0);
    const bestPrice = exactMatches.length > 0
      ? (params.direction === 'buy'
          ? Math.min(...exactMatches.map(o => o.price))
          : Math.max(...exactMatches.map(o => o.price)))
      : null;

    // Determine recommendation
    let recommendation: 'orderbook' | 'rfq';
    let reason: string;
    let nextStep: string;
    let partialFillAvailable = false;
    let partialSize: number | null = null;

    if (exactMatches.length > 0) {
      // Check size requirement
      if (params.size && params.size > totalAvailable) {
        // Partial fill available
        partialFillAvailable = true;
        partialSize = totalAvailable;
        recommendation = 'orderbook';
        reason = `Found ${totalAvailable.toFixed(4)} contracts at strike $${params.strike} (you requested ${params.size}). Partial fill available via orderbook, or use RFQ for full amount.`;
        nextStep = `Preview fill: npx tsx fill-order.ts --order-index ${exactMatches[0].index} --collateral <amount> (set WDK_SEED in env first)`;
      } else {
        recommendation = 'orderbook';
        reason = `Found orderbook liquidity at strike $${params.strike}. Best ${params.direction === 'buy' ? 'ask' : 'bid'} price: $${bestPrice?.toFixed(2)}. Available: ${totalAvailable.toFixed(4)} contracts. This will execute instantly.`;
        nextStep = `Preview fill: npx tsx fill-order.ts --order-index ${exactMatches[0].index} --collateral <amount> (set WDK_SEED in env first)`;
      }
    } else if (nearbyStrikes.length > 0) {
      recommendation = 'rfq';
      reason = `No orderbook liquidity at exact strike $${params.strike}. Nearby strikes available: ${nearbyStrikes.slice(0, 3).map(s => `$${s.strike} (${s.priceDiff})`).join(', ')}. Use RFQ for your exact strike, or consider nearby strikes.`;
      nextStep = `Build RFQ: npx tsx build-rfq.ts --underlying ${params.underlying} --type ${params.type} --strike ${params.strike} --expiry ${params.expiry} --contracts <amount> --direction ${params.direction}`;
    } else {
      recommendation = 'rfq';
      reason = `No orderbook liquidity at strike $${params.strike} or nearby. Submitting RFQ - market makers will respond within 6 minutes.`;
      nextStep = `Build RFQ: npx tsx build-rfq.ts --underlying ${params.underlying} --type ${params.type} --strike ${params.strike} --expiry ${params.expiry} --contracts <amount> --direction ${params.direction}`;
    }

    const result: CheckResult = {
      recommendation,
      reason,
      params,
      orderbookOrders: exactMatches.slice(0, 10), // Limit to top 10
      bestPrice,
      availableSize: totalAvailable > 0 ? totalAvailable : null,
      partialFillAvailable,
      partialSize,
      nearbyStrikes: nearbyStrikes.slice(0, 5), // Top 5 nearby
      nextStep,
      timestamp: new Date().toISOString(),
    };

    console.log(JSON.stringify(result, null, 2));

  } catch (error) {
    console.error(JSON.stringify({
      error: true,
      message: error instanceof Error ? error.message : 'Unknown error',
      recommendation: 'rfq',
      reason: 'Failed to check orderbook. Falling back to RFQ recommendation.',
      nextStep: `Build RFQ: npx tsx build-rfq.ts --underlying ${params.underlying} --type ${params.type} --strike ${params.strike} --expiry ${params.expiry} --contracts <amount> --direction ${params.direction}`,
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }
}

main();
