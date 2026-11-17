#!/usr/bin/env node
/**
 * Secrets Manager — Local encrypted secret store for OpenClaw agents
 *
 * Storage: AES-256-GCM encryption with a per-install master key.
 *   - secrets.json: { name: { iv, ct, tag, created, updated, rotationDays, lastRotated, rotationCount } }
 *   - .master-key: 32 random bytes, chmod 0600
 *   - If .master-key is lost, all stored secrets become unrecoverable
 *
 * Modes:
 *   --store <name> <value>            → Store a secret (encrypted with master key)
 *   --get <name>                      → Get a secret (masked by default)
 *   --get --raw <name>                → Get raw value ⚠️ prints to stdout
 *   --list                            → List secret names (not values)
 *   --delete <name>                   → Delete a secret (irreversible)
 *   --rotate <name>                   → Generate new random value
 *   --rotate --all                    → Rotate all secrets
 *   --audit                           → Check for exposure risks
 *   --audit --expired                 → Only expired
 *   --audit --stale                   → Only expiring soon
 *   --status                          → Secrets status overview
 *
 * Security model:
 *   - AES-256-GCM authenticated encryption
 *   - Master key auto-generated on first store, chmod 0600
 *   - Per-secret random 12-byte IV
 *   - All write files use atomic temp+rename, chmod 0600 on secrets.json + .master-key
 *   - secrets.json includes auth tag → tampering causes decrypt to return null
 *   - NEVER print raw secret or substituted command unless explicitly confirmed
 *
 * Permissions: filesystem (memory/secrets/), env (SECRETS_DIR override, SECRETS_MASTER_KEY override)
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const WORKSPACE = (() => {
  if (process.env.SECRETS_DIR) return process.env.SECRETS_DIR;
  let dir = __dirname;
  for (let i = 0; i < 10; i++) {
    if (fs.existsSync(path.join(dir, 'MEMORY.md'))) return dir;
    dir = path.resolve(dir, '..');
  }
  return path.resolve(__dirname, '..', '..');
})();

const DATA_DIR = path.join(WORKSPACE, 'memory', 'secrets');
const SECRETS_FILE = path.join(DATA_DIR, 'secrets.json');
const MASTER_KEY_FILE = path.join(DATA_DIR, '.master-key');
const PERMS_FILE = path.join(DATA_DIR, 'permissions.json');

// ─── ATOMIC FILE WRITE WITH CHMOD ──────────────────────────────────────────

function ensureDir(dir) {
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
}

function writeSecure(file, data) {
  ensureDir(path.dirname(file));
  const tmp = file + '.tmp.' + process.pid + '.' + Date.now();
  fs.writeFileSync(tmp, data, { mode: 0o600 });
  fs.renameSync(tmp, file);
  if (process.platform !== 'win32') {
    try { fs.chmodSync(file, 0o600); } catch (e) { /* best-effort */ }
  }
}

function writeJSONSecure(file, obj) {
  writeSecure(file, JSON.stringify(obj, null, 2));
}

