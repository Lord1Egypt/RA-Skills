#!/usr/bin/env npx tsx
/**
 * Calculate option payout at settlement from Thetanuts Finance
 * Usage: npx tsx calculate-payout.ts --type <PUT|CALL> --strike <price> --settlement <price> --contracts <amount> [--is-buyer]
 *
 * Examples:
 *   npx tsx calculate-payout.ts --type PUT --strike 2500 --settlement 2200 --contracts 1 --is-buyer
 *   npx tsx calculate-payout.ts --type CALL --strike 3000 --settlement 3500 --contracts 2
 */

import { ThetanutsClient } from '@thetanuts-finance/thetanuts-client';
import { JsonRpcProvider } from 'ethers';

const RPC_URL = process.env.THETANUTS_RPC_URL || 'https://mainnet.base.org';
const CHAIN_ID = 8453;

interface PayoutParams {
  type: 'PUT' | 'CALL';
  strike: number;
  settlement: number;
  contracts: number;
  isBuyer: boolean;
}

function parseArgs(args: string[]): PayoutParams {
  const params: Partial<PayoutParams> = {
    isBuyer: false,
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--type':
        params.type = args[++i]?.toUpperCase() as 'PUT' | 'CALL';
        break;
      case '--strike':
        params.strike = parseFloat(args[++i]);
        break;
      case '--settlement':
        params.settlement = parseFloat(args[++i]);
        break;
      case '--contracts':
        params.contracts = parseFloat(args[++i]);
        break;
      case '--is-buyer':
        params.isBuyer = true;
        break;
    }
  }

  // Validate required params
  const missing: string[] = [];
  if (!params.type || !['PUT', 'CALL'].includes(params.type)) missing.push('--type (PUT|CALL)');
  if (params.strike === undefined || isNaN(params.strike)) missing.push('--strike (price)');
  if (params.settlement === undefined || isNaN(params.settlement)) missing.push('--settlement (price)');
  if (params.contracts === undefined || isNaN(params.contracts)) missing.push('--contracts (amount)');

  if (missing.length > 0) {
    console.error(JSON.stringify({
      error: true,
      message: 'Missing or invalid required parameters',
      missing,
      usage: 'npx tsx calculate-payout.ts --type <PUT|CALL> --strike <price> --settlement <price> --contracts <amount> [--is-buyer]',
      examples: [
        'npx tsx calculate-payout.ts --type PUT --strike 2500 --settlement 2200 --contracts 1 --is-buyer',
        'npx tsx calculate-payout.ts --type CALL --strike 3000 --settlement 3500 --contracts 2',
      ],
    }, null, 2));
    process.exit(1);
  }

  return params as PayoutParams;
}

function calculatePayout(params: PayoutParams): { intrinsicValue: number; totalPayout: number; description: string } {
  let intrinsicValue = 0;
  let description = '';

  if (params.type === 'PUT') {
    // PUT: max(strike - settlement, 0)
    intrinsicValue = Math.max(params.strike - params.settlement, 0);
    if (params.settlement < params.strike) {
      description = `PUT is in-the-money: strike ($${params.strike}) > settlement ($${params.settlement})`;
    } else {
      description = `PUT is out-of-the-money: settlement ($${params.settlement}) >= strike ($${params.strike})`;
    }
  } else {
    // CALL: max(settlement - strike, 0)
    intrinsicValue = Math.max(params.settlement - params.strike, 0);
    if (params.settlement > params.strike) {
      description = `CALL is in-the-money: settlement ($${params.settlement}) > strike ($${params.strike})`;
    } else {
      description = `CALL is out-of-the-money: settlement ($${params.settlement}) <= strike ($${params.strike})`;
    }
  }

  const totalPayout = intrinsicValue * params.contracts;

  return { intrinsicValue, totalPayout, description };
}

async function main() {
  const args = process.argv.slice(2);
  const params = parseArgs(args);

  const { intrinsicValue, totalPayout, description } = calculatePayout(params);

  // Calculate scenario analysis
  const scenarios = [];
  const basePrice = params.settlement;
  const range = params.strike * 0.2; // 20% range

  for (let pct = -20; pct <= 20; pct += 5) {
    const scenarioPrice = Math.round(basePrice * (1 + pct / 100));
    const scenarioParams = { ...params, settlement: scenarioPrice };
    const scenarioPayout = calculatePayout(scenarioParams);
    scenarios.push({
      settlementPrice: scenarioPrice,
      change: `${pct >= 0 ? '+' : ''}${pct}%`,
      intrinsicValue: scenarioPayout.intrinsicValue,
      totalPayout: scenarioPayout.totalPayout,
      status: scenarioPayout.intrinsicValue > 0 ? 'ITM' : 'OTM',
    });
  }

  const result = {
    input: {
      type: params.type,
      strike: params.strike,
      settlementPrice: params.settlement,
      contracts: params.contracts,
      side: params.isBuyer ? 'BUYER' : 'SELLER',
    },
    payout: {
      intrinsicValuePerContract: intrinsicValue,
      totalPayout: totalPayout,
      payoutTo: params.isBuyer ? 'BUYER receives' : 'SELLER pays',
      description,
    },
    formula: params.type === 'PUT'
      ? `PUT payout = max(strike - settlement, 0) * contracts = max($${params.strike} - $${params.settlement}, 0) * ${params.contracts} = $${totalPayout}`
      : `CALL payout = max(settlement - strike, 0) * contracts = max($${params.settlement} - $${params.strike}, 0) * ${params.contracts} = $${totalPayout}`,
    scenarioAnalysis: scenarios,
    timestamp: new Date().toISOString(),
  };

  console.log(JSON.stringify(result, null, 2));
}

main();
