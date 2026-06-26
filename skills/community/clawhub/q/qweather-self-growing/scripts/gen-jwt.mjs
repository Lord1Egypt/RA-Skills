#!/usr/bin/env node
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { createPrivateKey, sign } from 'crypto';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const localDir = resolve(__dirname, '../local');
const localConfigPath = resolve(localDir, 'qweather.json');
const cachePath = resolve(localDir, 'jwt-cache.json');

function loadConfig() {
  const env = {
    kid: process.env.QWEATHER_KID,
    projectId: process.env.QWEATHER_PROJECT_ID,
    privateKeyPath: process.env.QWEATHER_PRIVATE_KEY_PATH,
    apiHost: process.env.QWEATHER_API_HOST,
  };

  if (env.kid && env.projectId && env.privateKeyPath && env.apiHost) return env;

  if (existsSync(localConfigPath)) {
    const local = JSON.parse(readFileSync(localConfigPath, 'utf8'));
    return {
      kid: env.kid || local.kid,
      projectId: env.projectId || local.projectId,
      privateKeyPath: env.privateKeyPath || local.privateKeyPath,
      apiHost: env.apiHost || local.apiHost,
    };
  }

  throw new Error(
    'Missing QWeather config. Set QWEATHER_KID, QWEATHER_PROJECT_ID, QWEATHER_PRIVATE_KEY_PATH, QWEATHER_API_HOST env vars, or create local/qweather.json'
  );
}

function base64url(buf) {
  return Buffer.from(buf).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
}

function tryCache() {
  if (!existsSync(cachePath)) return null;
  try {
    const cache = JSON.parse(readFileSync(cachePath, 'utf8'));
    const now = Math.floor(Date.now() / 1000);
    // 还剩 60 秒以上才复用
    if (cache.exp && cache.exp - now > 60 && cache.token) return cache.token;
  } catch {}
  return null;
}

function writeCache(token, exp) {
  try {
    writeFileSync(cachePath, JSON.stringify({ token, exp }), 'utf8');
  } catch {}
}

export function genJwt(opts = {}) {
  if (!opts.skipCache) {
    const cached = tryCache();
    if (cached) return cached;
  }

  const cfg = loadConfig();
  const privateKey = createPrivateKey(readFileSync(cfg.privateKeyPath));
  const now = Math.floor(Date.now() / 1000) - 30;
  const exp = now + 3600; // 1 小时有效期
  const header = base64url(JSON.stringify({ alg: 'EdDSA', kid: cfg.kid }));
  const payload = base64url(JSON.stringify({ sub: cfg.projectId, iat: now, exp }));
  const data = `${header}.${payload}`;
  const sig = sign(null, Buffer.from(data), privateKey);
  const token = `${data}.${base64url(sig)}`;

  writeCache(token, exp);
  return token;
}

export function getApiHost() {
  const cfg = loadConfig();
  if (!cfg.apiHost) throw new Error('Missing apiHost in config. Set QWEATHER_API_HOST or add apiHost to local/qweather.json');
  return cfg.apiHost;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const arg = process.argv[2];
  if (arg === '--host') {
    console.log(getApiHost());
  } else {
    console.log(genJwt());
  }
}
