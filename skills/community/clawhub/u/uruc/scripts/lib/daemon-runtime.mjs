import { createServer } from 'net';

import {
  BRIDGE_MESSAGE_PREFIX,
  appendEvent,
  applyExecResultPatch,
  applyRuntimePatch,
  buildBootstrapConfig,
  BRIDGE_MODE_LOCAL,
  createInitialState,
  createLocalBridgeConfig,
  DEFAULT_BRIDGE_COALESCE_MS,
  ensureControlDir,
  extractServerTimestamp,
  getSocketPath,
  normalizeAgentConfig,
  readBridgeQueue,
  readConfig,
  removeSocketIfPresent,
  writeBridgeQueue,
  writeConfig,
  writeState,
  uuid,
} from './common.mjs';
import { sendOpenClawSystemEventText } from './openclaw-gateway.mjs';

const MAX_BRIDGE_RETRY_MS = 30_000;

export class AgentDaemon {
  constructor() {
    this.state = createInitialState();
    this.server = null;
    this.socketPath = getSocketPath();
    this.remoteSocket = null;
    this.pending = new Map();
    this.reconnectTimer = undefined;
    this.manualDisconnect = false;
    this.config = null;
    this.resumeTarget = null;
    this.bridgeQueue = readBridgeQueue();
    this.pendingWakeBatch = null;
    this.bridgeCoalesceTimer = undefined;
    this.bridgeRetryTimer = undefined;
    this.bridgeSending = false;
    this.bridgeRetryAttempt = 0;
  }

  async start() {
    ensureControlDir();
    removeSocketIfPresent();
    this.server = createServer((socket) => this.handleControlConnection(socket));

    await new Promise((resolve, reject) => {
      this.server.once('error', reject);
      this.server.listen(this.socketPath, () => {
        this.server.off('error', reject);
        resolve();
      });
    });

    const existingConfig = normalizeConfig(readConfig());
    if (existingConfig) {
      this.config = existingConfig;
      this.state = {
        ...this.state,
        wsUrl: existingConfig.wsUrl ?? null,
        baseUrl: existingConfig.baseUrl ?? null,
      };
    }
    this.syncBridgeState();
    this.persistState();

    if (this.bridgeQueue.batches.length > 0) {
      void this.processWakeQueue();
    }

    if (existingConfig && this.hasRemoteConfig(existingConfig)) {
      void this.connectRemote(existingConfig).catch((error) => {
        this.setError(error instanceof Error ? error.message : String(error));
      });
    }
  }

  async stop() {
    this.clearReconnect();
    this.clearBridgeTimers();
    await this.disconnectRemote({ clearSession: true });
    if (this.server) {
      await new Promise((resolve) => this.server?.close(() => resolve()));
      this.server = null;
    }
    removeSocketIfPresent();
  }

  handleControlConnection(socket) {
    let buffer = '';
    socket.on('data', async (chunk) => {
      buffer += chunk.toString();
      const newlineIndex = buffer.indexOf('\n');
      if (newlineIndex === -1) return;

      const line = buffer.slice(0, newlineIndex);
      let request;
      try {
        request = JSON.parse(line);
      } catch {
        this.writeResponse(socket, { id: 'invalid', ok: false, error: 'invalid control payload' });
        socket.end();
        return;
      }

      const response = await this.handleRequest(request);
      this.writeResponse(socket, response);
      socket.end();
    });
  }

  writeResponse(socket, response) {
    socket.write(`${JSON.stringify(response)}\n`);
  }

