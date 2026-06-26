/**
 * Shadow Binance Bot - Shadow Strategy Simulator
 * Simulates alternative trading strategies to compare with real performance
 */

/**
 * Simulate improved Risk:Reward strategy
 * @param {object} analysis - Real trading analysis
 * @param {number} targetRR - Target risk:reward ratio
 * @returns {object} - Simulated results
 */
function simulateImprovedRiskReward(analysis, targetRR = 4) {
  const realTrades = analysis.trades.total;
  const realWinRate = parseFloat(analysis.trades.winRate) / 100;
  const avgLoss = parseFloat(analysis.averages.avgLoss);

  // Simulate with better R:R
  const avgWin = avgLoss * targetRR;

  const wins = Math.round(realTrades * realWinRate);
  const losses = realTrades - wins;

  const simulatedPnL = (wins * avgWin) + (losses * avgLoss);
  const improvement = simulatedPnL - parseFloat(analysis.pnl.realized);

  return {
    strategy: `Improved Risk:Reward (1:${targetRR})`,
    trades: realTrades,
    wins,
    losses,
    winRate: analysis.trades.winRate,
    avgWin: avgWin.toFixed(4),
    avgLoss: avgLoss.toFixed(4),
    riskReward: targetRR,
    pnl: simulatedPnL.toFixed(4),
    improvement: improvement.toFixed(4),
    description: `If you used 1:${targetRR} risk:reward instead of 1:${analysis.averages.riskReward}, you could have made ${improvement > 0 ? '+' : ''}${improvement} USDT more.`
  };
}

/**
 * Simulate selective trading (only good hours)
 * @param {object} analysis - Real trading analysis
 * @param {number} minWinRate - Minimum win rate threshold
 * @returns {object} - Simulated results
 */
function simulateSelectiveTrading(analysis, minWinRate = 50) {
  const hourly = analysis.hourly;

  // Find good hours
  const goodHours = Object.entries(hourly)
    .filter(([hour, data]) => parseInt(data.winRate) >= minWinRate)
    .map(([hour, data]) => ({
      hour: parseInt(hour),
      winRate: parseInt(data.winRate),
      pnl: parseFloat(data.pnl),
      total: data.total
    }));

  if (goodHours.length === 0) {
    return {
      strategy: 'Selective Trading',
      error: 'Not enough data to simulate'
    };
  }

  // Calculate what would happen if only trading during good hours
  const goodHourPnL = goodHours.reduce((sum, h) => sum + h.pnl, 0);
  const goodHourTrades = goodHours.reduce((sum, h) => sum + h.total, 0);

  const realPnL = parseFloat(analysis.pnl.realized);
  const improvement = goodHourPnL - realPnL;

  return {
    strategy: `Selective Trading (${minWinRate}%+ win rate hours)`,
    goodHours: goodHours.map(h => `${h.hour}:00 UTC (${h.winRate}% WR)`),
    simulatedTrades: goodHourTrades,
    simulatedPnL: goodHourPnL.toFixed(4),
    realPnL: realPnL.toFixed(4),
    improvement: improvement.toFixed(4),
    description: `If you only traded during hours with ${minWinRate}%+ win rate, you could have ${improvement > 0 ? 'gained' : 'lost'} ${Math.abs(improvement).toFixed(4)} USDT.`
  };
}

/**
 * Simulate reduced trading frequency
 * @param {object} analysis - Real trading analysis
 * @param {number} reductionPercent - How much to reduce trades by (0-100)
 * @returns {object} - Simulated results
 */
function simulateReducedTrading(analysis, reductionPercent = 50) {
  const realTrades = analysis.trades.total;
  const reducedTrades = Math.round(realTrades * (1 - reductionPercent / 100));

  const realWinRate = parseFloat(analysis.trades.winRate) / 100;
  const avgWin = parseFloat(analysis.averages.avgWin);
  const avgLoss = parseFloat(analysis.averages.avgLoss);

  // Calculate real PnL per trade
  const pnlPerTrade = parseFloat(analysis.pnl.realized) / realTrades;

  // Simulate reduced trades
  const wins = Math.round(reducedTrades * realWinRate);
  const losses = reducedTrades - wins;
  const simulatedPnL = (wins * avgWin) + (losses * avgLoss);

  // Also account for reduced commission
  const realCommission = parseFloat(analysis.trades.commissions);
  const reducedCommission = realCommission * (1 - reductionPercent / 100);
  const commissionSavings = realCommission - reducedCommission;

  const totalImprovement = (simulatedPnL - parseFloat(analysis.pnl.realized)) + commissionSavings;

  return {
    strategy: `Reduced Trading (-${reductionPercent}% trades)`,
    originalTrades: realTrades,
    simulatedTrades: reducedTrades,
    reduction: `${reductionPercent}%`,
    originalPnL: analysis.pnl.realized,
    simulatedPnL: simulatedPnL.toFixed(4),
    commissionSavings: commissionSavings.toFixed(4),
    improvement: totalImprovement.toFixed(4),
    description: `If you made ${reductionPercent}% fewer trades (${reducedTrades} instead of ${realTrades}), focusing only on the best setups, you could have made ${totalImprovement > 0 ? '+' : ''}${totalImprovement.toFixed(4)} USDT more.`
  };
}

