#!/usr/bin/env npx tsx
/**
 * Fetch orderbook from Thetanuts Finance
 * Usage: npx tsx fetch-orders.ts [--underlying ETH|BTC] [--type PUT|CALL]
 *
 * Examples:
 *   npx tsx fetch-orders.ts
 *   npx tsx fetch-orders.ts --underlying ETH
 *   npx tsx fetch-orders.ts --underlying ETH --type PUT
 */

import { ThetanutsClient } from '@thetanuts-finance/thetanuts-client';
import { JsonRpcProvider } from 'ethers';

const RPC_URL = process.env.THETANUTS_RPC_URL || 'https://mainnet.base.org';
const CHAIN_ID = 8453;

interface FilterParams {
  underlying?: 'ETH' | 'BTC';
  type?: 'PUT' | 'CALL';
}

function parseArgs(args: string[]): FilterParams {
  const params: FilterParams = {};

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--underlying':
        const underlying = args[++i]?.toUpperCase();
        if (underlying === 'ETH' || underlying === 'BTC') {
          params.underlying = underlying;
        }
        break;
      case '--type':
        const type = args[++i]?.toUpperCase();
        if (type === 'PUT' || type === 'CALL') {
          params.type = type;
        }
        break;
    }
  }

  return params;
}

async function main() {
  const args = process.argv.slice(2);
  const filters = parseArgs(args);

  const provider = new JsonRpcProvider(RPC_URL);
  const client = new ThetanutsClient({
    chainId: CHAIN_ID,
    provider,
  });

  try {
    // Fetch all orders
    const orders = await client.api.fetchOrders();

    // Helper to extract order data
    const extractOrderData = (o: any) => {
      const isCall = o.rawApiData?.isCall ?? true;
      const strike = o.order?.strikePrice ? Number(o.order.strikePrice) / 1e8 : null;
      const expiry = o.order?.expiry ? Number(o.order.expiry) : null;
      const price = o.order?.price ? Number(o.order.price) / 1e8 : null;
      const availableAmount = o.availableAmount ? Number(o.availableAmount) / 1e8 : null;

      return {
        type: isCall ? 'CALL' : 'PUT',
        strike,
        expiry,
        expiryDate: expiry ? new Date(expiry * 1000).toISOString() : null,
        side: o.order?.isBuyer ? 'BID' : 'ASK',
        price,
        availableContracts: availableAmount,
        maker: o.makerAddress,
        orderExpiry: o.rawApiData?.orderExpiryTimestamp,
      };
    };

    // Filter results
    let filtered = orders;

    if (filters.type) {
      filtered = filtered.filter((o: any) => {
        const isCall = o.rawApiData?.isCall ?? true;
        const optionType = isCall ? 'CALL' : 'PUT';
        return optionType === filters.type;
      });
    }

    // Format output
    const result = {
      filters,
      totalOrders: orders.length,
      filteredCount: filtered.length,
      orders: filtered.slice(0, 50).map(extractOrderData), // Limit to 50 orders
      timestamp: new Date().toISOString(),
    };

    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error(JSON.stringify({
      error: true,
      message: error instanceof Error ? error.message : 'Unknown error',
      filters,
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }
}

main();
