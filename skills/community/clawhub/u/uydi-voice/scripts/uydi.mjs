#!/usr/bin/env node
/**
 * Uydi Voice CLI — 零依赖（Node 18+，仅内置模块 + 全局 fetch/FormData/Blob）。
 * 通过 OAuth（授权码 + PKCE，降级设备码流）登录 Uydi，之后用 Bearer token 调用全部 API。
 *
 * 用法：node uydi.mjs <command> [options]，详见 SKILL.md 或 `node uydi.mjs help`。
 */
import { createServer } from 'node:http';
import { randomBytes, randomUUID, createHash } from 'node:crypto';
import { readFileSync, writeFileSync, mkdirSync, rmSync, existsSync } from 'node:fs';
import { homedir } from 'node:os';
import { join, basename, resolve } from 'node:path';
import { spawn } from 'node:child_process';

const BASE_URL = (process.env.UYDI_BASE_URL || 'https://uydi.com').replace(/\/+$/, '');
const CLIENT_ID = 'uydi-skill';
const CRED_DIR = process.env.UYDI_CONFIG_DIR || join(homedir(), '.uydi');
const CRED_FILE = join(CRED_DIR, 'credentials.json');
const CALLBACK_TIMEOUT_MS = 120_000;

// ---------- 凭证存取 ----------

function loadToken() {
  try {
    const data = JSON.parse(readFileSync(CRED_FILE, 'utf8'));
    if (data.baseUrl === BASE_URL && data.accessToken) return data.accessToken;
  } catch {}
  return null;
}

function saveToken(accessToken) {
  mkdirSync(CRED_DIR, { recursive: true, mode: 0o700 });
  writeFileSync(
    CRED_FILE,
    JSON.stringify({ baseUrl: BASE_URL, accessToken, savedAt: new Date().toISOString() }, null, 2),
    { mode: 0o600 }
  );
}

// ---------- HTTP 封装 ----------

async function api(path, { method = 'GET', json, form, raw = false, auth = true, idempotencyKey } = {}) {
  const headers = { Accept: 'application/json' };
  if (auth) {
    const token = loadToken();
    if (!token) fail('Not logged in. Run: node uydi.mjs login');
    headers.Authorization = `Bearer ${token}`;
  }
  if (idempotencyKey) headers['Idempotency-Key'] = idempotencyKey;
  let body;
  if (json !== undefined) {
    headers['Content-Type'] = 'application/json';
    body = JSON.stringify(json);
  } else if (form !== undefined) {
    body = form; // FormData 由 fetch 自动设置 Content-Type
  }
  const res = await fetch(`${BASE_URL}${path}`, { method, headers, body });
  if (res.status === 401) fail('Session expired or token revoked. Run: node uydi.mjs login');
  if (raw) {
    if (!res.ok) fail(`Request failed (HTTP ${res.status})`);
    return res;
  }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) fail(data.error || `Request failed (HTTP ${res.status})`);
  return data;
}

function fail(message) {
  console.error(`Error: ${message}`);
  process.exit(1);
}

// ---------- 参数解析 ----------

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith('--')) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next !== undefined && !next.startsWith('--') && !(next.startsWith('-') && next.length === 2)) {
        args[key] = next;
        i++;
      } else {
        args[key] = true;
      }
    } else if (a === '-o') {
      args.output = argv[++i];
    } else {
      args._.push(a);
    }
  }
  return args;
}

// ---------- OAuth 登录 ----------

