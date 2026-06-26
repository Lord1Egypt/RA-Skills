#!/usr/bin/env node
/**
 * SUPAH Portfolio Guardian
 * 
 * Automated portfolio monitoring and risk alerts for Base blockchain
 * All access via x402 USDC micropayments on Base — no API keys
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

const API_BASE = process.env.SUPAH_API_BASE || 'api.supah.ai';
const STATE_FILE = path.join(process.env.HOME || '/root', '.supah-guardian-state.json');

function loadState() {
  try {
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  } catch {
    return { watchedWallets: [], lastCheck: null };
  }
}

function saveState(state) {
  fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

function apiRequest(reqPath) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: API_BASE,
      port: 443,
      path: reqPath,
      method: 'GET',
      headers: { 'User-Agent': 'OpenClaw-SUPAH-Portfolio-Guardian/1.2.0' }
    };
    
    https.get(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { reject(new Error('Invalid JSON response')); }
      });
    }).on('error', reject);
  });
}

async function watchWallet(address) {
  try {
    const state = loadState();
    if (state.watchedWallets.find(w => w.address === address)) {
      return { success: false, error: 'Wallet already being watched' };
    }
    const data = await apiRequest(`/agent/v1/portfolio/${address}`);
    state.watchedWallets.push({
      address,
      addedAt: new Date().toISOString(),
      lastScore: data.riskScore,
      alertThreshold: 60
    });
    saveState(state);
    return { success: true, data: { address, initialScore: data.riskScore, watching: state.watchedWallets.length }, cost: '$0.10 (watch setup)' };
  } catch (err) {
    return { success: false, error: err.message };
  }
}

async function unwatchWallet(address) {
  const state = loadState();
  const before = state.watchedWallets.length;
  state.watchedWallets = state.watchedWallets.filter(w => w.address !== address);
  saveState(state);
  return { success: true, data: { removed: before > state.watchedWallets.length, stillWatching: state.watchedWallets.length } };
}

async function getPortfolioHealth(address) {
  try {
    const data = await apiRequest(`/agent/v1/portfolio/${address}`);
    const tokens = data.tokens || [];
    const avgScore = tokens.length ? tokens.reduce((sum, t) => sum + (t.score || 0), 0) / tokens.length : 0;
    const riskyTokens = tokens.filter(t => (t.score || 0) < 60);
    const safeTokens = tokens.filter(t => (t.score || 0) >= 80);
    let healthLevel = 'UNKNOWN';
    if (avgScore >= 80) healthLevel = 'EXCELLENT';
    else if (avgScore >= 70) healthLevel = 'GOOD';
    else if (avgScore >= 60) healthLevel = 'FAIR';
    else healthLevel = 'POOR';
    return {
      success: true,
      data: { address, healthLevel, avgScore: Math.round(avgScore), totalTokens: tokens.length, safeTokens: safeTokens.length, riskyTokens: riskyTokens.length, totalValue: data.totalValue, riskExposure: riskyTokens.reduce((sum, t) => sum + (t.value || 0), 0) },
      cost: '$0.10 (health check)'
    };
  } catch (err) {
    return { success: false, error: err.message };
  }
}

async function getRiskAlerts() {
  try {
    const state = loadState();
    const alerts = [];
    for (const wallet of state.watchedWallets) {
      const data = await apiRequest(`/agent/v1/portfolio/${wallet.address}`);
      if (data.riskScore < wallet.alertThreshold && data.riskScore < wallet.lastScore) {
        alerts.push({
          wallet: wallet.address,
          previousScore: wallet.lastScore,
          currentScore: data.riskScore,
          drop: wallet.lastScore - data.riskScore,
          severity: data.riskScore < 50 ? 'HIGH' : 'MEDIUM',
          action: 'Review portfolio immediately'
        });
      }
      wallet.lastScore = data.riskScore;
    }
    state.lastCheck = new Date().toISOString();
    saveState(state);
    return { success: true, data: { alerts, alertCount: alerts.length, walletsChecked: state.watchedWallets.length }, cost: '$0.10 (alert check)' };
  } catch (err) {
    return { success: false, error: err.message };
  }
}

async function getRebalanceSuggestions(address) {
  try {
    const data = await apiRequest(`/agent/v1/portfolio/${address}`);
    const tokens = data.tokens || [];
    const suggestions = [];
    tokens.forEach(token => {
      if (token.score < 60 && token.portfolioPercent > 10) {
        suggestions.push({ action: 'REDUCE', token: token.symbol, address: token.address, currentWeight: token.portfolioPercent, suggestedWeight: 5, reason: `Low risk score (${token.score}/100), overweight position` });
      }
    });
    tokens.forEach(token => {
      if (token.score >= 80 && token.portfolioPercent < 20) {
        suggestions.push({ action: 'INCREASE', token: token.symbol, address: token.address, currentWeight: token.portfolioPercent, suggestedWeight: 25, reason: `High risk score (${token.score}/100), underweight position` });
      }
    });
    return { success: true, data: { address, suggestions, suggestionsCount: suggestions.length, totalValue: data.totalValue, currentBalance: data.riskScore }, cost: '$0.10 (rebalance analysis)' };
  } catch (err) {
    return { success: false, error: err.message };
  }
}

function listWatchedWallets() {
  const state = loadState();
  return { success: true, data: { watchedWallets: state.watchedWallets, count: state.watchedWallets.length, lastCheck: state.lastCheck } };
}

// CLI interface
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  const param = args[1];
  
  (async () => {
    let result;
    switch (command) {
      case 'watch':
        if (!param) { console.log('Usage: supah-portfolio-guardian watch <wallet-address>'); process.exit(1); }
        result = await watchWallet(param);
        break;
      case 'unwatch':
        if (!param) { console.log('Usage: supah-portfolio-guardian unwatch <wallet-address>'); process.exit(1); }
        result = await unwatchWallet(param);
        break;
      case 'list':
        result = listWatchedWallets();
        break;
      case 'health':
        if (!param) { console.log('Usage: supah-portfolio-guardian health <wallet-address>'); process.exit(1); }
        result = await getPortfolioHealth(param);
        break;
      case 'alerts':
        result = await getRiskAlerts();
        break;
      case 'rebalance':
        if (!param) { console.log('Usage: supah-portfolio-guardian rebalance <wallet-address>'); process.exit(1); }
        result = await getRebalanceSuggestions(param);
        break;
      default:
        console.log('🎯 SUPAH Portfolio Guardian v1.2.0\n');
        console.log('Commands:');
        console.log('  watch <address>      - Monitor wallet ($0.10)');
        console.log('  unwatch <address>    - Stop monitoring');
        console.log('  list                 - List watched wallets');
        console.log('  health <address>     - Get health score ($0.10)');
        console.log('  alerts               - Check risk alerts ($0.10)');
        console.log('  rebalance <address>  - Get suggestions ($0.10)\n');
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

module.exports = { watchWallet, unwatchWallet, listWatchedWallets, getPortfolioHealth, getRiskAlerts, getRebalanceSuggestions };
