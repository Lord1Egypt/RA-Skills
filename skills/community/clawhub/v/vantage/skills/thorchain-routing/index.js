#!/usr/bin/env node
/**
 * THORChain Routing Skill — @morebetter/thorchain-routing
 * Cross-chain swap routing via THORChain for AI agents
 * No API key required — uses public THORNode + Midgard endpoints
 */

'use strict';

const https = require('https');

const THORNODE = 'https://thornode.ninerealms.com';
const MIDGARD  = 'https://midgard.ninerealms.com/v2';

// ── HTTP helper ────────────────────────────────────────────────────────────────
function _get(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'Accept': 'application/json' } }, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(body)); }
        catch (e) { reject(new Error(`JSON parse error from ${url}: ${e.message}`)); }
      });
    }).on('error', reject);
  });
}

// ── Core functions ─────────────────────────────────────────────────────────────

/**
 * Get a swap quote from THORChain
 * @param {string} fromAsset  - e.g. "ETH.ETH", "BTC.BTC", "THOR.RUNE"
 * @param {string} toAsset    - e.g. "THOR.RUNE", "ETH.USDC-0xa0b8..."
 * @param {number|string} amount - Amount in 1e8 base units (1 BTC = 100000000)
 * @param {string} [destination] - Optional destination address
 * @returns {Promise<Object>} Quote object with expected_amount_out, fees, memo
 */
async function thorQuote(fromAsset, toAsset, amount, destination) {
  let url = `${THORNODE}/thorchain/quote/swap?from_asset=${encodeURIComponent(fromAsset)}&to_asset=${encodeURIComponent(toAsset)}&amount=${amount}`;
  if (destination) url += `&destination=${encodeURIComponent(destination)}`;
  const raw = await _get(url);
  return {
    fromAsset,
    toAsset,
    amountIn: amount,
    amountOut: raw.expected_amount_out,
    fees: {
      affiliate: raw.fees?.affiliate,
      outbound: raw.fees?.outbound,
      liquidity: raw.fees?.liquidity,
      total: raw.fees?.total,
    },
    slippage: raw.slippage_bps,
    memo: raw.memo,
    inboundAddress: raw.inbound_address,
    expiry: raw.expiry,
    warnings: raw.warnings || [],
    minAmountIn: raw.recommended_min_amount_in,
    raw,
  };
}

/**
 * Scan THORChain pools for routing opportunities
 * @param {string[]} [tokens] - Optional filter tokens (e.g. ['BTC', 'ETH', 'RUNE'])
 * @returns {Promise<Object>} Scan result with top pools sorted by volume
 */
async function thorScan(tokens) {
  const pools = await _get(`${MIDGARD}/pools?status=available&period=24h`);

  let filtered = pools;
  if (tokens && tokens.length > 0) {
    const upper = tokens.map(t => t.toUpperCase());
    filtered = pools.filter(p => upper.some(t => p.asset.toUpperCase().includes(t)));
  }

  // Sort by 24h volume
  const sorted = [...filtered].sort((a, b) =>
    parseFloat(b.volume24h || 0) - parseFloat(a.volume24h || 0)
  );

  const top = sorted.slice(0, 10).map(p => ({
    asset: p.asset,
    price_usd: p.assetPriceUSD,
    volume_24h_rune: p.volume24h,
    liquidity_rune: p.runeDepth,
    apy: p.poolAPY,
    status: p.status,
  }));

  // Identify arbitrage opportunities: pools with high volume and positive APY
  const opportunities = top
    .filter(p => parseFloat(p.volume_24h_rune) > 1e10 && parseFloat(p.apy) > 0.05)
    .map(p => ({
      asset: p.asset,
      signal: 'high_volume_yield',
      apy: (parseFloat(p.apy) * 100).toFixed(2) + '%',
      volume_24h_rune: p.volume_24h_rune,
      note: 'Active liquidity provision opportunity or routing path',
    }));

  return {
    timestamp: new Date().toISOString(),
    totalPools: pools.length,
    filteredPools: filtered.length,
    topPools: top,
    opportunities,
    source: 'midgard_live',
  };
}

/**
 * Get THORChain inbound addresses (where to send assets for swaps)
 * @returns {Promise<Object[]>} Array of inbound addresses per chain
 */
async function thorInbound() {
  const raw = await _get(`${THORNODE}/thorchain/inbound_addresses`);
  return (raw || []).map(chain => ({
    chain: chain.chain,
    address: chain.address,
    halted: chain.halted,
    gas_rate: chain.gas_rate,
    gas_rate_units: chain.gas_rate_units,
    outbound_tx_size: chain.outbound_tx_size,
  }));
}

// ── CLI interface ──────────────────────────────────────────────────────────────
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (command === '--test' || command === 'test') {
    console.log('🔍 THORChain Routing Skill — Test Mode\n');

    console.log('1. Testing thorScan()...');
    try {
      const scan = await thorScan(['BTC', 'ETH', 'RUNE']);
      console.log(`   ✅ ${scan.filteredPools} pools found, ${scan.opportunities.length} opportunities`);
      if (scan.topPools[0]) {
        console.log(`   Top pool: ${scan.topPools[0].asset} @ $${parseFloat(scan.topPools[0].price_usd).toFixed(4)}`);
      }
    } catch (e) { console.error('   ❌', e.message); }

    console.log('\n2. Testing thorInbound()...');
    try {
      const inbound = await thorInbound();
      const active = inbound.filter(c => !c.halted);
      console.log(`   ✅ ${inbound.length} chains, ${active.length} active`);
      active.slice(0, 3).forEach(c => console.log(`   ${c.chain}: ${c.address ? c.address.slice(0,20) + '...' : 'N/A'}`));
    } catch (e) { console.error('   ❌', e.message); }

    console.log('\n3. Testing thorQuote() [ETH → RUNE, 0.01 ETH = 1000000 units]...');
    try {
      const quote = await thorQuote('ETH.ETH', 'THOR.RUNE', '1000000');
      console.log(`   ✅ Quote received — out: ${quote.amountOut}, memo: ${(quote.memo || '').slice(0, 40)}...`);
    } catch (e) { console.error('   ❌', e.message, '(expected if amount too small)'); }

    console.log('\n✅ Test complete.\n');
    return;
  }

  if (command === 'thor-quote') {
    const [, fromAsset, toAsset, amount, dest] = args;
    if (!fromAsset || !toAsset || !amount) {
      console.error('Usage: thor-quote <fromAsset> <toAsset> <amount> [destination]');
      process.exit(1);
    }
    const result = await thorQuote(fromAsset, toAsset, amount, dest);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (command === 'thor-scan') {
    const tokens = args.slice(1).filter(a => !a.startsWith('-'));
    const result = await thorScan(tokens.length ? tokens : undefined);
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  if (command === 'thor-inbound') {
    const result = await thorInbound();
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  console.log(`
THORChain Routing Skill — @morebetter/thorchain-routing

Commands:
  thor-quote <fromAsset> <toAsset> <amount> [destination]
  thor-scan [token1 token2 ...]
  thor-inbound
  --test

Assets: BTC.BTC | ETH.ETH | THOR.RUNE | ETH.USDC-0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48
Amount: in 1e8 base units (1 BTC = 100000000)
  `);
}

// ── Exports ────────────────────────────────────────────────────────────────────
module.exports = { thorQuote, thorScan, thorInbound };

if (require.main === module) {
  main().catch(err => { console.error('Error:', err.message); process.exit(1); });
}
