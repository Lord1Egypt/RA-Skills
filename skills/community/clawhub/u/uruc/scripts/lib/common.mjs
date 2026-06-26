import { mkdirSync, readFileSync, writeFileSync, existsSync, unlinkSync } from 'fs';
import { randomUUID } from 'crypto';
import os from 'os';
import path from 'path';

export const DEFAULT_BRIDGE_COALESCE_MS = 500;
export const BRIDGE_MODE_LOCAL = 'local';
export const BRIDGE_MESSAGE_PREFIX = '[URUC_EVENT]';

export function uuid() {
  return randomUUID();
}

export function ensureNodeVersion(minMajor = 22) {
  const major = Number(process.versions.node.split('.')[0]);
  if (!Number.isFinite(major) || major < minMajor) {
    throw new Error(`Node.js >= ${minMajor} is required (current: ${process.version})`);
  }
}

export function getControlDir() {
  if (typeof process.env.URUC_AGENT_CONTROL_DIR === 'string' && process.env.URUC_AGENT_CONTROL_DIR.trim() !== '') {
    return path.resolve(process.env.URUC_AGENT_CONTROL_DIR);
  }
  return path.join(os.homedir(), '.uruc', 'agent');
}

export function ensureControlDir() {
  const dir = getControlDir();
  mkdirSync(dir, { recursive: true, mode: 0o700 });
  return dir;
}

export function getSocketPath() {
  if (process.platform === 'win32') {
    const username = slug(os.userInfo().username || 'default');
    return `\\\\.\\pipe\\uruc-agent-${username}`;
  }
  return path.join(getControlDir(), 'daemon.sock');
}

export function getStatePath() {
  return path.join(getControlDir(), 'state.json');
}

export function getConfigPath() {
  return path.join(getControlDir(), 'config.json');
}

export function getLogPath() {
  return path.join(getControlDir(), 'daemon.log');
}

export function getBridgeQueuePath() {
  return path.join(getControlDir(), 'bridge-queue.json');
}

export function removeSocketIfPresent() {
  if (process.platform === 'win32') return;
  const socketPath = getSocketPath();
  if (existsSync(socketPath)) unlinkSync(socketPath);
}

export function createInitialState() {
  return {
    daemonPid: process.pid,
    daemonStartedAt: new Date().toISOString(),
    connectionStatus: 'idle',
    wsUrl: null,
    baseUrl: null,
    authenticated: false,
    hasController: false,
    isController: false,
    agentSession: null,
    inCity: false,
    currentLocation: null,
    serverTimestamp: null,
    availableCommands: [],
    availableLocations: [],
    lastError: '',
    lastEventAt: null,
    recentEvents: [],
    bridgeEnabled: true,
    lastWakeAt: null,
    lastWakeError: '',
    pendingWakeCount: 0,
  };
}

export function readConfig() {
  return readJsonFile(getConfigPath());
}

export function writeConfig(config) {
  writeJsonFile(getConfigPath(), config);
}

export function readState() {
  return readJsonFile(getStatePath());
}

export function writeState(state) {
  writeJsonFile(getStatePath(), state);
}

export function readBridgeQueue() {
  const queue = readJsonFile(getBridgeQueuePath());
  if (!queue || typeof queue !== 'object' || !Array.isArray(queue.batches)) {
    return { batches: [] };
  }
  return {
    batches: queue.batches
      .map((batch) => normalizePersistedWakeBatch(batch))
      .filter((batch) => batch !== null),
  };
}

export function writeBridgeQueue(queue) {
  writeJsonFile(getBridgeQueuePath(), queue);
}

function normalizePersistedWakeBatch(batch) {
  if (!batch || typeof batch !== 'object') return null;
  if (typeof batch.id !== 'string' || batch.id === '') return null;
  if (typeof batch.createdAt !== 'string' || batch.createdAt === '') return null;
  if (!Array.isArray(batch.messages)) return null;

  const messages = batch.messages
    .map((message) => normalizePersistedWakeMessage(message))
    .filter((message) => message !== null);

  if (messages.length === 0) return null;
  return {
    id: batch.id,
    createdAt: batch.createdAt,
    messages,
  };
}

function normalizePersistedWakeMessage(message) {
  if (!message || typeof message !== 'object') return null;
  if (typeof message.type !== 'string' || message.type === '') return null;

  const normalized = { type: message.type };
  if (typeof message.id === 'string' && message.id !== '') {
    normalized.id = message.id;
  }
  if (Object.prototype.hasOwnProperty.call(message, 'payload')) {
    normalized.payload = cloneJsonValue(message.payload);
  }
  return normalized;
}

function cloneJsonValue(value) {
  if (typeof value === 'undefined') return null;
  return JSON.parse(JSON.stringify(value));
}

