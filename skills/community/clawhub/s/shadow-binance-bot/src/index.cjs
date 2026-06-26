/**
 * Shadow Binance Bot - Main Entry Point
 * AI-powered trading coach that analyzes your Binance trades
 * and simulates alternative strategies
 *
 * Usage: node src/index.cjs
 *
 * Usage: node src/index.cjs
 *
 * Credentials: Set BINANCE_API_KEY and BINANCE_API_SECRET via:
 *   1. Environment variables (recommended — works on all platforms)
 *   2. Local config.env file (for local development)
 *   See config.env.example for all supported variables.
 */

const fs = require('fs');
const path = require('path');

// Import modules
const binance = require('./binance.cjs');
const analyzer = require('./analyzer.cjs');
const shadowSim = require('./shadowSim.cjs');
const coach = require('./coach.cjs');

// Default spot symbols — can be overridden via SPOT_SYMBOLS in config.env
const DEFAULT_SPOT_SYMBOLS = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'SHIBUSDT'];

// Load configuration.
// Priority: process.env (standard injection) > config.env (local dev override).
// Platforms that inject BINANCE_API_KEY/BINANCE_API_SECRET as environment
// variables will work automatically. Local developers can also use config.env.
function loadConfig() {
  const apiKey = process.env.BINANCE_API_KEY;
  const apiSecret = process.env.BINANCE_API_SECRET;
  const spotSymbols = process.env.SPOT_SYMBOLS;

  // If env vars are already set (platform injection), use them directly
  if (apiKey && apiSecret) {
    return { BINANCE_API_KEY: apiKey, BINANCE_API_SECRET: apiSecret, SPOT_SYMBOLS: spotSymbols || undefined };
  }

  // Otherwise fall back to local config.env for development
  const configPath = path.join(__dirname, '..', 'config.env');

  if (!fs.existsSync(configPath)) {
    console.log('Note: config.env not found. Running in Demo Mode.');
    return {};
  }

  const config = {};
  const content = fs.readFileSync(configPath, 'utf8');

  content.split('\n').forEach(line => {
    line = line.trim();
    if (line && !line.startsWith('#')) {
      const [key, value] = line.split('=');
      if (key && value) {
        config[key.trim()] = value.trim();
      }
    }
  });

  return config;
}

// Generate mock data for Demo Mode
function generateDemoData() {
  console.log('');
  console.log('+==============================================+');
  console.log('|     DEMO MODE - Using Sample Data           |');
  console.log('+==============================================+');
  console.log('');
  console.log('Note: No API keys found. Running with simulated');
  console.log('demo data to show how the bot works.');
  console.log('');

  const now = Date.now();
  const HOUR = 60 * 60 * 1000;
  const DAY = 24 * HOUR;

  // Generate 30 days of mock futures income
  const incomeHistory = [];
  let cumulativePnL = 0;
  for (let i = 0; i < 60; i++) {
    const isWin = Math.random() > 0.45; // ~55% win rate
    const amount = isWin
      ? (Math.random() * 80 + 10).toFixed(4)
      : (-(Math.random() * 30 + 5)).toFixed(4);
    cumulativePnL += parseFloat(amount);
    incomeHistory.push({
      incomeType: 'REALIZED_PNL',
      income: String(amount),
      time: now - (i * DAY * 0.5) // 60 records spread over 30 days
    });
  }

  // Add some commission and funding
  incomeHistory.push({ incomeType: 'COMMISSION', income: '-2.50', time: now - DAY });
  incomeHistory.push({ incomeType: 'FUNDING_FEE', income: '-1.20', time: now - DAY * 2 });

  // Sort by time ascending
  incomeHistory.sort((a, b) => a.time - b.time);

  // Generate mock spot trades
  const spotTrades = {
    BTCUSDT: [
      { id: 1, qty: '0.50', price: '62000', commission: '0.00025', isBuyer: true, time: now - DAY * 5 },
      { id: 2, qty: '0.30', price: '64000', commission: '0.00015', isBuyer: false, time: now - DAY * 3 },
      { id: 3, qty: '0.20', price: '61000', commission: '0.00010', isBuyer: true, time: now - DAY * 1 },
    ],
    ETHUSDT: [
      { id: 4, qty: '2.00', price: '3400', commission: '0.00100', isBuyer: true, time: now - DAY * 4 },
      { id: 5, qty: '1.50', price: '3500', commission: '0.00075', isBuyer: false, time: now - DAY * 2 },
    ]
  };

  return { incomeHistory, spotTrades, isDemo: true };
}

