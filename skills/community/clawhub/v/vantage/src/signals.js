/**
 * signals.js — Self-contained signal engine for HL Trading Agent
 *
 * Data sources (all public, no API keys required):
 *   - Hyperliquid: funding rates, open interest, mark prices
 *   - CoinGecko free tier: 24h price change, volume
 *   - THORChain Midgard: pool volumes, assetPriceUSD (NOT swap quotes)
 *   - THORChain NineRealms: network health
 *
 * All responses are cached for CRON_INTERVAL_MINUTES (default: 60 min).
 * Rate-limit errors get exponential backoff + retry.
 */

'use strict';

const https = require('https');

// ── Config ────────────────────────────────────────────────────────────────────

const FUNDING_EXTREME_THRESHOLD = 0.0005;      // 0.05%/hr
const MOMENTUM_THRESHOLD_PCT    = 5;            // 5% 24h change
const THORCHAIN_VOLUME_SPIKE_USD = 100_000_000; // $100M total ecosystem volume

const HL_INFO_URL    = 'https://api.hyperliquid.xyz/info';
const MIDGARD_URL    = 'https://midgard.ninerealms.com';
const THORNODE_URL   = 'https://thornode.ninerealms.com';
const COINGECKO_URL  = 'https://api.coingecko.com/api/v3';

// ── Response Cache ────────────────────────────────────────────────────────────

const _cache = {};

function _cacheTtlMs() {
  return (parseInt(process.env.CRON_INTERVAL_MINUTES, 10) || 60) * 60 * 1000;
}

function _getCached(key) {
  const entry = _cache[key];
  if (!entry || Date.now() > entry.expiresAt) return null;
  return entry.data;
}

function _setCache(key, data) {
  _cache[key] = { data, expiresAt: Date.now() + _cacheTtlMs() };
}

// ── HTTP Helpers ──────────────────────────────────────────────────────────────

function _httpGet(url, retriesLeft = 3) {
  return new Promise((resolve, reject) => {
    const attempt = (n) => {
      https.get(url, { headers: { 'User-Agent': 'HL-TradingAgent/2.0' } }, (res) => {
        let raw = '';
        res.on('data', (c) => (raw += c));
        res.on('end', () => {
          if (res.statusCode === 429 && n > 0) {
            const delay = Math.pow(2, retriesLeft - n + 1) * 1000;
            setTimeout(() => attempt(n - 1), delay);
            return;
          }
          if (res.statusCode >= 400) {
            reject(new Error(`HTTP ${res.statusCode} for ${url}`));
            return;
          }
          try { resolve(JSON.parse(raw)); }
          catch (e) { reject(new Error(`JSON parse failed: ${e.message}`)); }
        });
      }).on('error', (err) => {
        if (n > 0) setTimeout(() => attempt(n - 1), Math.pow(2, retriesLeft - n + 1) * 1000);
        else reject(err);
      });
    };
    attempt(retriesLeft);
  });
}

function _httpPost(url, body) {
  return new Promise((resolve, reject) => {
    const bodyStr = JSON.stringify(body);
    const u = new URL(url);
    const req = https.request({
      hostname: u.hostname,
      path: u.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(bodyStr),
        'User-Agent': 'HL-TradingAgent/2.0',
      },
    }, (res) => {
      let raw = '';
      res.on('data', (c) => (raw += c));
      res.on('end', () => {
        try { resolve(JSON.parse(raw)); }
        catch (e) { reject(new Error(`JSON parse failed: ${e.message}`)); }
      });
    });
    req.on('error', reject);
    req.write(bodyStr);
    req.end();
  });
}

// ── Data Fetchers (all cached) ────────────────────────────────────────────────

async function _fetchHlMetaAndCtxs() {
  const key = 'hl_meta_ctxs';
  const cached = _getCached(key);
  if (cached) return cached;
  const data = await _httpPost(HL_INFO_URL, { type: 'metaAndAssetCtxs' });
  _setCache(key, data);
  return data;
}

async function _fetchCoinGeckoPrice(coinId) {
  const key = `cg_${coinId}`;
  const cached = _getCached(key);
  if (cached) return cached;
  const url = `${COINGECKO_URL}/simple/price?ids=${coinId}&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true`;
  const data = await _httpGet(url);
  _setCache(key, data);
  return data;
}

