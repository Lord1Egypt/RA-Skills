#!/usr/bin/env node

/**
 * TradeBot Alpha Connector v0.1.13
 * MIT-0 License | © 2026 BlueFeza KG
 * 
 * Read-only signal fetcher for TradeBot Alpha API.
 * API endpoint: https://tradebot-alpha.bluefeza.com/api/v1
 */

const API_BASE = 'https://tradebot-alpha.bluefeza.com/api/v1';

// Parse CLI args
const args = process.argv.slice(2);
let apiKey = null;
let command = null;
let symbol = 'BTC';

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--key' && args[i + 1]) {
    apiKey = args[i + 1];
    i++;
  } else if (!command) {
    command = args[i];
  } else if (command === 'analyze') {
    symbol = args[i] || 'BTC';
  }
}

if (!command || command === 'help') {
  console.log(`
TradeBot Alpha Connector v0.1.10

Usage:
  tradebot-alpha --key KEY analyze [SYMBOL]   Get signals
  tradebot-alpha --key KEY status             Show status
  tradebot-alpha help                         This help

Get API key: https://tradebot-alpha.bluefeza.com
`);
  process.exit(0);
}

async function apiCall(endpoint) {
  if (!apiKey) {
    console.log('Pro tier required. Get API key:');
    console.log('https://tradebot-alpha.bluefeza.com');
    return null;
  }
 
  try {
    const res = await fetch(`${API_BASE}${endpoint}`, {
      headers: { 'Authorization': `Bearer ${apiKey}` }
    });
    
    if (res.status === 401) {
      console.log('Invalid API key');
      return null;
    }
    if (!res.ok) {
      console.log(`Error: ${res.status}`);
      return null;
    }
    
    return await res.json();
  } catch (e) {
    console.log('Connection failed');
    return null;
  }
}

async function status() {
  console.log('\nStatus:');
  console.log('Key: ' + (apiKey ? 'Provided' : 'None'));
  
  if (apiKey) {
    const s = await apiCall('/status');
    if (s) console.log('Tier: ' + (s.tier || 'Pro'));
  }
  console.log('');
}

async function analyze(sym) {
  console.log(`\n${sym} analysis...`);
  
  const a = await apiCall(`/analyze/${sym}`);
  if (!a) return;
  
  console.log(`Signal: ${a.signal?.toUpperCase() || 'NEUTRAL'}`);
  console.log(`Confidence: ${(a.confidence * 100).toFixed(1)}%`);
  console.log(`Entry: $${a.entryZone?.lower} - $${a.entryZone?.upper}`);
  console.log(`SL: $${a.stopLoss} | TP: $${a.takeProfit}`);
  
  if (a.plan?.status === 'ready') {
    console.log(`READY: ${a.plan.direction.toUpperCase()}`);
  }
  console.log('');
}

(async () => {
  if (command === 'status') await status();
  else if (command === 'analyze') await analyze(symbol);
  else {
    console.log('Unknown command. Use: help');
    process.exit(1);
  }
})();
