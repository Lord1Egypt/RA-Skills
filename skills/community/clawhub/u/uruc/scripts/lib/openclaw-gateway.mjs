import { chmodSync, existsSync, mkdirSync, readFileSync, writeFileSync } from 'fs';
import { createHash, createPrivateKey, createPublicKey, randomUUID, sign } from 'crypto';
import os from 'os';
import path from 'path';

const DEFAULT_OPENCLAW_GATEWAY_PORT = 18789;
const OPENCLAW_PROTOCOL_VERSION = 3;
const OPENCLAW_WRITE_SCOPE = 'operator.write';
const OPENCLAW_GATEWAY_CLIENT_ID = 'gateway-client';
const OPENCLAW_DEVICE_AUTH_FILE = 'device-auth.json';
const OPENCLAW_DEVICE_IDENTITY_FILE = 'device.json';
const ED25519_SPKI_PREFIX = Buffer.from('302a300506032b6570032100', 'hex');

export async function sendOpenClawSystemEventText(text, options = {}) {
  const target = options.target ?? resolveOpenClawGatewayTarget(options.env);
  if (!target.password && !target.token && !target.deviceToken && target.authMode !== 'none') {
    throw new Error(
      `缺少 OpenClaw Gateway 认证。请设置 OPENCLAW_GATEWAY_TOKEN，或在 ${target.configPath} 中提供 gateway.auth.token / device-auth token。`,
    );
  }

  const sessionKey = typeof options.sessionKey === 'string' && options.sessionKey.trim() !== ''
    ? options.sessionKey.trim()
    : 'main';
  const idempotencyKey = typeof options.idempotencyKey === 'string' && options.idempotencyKey.trim() !== ''
    ? options.idempotencyKey.trim()
    : null;
  if (!idempotencyKey) {
    throw new Error('chat.send requires idempotencyKey');
  }

  return await callOpenClawGateway('chat.send', {
    sessionKey,
    message: text,
    idempotencyKey,
  }, {
    ...target,
    timeoutMs: options.timeoutMs,
    clientName: options.clientName,
    clientDisplayName: options.clientDisplayName,
    clientVersion: options.clientVersion,
  });
}

export function resolveOpenClawGatewayTarget(env = process.env) {
  const { config, configPath } = readOpenClawConfig(env);
  const gateway = config?.gateway && typeof config.gateway === 'object' ? config.gateway : {};
  const auth = gateway.auth && typeof gateway.auth === 'object' ? gateway.auth : {};
  const port = normalizePort(firstDefined(env.OPENCLAW_GATEWAY_PORT, String(gateway.port ?? '')));
  const protocol = gateway.tls?.enabled === true ? 'wss' : 'ws';
  const url = firstDefined(env.OPENCLAW_GATEWAY_URL)
    ?? `${protocol}://127.0.0.1:${port ?? DEFAULT_OPENCLAW_GATEWAY_PORT}`;
  const deviceIdentity = readOpenClawDeviceIdentity(env);
  const deviceAuth = deviceIdentity ? readOpenClawDeviceAuth(env, deviceIdentity.deviceId, 'operator') : null;

  return {
    url,
    token: firstDefined(
      env.OPENCLAW_GATEWAY_TOKEN,
      env.CLAWDBOT_GATEWAY_TOKEN,
      typeof auth.token === 'string' ? auth.token : undefined,
    ),
    password: firstDefined(
      env.OPENCLAW_GATEWAY_PASSWORD,
      typeof auth.password === 'string' ? auth.password : undefined,
    ),
    deviceIdentity,
    deviceToken: firstDefined(
      env.OPENCLAW_GATEWAY_DEVICE_TOKEN,
      typeof deviceAuth?.token === 'string' ? deviceAuth.token : undefined,
    ),
    authMode: typeof auth.mode === 'string' ? auth.mode : 'token',
    configPath,
  };
}

export function readOpenClawConfig(env = process.env) {
  const configPath = resolveOpenClawConfigPath(env);
  if (!existsSync(configPath)) {
    return { config: null, configPath };
  }

  const raw = readFileSync(configPath, 'utf8');
  try {
    return {
      config: JSON.parse(raw),
      configPath,
    };
  } catch (error) {
    throw new Error(`无法解析 OpenClaw 配置 ${configPath}: ${error instanceof Error ? error.message : String(error)}`);
  }
}