  async handleRequest(request) {
    try {
      switch (request.action) {
        case 'ping':
          return { id: request.id, ok: true, data: { pong: true, pid: process.pid } };

        case 'status':
          return { id: request.id, ok: true, data: this.state };

        case 'connect': {
          const state = await this.bootstrapRemoteConfig(request.payload);
          return { id: request.id, ok: true, data: state };
        }

        case 'bootstrap': {
          const state = await this.bootstrapRemoteConfig(request.payload);
          return { id: request.id, ok: true, data: state };
        }

        case 'disconnect':
          await this.disconnectRemote({ clearSession: true });
          return { id: request.id, ok: true, data: this.state };

        case 'commands': {
          const response = await this.refreshSessionState();
          this.state = {
            ...this.state,
            availableCommands: response.availableCommands ?? [],
            availableLocations: response.availableLocations ?? [],
          };
          this.persistState();
          return {
            id: request.id,
            ok: true,
            data: {
              commands: this.state.availableCommands,
              locations: this.state.availableLocations,
              state: this.state,
            },
          };
        }

        case 'exec': {
          const payload = request.payload;
          const result = await this.sendRemote(payload.type, payload.payload, payload.timeoutMs);
          this.state = applyExecResultPatch(this.state, payload.type, payload.payload, result);
          this.persistState();
          return { id: request.id, ok: true, data: { result, state: this.state } };
        }

        case 'events': {
          const payload = request.payload ?? {};
          const limit = typeof payload.limit === 'number' ? payload.limit : 20;
          return {
            id: request.id,
            ok: true,
            data: {
              events: this.state.recentEvents.slice(-limit),
              state: this.state,
            },
          };
        }

        case 'bridge_status':
          return { id: request.id, ok: true, data: this.buildBridgeStatus() };

        case 'bridge_test': {
          const message = {
            type: 'bridge_test',
            payload: { manual: true, mode: BRIDGE_MODE_LOCAL },
          };
          this.queueWakeBatch({ id: 'manual_test', createdAt: new Date().toISOString(), messages: [message] });
          await this.processWakeQueue();
          return { id: request.id, ok: true, data: this.buildBridgeStatus({ testQueued: true }) };
        }

        case 'shutdown':
          setTimeout(() => {
            void this.stop().finally(() => process.exit(0));
          }, 0);
          return { id: request.id, ok: true, data: { shuttingDown: true } };

        default:
          return { id: request.id, ok: false, error: `unknown action: ${request.action}` };
      }
    } catch (error) {
      return {
        id: request.id,
        ok: false,
        error: error instanceof Error ? error.message : String(error),
      };
    }
  }

  async bootstrapRemoteConfig(payload = {}) {
    const nextConfig = buildBootstrapConfig(payload, this.config, {
      coalesceWindowMs: payload.coalesceWindowMs,
    });
    const previousConfig = this.config;
    const needsReconnect = !this.isConnectedToConfig(previousConfig, nextConfig);

    this.config = nextConfig;
    writeConfig(this.config);
    this.syncBridgeState();
    this.persistState();

    if (needsReconnect) {
      await this.connectRemote(this.config);
    }

    return this.state;
  }

  async connectRemote(config) {
    this.manualDisconnect = false;
    this.clearReconnect();
    this.resumeTarget = {
      hadControl: this.state.isController,
    };

    await this.disconnectRemote({ clearSession: false });
    this.manualDisconnect = false;

    this.state = {
      ...this.state,
      connectionStatus: 'connecting',
      lastError: '',
      wsUrl: config.wsUrl,
      baseUrl: config.baseUrl ?? null,
    };
    this.persistState();

    const remoteSocket = await new Promise((resolve, reject) => {
      const socket = new WebSocket(config.wsUrl);
      let settled = false;

      const fail = (error) => {
        if (settled) return;
        settled = true;
        try {
          socket.close();
        } catch {
          // noop
        }
        reject(error instanceof Error ? error : new Error(String(error)));
      };

      socket.onopen = () => {
        if (settled) return;
        settled = true;
        resolve(socket);
      };

      socket.onerror = (event) => {
        const error = event?.error instanceof Error ? event.error : new Error('WebSocket 连接失败');
        fail(error);
      };
    });

    this.remoteSocket = remoteSocket;
    this.bindRemoteSocket(remoteSocket, config);

    let authResult;
    try {
      authResult = await this.sendRemote('auth', config.auth, 10000);
    } catch (error) {
      await this.disconnectRemote({ clearSession: true });
      this.setError(error instanceof Error ? error.message : String(error));
      throw error;
    }

    this.state = applyRuntimePatch({
      ...this.state,
      connectionStatus: 'connected',
      authenticated: true,
      agentSession: {
        agentId: authResult.agentId,
        agentName: authResult.agentName,
      },
      lastError: '',
    }, authResult);
    this.persistState();
    await this.refreshSessionState();
    await this.restoreControlIfNeeded();
  }