/**
 * Simulate DCA (Dollar Cost Averaging) strategy
 * @param {object} analysis - Real trading analysis
 * @returns {object} - Simulated results
 */
function simulateDCA(analysis) {
  const realWinRate = parseFloat(analysis.trades.winRate) / 100;
  const realTrades = analysis.trades.total;
  const avgWin = parseFloat(analysis.averages.avgWin);
  const avgLoss = parseFloat(analysis.averages.avgLoss);

  // DCA improves win rate by averaging into positions
  const dcaWinRate = Math.min(realWinRate + 0.15, 0.7); // Cap at 70%

  const wins = Math.round(realTrades * dcaWinRate);
  const losses = realTrades - wins;

  // DCA also reduces average loss (better entries = smaller stops)
  const improvedAvgLoss = avgLoss * 0.8; // 20% smaller losses
  const improvedAvgWin = avgWin * 1.1;   // 10% bigger wins

  const simulatedPnL = (wins * improvedAvgWin) + (losses * improvedAvgLoss);
  const improvement = simulatedPnL - parseFloat(analysis.pnl.realized);

  return {
    strategy: 'DCA (Dollar Cost Averaging)',
    originalWinRate: `${(realWinRate * 100).toFixed(0)}%`,
    simulatedWinRate: `${(dcaWinRate * 100).toFixed(0)}%`,
    improvement: 'Win rate +15%, Loss -20%, Win +10%',
    pnl: simulatedPnL.toFixed(4),
    improvementPnL: improvement.toFixed(4),
    description: `Using DCA to split entries into 3 parts at different prices could improve your win rate to ${(dcaWinRate * 100).toFixed(0)}% and reduce average losses. Potential improvement: ${improvement > 0 ? '+' : ''}${improvement.toFixed(4)} USDT.`
  };
}

/**
 * Generate comprehensive shadow comparison
 * @param {object} analysis - Real trading analysis
 * @returns {object} - All simulations
 */
function generateShadowComparison(analysis) {
  return {
    original: {
      pnl: parseFloat(analysis.pnl.realized),
      winRate: parseFloat(analysis.trades.winRate),
      riskReward: parseFloat(analysis.averages.riskReward),
      totalTrades: analysis.trades.total
    },
    strategies: [
      simulateImprovedRiskReward(analysis, 4),
      simulateSelectiveTrading(analysis, 50),
      simulateReducedTrading(analysis, 50),
      simulateDCA(analysis)
    ]
  };
}

/**
 * Generate Spot shadow comparison
 * @param {object} spotAnalysis - Spot analysis results
 * @returns {object} - Spot shadow strategies
 */
function generateSpotShadowComparison(spotAnalysis) {
  return {
    original: {
      totalTrades: spotAnalysis.totalTrades,
      totalVolume: parseFloat(spotAnalysis.totalVolume),
      totalSymbols: spotAnalysis.totalSymbols
    },
    strategies: [
      simulateSpotDCA(spotAnalysis),
      simulateSpotHold(spotAnalysis)
    ]
  };
}

/**
 * Simulate DCA strategy for Spot
 * @param {object} spotAnalysis - Spot analysis results
 * @returns {object} - Simulated DCA results
 */
function simulateSpotDCA(spotAnalysis) {
  if (spotAnalysis.totalTrades === 0) {
    return { strategy: 'DCA Strategy', error: 'No trades to simulate' };
  }

  const baseVolume = parseFloat(spotAnalysis.totalVolume) || (spotAnalysis.totalTrades * 1000);
  const improvedVolume = baseVolume * 1.15;

  return {
    strategy: 'Dollar Cost Averaging (DCA)',
    originalVolume: spotAnalysis.totalVolume || String(spotAnalysis.totalTrades * 1000),
    simulatedVolume: improvedVolume.toFixed(2),
    improvement: 'Better average entry price',
    description: 'Split your purchases into multiple buys at different prices to reduce average entry cost.'
  };
}

/**
 * Simulate Hold strategy for Spot
 * @param {object} spotAnalysis - Spot analysis results
 * @returns {object} - Simulated Hold results
 */
function simulateSpotHold(spotAnalysis) {
  if (spotAnalysis.totalTrades === 0) {
    return { strategy: 'Hold Strategy', error: 'No trades to simulate' };
  }

  const activeTrades = spotAnalysis.totalTrades;
  const holdingTrades = Math.ceil(activeTrades * 0.2);

  return {
    strategy: 'Buy and Hold',
    originalTrades: activeTrades,
    simulatedTrades: holdingTrades,
    reduction: `${Math.round((1 - holdingTrades / activeTrades) * 100)}%`,
    improvement: 'Less fees, less emotional trading',
    description: `Instead of ${activeTrades} trades, only make ${holdingTrades} well-researched trades per year.`
  };
}

module.exports = {
  simulateImprovedRiskReward,
  simulateSelectiveTrading,
  simulateReducedTrading,
  simulateDCA,
  generateShadowComparison,
  generateSpotShadowComparison,
  simulateSpotDCA,
  simulateSpotHold
};
