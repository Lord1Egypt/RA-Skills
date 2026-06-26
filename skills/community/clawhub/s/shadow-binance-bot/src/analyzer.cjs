/**
 * Shadow Binance Bot - Trade Analyzer
 * Analyzes trading history and generates statistics
 */

/**
 * Analyze futures income history
 * @param {array} incomeHistory - Array of income events from Binance
 * @returns {object} - Analysis results
 */
function analyzeFuturesIncome(incomeHistory) {
  // Filter only realized PnL
  const pnlTrades = incomeHistory.filter(i => i.incomeType === 'REALIZED_PNL');
  const commissions = incomeHistory.filter(i => i.incomeType === 'COMMISSION');
  const fundingFees = incomeHistory.filter(i => i.incomeType === 'FUNDING_FEE');
  const transfers = incomeHistory.filter(i => i.incomeType === 'TRANSFER');

  // Calculate totals
  const totalRealizedPnL = pnlTrades.reduce((sum, i) => sum + parseFloat(i.income), 0);
  const totalCommission = commissions.reduce((sum, i) => sum + parseFloat(i.income), 0);
  const totalFunding = fundingFees.reduce((sum, i) => sum + parseFloat(i.income), 0);
  const totalTransfers = transfers.reduce((sum, i) => sum + parseFloat(i.income), 0);

  // Win/Loss analysis
  const wins = pnlTrades.filter(t => parseFloat(t.income) > 0);
  const losses = pnlTrades.filter(t => parseFloat(t.income) < 0);

  const winCount = wins.length;
  const lossCount = losses.length;
  const totalTrades = winCount + lossCount;
  const winRate = totalTrades > 0 ? (winCount / totalTrades) * 100 : 0;

  // Average win/loss
  const avgWin = winCount > 0
    ? wins.reduce((sum, t) => sum + parseFloat(t.income), 0) / winCount
    : 0;
  const avgLoss = lossCount > 0
    ? losses.reduce((sum, t) => sum + parseFloat(t.income), 0) / lossCount
    : 0;

  // Risk:Reward ratio
  const riskReward = avgLoss !== 0 ? Math.abs(avgWin / avgLoss) : 0;

  // Time analysis (by hour UTC)
  const hourlyStats = analyzeByHour(pnlTrades);

  // Streak analysis
  const streakStats = analyzeStreaks(pnlTrades);

  // Daily PnL
  const dailyPnL = analyzeDailyPnL(pnlTrades);

  // Date range
  const dates = incomeHistory.map(i => i.time).sort();
  const startDate = dates.length > 0 ? new Date(dates[0]) : null;
  const endDate = dates.length > 0 ? new Date(dates[dates.length - 1]) : null;

  return {
    period: {
      start: startDate ? startDate.toISOString().split('T')[0] : 'N/A',
      end: endDate ? endDate.toISOString().split('T')[0] : 'N/A',
      days: startDate && endDate
        ? Math.ceil((endDate - startDate) / (1000 * 60 * 60 * 24))
        : 0
    },
    trades: {
      total: totalTrades,
      wins: winCount,
      losses: lossCount,
      winRate: winRate.toFixed(1),
      commissions: totalCommission.toFixed(4),
      funding: totalFunding.toFixed(4)
    },
    pnl: {
      realized: totalRealizedPnL.toFixed(4),
      net: (totalRealizedPnL + totalCommission + totalFunding).toFixed(4),
      transfers: totalTransfers.toFixed(4)
    },
    averages: {
      avgWin: avgWin.toFixed(4),
      avgLoss: avgLoss.toFixed(4),
      riskReward: riskReward.toFixed(2)
    },
    streaks: streakStats,
    hourly: hourlyStats,
    daily: dailyPnL
  };
}

/**
 * Analyze trades by hour of day
 * @param {array} pnlTrades - Array of PnL trades (never mutated)
 * @returns {object} - Hourly statistics
 */
function analyzeByHour(pnlTrades) {
  const hourly = {};

  pnlTrades.forEach(trade => {
    const hour = new Date(trade.time).getUTCHours();
    const amount = parseFloat(trade.income);

    if (!hourly[hour]) {
      hourly[hour] = { wins: 0, losses: 0, pnl: 0, total: 0, winRate: 0, trades: [] };
    }

    hourly[hour].pnl += amount;
    hourly[hour].trades.push(amount);

    if (amount > 0) hourly[hour].wins++;
    else hourly[hour].losses++;
  });

  // Calculate win rates and finalize
  Object.keys(hourly).forEach(hour => {
    const h = hourly[hour];
    h.total = h.wins + h.losses;
    h.winRate = h.total > 0 ? ((h.wins / h.total) * 100).toFixed(0) : '0';
    h.pnl = h.pnl.toFixed(4);
    // Remove internal trades array before returning
    delete h.trades;
  });

  return hourly;
}

/**
 * Analyze win/loss streaks
 * @param {array} pnlTrades - Array of PnL trades
 * @returns {object} - Streak statistics
 */
function analyzeStreaks(pnlTrades) {
  // Sort by time
  const sorted = [...pnlTrades].sort((a, b) => a.time - b.time);

  let maxWinStreak = 0;
  let maxLossStreak = 0;
  let tempWinStreak = 0;
  let tempLossStreak = 0;

  sorted.forEach(trade => {
    const isWin = parseFloat(trade.income) > 0;

    if (isWin) {
      tempWinStreak++;
      tempLossStreak = 0;
      maxWinStreak = Math.max(maxWinStreak, tempWinStreak);
    } else {
      tempLossStreak++;
      tempWinStreak = 0;
      maxLossStreak = Math.max(maxLossStreak, tempLossStreak);
    }
  });

  return { maxWinStreak, maxLossStreak };
}

