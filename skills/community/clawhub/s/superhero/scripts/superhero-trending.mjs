#!/usr/bin/env node
// Check trending tokens and tags on superhero.com

const API_BASE = 'https://api.superhero.com';

async function main() {
  const command = process.argv[2] || 'help';

  switch (command) {
    case 'tokens': {
      const limit = parseInt(process.argv[3]) || 20;
      const orderBy = process.argv[4] || 'trending_score';
      const page = parseInt(process.argv[5]) || 1;
      const url = `${API_BASE}/api/tokens?order_by=${encodeURIComponent(orderBy)}&order_direction=DESC&limit=${limit}&page=${page}`;
      const res = await fetch(url);
      if (!res.ok) { console.error(`API error: ${res.status}`); process.exit(1); }
      const data = await res.json();
      const tokens = (data.items || data.data || []).map(t => ({
        name: t.name,
        symbol: t.symbol,
        sale_address: t.sale_address,
        price_ae: t.price,
        market_cap: t.market_cap,
        trending_score: t.trending_score,
        holders_count: t.holders_count,
      }));
      console.log(JSON.stringify(tokens, null, 2));
      break;
    }

    case 'tags': {
      const limit = parseInt(process.argv[3]) || 20;
      const url = `${API_BASE}/api/trending-tags?limit=${limit}`;
      const res = await fetch(url);
      if (!res.ok) { console.error(`API error: ${res.status}`); process.exit(1); }
      const data = await res.json();
      console.log(JSON.stringify(data, null, 2));
      break;
    }

    case 'token-info': {
      const address = process.argv[3];
      if (!address) {
        console.error('Usage: node scripts/superhero-trending.mjs token-info <sale_address>');
        process.exit(1);
      }
      const url = `${API_BASE}/api/tokens/${encodeURIComponent(address)}`;
      const res = await fetch(url);
      if (!res.ok) { console.error(`Token not found: ${res.status}`); process.exit(1); }
      console.log(JSON.stringify(await res.json(), null, 2));
      break;
    }

    case 'performance': {
      const address = process.argv[3];
      if (!address) {
        console.error('Usage: node scripts/superhero-trending.mjs performance <sale_address>');
        process.exit(1);
      }
      const url = `${API_BASE}/api/tokens/${encodeURIComponent(address)}/performance`;
      const res = await fetch(url);
      if (!res.ok) { console.error(`Not found: ${res.status}`); process.exit(1); }
      console.log(JSON.stringify(await res.json(), null, 2));
      break;
    }

    case 'leaderboard': {
      const url = `${API_BASE}/api/accounts/leaderboard`;
      const res = await fetch(url);
      if (!res.ok) { console.error(`API error: ${res.status}`); process.exit(1); }
      console.log(JSON.stringify(await res.json(), null, 2));
      break;
    }

    case 'analytics': {
      const url = `${API_BASE}/api/analytics`;
      const res = await fetch(url);
      if (!res.ok) { console.error(`API error: ${res.status}`); process.exit(1); }
      console.log(JSON.stringify(await res.json(), null, 2));
      break;
    }

    case 'help':
    default:
      console.log(`
Superhero Trending & Market Commands:

  tokens [limit] [order_by]       List tokens sorted by trending score
  tags [limit]                    Get trending hashtags
  token-info <sale_address>       Get detailed token info
  performance <sale_address>      Get price performance (24h/7d/30d)
  leaderboard                     Get trading leaderboard
  analytics                       Get platform analytics

Examples:
  node scripts/superhero-trending.mjs tokens 10
  node scripts/superhero-trending.mjs tags 5
  node scripts/superhero-trending.mjs token-info ct_abc...
  node scripts/superhero-trending.mjs performance ct_abc...
  node scripts/superhero-trending.mjs leaderboard
`);
  }
}

main().catch(e => { console.error('ERROR:', e.message || e); process.exit(1); });
