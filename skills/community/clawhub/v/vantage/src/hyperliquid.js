/**
 * hyperliquid.js — Hyperliquid perp DEX integration
 * Wraps the Hyperliquid public REST API (no auth required for read operations).
 * 
 * API docs: https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint
 */

'use strict';

const axios = require('axios');
const fs = require('fs');
const path = require('path');

const HL_API_URL = process.env.HYPERLIQUID_API_URL || 'https://api.hyperliquid.xyz/info';
const PAPER_TRADES_FILE = path.join(__dirname, '..', 'data', 'paper-trades.json');

const client = axios.create({
  baseURL: HL_API_URL,
  timeout: 10_000,
  headers: { 'Content-Type': 'application/json' },
});

async function post(body) {
  const res = await client.post('', body);
  return res.data;
}

/**
 * Get mid prices for all coins (or a specific coin).
 * @param {string} [coin] e.g. "RUNE" — if omitted, returns all
 * @returns {Promise<Array<{coin, midPrice, timestamp}>>}
 */
async function getMarketData(coin) {
  const data = await post({ type: 'allMids' });
  const timestamp = new Date().toISOString();
  const entries = Object.entries(data).map(([c, midPrice]) => ({
    coin: c,
    midPrice: parseFloat(midPrice),
    timestamp,
  }));
  if (coin) {
    return entries.filter(e => e.coin.toUpperCase() === coin.toUpperCase());
  }
  return entries.sort((a, b) => a.coin.localeCompare(b.coin));
}

/**
 * Get open perpetual positions for a wallet address.
 * @param {string} [walletAddress] — if empty/null, returns demo positions
 * @returns {Promise<Array>}
 */
async function getPositions(walletAddress) {
  if (!walletAddress) {
    return [
      { coin: 'DEMO', side: 'long', size: 0, entryPrice: 0, unrealisedPnl: 0, note: 'Set HYPERLIQUID_WALLET_ADDRESS in .env for live positions' },
    ];
  }
  const data = await post({ type: 'clearinghouseState', user: walletAddress });
  const positions = (data.assetPositions || []).map(p => {
    const pos = p.position;
    return {
      coin: pos.coin,
      side: parseFloat(pos.szi) > 0 ? 'long' : 'short',
      size: Math.abs(parseFloat(pos.szi || 0)),
      entryPrice: parseFloat(pos.entryPx || 0),
      unrealisedPnl: parseFloat(pos.unrealizedPnl || 0),
      leverage: pos.leverage?.value || null,
      liquidationPrice: parseFloat(pos.liquidationPx || 0),
    };
  });
  return positions.filter(p => p.size > 0);
}

/**
 * Get funding rates for all coins (or a specific coin).
 * @param {string} [coin] — if omitted, returns all
 * @returns {Promise<Array<{coin, fundingRate, openInterest}>>}
 */
async function getFundingRates(coin) {
  const data = await post({ type: 'metaAndAssetCtxs' });
  const meta = data[0] || {};
  const ctxs = data[1] || [];
  const universe = (meta.universe || []);

  const result = universe.map((asset, i) => {
    const ctx = ctxs[i] || {};
    return {
      coin: asset.name,
      fundingRate: parseFloat(ctx.funding || 0),
      openInterest: parseFloat(ctx.openInterest || 0),
      markPrice: parseFloat(ctx.markPx || 0),
    };
  });

  if (coin) {
    return result.filter(r => r.coin.toUpperCase() === coin.toUpperCase());
  }
  return result.sort((a, b) => b.openInterest - a.openInterest);
}

/**
 * Simulate a paper trade entry. Stored in data/paper-trades.json.
 * @param {string} coin
 * @param {string} side 'long' | 'short'
 * @param {number} size
 * @param {number} [price] — if omitted, fetches current mid price
 * @returns {Promise<object>}
 */
async function placePaperTrade(coin, side, size, price) {
  // Ensure data dir + file exists
  const dataDir = path.dirname(PAPER_TRADES_FILE);
  if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });
  if (!fs.existsSync(PAPER_TRADES_FILE)) fs.writeFileSync(PAPER_TRADES_FILE, '[]');

  // Get current price if not provided
  let entryPrice = price;
  if (!entryPrice) {
    const mids = await getMarketData(coin);
    if (mids.length === 0) throw new Error(`No market data found for ${coin}`);
    entryPrice = mids[0].midPrice;
  }

  const trades = JSON.parse(fs.readFileSync(PAPER_TRADES_FILE, 'utf8'));
  const trade = {
    id: `paper-${Date.now()}`,
    coin: coin.toUpperCase(),
    side: side.toLowerCase(),
    size: parseFloat(size),
    entryPrice,
    timestamp: new Date().toISOString(),
    pnl: 0,
    status: 'open',
  };

  trades.push(trade);
  fs.writeFileSync(PAPER_TRADES_FILE, JSON.stringify(trades, null, 2));
  return trade;
}

/**
 * Get all open paper positions.
 * @returns {Array}
 */
function getPaperPositions() {
  if (!fs.existsSync(PAPER_TRADES_FILE)) return [];
  const trades = JSON.parse(fs.readFileSync(PAPER_TRADES_FILE, 'utf8'));
  return trades.filter(t => t.status === 'open');
}

/**
 * Fetch the live account balance (USDC) for a wallet address.
 * Used by src/sizing.js before every trade.
 * Throws if fetch fails — callers must abort the trade, not default to a size.
 *
 * @param {string} walletAddress  0x-prefixed EVM address
 * @returns {Promise<number>}  Account value in USD
 */
async function getAccountBalance(walletAddress) {
  if (!walletAddress) {
    throw new Error('HYPERLIQUID_WALLET_ADDRESS is required to fetch account balance');
  }
  const data    = await post({ type: 'clearinghouseState', user: walletAddress });
  const balance = parseFloat(data?.marginSummary?.accountValue || '0');
  if (isNaN(balance)) {
    throw new Error('Could not parse account balance from Hyperliquid response');
  }
  return balance;
}

module.exports = {
  getMarketData,
  getPositions,
  getFundingRates,
  placePaperTrade,
  getPaperPositions,
  getAccountBalance,
};
