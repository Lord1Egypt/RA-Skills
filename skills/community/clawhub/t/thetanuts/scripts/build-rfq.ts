#!/usr/bin/env npx tsx
/**
 * Build RFQ request for Thetanuts Finance
 *
 * Usage:
 *   Vanilla (1 strike):
 *     npx tsx build-rfq.ts --underlying ETH --type PUT --strike 1900 --expiry <timestamp> --contracts 1 --direction buy
 *
 *   Multi-strike (spread/butterfly/condor):
 *     npx tsx build-rfq.ts --underlying ETH --type CALL --strikes 2000,2100 --expiry <timestamp> --contracts 1 --direction buy
 *
 * Examples:
 *   PUT:          npx tsx build-rfq.ts --underlying ETH --type PUT --strike 1900 --expiry 1774684800 --contracts 1 --direction buy
 *   CALL_SPREAD:  npx tsx build-rfq.ts --underlying ETH --type CALL --strikes 2000,2100 --expiry 1774684800 --contracts 1 --direction buy
 *   PUT_FLY:      npx tsx build-rfq.ts --underlying ETH --type PUT --strikes 1900,1850,1800 --expiry 1774684800 --contracts 1 --direction buy
 *   IRON_CONDOR:  npx tsx build-rfq.ts --underlying ETH --type PUT --strikes 1800,1900,2100,2200 --expiry 1774684800 --contracts 1 --direction sell
 */

import { ThetanutsClient } from '@thetanuts-finance/thetanuts-client';
import { JsonRpcProvider } from 'ethers';

const RPC_URL = process.env.THETANUTS_RPC_URL || 'https://mainnet.base.org';
const CHAIN_ID = 8453;

// Default deadline: 45 seconds (0.75 minutes)
const DEFAULT_DEADLINE_MINUTES = 0.75;

type StructureType =
  | 'PUT'
  | 'INVERSE_CALL'
  | 'CALL_SPREAD'
  | 'PUT_SPREAD'
  | 'CALL_FLY'
  | 'PUT_FLY'
  | 'CALL_CONDOR'
  | 'PUT_CONDOR'
  | 'IRON_CONDOR';

interface RFQParams {
  underlying: 'ETH' | 'BTC';
  type: 'PUT' | 'CALL';
  strike?: number;
  strikes?: number[];
  expiry: number;
  contracts: number;
  direction: 'buy' | 'sell';
  requester?: string;
  collateral?: 'USDC' | 'WETH';
  deadlineMinutes?: number;
}

function getStructureType(strikeCount: number, optionType: 'PUT' | 'CALL'): StructureType {
  switch (strikeCount) {
    case 1:
      return optionType === 'PUT' ? 'PUT' : 'INVERSE_CALL';
    case 2:
      return optionType === 'PUT' ? 'PUT_SPREAD' : 'CALL_SPREAD';
    case 3:
      return optionType === 'PUT' ? 'PUT_FLY' : 'CALL_FLY';
    case 4:
      // 4 strikes could be PUT_CONDOR, CALL_CONDOR, or IRON_CONDOR
      // For simplicity, we use the option type to determine
      return optionType === 'PUT' ? 'PUT_CONDOR' : 'CALL_CONDOR';
    default:
      throw new Error(`Invalid strike count: ${strikeCount}. Must be 1, 2, 3, or 4.`);
  }
}

