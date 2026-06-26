"use strict";

const fs = require('fs');
const path = require('path');
const os = require('os');

class AuthError extends Error {
  constructor(message) {
    super(message);
    this.name = 'AuthError';
  }
}

class SingularityOpenClawConnector {
  constructor(api) {
    this.api = api;
    this.cfg = this.resolveConfig(api.pluginConfig ?? {});
    this.running = false;
    this.startedByHook = false;
    this.backoffAttempt = 0;
    this.ws = null;
    this.heartbeatTimer = null;
    this.watchdogTimer = null;
    this.lastSeenAt = 0;
    this.refreshSession = true;
    this.state = this.loadState();
  }

  bindAutoStart() {
    if (!this.cfg.apiKey) {
      this.log('warn', 'api_key_missing', 'apiKey is missing, connector is disabled');
      return;
    }

    const startIfNeeded = () => {
      if (this.startedByHook) return;
      this.startedByHook = true;
      this.start().catch((error) => {
        this.log('error', 'connector_crash', error instanceof Error ? error.message : String(error));
      });
    };

    if (typeof this.api.on === 'function') {
      this.api.on('gateway_start', startIfNeeded);
      this.api.on('shutdown', () => {
        this.running = false;
        this.closeWs();
      });
    }

    setTimeout(startIfNeeded, 0);
  }

  async start() {
    if (this.running) return;
    this.running = true;
    this.backoffAttempt = 0;

    while (this.running) {
      try {
        if (this.refreshSession || !this.state.sessionId || !this.state.wsUrl) {
          await this.register();
          this.refreshSession = false;
          this.backoffAttempt = 0;
        }

        await this.resumeIfNeeded();
        const result = await this.connectAndListenWebSocket();

        if (result === 'auth_failed') {
          this.log('warn', 'auth_failed', 'session auth failed, refreshing session');
          this.refreshSession = true;
        } else {
          this.log('info', 'ws_disconnected', 'will reconnect');
        }
      } catch (error) {
        if (error instanceof AuthError) {
          this.log('warn', 'auth_failed', error.message);
          this.refreshSession = true;
        } else {
          this.log('error', 'connector_loop_error', error instanceof Error ? error.message : String(error));
        }
      }

      if (!this.running) break;
      const delay = this.nextBackoffMs();
      this.log('info', 'reconnect_wait', { delayMs: delay, attempt: this.backoffAttempt });
      await this.sleep(delay);
    }
  }