function b64url(buf) {
  return buf.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function openBrowser(url) {
  const cmd =
    process.platform === 'darwin' ? 'open' : process.platform === 'win32' ? 'start' : 'xdg-open';
  try {
    spawn(cmd, [url], { shell: process.platform === 'win32', stdio: 'ignore', detached: true }).unref();
  } catch {}
}

/** 授权码 + PKCE：本地起 loopback server 接收回调 */
async function loginPkce() {
  const verifier = b64url(randomBytes(32));
  const challenge = b64url(createHash('sha256').update(verifier).digest());
  const state = b64url(randomBytes(16));

  const { server, port } = await new Promise((res, rej) => {
    const srv = createServer();
    srv.once('error', rej);
    srv.listen(0, '127.0.0.1', () => res({ server: srv, port: srv.address().port }));
  });
  const redirectUri = `http://127.0.0.1:${port}/callback`;

  const authUrl = new URL(`${BASE_URL}/oauth/authorize`);
  authUrl.searchParams.set('client_id', CLIENT_ID);
  authUrl.searchParams.set('redirect_uri', redirectUri);
  authUrl.searchParams.set('state', state);
  authUrl.searchParams.set('code_challenge', challenge);
  authUrl.searchParams.set('code_challenge_method', 'S256');

  console.log('Opening your browser to authorize. If it does not open automatically, visit:\n');
  console.log(`  ${authUrl.toString()}\n`);
  openBrowser(authUrl.toString());

  const code = await new Promise((resolvePromise, rejectPromise) => {
    const timer = setTimeout(() => {
      server.close();
      rejectPromise(new Error('timeout'));
    }, CALLBACK_TIMEOUT_MS);
    server.on('request', (req, res) => {
      const url = new URL(req.url, `http://127.0.0.1:${port}`);
      if (url.pathname !== '/callback') {
        res.writeHead(404).end();
        return;
      }
      const err = url.searchParams.get('error');
      const gotCode = url.searchParams.get('code');
      const gotState = url.searchParams.get('state');
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      if (err || !gotCode || gotState !== state) {
        res.end('<h3>Authorization failed. You can close this tab.</h3>');
        clearTimeout(timer);
        server.close();
        rejectPromise(new Error(err || 'invalid callback'));
      } else {
        res.end('<h3>Authorized! You can close this tab and return to the terminal.</h3>');
        clearTimeout(timer);
        server.close();
        resolvePromise(gotCode);
      }
    });
  });

  const token = await api('/api/oauth/token', {
    method: 'POST',
    auth: false,
    json: {
      grant_type: 'authorization_code',
      client_id: CLIENT_ID,
      code,
      code_verifier: verifier,
      redirect_uri: redirectUri,
    },
  });
  return token.access_token;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/** 设备授权流（RFC 8628）：终端出码，浏览器批准，本地轮询 */
async function loginDevice() {
  const dc = await api('/api/oauth/device/code', {
    method: 'POST',
    auth: false,
    json: { client_id: CLIENT_ID },
  });
  console.log('Open the URL below in a browser and enter the device code to authorize:\n');
  console.log(`  URL:  ${dc.verification_uri}`);
  console.log(`  Code: ${dc.user_code}\n`);
  console.log(`(or open ${dc.verification_uri_complete} directly)\nWaiting for authorization…`);
  openBrowser(dc.verification_uri_complete);

  let interval = (dc.interval || 5) * 1000;
  const deadline = Date.now() + dc.expires_in * 1000;
  while (Date.now() < deadline) {
    await sleep(interval);
    const res = await fetch(`${BASE_URL}/api/oauth/token`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        grant_type: 'urn:ietf:params:oauth:grant-type:device_code',
        client_id: CLIENT_ID,
        device_code: dc.device_code,
      }),
    });
    const data = await res.json().catch(() => ({}));
    if (res.ok) return data.access_token;
    if (data.error === 'authorization_pending') continue;
    if (data.error === 'slow_down') {
      interval += 5000;
      continue;
    }
    if (data.error === 'access_denied') fail('Authorization denied by the user');
    if (data.error === 'expired_token') break;
    fail(data.error || 'Device code polling failed');
  }
  fail('Device code expired. Run login again');
}

async function cmdLogin(args) {
  let accessToken = null;
  if (!args.device) {
    try {
      accessToken = await loginPkce();
    } catch (err) {
      console.log(`\nBrowser authorization not completed (${err.message}); falling back to device code flow…\n`);
    }
  }
  if (!accessToken) accessToken = await loginDevice();
  saveToken(accessToken);
  const { user } = await api('/api/auth/me');
  console.log(`\n✅ Logged in as ${user.email} (token saved to ${CRED_FILE})`);
}

async function cmdLogout() {
  const token = loadToken();
  if (token) {
    await fetch(`${BASE_URL}/api/oauth/revoke`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
    }).catch(() => {});
  }
  if (existsSync(CRED_FILE)) rmSync(CRED_FILE);
  console.log('Logged out: token revoked and local credentials removed');
}

// ---------- 业务命令 ----------

async function cmdWhoami() {
  const { user } = await api('/api/auth/me');
  console.log(JSON.stringify(user, null, 2));
}

async function cmdCredits() {
  const c = await api('/api/credits');
  console.log(`Plan: ${c.plan}    Balance: ${c.balance} credits`);
  console.log(
    `Pricing: design=${c.pricing.design}, clone=${c.pricing.clone}, tts=1 credit / ${c.pricing.ttsUnitChars} chars`
  );
  if (c.canvasQuota) console.log(`Voice Canvas: ${c.canvasQuota.maxChars} characters per project`);
}

const fmtTime = (ts) => new Date(ts * 1000).toISOString().replace('T', ' ').slice(0, 19);

