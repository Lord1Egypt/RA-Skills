#!/usr/bin/env node
/**
 * Stock Monitor — checks WooCommerce products for out-of-stock status
 * Sends Telegram alert if any product changes from instock → outofstock
 * 
 * Usage: node scripts/stock-monitor.js
 * Cron: daily at 07:00 UTC
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const WOO_API_PATH = process.env.WOO_API_PATH || path.join(require('os').homedir(), 'woo-api.json');
const STATE_FILE = path.join(__dirname, '../memory/stock-state.json');
const TELEGRAM_TOKEN = process.env.TELEGRAM_BOT_TOKEN;
const TELEGRAM_CHAT = process.env.TELEGRAM_CHAT_ID;

function wooCfg() {
  const cfg = JSON.parse(fs.readFileSync(WOO_API_PATH, 'utf8'));
  const auth = Buffer.from(`${cfg.consumer_key}:${cfg.consumer_secret}`).toString('base64');
  return { base: cfg.url, auth };
}

function httpGet(url, headers = {}) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith('https') ? https : http;
    mod.get(url, { headers }, (res) => {
      let data = '';
      res.on('data', d => data += d);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch(e) { reject(new Error(`Parse error: ${data.slice(0,200)}`)); }
      });
    }).on('error', reject);
  });
}

async function fetchAllProducts(base, auth) {
  const products = [];
  let page = 1;
  while (true) {
    const url = `${base}/wp-json/wc/v3/products?per_page=100&page=${page}&status=publish`;
    const batch = await httpGet(url, { 'Authorization': `Basic ${auth}` });
    if (!Array.isArray(batch) || batch.length === 0) break;
    products.push(...batch);
    if (batch.length < 100) break;
    page++;
  }
  return products;
}

async function sendTelegramAlert(message) {
  if (!TELEGRAM_TOKEN || !TELEGRAM_CHAT) {
    console.log('[Telegram] No token/chat configured, skipping alert');
    return;
  }
  const body = JSON.stringify({ chat_id: TELEGRAM_CHAT, text: message, parse_mode: 'Markdown' });
  return new Promise((resolve) => {
    const req = https.request({
      hostname: 'api.telegram.org',
      path: `/bot${TELEGRAM_TOKEN}/sendMessage`,
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Content-Length': body.length }
    }, (res) => { res.on('data', () => {}); res.on('end', resolve); });
    req.on('error', (e) => console.error('Telegram error:', e.message));
    req.write(body);
    req.end();
  });
}

async function main() {
  console.log(`[${new Date().toISOString()}] Stock monitor starting...`);
  
  let cfg;
  try { cfg = wooCfg(); }
  catch(e) {
    console.error('WooCommerce config not found:', e.message);
    process.exit(1);
  }

  // Load previous state
  let prevState = {};
  if (fs.existsSync(STATE_FILE)) {
    prevState = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
  }

  // Fetch current products
  const products = await fetchAllProducts(cfg.base, cfg.auth);
  console.log(`Fetched ${products.length} products`);

  const currentState = {};
  const newlyOOS = [];
  const allOOS = [];

  for (const p of products) {
    const status = p.stock_status; // 'instock', 'outofstock', 'onbackorder'
    const key = String(p.id);
    currentState[key] = { name: p.name, status, sku: p.sku };

    if (status === 'outofstock') {
      allOOS.push({ id: p.id, name: p.name, sku: p.sku });
    }

    // Check for instock → outofstock transition
    if (prevState[key] && prevState[key].status === 'instock' && status === 'outofstock') {
      newlyOOS.push({ id: p.id, name: p.name, sku: p.sku });
    }
  }

  // Save new state
  fs.mkdirSync(path.dirname(STATE_FILE), { recursive: true });
  fs.writeFileSync(STATE_FILE, JSON.stringify(currentState, null, 2));

  const isFirstRun = Object.keys(prevState).length === 0;

  if (isFirstRun) {
    console.log(`First run baseline — ${allOOS.length} products currently out of stock`);
    if (allOOS.length > 0) {
      const list = allOOS.map(p => `• ${p.name} (SKU: ${p.sku || p.id})`).join('\n');
      const msg = `📦 *Stock Monitor — Baseline Report*\n\n${allOOS.length} products currently OOS:\n${list}`;
      await sendTelegramAlert(msg);
      console.log('Baseline alert sent');
    } else {
      console.log('All products in stock ✅');
    }
  } else if (newlyOOS.length > 0) {
    console.log(`⚠️  ${newlyOOS.length} product(s) just went out of stock!`);
    const list = newlyOOS.map(p => `• ${p.name} (SKU: ${p.sku || p.id})`).join('\n');
    const msg = `⚠️ *Stock Alert — Out of Stock*\n\n${newlyOOS.length} product(s) went OOS:\n${list}\n\nTotal OOS: ${allOOS.length}`;
    await sendTelegramAlert(msg);
    console.log('Alert sent');
  } else {
    console.log(`No new OOS products. Total OOS: ${allOOS.length} / ${products.length}`);
  }

  // Summary
  console.log(`Done. Products: ${products.length}, OOS: ${allOOS.length}, New OOS: ${newlyOOS.length}`);
}

main().catch(e => { console.error('Fatal:', e); process.exit(1); });
