/**
 * TradingView Signal Parser Skill
 * 
 * Parse TradingView signals and provide structured analysis
 * Price: 0.001 USDT per request
 * 
 * @param {Object} params
 * @param {string} params.signal - Signal text (e.g., "BTCUSD long from 42000, stop loss 40000, target 45000")
 * @param {string} [params.url] - Optional TradingView URL
 * @returns {Object} Structured signal analysis
 */

const axios = require('axios');

// SkillPay Configuration
const BILLING_URL = 'https://skillpay.me/api/v1/billing';
const API_KEY = 'sk_4312778b58aa7c81c15bd0e2b4fe544e12ca9e765f0deab630a50ecd4daf4ac2';
const SKILL_ID = '1481cef0-2cd0-4768-83d9-a51c57a46180';
const headers = { 'X-API-Key': API_KEY, 'Content-Type': 'application/json' };

/**
 * Charge user before executing skill
 */
async function chargeUser(userId) {
  try {
    const { data } = await axios.post(BILLING_URL + '/charge', {
      user_id: userId,
      skill_id: SKILL_ID,
      amount: 1, // 1 token = 0.001 USDT
    }, { headers });
    
    if (data.success) {
      return { ok: true, balance: data.balance };
    }
    return { ok: false, balance: data.balance, payment_url: data.payment_url };
  } catch (error) {
    console.error('Billing error:', error.message);
    return { ok: false, error: error.message };
  }
}

/**
 * Parse TradingView signal text
 */
function parseSignal(signalText) {
  const text = signalText.toLowerCase();
  
  // Extract direction
  let direction = 'unknown';
  if (text.includes('long') || text.includes('买入') || text.includes('做多')) {
    direction = 'long';
  } else if (text.includes('short') || text.includes('卖出') || text.includes('做空')) {
    direction = 'short';
  }
  
  // Extract prices using regex
  const entryMatch = text.match(/(?:entry|入|开|from|at)\s*[:\s]*(\d+[\.]?\d*)/i);
  const slMatch = text.match(/(?:stop\s*loss|止损|sl)\s*[:\s]*(\d+[\.]?\d*)/i);
  const tpMatch = text.match(/(?:target|take\s*profit|止盈|tp)\s*[:\s]*(\d+[\.]?\d*)/i);
  
  // Try to extract symbol
  const symbolMatch = signalText.match(/([A-Z]{2,10})(?:USD|USDT|USD)?/i);
  const symbol = symbolMatch ? symbolMatch[1].toUpperCase() : 'UNKNOWN';
  
  const entry = entryMatch ? parseFloat(entryMatch[1]) : null;
  const stopLoss = slMatch ? parseFloat(slMatch[1]) : null;
  const takeProfit = tpMatch ? parseFloat(tpMatch[1]) : null;
  
  // Calculate risk/reward
  let riskReward = null;
  if (entry && stopLoss && takeProfit) {
    const risk = Math.abs(entry - stopLoss);
    const reward = Math.abs(takeProfit - entry);
    riskReward = reward / risk;
  }
  
  return {
    symbol,
    direction,
    entry,
    stopLoss,
    takeProfit,
    riskReward: riskReward ? riskReward.toFixed(2) : null,
    riskRewardRating: riskReward ? (riskReward >= 2 ? '⭐⭐⭐ Excellent' : riskReward >= 1.5 ? '⭐⭐ Good' : '⚠️ Poor') : 'N/A'
  };
}

/**
 * Main skill handler
 */
module.exports = async function handler(params, context) {
  const { signal, url } = params;
  const userId = context?.user_id || 'anonymous';
  
  // Check if signal is provided
  if (!signal && !url) {
    return {
      success: false,
      error: 'Please provide a signal or TradingView URL'
    };
  }
  
  // Charge user first
  const charge = await chargeUser(userId);
  if (!charge.ok) {
    return {
      success: false,
      error: 'Insufficient balance',
      payment_url: charge.payment_url,
      message: 'Please deposit USDT to use this skill',
      instructions: 'Copy the payment link to deposit USDT, then try again'
    };
  }
  
  // Parse the signal
  let parsed = null;
  let source = 'text';
  
  if (signal) {
    parsed = parseSignal(signal);
  } else if (url) {
    // Could add URL parsing here in the future
    parsed = {
      symbol: 'URL_DETECTED',
      direction: 'unknown',
      note: 'Please provide signal text for analysis'
    };
    source = 'url';
  }
  
  // Generate analysis
  const analysis = {
    signal: signal || url,
    source,
    parsed,
    timestamp: new Date().toISOString(),
    remainingBalance: charge.balance,
    message: '✅ Signal parsed successfully!'
  };
  
  // Add recommendations
  if (parsed.direction !== 'unknown' && parsed.riskReward) {
    analysis.recommendation = parsed.riskReward >= 1.5 
      ? '✅ Good risk/reward ratio. Consider following this signal.'
      : '⚠️ Low risk/reward ratio. Trade with caution.';
  }
  
  return {
    success: true,
    ...analysis
  };
};
