#!/usr/bin/env node
/**
 * Zhipu GLM-Image helper
 * - check saved session
 * - auto-open browser login when needed
 * - generate images via image.z.ai
 */

let CDP;
try {
  CDP = require('chrome-remote-interface');
} catch {
  throw new Error('Missing dependency: chrome-remote-interface. Run npm install in scripts/ before using this skill.');
}
const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');
const { URL } = require('url');
const { exec } = require('child_process');

const API_BASE = 'https://image.z.ai/api/proxy';
const LOGIN_URL = 'https://image.z.ai/';
const SESSION_FILE = path.join(process.env.USERPROFILE, '.zhipu_image_session.json');
const DEFAULT_OUTPUT = path.join(process.cwd(), 'captures');

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function parseArgs(argv) {
  const args = { cmd: argv[0], prompt: '', output: DEFAULT_OUTPUT, timeoutMs: 120000, autoOpen: true, waitLogin: true };
  const rest = [];
  for (let i = 1; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--output') args.output = argv[++i] || DEFAULT_OUTPUT;
    else if (arg === '--timeout-ms') args.timeoutMs = Number(argv[++i]) || 120000;
    else if (arg === '--no-open-browser') args.autoOpen = false;
    else if (arg === '--no-wait-login') args.waitLogin = false;
    else rest.push(arg);
  }
  args.prompt = rest.join(' ').trim();
  return args;
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function loadSession() {
  try {
    if (fs.existsSync(SESSION_FILE)) return JSON.parse(fs.readFileSync(SESSION_FILE, 'utf8'));
  } catch {}
  return null;
}

function saveSession(session) {
  fs.writeFileSync(SESSION_FILE, JSON.stringify(session, null, 2));
}

function buildCookieString(cookies) {
  return (cookies || []).map(c => `${c.name}=${c.value}`).join('; ');
}

function buildHeaders(cookies) {
  return {
    'Content-Type': 'application/json',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
    'Cookie': buildCookieString(cookies),
    'Origin': 'https://image.z.ai',
    'Referer': 'https://image.z.ai/',
  };
}

function request(method, url, cookies, body = null) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const client = parsed.protocol === 'https:' ? https : http;
    const options = {
      hostname: parsed.hostname,
      port: parsed.port || (parsed.protocol === 'https:' ? 443 : 80),
      path: parsed.pathname + parsed.search,
      method,
      headers: buildHeaders(cookies),
    };
    const req = client.request(options, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve({ status: res.statusCode, data, headers: res.headers }));
    });
    req.on('error', reject);
    req.setTimeout(30000, () => req.destroy(new Error('Request timeout')));
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

async function captureCookies() {
  const client = await CDP({ port: 18800 });
  const { Network } = client;
  await Network.enable();
  const cookies = await Network.getCookies();
  await client.close();

  const picked = cookies.cookies.filter(c =>
    c.domain.includes('z.ai') || c.domain.includes('bigmodel.cn') || c.domain.includes('chatglm')
  );
  if (!picked.length) throw new Error('No Zhipu cookies found. Please log in at image.z.ai first.');

  const session = { cookies: picked.map(c => ({ name: c.name, value: c.value })), savedAt: new Date().toISOString() };
  saveSession(session);
  return session;
}

function openLoginPage() {
  return new Promise((resolve, reject) => {
    exec(`start "" "${LOGIN_URL}"`, { shell: 'cmd.exe' }, error => {
      if (error) return reject(error);
      resolve({ ok: true, url: LOGIN_URL });
    });
  });
}

async function checkSession() {
  const session = loadSession();
  if (!session?.cookies?.length) return { ok: false, reason: 'missing-session-file', sessionFile: SESSION_FILE };
  try {
    const resp = await request('POST', `${API_BASE}/images/generate`, session.cookies, {
      prompt: 'test', ratio: '1:1', resolution: '512x512', rm_label_watermark: true,
    });
    if (resp.status === 200) {
      return { ok: true, reason: 'session-valid', sessionFile: SESSION_FILE, cookieCount: session.cookies.length, savedAt: session.savedAt || null };
    }
    return { ok: false, reason: 'probe-failed', sessionFile: SESSION_FILE, status: resp.status, bodyPreview: String(resp.data).slice(0, 300) };
  } catch (error) {
    return { ok: false, reason: 'check-error', sessionFile: SESSION_FILE, error: error.message };
  }
}