function validateStrikeOrdering(strikes: number[], optionType: 'PUT' | 'CALL'): { valid: boolean; message: string } {
  if (strikes.length === 1) {
    return { valid: true, message: 'Single strike - no ordering required' };
  }

  // Check if ascending
  const isAscending = strikes.every((val, i) => i === 0 || val > strikes[i - 1]);
  // Check if descending
  const isDescending = strikes.every((val, i) => i === 0 || val < strikes[i - 1]);

  if (strikes.length === 4) {
    // Condors always require ascending order
    if (!isAscending) {
      return {
        valid: false,
        message: `Condor (4 strikes) requires ASCENDING order. Got: [${strikes.join(', ')}]. Should be: [${[...strikes].sort((a, b) => a - b).join(', ')}]`
      };
    }
    return { valid: true, message: 'Condor - ascending order valid' };
  }

  if (optionType === 'PUT') {
    // PUT spreads/flies require descending order
    if (!isDescending) {
      return {
        valid: false,
        message: `PUT structures require DESCENDING order (high→low). Got: [${strikes.join(', ')}]. Should be: [${[...strikes].sort((a, b) => b - a).join(', ')}]`
      };
    }
    return { valid: true, message: 'PUT structure - descending order valid' };
  } else {
    // CALL spreads/flies require ascending order
    if (!isAscending) {
      return {
        valid: false,
        message: `CALL structures require ASCENDING order (low→high). Got: [${strikes.join(', ')}]. Should be: [${[...strikes].sort((a, b) => a - b).join(', ')}]`
      };
    }
    return { valid: true, message: 'CALL structure - ascending order valid' };
  }
}

function parseArgs(args: string[]): RFQParams | null {
  const params: Partial<RFQParams> = {};

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
      case '--strikes':
        params.strikes = args[++i]?.split(',').map(s => parseFloat(s.trim()));
        break;
      case '--expiry':
        params.expiry = parseInt(args[++i]);
        break;
      case '--contracts':
        params.contracts = parseFloat(args[++i]);
        break;
      case '--direction':
        params.direction = args[++i]?.toLowerCase() as 'buy' | 'sell';
        break;
      case '--requester':
        params.requester = args[++i];
        break;
      case '--collateral':
        params.collateral = args[++i]?.toUpperCase() as 'USDC' | 'WETH';
        break;
      case '--deadline':
        params.deadlineMinutes = parseFloat(args[++i]);
        break;
    }
  }

  // Validate required params
  const missing: string[] = [];
  if (!params.underlying || !['ETH', 'BTC'].includes(params.underlying)) missing.push('--underlying (ETH|BTC)');
  if (!params.type || !['PUT', 'CALL'].includes(params.type)) missing.push('--type (PUT|CALL)');
  if (!params.strike && !params.strikes) missing.push('--strike or --strikes');
  if (!params.expiry || isNaN(params.expiry)) missing.push('--expiry (unix timestamp)');
  if (!params.contracts || isNaN(params.contracts)) missing.push('--contracts (amount)');
  if (!params.direction || !['buy', 'sell'].includes(params.direction)) missing.push('--direction (buy|sell)');

  if (missing.length > 0) {
    console.error(JSON.stringify({
      error: true,
      message: 'Missing or invalid required parameters',
      missing,
      usage: 'npx tsx build-rfq.ts --underlying <ETH|BTC> --type <PUT|CALL> --strike <price> OR --strikes <s1,s2,...> --expiry <timestamp> --contracts <amount> --direction <buy|sell>',
      examples: {
        vanilla: 'npx tsx build-rfq.ts --underlying ETH --type PUT --strike 1900 --expiry 1774684800 --contracts 1 --direction buy',
        spread: 'npx tsx build-rfq.ts --underlying ETH --type CALL --strikes 2000,2100 --expiry 1774684800 --contracts 1 --direction buy',
        butterfly: 'npx tsx build-rfq.ts --underlying ETH --type PUT --strikes 1900,1850,1800 --expiry 1774684800 --contracts 1 --direction buy',
        condor: 'npx tsx build-rfq.ts --underlying ETH --type PUT --strikes 1800,1900,2100,2200 --expiry 1774684800 --contracts 1 --direction sell',
      },
      help: {
        strike: 'Single strike for vanilla options (PUT or CALL)',
        strikes: 'Comma-separated strikes for multi-strike: 2=spread, 3=butterfly, 4=condor',
        strikeOrdering: 'PUT: descending (1900,1800). CALL: ascending (2000,2100). Condor: always ascending.',
        deadline: `Default: ${DEFAULT_DEADLINE_MINUTES * 60} seconds. Override with --deadline <minutes>`,
      },
    }, null, 2));
    return null;
  }

  return params as RFQParams;
}

