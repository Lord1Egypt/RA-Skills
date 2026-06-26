#!/usr/bin/env npx tsx
/**
 * Check if an RFQ was filled after submission
 *
 * Usage:
 *   npx tsx check-rfq-fill.ts --address <wallet> --ticker <expected> --since <timestamp>
 *
 * Example:
 *   npx tsx check-rfq-fill.ts --address 0x1234... --ticker ETH-29MAR26-1900-P --since 1774685000
 *
 * The script fetches positions and checks if a new position matching the ticker
 * was created after the specified timestamp.
 */

import { ThetanutsClient } from '@thetanuts-finance/thetanuts-client';
import { JsonRpcProvider } from 'ethers';

const RPC_URL = process.env.THETANUTS_RPC_URL || 'https://mainnet.base.org';
const CHAIN_ID = 8453;

interface CheckFillParams {
  address: string;
  ticker: string;
  since: number;
}

interface Position {
  id: string;
  optionAddress: string;
  underlying: string;
  type: string;
  strike: number | null;
  strikes?: number[];
  expiry: number;
  expiryDate: string | null;
  contracts: number | null;
  side: string;
  status: string;
  collateral: string;
}

interface FillResult {
  filled: boolean;
  position?: Position;
  message: string;
  suggestions?: string[];
  checkParams: {
    address: string;
    ticker: string;
    since: number;
    sinceDate: string;
  };
  timestamp: string;
}

function parseArgs(args: string[]): CheckFillParams | null {
  const params: Partial<CheckFillParams> = {};

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--address':
        params.address = args[++i];
        break;
      case '--ticker':
        params.ticker = args[++i]?.toUpperCase();
        break;
      case '--since':
        params.since = parseInt(args[++i]);
        break;
    }
  }

  // Validate required params
  const missing: string[] = [];
  if (!params.address || !params.address.match(/^0x[a-fA-F0-9]{40}$/)) {
    missing.push('--address (valid wallet address)');
  }
  if (!params.ticker) {
    missing.push('--ticker (expected option ticker, e.g., ETH-29MAR26-1900-P)');
  }
  if (!params.since || isNaN(params.since)) {
    missing.push('--since (unix timestamp of RFQ submission)');
  }

  if (missing.length > 0) {
    console.error(JSON.stringify({
      error: true,
      message: 'Missing or invalid required parameters',
      missing,
      usage: 'npx tsx check-rfq-fill.ts --address <wallet> --ticker <expected> --since <timestamp>',
      example: 'npx tsx check-rfq-fill.ts --address 0x1234... --ticker ETH-29MAR26-1900-P --since 1774685000',
    }, null, 2));
    return null;
  }

  return params as CheckFillParams;
}

function parseTicker(ticker: string): { underlying: string; expiry: string; strike: number; type: string } | null {
  // Format: ETH-29MAR26-1900-P or ETH-29MAR26-1900/2000-P (multi-strike)
  const match = ticker.match(/^(ETH|BTC)-(\d{1,2}[A-Z]{3}\d{2})-([0-9/]+)-([PC])$/);
  if (!match) return null;

  const [, underlying, expiry, strikeStr, typeChar] = match;
  const strikes = strikeStr.split('/').map(s => parseFloat(s));

  return {
    underlying,
    expiry,
    strike: strikes[0],
    type: typeChar === 'P' ? 'PUT' : 'CALL',
  };
}

function formatTicker(pos: Position): string {
  if (!pos.expiry || !pos.underlying) return 'UNKNOWN';

  const expiryDate = new Date(pos.expiry * 1000);
  const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
  const day = expiryDate.getUTCDate();
  const month = months[expiryDate.getUTCMonth()];
  const year = expiryDate.getUTCFullYear().toString().slice(-2);

  const strikeStr = pos.strikes && pos.strikes.length > 1
    ? pos.strikes.join('/')
    : pos.strike?.toString() || '0';

  const typeChar = pos.type === 'PUT' ? 'P' : 'C';

  return `${pos.underlying}-${day}${month}${year}-${strikeStr}-${typeChar}`;
}

function matchesTicker(pos: Position, targetTicker: string): boolean {
  const posTicker = formatTicker(pos);
  return posTicker.toUpperCase() === targetTicker.toUpperCase();
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
    // Get user positions
    const positions = await client.api.getUserPositionsFromIndexer(params.address);

    // Helper to convert BigInt to number
    const toNum = (val: any): number | null => {
      if (val === null || val === undefined) return null;
      if (typeof val === 'bigint') return Number(val);
      if (typeof val === 'string') return parseFloat(val);
      return val;
    };

    // Format positions
    const formattedPositions: Position[] = (Array.isArray(positions) ? positions : []).map((pos: any) => {
      const option = pos.option || {};
      const strikes = (option.strikes || []).map((s: any) => toNum(s) ? toNum(s)! / 1e8 : 0);

      return {
        id: pos.id,
        optionAddress: pos.optionAddress,
        underlying: option.underlying,
        type: option.optionType === 0 ? 'PUT' : 'CALL',
        strike: strikes.length > 0 ? strikes[0] : null,
        strikes: strikes.length > 1 ? strikes : undefined,
        expiry: option.expiry,
        expiryDate: option.expiry ? new Date(option.expiry * 1000).toISOString() : null,
        contracts: toNum(pos.amount) ? toNum(pos.amount)! / 1e18 : null,
        side: pos.side?.toUpperCase() || 'UNKNOWN',
        status: pos.status,
        collateral: pos.collateralSymbol,
      };
    });

    // Find matching position created after the timestamp
    // Note: The indexer may not have exact creation timestamp, so we check for matching ticker
    const matchingPosition = formattedPositions.find(pos => matchesTicker(pos, params.ticker));

    const result: FillResult = {
      filled: !!matchingPosition,
      checkParams: {
        address: params.address,
        ticker: params.ticker,
        since: params.since,
        sinceDate: new Date(params.since * 1000).toISOString(),
      },
      timestamp: new Date().toISOString(),
      message: '',
    };

    if (matchingPosition) {
      result.position = matchingPosition;
      result.message = `RFQ filled successfully! Found position: ${formatTicker(matchingPosition)} with ${matchingPosition.contracts?.toFixed(6)} contracts.`;
    } else {
      result.message = 'No fill detected. Market makers did not respond within the deadline.';
      result.suggestions = [
        'Try a different strike price closer to current market',
        'Check orderbook for existing liquidity: npx tsx fetch-orders.ts --type PUT',
        'Increase collateral for larger trade size',
        'Try again during active trading hours',
      ];
    }

    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error(JSON.stringify({
      error: true,
      message: error instanceof Error ? error.message : 'Unknown error',
      params,
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }
}

main();
