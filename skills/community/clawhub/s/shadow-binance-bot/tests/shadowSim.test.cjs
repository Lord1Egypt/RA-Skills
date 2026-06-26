/**
 * Unit tests for shadowSim.cjs
 */

const {
  simulateImprovedRiskReward,
  simulateSelectiveTrading,
  simulateReducedTrading,
  simulateDCA,
  simulateSpotDCA,
  simulateSpotHold
} = require('../src/shadowSim.cjs');

const MOCK_ANALYSIS = {
  trades: {
    total: 10,
    winRate: '60',
    commissions: '5.00'
  },
  pnl: {
    realized: '300.00'
  },
  averages: {
    avgWin: '60.00',
    avgLoss: '30.00',
    riskReward: '2.00'
  },
  hourly: {
    '2': { total: 3, winRate: 33, pnl: '-10.00' },
    '8': { total: 5, winRate: 80, pnl: '150.00' },
    '14': { total: 4, winRate: 50, pnl: '20.00' },
    '20': { total: 2, winRate: 100, pnl: '100.00' }
  }
};

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

console.log('Running shadowSim.cjs tests...\n');

// Test: simulateImprovedRiskReward
const rrResult = simulateImprovedRiskReward(MOCK_ANALYSIS, 4);
assert(rrResult.strategy.includes('1:4'), `Strategy should mention 1:4, got: ${rrResult.strategy}`);
assert(rrResult.wins === 6, `Should have 6 wins (60% of 10), got ${rrResult.wins}`);
assert(rrResult.losses === 4, `Should have 4 losses, got ${rrResult.losses}`);
assert(parseFloat(rrResult.pnl) > 300, `Simulated PnL should exceed real PnL (300), got ${rrResult.pnl}`);
assert(rrResult.improvement !== undefined, 'Should have improvement value');
assert(rrResult.description.length > 0, 'Should have a description');

// Test: simulateSelectiveTrading
const selResult = simulateSelectiveTrading(MOCK_ANALYSIS, 50);
assert(selResult.error === undefined, `Should not have error, got: ${selResult.error}`);
assert(selResult.strategy.includes('Selective'), 'Should mention Selective Trading');
assert(Array.isArray(selResult.goodHours), 'Should have goodHours array');
assert(selResult.goodHours.length >= 2, `Should have >= 2 good hours, got ${selResult.goodHours.length}`);
assert(selResult.simulatedPnL !== undefined, 'Should have simulatedPnL');
assert(parseFloat(selResult.realPnL) === 300, `Real PnL should be 300, got ${selResult.realPnL}`);
assert(selResult.simulatedTrades !== undefined, 'Should have simulatedTrades field');
assert(selResult.simulatedTrades >= 0, `simulatedTrades should be >= 0, got ${selResult.simulatedTrades}`);
assert(selResult.description.length > 0, 'Should have a description');

// Test: simulateSelectiveTrading with no good hours
const emptyResult = simulateSelectiveTrading({ hourly: {} }, 90);
assert(emptyResult.error === 'Not enough data to simulate', 'Should error when no good hours');

// Test: simulateSelectiveTrading with low threshold
const allResult = simulateSelectiveTrading(MOCK_ANALYSIS, 0);
assert(allResult.error === undefined, 'Should not error with 0 threshold');

// Test: simulateReducedTrading
const redResult = simulateReducedTrading(MOCK_ANALYSIS, 50);
assert(redResult.strategy.includes('50%'), 'Should mention 50% reduction');
assert(redResult.originalTrades === 10, `Original trades should be 10, got ${redResult.originalTrades}`);
assert(redResult.simulatedTrades === 5, `Simulated trades should be 5, got ${redResult.simulatedTrades}`);
assert(redResult.reduction === '50%', `Reduction should be 50%, got ${redResult.reduction}`);
assert(redResult.originalPnL === '300.00', `Original PnL should be 300.00, got ${redResult.originalPnL}`);
assert(redResult.commissionSavings !== undefined, 'Should have commission savings');
assert(redResult.improvement !== undefined, 'Should have improvement value');
assert(redResult.description.length > 0, 'Should have a description');

// Test: simulateDCA
const dcaResult = simulateDCA(MOCK_ANALYSIS);
assert(dcaResult.strategy.includes('DCA'), 'Should mention DCA');
assert(dcaResult.originalWinRate === '60%', `Original win rate should be 60%, got ${dcaResult.originalWinRate}`);
assert(parseFloat(dcaResult.simulatedWinRate.replace('%', '')) > 60, 'Simulated win rate should improve');
assert(dcaResult.improvementPnL !== undefined, 'Should have improvement PnL');
assert(dcaResult.description.length > 0, 'Should have a description');

// Test: simulateSpotDCA with trades
const spotDCA = simulateSpotDCA({ totalTrades: 10 });
assert(spotDCA.strategy.includes('DCA'), 'Should mention DCA');
assert(spotDCA.originalVolume !== undefined, 'Should have original volume');
assert(spotDCA.simulatedVolume !== undefined, 'Should have simulated volume');
assert(parseFloat(spotDCA.simulatedVolume) > parseFloat(spotDCA.originalVolume), `Simulated volume should be higher: ${spotDCA.simulatedVolume} vs ${spotDCA.originalVolume}`);
assert(spotDCA.description.length > 0, 'Should have a description');

// Test: simulateSpotDCA with no trades
const emptyDCA = simulateSpotDCA({ totalTrades: 0 });
assert(emptyDCA.error !== undefined, 'Should error with no trades');

// Test: simulateSpotHold with trades
const holdResult = simulateSpotHold({ totalTrades: 50 });
assert(holdResult.strategy.includes('Hold'), 'Should mention Hold');
assert(holdResult.originalTrades === 50, `Original trades should be 50, got ${holdResult.originalTrades}`);
assert(holdResult.simulatedTrades < holdResult.originalTrades, 'Simulated trades should be fewer');
assert(holdResult.reduction !== undefined, 'Should have reduction percentage');
assert(holdResult.description.length > 0, 'Should have a description');

// Test: simulateSpotHold with no trades
const emptyHold = simulateSpotHold({ totalTrades: 0 });
assert(emptyHold.error !== undefined, 'Should error with no trades');

// Test: generateShadowComparison (integration)
const shadow = require('../src/shadowSim.cjs').generateShadowComparison(MOCK_ANALYSIS);
assert(shadow.original !== undefined, 'Should have original stats');
assert(Array.isArray(shadow.strategies), 'Should have strategies array');
assert(shadow.strategies.length === 4, `Should have 4 strategies, got ${shadow.strategies.length}`);
assert(shadow.original.pnl === 300, `Original PnL should be 300, got ${shadow.original.pnl}`);
assert(shadow.original.winRate === 60, `Original win rate should be 60, got ${shadow.original.winRate}`);

console.log(`\n${'='.repeat(40)}`);
console.log(`Results: ${testsPassed} passed, ${testsFailed} failed`);
console.log(`${'='.repeat(40)}`);

process.exit(testsFailed > 0 ? 1 : 0);