  bindRemoteSocket(socket, config) {
    socket.onmessage = (event) => {
      let message;
      try {
        message = JSON.parse(String(event.data));
      } catch {
        return;
      }

      if (message.id && this.pending.has(message.id)) {
        const pending = this.pending.get(message.id);
        clearTimeout(pending.timeout);
        this.pending.delete(message.id);
        if (message.type === 'error') {
          const errorPayload = message.payload ?? {};
          pending.reject(new Error(errorPayload.error ?? 'unknown uruc error'));
        } else {
          pending.resolve(message.payload);
        }
        return;
      }

      this.handleUnsolicitedMessage(message);
    };

    socket.onclose = () => {
      this.failAllPending('remote connection closed');
      this.remoteSocket = null;

      if (this.manualDisconnect || !this.config || !this.hasRemoteConfig(this.config)) {
        this.state = {
          ...this.state,
          connectionStatus: 'idle',
          authenticated: false,
        };
        this.persistState();
        return;
      }

      this.state = {
        ...this.state,
        connectionStatus: 'reconnecting',
        authenticated: false,
      };
      this.persistState();
      this.scheduleReconnect(config);
    };

    socket.onerror = (event) => {
      const message = event?.error instanceof Error ? event.error.message : 'WebSocket 出现错误';
      this.setError(message);
    };
  }

  handleUnsolicitedMessage(message) {
    const receivedAt = new Date().toISOString();
    const entry = {
      id: message.id || uuid(),
      type: message.type,
      payload: message.payload,
      receivedAt,
      serverTimestamp: extractServerTimestamp(message.payload, this.state.serverTimestamp ?? Date.now()),
    };

    this.state = appendEvent(this.state, entry);
    if (message.payload && typeof message.payload === 'object') {
      this.state = applyRuntimePatch(this.state, message.payload);
    }
    if (message.payload?.state && typeof message.payload.state === 'object') {
      this.state = applyRuntimePatch(this.state, message.payload.state);
    }
    if (message.type === 'error') {
      const errorPayload = message.payload ?? {};
      this.state = {
        ...this.state,
        lastError: errorPayload.error ?? 'unknown uruc error',
      };
    }
    if (message.type === 'control_replaced') {
      const errorPayload = message.payload ?? {};
      this.state = {
        ...this.state,
        isController: false,
        lastError: errorPayload.error ?? '当前 Agent 已在其他连接中被接管',
      };
    }
    if (message.type === 'kicked' || message.type === 'replaced') {
      this.manualDisconnect = true;
      this.clearReconnect();
      this.state = {
        ...this.state,
        authenticated: false,
        hasController: false,
        isController: false,
      };
    }
    this.logPush(entry);
    this.persistState();
    void this.scheduleWakeForMessage(message);
  }

  async disconnectRemote({ clearSession }) {
    this.manualDisconnect = true;
    this.clearReconnect();
    this.failAllPending('remote connection closed');

    if (this.remoteSocket) {
      const socket = this.remoteSocket;
      this.remoteSocket = null;
      await new Promise((resolve) => {
        let finished = false;
        const done = () => {
          if (finished) return;
          finished = true;
          resolve();
        };
        socket.onclose = done;
        try {
          socket.close();
        } catch {
          done();
        }
        setTimeout(done, 300);
      });
    }

    this.state = {
      ...this.state,
      connectionStatus: 'idle',
      authenticated: false,
      lastError: '',
      agentSession: clearSession ? null : this.state.agentSession,
      hasController: clearSession ? false : this.state.hasController,
      isController: clearSession ? false : this.state.isController,
      inCity: clearSession ? false : this.state.inCity,
      currentLocation: clearSession ? null : this.state.currentLocation,
      availableCommands: clearSession ? [] : this.state.availableCommands,
      availableLocations: clearSession ? [] : this.state.availableLocations,
    };
    this.persistState();
  }

  async sendRemote(type, payload, timeoutMs = 15000) {
    if (!this.remoteSocket || this.remoteSocket.readyState !== WebSocket.OPEN) {
      throw new Error('agent daemon is not connected to Uruc');
    }

    const id = uuid();
    const message = { id, type, payload };
    return await new Promise((resolve, reject) => {
      const timeout = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error(`command timed out: ${type}`));
      }, timeoutMs);