async function _fetchMidgardPools() {
  const key = 'midgard_pools';
  const cached = _getCached(key);
  if (cached) return cached;
  const data = await _httpGet(`${MIDGARD_URL}/v2/pools?status=Available`);
  _setCache(key, data);
  return data;
}

async function _fetchMidgardStats() {
  const key = 'midgard_stats';
  const cached = _getCached(key);
  if (cached) return cached;
  const data = await _httpGet(`${MIDGARD_URL}/v2/stats`);
  _setCache(key, data);
  return data;
}

async function _fetchThorNodeHealth() {
  const key = 'thornode_health';
  const cached = _getCached(key);
  if (cached) return cached;
  const data = await _httpGet(`${THORNODE_URL}/thorchain/network`);
  _setCache(key, data);
  return data;
}

// ── Asset Mappings ────────────────────────────────────────────────────────────

const COINGECKO_IDS = {
  BTC:  'bitcoin',
  ETH:  'ethereum',
  RUNE: 'thorchain',
  SOL:  'solana',
  AVAX: 'avalanche-2',
  ATOM: 'cosmos',
  BNB:  'binancecoin',
  LTC:  'litecoin',
  DOGE: 'dogecoin',
  ARB:  'arbitrum',
  OP:   'optimism',
};

// Midgard pool asset identifiers
const MIDGARD_ASSET_MAP = {
  BTC:  'BTC.BTC',
  ETH:  'ETH.ETH',
  ATOM: 'GAIA.ATOM',
  BNB:  'BSC.BNB',
  AVAX: 'AVAX.AVAX',
  LTC:  'LTC.LTC',
  DOGE: 'DOGE.DOGE',
};

// ── Public: Midgard Price Fetch ───────────────────────────────────────────────

/**
 * Get USD prices from Midgard for a list of coins.
 * Uses assetPriceUSD directly — NOT swap quotes (swap quotes include fees
 * that distort pricing on small amounts, causing false arb signals).
 *
 * @param {string[]} coins  e.g. ['BTC', 'ETH', 'RUNE']
 * @returns {Promise<Object>}  { BTC: 63500.12, RUNE: 3.42, ... }
 */
async function getMidgardPrices(coins) {
  const prices = {};
  const coinsUpper = coins.map((c) => c.toUpperCase());

  try {
    const [poolsResult, statsResult] = await Promise.allSettled([
      _fetchMidgardPools(),
      _fetchMidgardStats(),
    ]);

    if (poolsResult.status === 'fulfilled' && Array.isArray(poolsResult.value)) {
      for (const coin of coinsUpper) {
        const midgardAsset = MIDGARD_ASSET_MAP[coin];
        if (midgardAsset) {
          const pool = poolsResult.value.find((p) => p.asset === midgardAsset);
          if (pool && pool.assetPriceUSD) {
            prices[coin] = parseFloat(pool.assetPriceUSD);
          }
        }
      }
    }

    // RUNE is the native asset — its USD price lives in stats.runePriceUSD
    if (coinsUpper.includes('RUNE') && statsResult.status === 'fulfilled') {
      const runePrice = parseFloat(statsResult.value?.runePriceUSD || 0);
      if (runePrice > 0) prices['RUNE'] = runePrice;
    }
  } catch (err) {
    // Return partial results; caller handles missing prices
  }

  return prices;
}

// ── Public: Signal Generation ─────────────────────────────────────────────────

/**
 * Generate a trading signal for one coin using live public APIs.
 * Returns signal object regardless of whether direction is actionable.
 *
 * @param {string} coin  e.g. 'RUNE'
 * @returns {Promise<object>}
 */
