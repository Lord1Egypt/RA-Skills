#!/usr/bin/env node
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const API_BASE = 'https://superlore-api.onrender.com';
const CONFIG_PATH = path.join(os.homedir(), '.config', 'superlore', 'agent.json');
const ALLOWED_SCOPES = new Set(['episodes:create', 'episodes:upload', 'sources:read']);

function option(name, fallback = null) {
  const index = process.argv.indexOf(`--${name}`);
  if (index < 0) return fallback;
  const next = process.argv[index + 1];
  return !next || next.startsWith('--') ? true : next;
}

function options(name) {
  const values = [];
  for (let index = 0; index < process.argv.length; index += 1) {
    if (process.argv[index] === `--${name}` && process.argv[index + 1] && !process.argv[index + 1].startsWith('--')) {
      values.push(process.argv[index + 1]);
    }
  }
  return values;
}

function loadConfig() {
  if (!fs.existsSync(CONFIG_PATH)) return {};
  return JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
}

function saveCredential(credential, connectionId) {
  const directory = path.dirname(CONFIG_PATH);
  fs.mkdirSync(directory, { recursive: true, mode: 0o700 });
  fs.writeFileSync(CONFIG_PATH, JSON.stringify({
    apiBaseUrl: API_BASE,
    credential,
    connectionId,
    updatedAt: new Date().toISOString(),
  }, null, 2) + '\n', { mode: 0o600 });
  fs.chmodSync(CONFIG_PATH, 0o600);
}

function credential() {
  const token = process.env.SUPERLORE_AGENT_TOKEN || loadConfig().credential;
  if (!token || !String(token).startsWith('slc_')) {
    throw new Error('Superlore is not paired. Run: node scripts/superlore.mjs pair --code 123456');
  }
  return String(token);
}

async function request(route, { method = 'GET', token, body, form } = {}) {
  const headers = {};
  if (token) headers.Authorization = `Bearer ${token}`;
  if (body !== undefined) headers['Content-Type'] = 'application/json';
  const response = await fetch(route.startsWith('http') ? route : `${API_BASE}${route}`, {
    method,
    headers,
    body: form || (body === undefined ? undefined : JSON.stringify(body)),
  });
  const text = await response.text();
  let data = {};
  try { data = text ? JSON.parse(text) : {}; } catch { data = { message: text }; }
  if (!response.ok) {
    const error = new Error(data.message || data.error || `Superlore request failed (${response.status})`);
    error.status = response.status;
    error.code = data.code;
    throw error;
  }
  return data;
}

const sleep = (milliseconds) => new Promise((resolve) => setTimeout(resolve, milliseconds));

async function pair() {
  const rawCode = String(option('code', '')).replace(/\D/g, '');
  if (rawCode.length !== 6) throw new Error('Provide the six-digit code from https://superlore.ai/agents with --code.');
  const scopes = String(option('scopes', 'episodes:create')).split(',').map((scope) => scope.trim()).filter(Boolean);
  if (!scopes.length || scopes.some((scope) => !ALLOWED_SCOPES.has(scope))) {
    throw new Error('Scopes must be episodes:create, episodes:upload, or sources:read.');
  }
  const claimed = await request('/agent/pair', {
    method: 'POST',
    body: { code: rawCode, agentName: String(option('name', 'OpenClaw')), requestedScopes: [...new Set(scopes)] },
  });
  process.stderr.write('Pairing code claimed. Approve the connection in Superlore; waiting for approval…\n');
  const timeoutSeconds = Math.max(30, Math.min(600, Number(option('timeout', 600))));
  const deadline = Date.now() + timeoutSeconds * 1000;
  while (Date.now() < deadline) {
    const status = await request(claimed.statusUrl, { token: claimed.claimSecret });
    if (status.status === 'approved') {
      saveCredential(status.credential, status.connectionId);
      await request(status.acknowledgeUrl, { method: 'POST', token: claimed.claimSecret });
      const tested = await request(status.testUrl, { method: 'POST', token: status.credential });
      process.stdout.write(JSON.stringify({
        ok: true,
        status: 'connected',
        connectionId: status.connectionId,
        scopes: tested.agent?.scopes || scopes,
        sideEffects: tested.sideEffects,
        credentialStoredAt: CONFIG_PATH,
      }, null, 2) + '\n');
      return;
    }
    if (['denied', 'cancelled', 'expired'].includes(status.status)) {
      throw new Error(`Pairing ${status.status}. Request a new code if you still want to connect.`);
    }
    await sleep(3000);
  }
  throw new Error('Pairing approval timed out. Request a new code and try again.');
}