async function cmdVoices() {
  const { voices } = await api('/api/voices');
  if (!voices.length) {
    console.log('(no voices yet — create one with design or clone)');
    return;
  }
  for (const v of voices) {
    const languages = Array.isArray(v.supportedLanguages) ? `  languages=${v.supportedLanguages.join(',')}` : '';
    console.log(`${v.id}  [${v.kind}/${v.provider}]  ${v.name}  (${v.status}, ${fmtTime(v.createdAt)})${languages}`);
  }
}

async function cmdDeleteVoice(args) {
  const id = args._[0];
  if (!id) fail('Usage: delete-voice <voiceId>');
  await api(`/api/voices/${id}`, { method: 'DELETE' });
  console.log(`Deleted voice ${id}`);
}

/** 用 Bearer 下载站内音频（如 /api/audio/xxx）到本地文件 */
async function downloadAudio(urlPath, outPath) {
  const res = await api(urlPath, { raw: true });
  writeFileSync(outPath, Buffer.from(await res.arrayBuffer()));
  console.log(`Audio saved: ${resolve(outPath)}`);
}

async function cmdDesign(args) {
  if (!args.name || !args.prompt || !args['preview-text']) {
    fail('Usage: design --name <name> --prompt <voice description> --preview-text <text> [--provider qwen|cosyvoice] [-o preview.wav]');
  }
  console.log('Designing voice (takes ~10-30s, consumes credits)…');
  const { voice } = await recoverableDesign({
    provider: args.provider || 'qwen',
    name: args.name,
    voicePrompt: args.prompt,
    previewText: args['preview-text'],
  });
  console.log(`✅ Voice created: ${voice.id} (${voice.name})`);
  if (args.output && voice.previewUrl) await downloadAudio(voice.previewUrl, args.output);
}