/**
 * Analyze daily PnL
 * @param {array} pnlTrades - Array of PnL trades
 * @returns {object} - Daily statistics
 */
function analyzeDailyPnL(pnlTrades) {
  const daily = {};

  pnlTrades.forEach(trade => {
    const date = new Date(trade.time).toLocaleDateString();
    const amount = parseFloat(trade.income);

    if (!daily[date]) {
      daily[date] = { pnl: 0, trades: 0 };
    }

    daily[date].pnl += amount;
    daily[date].trades++;
  });

  // Find best and worst days
  let bestDay = { date: '', pnl: -Infinity };
  let worstDay = { date: '', pnl: Infinity };

  Object.entries(daily).forEach(([date, data]) => {
    if (data.pnl > bestDay.pnl) bestDay = { date, pnl: data.pnl };
    if (data.pnl < worstDay.pnl) worstDay = { date, pnl: data.pnl };
  });

  return {
    days: daily,
    bestDay: { date: bestDay.date, pnl: bestDay.pnl.toFixed(4) },
    worstDay: { date: worstDay.date, pnl: worstDay.pnl.toFixed(4) }
  };
}

/**
 * Get trading behavior analysis
 * @param {object} analysis - Full analysis object
 * @returns {object} - Behavior insights
 */
function analyzeBehavior(analysis) {
  const insights = [];

  // Check win rate
  if (parseFloat(analysis.trades.winRate) < 30) {
    insights.push({
      type: 'warning',
      message: `Win rate is only ${analysis.trades.winRate}%. Aim for 40%+ to be profitable.`
    });
  }

  // Check risk:reward
  if (parseFloat(analysis.averages.riskReward) < 2) {
    insights.push({
      type: 'warning',
      message: `Risk:Reward is only 1:${analysis.averages.riskReward}. Use at least 1:3 to cover losses.`
    });
  }

  // Check loss streak
  if (analysis.streaks.maxLossStreak > 10) {
    insights.push({
      type: 'danger',
      message: `Max loss streak of ${analysis.streaks.maxLossStreak} detected! This indicates revenge trading or tilting.`
    });
  }

  // Check overtrading
  const tradesPerDay = analysis.trades.total / (analysis.period.days || 1);
  if (tradesPerDay > 3) {
    insights.push({
      type: 'warning',
      message: `You're trading ${tradesPerDay.toFixed(1)} times per day on average. Consider trading less and waiting for better setups.`
    });
  }

  // Check worst trading hours
  const hourly = analysis.hourly;
  const badHours = Object.entries(hourly)
    .filter(([h, data]) => data.winRate < 30 && data.total > 3)
    .map(([h]) => `${h}:00 UTC`);

  if (badHours.length > 0) {
    insights.push({
      type: 'tip',
      message: `Avoid trading at these hours (low win rate): ${badHours.join(', ')}`
    });
  }

  // Check best trading hours
  const goodHours = Object.entries(hourly)
    .filter(([h, data]) => data.winRate >= 60)
    .map(([h, data]) => `${h}:00 UTC (${data.winRate}% win rate)`);

  if (goodHours.length > 0) {
    insights.push({
      type: 'success',
      message: `Your best trading hours (highest win rate): ${goodHours.join(', ')}`
    });
  }

  return insights;
}

/**
 * Analyze Spot trades from multiple symbols
 * @param {object} allTrades - Object with trades grouped by symbol
 * @returns {object} - Spot analysis results
 */
function analyzeSpotTrades(allTrades) {
  // Handle the { trades, errors } shape from getAllSpotTrades
  const tradesBySymbol = (allTrades && allTrades.trades) ? allTrades.trades : allTrades;

  let totalTrades = 0;
  let totalVolume = 0;
  let totalCommission = 0;
  const symbols = Object.keys(tradesBySymbol);
  const symbolStats = {};

  symbols.forEach(symbol => {
    const trades = tradesBySymbol[symbol];
    if (!trades || trades.length === 0) return;

    let symbolVolume = 0;
    let symbolCommission = 0;
    let buys = 0;
    let sells = 0;

    trades.forEach(trade => {
      const qty = parseFloat(trade.qty);
      const price = parseFloat(trade.price);
      const commission = parseFloat(trade.commission);

      symbolVolume += qty * price;
      symbolCommission += commission;

      if (trade.isBuyer) buys++;
      else sells++;

      totalCommission += commission;
    });

    totalTrades += trades.length;
    totalVolume += symbolVolume;

    symbolStats[symbol] = {
      trades: trades.length,
      volume: symbolVolume.toFixed(2),
      buys,
      sells,
      commission: symbolCommission.toFixed(6)
    };
  });

  // Calculate average trade size
  const avgTradeSize = totalTrades > 0 ? (totalVolume / totalTrades) : 0;

  return {
    totalSymbols: symbols.length,
    totalTrades,
    totalVolume: totalVolume.toFixed(2),
    avgTradeSize: avgTradeSize.toFixed(2),
    totalCommission: totalCommission.toFixed(6),
    symbols: symbolStats
  };
}

module.exports = {
  analyzeFuturesIncome,
  analyzeBehavior,
  analyzeSpotTrades
};
