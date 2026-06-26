/**
 * Unit tests for analyzer.cjs
 */

const { analyzeFuturesIncome, analyzeBehavior, analyzeSpotTrades } = require('../src/analyzer.cjs');

const MOCK_INCOME_HISTORY = [
  { incomeType: 'REALIZED_PNL', income: '100.50', time: 1710000000000 },
  { incomeType: 'REALIZED_PNL', income: '-30.25', time: 1710003600000 },
  { incomeType: 'REALIZED_PNL', income: '200.00', time: 1710007200000 },
  { incomeType: 'REALIZED_PNL', income: '-15.75', time: 1710010800000 },
  { incomeType: 'REALIZED_PNL', income: '80.00', time: 1710014400000 },
  { incomeType: 'COMMISSION', income: '-1.50', time: 1710000000000 },
  { incomeType: 'FUNDING_FEE', income: '-0.50', time: 1710000000000 },
  { incomeType: 'TRANSFER', income: '50.00', time: 1710000000000 },
];

let testsPassed = 0;
let testsFailed = 0;

function assert(condition, message) {
  if (condition) {
    testsPassed++;
  } else {
    testsFailed++;
    console.error(`FAIL: ${message}`);
  }
}

console.log('Running analyzer.cjs tests...\n');

// Test: analyzeFuturesIncome
const result = analyzeFuturesIncome(MOCK_INCOME_HISTORY);

assert(result.trades.total === 5, 'Should count 5 PnL trades');
assert(result.trades.wins === 3, 'Should have 3 wins (100.50, 200.00, 80.00)');
assert(result.trades.losses === 2, 'Should have 2 losses (-30.25, -15.75)');
assert(result.trades.winRate === '60.0', `Win rate should be 60.0, got ${result.trades.winRate}`);

const realized = parseFloat(result.pnl.realized);
assert(realized > 334 && realized < 335, `Realized PnL should be ~334.50, got ${realized}`);

const commissions = parseFloat(result.trades.commissions);
// Commission: -0.50 (FUNDING_FEE) + -1.50 (COMMISSION) = -2.00
assert(parseFloat(result.trades.commissions) === -1.5, `Commissions should be -1.50, got ${result.trades.commissions}`);

const avgWin = parseFloat(result.averages.avgWin);
assert(avgWin > 126 && avgWin < 127, `Avg win should be ~126.83, got ${avgWin}`);

const avgLoss = parseFloat(result.averages.avgLoss);
assert(avgLoss === -23, `Avg loss should be -23.00 (negative), got ${avgLoss}`);

const rr = parseFloat(result.averages.riskReward);
assert(rr > 5.5 && rr < 5.6, `Risk:reward should be ~5.52, got ${rr}`);

assert(result.streaks.maxWinStreak === 1, `Max win streak should be 1, got ${result.streaks.maxWinStreak}`);
assert(result.streaks.maxLossStreak >= 1, `Max loss streak should be >= 1, got ${result.streaks.maxLossStreak}`);

assert(result.period.days === 1, `Period days should be 1, got ${result.period.days}`);

// Test: analyzeByHour (via hourly field)
const hourlyKeys = Object.keys(result.hourly);
assert(hourlyKeys.length > 0, 'Should have hourly breakdown entries');

// Test: analyzeSpotTrades
const MOCK_SPOT_TRADES = {
  BTCUSDT: [
    { qty: '0.5', price: '50000', commission: '0.00025', isBuyer: true },
    { qty: '0.3', price: '51000', commission: '0.00015', isBuyer: false },
    { qty: '0.2', price: '49000', commission: '0.00010', isBuyer: true },
  ],
};

const spotResult = analyzeSpotTrades(MOCK_SPOT_TRADES);
assert(spotResult.totalSymbols === 1, `Should have 1 symbol, got ${spotResult.totalSymbols}`);
assert(spotResult.totalTrades === 3, `Should have 3 trades, got ${spotResult.totalTrades}`);

const volume = parseFloat(spotResult.totalVolume);
assert(volume > 49000, `Total volume should be > 49000, got ${volume}`);

assert(spotResult.symbols.BTCUSDT.buys === 2, 'BTCUSDT should have 2 buys');
assert(spotResult.symbols.BTCUSDT.sells === 1, 'BTCUSDT should have 1 sell');

const avgSize = parseFloat(spotResult.avgTradeSize);
// (0.5*50000 + 0.3*51000 + 0.2*49000) / 3 = 49700/3 = 16566.67
assert(avgSize > 16000 && avgSize < 17000, `Avg trade size should be ~16567, got ${avgSize}`);

// Test: analyzeBehavior
const badBehavior = analyzeBehavior({
  trades: { winRate: '20', total: 30 },
  averages: { riskReward: '1.5' },
  streaks: { maxLossStreak: 15 },
  period: { days: 10 },
  hourly: {}
});

const lowWR = badBehavior.find(i => i.message.includes('Win rate'));
assert(lowWR !== undefined, 'Should flag low win rate');

const lowRR = badBehavior.find(i => i.message.includes('Risk:Reward'));
assert(lowRR !== undefined, 'Should flag low risk:reward');

const tilt = badBehavior.find(i => i.message.includes('15'));
assert(tilt !== undefined, 'Should flag loss streak > 10');

console.log(`\n${'='.repeat(40)}`);
console.log(`Results: ${testsPassed} passed, ${testsFailed} failed`);
console.log(`${'='.repeat(40)}`);

process.exit(testsFailed > 0 ? 1 : 0);
