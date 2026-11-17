#!/usr/bin/env node

function parseArgs(argv) {
  const values = {};
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (token === '--self-test') {
      values.selfTest = true;
      continue;
    }
    if (!token.startsWith('--')) {
      throw new Error(`Unexpected argument: ${token}`);
    }
    const key = token.slice(2);
    const value = argv[index + 1];
    if (value === undefined || value.startsWith('--')) {
      throw new Error(`Missing value for --${key}`);
    }
    values[key] = value;
    index += 1;
  }
  return values;
}

function finiteNumber(value, name) {
  const number = Number(value);
  if (!Number.isFinite(number)) {
    throw new Error(`${name} must be a finite number.`);
  }
  return number;
}

function round(value, decimals = 8) {
  const factor = 10 ** decimals;
  return Math.round((value + Number.EPSILON) * factor) / factor;
}

function buildGrid({ price, lower, upper, levels }) {
  if (!(price > 0 && lower > 0 && upper > lower)) {
    throw new Error('Require positive prices and upper > lower.');
  }
  if (price < lower || price > upper) {
    throw new Error('Starting price must be inside the grid range.');
  }
  if (!Number.isInteger(levels) || levels < 2 || levels > 100) {
    throw new Error('levels must be an integer from 2 to 100.');
  }
  const spacing = (upper - lower) / (levels - 1);
  const prices = Array.from(
    { length: levels },
    (_, index) => round(lower + spacing * index)
  );
  return { spacing: round(spacing), prices };
}

function simulatePath({ path, gridPrices, amount, feeRate }) {
  const lots = [];
  const events = [];
  let grossPnl = 0;
  let fees = 0;
  let buys = 0;
  let sells = 0;

  for (let index = 1; index < path.length; index += 1) {
    const previous = path[index - 1];
    const current = path[index];
    if (current < previous) {
      const crossed = gridPrices
        .filter((grid) => current <= grid && grid < previous)
        .sort((a, b) => b - a);
      for (const grid of crossed) {
        lots.push({ price: grid, amount });
        fees += grid * amount * feeRate;
        buys += 1;
        events.push({ action: 'buy', price: grid, amount });
      }
    } else if (current > previous) {
      const crossed = gridPrices
        .filter((grid) => previous < grid && grid <= current)
        .sort((a, b) => a - b);
      for (const grid of crossed) {
        let lotIndex = -1;
        let highestBuy = -Infinity;
        for (let candidate = 0; candidate < lots.length; candidate += 1) {
          if (lots[candidate].price < grid && lots[candidate].price > highestBuy) {
            highestBuy = lots[candidate].price;
            lotIndex = candidate;
          }
        }
        if (lotIndex === -1) continue;
        const [lot] = lots.splice(lotIndex, 1);
        grossPnl += (grid - lot.price) * amount;
        fees += grid * amount * feeRate;
        sells += 1;
        events.push({
          action: 'sell',
          price: grid,
          amount,
          matchedBuyPrice: lot.price,
          grossPnl: round((grid - lot.price) * amount)
        });
      }
    }
  }

  return {
    buys,
    sells,
    openLots: lots.length,
    endingBaseInventory: round(lots.length * amount),
    grossPnl: round(grossPnl),
    modeledFees: round(fees),
    netPnl: round(grossPnl - fees),
    events
  };
}

export function simulate(input) {
  const price = finiteNumber(input.price, 'price');
  const levels = finiteNumber(input.levels, 'levels');
  const amount = finiteNumber(input.amount, 'amount');
  const feeBps = finiteNumber(input.feeBps, 'fee-bps');
  if (amount <= 0) throw new Error('amount must be positive.');
  if (feeBps < 0 || feeBps > 1000) {
    throw new Error('fee-bps must be between 0 and 1000.');
  }

  let lower;
  let upper;
  if (input.rangePercent !== undefined) {
    const rangePercent = finiteNumber(input.rangePercent, 'range-percent');
    if (rangePercent <= 0 || rangePercent > 90) {
      throw new Error('range-percent must be greater than 0 and at most 90.');
    }
    lower = price * (1 - rangePercent / 100);
    upper = price * (1 + rangePercent / 100);
  } else {
    lower = finiteNumber(input.lower, 'lower');
    upper = finiteNumber(input.upper, 'upper');
  }

  const grid = buildGrid({ price, lower, upper, levels });
  const buyPrices = grid.prices.filter((gridPrice) => gridPrice < price);
  const sellPrices = grid.prices.filter((gridPrice) => gridPrice > price);
  const feeRate = feeBps / 10_000;

  let pathSummary = null;
  if (input.path !== undefined) {
    const path = String(input.path)
      .split(',')
      .map((value) => finiteNumber(value.trim(), 'path price'));
    if (path.length < 2 || path.some((value) => value <= 0)) {
      throw new Error('path must contain at least two positive prices.');
    }
    pathSummary = simulatePath({
      path,
      gridPrices: grid.prices,
      amount,
      feeRate
    });
  }

  return {
    disclaimer: 'Not investment advice.',
    mode: 'offline-simulation-only',
    inputs: {
      symbol: input.symbol || 'UNSPECIFIED',
      startingPrice: round(price),
      lowerPrice: round(lower),
      upperPrice: round(upper),
      levels,
      amountPerGrid: amount,
      feeBps
    },
    grid: {
      spacing: grid.spacing,
      prices: grid.prices
    },
    reserveEstimates: {
      quoteForBuysBelowStart: round(
        buyPrices.reduce((total, gridPrice) => total + gridPrice * amount, 0)
      ),
      baseForSellsAboveStart: round(sellPrices.length * amount),
      buyGridCount: buyPrices.length,
      sellGridCount: sellPrices.length
    },
    pathSimulation: pathSummary,
    limitations: [
      'Hypothetical fills occur exactly at grid prices.',
      'Spread, slippage, latency, partial fills, funding, liquidation, outages, minimum-order rules, and tax are excluded.',
      'No exchange, wallet, account, or live market is connected.',
      'Results are scenarios, not forecasts or verified performance.'
    ]
  };
}

function runSelfTest() {
  const result = simulate({
    symbol: 'BTC/USDT',
    price: '100',
    rangePercent: '10',
    levels: '5',
    amount: '1',
    feeBps: '10',
    path: '100,90,110'
  });
  if (result.grid.prices.length !== 5) throw new Error('grid length test failed');
  if (result.inputs.lowerPrice !== 90) throw new Error('lower range test failed');
  if (result.inputs.upperPrice !== 110) throw new Error('upper range test failed');
  if (!result.pathSimulation || result.pathSimulation.buys < 1) {
    throw new Error('path buy test failed');
  }
  if (result.pathSimulation.sells < 1) throw new Error('path sell test failed');
  if (result.mode !== 'offline-simulation-only') throw new Error('mode test failed');
  console.log('self-test passed');
}

try {
  const args = parseArgs(process.argv.slice(2));
  if (args.selfTest) {
    runSelfTest();
  } else {
    const result = simulate({
      symbol: args.symbol,
      price: args.price,
      lower: args.lower,
      upper: args.upper,
      rangePercent: args['range-percent'],
      levels: args.levels,
      amount: args.amount,
      feeBps: args['fee-bps'] ?? '10',
      path: args.path
    });
    process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  }
} catch (error) {
  process.stderr.write(`Error: ${error.message}\n`);
  process.exitCode = 1;
}
