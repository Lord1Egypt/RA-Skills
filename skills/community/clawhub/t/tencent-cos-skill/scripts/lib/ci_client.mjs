#!/usr/bin/env node
/**
 * Minimal COS/CI XML client for the unified Tencent Cloud COS Skill runtime.
 *
 * 数据万象（CI）数据集相关接口（如 DatasetSimpleQuery）本质是挂在桶 CI 域名
 * <bucket>.ci.<region>.myqcloud.com 下的 COS 风格子资源，复用同一套 COS XML 签名。
 * 本模块提供通用签名请求原语 cosRequest，供 CI 查询与生命周期模块调用。
 *
 * Auth: 优先使用运行时 TENCENTCLOUD_*，否则使用 TENCENT_COS_*。
 * KIKI=1 仅控制严格模式下的功能隐藏，不参与凭证选择。
 * 提供 COS 签名请求原语；具体 HTTP 方法及安全限制由上层业务模块控制。
 */

import crypto from 'node:crypto';
import { assertCiActivationRequestAllowed } from './ci_activation.mjs';
import { existsSync, readFileSync } from 'node:fs';
import os from 'node:os';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

export const DEFAULT_SERVICE_HOST = 'service.cos.myqcloud.com';
export const STRICT_HIDDEN_ACTIONS = Object.freeze([
  'delete',
  'delete-multiple',
  'delete-file-meta-index',
  'delete-ai-process-bucket',
  'delete-async-image-process-bucket',
  'delete-ci-bucket',
  'delete-doc-process-bucket',
  'delete-media-bucket',
  'delete-asr-bucket',
  'delete-file-process-bucket',
  'encrypt-env',
  'decrypt-env',
]);

const skillRoot = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const envPath = resolve(skillRoot, '.env');
const envEncPath = resolve(skillRoot, '.env.enc');
let externalEnvLoaded = false;
let credentialSource = 'env';

export function isStrictMode(env = process.env) {
  return String(env.KIKI || '').trim() === '1';
}

export function getRuntimeMode(env = process.env) {
  return isStrictMode(env) ? 'strict' : 'public';
}

export function isActionHiddenInStrictMode(action) {
  return STRICT_HIDDEN_ACTIONS.includes(action)
    || /^delete(?:-|$)/i.test(String(action || ''));
}

export function getHiddenActions(env = process.env, actions = []) {
  if (!isStrictMode(env)) return [];
  return [...new Set([
    ...STRICT_HIDDEN_ACTIONS,
    ...actions.filter(isActionHiddenInStrictMode),
  ])];
}

export function assertActionAllowed(action, env = process.env, options = {}) {
  const strictMode = isStrictMode(env);
  if (
    strictMode
    && isActionHiddenInStrictMode(action)
  ) {
    const err = new Error(`action ${action} is hidden in strict mode`);
    err.code = 'ActionDenied';
    throw err;
  }

  const method = String(options.method || '').trim().toUpperCase();
  if (strictMode && method === 'DELETE') {
    const err = new Error('DELETE requests are not allowed in strict mode');
    err.code = 'ActionDenied';
    throw err;
  }
}

function deriveEnvKey() {
  const seed = `${os.hostname()}:${os.userInfo().username}:${skillRoot}`;
  return crypto.createHash('sha256').update(seed).digest();
}

export function encryptEnvBuffer(plaintext) {
  const iv = crypto.randomBytes(12);
  const cipher = crypto.createCipheriv('aes-256-gcm', deriveEnvKey(), iv);
  const encrypted = Buffer.concat([cipher.update(plaintext, 'utf-8'), cipher.final()]);
  return Buffer.concat([iv, cipher.getAuthTag(), encrypted]);
}

export function decryptEnvBuffer(encBuffer) {
  const iv = encBuffer.subarray(0, 12);
  const authTag = encBuffer.subarray(12, 28);
  const ciphertext = encBuffer.subarray(28);
  const decipher = crypto.createDecipheriv('aes-256-gcm', deriveEnvKey(), iv);
  decipher.setAuthTag(authTag);
  return decipher.update(ciphertext, undefined, 'utf-8') + decipher.final('utf-8');
}

