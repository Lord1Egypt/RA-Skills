#!/usr/bin/env node
/**
 * SUPAH DeFi Optimizer
 * All access via x402 USDC micropayments on Base — no API keys
 */
const https = require('https');
const API = process.env.SUPAH_API_BASE || 'https://api.supah.ai';

function api(path, params = {}) {
  return new Promise((resolve, reject) => {
    const qs = new URLSearchParams(params).toString();
    https.get(`${API}${path}${qs ? '?' + qs : ''}`, { headers: { 'User-Agent': 'OpenClaw-SUPAH-DeFi/1.2.0' } }, res => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => { try { resolve(JSON.parse(d)); } catch (e) { resolve({ error: 'Invalid response' }); } });
    }).on('error', reject);
  });
}

async function main() {
  const args = process.argv.slice(2);
  if (!args[0]) {
    console.log('\n🔄 SUPAH DeFi Optimizer v1.2.0\n');
    console.log('Commands:');
    console.log('  positions <wallet>  - View positions ($0.10)');
    console.log('  optimize <wallet>   - Auto-optimize ($0.10)');
    console.log('  yields              - Compare APYs ($0.10)');
    console.log('  rebalance <wallet>  - Suggestions ($0.10)');
    console.log('  il <position>       - IL calculator ($0.10)\n');
    console.log('Payment: x402 USDC micropayments on Base (automatic)\n');
    return;
  }
  
  const cmd = args[0];
  const input = args.slice(1).join(' ');
  const endpoint = cmd === 'positions' ? `/agent/v1/defi/positions/${input}` :
                   cmd === 'optimize' ? `/agent/v1/defi/optimize/${input}` :
                   cmd === 'yields' ? '/agent/v1/defi/yields' :
                   cmd === 'rebalance' ? `/agent/v1/defi/rebalance/${input}` :
                   cmd === 'il' ? `/agent/v1/defi/il/${input}` : null;
  
  if (!endpoint) { console.log('Unknown command. Run without arguments for help.'); return; }
  
  const res = await api(endpoint);
  console.log(JSON.stringify(res, null, 2));
}

main().catch(console.error);