// Main function
async function main() {
  console.log('');
  console.log('+==============================================+');
  console.log('|     SHADOW BINANCE BOT                      |');
  console.log('|     Your Personal Trading Coach              |');
  console.log('+==============================================+');
  console.log('');

  // Load config
  const config = loadConfig();
  const { BINANCE_API_KEY, BINANCE_API_SECRET, SPOT_SYMBOLS } = config;

  // Parse spot symbols from config (comma-separated) or use defaults
  const spotSymbols = SPOT_SYMBOLS
    ? SPOT_SYMBOLS.split(',').map(s => s.trim())
    : DEFAULT_SPOT_SYMBOLS;

  // Check if running in demo mode (no API keys)
  const isDemoMode = !BINANCE_API_KEY || !BINANCE_API_SECRET;

  if (isDemoMode) {
    const { incomeHistory, spotTrades } = generateDemoData();

    // ===== DEMO FUTURES ANALYSIS =====
    console.log('============================================');
    console.log('         FUTURES ANALYSIS [DEMO]            ');
    console.log('============================================');
    console.log('');

    const futuresAnalysis = analyzer.analyzeFuturesIncome(incomeHistory);
    const futuresShadow = shadowSim.generateShadowComparison(futuresAnalysis);
    const futuresCoach = coach.generateCoachReport(futuresAnalysis, futuresShadow);
    console.log(coach.formatReport(futuresCoach));

    // ===== DEMO SPOT ANALYSIS =====
    console.log('');
    console.log('============================================');
    console.log('           SPOT ANALYSIS [DEMO]             ');
    console.log('============================================');
    console.log('');

    const spotAnalysis = analyzer.analyzeSpotTrades(spotTrades);
    const spotShadow = shadowSim.generateSpotShadowComparison(spotAnalysis);
    const spotCoach = coach.generateSpotCoachReport(spotAnalysis);
    console.log(coach.formatSpotReport(spotCoach));

    console.log('============================================');
    console.log('         END OF DEMO MODE                   ');
    console.log('============================================');
    console.log('');
    console.log('To run with your real data:');
    console.log('  1. Set BINANCE_API_KEY and BINANCE_API_SECRET');
    console.log('     - As environment variables (recommended), OR');
    console.log('     - Copy config.env.example to config.env and fill in keys');
    console.log('  2. Run: node src/index.cjs');
    console.log('');
    return;
  }

  console.log('Connecting to Binance...');

  // Test connection
  const connected = await binance.testConnection(BINANCE_API_KEY, BINANCE_API_SECRET);
  if (!connected) {
    console.error('x Failed to connect to Binance. Check your API keys.');
    process.exit(1);
  }
  console.log('Connected to Binance!');
  console.log('');

  try {
    // ===== FUTURES ANALYSIS =====
    console.log('============================================');
    console.log('         FUTURES ANALYSIS                   ');
    console.log('============================================');
    console.log('');

    console.log('Fetching Futures trading history...');
    const incomeHistory = await binance.getFuturesIncome(BINANCE_API_KEY, BINANCE_API_SECRET, 365);

    if (!incomeHistory || incomeHistory.length === 0) {
      console.log('No Futures trading history found.');
    } else {
      console.log(`   Found ${incomeHistory.length} records`);
    }
    console.log('');

    // Analyze Futures
    console.log('Analyzing Futures patterns...');
    const futuresAnalysis = analyzer.analyzeFuturesIncome(incomeHistory);

    // Shadow Simulation for Futures
    console.log('Running Futures shadow simulations...');
    const futuresShadow = shadowSim.generateShadowComparison(futuresAnalysis);

    // Generate Futures Coach Report
    const futuresCoach = coach.generateCoachReport(futuresAnalysis, futuresShadow);
    console.log('');

    // Display Futures Report
    console.log(coach.formatReport(futuresCoach));

    // ===== SPOT ANALYSIS =====
    console.log('');
    console.log('============================================');
    console.log('           SPOT ANALYSIS                    ');
    console.log('============================================');
    console.log('');

    console.log('Fetching Spot trading history...');
    const allSpotTrades = await binance.getAllSpotTrades(BINANCE_API_KEY, BINANCE_API_SECRET, spotSymbols);

    const spotAnalysis = analyzer.analyzeSpotTrades(allSpotTrades);

    console.log(`   Found ${spotAnalysis.totalTrades} trades across ${spotAnalysis.totalSymbols} symbols`);
    console.log('');

    // Spot Shadow Simulation
    console.log('Running Spot shadow simulations...');
    const spotShadow = shadowSim.generateSpotShadowComparison(spotAnalysis);

    // Spot Coaching
    console.log('Generating Spot coaching...');
    const spotCoach = coach.generateSpotCoachReport(spotAnalysis);
    console.log('');

    // Display Spot Report
    console.log(coach.formatSpotReport(spotCoach));

    // Show Spot Shadow Strategies
    if (spotAnalysis.totalTrades > 0) {
      console.log('============================================');
      console.log('      SPOT SHADOW STRATEGIES                ');
      console.log('============================================');
      spotShadow.strategies.forEach(strategy => {
        if (!strategy.error) {
          console.log('');
          console.log(`[${strategy.strategy}]`);
          console.log(`   ${strategy.description}`);
        }
      });
      console.log('');
    }

    // ===== COMBINED TOTAL =====
    const futuresNetPnL = parseFloat(futuresAnalysis.pnl.net);
    const spotVolume = parseFloat(spotAnalysis.totalVolume);

    console.log('');
    console.log('============================================');
    console.log('        COMBINED TOTAL                      ');
    console.log('============================================');
    console.log(`Futures Net PnL: ${futuresNetPnL.toFixed(4)} USDT`);
    console.log(`Spot Volume: ${spotVolume.toFixed(2)} USDT`);
    console.log('');

    if (futuresNetPnL < 0) {
      console.log('Focus on fixing your Futures trading first!');
      console.log('   - Use better Risk:Reward (1:3 minimum)');
      console.log('   - Trade during your best hours');
      console.log('   - Implement 3-loss rule');
    }

    console.log('');
    console.log('============================================');
    console.log('Keep practicing and stay disciplined!');
    console.log('============================================');

  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main().catch(console.error);
}

module.exports = { main };