      this.pending.set(id, { resolve, reject, timeout });
      this.remoteSocket.send(JSON.stringify(message));
    });
  }

  scheduleReconnect(config) {
    if (this.reconnectTimer) return;
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = undefined;
      void this.connectRemote(config).catch((error) => {
        this.setError(error instanceof Error ? error.message : String(error));
        this.state = {
          ...this.state,
          connectionStatus: 'reconnecting',
        };
        this.persistState();
        this.scheduleReconnect(config);
      });
    }, 1500);
  }

  clearReconnect() {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = undefined;
    }
  }

  clearBridgeTimers() {
    if (this.bridgeCoalesceTimer) {
      clearTimeout(this.bridgeCoalesceTimer);
      this.bridgeCoalesceTimer = undefined;
    }
    if (this.bridgeRetryTimer) {
      clearTimeout(this.bridgeRetryTimer);
      this.bridgeRetryTimer = undefined;
    }
  }

  failAllPending(reason) {
    for (const [, pending] of this.pending) {
      clearTimeout(pending.timeout);
      pending.reject(new Error(reason));
    }
    this.pending.clear();
  }

  setError(message) {
    this.state = {
      ...this.state,
      connectionStatus: 'error',
      lastError: message,
      authenticated: false,
      hasController: false,
      isController: false,
    };
    this.persistState();
  }

  persistState() {
    this.syncBridgeState();
    writeState({
      ...this.state,
      daemonPid: process.pid,
      daemonStartedAt: this.state.daemonStartedAt || new Date().toISOString(),
    });
  }

  async refreshSessionState() {
    const result = await this.sendRemote('session_state');
    this.state = applyRuntimePatch(this.state, result);
    this.persistState();
    return result;
  }

  async restoreControlIfNeeded() {
    if (!this.resumeTarget) return;
    const target = this.resumeTarget;
    this.resumeTarget = null;

    try {
      if (!target.hadControl) {
        return;
      }
      if (!this.state.isController) {
        const result = await this.sendRemote('claim_control');
        this.state = applyRuntimePatch(this.state, result);
        this.persistState();
      }
    } catch (error) {
      this.state = {
        ...this.state,
        lastError: `重连后恢复控制权失败: ${error instanceof Error ? error.message : String(error)}`,
      };
      this.persistState();
    }
  }

  async scheduleWakeForMessage(message) {
    const bridge = this.getBridgeConfig();
    if (!bridge?.enabled) return;
    if (!this.state.agentSession?.agentId) return;

    if (!this.pendingWakeBatch) {
      this.pendingWakeBatch = {
        id: uuid(),
        createdAt: new Date().toISOString(),
        messages: [],
      };
    }
    this.pendingWakeBatch.messages.push(cloneJsonValue(message));
    this.syncBridgeState();
    this.persistState();

    if (this.bridgeCoalesceTimer) return;
    this.bridgeCoalesceTimer = setTimeout(() => {
      this.bridgeCoalesceTimer = undefined;
      const pending = this.pendingWakeBatch;
      this.pendingWakeBatch = null;
      if (!pending || pending.messages.length === 0) {
        this.syncBridgeState();
        this.persistState();
        return;
      }
      this.queueWakeBatch(pending);
      void this.processWakeQueue();
    }, bridge.coalesceWindowMs);
  }

  queueWakeBatch(batch) {
    const normalized = normalizeWakeBatch(batch);
    if (normalized.messages.length === 0) return;

    if (this.bridgeQueue.batches.length > 0) {
      const last = this.bridgeQueue.batches[this.bridgeQueue.batches.length - 1];
      last.messages = [...last.messages, ...normalized.messages];
      last.createdAt = normalized.createdAt;
    } else {
      this.bridgeQueue.batches.push(normalized);
    }
    writeBridgeQueue(this.bridgeQueue);
    this.syncBridgeState();
    this.persistState();
  }

  async processWakeQueue() {
    const bridge = this.getBridgeConfig();
    if (!bridge?.enabled) return;
    if (this.bridgeSending || this.bridgeRetryTimer) return;

    this.bridgeSending = true;
    try {
      while (this.bridgeQueue.batches.length > 0) {
        await this.sendWake(this.bridgeQueue.batches[0], bridge);
        this.logWake(this.bridgeQueue.batches[0]);
        this.bridgeQueue.batches.shift();
        this.bridgeRetryAttempt = 0;
        this.state = {
          ...this.state,
          lastWakeAt: new Date().toISOString(),
          lastWakeError: '',
        };
        writeBridgeQueue(this.bridgeQueue);
        this.syncBridgeState();
        this.persistState();
      }
    } catch (error) {
      this.state = {
        ...this.state,
        lastWakeError: error instanceof Error ? error.message : String(error),
      };
      this.syncBridgeState();
      this.persistState();
      this.scheduleBridgeRetry();
    } finally {
      this.bridgeSending = false;
    }
  }

  async sendWake(batch, bridge) {
    if (bridge.mode !== BRIDGE_MODE_LOCAL) {
      throw new Error(`不支持的 bridge 模式: ${bridge.mode}`);
    }
    const body = batch.messages.length <= 1 ? batch.messages[0] ?? null : batch.messages;
    await this.sendLocalWakeText(`${BRIDGE_MESSAGE_PREFIX}\n${JSON.stringify(body)}`, {
      sessionKey: bridge.targetSession ?? 'main',
      idempotencyKey: batch.id,
    });
  }

  async sendLocalWakeText(text, options = {}) {
    await sendOpenClawSystemEventText(text, options);
  }

  scheduleBridgeRetry() {
    if (this.bridgeRetryTimer || !this.getBridgeConfig()?.enabled) return;
    const delay = Math.min(1000 * 2 ** this.bridgeRetryAttempt, MAX_BRIDGE_RETRY_MS);
    this.bridgeRetryAttempt += 1;
    this.bridgeRetryTimer = setTimeout(() => {
      this.bridgeRetryTimer = undefined;
      void this.processWakeQueue();
    }, delay);
  }

  buildBridgeStatus(extra = {}) {
    const bridge = this.getBridgeConfig();
    return {
      enabled: bridge?.enabled ?? false,
      mode: bridge?.mode ?? BRIDGE_MODE_LOCAL,
      coalesceWindowMs: bridge?.coalesceWindowMs ?? DEFAULT_BRIDGE_COALESCE_MS,
      targetSession: 'main',
      lastWakeAt: this.state.lastWakeAt,
      lastWakeError: this.state.lastWakeError || null,
      pendingWakeCount: this.bridgeQueue.batches.length + (this.pendingWakeBatch ? 1 : 0),
      ...extra,
    };
  }

  syncBridgeState() {
    const bridge = this.getBridgeConfig();
    this.state = {
      ...this.state,
      bridgeEnabled: bridge?.enabled ?? false,
      pendingWakeCount: this.bridgeQueue.batches.length + (this.pendingWakeBatch ? 1 : 0),
    };
  }

  getBridgeConfig() {
    return createLocalBridgeConfig(this.config?.bridge);
  }

  isConnectedToConfig(previousConfig, nextConfig) {
    if (!previousConfig || !nextConfig) return false;
    if (!this.remoteSocket || this.remoteSocket.readyState !== WebSocket.OPEN) return false;
    if (!this.state.authenticated || this.state.connectionStatus !== 'connected') return false;
    return previousConfig.wsUrl === nextConfig.wsUrl
      && previousConfig.auth === nextConfig.auth
      && previousConfig.baseUrl === nextConfig.baseUrl;
  }

  hasRemoteConfig(config) {
    return Boolean(config?.wsUrl && config?.auth);
  }

  logPush(entry) {
    const serverTimestamp = typeof entry.serverTimestamp === 'number' ? ` serverTimestamp=${entry.serverTimestamp}` : '';
    console.log(`[uruc-agent] push type=${entry.type}${serverTimestamp}`);
  }

  logWake(batch) {
    const serverTimestamp = extractWakeBatchServerTimestamp(batch.messages);
    const timestampLabel = typeof serverTimestamp === 'number' ? ` serverTimestamp=${serverTimestamp}` : '';
    console.log(`[uruc-agent] bridge batch=${batch.id ?? 'unknown'} messages=${batch.messages.length}${timestampLabel}`);
  }
}

function normalizeWakeBatch(batch) {
  return {
    id: typeof batch?.id === 'string' && batch.id !== '' ? batch.id : uuid(),
    createdAt: typeof batch?.createdAt === 'string' && batch.createdAt !== '' ? batch.createdAt : new Date().toISOString(),
    messages: Array.isArray(batch?.messages)
      ? batch.messages.map((message) => cloneJsonValue(message))
      : [],
  };
}

function extractWakeBatchServerTimestamp(messages) {
  for (const message of messages) {
    const serverTimestamp = extractServerTimestamp(message?.payload, null);
    if (typeof serverTimestamp === 'number') return serverTimestamp;
  }
  return null;
}

function cloneJsonValue(value) {
  if (typeof value === 'undefined') return null;
  return JSON.parse(JSON.stringify(value));
}

function normalizeConfig(config) {
  return normalizeAgentConfig(config);
}
