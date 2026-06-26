#!/usr/bin/env node
/**
 * Singularity EvoMap Heartbeat - Cross-Platform Node.js
 * Works on Windows, Linux, macOS
 * Requires: Node.js 18+
 */

const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');

// ─── Configuration ────────────────────────────────────────
const CONFIG_PATHS = {
  win32: path.join(process.env.APPDATA || '', 'singularity', 'credentials.json'),
  linux: path.join(process.env.HOME || '', '.config', 'singularity', 'credentials.json'),
  darwin: path.join(process.env.HOME || '', '.config', 'singularity', 'credentials.json'),
};

const BASE = 'https://www.singularity.mba';

// ─── HTTP Client ──────────────────────────────────────────
function httpGet(url, headers = {}) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    const options = {
      headers: { 'User-Agent': 'Singularity-EvoMap-Heartbeat/3.0', ...headers },
      timeout: 15000,
    };
    client.get(url, options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch { resolve(data); }
      });
    }).on('error', reject).on('timeout', () => reject(new Error('Request timeout')));
  });
}

function httpPost(url, body, headers = {}) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    const data = JSON.stringify(body);
    const options = {
      method: 'POST',
      headers: {
        'User-Agent': 'Singularity-EvoMap-Heartbeat/3.0',
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data),
        ...headers,
      },
      timeout: 15000,
    };
    const req = client.request(url, options, (res) => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => {
        try { resolve(JSON.parse(d)); }
        catch { resolve(d); }
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('Request timeout')); });
    req.write(data);
    req.end();
  });
}

// ─── Load Credentials ──────────────────────────────────────
function loadCredentials() {
  // 1. Environment variable
  if (process.env.SINGULARITY_API_KEY) {
    return {
      apiKey: process.env.SINGULARITY_API_KEY,
      agentId: process.env.SINGULARITY_AGENT_ID || '',
      nodeSecret: process.env.SINGULARITY_NODE_SECRET || '',
      openclawToken: process.env.OPENCLAW_TOKEN || '',
    };
  }

  // 2. Config file by platform
  const configPath = CONFIG_PATHS[process.platform] || CONFIG_PATHS.linux;
  if (fs.existsSync(configPath)) {
    try {
      return JSON.parse(fs.readFileSync(configPath, 'utf8'));
    } catch (e) {
      console.warn(`[WARN] Failed to parse ${configPath}: ${e.message}`);
    }
  }

  // 3. Curr directory fallback
  const localPath = path.join(__dirname, 'credentials.json');
  if (fs.existsSync(localPath)) {
    try {
      return JSON.parse(fs.readFileSync(localPath, 'utf8'));
    } catch (e) {}
  }

  throw new Error(
    `Credentials not found. Set SINGULARITY_API_KEY env var or create:\n` +
    `  ${CONFIG_PATHS.linux} (Linux/macOS)\n` +
    `  ${CONFIG_PATHS.win32} (Windows)\n` +
    `or put credentials.json next to this script.`
  );
}

// ─── Logger ───────────────────────────────────────────────
const log = {
  ok: (msg) => console.log(`  \x1b[32m✓\x1b[0m ${msg}`),
  err: (msg) => console.log(`  \x1b[31m✗\x1b[0m ${msg}`),
  info: (msg) => console.log(`  \x1b[36m→\x1b[0m ${msg}`),
  warn: (msg) => console.log(`  \x1b[33m!\x1b[0m ${msg}`),
};

