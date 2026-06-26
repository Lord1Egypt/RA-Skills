#!/usr/bin/env node
/**
 * SUPAH Base Intelligence Skill
 * 
 * Provides token intelligence for Base blockchain via SUPAH API
 * All access via x402 USDC micropayments on Base — no API keys
 */

const https = require('https');

const API_BASE = process.env.SUPAH_API_BASE || 'api.supah.ai';

function apiRequest(path) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: API_BASE,
      port: 443,
      path: path,
      method: 'GET',
      headers: {
        'User-Agent': 'OpenClaw-SUPAH-Skill/1.2.0'
      }
    };
    
    https.get(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error('Invalid JSON response'));
        }
      });
    }).on('error', reject);
  });
}

async function getEthMarketRegime() {
  try {
    const data = await apiRequest('/agent/v1/market/regime');
    return { success: true, data };
  } catch (err) {
    return { success: false, error: err.message };
  }
}

async function scanToken(address) {
  try {
    const data = await apiRequest(`/agent/v1/token/${address}`);
    return { success: true, data, cost: '$0.08 (token scan)' };
  } catch (err) {
    return { success: false, error: err.message };
  }
}

async function checkSafety(address) {
  try {
    const data = await apiRequest(`/agent/v1/safety/${address}`);
    return { success: true, data, cost: '$0.08 (safety scan)' };
  } catch (err) {
    return { success: false, error: err.message };
  }
}

async function analyzeWallet(wallet) {
  try {
    const data = await apiRequest(`/agent/v1/portfolio/${wallet}`);
    return { success: true, data, cost: '$0.05 (portfolio scan)' };
  } catch (err) {
    return { success: false, error: err.message };
  }
}

async function getSignals() {
  try {
    const data = await apiRequest('/agent/v1/signals?minScore=85');
    return { success: true, data, cost: '$0.15 (signal feed)' };
  } catch (err) {
    return { success: false, error: err.message };
  }
}

async function getDegenTop5() {
  try {
    const data = await apiRequest('/agent/v1/discovery/degen/top5');
    return { success: true, data, cost: '$0.15 (degen top 5)' };
  } catch (err) {
    return { success: false, error: err.message };
  }
}

async function getSwingTop5() {
  try {
    const data = await apiRequest('/agent/v1/discovery/swing/top5');
    return { success: true, data, cost: '$0.15 (swing top 5)' };
  } catch (err) {
    return { success: false, error: err.message };
  }
}

async function trackWhales(address) {
  try {
    const data = await apiRequest(`/agent/v1/whales/${address}`);
    return { success: true, data, cost: '$0.15 (whale tracking)' };
  } catch (err) {
    return { success: false, error: err.message };
  }
}

async function getWhaleAlerts() {
  try {
    const data = await apiRequest('/agent/v1/whale-alerts');
    return { success: true, data, cost: '$0.15 (whale alerts)' };
  } catch (err) {
    return { success: false, error: err.message };
  }
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  const param = args[1];
  
  (async () => {
    let result;
    
    switch (command) {
      case 'eth':
      case 'market':
        result = await getEthMarketRegime();
        break;
      case 'scan':
      case 'token':
        if (!param) { console.log('Usage: supah-base-intelligence scan <token-address>'); process.exit(1); }
        result = await scanToken(param);
        break;
      case 'safety':
        if (!param) { console.log('Usage: supah-base-intelligence safety <token-address>'); process.exit(1); }
        result = await checkSafety(param);
        break;
      case 'wallet':
      case 'portfolio':
        if (!param) { console.log('Usage: supah-base-intelligence wallet <address>'); process.exit(1); }
        result = await analyzeWallet(param);
        break;
      case 'signals':
        result = await getSignals();
        break;
      case 'degen':
        result = await getDegenTop5();
        break;
      case 'swing':
        result = await getSwingTop5();
        break;
      case 'whales':
        if (!param) { console.log('Usage: supah-base-intelligence whales <token-address>'); process.exit(1); }
        result = await trackWhales(param);
        break;
      case 'whale-alerts':
        result = await getWhaleAlerts();
        break;
      default:
        console.log('🦸 SUPAH Base Intelligence Skill v1.2.0\n');
        console.log('Commands:');
        console.log('  eth                    - ETH market regime ($0.03)');
        console.log('  scan <address>         - Token risk score ($0.08)');
        console.log('  safety <address>       - Security scan ($0.08)');
        console.log('  wallet <address>       - Portfolio analysis ($0.05)');
        console.log('  signals                - High-conviction signals ($0.15)');
        console.log('  degen                  - Degen top 5 ($0.15)');
        console.log('  swing                  - Swing top 5 ($0.15)');
        console.log('  whales <address>       - Whale tracking ($0.15)');
        console.log('  whale-alerts           - Recent whale alerts ($0.15)\n');
        console.log('Payment: x402 USDC micropayments on Base (automatic)\n');
        process.exit(0);
    }
    
    if (result.success) {
      console.log(JSON.stringify(result.data, null, 2));
      if (result.cost) console.error(`\n💰 Cost: ${result.cost}`);
    } else {
      console.error('❌ Error:', result.error);
      process.exit(1);
    }
  })();
}

module.exports = {
  getEthMarketRegime, scanToken, checkSafety, analyzeWallet,
  getSignals, getDegenTop5, getSwingTop5, trackWhales, getWhaleAlerts
};