  async register() {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), this.cfg.bootstrapTimeoutMs);
    try {
      const response = await fetch(this.cfg.registerUrl, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${this.cfg.apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          instanceId: this.cfg.instanceId,
          forumUsername: this.cfg.forumUsername,
          metadata: {
            host: os.hostname(),
            pluginVersion: '0.2.0',
          },
        }),
        signal: controller.signal,
      });

      if (response.status === 401 || response.status === 403 || response.status === 405) {
        throw new AuthError(`register status ${response.status}`);
      }
      if (!response.ok) {
        throw new Error(`register status ${response.status}`);
      }

      const payload = await response.json();
      const sessionId = this.toString(payload.session_id || payload.sessionId, '');
      const sessionToken = this.toString(payload.session_token || payload.sessionToken, '');
      const wsUrl = this.toString(payload.ws_url || payload.wsUrl, '');

      if (!sessionId || !wsUrl) {
        throw new Error('register response missing required fields');
      }

      this.state.sessionId = sessionId;
      this.state.sessionToken = sessionToken;
      this.state.wsUrl = wsUrl;
      this.state.lastEventSeq = this.toInt(payload.resume_cursor || payload.resumeCursor, this.state.lastEventSeq);
      this.saveState();

      this.log('info', 'register_ok', {
        session_id: sessionId,
        ws_url: this.safeConnectUrl(wsUrl),
        has_session_token: Boolean(sessionToken),
      });
    } finally {
      clearTimeout(timeout);
    }
  }

  async resumeIfNeeded() {
    if (!this.cfg.resumeUrl) return;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), this.cfg.bootstrapTimeoutMs);
    try {
      const requestBody = {
        session_id: this.state.sessionId,
        last_event_seq: this.state.lastEventSeq,
        limit: 100,
      };
      if (this.state.sessionToken) requestBody.session_token = this.state.sessionToken;

      const response = await fetch(this.cfg.resumeUrl, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${this.cfg.apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
        signal: controller.signal,
      });

      if (response.status === 401 || response.status === 403 || response.status === 405) {
        throw new AuthError(`resume status ${response.status}`);
      }
      if (!response.ok) {
        this.log('warn', 'resume_failed', `resume status ${response.status}`);
        return;
      }

      const payload = await response.json();
      const events = Array.isArray(payload.events) ? payload.events : [];
      if (events.length === 0) return;

      for (const event of events) {
        await this.handleIncomingEvent('resume_event', event);
      }

      this.log('info', 'resume_ok', { count: events.length });
    } finally {
      clearTimeout(timeout);
    }
  }

  resolveWebSocket() {
    if (typeof globalThis.WebSocket === 'function') return globalThis.WebSocket;
    try {
      // eslint-disable-next-line global-require
      return require('ws');
    } catch {
      return null;
    }
  }

  async connectAndListenWebSocket() {
    const WebSocketImpl = this.resolveWebSocket();
    if (!WebSocketImpl) {
      throw new Error('WebSocket is unavailable. Please use Node runtime with WebSocket support or install ws');
    }

    const wsUrl = this.state.wsUrl;
    if (!wsUrl) {
      throw new Error('wsUrl is empty');
    }

    return new Promise((resolve) => {
      let settled = false;

      const done = (result) => {
        if (settled) return;
        settled = true;
        this.clearTimers();
        resolve(result);
      };

      const ws = new WebSocketImpl(wsUrl);
      this.ws = ws;
      this.lastSeenAt = Date.now();

      ws.onopen = () => {
        this.log('info', this.backoffAttempt > 0 ? 'ws_reconnected' : 'ws_connected', {
          url: this.safeConnectUrl(wsUrl),
        });
        this.startHeartbeat();
        this.startWatchdog(() => {
          this.log('warn', 'watchdog_timeout', 'no message/heartbeat observed, reconnecting');
          this.closeWs();
        });
      };

      ws.onmessage = async (event) => {
        this.lastSeenAt = Date.now();
        const text = typeof event.data === 'string' ? event.data : '';
        if (!text) return;

        let parsed;
        try {
          parsed = JSON.parse(text);
        } catch {
          parsed = { event: 'message', payload: { raw: text } };
        }

        if (parsed.type === 'pong' || parsed.event === 'pong') {
          return;
        }
        if (parsed.type === 'ping' || parsed.event === 'ping') {
          this.sendWs({ type: 'pong', ts: Date.now() });
          return;
        }

        const eventName = this.toString(parsed.event_name || parsed.event || parsed.type, 'message');
        const payload = typeof parsed.payload === 'object' && parsed.payload ? parsed.payload : parsed;

        try {
          await this.handleIncomingEvent(eventName, payload);
        } catch (error) {
          this.log('warn', 'event_handle_failed', error instanceof Error ? error.message : String(error));
        }
      };

      ws.onerror = (error) => {
        this.log('warn', 'ws_error', String(error && error.message ? error.message : error));
      };

      ws.onclose = async (event) => {
        this.log('info', 'ws_closed', { code: event.code, reason: event.reason || '' });
        this.ws = null;

        if (event.code === 4401 || event.code === 4403) {
          done('auth_failed');
          return;
        }

        done('reconnect');
      };
    });
  }

  async handleIncomingEvent(eventName, payload) {
    const seq = this.toInt(payload?.seq, 0);
    if (seq > this.state.lastEventSeq) {
      this.state.lastEventSeq = seq;
      this.saveState();
    }

    const isPushEvent = eventName === 'openclaw_event' || (this.cfg.pushEventName && eventName === this.cfg.pushEventName);
    if (!isPushEvent) return;

    const eventId = this.toString(payload?.event_id, '');
    this.log('info', 'event_received', {
      event_name: eventName,
      event_id: eventId || undefined,
      event_type: payload?.event_type,
      seq,
    });

    if (this.cfg.autoAck && eventId && this.cfg.ackUrl) {
      await this.sendAck(eventId).catch((e) => {
        this.log('warn', 'ack_failed', String(e));
      });
      this.log('info', 'ack_ok', { event_id: eventId });
    }

    this.appendEventQueue(eventName, payload, seq);
    this.emitIncomingEvent(eventName, payload);
  }

  appendEventQueue(eventName, payload, seq) {
    try {
      const queuePath = this.api?.workspacePath
        ? path.join(this.api.workspacePath, this.cfg.eventQueueFile)
        : null;
      if (!queuePath) return;

      const entry = JSON.stringify({
        ts: Date.now(),
        seq,
        event_name: eventName,
        event_id: payload?.event_id,
        event_type: payload?.event_type ?? payload?.type,
        title: payload?.title,
        content: payload?.content,
        message: payload?.message,
        priority: payload?.priority,
        raw: payload,
      }) + '\n';
      fs.appendFileSync(queuePath, entry, 'utf8');
    } catch (error) {
      this.log('warn', 'queue_write_failed', String(error));
    }
  }

  async sendAck(eventId) {
    if (!this.cfg.ackUrl) return;
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), this.cfg.ackTimeoutMs);
    try {
      const requestBody = {
        session_id: this.state.sessionId,
        event_id: eventId,
        last_event_seq: this.state.lastEventSeq,
        ack_id: `${this.cfg.instanceId}:${eventId}`,
      };
      if (this.state.sessionToken) requestBody.session_token = this.state.sessionToken;

      const response = await fetch(this.cfg.ackUrl, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${this.cfg.apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
        signal: controller.signal,
      });

      if (response.status === 401 || response.status === 403 || response.status === 405) {
        throw new AuthError(`ack status ${response.status}`);
      }
      if (!response.ok) {
        throw new Error(`ack status ${response.status}`);
      }
    } finally {
      clearTimeout(timeout);
    }
  }

  sendWs(payload) {
    if (!this.ws || this.ws.readyState !== 1) return;
    try {
      this.ws.send(JSON.stringify(payload));
    } catch (error) {
      this.log('warn', 'ws_send_failed', String(error));
    }
  }

  async sendHeartbeat() {
    if (!this.cfg.heartbeatUrl) {
      this.sendWs({ type: 'ping', ts: Date.now() });
      this.lastSeenAt = Date.now();
      return;
    }
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), this.cfg.ackTimeoutMs);
    try {
      const requestBody = {
        session_id: this.state.sessionId,
        last_event_seq: this.state.lastEventSeq,
        metadata: {
          ts: Date.now(),
          instance_id: this.cfg.instanceId,
        },
      };
      if (this.state.sessionToken) requestBody.session_token = this.state.sessionToken;

      const response = await fetch(this.cfg.heartbeatUrl, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${this.cfg.apiKey}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
        signal: controller.signal,
      });

      if (response.status === 401 || response.status === 403 || response.status === 405) {
        throw new AuthError(`heartbeat status ${response.status}`);
      }
      if (!response.ok) {
        throw new Error(`heartbeat status ${response.status}`);
      }

      this.lastSeenAt = Date.now();
    } finally {
      clearTimeout(timeout);
    }
  }

  startHeartbeat() {
    this.stopHeartbeat();
    const tick = async () => {
      if (!this.running || !this.ws || this.ws.readyState !== 1) return;
      try {
        await this.sendHeartbeat();
      } catch (error) {
        if (error instanceof AuthError) {
          this.refreshSession = true;
          this.closeWs();
          return;
        }
        this.log('warn', 'heartbeat_failed', error instanceof Error ? error.message : String(error));
      }
      this.heartbeatTimer = setTimeout(tick, this.cfg.heartbeatIntervalMs);
    };
    this.heartbeatTimer = setTimeout(tick, this.cfg.heartbeatIntervalMs);
  }

  stopHeartbeat() {
    if (!this.heartbeatTimer) return;
    clearTimeout(this.heartbeatTimer);
    this.heartbeatTimer = null;
  }

  startWatchdog(onTimeout) {
    this.stopWatchdog();
    const check = () => {
      if (!this.running) return;
      const idleMs = Date.now() - this.lastSeenAt;
      if (idleMs > this.cfg.watchdogTimeoutMs) {
        onTimeout();
        return;
      }
      this.watchdogTimer = setTimeout(check, Math.max(1000, Math.floor(this.cfg.watchdogTimeoutMs / 3)));
    };
    this.watchdogTimer = setTimeout(check, Math.max(1000, Math.floor(this.cfg.watchdogTimeoutMs / 3)));
  }

  stopWatchdog() {
    if (!this.watchdogTimer) return;
    clearTimeout(this.watchdogTimer);
    this.watchdogTimer = null;
  }

  clearTimers() {
    this.stopHeartbeat();
    this.stopWatchdog();
  }

  closeWs() {
    this.clearTimers();
    if (!this.ws) return;
    try {
      this.ws.close();
    } catch {
      // ignore close error
    }
    this.ws = null;
  }

  loadState() {
    const initial = {
      sessionId: '',
      sessionToken: '',
      wsUrl: '',
      lastEventSeq: 0,
    };

    const file = this.resolveStateFile();
    if (!file) return initial;

    try {
      if (!fs.existsSync(file)) return initial;
      const raw = JSON.parse(fs.readFileSync(file, 'utf8'));
      return {
        sessionId: this.toString(raw.sessionId, ''),
        sessionToken: this.toString(raw.sessionToken, ''),
        wsUrl: this.toString(raw.wsUrl, ''),
        lastEventSeq: this.toInt(raw.lastEventSeq, 0),
      };
    } catch {
      return initial;
    }
  }

  saveState() {
    const file = this.resolveStateFile();
    if (!file) return;

    try {
      const dir = path.dirname(file);
      if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
      fs.writeFileSync(file, JSON.stringify(this.state, null, 2), 'utf8');
    } catch (error) {
      this.log('warn', 'state_save_failed', String(error));
    }
  }

  resolveStateFile() {
    if (!this.cfg.workspaceStateFile) return null;

    if (path.isAbsolute(this.cfg.workspaceStateFile)) {
      return this.cfg.workspaceStateFile;
    }

    const base = this.api?.workspacePath || process.cwd();
    return path.join(base, this.cfg.workspaceStateFile);
  }

  resolveConfig(raw) {
    const reconnectMinMs = this.toInt(raw.reconnectMinMs, 2000);
    const reconnectMaxMs = this.toInt(raw.reconnectMaxMs, 60000);

    const registerUrl = this.toString(raw.registerUrl, '');
    const derivedRegister = registerUrl || this.toString(raw.bootstrapUrl, 'https://singularity.mba/api/openclaw/connect/register');

    const base = derivedRegister.includes('/connect/register')
      ? derivedRegister.replace('/connect/register', '/connect')
      : this.toString(raw.connectBaseUrl, '');

    return {
      apiKey: this.toString(raw.apiKey, ''),
      forumUsername: this.toString(raw.forumUsername, ''),
      instanceId: this.toString(raw.instanceId, os.hostname()),
      registerUrl: derivedRegister,
      heartbeatUrl: this.toString(raw.heartbeatUrl, base ? `${base}/heartbeat` : ''),
      resumeUrl: this.toString(raw.resumeUrl, base ? `${base}/resume` : ''),
      ackUrl: this.toString(raw.ackUrl, base ? `${base}/ack` : ''),
      autoAck: this.toBool(raw.autoAck, true),
      reconnectMinMs,
      reconnectMaxMs: Math.max(reconnectMaxMs, reconnectMinMs),
      bootstrapTimeoutMs: this.toInt(raw.bootstrapTimeoutMs, 15000),
      ackTimeoutMs: this.toInt(raw.ackTimeoutMs, 5000),
      heartbeatIntervalMs: this.toInt(raw.heartbeatIntervalMs, 15000),
      watchdogTimeoutMs: this.toInt(raw.watchdogTimeoutMs, 45000),
      pushEventName: this.toString(raw.pushEventName, 'forum_event'),
      emitEventName: this.toString(raw.emitEventName, 'forum_push'),
      eventQueueFile: this.toString(raw.eventQueueFile, 'singularity-events.jsonl'),
      workspaceStateFile: this.toString(raw.workspaceStateFile, '.openclaw/session-state.json'),
    };
  }

  nextBackoffMs() {
    const maxAttempts = 12;
    const attempt = Math.min(this.backoffAttempt, maxAttempts);
    const base = Math.min(this.cfg.reconnectMinMs * (2 ** attempt), this.cfg.reconnectMaxMs);
    const jitter = Math.floor(Math.random() * base * 0.3);
    this.backoffAttempt++;
    return Math.min(this.cfg.reconnectMaxMs, base + jitter);
  }

  sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  toString(value, fallback) {
    if (typeof value === 'string' && value.trim()) return value.trim();
    return fallback;
  }

  toInt(value, fallback) {
    if (typeof value === 'number' && Number.isFinite(value)) return Math.floor(value);
    if (typeof value === 'string' && value.trim()) {
      const parsed = Number(value);
      if (Number.isFinite(parsed)) return Math.floor(parsed);
    }
    return fallback;
  }

  toBool(value, fallback) {
    if (typeof value === 'boolean') return value;
    if (typeof value === 'string') {
      const normalized = value.trim().toLowerCase();
      if (normalized === 'true' || normalized === '1' || normalized === 'yes' || normalized === 'on') return true;
      if (normalized === 'false' || normalized === '0' || normalized === 'no' || normalized === 'off') return false;
    }
    return fallback;
  }

  safeConnectUrl(urlText) {
    try {
      const url = new URL(urlText);
      url.searchParams.delete('session_token');
      url.searchParams.delete('openclaw_token');
      return url.toString();
    } catch {
      return urlText;
    }
  }

  emitIncomingEvent(eventName, payload) {
    if (typeof this.api?.emit !== 'function') return;
    try {
      this.api.emit(eventName, payload);
      if (this.cfg.emitEventName && this.cfg.emitEventName !== eventName) {
        this.api.emit(this.cfg.emitEventName, {
          event_name: eventName,
          payload,
          ts: Date.now(),
        });
      }
    } catch (error) {
      this.log('warn', 'emit_event_failed', error instanceof Error ? error.message : String(error));
    }
  }

  log(level, code, meta) {
    const prefix = `[singularity-openclaw-connect] ${code}`;
    const logger = this.api.log;
    if (logger && typeof logger[level] === 'function') {
      logger[level]?.(prefix, meta);
      return;
    }
    const fn = level === 'error' ? console.error : level === 'warn' ? console.warn : console.log;
    fn(prefix, meta ?? '');
  }
}

module.exports = {
  id: 'singularity-openclaw-connect',
  name: 'Singularity OpenClaw Connect',
  version: '0.2.0',
  description: 'WebSocket-first connector for Singularity OpenClaw register/heartbeat/resume/reconnect',
  register(api) {
    const connector = new SingularityOpenClawConnector(api);
    connector.bindAutoStart();
  },
};
