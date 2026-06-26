#!/usr/bin/env node
/**
 * Aggressive Trading Strategy
 * Goal: 30%+ profit in 1 week
 *
 * Strategy:
 * - Day 1 (Mon): All-in NVDA
 * - Take profit: +10%
 * - Stop loss: -5%
 * - Daily swing trading
 */

const { execSync } = require("child_process");

function exec(cmd) {
  try {
    return execSync(cmd, { cwd: __dirname, encoding: "utf8" });
  } catch (err) {
    return err.stdout || err.message;
  }
}

async function getAccountBalance() {
  const output = exec("node trading.js account");
  const match = output.match(/Cash: \$([0-9,.]+)/);
  return match ? parseFloat(match[1].replace(/,/g, "")) : 0;
}

async function getCurrentPrice(symbol) {
  const output = exec(`node trading.js quote ${symbol}`);
  const match = output.match(/Last: \$([0-9.]+)/);
  return match ? parseFloat(match[1]) : 0;
}

async function buyMaxShares(symbol) {
  const cash = await getAccountBalance();
  const price = await getCurrentPrice(symbol);
  const shares = Math.floor(cash / price);

  console.log(`💰 Cash: $${cash.toFixed(2)}`);
  console.log(`📊 ${symbol} Price: $${price.toFixed(2)}`);
  console.log(`🛒 Buying ${shares} shares (~$${(shares * price).toFixed(2)})`);

  if (shares > 0) {
    const result = exec(`node trading.js buy ${symbol} ${shares}`);
    console.log(result);
    return { shares, price, total: shares * price };
  }
  return null;
}

async function checkPositionAndTakeProfitStopLoss(symbol, targetProfit = 0.1, stopLoss = 0.05) {
  const posOutput = exec("node trading.js positions");

  // Parse position
  const symbolMatch = posOutput.match(new RegExp(`${symbol}: (\\d+) shares`));
  const pnlMatch = posOutput.match(/P&L: \$([0-9.-]+) \(([0-9.-]+)%\)/);

  if (!symbolMatch || !pnlMatch) {
    console.log("⏸  No position or unable to parse");
    return false;
  }

  const shares = parseInt(symbolMatch[1]);
  const pnlPct = parseFloat(pnlMatch[2]) / 100;

  console.log(`📊 Position: ${shares} shares, P&L: ${(pnlPct * 100).toFixed(2)}%`);

  // Take profit
  if (pnlPct >= targetProfit) {
    console.log(`🎉 Target reached! Taking profit at +${(pnlPct * 100).toFixed(2)}%`);
    exec(`node trading.js sell ${symbol} ${shares}`);
    return true;
  }

  // Stop loss
  if (pnlPct <= -stopLoss) {
    console.log(`🛑 Stop loss triggered at ${(pnlPct * 100).toFixed(2)}%`);
    exec(`node trading.js sell ${symbol} ${shares}`);
    return true;
  }

  return false;
}

async function dailyReport() {
  console.log("\n📊 Daily Report:");
  exec("node trading.js account");
  exec("node trading.js positions");
}

// Main
(async () => {
  const action = process.argv[2];

  if (action === "buy-nvda") {
    console.log("🚀 Executing: Buy max NVDA");
    await buyMaxShares("NVDA");
  } else if (action === "check-and-exit") {
    console.log("🔍 Checking position...");
    await checkPositionAndTakeProfitStopLoss("NVDA", 0.1, 0.05);
  } else if (action === "report") {
    await dailyReport();
  } else {
    console.log("Usage:");
    console.log("  node aggressive-strategy.js buy-nvda         - Buy max NVDA");
    console.log("  node aggressive-strategy.js check-and-exit   - Check take-profit/stop-loss");
    console.log("  node aggressive-strategy.js report           - Daily report");
  }
})();
