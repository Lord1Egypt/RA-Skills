/**
 * TKSeller data-service API client.
 *
 * 所有 /api/v1/* 接口走这里。统一加 Authorization: Bearer <token>。
 * 401 自动清 token 并抛 InvalidToken，由上层提示老板重登。
 */
import { readFileSync, writeFileSync, existsSync, mkdirSync, unlinkSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import { createHash, randomUUID } from 'crypto';
import { execSync } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export const SKILL_DIR = dirname(__dirname);
export const CONFIG_PATH = join(SKILL_DIR, 'config.json');
export const TOKEN_PATH = join(SKILL_DIR, 'data', 'token.json');

const DEFAULT_TIMEOUT_MS = 60000;

// ========== Error classes ==========
export class InvalidToken extends Error {
  constructor(msg = 'invalid_token') {
    super(msg);
    this.name = 'InvalidToken';
  }
}

export class ApiError extends Error {
  constructor(status, message, body = null) {
    super(`API ${status}: ${message}`);
    this.name = 'ApiError';
    this.status = status;
    this.body = body;
  }
}

// ========== config / token ==========
function _cfg() {
  return JSON.parse(readFileSync(CONFIG_PATH, 'utf-8'));
}

export function baseUrl() {
  return _cfg().data_service.base_url.replace(/\/+$/, '');
}

export function loadToken() {
  if (!existsSync(TOKEN_PATH)) return null;
  try {
    const d = JSON.parse(readFileSync(TOKEN_PATH, 'utf-8'));
    return d.token || null;
  } catch {
    return null;
  }
}

export function saveToken(token, username = null, deviceId = null) {
  mkdirSync(dirname(TOKEN_PATH), { recursive: true });
  const d = { token };
  if (username) d.username = username;
  if (deviceId) d.device_id = deviceId;
  writeFileSync(TOKEN_PATH, JSON.stringify(d, null, 2), 'utf-8');
}

export function clearToken() {
  if (existsSync(TOKEN_PATH)) {
    try { unlinkSync(TOKEN_PATH); } catch { /* ignore */ }
  }
}

export function hasToken() {
  return loadToken() !== null;
}

// ========== device_id（绑定主板，重装系统也不变） ==========
let _deviceIdCache = null;

export function getDeviceId() {
  if (_deviceIdCache) return _deviceIdCache;

  let biosUuid = null;
  try {
    if (process.platform === 'win32') {
      const out = execSync('wmic csproduct get uuid', { encoding: 'utf-8', timeout: 10000, stdio: ['pipe', 'pipe', 'pipe'] });
      for (const line of out.trim().split(/\r?\n/)) {
        const l = line.trim();
        if (l && l.toUpperCase() !== 'UUID') {
          biosUuid = l;
          break;
        }
      }
    } else {
      const out = execSync('cat /sys/class/dmi/id/product_uuid', { encoding: 'utf-8', timeout: 10000, stdio: ['pipe', 'pipe', 'pipe'] });
      biosUuid = out.trim();
    }
  } catch { /* ignore */ }

  if (!biosUuid) {
    // fallback: machine-id (Linux) or random
    try {
      biosUuid = readFileSync('/etc/machine-id', 'utf-8').trim();
    } catch {
      biosUuid = randomUUID();
    }
  }

  _deviceIdCache = `openclaw_${createHash('md5').update(biosUuid).digest('hex').slice(0, 12)}`;
  return _deviceIdCache;
}

// ========== 请求封装 ==========
function _headers(auth = true) {
  const h = { 'Content-Type': 'application/json' };
  if (auth) {
    const token = loadToken();
    if (!token) throw new InvalidToken('local token missing');
    h['Authorization'] = `Bearer ${token}`;
  }
  return h;
}

async function _request(method, path, { auth = true, jsonBody = null, timeoutMs = null, params = null } = {}) {
  let url = `${baseUrl()}${path}`;
  if (params) {
    const qs = new URLSearchParams(params).toString();
    if (qs) url += `?${qs}`;
  }

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs || DEFAULT_TIMEOUT_MS);

  let r;
  try {
    r = await fetch(url, {
      method,
      headers: _headers(auth),
      body: jsonBody ? JSON.stringify(jsonBody) : undefined,
      signal: controller.signal,
    });
  } catch (e) {
    clearTimeout(timer);
    throw new ApiError(0, `network error: ${e.message}`);
  }
  clearTimeout(timer);

  // 401 -> 清 token
  if (r.status === 401) {
    clearToken();
    let body;
    try { body = await r.json(); } catch { body = { error: (await r.text()).slice(0, 200) }; }
    throw new InvalidToken(body.error || 'invalid_token');
  }

  if (r.status >= 400) {
    let body;
    try { body = await r.json(); } catch { body = { error: (await r.text()).slice(0, 200) }; }
    throw new ApiError(r.status, body.error || 'http_error', body);
  }

  try {
    return await r.json();
  } catch {
    return { ok: true, raw: await r.text() };
  }
}

