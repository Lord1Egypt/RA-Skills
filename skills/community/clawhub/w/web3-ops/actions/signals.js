import axios from "axios";
import {
  getWallet,
  getChainConfig,
  logInfo,
  logSuccess,
  logWarning,
  logError,
  printColor,
  resolveTokenAddress
} from "./common.js";

// Map our chain name to GeckoTerminal network IDs
const GECKO_NETWORK_MAP = {
  1: "eth",
  8453: "base",
  42161: "arbitrum",
  10: "optimism",
  137: "polygon_pos",
  56: "bsc",
  43114: "avalanche",
  59144: "linea",
  534352: "scroll",
  146: "sonic"
};

// Calculate RSI (Relative Strength Index)
function calculateRSI(prices, period = 14) {
  if (prices.length < period + 1) return 50; // default neutral if not enough data
  
  let gains = [];
  let losses = [];
  
  for (let i = 1; i < prices.length; i++) {
    const diff = prices[i] - prices[i - 1];
    if (diff > 0) {
      gains.push(diff);
      losses.push(0);
    } else {
      gains.push(0);
      losses.push(Math.abs(diff));
    }
  }
  
  // First Average
  let avgGain = gains.slice(0, period).reduce((a, b) => a + b, 0) / period;
  let avgLoss = losses.slice(0, period).reduce((a, b) => a + b, 0) / period;
  
  // Wilder's Smoothing Technique
  for (let i = period; i < gains.length; i++) {
    avgGain = (avgGain * (period - 1) + gains[i]) / period;
    avgLoss = (avgLoss * (period - 1) + losses[i]) / period;
  }
  
  if (avgLoss === 0) return 100;
  const rs = avgGain / avgLoss;
  return 100 - (100 / (1 + rs));
}

// Calculate EMA (Exponential Moving Average)
function calculateEMA(prices, period) {
  if (prices.length < period) return prices[prices.length - 1];
  
  const k = 2 / (period + 1);
  // Start with SMA as initial value
  let ema = prices.slice(0, period).reduce((a, b) => a + b, 0) / period;
  
  for (let i = period; i < prices.length; i++) {
    ema = prices[i] * k + ema * (1 - k);
  }
  return ema;
}

