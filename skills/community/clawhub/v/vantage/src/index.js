#!/usr/bin/env node
/**
 * HL Trading Agent — CLI entrypoint
 *
 * Commands:
 *   start [--paper]          Autonomous trading loop (paper or live)
 *   hl-data [coin]           Live market prices + funding rates
 *   hl-positions [--paper]   Open positions (live wallet or paper)
 *   hl-trade ...             Manual paper trade entry
 *   hl-arb [coin ...]        THORChain vs Hyperliquid price gap scanner
 *   quote ...                THORChain swap quote
 *   inbound [chain]          THORChain inbound vault addresses
 *   scan [asset] ...         Legacy market scan (research.js)
 */

'use strict';

require('dotenv').config();

const https = require('https');

const { getQuote, getInboundAddresses, formatSwapMemo } = require('./thorchain');
const { getEcosystemSignals, getMarketScan }            = require('./research');
const {
  getMarketData,
  getPositions,
  getFundingRates,
  placePaperTrade,
  getPaperPositions,
}                                                        = require('./hyperliquid');
const { scanSignals, getMidgardPrices }                  = require('./signals');

const [, , command, ...args] = process.argv;

// ── LLM Decision Layer ────────────────────────────────────────────────────────

function _httpPostJson(url, body, extraHeaders = {}) {
  return new Promise((resolve, reject) => {
    const bodyStr = JSON.stringify(body);
    const u       = new URL(url);
    const req     = https.request({
      hostname: u.hostname,
      path:     u.pathname,
      method:   'POST',
      headers:  {
        'Content-Type':   'application/json',
        'Content-Length': Buffer.byteLength(bodyStr),
        ...extraHeaders,
      },
    }, (res) => {
      let raw = '';
      res.on('data', (c) => (raw += c));
      res.on('end', () => {
        try { resolve(JSON.parse(raw)); }
        catch (e) { reject(new Error(`JSON parse: ${e.message}`)); }
      });
    });
    req.setTimeout(15_000, () => { req.destroy(); reject(new Error('LLM request timed out')); });
    req.on('error', reject);
    req.write(bodyStr);
    req.end();
  });
}

async function _callLlm(signal, provider) {
  const prompt = `You are a crypto trading decision engine. Analyze this market signal and decide whether to execute a trade or hold.

Signal data:
${JSON.stringify(signal, null, 2)}

Rules:
- Only trade if confidence is genuinely high and the signal is clear
- Avoid over-trading; a hold is often the correct answer
- Direction is already determined by the signal engine

Respond with ONLY valid JSON, no markdown, no extra text:
{"action": "trade", "reasoning": "one sentence"}
or
{"action": "hold", "reasoning": "one sentence"}`;

  if (provider === 'ollama') {
    const model    = process.env.OLLAMA_MODEL || 'qwen3.5:35b';
    const baseUrl  = process.env.OLLAMA_URL.replace(/\/$/, '');
    const response = await _httpPostJson(`${baseUrl}/api/chat`, {
      model,
      messages: [{ role: 'user', content: prompt }],
      stream:   false,
    });
    const content = response.message?.content || '';
    return JSON.parse(content.trim());
  }

  if (provider === 'openai') {
    const response = await _httpPostJson(
      'https://api.openai.com/v1/chat/completions',
      { model: 'gpt-4o-mini', messages: [{ role: 'user', content: prompt }] },
      { Authorization: `Bearer ${process.env.OPENAI_API_KEY}` },
    );
    const content = response.choices?.[0]?.message?.content || '';
    return JSON.parse(content.trim());
  }

  throw new Error(`Unknown LLM provider: ${provider}`);
}