// ========== 鉴权 ==========
export async function login(username, password) {
  const deviceId = getDeviceId();
  const resp = await _request('POST', '/api/v1/auth/login', {
    auth: false,
    jsonBody: { username, password, device_id: deviceId },
    timeoutMs: 30000,
  });
  if (resp.ok && resp.token) {
    saveToken(resp.token, username, deviceId);
  }
  return resp;
}

// ========== 业务接口 ==========
export async function recommend(url = null) {
  const body = url ? { video_url: url } : {};
  return _request('POST', '/api/v1/recommend', { jsonBody: body, timeoutMs: 60000 });
}

const APPROVE_PATH = {
  review_1: '/approve',
  review_1_5: '/storyboard/approve',
  review_2: '/video/approve',
};

export async function taskApprove(videoId, step) {
  if (!APPROVE_PATH[step]) throw new Error(`unknown step: ${step}`);
  const path = `/api/v1/tasks/${videoId}${APPROVE_PATH[step]}`;
  return _request('POST', path, { jsonBody: {} });
}

export async function taskReject(videoId) {
  return _request('POST', `/api/v1/tasks/${videoId}/reject`, { jsonBody: {} });
}

export async function taskChangeProduct(videoId) {
  return _request('POST', `/api/v1/tasks/${videoId}/change-product`, { jsonBody: {} });
}

export async function taskChangeVideo(videoId) {
  return _request('POST', `/api/v1/tasks/${videoId}/change-video`, { jsonBody: {} });
}

export async function taskStoryboardRedo(videoId) {
  return _request('POST', `/api/v1/tasks/${videoId}/storyboard/redo`, { jsonBody: {} });
}

export async function taskVideoRedo(videoId) {
  return _request('POST', `/api/v1/tasks/${videoId}/video/redo`, { jsonBody: {} });
}

// ========== 事件接口 ==========
export async function eventsPending() {
  return _request('GET', '/api/v1/events/pending', { timeoutMs: 30000 });
}

export async function eventAck(eventId) {
  return _request('POST', `/api/v1/events/${eventId}/ack`, { timeoutMs: 30000 });
}

// ========== 数字人接口 ==========
export async function personaCreate(description = null) {
  const body = {};
  if (description) body.description = description;
  return _request('POST', '/api/v1/persona/create', { jsonBody: body, timeoutMs: 180000 });
}

export async function personaConfirm(personaId = null) {
  const body = {};
  if (personaId) body.persona_id = personaId;
  return _request('POST', '/api/v1/persona/confirm', { jsonBody: body, timeoutMs: 30000 });
}

export async function personaSwitch(personaId) {
  return _request('POST', '/api/v1/persona/switch', { jsonBody: { persona_id: personaId } });
}

export async function personaList() {
  return _request('GET', '/api/v1/persona/list', { timeoutMs: 30000 });
}

export async function personaActive() {
  return _request('GET', '/api/v1/persona/active', { timeoutMs: 30000 });
}