export async function getTradingSignal(options = {}) {
  const chainInput = options.chain;
  const tokenInput = options.token;
  const forceAlert = options.alert || false;

  try {
    const { chainConfig } = await getWallet(chainInput, options);
    
    if (!tokenInput) {
      throw new Error("Please specify a target --token <symbolOrAddress> to check signals.");
    }

    const tokenAddress = await resolveTokenAddress(tokenInput, chainConfig.id, options);
    const isNative = tokenAddress === "0x0000000000000000000000000000000000000000";
    
    let targetAddress = tokenAddress;
    if (isNative) {
      // Resolve to wrapped version for pool lookup
      if (chainConfig.id === 1) targetAddress = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"; // WETH
      else if (chainConfig.id === 8453) targetAddress = "0x4200000000000000000000000000000000000006"; // WETH Base
      else if (chainConfig.id === 42161) targetAddress = "0x82aF49447D8a07e3bd95BD0d56f352415231C111"; // WETH Arb
      else if (chainConfig.id === 137) targetAddress = "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270"; // WMATIC
      else if (chainConfig.id === 56) targetAddress = "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"; // WBNB
    }

    logInfo(`Retrieving pool and market pairs from DexScreener...`, options);
    
    const dexUrl = `https://api.dexscreener.com/latest/dex/tokens/${targetAddress}`;
    const dexResponse = await axios.get(dexUrl, { timeout: 6000 });
    
    if (!dexResponse.data || !dexResponse.data.pairs || dexResponse.data.pairs.length === 0) {
      throw new Error(`No trading pairs found for token ${tokenInput} (${targetAddress}).`);
    }
    
    const pairs = dexResponse.data.pairs.sort((a, b) => (b.liquidity?.usd || 0) - (a.liquidity?.usd || 0));
    const bestPair = pairs[0];
    const poolAddress = bestPair.pairAddress;
    const geckoNetwork = GECKO_NETWORK_MAP[chainConfig.id];
    
    let prices = [];
    let rsi = 50;
    let ema20 = 0;
    let ema50 = 0;
    let priceIndicatorSource = "DexScreener Price Momentum Profile";
    
    if (geckoNetwork && poolAddress) {
      logInfo(`Fetching historical OHLCV data from GeckoTerminal...`, options);
      try {
        // Fetch 30 daily candles
        const geckoUrl = `https://api.geckoterminal.com/api/v2/networks/${geckoNetwork}/pools/${poolAddress}/ohlcv/day`;
        const geckoResponse = await axios.get(geckoUrl, {
          params: { limit: 40 },
          timeout: 7000
        });
        
        if (geckoResponse.data && geckoResponse.data.data && geckoResponse.data.data.attributes && Array.isArray(geckoResponse.data.data.attributes.ohlcv_list)) {
          const ohlcv = geckoResponse.data.data.attributes.ohlcv_list;
          // Format is [timestamp, open, high, low, close, volume]
          // Sort oldest to newest
          const sortedOhlcv = ohlcv.sort((a, b) => a[0] - b[0]);
          prices = sortedOhlcv.map(item => parseFloat(item[4])); // close prices
          
          if (prices.length >= 15) {
            rsi = calculateRSI(prices, 14);
            ema20 = calculateEMA(prices, 20);
            ema50 = calculateEMA(prices, 50);
            priceIndicatorSource = "GeckoTerminal Daily OHLCV Indicators";
          }
        }
      } catch (err) {
        logWarning(`GeckoTerminal OHLCV fetch failed: ${err.message}. Falling back to momentum calculations.`, options);
      }
    }
    
    // Core Decision Matrix (combining RSI, EMA, and DexScreener short-term momentum)
    const m5Change = bestPair.priceChange?.m5 || 0;
    const h1Change = bestPair.priceChange?.h1 || 0;
    const h24Change = bestPair.priceChange?.h24 || 0;
    const currentPrice = parseFloat(bestPair.priceUsd || 0);
    
    let bullishSignals = 0;
    let bearishSignals = 0;
    let neutralSignals = 0;
    
    // 1. RSI Scoring
    let rsiText = "Neutral";
    if (rsi < 30) {
      bullishSignals += 2; // Oversold - Buy trigger
      rsiText = "Oversold (Buy Alert)";
    } else if (rsi > 70) {
      bearishSignals += 2; // Overbought - Sell trigger
      rsiText = "Overbought (Sell Alert)";
    } else if (rsi > 50) {
      bullishSignals += 0.5;
    } else {
      bearishSignals += 0.5;
    }
    
    // 2. EMA Crossover Scoring
    let emaText = "No trend data";
    if (ema20 > 0 && ema50 > 0) {
      if (ema20 > ema50) {
        bullishSignals += 1.5; // Golden cross / Uptrend
        emaText = "Bullish Uptrend (EMA20 > EMA50)";
      } else {
        bearishSignals += 1.5; // Death cross / Downtrend
        emaText = "Bearish Downtrend (EMA20 < EMA50)";
      }
    }
    
    // 3. Momentum changes
    if (h1Change > 5) bullishSignals += 1;
    else if (h1Change < -5) bearishSignals += 1;
    else neutralSignals += 0.5;
    
    if (h24Change > 15) bullishSignals += 1;
    else if (h24Change < -15) bearishSignals += 1;
    
    // Make final decision
    let decision = "HOLD";
    let signalStrength = "NEUTRAL";
    
    const totalScore = bullishSignals - bearishSignals;
    
    if (totalScore >= 3.5) {
      decision = "BUY";
      signalStrength = "STRONG BUY";
    } else if (totalScore >= 1.5) {
      decision = "BUY";
      signalStrength = "BUY";
    } else if (totalScore <= -3.5) {
      decision = "SELL";
      signalStrength = "STRONG SELL";
    } else if (totalScore <= -1.5) {
      decision = "SELL";
      signalStrength = "SELL";
    }
    
    // Handle Alerts
    let isAlertTriggered = false;
    let alertMsg = "";
    if (forceAlert) {
      if (signalStrength === "STRONG BUY" || signalStrength === "STRONG SELL") {
        isAlertTriggered = true;
        alertMsg = `🚨 TRADING ALERT: ${bestPair.baseToken.symbol} shows ${signalStrength} signal. RSI: ${rsi.toFixed(2)} (${rsiText}), 24h change: ${h24Change}%!`;
      }
    }

    logSuccess(`Trading signal analysis complete`, options);
    
    if (!options.json) {
      console.log(`\n==================================================`);
      console.log(printColor(`TRADING SIGNAL REPORT: ${bestPair.baseToken.symbol}`, "bold"));
      console.log(`Token          : ${bestPair.baseToken.name} (${bestPair.baseToken.symbol})`);
      console.log(`Pool/Pair      : ${bestPair.quoteToken.symbol}/${bestPair.baseToken.symbol} (${bestPair.dexId.toUpperCase()})`);
      console.log(`Price USD      : $${currentPrice.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 6 })}`);
      console.log(`Source         : ${priceIndicatorSource}`);
      console.log(`--------------------------------------------------`);
      console.log(`RSI (14)       : ${rsi.toFixed(2)} (${rsiText})`);
      if (ema20 > 0 && ema50 > 0) {
        console.log(`EMA (20)       : $${ema20.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 6 })}`);
        console.log(`EMA (50)       : $${ema50.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 6 })}`);
        console.log(`EMA Trend      : ${emaText}`);
      }
      console.log(`--------------------------------------------------`);
      console.log(`Changes        : 5m: ${m5Change}%, 1h: ${h1Change}%, 24h: ${h24Change}%`);
      
      let signalColor = "yellow";
      if (decision === "BUY") signalColor = "green";
      else if (decision === "SELL") signalColor = "red";
      
      console.log(`Recommendation : ${printColor(signalStrength, signalColor)}`);
      
      if (isAlertTriggered) {
        console.log(`--------------------------------------------------`);
        console.log(printColor(alertMsg, "yellow"));
      }
      console.log(`==================================================\n`);
    }
    
    console.log(JSON.stringify({
      success: true,
      token: bestPair.baseToken.symbol,
      tokenName: bestPair.baseToken.name,
      tokenAddress: targetAddress,
      priceUsd: currentPrice,
      rsi: rsi,
      rsiStatus: rsiText,
      ema20: ema20,
      ema50: ema50,
      emaStatus: emaText,
      priceChange: {
        m5: m5Change,
        h1: h1Change,
        h24: h24Change
      },
      signal: signalStrength,
      recommendation: decision,
      alertTriggered: isAlertTriggered,
      alertMessage: alertMsg
    }, null, 2));

  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message
    }, null, 2));
  }
}
