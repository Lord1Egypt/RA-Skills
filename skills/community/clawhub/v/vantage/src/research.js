/**
 * research.js — DEPRECATED
 *
 * This module is superseded by src/signals.js which provides a
 * fully self-contained, production-grade signal engine.
 *
 * This file is retained only to keep the legacy `scan` CLI command working.
 * Do not use this module in new code.
 */

'use strict';

require('dotenv').config();
const https = require('https');

// ─── Live Data Fetchers ───────────────────────────────────────────────────────

/**
 * Fetch current RUNE price and 24h stats from CoinGecko (free, no key).
 */
async function fetchRunePrice() {
  return _fetch('https://api.coingecko.com/api/v3/simple/price?ids=thorchain&vs_currencies=usd&include_24hr_change=true&include_24hr_vol=true');
}

/**
 * Fetch THORChain network stats from THORNode.
 * Returns pool depths, swap volumes, and active validator count.
 */
async function fetchThorchainStats() {
  return _fetch('https://thornode.ninerealms.com/thorchain/network');
}

/**
 * Fetch top pools by volume from THORChain Midgard API.
 */
async function fetchTopPools(limit = 5) {
  return _fetch(`https://midgard.ninerealms.com/v2/pools?status=Available&order=volume24h&limit=${limit}`);
}

/**
 * Fetch funding rates and open interest from Hyperliquid public API.
 *
 * @param {string[]} [assets] assets to check e.g. ['ETH', 'BTC', 'RUNE']
 */
async function fetchHyperliquidFunding(assets = ['ETH', 'BTC', 'RUNE', 'SOL', 'AVAX']) {
  try {
    const body = JSON.stringify({ type: 'metaAndAssetCtxs' });
    const data = await _fetchPost('https://api.hyperliquid.xyz/info', body);
    if (!Array.isArray(data) || data.length < 2) return [];

    const meta = data[0].universe || [];
    const ctxs = data[1] || [];

    return meta
      .map((asset, i) => ({
        asset: asset.name,
        fundingRate: parseFloat(ctxs[i]?.funding || 0),
        openInterest: parseFloat(ctxs[i]?.openInterest || 0),
        markPrice: parseFloat(ctxs[i]?.markPx || 0),
      }))
      .filter(a => assets.length === 0 || assets.includes(a.asset))
      .sort((a, b) => Math.abs(b.fundingRate) - Math.abs(a.fundingRate));
  } catch (err) {
    console.warn('[research] Hyperliquid funding fetch failed:', err.message);
    return [];
  }
}

// ─── Signal Synthesis ─────────────────────────────────────────────────────────

/**
 * Get ecosystem signals for a given asset.
 * Combines live price data, THORChain stats, and Hyperliquid funding.
 *
 * @param {string} [asset] optional asset filter e.g. "RUNE", "ETH", "BTC"
 * @returns {Promise<object>} ecosystem signals
 */
async function getEcosystemSignals(asset = 'ALL') {
  const signals = [];

  try {
    // THORChain RUNE specific signals
    if (asset === 'ALL' || asset === 'RUNE') {
      const [runeData, thorStats, topPools] = await Promise.allSettled([
        fetchRunePrice(),
        fetchThorchainStats(),
        fetchTopPools(5),
      ]);

      if (runeData.status === 'fulfilled' && runeData.value?.thorchain) {
        const rune = runeData.value.thorchain;
        const change24h = rune.usd_24h_change || 0;
        signals.push({
          type: 'price_momentum',
          asset: 'RUNE',
          score: _normalise(change24h, -10, 10),
          label: change24h > 2 ? 'Bullish' : change24h < -2 ? 'Bearish' : 'Neutral',
          value: `$${rune.usd?.toFixed(4)} (${change24h.toFixed(2)}% 24h)`,
          source: 'coingecko_live',
        });
      }

      if (thorStats.status === 'fulfilled') {
        const stats = thorStats.value;
        const poolCount = parseInt(stats.activeBonds?.length || stats.bondMetrics?.totalBondUnits || 0);
        signals.push({
          type: 'network_health',
          asset: 'THORChain',
          score: 0.75, // strong if THORNode is responding
          label: 'Healthy',
          value: `Blocks: ${stats.blockHeight || 'unknown'}`,
          source: 'thornode_live',
        });
      }

      if (topPools.status === 'fulfilled' && Array.isArray(topPools.value)) {
        const totalVol24h = topPools.value.reduce((s, p) => s + parseFloat(p.volume24h || 0), 0);
        signals.push({
          type: 'dex_volume',
          asset: 'THORChain_pools',
          score: _normalise(totalVol24h, 0, 5e9), // 5B = fully bullish
          label: totalVol24h > 1e9 ? 'High Volume' : 'Moderate Volume',
          value: `Top 5 pools 24h vol: $${(totalVol24h / 1e6).toFixed(1)}M`,
          source: 'midgard_live',
        });
      }
    }

    // Hyperliquid funding signal
    const hlData = await fetchHyperliquidFunding(asset === 'ALL' ? [] : [asset]);
    for (const item of hlData.slice(0, 3)) {
      const fr = item.fundingRate;
      signals.push({
        type: 'funding_rate',
        asset: item.asset,
        score: _normalise(fr, -0.005, 0.005),
        label: fr > 0.0005 ? 'Longs paying (Bearish lean)' : fr < -0.0005 ? 'Shorts paying (Bullish lean)' : 'Neutral',
        value: `${(fr * 100).toFixed(4)}%/hr | OI: $${(item.openInterest / 1e6).toFixed(1)}M`,
        source: 'hyperliquid_live',
      });
    }

  } catch (err) {
    console.warn('[research] getEcosystemSignals partial failure:', err.message);
  }

  // Fallback if no live data
  if (signals.length === 0) {
    console.warn('[research] No live data available — returning stub signals');
    signals.push({
      type: 'sentiment', score: 0.5, label: 'Neutral', source: 'stub',
      note: 'Live feeds unavailable. Configure internet access.',
    });
  }

  return { asset, timestamp: new Date().toISOString(), signals };
}