async function _getDecision(signal) {
  if (process.env.OLLAMA_URL) {
    try {
      const result = await _callLlm(signal, 'ollama');
      return { ...result, layer: 'ollama' };
    } catch (err) {
      console.warn(`  [decision] Ollama failed: ${err.message}`);
    }
  }

  if (process.env.OPENAI_API_KEY) {
    try {
      const result = await _callLlm(signal, 'openai');
      return { ...result, layer: 'openai' };
    } catch (err) {
      console.warn(`  [decision] OpenAI failed: ${err.message}`);
    }
  }

  // Rule-based fallback: confidence >= 0.7 => trade
  const action = signal.confidence >= 0.7 ? 'trade' : 'hold';
  return {
    action,
    layer:     'rule-based',
    reasoning: action === 'trade'
      ? `confidence ${signal.confidence} >= 0.7 threshold`
      : `confidence ${signal.confidence} < 0.7 threshold`,
  };
}

// ── Profit Sweep ──────────────────────────────────────────────────────────────

async function _checkProfitSweep(walletAddress, baselineBalance, isPaper) {
  const threshold    = parseFloat(process.env.PROFIT_SWEEP_THRESHOLD_USD) || 100;
  const sweepAddress = process.env.PROFIT_SWEEP_ADDRESS;

  if (!sweepAddress) { console.warn('[sweep] PROFIT_SWEEP_ADDRESS not set'); return; }

  try {
    const { getAccountBalance } = require('./hyperliquid');
    const balance = await getAccountBalance(walletAddress);
    const profit  = balance - baselineBalance;

    if (profit >= threshold) {
      if (isPaper) {
        console.log(`[sweep] PAPER: profit $${profit.toFixed(2)} exceeds threshold $${threshold} — would sweep to ${sweepAddress}`);
      } else {
        console.log(`[sweep] Profit $${profit.toFixed(2)} >= threshold $${threshold} — manual withdrawal recommended to: ${sweepAddress}`);
      }
    }
  } catch (err) {
    console.warn(`[sweep] Check failed: ${err.message}`);
  }
}

// ── Main ──────────────────────────────────────────────────────────────────────