/** Retain the same design key across a lost response or CLI restart, scoped to these credentials. */
async function recoverableDesign(input) {
  const token = loadToken();
  if (!token) fail('Not logged in. Run: node uydi.mjs login');
  const fingerprint = createHash('sha256').update(JSON.stringify([BASE_URL, token, 'design', input])).digest('hex');
  const directory = join(CRED_DIR, 'operations');
  const file = join(directory, `design-${fingerprint}.json`);
  mkdirSync(directory, { recursive: true, mode: 0o700 });
  const resuming = existsSync(file);
  let key;
  if (resuming) {
    try { key = JSON.parse(readFileSync(file, 'utf8')).key; } catch { fail('Cannot read the pending design operation. Check your local configuration before retrying.'); }
    if (typeof key !== 'string' || !/^[A-Za-z0-9._:-]{8,200}$/.test(key)) fail('Invalid pending design operation. Check your local configuration before retrying.');
  } else {
    key = randomUUID();
    writeFileSync(file, JSON.stringify({ key }), { mode: 0o600, flag: 'wx' });
  }
  console.log(`Idempotency-Key: ${key}`);
  const headers = { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' };
  const lookup = `/api/operations/design/${encodeURIComponent(key)}`;
  let shouldPost = !resuming;
  const deadline = Date.now() + 180_000;
  while (Date.now() < deadline) {
    const posting = shouldPost;
    shouldPost = false;
    try {
      const response = await fetch(`${BASE_URL}${posting ? '/api/voices/design' : lookup}`, {
        method: posting ? 'POST' : 'GET',
        headers: posting ? { ...headers, 'Idempotency-Key': key } : headers,
        ...(posting ? { body: JSON.stringify(input) } : {}),
        signal: AbortSignal.timeout(posting ? 120_000 : 10_000),
      });
      const data = await response.json();
      if (response.status === 401 || response.status === 403) fail(data.error || 'This account cannot access the pending design.');
      if (!posting && response.status === 404) { shouldPost = true; continue; }
      if (posting && response.ok && data.voice) { rmSync(file, { force: true }); return data; }
      if (!posting && response.ok && data.status === 'completed' && data.response?.voice) {
        rmSync(file, { force: true }); return data.response;
      }
      if (!posting && response.ok && data.status === 'failed') {
        rmSync(file, { force: true }); fail(data.response?.error || 'Voice design failed.');
      }
      if (posting && response.status >= 400 && response.status < 500) {
        rmSync(file, { force: true }); fail(data.error || `Voice design failed (HTTP ${response.status})`);
      }
      // Unknown server errors and interrupted responses must be reconciled before another POST.
    } catch { /* Keep the request key and query the server after a transport failure. */ }
    await new Promise((resolve) => setTimeout(resolve, 1500));
  }
  fail('Voice design is still unresolved. Run the same command again to resume this request without starting a new design.');
}

async function cmdClone(args) {
  if (!args.name || !args.file) {
    fail('Usage: clone --name <name> --file <audio> --rights-basis self|authorized-adult --confirm-rights [--provider qwen|cosyvoice] [--language code]');
  }
  if (!['self', 'authorized-adult'].includes(args['rights-basis']))
    fail('--rights-basis must be self or authorized-adult');
  if (args['confirm-rights'] !== true)
    fail('--confirm-rights is required and confirms adult status, explicit authorization, and Uydi acceptable-use rules');
  if (!existsSync(args.file)) fail(`File not found: ${args.file}`);
  console.log('Uploading sample and cloning voice (takes ~10-60s, consumes credits)…');
  const form = new FormData();
  form.set('provider', args.provider || 'qwen');
  form.set('name', args.name);
  if (args.language && !LANGUAGE_CODES.has(args.language)) fail('Unsupported language code');
  if (args.language) form.set('language', args.language);
  form.set('rightsBasis', args['rights-basis'] === 'self' ? 'self' : 'authorized_adult');
  form.set('voiceOwnerAdult', 'true');
  form.set('authorizationConfirmed', 'true');
  form.set('acceptableUseConfirmed', 'true');
  form.set('file', new Blob([readFileSync(args.file)]), basename(args.file));
  const { voice } = await api('/api/voices/clone', {
    method: 'POST',
    form,
    idempotencyKey: randomUUID(),
  });
  console.log(`✅ Voice cloned: ${voice.id} (${voice.name})`);
}

async function cmdTts(args) {
  if (!args.voice || !args.text) {
    fail('Usage: tts --voice <voiceId> --text "text to speak" -o out.wav');
  }
  const voiceType = args['voice-type'];
  if (voiceType && !['user', 'system'].includes(voiceType)) fail('--voice-type must be user or system');
  if (voiceType === 'system' && !args.language) fail('System voices require --language (for example, en)');
  const out = args.output || 'out.wav';
  console.log('Synthesizing speech (1 credit / 10 chars)…');
  const { synthesis } = await api('/api/synthesize', {
    method: 'POST',
    json: { voiceId: args.voice, text: args.text, ...(voiceType ? { voiceType } : {}), ...(args.language ? { language: args.language } : {}) },
    idempotencyKey: randomUUID(),
  });
  console.log(`✅ Synthesis complete: ${synthesis.id} (${synthesis.chars} chars)`);
  await downloadAudio(synthesis.audioUrl, out);
}

async function cmdHistory(args) {
  const limit = Number(args.limit || 20);
  const { syntheses } = await api('/api/syntheses');
  if (!syntheses.length) {
    console.log('(no synthesis history yet)');
    return;
  }
  for (const s of syntheses.slice(0, limit)) {
    const text = s.text.length > 40 ? `${s.text.slice(0, 40)}…` : s.text;
    console.log(`${s.id}  [${s.voiceName}]  ${fmtTime(s.createdAt)}  "${text}"`);
  }
}

// ---------- Voice Canvas ----------

const LANGUAGE_CODES = new Set(['zh', 'en', 'ja', 'ko', 'fr', 'de', 'ru', 'pt', 'th', 'id', 'vi', 'es', 'it', 'ms', 'fil', 'ar']);

function positionalId(args, usage) {
  const id = args._[0];
  if (!id) fail(`Usage: ${usage}`);
  return encodeURIComponent(id);
}

function positiveNumber(value, fallback, label) {
  const number = Number(value ?? fallback);
  if (!Number.isFinite(number) || number <= 0) fail(`${label} must be a positive number`);
  return number;
}

function loadCanvasDocument(file) {
  if (!file) fail('Usage: canvas-save <projectId> --file <canvas.json>');
  if (!existsSync(file)) fail(`File not found: ${file}`);
  let document;
  try {
    document = JSON.parse(readFileSync(file, 'utf8'));
  } catch {
    fail(`Invalid JSON file: ${file}`);
  }
  if (!document || typeof document !== 'object' || Array.isArray(document)) fail('Canvas JSON must be an object');
  if (!Number.isInteger(document.version)) fail('Canvas JSON must include the current integer project version');
  if (!Array.isArray(document.nodes) || document.nodes.length < 1) fail('Canvas JSON must include at least one node');
  for (let index = 0; index < document.nodes.length; index++) {
    const node = document.nodes[index];
    if (!node || typeof node !== 'object') fail(`Node ${index + 1} must be an object`);
    if (!LANGUAGE_CODES.has(node.language)) fail(`Node ${index + 1} has an unsupported language code`);
    if (node.languageSource !== 'auto' && node.languageSource !== 'manual') fail(`Node ${index + 1} needs languageSource auto or manual`);
    if (typeof node.text !== 'string' || node.text.length > 600) fail(`Node ${index + 1} text must be 0-600 characters`);
    const pause = node.pauseAfterMs ?? 300;
    if (!Number.isInteger(pause) || pause < 0 || pause > 3000) fail(`Node ${index + 1} pauseAfterMs must be an integer from 0 to 3000`);
    if (node.voice !== null && (typeof node.voice !== 'object' || !['system', 'user'].includes(node.voice.type) || !node.voice.id)) {
      fail(`Node ${index + 1} voice must be null or { type: "system"|"user", id, name }`);
    }
  }
  return document;
}

async function cmdSystemVoices(args) {
  const language = args.language;
  if (!LANGUAGE_CODES.has(language)) fail('Usage: system-voices --language <languageCode> [--search <text>] [--limit n]');
  const params = new URLSearchParams({ language, limit: String(Math.min(100, Math.floor(positiveNumber(args.limit, 50, 'limit')))) });
  if (args.search) params.set('search', args.search);
  if (args.gender) params.set('gender', args.gender);
  if (args.age) params.set('age', args.age);
  if (args.scenario) params.set('scenario', args.scenario);
  if (args.cursor) params.set('cursor', args.cursor);
  const result = await api(`/api/system-voices?${params}`);
  console.log(JSON.stringify(result, null, 2));
}

async function cmdCanvasList() {
  const { projects } = await api('/api/dubbing/projects');
  if (!projects.length) {
    console.log('(no Voice Canvas projects yet — create one with canvas-create)');
    return;
  }
  for (const project of projects) {
    console.log(`${project.id}  v${project.version}  [${project.status}]  ${project.title}  (${fmtTime(project.updatedAt)})`);
  }
}

async function cmdCanvasCreate(args) {
  const result = await api('/api/dubbing/projects', {
    method: 'POST',
    json: { title: typeof args.title === 'string' ? args.title : undefined },
  });
  console.log(JSON.stringify(result, null, 2));
}

async function cmdCanvasShow(args) {
  const id = positionalId(args, 'canvas-show <projectId>');
  console.log(JSON.stringify(await api(`/api/dubbing/projects/${id}`), null, 2));
}

async function cmdCanvasSave(args) {
  const id = positionalId(args, 'canvas-save <projectId> --file <canvas.json>');
  const document = loadCanvasDocument(args.file);
  const result = await api(`/api/dubbing/projects/${id}/nodes`, {
    method: 'PUT',
    json: { version: document.version, title: document.title, nodes: document.nodes },
  });
  console.log(JSON.stringify(result, null, 2));
}

async function cmdCanvasDelete(args) {
  const id = positionalId(args, 'canvas-delete <projectId>');
  await api(`/api/dubbing/projects/${id}`, { method: 'DELETE' });
  console.log(`Deleted Voice Canvas project ${args._[0]}`);
}

async function currentCanvasVersion(projectId) {
  const detail = await api(`/api/dubbing/projects/${encodeURIComponent(projectId)}`);
  return detail;
}

async function canvasEstimate(projectId, version) {
  return api(`/api/dubbing/projects/${encodeURIComponent(projectId)}/render-estimate?version=${encodeURIComponent(version)}`);
}

async function cmdCanvasEstimate(args) {
  const projectId = args._[0];
  if (!projectId) fail('Usage: canvas-estimate <projectId> [--version n]');
  const detail = await currentCanvasVersion(projectId);
  const version = args.version === undefined ? detail.project.version : Number(args.version);
  if (!Number.isInteger(version)) fail('version must be an integer');
  console.log(JSON.stringify(await canvasEstimate(projectId, version), null, 2));
}

async function waitForCanvasRender(renderId, timeoutSeconds) {
  const deadline = Date.now() + timeoutSeconds * 1000;
  let lastProgress = '';
  while (Date.now() < deadline) {
    const detail = await api(`/api/dubbing/renders/${encodeURIComponent(renderId)}`);
    const render = detail.render;
    const progress = `${render.status}:${render.completedNodes}/${render.totalNodes}`;
    if (progress !== lastProgress) {
      console.log(`Render ${render.status}: ${render.completedNodes}/${render.totalNodes} nodes`);
      lastProgress = progress;
    }
    if (render.status === 'completed') return detail;
    if (render.status === 'failed') fail(render.error || `Voice Canvas render ${renderId} failed`);
    await sleep(2000);
  }
  fail(`Render is still running after ${timeoutSeconds} seconds. Check it with: canvas-status ${renderId}`);
}

function defaultCanvasOutput(title) {
  const safe = String(title || 'voice-canvas').replace(/[^a-z0-9 _-]/gi, '').trim();
  return `${safe || 'voice-canvas'}.wav`;
}

async function cmdCanvasRender(args) {
  const projectId = args._[0];
  if (!projectId) fail('Usage: canvas-render <projectId> [--version n] [--key idempotency-key] [--no-wait] [--timeout seconds] [-o output.wav]');
  const detail = await currentCanvasVersion(projectId);
  const version = args.version === undefined ? detail.project.version : Number(args.version);
  if (!Number.isInteger(version)) fail('version must be an integer');
  const estimate = await canvasEstimate(projectId, version);
  console.log(`Estimate: ${estimate.estimatedCost} credits, balance ${estimate.balance}, ${estimate.totalChars}/${estimate.characterLimit} characters, ${estimate.reusedNodes} nodes reused`);
  if (!estimate.sufficient) fail(`Insufficient credits: ${estimate.estimatedCost} needed, ${estimate.balance} available`);

  const key = typeof args.key === 'string' ? args.key : randomUUID();
  console.log(`Idempotency-Key: ${key}`);
  const started = await api(`/api/dubbing/projects/${encodeURIComponent(projectId)}/renders`, {
    method: 'POST',
    json: { version },
    idempotencyKey: key,
  });
  console.log(`Render started: ${started.renderId} (${started.status})`);
  if (args['no-wait']) {
    console.log(JSON.stringify(started, null, 2));
    return;
  }
  const completed = await waitForCanvasRender(started.renderId, positiveNumber(args.timeout, 1800, 'timeout'));
  const out = args.output || defaultCanvasOutput(detail.project.title);
  await downloadAudio(`${completed.render.audioUrl}?download=1`, out);
  console.log(`✅ Voice Canvas complete: ${completed.render.id} (${completed.render.durationMs ?? 0} ms, ${completed.render.totalCost} credits)`);
}

async function cmdCanvasStatus(args) {
  const renderId = args._[0];
  if (!renderId) fail('Usage: canvas-status <renderId> [--wait] [--timeout seconds] [-o output.wav]');
  const detail = args.wait
    ? await waitForCanvasRender(renderId, positiveNumber(args.timeout, 1800, 'timeout'))
    : await api(`/api/dubbing/renders/${encodeURIComponent(renderId)}`);
  console.log(JSON.stringify(detail, null, 2));
  if (args.output) {
    if (detail.render.status !== 'completed' || !detail.render.audioUrl) fail('The render is not complete yet');
    await downloadAudio(`${detail.render.audioUrl}?download=1`, args.output);
  }
}

async function cmdCanvasRenders(args) {
  const limit = Math.floor(positiveNumber(args.limit, 20, 'limit'));
  const { renders } = await api('/api/dubbing/renders');
  console.log(JSON.stringify(renders.slice(0, limit), null, 2));
}

// ---------- Freestyle Sound Scenes ----------

function loadSceneDocument(file) {
  if (!file) fail('Usage: scene-create|scene-save <projectId> --file <scene.json>');
  if (!existsSync(file)) fail(`File not found: ${file}`);
  let document;
  try { document = JSON.parse(readFileSync(file, 'utf8')); } catch { fail(`Invalid JSON file: ${file}`); }
  if (!document || typeof document !== 'object' || Array.isArray(document)) fail('Scene JSON must be an object');
  const project = document.project && typeof document.project === 'object' ? document.project : document;
  const draft = document.suggestion?.draft || project.draft || document.draft || document;
  if (!draft || typeof draft !== 'object' || !['zh', 'en'].includes(draft.language)) fail('Scene draft must specify language "zh" or "en"');
  return { version: project.version ?? document.version, draft };
}

async function cmdSceneOptimize(args) {
  if (!['zh', 'en'].includes(args.language) || !args.idea) fail('Usage: scene-optimize --language zh|en --idea <idea> [--draft-file <scene.json>]');
  const draft = args['draft-file'] ? loadSceneDocument(args['draft-file']).draft : undefined;
  const result = await api('/api/scenes/optimize', { method: 'POST', json: { language: args.language, idea: args.idea, ...(draft ? { draft } : {}) } });
  console.log(JSON.stringify(result, null, 2));
}

async function cmdSceneList() {
  const { projects } = await api('/api/scenes/projects');
  if (!projects.length) { console.log('(no Sound Scenes yet — create one with scene-create)'); return; }
  for (const project of projects) console.log(`${project.id}  v${project.version}  ${project.draft.title}  (${fmtTime(project.updatedAt)})`);
}

async function cmdSceneCreate(args) {
  const { draft } = loadSceneDocument(args.file);
  console.log(JSON.stringify(await api('/api/scenes/projects', { method: 'POST', json: { draft } }), null, 2));
}

async function cmdSceneShow(args) {
  const id = positionalId(args, 'scene-show <projectId>');
  console.log(JSON.stringify(await api(`/api/scenes/projects/${id}`), null, 2));
}

async function cmdSceneSave(args) {
  const id = positionalId(args, 'scene-save <projectId> --file <scene.json>');
  const document = loadSceneDocument(args.file);
  if (!Number.isSafeInteger(document.version) || document.version < 1) fail('Scene JSON must include the current integer project version');
  console.log(JSON.stringify(await api(`/api/scenes/projects/${id}`, { method: 'PUT', json: { version: document.version, draft: document.draft } }), null, 2));
}

async function cmdSceneEstimate(args) {
  const id = args._[0];
  if (!id) fail('Usage: scene-estimate <projectId> [--version n]');
  const { project } = await api(`/api/scenes/projects/${encodeURIComponent(id)}`);
  const version = args.version === undefined ? project.version : Number(args.version);
  if (!Number.isSafeInteger(version) || version < 1) fail('version must be a positive integer');
  const { estimate } = await api(`/api/scenes/projects/${encodeURIComponent(id)}/estimate`, { method: 'POST', json: { version } });
  console.log(JSON.stringify({ projectId: id, title: project.draft.title, ...estimate }, null, 2));
}

async function waitForSceneRender(renderId, timeoutSeconds) {
  const deadline = Date.now() + timeoutSeconds * 1000; let last = '';
  while (Date.now() < deadline) {
    const detail = await api(`/api/scenes/renders/${encodeURIComponent(renderId)}`); const render = detail.render;
    if (render.status !== last) { console.log(`Scene ${render.status}`); last = render.status; }
    if (render.status === 'completed') return detail;
    if (render.status === 'failed') fail(render.error || `Sound Scene render ${renderId} failed`);
    await new Promise(resolve => setTimeout(resolve, 2000));
  }
  fail(`Render is still running after ${timeoutSeconds} seconds. Check it with: scene-status ${renderId}`);
}

async function cmdSceneGenerate(args) {
  const projectId = args._[0];
  if (!projectId || args['quoted-credits'] === undefined) fail('Usage: scene-generate <projectId> --quoted-credits <exact-estimate> [--key idempotency-key] [--no-wait] [--timeout seconds] [-o scene.wav]');
  const { project } = await api(`/api/scenes/projects/${encodeURIComponent(projectId)}`);
  const version = args.version === undefined ? project.version : Number(args.version);
  if (!Number.isSafeInteger(version) || version < 1) fail('version must be a positive integer');
  const { estimate } = await api(`/api/scenes/projects/${encodeURIComponent(projectId)}/estimate`, { method: 'POST', json: { version } });
  const quotedCredits = Number(args['quoted-credits']);
  if (!Number.isSafeInteger(quotedCredits) || quotedCredits !== estimate.totalCost) fail(`Quote changed or not confirmed: current estimate is ${estimate.totalCost} credits. Review it, then pass --quoted-credits ${estimate.totalCost}`);
  console.log(`Confirmed quote: ${estimate.totalCost} credits · balance ${estimate.balance}`);
  if (!estimate.canGenerate) fail('Insufficient credits for this scene.');
  const idempotencyKey = typeof args.key === 'string' ? args.key : randomUUID();
  console.log(`Idempotency-Key: ${idempotencyKey}`);
  const { render } = await api(`/api/scenes/projects/${encodeURIComponent(projectId)}/generate`, { method: 'POST', json: { version, idempotencyKey, quotedCredits } });
  console.log(`Scene render ${render.status}: ${render.id}`);
  if (args['no-wait']) { console.log(JSON.stringify({ render }, null, 2)); return; }
  const completed = await waitForSceneRender(render.id, positiveNumber(args.timeout, 1800, 'timeout'));
  const out = args.output || `${String(project.draft.title || 'sound-scene').replace(/[^a-z0-9 _-]/gi, '').trim() || 'sound-scene'}.wav`;
  await downloadAudio(completed.render.audioUrl, out);
  console.log(`✅ Sound Scene complete: ${completed.render.id} (${completed.render.durationMs ?? 0} ms, ${completed.render.totalCost} credits)`);
}

async function cmdSceneStatus(args) {
  const id = args._[0];
  if (!id) fail('Usage: scene-status <renderId> [--wait] [--timeout seconds] [-o scene.wav]');
  const detail = args.wait ? await waitForSceneRender(id, positiveNumber(args.timeout, 1800, 'timeout')) : await api(`/api/scenes/renders/${encodeURIComponent(id)}`);
  console.log(JSON.stringify(detail, null, 2));
  if (args.output) {
    if (detail.render.status !== 'completed' || !detail.render.audioUrl) fail('The scene render is not complete yet');
    await downloadAudio(detail.render.audioUrl, args.output);
  }
}

async function cmdSceneRenders(args) {
  const limit = Math.floor(positiveNumber(args.limit, 20, 'limit'));
  const { renders } = await api('/api/scenes/renders');
  console.log(JSON.stringify(renders.slice(0, limit), null, 2));
}

async function cmdSceneDelete(args) {
  const id = positionalId(args, 'scene-delete <projectId>');
  await api(`/api/scenes/projects/${id}`, { method: 'DELETE' });
  console.log(`Deleted Sound Scenes project ${args._[0]}`);
}

// ---------- 入口 ----------

const HELP = `Uydi Voice CLI — voice design / cloning / TTS / Sound Scenes / Voice Canvas (${BASE_URL})

Usage: node uydi.mjs <command> [options]

  login [--device]        OAuth login (browser flow by default; --device forces device code flow)
  logout                  Revoke token and delete local credentials
  whoami                  Current account
  credits                 Credit balance and pricing
  voices                  List my voices
  delete-voice <id>       Delete a voice
  design --name <n> --prompt <desc> --preview-text <t> [--provider qwen|cosyvoice] [-o preview.wav]
  clone --name <n> --file <audio> --rights-basis self|authorized-adult --confirm-rights [--provider qwen|cosyvoice] [--language code]
  tts --voice <voiceId> --text "text" -o out.wav [--voice-type system --language en]
  history [--limit n]     Synthesis history
  system-voices --language <code> [--search text] [--gender value] [--age value] [--scenario value] [--limit n]
  canvas-list             List Voice Canvas projects
  canvas-create [--title text]
  canvas-show <projectId>
  canvas-save <projectId> --file <canvas.json>
  canvas-estimate <projectId> [--version n]
  canvas-render <projectId> [--version n] [--key value] [--no-wait] [--timeout seconds] [-o output.wav]
  canvas-status <renderId> [--wait] [--timeout seconds] [-o output.wav]
  canvas-renders [--limit n]
  canvas-delete <projectId>
  scene-optimize --language zh|en --idea <text> [--draft-file file.json]
  scene-list
  scene-create --file <scene.json>
  scene-show <projectId>
  scene-save <projectId> --file <scene.json>
  scene-estimate <projectId> [--version n]
  scene-generate <projectId> --quoted-credits <exact-estimate> [--key value] [--no-wait] [-o scene.wav]
  scene-status <renderId> [--wait] [--timeout seconds] [-o scene.wav]
  scene-renders [--limit n]
  scene-delete <projectId>

Env: UYDI_BASE_URL overrides the service URL (default https://uydi.com)`;

const COMMANDS = {
  login: cmdLogin,
  logout: cmdLogout,
  whoami: cmdWhoami,
  credits: cmdCredits,
  voices: cmdVoices,
  'delete-voice': cmdDeleteVoice,
  design: cmdDesign,
  clone: cmdClone,
  tts: cmdTts,
  history: cmdHistory,
  'system-voices': cmdSystemVoices,
  'canvas-list': cmdCanvasList,
  'canvas-create': cmdCanvasCreate,
  'canvas-show': cmdCanvasShow,
  'canvas-save': cmdCanvasSave,
  'canvas-estimate': cmdCanvasEstimate,
  'canvas-render': cmdCanvasRender,
  'canvas-status': cmdCanvasStatus,
  'canvas-renders': cmdCanvasRenders,
  'canvas-delete': cmdCanvasDelete,
  'scene-optimize': cmdSceneOptimize,
  'scene-list': cmdSceneList,
  'scene-create': cmdSceneCreate,
  'scene-show': cmdSceneShow,
  'scene-save': cmdSceneSave,
  'scene-estimate': cmdSceneEstimate,
  'scene-generate': cmdSceneGenerate,
  'scene-status': cmdSceneStatus,
  'scene-renders': cmdSceneRenders,
  'scene-delete': cmdSceneDelete,
};

const [cmd, ...rest] = process.argv.slice(2);
if (!cmd || cmd === 'help' || cmd === '--help') {
  console.log(HELP);
  process.exit(0);
}
const handler = COMMANDS[cmd];
if (!handler) {
  console.error(`Unknown command: ${cmd}\n`);
  console.log(HELP);
  process.exit(1);
}
handler(parseArgs(rest)).catch((err) => fail(err.message));
