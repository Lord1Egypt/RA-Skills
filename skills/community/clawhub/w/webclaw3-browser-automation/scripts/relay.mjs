// relay.mjs - WebSocket server that bridges skill.mjs (function calls) to Chrome extension.
// No external deps; uses only Node built-ins. Target: Node 22+.
//
// Usage:
//   import { Relay } from './relay.mjs';
//   const relay = new Relay({ wsPort: 3457 });
//   await relay.waitForExtension();
//   const tabs = await relay.tab.list();
//   await relay.close();

import http from 'node:http';
import crypto from 'node:crypto';
import { EventEmitter } from 'node:events';
import { randomUUID } from 'node:crypto';
import { appendFile } from 'node:fs/promises';

const WS_MAGIC = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11';
const PING_INTERVAL = 10_000;        // send ping every 10s
const PING_TIMEOUT = 30_000;         // consider connection dead if no pong for 30s
const DEFAULT_REQUEST_TIMEOUT = 30_000;
const DEFAULT_CONNECT_TIMEOUT = 10_000;

function log(...args) {
  console.log('[relay]', ...args);
}

const LOG_RESULT_MAX = 500;
function truncateForLog(value) {
  const s = typeof value === 'string' ? value : JSON.stringify(value);
  if (!s || s.length <= LOG_RESULT_MAX) return s;
  return s.slice(0, LOG_RESULT_MAX) + `...(truncated, original ${s.length} chars)`;
}

// ---------- Minimal WebSocket server (no deps) ----------

class WSConnection extends EventEmitter {
  constructor(socket) {
    super();
    this.socket = socket;
    this.buffer = Buffer.alloc(0);
    this.closed = false;

    socket.on('data', (data) => this._onData(data));
    socket.on('close', () => {
      if (this.closed) return;
      this.closed = true;
      this.emit('close');
    });
    socket.on('error', (err) => this.emit('error', err));
  }

  _onData(data) {
    this.buffer = Buffer.concat([this.buffer, data]);
    while (true) {
      const frame = this._parseFrame();
      if (frame === null) break;       // need more data
      if (frame === undefined) break;  // parse error, connection should close

      switch (frame.opcode) {
        case 0x1: // text
          this.emit('message', frame.payload.toString('utf8'));
          break;
        case 0x8: // close
          this.close(1000, '');
          break;
        case 0x9: // ping
          this._writeFrame(0xA, frame.payload); // pong
          break;
        case 0xA: // pong
          // ignore (we don't initiate pings on this side)
          break;
      }
    }
  }

  _parseFrame() {
    const buf = this.buffer;
    if (buf.length < 2) return null;

    const b1 = buf[0];
    const b2 = buf[1];
    const fin = (b1 & 0x80) !== 0;
    const opcode = b1 & 0x0F;
    const masked = (b2 & 0x80) !== 0;
    let payloadLen = b2 & 0x7F;
    let offset = 2;

    if (payloadLen === 126) {
      if (buf.length < offset + 2) return null;
      payloadLen = buf.readUInt16BE(offset);
      offset += 2;
    } else if (payloadLen === 127) {
      if (buf.length < offset + 8) return null;
      // BigInt; for our use case (small messages), this is overkill but parse it
      const hi = buf.readUInt32BE(offset);
      const lo = buf.readUInt32BE(offset + 4);
      payloadLen = hi * 0x100000000 + lo;
      offset += 8;
    }

    let maskKey = null;
    if (masked) {
      if (buf.length < offset + 4) return null;
      maskKey = buf.slice(offset, offset + 4);
      offset += 4;
    }

    if (buf.length < offset + payloadLen) return null;

    let payload = buf.slice(offset, offset + payloadLen);
    if (masked) {
      const unmasked = Buffer.alloc(payloadLen);
      for (let i = 0; i < payloadLen; i++) {
        unmasked[i] = payload[i] ^ maskKey[i % 4];
      }
      payload = unmasked;
    }

    this.buffer = buf.slice(offset + payloadLen);

    return { fin, opcode, payload };
  }

