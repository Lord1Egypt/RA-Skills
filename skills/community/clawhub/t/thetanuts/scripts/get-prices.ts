#!/usr/bin/env npx tsx
/**
 * Get current market prices and protocol stats from Thetanuts Finance
 * Usage: npx tsx get-prices.ts
 */

import { ThetanutsClient } from '@thetanuts-finance/thetanuts-client';
import { JsonRpcProvider } from 'ethers';

const RPC_URL = process.env.THETANUTS_RPC_URL || 'https://mainnet.base.org';
const CHAIN_ID = 8453; // Base Mainnet

async function main() {
  const provider = new JsonRpcProvider(RPC_URL);
  const client = new ThetanutsClient({
    chainId: CHAIN_ID,
    provider,
  });

  try {
    // Get market data (current prices)
    const marketData = await client.api.getMarketData();

    // Get protocol stats from indexer
    const stats = await client.api.getStatsFromIndexer();

    const result = {
      prices: marketData,
      stats: stats || {},
      chain: {
        id: CHAIN_ID,
        name: 'Base Mainnet',
        rpcUrl: RPC_URL,
      },
      timestamp: new Date().toISOString(),
    };

    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error(JSON.stringify({
      error: true,
      message: error instanceof Error ? error.message : 'Unknown error',
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }
}

main();