export function readLogTail(lines = 40) {
  const logPath = getLogPath();
  if (!existsSync(logPath)) return '';
  const content = readFileSync(logPath, 'utf8').trim();
  if (!content) return '';
  return content.split(/\r?\n/).slice(-lines).join('\n');
}

export function resolveConnectInput(input, env = process.env) {
  const baseUrl = firstDefined(input.baseUrl, env.URUC_AGENT_BASE_URL);
  const wsUrl = firstDefined(input.wsUrl, env.URUC_AGENT_WS_URL) ?? inferWsUrl(baseUrl);
  if (!wsUrl) {
    throw new Error('缺少连接地址。请传入 --ws-url 或 --base-url，或设置 URUC_AGENT_WS_URL / URUC_AGENT_BASE_URL');
  }

  const auth = firstDefined(
    input.auth,
    input.authEnv ? env[input.authEnv] : undefined,
    env.URUC_AGENT_AUTH,
  );
  if (!auth) {
    throw new Error('缺少认证凭证。请传入 --auth，或设置 URUC_AGENT_AUTH，或用 --auth-env 指定环境变量');
  }

  return { wsUrl, auth, baseUrl: baseUrl ?? undefined };
}

export function resolveSkillConnectInput(env = process.env) {
  const baseUrl = firstDefined(env.URUC_AGENT_BASE_URL);
  if (!baseUrl) {
    throw new Error('缺少 OpenClaw skill env: URUC_AGENT_BASE_URL');
  }

  const auth = firstDefined(env.URUC_AGENT_AUTH);
  if (!auth) {
    throw new Error('缺少 OpenClaw skill env: URUC_AGENT_AUTH');
  }

  return resolveConnectInput({ baseUrl, auth }, env);
}

export function inferWsUrl(baseUrl) {
  if (!baseUrl) return null;
  const parsed = new URL(baseUrl);

  if (parsed.protocol === 'https:') {
    return `wss://${parsed.host}/ws`;
  }
  if (parsed.protocol !== 'http:') {
    throw new Error(`不支持的 BASE_URL 协议: ${parsed.protocol}`);
  }

  const localHosts = new Set(['localhost', '127.0.0.1', '0.0.0.0']);
  if (localHosts.has(parsed.hostname)) {
    const httpPort = parsed.port ? Number(parsed.port) : 3000;
    const wsPort = Number.isInteger(httpPort) ? httpPort + 1 : 3001;
    return `ws://${parsed.hostname}:${wsPort}`;
  }
  return `ws://${parsed.host}/ws`;
}

export function parsePayloadArg(value) {
  if (!value) return undefined;
  try {
    return JSON.parse(value);
  } catch (error) {
    throw new Error(`payload 不是合法 JSON: ${error instanceof Error ? error.message : String(error)}`);
  }
}

export function filterCommandSchemas(commands, filters) {
  return commands.filter((command) => {
    if (filters.prefix && !command.type.startsWith(filters.prefix)) return false;
    if (filters.plugin && command.pluginName !== filters.plugin) return false;
    if (filters.search) {
      const haystack = `${command.type} ${command.description} ${command.pluginName ?? ''}`.toLowerCase();
      if (!haystack.includes(filters.search.toLowerCase())) return false;
    }
    return true;
  });
}

export function appendEvent(state, entry) {
  const recentEvents = [...state.recentEvents, entry].slice(-200);
  return {
    ...state,
    recentEvents,
    lastEventAt: entry.receivedAt,
  };
}

export function extractServerTimestamp(payload, fallback = null) {
  if (payload && typeof payload === 'object') {
    if (typeof payload.serverTimestamp === 'number') return payload.serverTimestamp;
    if (payload.state && typeof payload.state === 'object' && typeof payload.state.serverTimestamp === 'number') {
      return payload.state.serverTimestamp;
    }
    if (typeof payload.timestamp === 'number') return payload.timestamp;
  }
  return fallback;
}

export function applyRuntimePatch(state, payload) {
  if (!payload || typeof payload !== 'object') return state;
  const data = payload;
  const next = { ...state };

  if (typeof data.hasController === 'boolean') next.hasController = data.hasController;
  if (typeof data.isController === 'boolean') next.isController = data.isController;
  if (typeof data.inCity === 'boolean') next.inCity = data.inCity;
  if (typeof data.serverTimestamp === 'number') next.serverTimestamp = data.serverTimestamp;
  if (typeof data.currentLocation === 'string' || data.currentLocation === null) {
    next.currentLocation = data.currentLocation;
  }
  if (typeof data.locationId === 'string' || data.locationId === null) {
    next.currentLocation = data.locationId;
  }
  if (Array.isArray(data.availableCommands)) {
    next.availableCommands = data.availableCommands;
  }
  if (Array.isArray(data.availableLocations)) {
    next.availableLocations = data.availableLocations;
  }
  return next;
}