  send(text) {
    if (this.closed) return;
    this._writeFrame(0x1, Buffer.from(text, 'utf8'));
  }

  _writeFrame(opcode, payload) {
    if (this.closed) return;
    const payloadLen = payload.length;
    let header;

    if (payloadLen < 126) {
      header = Buffer.alloc(2);
      header[0] = 0x80 | opcode;
      header[1] = payloadLen;
    } else if (payloadLen < 65536) {
      header = Buffer.alloc(4);
      header[0] = 0x80 | opcode;
      header[1] = 126;
      header.writeUInt16BE(payloadLen, 2);
    } else {
      header = Buffer.alloc(10);
      header[0] = 0x80 | opcode;
      header[1] = 127;
      header.writeUInt32BE(Math.floor(payloadLen / 0x100000000), 2);
      header.writeUInt32BE(payloadLen & 0xFFFFFFFF, 6);
    }

    try {
      this.socket.write(Buffer.concat([header, payload]));
    } catch (err) {
      // socket may be closed
    }
  }

  close(code = 1000, reason = '') {
    if (this.closed) return;
    this.closed = true;
    const reasonBuf = Buffer.from(reason, 'utf8');
    const payload = Buffer.alloc(2 + reasonBuf.length);
    payload.writeUInt16BE(code, 0);
    reasonBuf.copy(payload, 2);
    try {
      this._writeFrame(0x8, payload);
    } catch {}
    this.emit('close');
    this.socket.end();
  }
}

class WebSocketServer extends EventEmitter {
  constructor({ port, host = '127.0.0.1', httpHandler } = {}) {
    super();
    this.port = port;
    this.host = host;

    this.httpServer = http.createServer((req, res) => {
      if (httpHandler) {
        httpHandler(req, res);
        return;
      }
      res.writeHead(426, { 'Content-Type': 'text/plain' });
      res.end('Upgrade Required: this endpoint expects a WebSocket connection');
    });

    this.httpServer.on('upgrade', (req, socket, head) => this._handleUpgrade(req, socket));
    this.httpServer.on('error', (err) => this.emit('error', err));

    this.httpServer.listen(port, host, () => this.emit('listening'));
  }

  _handleUpgrade(req, socket) {
    const upgrade = (req.headers.upgrade || '').toLowerCase();
    const key = req.headers['sec-websocket-key'];

    if (upgrade !== 'websocket' || !key) {
      socket.write('HTTP/1.1 400 Bad Request\r\n\r\n');
      socket.destroy();
      return;
    }

    const accept = crypto.createHash('sha1')
      .update(key + WS_MAGIC)
      .digest('base64');

    const response = [
      'HTTP/1.1 101 Switching Protocols',
      'Upgrade: websocket',
      'Connection: Upgrade',
      `Sec-WebSocket-Accept: ${accept}`,
      '',
      ''
    ].join('\r\n');

    socket.write(response);

    const conn = new WSConnection(socket);
    this.emit('connection', conn, req);
  }

  close(callback) {
    this.httpServer.close(callback);
  }
}

// ---------- Relay: WS server + JSON-RPC client ----------

export class Relay {
  constructor({ wsPort = 3459, host = '127.0.0.1' } = {}) {
    this.wsPort = wsPort;
    this.host = host;
    this.wss = null;
    this.ws = null;        // active WSConnection or null
    this.pending = new Map();  // id → { resolve, reject, timer }
    this.pingTimer = null;
    this.lastPongAt = 0;
    this._extensionReadyResolve = null;
    this._extensionReadyReject = null;

    this._startServer();
    this._startHeartbeat();
  }

