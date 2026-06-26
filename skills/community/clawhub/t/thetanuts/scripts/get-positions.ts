#!/usr/bin/env npx tsx
/**
 * Get user positions from Thetanuts Finance
 * Usage: npx tsx get-positions.ts <wallet_address>
 *
 * Example:
 *   npx tsx get-positions.ts 0x1234567890abcdef1234567890abcdef12345678
 */

import { ThetanutsClient } from '@thetanuts-finance/thetanuts-client';
import { JsonRpcProvider } from 'ethers';

const RPC_URL = process.env.THETANUTS_RPC_URL || 'https://mainnet.base.org';
const CHAIN_ID = 8453;

function parseArgs(args: string[]): { address: string } {
  const address = args[0];

  if (!address || !address.match(/^0x[a-fA-F0-9]{40}$/)) {
    console.error(JSON.stringify({
      error: true,
      message: 'Usage: npx tsx get-positions.ts <wallet_address>',
      example: 'npx tsx get-positions.ts 0x1234567890abcdef1234567890abcdef12345678',
    }, null, 2));
    process.exit(1);
  }

  return { address };
}

async function main() {
  const args = process.argv.slice(2);
  const { address } = parseArgs(args);

  const provider = new JsonRpcProvider(RPC_URL);
  const client = new ThetanutsClient({
    chainId: CHAIN_ID,
    provider,
  });

  try {
    // Get user positions from indexer
    const positions = await client.api.getUserPositionsFromIndexer(address);

    // Helper to convert BigInt to number
    const toNum = (val: any): number | null => {
      if (val === null || val === undefined) return null;
      if (typeof val === 'bigint') return Number(val);
      if (typeof val === 'string') return parseFloat(val);
      return val;
    };

    // Format output - limit to recent 100 positions
    const recentPositions = Array.isArray(positions) ? positions.slice(0, 100) : [];

    const result = {
      address,
      totalPositions: Array.isArray(positions) ? positions.length : 0,
      displayedCount: recentPositions.length,
      positions: recentPositions.map((pos: any) => {
        const option = pos.option || {};
        const strikes = option.strikes || [];
        const strike = strikes.length > 0 ? toNum(strikes[0]) : null;

        return {
          id: pos.id,
          optionAddress: pos.optionAddress,
          underlying: option.underlying,
          type: option.optionType === 0 ? 'PUT' : 'CALL',
          strike: strike ? strike / 1e8 : null,
          expiry: option.expiry,
          expiryDate: option.expiry ? new Date(option.expiry * 1000).toISOString() : null,
          contracts: toNum(pos.amount) ? toNum(pos.amount)! / 1e18 : null,
          side: pos.side?.toUpperCase() || 'UNKNOWN',
          status: pos.status,
          collateral: pos.collateralSymbol,
          pnlUsd: pos.pnlUsd,
        };
      }),
      timestamp: new Date().toISOString(),
    };

    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error(JSON.stringify({
      error: true,
      message: error instanceof Error ? error.message : 'Unknown error',
      address,
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }
}

main();
