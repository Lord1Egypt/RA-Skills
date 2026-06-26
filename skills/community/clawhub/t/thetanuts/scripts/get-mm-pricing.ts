#!/usr/bin/env npx tsx
/**
 * Get market maker option pricing from Thetanuts Finance
 * Usage: npx tsx get-mm-pricing.ts <underlying> [--type PUT|CALL] [--expiry DDMMMYY]
 *
 * Examples:
 *   npx tsx get-mm-pricing.ts ETH
 *   npx tsx get-mm-pricing.ts ETH --type PUT
 *   npx tsx get-mm-pricing.ts BTC --expiry 28MAR26
 */

import { ThetanutsClient } from '@thetanuts-finance/thetanuts-client';
import { JsonRpcProvider } from 'ethers';

const RPC_URL = process.env.THETANUTS_RPC_URL || 'https://mainnet.base.org';
const CHAIN_ID = 8453;

function parseArgs(args: string[]): { underlying: string; type?: string; expiry?: string } {
  const underlying = args[0]?.toUpperCase();

  if (!underlying || !['ETH', 'BTC'].includes(underlying)) {
    console.error(JSON.stringify({
      error: true,
      message: 'Usage: npx tsx get-mm-pricing.ts <ETH|BTC> [--type PUT|CALL] [--expiry DDMMMYY]',
      examples: [
        'npx tsx get-mm-pricing.ts ETH',
        'npx tsx get-mm-pricing.ts ETH --type PUT',
        'npx tsx get-mm-pricing.ts BTC --expiry 28MAR26',
      ],
    }, null, 2));
    process.exit(1);
  }

  let type: string | undefined;
  let expiry: string | undefined;

  for (let i = 1; i < args.length; i++) {
    if (args[i] === '--type' && args[i + 1]) {
      type = args[i + 1].toUpperCase();
      i++;
    } else if (args[i] === '--expiry' && args[i + 1]) {
      expiry = args[i + 1].toUpperCase();
      i++;
    }
  }

  return { underlying, type, expiry };
}

async function main() {
  const args = process.argv.slice(2);
  const { underlying, type, expiry } = parseArgs(args);

  const provider = new JsonRpcProvider(RPC_URL);
  const client = new ThetanutsClient({
    chainId: CHAIN_ID,
    provider,
  });

  try {
    // Get all MM pricing for the underlying (returns object keyed by ticker)
    const pricingData = await client.mmPricing.getAllPricing(underlying as 'ETH' | 'BTC');

    // Convert object to array
    let options = Object.values(pricingData) as any[];

    // Filter by type (PUT/CALL)
    if (type) {
      options = options.filter((p: any) => {
        const optionType = p.isCall === false ? 'PUT' : 'CALL';
        return optionType === type;
      });
    }

    // Filter by expiry (e.g., "28MAR26")
    if (expiry) {
      options = options.filter((p: any) => p.ticker?.includes(expiry));
    }

    // Format output
    const result = {
      underlying,
      filters: { type, expiry },
      count: options.length,
      options: options.map((p: any) => ({
        ticker: p.ticker,
        strike: p.strike,
        expiry: p.expiry,
        expiryDate: p.expiry ? new Date(p.expiry * 1000).toISOString() : null,
        type: p.isCall === false ? 'PUT' : 'CALL',
        bid: p.feeAdjustedBid,
        ask: p.feeAdjustedAsk,
        mark: p.markPrice,
        underlyingPrice: p.underlyingPrice,
      })),
      timestamp: new Date().toISOString(),
    };

    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error(JSON.stringify({
      error: true,
      message: error instanceof Error ? error.message : 'Unknown error',
      underlying,
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }
}

main();