export function resolveOpenClawConfigPath(env = process.env) {
  const explicit = firstDefined(env.OPENCLAW_CONFIG_PATH, env.CLAWDBOT_CONFIG_PATH);
  if (explicit) return resolveUserPath(explicit, resolveHomeDir(env));
  return path.join(resolveOpenClawStateDir(env), 'openclaw.json');
}

export function resolveOpenClawStateDir(env = process.env) {
  const explicit = firstDefined(env.OPENCLAW_STATE_DIR, env.CLAWDBOT_STATE_DIR);
  if (explicit) return resolveUserPath(explicit, resolveHomeDir(env));
  return path.join(resolveHomeDir(env), '.openclaw');
}

export async function callOpenClawGateway(method, params, options = {}) {
  const timeoutMs = normalizeTimeout(options.timeoutMs);
  const token = typeof options.token === 'string' && options.token.trim() !== '' ? options.token.trim() : undefined;
  const password = typeof options.password === 'string' && options.password.trim() !== '' ? options.password.trim() : undefined;
  const deviceToken = typeof options.deviceToken === 'string' && options.deviceToken.trim() !== '' ? options.deviceToken.trim() : undefined;
  const deviceIdentity = normalizeDeviceIdentity(options.deviceIdentity);
  const url = typeof options.url === 'string' && options.url.trim() !== '' ? options.url.trim() : null;
  if (!url) {
    throw new Error('缺少 OpenClaw Gateway URL');
  }

  return await new Promise((resolve, reject) => {
    const ws = new WebSocket(url);
    const connectRequestId = randomUUID();
    const methodRequestId = randomUUID();
    let settled = false;
    let connectSent = false;
    let methodSent = false;

    const finish = (error, value) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      try {
        if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
          ws.close();
        }
      } catch {
        // noop
      }

      if (error) {
        reject(error);
        return;
      }
      resolve(value);
    };

    const sendRequest = (id, requestMethod, requestParams) => {
      ws.send(JSON.stringify({
        type: 'req',
        id,
        method: requestMethod,
        params: requestParams,
      }));
    };

    const timer = setTimeout(() => {
      finish(new Error(`OpenClaw Gateway 请求超时: ${method} (${timeoutMs}ms)`));
    }, timeoutMs);

    ws.onmessage = (event) => {
      let message;
      try {
        message = JSON.parse(String(event.data));
      } catch {
        return;
      }

      if (message?.event === 'connect.challenge') {
        if (connectSent) return;
        const nonce = typeof message.payload?.nonce === 'string' ? message.payload.nonce.trim() : '';
        if (!nonce) {
          finish(new Error('OpenClaw Gateway 缺少 connect challenge nonce'));
          return;
        }
        connectSent = true;
        sendRequest(connectRequestId, 'connect', buildConnectParams({
          token,
          password,
          deviceToken,
          deviceIdentity,
          nonce,
          clientDisplayName: options.clientDisplayName,
          clientVersion: options.clientVersion,
        }));
        return;
      }

      if (message?.type !== 'res') return;

      if (message.id === connectRequestId) {
        if (!message.ok) {
          finish(new Error(message.error?.message ?? 'OpenClaw Gateway connect 失败'));
          return;
        }
        storeIssuedDeviceToken(message.payload?.auth, deviceIdentity, options.env);
        if (methodSent) return;
        methodSent = true;
        sendRequest(methodRequestId, method, params);
        return;
      }

      if (message.id === methodRequestId) {
        if (!message.ok) {
          finish(new Error(message.error?.message ?? `OpenClaw Gateway ${method} 失败`));
          return;
        }
        finish(undefined, message.payload);
      }
    };

    ws.onerror = (event) => {
      const message = event?.error instanceof Error ? event.error.message : 'WebSocket 连接失败';
      finish(new Error(`OpenClaw Gateway 连接失败: ${message}`));
    };

    ws.onclose = (event) => {
      if (settled) return;
      finish(new Error(formatCloseError(event.code, event.reason)));
    };
  });
}