  _startServer() {
    this.wss = new WebSocketServer({
      port: this.wsPort,
      host: this.host,
      httpHandler: (req, res) => this._handleHttpRequest(req, res),
    });

    this.wss.on('listening', () => {
      log('Listening on', `ws://${this.host}:${this.wsPort}`);
      log('HTTP API at', `http://${this.host}:${this.wsPort}/api/`);
    });

    this.wss.on('error', (err) => {
      log('Server error:', err.message);
    });

    this.wss.on('connection', (conn) => {
      if (this.ws) {
        // First-connection-wins: a connection is already active
        log('Rejecting new connection (already have one)');
        conn.close(1000, 'busy');
        return;
      }

      log('Extension connected');
      this.ws = conn;
      this.lastPongAt = Date.now();

      if (this._extensionReadyResolve) {
        this._extensionReadyResolve();
        this._extensionReadyResolve = null;
        this._extensionReadyReject = null;
      }

      conn.on('message', (text) => this._onMessage(text));
      conn.on('close', () => this._onClose());
      conn.on('error', (err) => log('Connection error:', err.message));
    });
  }

  _handleHttpRequest(req, res) {
    const url = new URL(req.url, `http://${req.headers.host}`);

    if (url.pathname === '/api/status' && req.method === 'GET') {
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        extensionConnected: !!this.ws,
        wsPort: this.wsPort,
      }));
      return;
    }

    if (url.pathname === '/api/call' && req.method === 'POST') {
      let body = '';
      req.on('data', (chunk) => { body += chunk; });
      req.on('end', async () => {
        let parsed;
        try {
          parsed = JSON.parse(body);
        } catch {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'invalid JSON body' }));
          return;
        }
        const { op, params = {}, timeout, logFile } = parsed;
        if (!op) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'missing "op" field' }));
          return;
        }
        if (!this.ws) {
          try {
            await this.waitForExtension({ timeout: 5_000 });
          } catch {
            res.writeHead(503, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Extension not connected (waited 5s for reconnect)' }));
            return;
          }
        }
        const startTime = Date.now();
        try {
          const result = await this.call(op, params, timeout ? { timeout } : {});
          const duration = Date.now() - startTime;

          if (logFile) {
            await appendFile(logFile, JSON.stringify({
              op, params,
              result: truncateForLog(result),
              timestamp: new Date().toISOString(),
              channel: 'extension_relay',
              duration_ms: duration,
            }) + '\n', 'utf-8');
          }

          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ result }));
        } catch (err) {
          if (logFile) {
            try {
              await appendFile(logFile, JSON.stringify({
                op, params,
                error: err.message,
                timestamp: new Date().toISOString(),
                channel: 'extension_relay',
                duration_ms: Date.now() - startTime,
              }) + '\n', 'utf-8');
            } catch {}
          }
          const status = err.message?.includes('not connected') ? 503 : 500;
          res.writeHead(status, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: err.message }));
        }
      });
      return;
    }

    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      error: 'Not Found',
      endpoints: ['GET /api/status', 'POST /api/call'],
    }));
  }

  _startHeartbeat() {
    this.pingTimer = setInterval(() => {
      if (!this.ws) return;
      const sinceLastPong = Date.now() - this.lastPongAt;
      if (sinceLastPong > PING_TIMEOUT) {
        log('No pong for', Math.round(sinceLastPong / 1000), 's, closing');
        this.ws.close(1000, 'pong timeout');
        return;
      }
      this._sendPing().catch(() => {});
    }, PING_INTERVAL);
  }

  async _sendPing() {
    try {
      await this.call('ping', {}, { timeout: 5_000 });
    } catch (err) {
      log('Ping failed:', err.message);
    }
  }

  _onMessage(text) {
    let msg;
    try {
      msg = JSON.parse(text);
    } catch (e) {
      log('Invalid JSON from extension:', text.slice(0, 100));
      return;
    }
    if (!msg || !msg.id) return;

    // Track pong
    if (msg.id === '__pong__') {
      this.lastPongAt = Date.now();
      return;
    }

    const pending = this.pending.get(msg.id);
    if (!pending) return;

    clearTimeout(pending.timer);
    this.pending.delete(msg.id);

    if (msg.error) {
      const err = new Error(msg.error.message || 'Unknown error');
      err.code = msg.error.code;
      pending.reject(err);
    } else {
      pending.resolve(msg.result);
    }
  }

  _onClose() {
    log('Extension disconnected');
    this.ws = null;
    for (const [, p] of this.pending) {
      clearTimeout(p.timer);
      p.reject(new Error('Extension disconnected'));
    }
    this.pending.clear();
  }

  // Wait for the extension to connect. Resolves on connection, rejects on timeout.
  waitForExtension({ timeout = DEFAULT_CONNECT_TIMEOUT } = {}) {
    if (this.ws) return Promise.resolve();

    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this._extensionReadyResolve = null;
        this._extensionReadyReject = null;
        reject(new Error(`Extension did not connect within ${timeout}ms. Is the extension loaded in Chrome?`));
      }, timeout);

      this._extensionReadyResolve = () => {
        clearTimeout(timer);
        resolve();
      };
      this._extensionReadyReject = (err) => {
        clearTimeout(timer);
        reject(err);
      };
    });
  }

  // Send a JSON-RPC request to the extension.
  call(op, params = {}, { timeout = DEFAULT_REQUEST_TIMEOUT } = {}) {
    return new Promise((resolve, reject) => {
      if (!this.ws) {
        reject(new Error('Extension not connected'));
        return;
      }

      const id = randomUUID();
      const timer = setTimeout(() => {
        this.pending.delete(id);
        reject(new Error(`Request '${op}' timed out after ${timeout}ms`));
      }, timeout);

      this.pending.set(id, { resolve, reject, timer });
      this.ws.send(JSON.stringify({ id, op, params }));
    });
  }

  // ---- Convenience API (skill.mjs calls these) ----
  //
  // page.eval 是核心: 传入任意 JS 字符串, 扩展里走 executeScript (受 page CSP 限制).

  tab = {
    list:      (opts = {})    => this.call('tab.list', opts),
    create:    (params)    => this.call('tab.create', params),
    close:     (tabId)     => this.call('tab.close', { tabId }),
    setStatus: (tabId, status) => this.call('tab.setStatus', { tabId, status }),
    groupInfo: (opts = {}) => this.call('tab.groupInfo', opts),
  };

  // 任务分组: 每个任务一个 Chrome Tab Group, 多任务结构隔离.
  // group.create -> { groupId }; tab.create({url, groupId}); tab.list({groupId});
  // page.* 可带 groupId 做归属校验; 结束 group.close({groupId}).
  group = {
    create:    (name) => this.call('group.create', { name }),
    close:     (groupId) => this.call('group.close', { groupId }),
    list:      ()     => this.call('group.list'),
    setStatus: (groupId, status) => this.call('group.setStatus', { groupId, status }),
  };

  page = {
    eval:      (tabId, code, groupId) => this.call('page.eval', { tabId, code, groupId }),
    ariaTree:  (tabId, opts = {}) => this.call('page.ariaTree', { tabId, ...opts }),
    getText:   (tabId, opts = {}) => this.call('page.getText', { tabId, ...opts }),
    fillForm:  (tabId, ref, value, groupId) => this.call('page.fillForm', { tabId, ref, value, groupId }),
    scrollTo:  (tabId, ref, groupId) => this.call('page.scrollTo', { tabId, ref, groupId }),
    screenshot:(tabId) => this.call('page.screenshot', { tabId }),
    search:    (tabId, query, opts = {}) => this.call('page.search', { tabId, query, ...opts }),
    click:     (tabId, ref, groupId) => this.call('page.click', { tabId, ref, groupId }),
    waitForElement: (tabId, selector, opts = {}) => this.call('page.waitForElement', { tabId, selector, ...opts }),
  };

  async close() {
    if (this.pingTimer) {
      clearInterval(this.pingTimer);
      this.pingTimer = null;
    }
    if (this.ws) {
      try { this.ws.close(1000, 'relay closing'); } catch {}
      this.ws = null;
    }
    if (this.wss) {
      await new Promise((resolve) => this.wss.close(() => resolve()));
      this.wss = null;
    }
  }
}