async function testConnection() {
  const result = await request('/agent/v1/test', { method: 'POST', token: credential() });
  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
}

async function context() {
  const result = await request('/agent/v1/context', { token: credential() });
  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
}

async function status(generationId = option('generation')) {
  if (!generationId || generationId === true) throw new Error('Provide --generation gen_...');
  return request(`/agent/v1/generations/${encodeURIComponent(String(generationId))}`, { token: credential() });
}

async function create() {
  const prompt = option('prompt');
  if (!prompt || prompt === true || String(prompt).trim().length < 10) throw new Error('Provide a descriptive --prompt.');
  const minutes = Number(option('minutes', 5));
  if (![5, 10, 15, 20, 30].includes(minutes)) throw new Error('--minutes must be 5, 10, 15, 20, or 30.');
  const payload = {
    prompt: String(prompt).trim(),
    targetMinutes: minutes,
    sourceIds: options('source'),
  };
  const feedId = option('feed');
  if (feedId && feedId !== true) payload.feedId = String(feedId);
  const queued = await request('/agent/v1/episodes', { method: 'POST', token: credential(), body: payload });
  if (option('no-wait', false)) {
    process.stdout.write(JSON.stringify(queued, null, 2) + '\n');
    return;
  }
  const timeoutSeconds = Math.max(60, Math.min(1800, Number(option('timeout', 900))));
  const deadline = Date.now() + timeoutSeconds * 1000;
  while (Date.now() < deadline) {
    const current = await status(queued.generationId);
    if (current.generation?.status === 'completed') {
      process.stdout.write(JSON.stringify(current, null, 2) + '\n');
      return;
    }
    if (current.generation?.status === 'failed') {
      throw new Error(current.generation.errorMessage || current.generation.errorCode || 'Episode generation failed.');
    }
    await sleep(5000);
  }
  throw new Error(`Generation is still running. Check later with --generation ${queued.generationId}`);
}

async function upload() {
  const feedId = option('feed');
  const audioPath = option('audio');
  const title = option('title');
  if (!feedId || feedId === true) throw new Error('Provide --feed feed_...');
  if (!audioPath || audioPath === true || !fs.existsSync(String(audioPath))) throw new Error('Provide an existing audio file with --audio.');
  if (!title || title === true) throw new Error('Provide --title.');
  const bytes = fs.readFileSync(String(audioPath));
  const extension = path.extname(String(audioPath)).toLowerCase();
  const mimeTypes = { '.mp3': 'audio/mpeg', '.m4a': 'audio/mp4', '.wav': 'audio/wav', '.aac': 'audio/aac', '.ogg': 'audio/ogg' };
  const mimeType = mimeTypes[extension];
  if (!mimeType) throw new Error('Audio must be MP3, M4A, WAV, AAC, or OGG.');
  const form = new FormData();
  form.append('audio', new Blob([bytes], { type: mimeType }), path.basename(String(audioPath)));
  form.append('title', String(title));
  const description = option('description');
  if (description && description !== true) form.append('description', String(description));
  const result = await request(`/agent/v1/feeds/${encodeURIComponent(String(feedId))}/items`, {
    method: 'POST',
    token: credential(),
    form,
  });
  process.stdout.write(JSON.stringify(result, null, 2) + '\n');
}

const command = process.argv[2];
try {
  if (command === 'pair') await pair();
  else if (command === 'test') await testConnection();
  else if (command === 'context') await context();
  else if (command === 'create') await create();
  else if (command === 'status') process.stdout.write(JSON.stringify(await status(), null, 2) + '\n');
  else if (command === 'upload') await upload();
  else throw new Error('Usage: superlore.mjs <pair|test|context|create|status|upload> [options]');
} catch (error) {
  process.stderr.write(`Superlore: ${error.message || String(error)}${error.code ? ` [${error.code}]` : ''}\n`);
  process.exitCode = 1;
}
