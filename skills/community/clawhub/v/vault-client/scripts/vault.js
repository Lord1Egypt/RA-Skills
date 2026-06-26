#!/usr/bin/env node
/**
 * vault-client — Hashicorp Vault CLI for OpenClaw agents
 *
 * Usage:
 *   vault.js check                        # connectivity + token expiry
 *   vault.js get <path> [key]             # read secret (or single key)
 *   vault.js put <path> key=value ...     # write secret
 *   vault.js list <path>                  # list keys at path
 *   vault.js token-info                   # show token details + expiry
 *   vault.js token-renew                  # renew token
 *   vault.js setup                        # interactive setup wizard
 *
 * Config: ~/.openclaw/vault.json
 */

const https = require('https');
const http  = require('http');
const fs    = require('fs');
const path  = require('path');
const os    = require('os');
const readline = require('readline');

const CONFIG_PATH = path.join(os.homedir(), '.openclaw', 'vault.json');
const CACHE_PATH  = path.join(os.homedir(), '.openclaw', 'vault-cache.json');

// ── Config ────────────────────────────────────────────────────────────────────
function loadConfig() {
  if (!fs.existsSync(CONFIG_PATH)) {
    console.error(`\n⚠️  vault-client not configured — run: node vault.js setup\n`);
    process.exit(2);
  }
  return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
}

function saveConfig(cfg) {
  fs.mkdirSync(path.dirname(CONFIG_PATH), { recursive: true });
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(cfg, null, 2));
}