async function main() {
  const args = process.argv.slice(2);
  const params = parseArgs(args);

  if (!params) {
    process.exit(1);
  }

  // Determine strikes array
  const strikes = params.strikes || [params.strike!];
  const strikeCount = strikes.length;

  // Validate strike count
  if (![1, 2, 3, 4].includes(strikeCount)) {
    console.error(JSON.stringify({
      error: true,
      message: `Invalid strike count: ${strikeCount}. Must be 1 (vanilla), 2 (spread), 3 (butterfly), or 4 (condor).`,
      strikes,
    }, null, 2));
    process.exit(1);
  }

  // Validate strike ordering
  const orderingResult = validateStrikeOrdering(strikes, params.type);
  if (!orderingResult.valid) {
    console.error(JSON.stringify({
      error: true,
      message: orderingResult.message,
      strikes,
      optionType: params.type,
    }, null, 2));
    process.exit(1);
  }

  // Determine structure type
  const structureType = getStructureType(strikeCount, params.type);

  const provider = new JsonRpcProvider(RPC_URL);
  const client = new ThetanutsClient({
    chainId: CHAIN_ID,
    provider,
  });

  try {
    // Use a placeholder address if requester not provided
    const requesterAddress = params.requester || '0x0000000000000000000000000000000000000001';

    // Determine correct collateral based on option type:
    // - PUT options use USDC (quote asset)
    // - CALL options (INVERSE_CALL) use WETH (base asset)
    // - Multi-strike structures typically use USDC
    const defaultCollateral = params.type === 'CALL' && strikeCount === 1 ? 'WETH' : 'USDC';
    const collateralToken = params.collateral || defaultCollateral;

    // Build RFQ request
    const rfqRequest = client.optionFactory.buildRFQRequest({
      requester: requesterAddress as `0x${string}`,
      underlying: params.underlying,
      optionType: params.type,
      strikes: strikeCount === 1 ? strikes[0] : strikes,
      expiry: params.expiry,
      numContracts: params.contracts,
      isLong: params.direction === 'buy',
      collateralToken,
      offerDeadlineMinutes: params.deadlineMinutes || DEFAULT_DEADLINE_MINUTES,
    });

    // Encode the transaction
    const encoded = client.optionFactory.encodeRequestForQuotation(rfqRequest);

    // Format ticker
    const expiryDate = new Date(params.expiry * 1000);
    const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'];
    const day = expiryDate.getUTCDate();
    const month = months[expiryDate.getUTCMonth()];
    const year = expiryDate.getUTCFullYear().toString().slice(-2);

    const strikeStr = strikeCount === 1
      ? `${strikes[0]}`
      : strikes.join('/');
    const ticker = `${params.underlying}-${day}${month}${year}-${strikeStr}-${params.type === 'PUT' ? 'P' : 'C'}`;

    const deadlineSeconds = (params.deadlineMinutes || DEFAULT_DEADLINE_MINUTES) * 60;

    const result = {
      rfq: {
        ticker,
        underlying: params.underlying,
        type: params.type,
        structureType,
        strikes,
        strikeCount,
        expiry: params.expiry,
        expiryDate: expiryDate.toISOString(),
        contracts: params.contracts,
        direction: params.direction,
        isBuy: params.direction === 'buy',
        collateral: collateralToken,
        deadlineSeconds,
        collateralNote: strikeCount === 1 && params.type === 'CALL'
          ? 'INVERSE_CALL requires WETH collateral'
          : 'This structure uses USDC collateral',
      },
      transaction: {
        to: encoded.to,
        data: encoded.data,
        value: '0',
      },
      instructions: [
        'This transaction data is ready to be signed and sent.',
        'Use your wallet (MetaMask, etc.) to sign and broadcast.',
        'The transaction will submit an RFQ to Thetanuts market makers.',
        `Market makers have ${deadlineSeconds} seconds to respond.`,
      ],
      timestamp: new Date().toISOString(),
    };

    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error(JSON.stringify({
      error: true,
      message: error instanceof Error ? error.message : 'Unknown error',
      params,
      structureType,
      strikes,
      timestamp: new Date().toISOString(),
    }, null, 2));
    process.exit(1);
  }
}

main();