export function applyExecResultPatch(state, commandType, commandPayload, resultPayload) {
  let next = applyRuntimePatch(state, resultPayload);

  if (commandType === 'enter_city') {
    next = { ...next, inCity: true };
  }
  if (commandType === 'leave_city') {
    next = { ...next, inCity: false, currentLocation: null };
  }
  if (commandType === 'enter_location') {
    const locationId = extractLocationId(resultPayload)
      ?? (commandPayload && typeof commandPayload === 'object' ? commandPayload.locationId ?? null : null);
    next = { ...next, currentLocation: locationId };
  }
  if (commandType === 'leave_location') {
    next = { ...next, currentLocation: null };
  }
  return next;
}

export function formatJson(value) {
  if (typeof value === 'undefined') return 'null';
  return JSON.stringify(value, null, 2);
}

export function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function isPidAlive(pid) {
  try {
    process.kill(pid, 0);
    return true;
  } catch {
    return false;
  }
}

export function normalizeCoalesceWindow(value) {
  const numberValue = typeof value === 'number' ? value : Number(value);
  if (!Number.isFinite(numberValue) || numberValue <= 0) {
    return DEFAULT_BRIDGE_COALESCE_MS;
  }
  return Math.max(50, Math.floor(numberValue));
}

export function createLocalBridgeConfig(existingBridge = null, overrides = {}) {
  const bridge = existingBridge && typeof existingBridge === 'object' ? existingBridge : {};
  return {
    enabled: true,
    mode: BRIDGE_MODE_LOCAL,
    coalesceWindowMs: normalizeCoalesceWindow(overrides.coalesceWindowMs ?? bridge.coalesceWindowMs),
    targetSession: 'main',
    updatedAt: typeof overrides.updatedAt === 'string'
      ? overrides.updatedAt
      : typeof bridge.updatedAt === 'string'
        ? bridge.updatedAt
        : undefined,
  };
}

export function normalizeAgentConfig(config) {
  if (!config || typeof config !== 'object') return null;

  const normalized = {
    ...config,
    wsUrl: typeof config.wsUrl === 'string' ? config.wsUrl : undefined,
    auth: typeof config.auth === 'string' ? config.auth : undefined,
    baseUrl: typeof config.baseUrl === 'string' ? config.baseUrl : undefined,
  };

  if (config.bridge && typeof config.bridge === 'object') {
    normalized.bridge = createLocalBridgeConfig(config.bridge, {
      coalesceWindowMs: config.bridge.coalesceWindowMs,
      updatedAt: typeof config.bridge.updatedAt === 'string' ? config.bridge.updatedAt : undefined,
    });
  }

  return normalized;
}

export function buildBootstrapConfig(input, currentConfig = null, options = {}) {
  const existing = currentConfig && typeof currentConfig === 'object' ? currentConfig : {};
  const updatedAt = typeof options.updatedAt === 'string' ? options.updatedAt : new Date().toISOString();
  return normalizeAgentConfig({
    ...existing,
    wsUrl: input.wsUrl,
    auth: input.auth,
    baseUrl: input.baseUrl,
    updatedAt,
    bridge: createLocalBridgeConfig(existing.bridge, {
      coalesceWindowMs: options.coalesceWindowMs,
      updatedAt,
    }),
  });
}

export function isBootstrapConfigSatisfied(config, input) {
  const normalized = normalizeAgentConfig(config);
  if (!normalized) return false;
  return normalized.wsUrl === input.wsUrl
    && normalized.auth === input.auth
    && normalized.baseUrl === input.baseUrl
    && normalized.bridge?.enabled === true
    && normalized.bridge?.mode === BRIDGE_MODE_LOCAL;
}

function extractLocationId(payload) {
  if (!payload || typeof payload !== 'object') return null;
  if (typeof payload.locationId === 'string') return payload.locationId;
  return null;
}

function readJsonFile(filename) {
  try {
    if (!existsSync(filename)) return null;
    return JSON.parse(readFileSync(filename, 'utf8'));
  } catch {
    return null;
  }
}

function writeJsonFile(filename, value) {
  ensureControlDir();
  writeFileSync(filename, `${JSON.stringify(value, null, 2)}\n`, { mode: 0o600 });
}

function slug(value) {
  return value.replace(/[^A-Za-z0-9_-]+/g, '-');
}

function firstDefined(...values) {
  for (const value of values) {
    if (typeof value === 'string' && value.trim() !== '') return value;
  }
  return undefined;
}