// ── HTTP ──────────────────────────────────────────────────────────────────────
function vaultRequest(cfg, method, urlPath, body = null) {
  return new Promise((resolve, reject) => {
    const url    = new URL(urlPath, cfg.address);
    const isHttps = url.protocol === 'https:';
    const lib    = isHttps ? https : http;
    const token  = cfg.auth?.token || '';

    const options = {
      hostname: url.hostname,
      port:     url.port || (isHttps ? 443 : 80),
      path:     url.pathname + url.search,
      method,
      headers: {
        'X-Vault-Token': token,
        'Content-Type':  'application/json',
      },
      timeout: 8000,
      // allow self-signed certs on internal Vault
      rejectUnauthorized: cfg.tls?.verify !== false,
    };

    if (body) {
      const data = JSON.stringify(body);
      options.headers['Content-Length'] = Buffer.byteLength(data);
    }

    const req = lib.request(options, (res) => {
      let raw = '';
      res.on('data', chunk => raw += chunk);
      res.on('end', () => {
        try { resolve({ status: res.statusCode, body: JSON.parse(raw) }); }
        catch { resolve({ status: res.statusCode, body: raw }); }
      });
    });

    req.on('timeout', () => { req.destroy(); reject(new Error('Request timed out (8s)')); });
    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

// ── Secret cache (session-level) ──────────────────────────────────────────────
function loadCache() {
  try { return JSON.parse(fs.readFileSync(CACHE_PATH, 'utf8')); }
  catch { return {}; }
}

function saveCache(cache) {
  fs.writeFileSync(CACHE_PATH, JSON.stringify(cache, null, 2));
}

function cacheKey(mount, secretPath) {
  return `${mount}:${secretPath}`;
}

// ── Commands ──────────────────────────────────────────────────────────────────
async function cmdCheck(cfg) {
  try {
    const res = await vaultRequest(cfg, 'GET', '/v1/auth/token/lookup-self');
    if (res.status === 403 || res.status === 401) {
      console.error(`\n⚠️  vault-client: token invalid or expired`);
      console.error(`   Address: ${cfg.address}`);
      console.error(`   Run: node vault.js token-renew  (or re-run setup with a new token)`);
      process.exit(2);
    }
    if (res.status !== 200) {
      console.error(`\n⚠️  vault-client: unexpected status ${res.status} from ${cfg.address}`);
      process.exit(2);
    }
    const d = res.body.data;
    const ttl = d.ttl;
    const exp = ttl > 0 ? `expires in ${Math.floor(ttl / 3600)}h ${Math.floor((ttl % 3600) / 60)}m` : 'does not expire';
    const warn = ttl > 0 && ttl < 3600;
    console.log(`✓ Vault OK — ${cfg.address}`);
    console.log(`  Token: ${d.display_name || d.accessor}  (${exp})${warn ? '  ⚠️ renew soon!' : ''}`);
    if (warn) process.exit(1);
    process.exit(0);
  } catch (e) {
    console.error(`\n⚠️  vault-client UNREACHABLE — ${cfg.address}`);
    console.error(`   Error: ${e.message}`);
    console.error(`   Check: is Vault running? Is the address correct in ~/.openclaw/vault.json?`);
    process.exit(2);
  }
}

async function cmdGet(cfg, secretPath, key = null) {
  const mount = cfg.mount || 'secret';
  // Strip mount prefix if user included it (e.g. "shopwalk/r2" when mount="shopwalk")
  const stripped = secretPath.startsWith(mount + '/') ? secretPath.slice(mount.length + 1) : secretPath;
  secretPath = stripped;
  const ck    = cacheKey(mount, secretPath);
  const cache = loadCache();

  if (cache[ck] && cache[ck].expires > Date.now()) {
    const data = cache[ck].data;
    if (key) { printValue(data[key], key); return; }
    printSecrets(data, secretPath);
    return;
  }

  try {
    const res = await vaultRequest(cfg, 'GET', `/v1/${mount}/data/${secretPath}`);
    if (res.status === 404) {
      console.error(`✗ Not found: ${mount}/data/${secretPath}`);
      process.exit(1);
    }
    if (res.status !== 200) {
      console.error(`✗ Vault error ${res.status}: ${JSON.stringify(res.body)}`);
      process.exit(1);
    }
    const data = res.body.data?.data || res.body.data || {};
    const ttlMs = (cfg.cache_ttl_seconds || 300) * 1000;
    cache[ck] = { data, expires: Date.now() + ttlMs };
    saveCache(cache);

    if (key) { printValue(data[key], key); return; }
    printSecrets(data, secretPath);
  } catch (e) {
    console.error(`✗ vault get failed: ${e.message}`);
    process.exit(1);
  }
}

async function cmdPut(cfg, secretPath, pairs) {
  const mount = cfg.mount || 'secret';
  if (secretPath.startsWith(mount + '/')) secretPath = secretPath.slice(mount.length + 1);
  const data  = {};
  for (const p of pairs) {
    const idx = p.indexOf('=');
    if (idx < 0) { console.error(`✗ Invalid key=value: ${p}`); process.exit(1); }
    data[p.slice(0, idx)] = p.slice(idx + 1);
  }

  try {
    // KV v2: merge with existing
    const existing = await vaultRequest(cfg, 'GET', `/v1/${mount}/data/${secretPath}`);
    const prev = existing.status === 200 ? (existing.body.data?.data || {}) : {};
    const merged = { ...prev, ...data };

    const res = await vaultRequest(cfg, 'POST', `/v1/${mount}/data/${secretPath}`, { data: merged });
    if (res.status !== 200 && res.status !== 204) {
      console.error(`✗ Vault error ${res.status}: ${JSON.stringify(res.body)}`);
      process.exit(1);
    }
    // Invalidate cache
    const cache = loadCache();
    delete cache[cacheKey(mount, secretPath)];
    saveCache(cache);
    console.log(`✓ Written: ${mount}/${secretPath}  (${Object.keys(data).join(', ')})`);
  } catch (e) {
    console.error(`✗ vault put failed: ${e.message}`);
    process.exit(1);
  }
}

async function cmdList(cfg, listPath) {
  const mount = cfg.mount || 'secret';
  if (listPath.startsWith(mount + '/')) listPath = listPath.slice(mount.length + 1);
  if (listPath === mount) listPath = '';
  try {
    const res = await vaultRequest(cfg, 'LIST', `/v1/${mount}/metadata/${listPath}`);
    if (res.status === 404) { console.log(`(empty)`); return; }
    if (res.status !== 200) {
      console.error(`✗ Vault error ${res.status}: ${JSON.stringify(res.body)}`);
      process.exit(1);
    }
    const keys = res.body.data?.keys || [];
    console.log(`Keys at ${mount}/${listPath}:`);
    for (const k of keys) console.log(`  ${k}`);
  } catch (e) {
    console.error(`✗ vault list failed: ${e.message}`);
    process.exit(1);
  }
}

async function cmdTokenInfo(cfg) {
  try {
    const res = await vaultRequest(cfg, 'GET', '/v1/auth/token/lookup-self');
    if (res.status !== 200) { console.error(`✗ ${res.status}: ${JSON.stringify(res.body)}`); process.exit(1); }
    const d = res.body.data;
    console.log(`Token info:`);
    console.log(`  Display name : ${d.display_name || '(none)'}`);
    console.log(`  Policies     : ${(d.policies || []).join(', ')}`);
    console.log(`  Renewable    : ${d.renewable}`);
    console.log(`  TTL          : ${d.ttl > 0 ? `${Math.floor(d.ttl/3600)}h ${Math.floor((d.ttl%3600)/60)}m` : 'never expires'}`);
    console.log(`  Accessor     : ${d.accessor}`);
  } catch (e) {
    console.error(`✗ token-info failed: ${e.message}`); process.exit(1);
  }
}

async function cmdTokenRenew(cfg) {
  try {
    const res = await vaultRequest(cfg, 'POST', '/v1/auth/token/renew-self');
    if (res.status !== 200) { console.error(`✗ Renew failed: ${JSON.stringify(res.body)}`); process.exit(1); }
    const ttl = res.body.auth?.lease_duration;
    console.log(`✓ Token renewed — new TTL: ${Math.floor(ttl/3600)}h ${Math.floor((ttl%3600)/60)}m`);
  } catch (e) {
    console.error(`✗ token-renew failed: ${e.message}`); process.exit(1);
  }
}

// ── Setup wizard ──────────────────────────────────────────────────────────────
async function cmdSetup() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const ask = (q) => new Promise(resolve => rl.question(q, resolve));

  console.log('\n╔══════════════════════════════╗');
  console.log('║  vault-client setup          ║');
  console.log('╚══════════════════════════════╝\n');

  const existing = fs.existsSync(CONFIG_PATH) ? JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8')) : {};

  const address  = await ask(`Vault address [${existing.address || 'https://vault.example.com:8200'}]: `);
  const mount    = await ask(`Secret mount  [${existing.mount   || 'secret'}]: `);
  const token    = await ask(`Vault token   [${existing.auth?.token ? '(existing)' : 'hvs.xxx'}]: `);
  const cacheTtl = await ask(`Cache TTL seconds [${existing.cache_ttl_seconds || 300}]: `);

  const cfg = {
    address:           address.trim()  || existing.address  || 'https://vault.example.com:8200',
    mount:             mount.trim()    || existing.mount    || 'secret',
    auth:              { method: 'token', token: token.trim() || existing.auth?.token || '' },
    cache_ttl_seconds: parseInt(cacheTtl.trim() || String(existing.cache_ttl_seconds || 300)),
    tls:               { verify: true },
  };
  rl.close();

  saveConfig(cfg);
  console.log(`\n✓ Config saved to ${CONFIG_PATH}`);

  // Test connectivity
  process.stdout.write('  Testing connection... ');
  try {
    const res = await vaultRequest(cfg, 'GET', '/v1/auth/token/lookup-self');
    if (res.status === 200) {
      const d = res.body.data;
      console.log(`✓ OK — token: ${d.display_name || d.accessor}`);
    } else {
      console.log(`⚠️  Status ${res.status} — check token`);
    }
  } catch (e) {
    console.log(`⚠️  Unreachable — ${e.message}`);
  }

  // Scaffold AGENTS.md
  const skillDir   = path.resolve(__dirname, '..');
  const agentsMd   = path.join(os.homedir(), '.openclaw', 'workspace', 'AGENTS.md');
  const vaultBlock = `
<!-- vault-client:section -->
## vault-client — Hashicorp Vault

**Config:** \`${CONFIG_PATH}\`

### Startup (MANDATORY)
\`\`\`bash
node ${skillDir}/scripts/vault.js check
\`\`\`
If exit 2: warn the user and fall back to manual token curl commands.

### Reading secrets
\`\`\`bash
node ${skillDir}/scripts/vault.js get shopwalk/r2             # all keys
node ${skillDir}/scripts/vault.js get shopwalk/r2 secret_access_key  # single key
\`\`\`

### Writing secrets
\`\`\`bash
node ${skillDir}/scripts/vault.js put shopwalk/r2 secret_access_key=newvalue
\`\`\`

### Other commands
\`\`\`bash
node ${skillDir}/scripts/vault.js list shopwalk/
node ${skillDir}/scripts/vault.js token-info
node ${skillDir}/scripts/vault.js token-renew
\`\`\`
`;

  if (fs.existsSync(agentsMd)) {
    const content = fs.readFileSync(agentsMd, 'utf8');
    if (!content.includes('<!-- vault-client:section -->')) {
      fs.appendFileSync(agentsMd, vaultBlock);
      console.log(`  ✓ vault-client section added to AGENTS.md`);
    } else {
      console.log(`  ✓ AGENTS.md already has vault-client section`);
    }
  }

  console.log(`\nvault-client is ready!`);
  console.log(`  Check:  node ${path.join(__dirname, 'vault.js')} check`);
  console.log(`  Get:    node ${path.join(__dirname, 'vault.js')} get <path>`);
}

// ── Output helpers ────────────────────────────────────────────────────────────
function printSecrets(data, secretPath) {
  console.log(`Secret: ${secretPath}`);
  for (const [k, v] of Object.entries(data)) {
    console.log(`  ${k}: ${v}`);
  }
}

function printValue(val, key) {
  if (val === undefined) { console.error(`✗ Key not found: ${key}`); process.exit(1); }
  console.log(val);
}

// ── Main ──────────────────────────────────────────────────────────────────────
async function main() {
  const [,, cmd, ...rest] = process.argv;

  if (!cmd || cmd === 'help' || cmd === '--help') {
    console.log(`vault-client — Hashicorp Vault for OpenClaw agents

Commands:
  check                  Connectivity + token expiry check (exit 0=ok, 1=warn, 2=down)
  get <path> [key]       Read secret (all keys, or single key)
  put <path> key=value   Write/merge secret
  list <path>            List keys at path
  token-info             Show token details
  token-renew            Renew token TTL
  setup                  Interactive setup wizard

Config: ~/.openclaw/vault.json`);
    process.exit(0);
  }

  if (cmd === 'setup') { await cmdSetup(); return; }

  const cfg = loadConfig();

  switch (cmd) {
    case 'check':       return cmdCheck(cfg);
    case 'get':         return cmdGet(cfg, rest[0], rest[1] || null);
    case 'put':         return cmdPut(cfg, rest[0], rest.slice(1));
    case 'list':        return cmdList(cfg, rest[0] || '');
    case 'token-info':  return cmdTokenInfo(cfg);
    case 'token-renew': return cmdTokenRenew(cfg);
    default:
      console.error(`✗ Unknown command: ${cmd}  (run vault.js help)`);
      process.exit(1);
  }
}

main().catch(e => { console.error(`✗ ${e.message}`); process.exit(1); });