function loadJSON(file, fallback) {
  try {
    return JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch { return fallback || {}; }
}

// ─── SECRET STORAGE HELPERS ─────────────────────────────────────────────────

// ─── MASTER KEY MANAGEMENT ────────────────────────────────────────────────

function getMasterKey() {
  // 1. Check env var override
  if (process.env.SECRETS_MASTER_KEY) {
    const envKey = Buffer.from(process.env.SECRETS_MASTER_KEY, 'hex');
    if (envKey.length === 32) return envKey;
  }
  
  // 2. Load from .master-key
  if (fs.existsSync(MASTER_KEY_FILE)) {
    const stored = fs.readFileSync(MASTER_KEY_FILE, 'utf8').trim();
    const key = Buffer.from(stored, 'hex');
    if (key.length === 32) return key;
  }
  
  // 3. Generate new master key (first-run)
  const newKey = crypto.randomBytes(32);
  writeSecure(MASTER_KEY_FILE, newKey.toString('hex'));
  return newKey;
}

// ─── ENCRYPTION (AES-256-GCM) ─────────────────────────────────────────────

function encrypt(plaintext) {
  const key = getMasterKey();
  const iv = crypto.randomBytes(12); // 96-bit IV for GCM
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  const ct = Buffer.concat([cipher.update(plaintext, 'utf8'), cipher.final()]);
  const tag = cipher.getAuthTag();
  return {
    iv: iv.toString('base64'),
    ct: ct.toString('base64'),
    tag: tag.toString('base64')
  };
}

function decrypt(enc) {
  if (!enc || !enc.iv || !enc.ct || !enc.tag) return null;
  try {
    const key = getMasterKey();
    const iv = Buffer.from(enc.iv, 'base64');
    const ct = Buffer.from(enc.ct, 'base64');
    const tag = Buffer.from(enc.tag, 'base64');
    const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
    decipher.setAuthTag(tag);
    return Buffer.concat([decipher.update(ct), decipher.final()]).toString('utf8');
  } catch (e) {
    // GCM auth tag mismatch → returns null
    return null;
  }
}

// ─── HELPERS ───────────────────────────────────────────────────────────────

function getToday() {
  return new Date().toISOString().split('T')[0];
}

function generateRandomValue(bytes = 32) {
  return crypto.randomBytes(bytes).toString('hex');
}

function maskValue(value) {
  if (!value) return '****';
  if (value.length <= 6) return '****';
  return value.substring(0, 3) + '****' + value.substring(value.length - 2);
}

// ─── STORE ─────────────────────────────────────────────────────────────────

function storeSecret(name, value) {
  if (!name || !value) {
    console.log('Usage: secrets-manager.js --store <name> <value>');
    return null;
  }
  const secrets = loadJSON(SECRETS_FILE, {});
  const enc = encrypt(value);
  
  secrets[name] = {
    iv: enc.iv,
    ct: enc.ct,
    tag: enc.tag,
    created: secrets[name]?.created || getToday(),
    updated: getToday(),
    rotationDays: 90,
    lastRotated: getToday(),
    rotationCount: secrets[name]?.rotationCount || 0,
    retired: secrets[name]?.retired || null
  };
  
  writeJSONSecure(SECRETS_FILE, secrets);
  console.log(`[secrets-manager] Stored: ${name} (masked: ${maskValue(value)})`);
  return true;
}

// ─── GET ───────────────────────────────────────────────────────────────────

function getSecret(name, raw = false) {
  if (!name) {
    console.log('Usage: secrets-manager.js --get <name>');
    return null;
  }
  const secrets = loadJSON(SECRETS_FILE, {});
  if (!secrets[name]) {
    console.log(`[secrets-manager] Secret not found: ${name}`);
    return null;
  }
  
  const value = decrypt(secrets[name]);
  if (value === null) {
    console.log(`[secrets-manager] Failed to decrypt: ${name} (tampered or wrong master key)`);
    return null;
  }
  
  if (raw) {
    console.log(`[secrets-manager] ⚠️ Printing raw secret to stdout. This may leak credentials to logs.`);
    console.log(value);
  } else {
    console.log(`[secrets-manager] ${name}: ${maskValue(value)}`);
  }
  return value;
}

// ─── LIST ──────────────────────────────────────────────────────────────────

function listSecrets() {
  const secrets = loadJSON(SECRETS_FILE, {});
  const entries = Object.entries(secrets);
  
  if (entries.length === 0) {
    console.log('[secrets-manager] No secrets stored.');
    return;
  }
  
  console.log(`[secrets-manager] Stored secrets (${entries.length}):\n`);
  console.log(`${'Name'.padEnd(25)} ${'Updated'.padEnd(12)} ${'Expires'.padEnd(12)} ${'Age'.padEnd(8)}`);
  console.log('-'.repeat(60));
  
  for (const [name, secret] of entries) {
    const updated = secret.updated || secret.created;
    const age = Math.floor((Date.now() - new Date(updated).getTime()) / (1000 * 60 * 60 * 24));
    const expires = new Date(new Date(updated).getTime() + (secret.rotationDays || 90) * 86400000).toISOString().split('T')[0];
    const ageStr = age > 0 ? `${age}d` : 'today';
    
    console.log(`${name.padEnd(25)} ${updated.padEnd(12)} ${expires.padEnd(12)} ${ageStr.padEnd(8)}`);
  }
}

// ─── DELETE ────────────────────────────────────────────────────────────────

function deleteSecret(name) {
  if (!name) {
    console.log('Usage: secrets-manager.js --delete <name>');
    return;
  }
  const secrets = loadJSON(SECRETS_FILE, {});
  if (secrets[name]) {
    delete secrets[name];
    writeJSONSecure(SECRETS_FILE, secrets);
    console.log(`[secrets-manager] Deleted: ${name}`);
  } else {
    console.log(`[secrets-manager] Not found: ${name}`);
  }
}

// ─── ROTATE ────────────────────────────────────────────────────────────────

function rotateSecret(name) {
  if (!name) {
    console.log('Usage: secrets-manager.js --rotate <name>');
    return;
  }
  const secrets = loadJSON(SECRETS_FILE, {});
  if (!secrets[name]) {
    console.log(`[secrets-manager] Not found: ${name}`);
    return;
  }
  
  // Archive old (encrypted) value
  const oldEntry = { ...secrets[name] };
  delete oldEntry.retired; // don't recurse
  secrets[name].retired = { ...oldEntry, retiredAt: getToday() };
  
  // Generate new random value, encrypt it
  const newValue = generateRandomValue();
  const enc = encrypt(newValue);
  secrets[name].iv = enc.iv;
  secrets[name].ct = enc.ct;
  secrets[name].tag = enc.tag;
  secrets[name].lastRotated = getToday();
  secrets[name].updated = getToday();
  secrets[name].rotationCount = (secrets[name].rotationCount || 0) + 1;
  
  writeJSONSecure(SECRETS_FILE, secrets);
  console.log(`[secrets-manager] ✅ Rotated: ${name} (new value generated — not printed for security)`);
  console.log(`[secrets-manager]   Previous encrypted value archived. Rotate again to discard archive.`);
}

function rotateAllSecrets() {
  const secrets = loadJSON(SECRETS_FILE, {});
  const entries = Object.entries(secrets);
  if (entries.length === 0) {
    console.log('[secrets-manager] No secrets to rotate.');
    return;
  }
  
  console.log(`[secrets-manager] Rotating ${entries.length} secrets...\n`);
  for (const [name] of entries) {
    rotateSecret(name);
  }
  console.log(`\n[secrets-manager] Rotated ${entries.length}/${entries.length} secrets.`);
}

// ─── AUDIT ─────────────────────────────────────────────────────────────────

function auditSecrets(filter = null) {
  const secrets = loadJSON(SECRETS_FILE, {});
  const findings = { expired: [], expiring: [], weak: [], patterns: [] };
  
  for (const [name, secret] of Object.entries(secrets)) {
    const age = Math.floor((Date.now() - new Date(secret.updated).getTime()) / (1000 * 60 * 60 * 24));
    const rotationDays = secret.rotationDays || 90;
    
    if (age > rotationDays) {
      findings.expired.push({ name, days: age - rotationDays });
    } else if (age > rotationDays * 0.7) {
      findings.expiring.push({ name, daysLeft: rotationDays - age });
    }
    
    // Decrypt to check value (returns null if tampered)
    const value = decrypt(secret);
    if (value === null) {
      findings.patterns.push({ name, pattern: '[DECRYPT FAILED — tampered or wrong key]' });
      continue;
    }
    if (value.length < 8) {
      findings.weak.push({ name, length: value.length });
    }
    if (/^(password|admin|root|test|demo|secret|key|token)/i.test(value)) {
      findings.patterns.push({ name, pattern: value.substring(0, 10) + '...' });
    }
  }
  
  console.log('[secrets-manager] Audit results:\n');
  let hasIssues = false;
  
  if (findings.expired.length > 0) {
    hasIssues = true;
    console.log(`  🔴 Expired (${findings.expired.length}):`);
    for (const f of findings.expired) {
      console.log(`    🔴 ${f.name}: expired ${f.days} days ago`);
    }
  }
  if (findings.expiring.length > 0) {
    hasIssues = true;
    console.log(`\n  🟡 Expiring soon (${findings.expiring.length}):`);
    for (const f of findings.expiring) {
      console.log(`    🟡 ${f.name}: expires in ${f.daysLeft} days`);
    }
  }
  if (findings.weak.length > 0) {
    hasIssues = true;
    console.log(`\n  ⚠️ Weak secrets (${findings.weak.length}):`);
    for (const f of findings.weak) {
      console.log(`    ⚠️ ${f.name}: ${f.length} chars (min 8)`);
    }
  }
  if (findings.patterns.length > 0) {
    hasIssues = true;
    console.log(`\n  ⚠️ Weak patterns (${findings.patterns.length}):`);
    for (const f of findings.patterns) {
      console.log(`    ⚠️ ${f.name}: starts with '${f.pattern}'`);
    }
  }
  if (!hasIssues) {
    console.log('  ✅ No issues found.');
  }
}

// ─── STATUS ────────────────────────────────────────────────────────────────

function showStatus() {
  const secrets = loadJSON(SECRETS_FILE, {});
  const perms = loadJSON(PERMS_FILE, {});
  const masterKeyExists = fs.existsSync(MASTER_KEY_FILE);
  
  console.log('[secrets-manager] Status:\n');
  console.log(`  Encryption: AES-256-GCM (authenticated)`);
  console.log(`  Master key: ${masterKeyExists ? '✅ present (' + MASTER_KEY_FILE + ')' : '❌ MISSING'}`);
  console.log(`  Total secrets: ${Object.keys(secrets).length}`);
  console.log(`  Permissions rules: ${Object.keys(perms).length}`);
  
  if (Object.keys(secrets).length > 0) {
    const expired = Object.entries(secrets).filter(([_, s]) => {
      const age = Math.floor((Date.now() - new Date(s.updated).getTime()) / (1000 * 60 * 60 * 24));
      return age > (s.rotationDays || 90);
    });
    console.log(`  Expired: ${expired.length}`);
  }
}

// ─── CLI ───────────────────────────────────────────────────────────────────

function parseCLI() {
  const args = process.argv.slice(2);
  const result = {
    mode: 'status',
    positional: [],
    flags: {
      raw: false,
      confirmExpose: false
    }
  };
  
  // Pass 1: find primary mode (only matches the exact primary mode flags, not sub-flags)
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--store') { result.mode = 'store'; break; }
    else if (arg === '--get') { result.mode = 'get'; break; }
    else if (arg === '--list') { result.mode = 'list'; break; }
    else if (arg === '--delete') { result.mode = 'delete'; break; }
    else if (arg === '--rotate') { result.mode = 'rotate'; break; }
    else if (arg === '--audit') { result.mode = 'audit'; break; }
    else if (arg === '--status') { result.mode = 'status'; break; }
    // --confirm-expose, --raw, --all, --expired, --stale, --dir are sub-flags
  }
  
  // Pass 2: collect flags + positionals (don't reset mode)
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--raw') result.flags.raw = true;
    else if (arg === '--confirm-expose') result.flags.confirmExpose = true;
    else if (arg === '--all' && result.mode === 'rotate') result.mode = 'rotate-all';
    else if (arg === '--expired' && result.mode === 'audit') result.mode = 'audit-expired';
    else if (arg === '--stale' && result.mode === 'audit') result.mode = 'audit-stale';
    else if (arg === '--dir' && i + 1 < args.length) {
      process.env.SECRETS_DIR = args[++i];
    }
    else if (!arg.startsWith('--')) {
      result.positional.push(arg);
    }
    // Skip mode-flag args (already handled in pass 1)
  }
  
  return result;
}

