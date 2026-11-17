'use strict';

// 扩展提供方（provider）装载器 v1：外部子进程 + stdin/stdout JSON。
// 设计：docs/路线B-P1-接口预留设计-2026-09-28.md（根仓库）；对外协议：references/provider-protocol.md。
// 零依赖；未配置 / 任何失败都 fail-open 回开源基线，不阻断调用方。

const fs = require('fs');
const os = require('os');
const path = require('path');
const crypto = require('crypto');
const { spawnSync } = require('child_process');

const SCHEMA = 1;
const DEFAULT_TIMEOUT_MS = 600;
const MAX_TIMEOUT_MS = 5000;
const MIN_TIMEOUT_MS = 50;
const MAX_STDOUT_BYTES = 256 * 1024;
const KNOWN_CAPABILITIES = ['o1.route', 'm1.adjudicate', 'memory.hook', 'context.paging'];

function providerHome() {
  const fromEnv = process.env.YOTTA_PROVIDER_HOME;
  if (fromEnv && String(fromEnv).trim()) return path.resolve(String(fromEnv).trim());
  return path.join(os.homedir(), '.yottameta');
}

function configPath() {
  return path.join(providerHome(), 'provider.json');
}

function validateProvider(item) {
  if (!item || typeof item !== 'object' || Array.isArray(item)) return 'provider 条目必须是对象';
  if (!item.id || typeof item.id !== 'string') return 'provider 缺 id';
  if (!Array.isArray(item.capabilities) || !item.capabilities.length) return 'provider ' + item.id + ' 缺 capabilities';
  for (const capability of item.capabilities) {
    if (KNOWN_CAPABILITIES.indexOf(capability) === -1) return 'provider ' + item.id + ' 含未知 capability：' + capability;
  }
  if (!Array.isArray(item.command) || !item.command.length) return 'provider ' + item.id + ' 的 command 必须是数组';
  for (const part of item.command) {
    if (typeof part !== 'string' || !part) return 'provider ' + item.id + ' 的 command 含非法参数';
    if (part.indexOf('\0') !== -1) return 'provider ' + item.id + ' 的 command 含非法字符';
  }
  if (item.timeout_ms !== undefined && (!Number.isFinite(item.timeout_ms) || item.timeout_ms <= 0)) {
    return 'provider ' + item.id + ' 的 timeout_ms 非法';
  }
  return '';
}

function normalizeProvider(item) {
  return {
    id: item.id,
    version: typeof item.version === 'string' ? item.version : '',
    capabilities: item.capabilities.slice(),
    command: item.command.slice(),
    timeout_ms: Math.min(MAX_TIMEOUT_MS, Math.max(MIN_TIMEOUT_MS, Math.round(item.timeout_ms || DEFAULT_TIMEOUT_MS))),
  };
}

function readConfig() {
  const file = configPath();
  if (!fs.existsSync(file)) return { status: 'not_installed', providers: [], error: '' };
  let raw;
  try {
    raw = JSON.parse(fs.readFileSync(file, 'utf8'));
  } catch (e) {
    return { status: 'error', providers: [], error: 'provider.json 解析失败：' + e.message };
  }
  if (!raw || typeof raw !== 'object' || Array.isArray(raw)) {
    return { status: 'error', providers: [], error: 'provider.json 必须是对象' };
  }
  if (raw.schema !== SCHEMA) {
    return { status: 'error', providers: [], error: 'provider.json schema 不支持：' + String(raw.schema) };
  }
  if (!Array.isArray(raw.providers)) {
    return { status: 'error', providers: [], error: 'provider.json providers 必须是数组' };
  }
  const providers = [];
  for (const item of raw.providers) {
    const invalid = validateProvider(item);
    if (invalid) return { status: 'error', providers: [], error: invalid };
    providers.push(normalizeProvider(item));
  }
  return { status: 'ok', providers, error: '' };
}

function pickProvider(config, capability) {
  if (!config || config.status !== 'ok') return null;
  for (const item of config.providers) {
    if (item.capabilities.indexOf(capability) !== -1) return item;
  }
  return null;
}

function minimalEnv() {
  const keep = [
    'PATH', 'Path', 'PATHEXT', 'SystemRoot', 'windir', 'COMSPEC', 'ComSpec',
    'TEMP', 'TMP', 'HOME', 'USERPROFILE', 'LANG', 'LC_ALL',
    'YOTTA_LICENSE_HOME', 'YOTTA_LICENSE_KEYS_DIR', 'YOTTA_LICENSE_BASE_URL', 'YOTTA_LICENSE_SERVER_ID',
  ];
  const env = {};
  for (const key of keep) {
    if (process.env[key] !== undefined) env[key] = process.env[key];
  }
  env.YOTTA_PROVIDER_HOME = providerHome();
  return env;
}