async function getSignal(coin) {
  const coinUpper = coin.toUpperCase();
  const timestamp = new Date().toISOString();

  let fundingRate   = 0;
  let openInterest  = 0;
  let markPrice     = 0;
  let price24hChange = 0;
  let oiUsd         = 0;
  let thorVolumeUsd = 0;
  const sources     = [];

  // 1. Hyperliquid: funding rate, OI, mark price
  try {
    const metaCtxs = await _fetchHlMetaAndCtxs();
    const universe = (metaCtxs[0] || {}).universe || [];
    const ctxs     = metaCtxs[1] || [];
    const idx      = universe.findIndex((a) => a.name.toUpperCase() === coinUpper);
    if (idx !== -1) {
      const ctx   = ctxs[idx] || {};
      fundingRate  = parseFloat(ctx.funding      || 0);
      openInterest = parseFloat(ctx.openInterest || 0);
      markPrice    = parseFloat(ctx.markPx       || 0);
      oiUsd        = openInterest * markPrice;
      sources.push('hyperliquid_live');
    }
  } catch (_) { /* continue — will use other sources */ }

  // 2. CoinGecko: 24h price change
  const cgId = COINGECKO_IDS[coinUpper];
  if (cgId) {
    try {
      const cgData   = await _fetchCoinGeckoPrice(cgId);
      const coinData = cgData[cgId];
      if (coinData) {
        price24hChange = coinData.usd_24h_change || 0;
        sources.push('coingecko_live');
      }
    } catch (_) { /* continue */ }
  }

  // 3. THORChain Midgard: ecosystem volume (used for RUNE volume spike signal)
  try {
    const [statsResult] = await Promise.allSettled([_fetchMidgardStats()]);
    if (statsResult.status === 'fulfilled' && statsResult.value) {
      const stats      = statsResult.value;
      const runePrice  = parseFloat(stats.runePriceUSD || 0);
      const swapVolRune = parseFloat(stats.swapVolume  || 0); // in 8-decimal RUNE
      thorVolumeUsd    = (swapVolRune / 1e8) * runePrice;
      sources.push('midgard_live');
    }
  } catch (_) { /* continue */ }

  // ── Signal Logic ────────────────────────────────────────────────────────────

  let signal    = 'neutral';
  let direction = null;
  let confidence = 0;

  // Funding rate extreme → contrarian mean-reversion signal
  if (fundingRate > FUNDING_EXTREME_THRESHOLD) {
    signal     = 'funding_extreme_short';
    direction  = 'short';
    // 0.5 at threshold, scales up to 1.0 at 5× threshold
    confidence = Math.min(0.5 + (fundingRate - FUNDING_EXTREME_THRESHOLD) / (FUNDING_EXTREME_THRESHOLD * 4), 1.0);

  } else if (fundingRate < -FUNDING_EXTREME_THRESHOLD) {
    signal     = 'funding_extreme_long';
    direction  = 'long';
    confidence = Math.min(0.5 + (Math.abs(fundingRate) - FUNDING_EXTREME_THRESHOLD) / (FUNDING_EXTREME_THRESHOLD * 4), 1.0);

  // Price momentum + positive open interest
  } else if (price24hChange > MOMENTUM_THRESHOLD_PCT && oiUsd > 0) {
    signal     = 'price_momentum_long';
    direction  = 'long';
    confidence = Math.min(0.5 + (price24hChange - MOMENTUM_THRESHOLD_PCT) / 20, 0.9);

  } else if (price24hChange < -MOMENTUM_THRESHOLD_PCT && oiUsd > 0) {
    signal     = 'price_momentum_short';
    direction  = 'short';
    confidence = Math.min(0.5 + (Math.abs(price24hChange) - MOMENTUM_THRESHOLD_PCT) / 20, 0.9);

  // THORChain volume spike → ecosystem demand bullish on RUNE
  } else if (coinUpper === 'RUNE' && thorVolumeUsd > THORCHAIN_VOLUME_SPIKE_USD) {
    signal     = 'thorchain_volume_spike';
    direction  = 'long';
    confidence = Math.min(0.5 + (thorVolumeUsd - THORCHAIN_VOLUME_SPIKE_USD) / (THORCHAIN_VOLUME_SPIKE_USD * 2), 0.8);
  }

  return {
    timestamp,
    coin:            coinUpper,
    signal,
    direction,
    confidence:      parseFloat(confidence.toFixed(3)),
    funding_rate:    parseFloat(fundingRate.toFixed(6)),
    price_24h_change: parseFloat(price24hChange.toFixed(2)),
    oi_usd:          parseFloat(oiUsd.toFixed(0)),
    source:          sources,
  };
}

/**
 * Scan multiple coins and return all signals (including neutral).
 *
 * @param {string[]} coins  e.g. ['BTC', 'ETH', 'RUNE']
 * @returns {Promise<object[]>}
 */
async function scanSignals(coins) {
  const results = await Promise.allSettled(coins.map((c) => getSignal(c)));
  return results
    .map((r, i) => {
      if (r.status === 'fulfilled') return r.value;
      console.warn(`[signals] ${coins[i]}: ${r.reason?.message}`);
      return null;
    })
    .filter(Boolean);
}

module.exports = { getSignal, scanSignals, getMidgardPrices };