async function main() {
  switch (command) {

    // ── Autonomous Trading Loop ───────────────────────────────────────────────

    case 'start': {
      const isPaper       = args.includes('--paper');
      const walletAddress = process.env.HYPERLIQUID_WALLET_ADDRESS || '';
      const intervalMs    = Math.min((parseInt(process.env.CRON_INTERVAL_MINUTES, 10) || 60) * 60 * 1000, 2_147_483_647); // cap at ~24.8 days (setInterval 32-bit limit)
      const maxOpenPos    = parseInt(process.env.MAX_OPEN_POSITIONS, 10)  || 3;
      const maxPosUsd     = parseFloat(process.env.MAX_POSITION_SIZE_USD) || 500;
      const kellyFraction = parseFloat(process.env.KELLY_FRACTION)        || 0.25;
      const scanCoins     = (process.env.SCAN_COINS || 'BTC,ETH,RUNE,SOL,AVAX')
        .split(',').map((s) => s.trim().toUpperCase()).filter(Boolean);

      if (!isPaper && !process.env.HYPERLIQUID_PRIVATE_KEY) {
        console.error('Error: HYPERLIQUID_PRIVATE_KEY not set. Use --paper for paper trading.');
        console.error('Run: node src/setup-check.js');
        process.exit(1);
      }

      console.log('\n-- HL Trading Agent -------------------------------------------------');
      console.log(`Mode:     ${isPaper ? 'PAPER (no real orders)' : 'LIVE'}`);
      console.log(`Coins:    ${scanCoins.join(', ')}`);
      console.log(`Interval: every ${process.env.CRON_INTERVAL_MINUTES || 60} minutes`);
      console.log(`Max pos:  $${maxPosUsd} / position, ${maxOpenPos} max open`);

      let baselineBalance = 0;
      if (!isPaper && walletAddress) {
        try {
          const { getAccountBalance } = require('./hyperliquid');
          baselineBalance = await getAccountBalance(walletAddress);
          console.log(`Balance:  $${baselineBalance.toFixed(2)} USDC`);
        } catch (err) {
          console.warn(`[start] Balance fetch failed: ${err.message}`);
        }
      }

      const runCycle = async () => {
        const ts = new Date().toISOString();
        console.log(`\n[${ts}] Cycle start`);

        try {
          const allSignals = await scanSignals(scanCoins);
          const actionable = allSignals.filter((s) => s.direction !== null);
          console.log(`  Signals: ${allSignals.length} scanned, ${actionable.length} actionable`);

          for (const signal of actionable) {
            console.log(`  Signal: ${signal.coin} ${signal.signal} | ${signal.direction} | conf ${signal.confidence}`);

            const decision = await _getDecision(signal);
            console.log(`  Decision [${decision.layer}]: ${decision.action} -- ${decision.reasoning}`);

            if (decision.action !== 'trade') continue;

            // Enforce max open positions (live only)
            if (!isPaper && walletAddress) {
              const openPos = await getPositions(walletAddress);
              if (openPos.length >= maxOpenPos) {
                console.log(`  Skip ${signal.coin}: ${maxOpenPos} positions open`);
                continue;
              }
            }

            // Position sizing
            let sizeUsd;
            if (isPaper) {
              sizeUsd = Math.min(signal.confidence * kellyFraction * 10_000, maxPosUsd);
            } else {
              try {
                const { calculatePositionSize } = require('./sizing');
                const sizing = await calculatePositionSize(signal.confidence, walletAddress);
                sizeUsd = sizing.sizeUsd;
                console.log(`  Sizing: $${sizeUsd} (${sizing.kellySizePct}% Kelly of $${sizing.balance})`);
              } catch (err) {
                console.warn(`  Sizing failed: ${err.message} -- aborting trade`);
                continue;
              }
            }

            if (sizeUsd < 5) {
              console.log(`  Skip ${signal.coin}: size $${sizeUsd.toFixed(2)} < $5 minimum`);
              continue;
            }

            const isBuy = signal.direction === 'long';

            if (isPaper) {
              const side  = isBuy ? 'long' : 'short';
              const trade = await placePaperTrade(signal.coin, side, sizeUsd);
              console.log(`  Paper trade: ${side.toUpperCase()} $${sizeUsd.toFixed(2)} ${signal.coin} @ $${trade.entryPrice}`);
            } else {
              const { placeOrder } = require('./trader');
              const mids = await getMarketData(signal.coin);
              if (mids.length === 0) {
                console.warn(`  No market data for ${signal.coin} -- skip`);
                continue;
              }
              const result = await placeOrder({
                coin: signal.coin, isBuy, sizeUsd,
                markPrice: mids[0].midPrice, orderType: 'market',
              });
              if (result.success) {
                console.log(`  Trade: ${result.side.toUpperCase()} ${result.size} ${result.coin} @ $${result.fillPrice} (id: ${result.orderId})`);
              } else {
                console.warn(`  Trade failed: ${result.error}`);
              }
            }
          }

          if (actionable.length === 0) console.log('  No actionable signals -- holding.');

          if (process.env.PROFIT_SWEEP_ENABLED === 'true') {
            await _checkProfitSweep(walletAddress, baselineBalance, isPaper);
          }

        } catch (err) {
          console.error(`  Cycle error: ${err.message}`);
        }
      };

      await runCycle();

      if (intervalMs > 0) {
        const timer = setInterval(runCycle, intervalMs);
        console.log(`\nRunning every ${process.env.CRON_INTERVAL_MINUTES || 60} min. Ctrl+C to stop.`);
        process.on('SIGINT', () => { clearInterval(timer); console.log('\nAgent stopped.'); process.exit(0); });
      }
      break;
    }

    // ── THORChain ─────────────────────────────────────────────────────────────

    case 'quote': {
      const [fromAsset, toAsset, amount, destination] = args;
      if (!fromAsset || !toAsset || !amount) {
        console.error('Usage: quote <fromAsset> <toAsset> <amount> [destination]');
        console.error('Example: quote ETH.ETH BTC.BTC 100000000');
        process.exit(1);
      }
      console.log(`\nFetching THORChain quote: ${fromAsset} -> ${toAsset} (amount: ${amount})`);
      try {
        const quote = await getQuote(fromAsset, toAsset, amount, destination);
        console.log('\nQuote:');
        console.log(JSON.stringify(quote, null, 2));
        if (destination) {
          const memo = formatSwapMemo(toAsset, destination, quote.recommended_min_amount_in || 0);
          console.log(`\nSuggested memo: ${memo}`);
        }
      } catch (err) {
        console.error('Error fetching quote:', err.message);
        if (err.response) console.error('Response:', err.response.data);
        process.exit(1);
      }
      break;
    }

    case 'inbound': {
      const [chain] = args;
      console.log('\nFetching THORChain inbound addresses...');
      try {
        const addresses = await getInboundAddresses();
        const filtered  = chain
          ? addresses.filter((a) => a.chain?.toUpperCase() === chain.toUpperCase())
          : addresses;
        console.log(JSON.stringify(filtered, null, 2));
      } catch (err) {
        console.error('Error fetching inbound addresses:', err.message);
        process.exit(1);
      }
      break;
    }

    case 'scan': {
      const asset       = args.find((a) => !a.startsWith('--')) || 'ALL';
      const strategyIdx = args.indexOf('--strategy');
      const strategy    = strategyIdx !== -1 ? args[strategyIdx + 1] : 'all';
      const limitIdx    = args.indexOf('--limit');
      const limit       = limitIdx !== -1 ? parseInt(args[limitIdx + 1], 10) : 10;

      console.log(`\nRunning market scan (asset: ${asset}, strategy: ${strategy}, limit: ${limit})...`);
      try {
        const [signals, opportunities] = await Promise.all([
          getEcosystemSignals(asset),
          getMarketScan({ limit, strategy }),
        ]);
        console.log('\n-- Ecosystem Signals --');
        console.log(JSON.stringify(signals, null, 2));
        console.log('\n-- Market Opportunities --');
        console.log(JSON.stringify(opportunities, null, 2));
      } catch (err) {
        console.error('Error running scan:', err.message);
        process.exit(1);
      }
      break;
    }

    // ── Hyperliquid ───────────────────────────────────────────────────────────

    case 'hl-data': {
      const [coin] = args;
      console.log(`\nFetching Hyperliquid market data${coin ? ` for ${coin.toUpperCase()}` : ' (all coins)'}...`);
      try {
        const [prices, funding] = await Promise.all([
          getMarketData(coin),
          getFundingRates(coin),
        ]);

        const fundingMap = {};
        funding.forEach((f) => { fundingMap[f.coin] = f; });

        console.log('\n-- Mid Prices --');
        if (prices.length === 0) {
          console.log(`No data found for ${coin}`);
        } else {
          prices.slice(0, 20).forEach((p) => {
            const f       = fundingMap[p.coin];
            const fundStr = f ? ` | funding: ${(f.fundingRate * 100).toFixed(4)}%/hr` : '';
            console.log(`  ${p.coin.padEnd(12)} $${p.midPrice.toFixed(4).padStart(12)}${fundStr}`);
          });
          if (prices.length > 20) console.log(`  ... and ${prices.length - 20} more`);
        }

        if (funding.length > 0 && !coin) {
          console.log('\n-- Top Funding Rates (by OI) --');
          funding.slice(0, 10).forEach((f) => {
            const annualised = (f.fundingRate * 8760 * 100).toFixed(1);
            console.log(`  ${f.coin.padEnd(12)} ${(f.fundingRate * 100).toFixed(4)}%/hr (${annualised}% APR) | OI: $${(f.openInterest / 1e6).toFixed(2)}M`);
          });
        }
      } catch (err) {
        console.error('Error fetching Hyperliquid data:', err.message);
        if (err.response) console.error('Response:', JSON.stringify(err.response.data));
        process.exit(1);
      }
      break;
    }

    case 'hl-positions': {
      const walletAddress = args.find((a) => !a.startsWith('--')) || process.env.HYPERLIQUID_WALLET_ADDRESS || '';
      const isPaper       = args.includes('--paper');

      if (isPaper) {
        const positions = getPaperPositions();
        console.log(`\n-- Paper Positions (${positions.length}) --`);
        if (positions.length === 0) {
          console.log('No open paper positions. Use hl-trade --paper to add one.');
        } else {
          positions.forEach((p) => {
            console.log(`  ${p.id} | ${p.coin} ${p.side.toUpperCase()} | size: ${p.size} | entry: $${p.entryPrice} | pnl: $${p.pnl}`);
          });
        }
      } else {
        console.log(`\nFetching positions${walletAddress ? ` for ${walletAddress}` : ' (demo mode)'}...`);
        try {
          const positions = await getPositions(walletAddress);
          if (positions.length === 0) {
            console.log('No open positions.');
          } else {
            console.log('\n-- Open Positions --');
            positions.forEach((p) => {
              console.log(`  ${p.coin.padEnd(10)} ${p.side.toUpperCase()} | size: ${p.size} | entry: $${p.entryPrice} | uPnL: $${p.unrealisedPnl.toFixed(2)}`);
            });
          }
        } catch (err) {
          console.error('Error fetching positions:', err.message);
          if (err.response) console.error('Response:', JSON.stringify(err.response.data));
          process.exit(1);
        }
      }
      break;
    }

    case 'hl-trade': {
      const coinIdx  = args.indexOf('--coin');
      const sideIdx  = args.indexOf('--side');
      const sizeIdx  = args.indexOf('--size');
      const priceIdx = args.indexOf('--price');
      const isPaper  = args.includes('--paper');

      const coin  = coinIdx  !== -1 ? args[coinIdx  + 1] : null;
      const side  = sideIdx  !== -1 ? args[sideIdx  + 1] : null;
      const size  = sizeIdx  !== -1 ? parseFloat(args[sizeIdx  + 1]) : null;
      const price = priceIdx !== -1 ? parseFloat(args[priceIdx + 1]) : undefined;

      if (!coin || !side || !size) {
        console.error('Usage: hl-trade --coin <COIN> --side <long|short> --size <n> [--price <p>] --paper');
        console.error('Example: node src/index.js hl-trade --coin RUNE --side long --size 10 --paper');
        process.exit(1);
      }
      if (!isPaper) {
        console.error('Use the "start" command for live trading. hl-trade is paper-only.');
        process.exit(1);
      }

      console.log(`\nPlacing paper trade: ${side.toUpperCase()} ${size} ${coin.toUpperCase()}${price ? ` @ $${price}` : ' @ market'}...`);
      try {
        const trade = await placePaperTrade(coin, side, size, price);
        console.log('\nPaper trade recorded:');
        console.log(`  ID:    ${trade.id}`);
        console.log(`  Coin:  ${trade.coin}`);
        console.log(`  Side:  ${trade.side.toUpperCase()}`);
        console.log(`  Size:  ${trade.size}`);
        console.log(`  Entry: $${trade.entryPrice}`);
        console.log(`  Time:  ${trade.timestamp}`);
        console.log(`\nStored in data/paper-trades.json -- run hl-positions --paper to view.`);
      } catch (err) {
        console.error('Error placing paper trade:', err.message);
        process.exit(1);
      }
      break;
    }

    case 'hl-arb': {
      // FIXED: uses Midgard assetPriceUSD instead of THORChain swap quotes.
      // Swap quotes include flat outbound fees that distort pricing on small amounts.
      const coins        = args.length > 0 ? args : ['BTC', 'ETH', 'RUNE', 'ATOM', 'BNB', 'AVAX', 'LTC', 'DOGE'];
      const arbThreshold = 0.01;

      console.log(`\nRunning arb scan: THORChain vs Hyperliquid for [${coins.join(', ')}]...`);
      console.log('  (Prices via Midgard assetPriceUSD -- fee-free spot prices)');
      console.log('-'.repeat(70));
      console.log(`  ${'Coin'.padEnd(8)} ${'THORChain'.padStart(12)} ${'Hyperliquid'.padStart(13)} ${'Gap %'.padStart(8)}  Signal`);
      console.log('-'.repeat(70));

      const thorPrices = await getMidgardPrices(coins);

      const results = [];
      for (const coin of coins) {
        try {
          const hlMids    = await getMarketData(coin);
          const hlPrice   = hlMids.length > 0 ? hlMids[0].midPrice : null;
          const thorPrice = thorPrices[coin.toUpperCase()] || null;

          if (hlPrice && thorPrice && thorPrice > 0) {
            const gapPct = ((hlPrice - thorPrice) / thorPrice) * 100;
            const signal = Math.abs(gapPct) >= arbThreshold * 100 ? '!! POTENTIAL ARB' : '--';
            results.push({ coin, thorPrice, hlPrice, gapPct, signal });
            console.log(
              `  ${coin.padEnd(8)} ` +
              `$${thorPrice.toFixed(4).padStart(11)} ` +
              `$${hlPrice.toFixed(4).padStart(12)} ` +
              `${gapPct.toFixed(2).padStart(7)}%  ${signal}`,
            );
          } else if (hlPrice) {
            console.log(
              `  ${coin.padEnd(8)} ${'N/A'.padStart(11)} ` +
              `$${hlPrice.toFixed(4).padStart(12)} ` +
              `${'--'.padStart(7)}%  (Midgard price unavailable)`,
            );
          }
        } catch (err) {
          console.log(`  ${coin.padEnd(8)} Error: ${err.message}`);
        }
      }
      console.log('-'.repeat(70));

      const arbOpps = results.filter((r) => Math.abs(r.gapPct) >= arbThreshold * 100);
      if (arbOpps.length > 0) {
        console.log(`\n${arbOpps.length} arb opportunity(ies) above ${arbThreshold * 100}% threshold:`);
        arbOpps.forEach((o) => {
          const dir = o.gapPct > 0 ? 'buy on THORChain, sell on Hyperliquid' : 'buy on Hyperliquid, sell on THORChain';
          console.log(`  ${o.coin}: ${Math.abs(o.gapPct).toFixed(2)}% gap -- ${dir}`);
        });
      } else {
        console.log('\nNo arb opportunities above 1% threshold found.');
      }
      break;
    }

    default: {
      console.log(`
HL Trading Agent -- Hyperliquid perp DEX + THORChain routing

-- Autonomous Trading -------------------------------------------------

  start [--paper]
      Run the full signal -> decision -> trade loop autonomously.
      --paper  Simulates trades only. No private key needed.
      Example: node src/index.js start --paper
      Example: node src/index.js start

-- Hyperliquid --------------------------------------------------------

  hl-data [coin]
      Live mid prices and funding rates.
      Example: node src/index.js hl-data RUNE

  hl-positions [address] [--paper]
      Open positions for a wallet, or paper trade log.
      Example: node src/index.js hl-positions 0xabc...
      Example: node src/index.js hl-positions --paper

  hl-trade --coin <COIN> --side <long|short> --size <n> [--price <p>] --paper
      Record a manual paper trade.
      Example: node src/index.js hl-trade --coin RUNE --side long --size 10 --paper

  hl-arb [coin ...]
      THORChain spot (Midgard) vs Hyperliquid mark price comparison.
      Example: node src/index.js hl-arb
      Example: node src/index.js hl-arb BTC ETH RUNE

-- THORChain ----------------------------------------------------------

  quote <fromAsset> <toAsset> <amount> [destination]
      THORChain swap quote.
      Example: node src/index.js quote ETH.ETH BTC.BTC 100000000

  inbound [chain]
      THORChain inbound vault addresses.
      Example: node src/index.js inbound ETH

  scan [asset] [--strategy all|momentum|funding_arbitrage] [--limit n]
      Market opportunity scan.
      Example: node src/index.js scan ETH --strategy momentum

-- Setup --------------------------------------------------------------

  node src/setup-check.js
      Validate your .env and test API connectivity before going live.
`);
      process.exit(0);
    }
  }
}

main().catch((err) => {
  console.error('Fatal:', err.message);
  process.exit(1);
});