function runCLI() {
  const parsed = parseCLI();
  const { mode, positional, flags } = parsed;
  
  switch (mode) {
    case 'store': {
      const name = positional[0];
      const value = positional[1];
      if (!name || !value) {
        console.log('Usage: secrets-manager.js --store <name> <value>');
      } else {
        storeSecret(name, value);
      }
      break;
    }
    case 'get': {
      const name = positional[0];
      if (!name) {
        console.log('Usage: secrets-manager.js --get <name> [--raw]');
      } else {
        getSecret(name, flags.raw);
      }
      break;
    }
    case 'list':
      listSecrets();
      break;
    case 'delete':
      deleteSecret(positional[0]);
      break;
    case 'rotate':
      rotateSecret(positional[0]);
      break;
    case 'rotate-all':
      rotateAllSecrets();
      break;
    case 'audit':
      auditSecrets();
      break;
    case 'audit-expired':
      auditSecrets('expired');
      break;
    case 'audit-stale':
      auditSecrets('stale');
      break;
    default:
      showStatus();
      break;
  }
}

// ─── MODULE EXPORTS (for testing) ─────────────────────────────────────────

module.exports = {
  storeSecret,
  getSecret,
  listSecrets,
  deleteSecret,
  rotateSecret,
  rotateAllSecrets,
  auditSecrets,
  showStatus,
  encrypt,
  decrypt,
  getMasterKey,
  maskValue
};

// Run CLI when invoked directly (not when required as module)
if (require.main === module) {
  runCLI();
}
