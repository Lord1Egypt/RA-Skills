#!/usr/bin/env node
/**
 * SUPAH Whale Tracker
 * All access via x402 USDC micropayments on Base — no API keys
 */
const https = require('https');
const API = process.env.SUPAH_API_BASE || 'https://api.supah.ai';

function api(path, params = {}) {
  return new Promise((resolve, reject) => {
    const qs = new URLSearchParams(params).toString();
    const url = `${API}${path}${qs ? '?' + qs : ''}`;
    https.get(url, { headers: { 'User-Agent': 'OpenClaw-SUPAH-Whale-Tracker/1.2.0' } }, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => { try { resolve(JSON.parse(d)); } catch (e) { resolve({ error: 'Invalid response' }); } });
    }).on('error', reject);
  });
}

async function main() {
  const args = process.argv.slice(2);
  if (!args[0]) {
    console.log('\n🐋 SUPAH Whale Tracker v1.2.0\n');
    console.log('Commands:');
    console.log('  recent          - Recent whale moves ($0.15)');
    console.log('  track <token>   - Track token whales ($0.15)');
    console.log('  watch <wallet>  - Monitor wallet ($0.15)');
    console.log('  analyze <token> - Historical analysis ($0.15)');
    console.log('  smart           - Smart money following ($0.15)\n');
    console.log('Payment: x402 USDC micropayments on Base (automatic)\n');
    return;
  }
  
  const cmd = args[0];
  const input = args.slice(1).join(' ');
  
  if (cmd === 'recent') {
    console.log('\n🐋 Recent Whale Moves (24h)\n');
    const res = await api('/agent/v1/whale-alerts');
    if (res.error) { console.log('⚠️  API unavailable. Try again shortly.\n'); return; }
    if (res.moves) {
      res.moves.forEach((m, i) => {
        console.log(`${i + 1}. ${m.token} - $${m.valueUSD.toLocaleString()}`);
        console.log(`   ${m.from.slice(0, 10)}... → ${m.to.slice(0, 10)}...`);
        console.log(`   ${m.timeAgo}\n`);
      });
    } else {
      console.log(JSON.stringify(res, null, 2));
    }
  } else if (['track', 'watch', 'analyze', 'smart'].includes(cmd)) {
    const endpoint = cmd === 'track' ? `/agent/v1/whales/${input}` :
                     cmd === 'watch' ? `/agent/v1/portfolio/${input}` :
                     cmd === 'analyze' ? `/agent/v1/whales/${input}/history` :
                     '/agent/v1/whale-alerts/smart';
    const res = await api(endpoint);
    console.log(JSON.stringify(res, null, 2));
  } else {
    console.log('Unknown command. Run without arguments for help.');
  }
}

main().catch(console.error);
