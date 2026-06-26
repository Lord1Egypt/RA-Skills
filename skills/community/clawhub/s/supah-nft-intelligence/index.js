#!/usr/bin/env node
/**
 * SUPAH NFT Intelligence
 * All access via x402 USDC micropayments on Base — no API keys
 */
const https = require('https');
const API = process.env.SUPAH_API_BASE || 'https://api.supah.ai';

function api(path, params = {}) {
  return new Promise((resolve, reject) => {
    const qs = new URLSearchParams(params).toString();
    https.get(`${API}${path}${qs ? '?' + qs : ''}`, { headers: { 'User-Agent': 'OpenClaw-SUPAH-NFT/1.2.0' } }, res => {
      let d = ''; res.on('data', c => d += c);
      res.on('end', () => { try { resolve(JSON.parse(d)); } catch (e) { resolve({ error: 'Invalid response' }); } });
    }).on('error', reject);
  });
}

async function main() {
  const args = process.argv.slice(2);
  if (!args[0]) {
    console.log('\n🖼️ SUPAH NFT Intelligence v1.2.0\n');
    console.log('Commands:');
    console.log('  floor <collection> - Floor price ($0.05)');
    console.log('  track <collection> - Track floor ($0.05)');
    console.log('  value <wallet>     - Portfolio value ($0.05)');
    console.log('  alerts <collection>- Sale alerts ($0.05)\n');
    console.log('Payment: x402 USDC micropayments on Base (automatic)\n');
    return;
  }
  
  const cmd = args[0];
  const input = args.slice(1).join(' ');
  const endpoint = cmd === 'floor' ? `/agent/v1/nft/floor/${input}` :
                   cmd === 'track' ? `/agent/v1/nft/track/${input}` :
                   cmd === 'value' ? `/agent/v1/nft/portfolio/${input}` :
                   cmd === 'alerts' ? `/agent/v1/nft/alerts/${input}` : null;
  
  if (!endpoint) { console.log('Unknown command. Run without arguments for help.'); return; }
  
  const res = await api(endpoint);
  console.log(JSON.stringify(res, null, 2));
}

main().catch(console.error);