function requestId() {
  try {
    if (typeof crypto.randomUUID === 'function') return crypto.randomUUID();
  } catch (e) {
    // 回退到随机 hex
  }
  return crypto.randomBytes(16).toString('hex');
}

function invokeProvider(provider, capability, payload) {
  const started = Date.now();
  const request = {
    schema: SCHEMA,
    capability,
    request_id: requestId(),
    payload: payload || {},
  };
  let proc;
  try {
    proc = spawnSync(provider.command[0], provider.command.slice(1), {
      input: JSON.stringify(request),
      encoding: 'utf8',
      timeout: provider.timeout_ms,
      maxBuffer: MAX_STDOUT_BYTES,
      shell: false,
      cwd: providerHome(),
      env: minimalEnv(),
      windowsHide: true,
    });
  } catch (e) {
    return {
      status: 'error',
      provider_id: provider.id,
      duration_ms: Date.now() - started,
      note: 'provider 启动失败：' + e.message,
    };
  }
  const duration = Date.now() - started;
  if (proc.error) {
    const code = proc.error.code || '';
    const timedOut = code === 'ETIMEDOUT';
    const oversize = code === 'ERR_CHILD_PROCESS_STDIO_MAXBUFFER';
    return {
      status: timedOut ? 'timeout' : 'error',
      provider_id: provider.id,
      duration_ms: duration,
      note: timedOut
        ? 'provider 超时'
        : (oversize
          ? 'provider 输出超过 ' + MAX_STDOUT_BYTES + ' 字节'
          : 'provider 执行失败：' + (code || proc.error.message || 'unknown')),
    };
  }
  if (proc.status !== 0) {
    return {
      status: 'error',
      provider_id: provider.id,
      duration_ms: duration,
      note: 'provider 退出码非 0：' + proc.status,
    };
  }
  let response;
  try {
    response = JSON.parse(String(proc.stdout || '').trim() || '{}');
  } catch (e) {
    return { status: 'invalid_output', provider_id: provider.id, duration_ms: duration, note: 'provider 输出不是 JSON' };
  }
  if (!response || typeof response !== 'object' || Array.isArray(response)) {
    return { status: 'invalid_output', provider_id: provider.id, duration_ms: duration, note: 'provider 输出不是对象' };
  }
  if (response.ok === false) {
    const code = typeof response.code === 'string' && response.code ? response.code : 'provider_error';
    return {
      status: code === 'license_required' ? 'license_required' : 'error',
      provider_id: provider.id,
      code,
      message: typeof response.message === 'string' ? response.message : '',
      duration_ms: duration,
      note: typeof response.message === 'string' ? response.message : code,
    };
  }
  if (response.ok !== true) {
    return { status: 'invalid_output', provider_id: provider.id, duration_ms: duration, note: 'provider 响应缺 ok 字段' };
  }
  return {
    status: 'active',
    provider_id: provider.id,
    data: response.data,
    duration_ms: duration,
    bytes_out: Buffer.byteLength(String(proc.stdout || ''), 'utf8'),
    note: '',
  };
}

function appendAudit(entry) {
  try {
    const home = providerHome();
    fs.mkdirSync(home, { recursive: true });
    fs.appendFileSync(
      path.join(home, 'provider-audit.jsonl'),
      JSON.stringify(Object.assign({ schema: SCHEMA, ts: new Date().toISOString() }, entry)) + '\n',
      'utf8',
    );
  } catch (e) {
    // 审计失败不影响调用
  }
}

function runCapability(capability, payload) {
  const config = readConfig();
  if (config.status === 'not_installed') {
    return { status: 'not_installed', provider_id: '', note: '未配置扩展提供方' };
  }
  if (config.status === 'error') {
    return { status: 'error', provider_id: '', note: config.error };
  }
  const provider = pickProvider(config, capability);
  if (!provider) {
    return { status: 'not_installed', provider_id: '', note: '未配置声明 ' + capability + ' 的提供方' };
  }
  const result = invokeProvider(provider, capability, payload);
  appendAudit({
    capability,
    provider_id: result.provider_id,
    status: result.status,
    duration_ms: result.duration_ms,
    bytes_out: result.bytes_out || 0,
  });
  return result;
}

module.exports = {
  SCHEMA,
  DEFAULT_TIMEOUT_MS,
  MAX_TIMEOUT_MS,
  MAX_STDOUT_BYTES,
  KNOWN_CAPABILITIES,
  providerHome,
  configPath,
  readConfig,
  pickProvider,
  runCapability,
};