async function waitForLogin(timeoutMs = 120000) {
  const started = Date.now();
  let lastError = null;
  while (Date.now() - started < timeoutMs) {
    try {
      const session = await captureCookies();
      return { ok: true, waitedMs: Date.now() - started, cookieCount: session.cookies.length };
    } catch (error) {
      lastError = error;
      await sleep(5000);
    }
  }
  return { ok: false, reason: 'login-timeout', waitedMs: Date.now() - started, error: lastError?.message || 'Timed out waiting for login' };
}

async function ensureSession(opts = {}) {
  const checked = await checkSession();
  if (checked.ok) return { ...checked, refreshed: false, openedBrowser: false };
  try {
    const session = await captureCookies();
    return { ok: true, reason: 'session-refreshed', refreshed: true, openedBrowser: false, cookieCount: session.cookies.length, sessionFile: SESSION_FILE };
  } catch (error) {
    if (opts.autoOpen === false) throw error;
    await openLoginPage();
    if (opts.waitLogin === false) {
      return { ok: false, reason: 'login-required-browser-opened', openedBrowser: true, loginUrl: LOGIN_URL, sessionFile: SESSION_FILE };
    }
    const waited = await waitForLogin(opts.timeoutMs || 120000);
    if (!waited.ok) return { ok: false, ...waited, openedBrowser: true, loginUrl: LOGIN_URL, sessionFile: SESSION_FILE };
    const rechecked = await checkSession();
    return { ...rechecked, refreshed: true, openedBrowser: true, loginUrl: LOGIN_URL, waitedMs: waited.waitedMs };
  }
}

async function downloadImage(url, outputDir, nameBase) {
  ensureDir(outputDir);
  const filePath = path.join(outputDir, `${nameBase}.png`);
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https:') ? https : http;
    client.get(url, res => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        res.resume();
        return resolve(downloadImage(res.headers.location, outputDir, nameBase));
      }
      if (res.statusCode !== 200) {
        res.resume();
        return reject(new Error(`HTTP ${res.statusCode}`));
      }
      const file = fs.createWriteStream(filePath);
      res.pipe(file);
      file.on('finish', () => file.close(() => resolve(filePath)));
      file.on('error', reject);
    }).on('error', reject);
  });
}

async function generate(prompt, outputDir) {
  const ensured = await ensureSession({ autoOpen: true, waitLogin: true, timeoutMs: 120000 });
  if (!ensured.ok) throw new Error(`Session unavailable: ${ensured.reason}`);
  const session = loadSession();
  const resp = await request('POST', `${API_BASE}/images/generate`, session.cookies, {
    prompt,
    ratio: '1:1',
    resolution: '1K',
    rm_label_watermark: true,
  });
  const result = JSON.parse(resp.data || '{}');
  const imageUrl = result?.data?.image?.image_url || result?.data?.[0]?.url || null;
  if (!imageUrl) throw new Error(`Generate failed: ${String(resp.data).slice(0, 500)}`);
  const saved = await downloadImage(imageUrl, outputDir, `zhipu-${Date.now()}`);
  return { ok: true, prompt, imageUrl, saved };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const cmd = args.cmd;

  if (cmd === 'check-session' || cmd === 'check') {
    const result = await checkSession();
    console.log(JSON.stringify(result, null, 2));
    process.exit(result.ok ? 0 : 1);
  }
  if (cmd === 'login') {
    const result = await captureCookies();
    console.log(JSON.stringify({ ok: true, cookieCount: result.cookies.length, sessionFile: SESSION_FILE }, null, 2));
    return;
  }
  if (cmd === 'login-if-needed') {
    const result = await ensureSession(args);
    console.log(JSON.stringify(result, null, 2));
    process.exit(result.ok ? 0 : 1);
  }
  if (cmd === 'ready') {
    const result = await ensureSession(args);
    console.log(JSON.stringify({
      ok: !!result.ok,
      status: result.ok ? 'available' : 'unavailable',
      sessionFile: SESSION_FILE,
      refreshed: !!result.refreshed,
      openedBrowser: !!result.openedBrowser,
      cookieCount: result.cookieCount || 0,
      reason: result.reason || null,
      loginUrl: result.loginUrl || null,
      waitedMs: result.waitedMs || 0,
    }, null, 2));
    process.exit(result.ok ? 0 : 1);
  }

  const prompt = cmd === 'generate' ? (args.prompt || 'a cute tiger mascot') : ([cmd, args.prompt].filter(Boolean).join(' ') || 'a cute tiger mascot');
  const result = await generate(prompt, args.output);
  console.log(JSON.stringify(result, null, 2));
}

main().catch(error => {
  console.error(error.message);
  process.exit(1);
});
