#!/usr/bin/env node
// View token holdings and portfolio history for your wallet or any account

import { MemoryAccount } from '@aeternity/aepp-sdk';

const API_BASE = 'https://api.superhero.com';

function loadAddress() {
  const privateKey = process.env.AE_PRIVATE_KEY;
  if (!privateKey) {
    console.error('AE_PRIVATE_KEY environment variable is not set. Set it with: export AE_PRIVATE_KEY=<your_secret_key>');
    process.exit(1);
  }
  return new MemoryAccount(privateKey).address;
}

async function main() {
  const command = process.argv[2] || 'help';

  switch (command) {
    case 'holdings': {
      // Get tokens currently held by an account
      const address = process.argv[3] || loadAddress();
      const limit = parseInt(process.argv[4]) || 50;
      const page = parseInt(process.argv[5]) || 1;
      const url = `${API_BASE}/api/accounts/${encodeURIComponent(address)}/tokens?includes=token&limit=${limit}&page=${page}`;
      const res = await fetch(url);
      if (!res.ok) { console.error(`API error: ${res.status} ${await res.text()}`); process.exit(1); }
      const data = await res.json();
      const items = (data.items || data.data || data || []).map(h => ({
        token_name: h.token?.name,
        token_symbol: h.token?.symbol,
        sale_address: h.token?.sale_address,
        token_address: h.aex9_address || h.token?.address,
        balance: h.balance,
        buy_price_ae: h.token?.price,
        sell_price_ae: h.token?.sell_price,
        trending_score: h.token?.trending_score,
      }));
      console.log(JSON.stringify({ address, holdings: items }, null, 2));
      break;
    }

    case 'history': {
      // Get portfolio value history (PnL over time)
      const address = process.argv[3] || loadAddress();
      const url = `${API_BASE}/api/accounts/${encodeURIComponent(address)}/portfolio/history`;
      const res = await fetch(url);
      if (!res.ok) { console.error(`API error: ${res.status} ${await res.text()}`); process.exit(1); }
      const data = await res.json();
      // Return latest snapshot + summary
      const snapshots = Array.isArray(data) ? data : data.items || [];
      if (snapshots.length === 0) {
        console.log(JSON.stringify({ address, message: 'No portfolio history found', snapshots: [] }, null, 2));
        break;
      }
      const latest = snapshots[snapshots.length - 1];
      const oldest = snapshots[0];
      const summary = {
        address,
        latest_snapshot: latest,
        oldest_snapshot: oldest,
        period_pnl_ae: latest.total_value_ae != null && oldest.total_value_ae != null
          ? (latest.total_value_ae - oldest.total_value_ae).toFixed(6)
          : null,
        period_pnl_usd: latest.total_value_usd != null && oldest.total_value_usd != null
          ? (latest.total_value_usd - oldest.total_value_usd).toFixed(4)
          : null,
        snapshots_count: snapshots.length,
        all_snapshots: snapshots,
      };
      console.log(JSON.stringify(summary, null, 2));
      break;
    }

    case 'summary': {
      // Combined: current AE balance + holdings + latest portfolio snapshot
      const address = process.argv[3] || loadAddress();

      const [holdingsRes, historyRes] = await Promise.all([
        fetch(`${API_BASE}/api/accounts/${encodeURIComponent(address)}/tokens?includes=token&limit=50`),
        fetch(`${API_BASE}/api/accounts/${encodeURIComponent(address)}/portfolio/history`),
      ]);

      const holdingsData = holdingsRes.ok ? await holdingsRes.json() : null;
      const historyData = historyRes.ok ? await historyRes.json() : null;

      const holdings = holdingsData
        ? (holdingsData.items || holdingsData.data || holdingsData || []).map(h => ({
            token_name: h.token?.name,
            token_symbol: h.token?.symbol,
            sale_address: h.token?.sale_address,
            token_address: h.aex9_address || h.token?.address,
            balance: h.balance,
            buy_price_ae: h.token?.price,
            sell_price_ae: h.token?.sell_price,
            trending_score: h.token?.trending_score,
          }))
        : [];

      const snapshots = historyData
        ? (Array.isArray(historyData) ? historyData : historyData.items || [])
        : [];
      const latest = snapshots.length > 0 ? snapshots[snapshots.length - 1] : null;

      console.log(JSON.stringify({
        address,
        holdings_count: holdings.length,
        holdings,
        portfolio_snapshot: latest,
      }, null, 2));
      break;
    }

    case 'help':
    default:
      console.log(`
Superhero Portfolio Commands:

  holdings [address] [limit] [page]
    List tokens currently held by your wallet (or any address)
    Defaults to your configured wallet address

  history [address]
    Portfolio value over time: AE value, USD value, PnL
    Returns all snapshots + period PnL summary

  summary [address]
    Combined view: holdings + latest portfolio snapshot

Examples:
  node scripts/superhero-portfolio.mjs holdings
  node scripts/superhero-portfolio.mjs holdings ak_abc... 20
  node scripts/superhero-portfolio.mjs history
  node scripts/superhero-portfolio.mjs history ak_abc...
  node scripts/superhero-portfolio.mjs summary
`);
      break;
  }
}

main().catch(err => {
  console.error(err.message || err);
  process.exit(1);
});