/**
 * Market scan: combines Hyperliquid funding extremes + THORChain pool momentum.
 *
 * @param {object} [options]
 * @returns {Promise<object>} opportunities with direction and confidence
 */
async function getMarketScan({ limit = 10, strategy = 'all' } = {}) {
  const opportunities = [];

  try {
    const [hlFunding, topPools] = await Promise.allSettled([
      fetchHyperliquidFunding([]),
      fetchTopPools(10),
    ]);

    // High funding rate = overcrowded longs → potential short
    if (hlFunding.status === 'fulfilled') {
      for (const item of hlFunding.value) {
        const fr = item.fundingRate;
        if (Math.abs(fr) < 0.0003) continue; // skip noise

        const dir = fr > 0 ? 'short' : 'long'; // longs paying → short bias
        const strength = Math.min(Math.abs(fr) / 0.001, 1);

        opportunities.push({
          asset: `${item.asset}/USDC`,
          strategy: 'funding_arbitrage',
          signal_strength: parseFloat(strength.toFixed(3)),
          direction: dir,
          entry_zone: `~$${item.markPrice.toFixed(2)}`,
          confidence: strength > 0.7 ? 'high' : strength > 0.4 ? 'medium' : 'low',
          note: `Funding: ${(fr * 100).toFixed(4)}%/hr — ${dir === 'short' ? 'longs crowded' : 'shorts crowded'}`,
          source: 'hyperliquid_live',
        });
      }
    }

    // THORChain pool momentum
    if (topPools.status === 'fulfilled' && Array.isArray(topPools.value)) {
      for (const pool of topPools.value.slice(0, 3)) {
        const vol = parseFloat(pool.volume24h || 0);
        if (vol < 1e7) continue; // skip low volume

        const asset = pool.asset?.split('.')[1]?.split('-')[0] || pool.asset;
        opportunities.push({
          asset: `${asset}/USDC`,
          strategy: 'momentum',
          signal_strength: _normalise(vol, 0, 1e9),
          direction: 'long',
          entry_zone: 'market',
          confidence: vol > 1e8 ? 'medium' : 'low',
          note: `THORChain 24h volume: $${(vol / 1e6).toFixed(1)}M`,
          source: 'midgard_live',
        });
      }
    }
  } catch (err) {
    console.warn('[research] getMarketScan error:', err.message);
  }

  const filtered = strategy === 'all'
    ? opportunities
    : opportunities.filter(o => o.strategy === strategy);

  return {
    timestamp: new Date().toISOString(),
    strategy,
    count: Math.min(filtered.length, limit),
    opportunities: filtered
      .sort((a, b) => b.signal_strength - a.signal_strength)
      .slice(0, limit),
  };
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function _normalise(val, min, max) {
  return parseFloat(Math.max(0, Math.min(1, (val - min) / (max - min))).toFixed(3));
}

function _fetch(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'HL-TradingAgent/2.0' } }, res => {
      let data = '';
      res.on('data', c => (data += c));
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { reject(new Error(`JSON parse failed: ${e.message}`)); }
      });
    }).on('error', reject);
  });
}

function _fetchPost(url, body) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const opts = {
      hostname: u.hostname, path: u.pathname,
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': Buffer.byteLength(body) },
    };
    const req = https.request(opts, res => {
      let data = '';
      res.on('data', c => (data += c));
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { reject(new Error(`JSON parse failed: ${e.message}`)); }
      });
    });
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

module.exports = { getEcosystemSignals, getMarketScan };