function parseEnvContent(content, env) {
  content.split('\n').forEach(line => {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) {
      return;
    }
    const eqIndex = trimmed.indexOf('=');
    if (eqIndex === -1) {
      return;
    }
    const key = trimmed.slice(0, eqIndex).trim();
    let value = trimmed.slice(eqIndex + 1).trim();
    if (
      (value.startsWith('"') && value.endsWith('"'))
      || (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    if (!env[key]) {
      env[key] = value;
    }
  });
}

function loadExternalCredentialFiles(env) {
  if (externalEnvLoaded) {
    return;
  }
  externalEnvLoaded = true;

  if (existsSync(envEncPath)) {
    try {
      parseEnvContent(decryptEnvBuffer(readFileSync(envEncPath)), env);
      credentialSource = 'env.enc';
      return;
    } catch {
      credentialSource = 'env';
    }
  }
  if (existsSync(envPath)) {
    parseEnvContent(readFileSync(envPath, 'utf-8'), env);
    credentialSource = 'env';
  }
}

export function getRuntimeCredentials(env = process.env) {
  if (env === process.env) {
    loadExternalCredentialFiles(env);
  }

  const hasRuntimeCredentials = !!(
    env.TENCENTCLOUD_SECRET_ID
    || env.TENCENTCLOUD_SECRET_KEY
    || env.TENCENTCLOUD_TOKEN
  );
  if (hasRuntimeCredentials) {
    return {
      secretId: env.TENCENTCLOUD_SECRET_ID || '',
      secretKey: env.TENCENTCLOUD_SECRET_KEY || '',
      token: env.TENCENTCLOUD_TOKEN || '',
      uin: env.TENCENTCLOUD_UIN || '',
      ownerUin: env.TENCENTCLOUD_OWNER_UIN || env.TENCENTCLOUD_UIN || '',
      source: 'runtime',
    };
  }

  return {
    secretId: env.TENCENT_COS_SECRET_ID || '',
    secretKey: env.TENCENT_COS_SECRET_KEY || '',
    token: env.TENCENT_COS_TOKEN || '',
    uin: '',
    ownerUin: '',
    source: credentialSource,
  };
}

export function assertCredentials(creds) {
  const prefix = creds.source === 'runtime' ? 'TENCENTCLOUD' : 'TENCENT_COS';
  const missing = [];
  if (!creds.secretId) {
    missing.push(`${prefix}_SECRET_ID`);
  }
  if (!creds.secretKey) {
    missing.push(`${prefix}_SECRET_KEY`);
  }
  if (missing.length > 0) {
    const err = new Error(`missing credentials: ${missing.join(', ')}`);
    err.code = 'MissingCredentials';
    throw err;
  }
}

function hmacSha1(key, data) {
  return crypto.createHmac("sha1", key).update(data).digest("hex");
}

function sha1(data) {
  return crypto.createHash("sha1").update(data).digest("hex");
}

function camSafeUrlEncode(value) {
  return encodeURIComponent(value)
    .replace(/[!'()*]/g, (char) => `%${char.charCodeAt(0).toString(16).toUpperCase()}`);
}

/**
 * COS 签名串拼接：key 需 lowercase（COS 规范），value 保留原始大小写。
 * 注意：不能对 value 做 lowercase，否则含大写的参数值（如 ci-process=AIImageAnalysis、
 * type=ImageLabels、nexttoken/prefix 等）签名串与实际 URL 不一致 → SignatureDoesNotMatch。
 */
function objectToSignString(obj) {
  return Object.keys(obj)
    .sort()
    .map((key) => `${camSafeUrlEncode(key).toLowerCase()}=${camSafeUrlEncode(String(obj[key]))}`)
    .join("&");
}

export function createCosAuthorization({ secretId, secretKey, method, pathname, query = {}, headers = {} }) {
  const now = Math.floor(Date.now() / 1000) - 1;
  const keyTime = `${now};${now + 900}`;
  const lowerHeaders = {};

  for (const [key, value] of Object.entries(headers)) {
    lowerHeaders[key.toLowerCase()] = String(value);
  }

  const signKey = hmacSha1(secretKey, keyTime);
  const formatString = [
    method.toLowerCase(),
    pathname,
    objectToSignString(query),
    objectToSignString(lowerHeaders),
    "",
  ].join("\n");
  const stringToSign = ["sha1", keyTime, sha1(formatString), ""].join("\n");
  const signature = hmacSha1(signKey, stringToSign);

  return [
    "q-sign-algorithm=sha1",
    `q-ak=${secretId}`,
    `q-sign-time=${keyTime}`,
    `q-key-time=${keyTime}`,
    `q-header-list=${Object.keys(lowerHeaders).sort().join(";")}`,
    `q-url-param-list=${Object.keys(query).map(key => key.toLowerCase()).sort().join(";")}`,
    `q-signature=${signature}`,
  ].join("&");
}

/** COS 桶域名（用于图片分析、EXIF 等桶级接口） */
export function bucketHost(bucket, region) {
  return `${bucket}.cos.${region}.myqcloud.com`;
}

/** CI 数据洞察域名（DatasetSimpleQuery 等数据集接口挂在此处） */
export function ciHost(bucket, region) {
  return `${bucket}.ci.${region}.myqcloud.com`;
}

/** 账号级 CI 域名（ListDatasets 等挂在账号 AppId 下，而非某个桶） */
export function ciAccountHost(appId, region) {
  return `${appId}.ci.${region}.myqcloud.com`;
}

function buildQueryString(query = {}) {
  const keys = Object.keys(query).sort();
  if (!keys.length) return "";
  return keys
    .map((key) => {
      const value = query[key];
      if (value === "" || value == null) return encodeURIComponent(key);
      return `${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`;
    })
    .join("&");
}

function getBodySnippet(text, max = 4000) {
  if (!text) return "";
  return text.length > max ? `${text.slice(0, max)}…` : text;
}

export function extractXmlTag(xml, tag) {
  if (!xml) return null;
  const re = new RegExp(`<${tag}>([\\s\\S]*?)</${tag}>`, 'i');
  const match = xml.match(re);
  return match ? match[1].trim() : null;
}

export function parseCosErrorXml(xml) {
  return {
    code: extractXmlTag(xml, 'Code'),
    message: extractXmlTag(xml, 'Message'),
    resource: extractXmlTag(xml, 'Resource'),
    requestId: extractXmlTag(xml, 'RequestId'),
    traceId: extractXmlTag(xml, 'TraceId'),
  };
}

export function parseCiRawError(raw) {
  if (raw?.timedOut) {
    return {
      code: raw.errorCode || 'Timeout',
      message: raw.errorMessage || 'request timed out',
      requestId: raw.requestId || null,
    };
  }
  if (raw?.body?.trim().startsWith('<')) {
    return parseCosErrorXml(raw.body);
  }
  let json = null;
  try {
    json = JSON.parse(String(raw?.body || ''));
  } catch {
    json = null;
  }
  return {
    code: json?.Code || json?.code || `HTTP_${raw?.status || 0}`,
    message: json?.Message || json?.message || raw?.bodySnippet || raw?.body || 'request failed',
    requestId: json?.RequestId || json?.requestId || raw?.requestId || null,
  };
}

export function summarizeCiRequest(raw) {
  return {
    method: raw.method,
    host: raw.host,
    pathname: raw.pathname,
    query: raw.query,
    status: raw.status,
    requestId: raw.requestId,
    elapsedMs: raw.elapsedMs,
  };
}

export function validateCosBucket(bucket) {
  if (!/^[a-z0-9][a-z0-9.-]*-[0-9]+$/i.test(String(bucket || ''))) {
    const error = new Error('invalid bucket; expected <BucketName-APPID>');
    error.code = 'InvalidArgs';
    throw error;
  }
}

export function validateCosRegion(region) {
  if (!/^[a-z0-9][a-z0-9-]*$/i.test(String(region || ''))) {
    const error = new Error('invalid region');
    error.code = 'InvalidArgs';
    throw error;
  }
}

export function validateCosHost(host) {
  const normalized = String(host || '').trim().toLowerCase();
  const serviceHost = normalized === DEFAULT_SERVICE_HOST;
  const regionalHost = /^(?:[a-z0-9][a-z0-9.-]*\.)?(?:ci|cos)\.[a-z0-9-]+\.myqcloud\.com$/.test(normalized);
  if (!serviceHost && !regionalHost) {
    const error = new Error('invalid COS/CI service host');
    error.code = 'InvalidArgs';
    throw error;
  }
}

/**
 * 通用 COS/CI 签名请求原语。
 * @param {object} opts
 * @param {string} opts.method  GET / HEAD / POST / PUT / DELETE
 * @param {string} opts.host    目标域名，如 <bucket>.ci.<region>.myqcloud.com
 * @param {string} [opts.pathname] 资源路径，默认 "/"
 * @param {object} [opts.query] 查询参数（子资源/分页等）
 * @param {object} opts.creds   getRuntimeCredentials() 返回值
 * @param {string|null} [opts.body] POST 请求体（JSON 字符串）
 * @param {object} [opts.extraHeaders] 透传到 fetch 的额外请求头（不计入签名，如 Accept）
 * @param {number} [opts.timeoutMs] 超时，默认 25000
 * @returns {Promise<object>} 结构化响应
 */
export async function cosRequest({
  method,
  host,
  pathname = "/",
  query = {},
  creds,
  body = null,
  extraHeaders = {},
  timeoutMs = 25000,
  activationConfirmation,
}) {
  assertActionAllowed('cos-request', process.env, { method });
  assertCiActivationRequestAllowed({ method, host, pathname, query, activationConfirmation });
  validateCosHost(host);
  assertCredentials(creds);

  const headers = { host };
  const authorization = createCosAuthorization({
    secretId: creds.secretId,
    secretKey: creds.secretKey,
    method,
    pathname,
    query,
    headers,
  });

  const qs = buildQueryString(query);
  const url = `https://${host}${pathname}${qs ? `?${qs}` : ""}`;

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  const started = Date.now();
  try {
    const response = await fetch(url, {
      method,
      headers: {
        Authorization: authorization,
        Host: host,
        ...(creds.token ? { "x-cos-security-token": creds.token } : {}),
        ...(body != null ? { "Content-Type": "application/json" } : {}),
        ...extraHeaders,
      },
      body,
      signal: controller.signal,
    });

    const text = method.toUpperCase() === "HEAD" ? "" : await response.text();
    const requestId =
      response.headers.get("x-cos-request-id") ||
      response.headers.get("x-cos-req-id") ||
      null;
    const traceId = response.headers.get("x-cos-trace-id") || null;

    return {
      ok: response.ok,
      status: response.status,
      timedOut: false,
      requestId,
      traceId,
      url,
      host,
      method: method.toUpperCase(),
      pathname,
      query,
      elapsedMs: Date.now() - started,
      contentType: response.headers.get("content-type"),
      body: text,
      bodySnippet: getBodySnippet(text),
    };
  } catch (error) {
    const aborted =
      (error && error.name === "AbortError") ||
      (error && /aborted|timeout/i.test(String(error.message || error)));
    if (aborted) {
      return {
        ok: false,
        status: 0,
        timedOut: true,
        error: "timeout",
        errorCode: "Timeout",
        errorMessage: `request timed out after ${timeoutMs}ms`,
        requestId: null,
        traceId: null,
        url,
        host,
        method: method.toUpperCase(),
        pathname,
        query,
        elapsedMs: Date.now() - started,
        contentType: null,
        body: "",
        bodySnippet: "",
      };
    }
    throw error;
  } finally {
    clearTimeout(timer);
  }
}

export function runtimeMeta() {
  const mode = getRuntimeMode();
  return {
    mode,
    hasWindow: typeof window !== 'undefined',
    hasProcess: typeof process !== 'undefined',
    nodeVersion: typeof process !== 'undefined' ? process.version : null,
    platform: typeof process !== 'undefined' ? process.platform : null,
    cwd: typeof process !== 'undefined' ? process.cwd() : null,
    envPresence: {
      KIKI: process.env.KIKI === '1',
      TENCENTCLOUD_SECRET_ID: Boolean(process.env.TENCENTCLOUD_SECRET_ID),
      TENCENTCLOUD_SECRET_KEY: Boolean(process.env.TENCENTCLOUD_SECRET_KEY),
      TENCENTCLOUD_TOKEN: Boolean(process.env.TENCENTCLOUD_TOKEN),
      TENCENT_COS_SECRET_ID: Boolean(process.env.TENCENT_COS_SECRET_ID),
      TENCENT_COS_SECRET_KEY: Boolean(process.env.TENCENT_COS_SECRET_KEY),
      TENCENT_COS_TOKEN: Boolean(process.env.TENCENT_COS_TOKEN),
    },
  };
}
