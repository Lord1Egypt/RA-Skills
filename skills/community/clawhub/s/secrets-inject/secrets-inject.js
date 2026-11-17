#!/usr/bin/env node
/**
 * secrets-inject — HIGH-PRIVILEGE companion to secrets-manager.
 *
 * ⚠️  WARNING: This skill intentionally expands a secret store into
 * executable command material. It decrypts secrets and substitutes them
 * into command strings, then either prints the resolved command (stdout)
 * or writes it to a temp shell script you are meant to run with `sh`.
 * That is a secret-exfiltration-capable capability by design. It lives in
 * its OWN skill (separate from the pure secrets-manager store) so the core
 * store can stay clean and this dangerous capability is opt-in and clearly
 * labeled.
 *
 * Modes:
 *   --inject <command>                → Substitute {{secret}} placeholders,
 *                                        write resolved command to a temp
 *                                        file (chmod 0600) and print its path.
 *   --inject-stdout <command>         → Print resolved command to stdout
 *                                        (⚠️ REQUIRES --confirm-expose).
 *   --cleanup-tmp                     → Delete tracked temp injection files.
 *   --status                          → Show store reachability.
 *
 * Required env: SECRETS_DIR (or it auto-locates the workspace memory/secrets).
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
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
const TMP_INJECTIONS_FILE = path.join(DATA_DIR, '.tmp-injections.json');

// ─── crypto (mirror of secrets-manager) ────────────────────────────────────

function getMasterKey() {
  if (process.env.SECRETS_MASTER_KEY) {
    const k = Buffer.from(process.env.SECRETS_MASTER_KEY, 'hex');
    if (k.length === 32) return k;
  }
  if (fs.existsSync(MASTER_KEY_FILE)) {
    const k = Buffer.from(fs.readFileSync(MASTER_KEY_FILE, 'utf8').trim(), 'hex');
    if (k.length === 32) return k;
  }
  console.log('[secrets-inject] ❌ No master key found. Store a secret with secrets-manager first.');
  process.exit(1);
}

function decrypt(entry) {
  try {
    const key = getMasterKey();
    const iv = Buffer.from(entry.iv, 'base64');
    const ct = Buffer.from(entry.ct, 'base64');
    const tag = Buffer.from(entry.tag, 'base64');
    const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
    decipher.setAuthTag(tag);
    const pt = Buffer.concat([decipher.update(ct), decipher.final()]);
    return pt.toString('utf8');
  } catch {
    return null;
  }
}

function writeSecure(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true, mode: 0o700 });
  const tmp = file + '.tmp.' + process.pid;
  fs.writeFileSync(tmp, data, { mode: 0o600 });
  fs.renameSync(tmp, file);
  try { fs.chmodSync(file, 0o600); } catch {}
}

function loadJSON(file, fallback) {
  try { return JSON.parse(fs.readFileSync(file, 'utf8')); }
  catch { return fallback || {}; }
}

function trackTmpInjection(tmpFile, secretNames) {
  const reg = loadJSON(TMP_INJECTIONS_FILE, { files: [] });
  reg.files.push({ path: tmpFile, secrets: secretNames, createdAt: new Date().toISOString(), pid: process.pid });
  writeSecure(TMP_INJECTIONS_FILE, JSON.stringify(reg, null, 2));
}

function cleanupTmpInjections() {
  const reg = loadJSON(TMP_INJECTIONS_FILE, { files: [] });
  let removed = 0;
  const remaining = [];
  for (const e of reg.files) {
    try {
      if (fs.existsSync(e.path)) { fs.unlinkSync(e.path); removed++; }
      else remaining.push(e);
    } catch { remaining.push(e); }
  }
  writeSecure(TMP_INJECTIONS_FILE, JSON.stringify({ files: remaining }, null, 2));
  console.log(`[secrets-inject] Removed ${removed} temp injection file(s).`);
}

function injectSecrets(command, secrets, { stdoutMode, confirmExpose }) {
  let result = command;
  let injected = 0;
  for (const [name, secret] of Object.entries(secrets)) {
    const ph = `{{${name}}}`;
    if (result.includes(ph)) {
      const v = decrypt(secret);
      if (v === null) {
        console.log(`[secrets-inject] ⚠️ Skipped ${ph}: decrypt failed`);
        continue;
      }
      result = result.replace(new RegExp(ph.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), v);
      injected++;
    }
  }
  if (stdoutMode) {
    if (!confirmExpose) {
      console.log('[secrets-inject] ❌ Refusing to print resolved command (leaks secrets to logs).');
      console.log('[secrets-inject]    Re-run with --confirm-expose to acknowledge the risk.');
      return null;
    }
    console.log(`[secrets-inject] ⚠️ The command below contains ${injected} plaintext secret value(s):`);
    console.log(result);
    return result;
  }
  const tmpFile = path.join(os.tmpdir(), `secrets-inject-${process.pid}-${Date.now()}.sh`);
  writeSecure(tmpFile, '#!/bin/sh\n' + result + '\n');
  trackTmpInjection(tmpFile, Object.keys(secrets));
  console.log(`[secrets-inject] ✅ Injected ${injected} secret(s) into: ${tmpFile}`);
  console.log(`[secrets-inject]    Run with:  sh ${tmpFile}`);
  console.log(`[secrets-inject]    File mode 0600. Clear with --cleanup-tmp.`);
  console.log(`[secrets-inject]    ⚠️ This temp file contains PLAINTEXT secrets. Delete it after use.`);
  return tmpFile;
}

// ─── CLI ───────────────────────────────────────────────────────────────────

function parseCLI() {
  const args = process.argv.slice(2);
  const r = { mode: 'status', command: '', flags: { stdout: false, confirmExpose: false } };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--inject') { r.mode = 'inject'; r.command = args.slice(i + 1).join(' '); break; }
    if (a === '--inject-stdout') { r.mode = 'inject'; r.flags.stdout = true; r.command = args.slice(i + 1).join(' '); break; }
    if (a === '--cleanup-tmp') { r.mode = 'cleanup-tmp'; break; }
    if (a === '--confirm-expose') r.flags.confirmExpose = true;
  }
  return r;
}

function main() {
  const { mode, command, flags } = parseCLI();
  if (mode === 'cleanup-tmp') return cleanupTmpInjections();
  if (mode === 'status') {
    if (!fs.existsSync(SECRETS_FILE)) {
      console.log('[secrets-inject] No secrets store found at', SECRETS_FILE);
      console.log('[secrets-inject] Store secrets with the secrets-manager skill first.');
      return;
    }
    const n = Object.keys(loadJSON(SECRETS_FILE, {})).length;
    console.log(`[secrets-inject] Store reachable: ${n} secret(s) at ${SECRETS_FILE}`);
    return;
  }
  if (mode === 'inject') {
    if (!command) {
      console.log('Usage: secrets-inject.js --inject "command with {{secret_name}} placeholders"');
      console.log('       secrets-inject.js --inject-stdout --confirm-expose "command {{secret}}"  (prints plaintext)');
      return;
    }
    const secrets = loadJSON(SECRETS_FILE, {});
    return injectSecrets(command, secrets, { stdoutMode: flags.stdout, confirmExpose: flags.confirmExpose });
  }
}

if (require.main === module) main();
module.exports = { injectSecrets, decrypt, getMasterKey };