function buildConnectParams({ token, password, deviceToken, deviceIdentity, nonce, clientDisplayName, clientVersion }) {
  const auth = token || password || deviceToken ? {
    ...(token ? { token } : {}),
    ...(password ? { password } : {}),
    ...(deviceToken ? { deviceToken } : {}),
  } : undefined;
  const signedAt = Date.now();
  const platform = process.platform;
  const signatureToken = token ?? deviceToken ?? undefined;

  return {
    minProtocol: OPENCLAW_PROTOCOL_VERSION,
    maxProtocol: OPENCLAW_PROTOCOL_VERSION,
    client: {
      id: OPENCLAW_GATEWAY_CLIENT_ID,
      displayName: clientDisplayName ?? 'URUC Agent Bridge',
      version: clientVersion ?? '0.1.0',
      platform,
      mode: 'backend',
    },
    caps: [],
    auth,
    role: 'operator',
    scopes: [OPENCLAW_WRITE_SCOPE],
    device: deviceIdentity ? {
      id: deviceIdentity.deviceId,
      publicKey: publicKeyRawBase64UrlFromPem(deviceIdentity.publicKeyPem),
      signature: signDevicePayload(
        deviceIdentity.privateKeyPem,
        buildDeviceAuthPayloadV3({
          deviceId: deviceIdentity.deviceId,
          clientId: OPENCLAW_GATEWAY_CLIENT_ID,
          clientMode: 'backend',
          role: 'operator',
          scopes: [OPENCLAW_WRITE_SCOPE],
          signedAtMs: signedAt,
          token: signatureToken ?? null,
          nonce,
          platform,
          deviceFamily: '',
        }),
      ),
      signedAt,
      nonce,
    } : undefined,
    pathEnv: process.env.PATH,
  };
}

function readOpenClawDeviceIdentity(env = process.env) {
  const identityPath = resolveOpenClawDeviceIdentityPath(env);
  if (!existsSync(identityPath)) {
    return null;
  }

  try {
    const raw = readFileSync(identityPath, 'utf8');
    const parsed = JSON.parse(raw);
    if (parsed?.version !== 1) return null;
    if (typeof parsed.deviceId !== 'string' || parsed.deviceId.trim() === '') return null;
    if (typeof parsed.publicKeyPem !== 'string' || parsed.publicKeyPem.trim() === '') return null;
    if (typeof parsed.privateKeyPem !== 'string' || parsed.privateKeyPem.trim() === '') return null;
    const derivedId = fingerprintPublicKey(parsed.publicKeyPem);
    return {
      deviceId: derivedId || parsed.deviceId.trim(),
      publicKeyPem: parsed.publicKeyPem,
      privateKeyPem: parsed.privateKeyPem,
    };
  } catch {
    return null;
  }
}

function readOpenClawDeviceAuth(env, deviceId, role) {
  const authPath = resolveOpenClawDeviceAuthPath(env);
  if (!existsSync(authPath)) {
    return null;
  }

  try {
    const raw = readFileSync(authPath, 'utf8');
    const parsed = JSON.parse(raw);
    if (parsed?.version !== 1) return null;
    if (parsed.deviceId !== deviceId) return null;
    const entry = parsed.tokens?.[role];
    if (!entry || typeof entry.token !== 'string' || entry.token.trim() === '') {
      return null;
    }
    return {
      token: entry.token.trim(),
      role,
      scopes: Array.isArray(entry.scopes) ? entry.scopes.filter((scope) => typeof scope === 'string') : [],
    };
  } catch {
    return null;
  }
}

function storeIssuedDeviceToken(auth, deviceIdentity, env = process.env) {
  if (!deviceIdentity) return;
  if (!auth || typeof auth !== 'object') return;
  if (typeof auth.deviceToken !== 'string' || auth.deviceToken.trim() === '') return;

  const role = typeof auth.role === 'string' && auth.role.trim() !== '' ? auth.role.trim() : 'operator';
  const scopes = Array.isArray(auth.scopes) ? auth.scopes.filter((scope) => typeof scope === 'string') : [];
  const authPath = resolveOpenClawDeviceAuthPath(env);
  let store = null;

  try {
    if (existsSync(authPath)) {
      store = JSON.parse(readFileSync(authPath, 'utf8'));
    }
  } catch {
    store = null;
  }

  const next = {
    version: 1,
    deviceId: deviceIdentity.deviceId,
    tokens: store && typeof store === 'object' && store.deviceId === deviceIdentity.deviceId && store.tokens && typeof store.tokens === 'object'
      ? { ...store.tokens }
      : {},
  };
  next.tokens[role] = {
    token: auth.deviceToken.trim(),
    role,
    scopes,
    updatedAtMs: Date.now(),
  };

  mkdirSync(path.dirname(authPath), { recursive: true });
  writeFileSync(authPath, `${JSON.stringify(next, null, 2)}\n`, { mode: 0o600 });
  try {
    chmodSync(authPath, 0o600);
  } catch {
    // noop
  }
}