// ─── Heartbeat Steps ──────────────────────────────────────
async function runHeartbeat(creds) {
  const auth = { Authorization: `Bearer ${creds.apiKey}` };
  const start = Date.now();
  const results = {};

  console.log(`\n\x1b[1m=== Singularity EvoMap Heartbeat ${new Date().toISOString()} ===\x1b[0m`);
  console.log(`API Key: ${creds.apiKey.slice(0, 12)}***`);
  console.log('');

  // Step 1: Home
  try {
    const home = await httpGet(`${BASE}/api/home`, auth);
    const account = home.your_account || {};
    const karma = account.karma || 0;
    const followers = account.followerCount || 0;
    const following = account.followingCount || 0;
    const tasks = home.what_to_do_next || [];
    log.ok(`Account: ${account.name} | Karma: ${karma} | Following: ${following}`);
    results.account = { karma, followers, following };
    if (tasks.length) {
      log.info(`Tasks pending: ${tasks.length}`);
      tasks.slice(0, 2).forEach(t => log.info(`  - ${t.action}`));
    }
  } catch (e) {
    log.err(`Home API: ${e.message}`);
  }

  // Step 2: Stats
  try {
    const stats = await httpGet(`${BASE}/api/evomap/stats`, auth);
    const genes = stats.myGenes?.total || 0;
    const applied = stats.appliedGenes?.total || 0;
    const rank = stats.ranking?.rank || '-';
    const totalAgents = stats.ranking?.totalAgents || '-';
    log.ok(`Genes: ${genes} | Applied: ${applied} | Rank: ${rank}/${totalAgents}`);
    results.stats = { genes, applied, rank };
  } catch (e) {
    log.err(`Stats API: ${e.message}`);
  }

  // Step 3: Fetch Genes
  try {
    const fetch = await httpPost(
      `${BASE}/api/evomap/a2a/fetch`,
      { protocol: 'gep-a2a', message_type: 'fetch', payload: { asset_type: 'auto', signals: [], min_confidence: 0, fallback: true } },
      auth
    );
    const geneCount = fetch.genes?.length || 0;
    const capsCount = fetch.capsules?.length || 0;
    log.ok(`Fetched: ${geneCount} genes, ${capsCount} capsules`);
    if (fetch.selected) {
      log.info(`Selected: ${fetch.selected.name || fetch.selected.gene_id} (${(fetch.selected.confidence * 100).toFixed(0)}%)`);
    }
    results.fetch = { geneCount, capsCount };
  } catch (e) {
    log.err(`Fetch API: ${e.message}`);
  }

  // Step 4: Leaderboard
  try {
    const lb = await httpGet(`${BASE}/api/evomap/leaderboard?type=genes&sort=downloads&limit=3`, auth);
    const entries = lb.leaderboard || [];
    log.ok(`Leaderboard: ${entries.length} entries`);
    results.leaderboard = { entries: entries.length };
  } catch (e) {
    log.err(`Leaderboard API: ${e.message}`);
  }

  // Step 5: Node Heartbeat
  try {
    const hb = await httpPost(
      `${BASE}/api/a2a/heartbeat`,
      { nodeId: creds.agentId || 'xhs-dy', nodeSecret: creds.nodeSecret || '' },
      {}
    );
    if (hb.ok || hb.status === 'ok') {
      log.ok('Node heartbeat sent');
    } else {
      log.warn(`Heartbeat: ${JSON.stringify(hb).slice(0, 60)}`);
    }
    results.heartbeat = hb;
  } catch (e) {
    log.warn(`Heartbeat API: ${e.message} (non-critical)`);
  }

  // Step 6: Feed + Interaction
  try {
    const feed = await httpGet(`${BASE}/api/feed?sort=new&limit=5`, auth);
    const posts = feed.posts || feed.items || [];
    log.ok(`Feed: ${posts.length} posts fetched`);
    results.feed = { count: posts.length };
  } catch (e) {
    log.err(`Feed API: ${e.message}`);
  }

  // Step 7: Summary
  const elapsed = ((Date.now() - start) / 1000).toFixed(1);
  console.log(`\n\x1b[1m=== Done in ${elapsed}s ===\x1b[0m\n`);

  return results;
}

// ─── CLI ─────────────────────────────────────────────────
(async () => {
  try {
    const creds = loadCredentials();
    await runHeartbeat(creds);
    process.exit(0);
  } catch (e) {
    console.error(`\n\x1b[31m[ERROR]\x1b[0m ${e.message}\n`);
    process.exit(1);
  }
})();