function resolveOpenClawDeviceIdentityPath(env = process.env) {
  return path.join(resolveOpenClawStateDir(env), 'identity', OPENCLAW_DEVICE_IDENTITY_FILE);
}

function resolveOpenClawDeviceAuthPath(env = process.env) {
  return path.join(resolveOpenClawStateDir(env), 'identity', OPENCLAW_DEVICE_AUTH_FILE);
}

function normalizeDeviceIdentity(deviceIdentity) {
  if (!deviceIdentity || typeof deviceIdentity !== 'object') return null;
  if (typeof deviceIdentity.deviceId !== 'string' || deviceIdentity.deviceId.trim() === '') return null;
  if (typeof deviceIdentity.publicKeyPem !== 'string' || deviceIdentity.publicKeyPem.trim() === '') return null;
  if (typeof deviceIdentity.privateKeyPem !== 'string' || deviceIdentity.privateKeyPem.trim() === '') return null;
  return deviceIdentity;
}

function buildDeviceAuthPayloadV3(params) {
  const scopes = params.scopes.join(',');
  const token = params.token ?? '';
  const platform = normalizeDeviceMetadata(params.platform);
  const deviceFamily = normalizeDeviceMetadata(params.deviceFamily);
  return [
    'v3',
    params.deviceId,
    params.clientId,
    params.clientMode,
    params.role,
    scopes,
    String(params.signedAtMs),
    token,
    params.nonce,
    platform,
    deviceFamily,
  ].join('|');
}

function normalizeDeviceMetadata(value) {
  return typeof value === 'string' ? value.trim().normalize('NFKD').replace(/\p{M}/gu, '').toLowerCase() : '';
}

function signDevicePayload(privateKeyPem, payload) {
  return base64UrlEncode(sign(null, Buffer.from(payload, 'utf8'), createPrivateKey(privateKeyPem)));
}

function publicKeyRawBase64UrlFromPem(publicKeyPem) {
  return base64UrlEncode(derivePublicKeyRaw(publicKeyPem));
}

function fingerprintPublicKey(publicKeyPem) {
  const raw = derivePublicKeyRaw(publicKeyPem);
  return createHash('sha256').update(raw).digest('hex');
}

function derivePublicKeyRaw(publicKeyPem) {
  const spki = createPublicKey(publicKeyPem).export({
    type: 'spki',
    format: 'der',
  });
  if (
    spki.length === ED25519_SPKI_PREFIX.length + 32
    && spki.subarray(0, ED25519_SPKI_PREFIX.length).equals(ED25519_SPKI_PREFIX)
  ) {
    return spki.subarray(ED25519_SPKI_PREFIX.length);
  }
  return spki;
}

function base64UrlEncode(buffer) {
  return buffer.toString('base64').replaceAll('+', '-').replaceAll('/', '_').replace(/=+$/g, '');
}

function formatCloseError(code, reason) {
  const suffix = typeof reason === 'string' && reason.trim() !== '' ? ` ${reason.trim()}` : '';
  return `OpenClaw Gateway 连接已关闭 (${code})${suffix}`;
}

function normalizeTimeout(value) {
  const numberValue = typeof value === 'number' ? value : Number(value);
  if (!Number.isFinite(numberValue) || numberValue <= 0) return 10_000;
  return Math.max(1000, Math.floor(numberValue));
}

function normalizePort(value) {
  const numberValue = Number(value);
  if (!Number.isInteger(numberValue) || numberValue <= 0) return null;
  return numberValue;
}

function resolveHomeDir(env) {
  const home = firstDefined(env.HOME);
  if (home) return resolveUserPath(home, os.homedir());
  return os.homedir();
}

function resolveUserPath(value, homeDir) {
  if (value.startsWith('~/')) return path.join(homeDir, value.slice(2));
  return path.resolve(value);
}

function firstDefined(...values) {
  for (const value of values) {
    if (typeof value === 'string' && value.trim() !== '') return value.trim();
  }
  return undefined;
}
