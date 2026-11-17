import net from "node:net";
import { encodeCommand, parseProtocolFrame, ProtocolError, nextRequestId } from "./protocol.mjs";
import { PROTOCOL_CATALOG } from "./catalog.mjs";

const ACTIVE_CONNECTIONS = new Map();

export class TransportError extends Error {
  constructor(code, message, details = {}) {
    super(message);
    this.name = "TransportError";
    this.code = code;
    this.details = sanitize(details);
  }
}

export class CRLFFrameParser {
  constructor({ maxFrameBytes = PROTOCOL_CATALOG.limits.maxFrameBytes, maxBufferBytes = PROTOCOL_CATALOG.limits.maxBufferBytes } = {}) {
    this.maxFrameBytes = maxFrameBytes;
    this.maxBufferBytes = maxBufferBytes;
    this.buffer = Buffer.alloc(0);
  }

  push(chunk) {
    const value = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    if (value.length === 0) return [];
    this.buffer = Buffer.concat([this.buffer, value]);
    if (this.buffer.length > this.maxBufferBytes) throw new TransportError("buffer_too_large", "The device connection buffer exceeded its limit.");
    const frames = [];
    while (true) {
      const delimiter = this.buffer.indexOf(Buffer.from("\r\n"));
      const newline = this.buffer.indexOf(0x0a);
      if (newline >= 0 && (delimiter < 0 || newline < delimiter)) throw new TransportError("framing_invalid", "The device connection used LF without CRLF.");
      if (delimiter < 0) {
        if (this.buffer.length > this.maxFrameBytes) throw new TransportError("frame_too_large", "The device frame exceeded its limit.");
        break;
      }
      const frame = this.buffer.subarray(0, delimiter);
      this.buffer = this.buffer.subarray(delimiter + 2);
      if (frame.length > this.maxFrameBytes) throw new TransportError("frame_too_large", "The device frame exceeded its limit.");
      if (frame.length) frames.push(frame.toString("utf8"));
    }
    return frames;
  }

  finish() {
    if (this.buffer.length) throw new TransportError("trailing_frame", "The device closed with an incomplete CRLF frame.");
  }
}

export class SlidingQuota {
  constructor({ limit = 60, windowMs = 60000, now = () => Date.now() } = {}) {
    this.limit = limit;
    this.windowMs = windowMs;
    this.now = now;
    this.events = [];
  }

  consume(count = 1) {
    const now = this.now();
    this.events = this.events.filter((timestamp) => timestamp > now - this.windowMs);
    if (this.events.length + count > this.limit) return false;
    for (let index = 0; index < count; index += 1) this.events.push(now);
    return true;
  }

  remaining() {
    const now = this.now();
    this.events = this.events.filter((timestamp) => timestamp > now - this.windowMs);
    return Math.max(0, this.limit - this.events.length);
  }
}

export class YeelightTransport {
  constructor({
    host,
    port = PROTOCOL_CATALOG.limits.controlPort,
    socketFactory = (endpoint) => net.createConnection(endpoint),
    maxFrameBytes = PROTOCOL_CATALOG.limits.maxFrameBytes,
    maxBufferBytes = PROTOCOL_CATALOG.limits.maxBufferBytes,
    commandTimeoutMs = 3000,
    connectionTimeoutMs = 3000,
    maxConnections = PROTOCOL_CATALOG.limits.maxConnectionsPerDevice,
    quota = new SlidingQuota({ limit: PROTOCOL_CATALOG.limits.commandsPerMinutePerConnection }),
    globalQuota = new SlidingQuota({ limit: PROTOCOL_CATALOG.limits.commandsPerMinutePerLan }),
    onNotification = null,
  } = {}) {
    if (typeof host !== "string" || !host) throw new TransportError("endpoint_invalid", "A control host is required.");
    this.endpoint = { host, port };
    this.socketFactory = socketFactory;
    this.maxFrameBytes = maxFrameBytes;
    this.maxBufferBytes = maxBufferBytes;
    this.commandTimeoutMs = commandTimeoutMs;
    this.connectionTimeoutMs = connectionTimeoutMs;
    this.maxConnections = maxConnections;
    this.quota = quota;
    this.globalQuota = globalQuota;
    this.notificationHandlers = new Set();
    if (typeof onNotification === "function") this.notificationHandlers.add(onNotification);
    this.socket = null;
    this.parser = new CRLFFrameParser({ maxFrameBytes, maxBufferBytes });
    this.pending = new Map();
    this.requestId = 0;
    this.state = "idle";
    this.openPromise = null;
    this.warnings = [];
    this.connectionRegistered = false;
  }

  async open() {
    if (this.state === "open") return this;
    if (this.openPromise) return this.openPromise;
    const key = `${this.endpoint.host}:${this.endpoint.port}`;
    const active = ACTIVE_CONNECTIONS.get(key) || 0;
    if (active >= this.maxConnections) throw new TransportError("connection_limit", "The device connection limit is already in use.");
    ACTIVE_CONNECTIONS.set(key, active + 1);
    this.connectionRegistered = true;
    this.state = "opening";
    this.openPromise = new Promise((resolve, reject) => {
      let settled = false;
      let timer;
      const socket = this.socketFactory({ host: this.endpoint.host, port: this.endpoint.port });
      this.socket = socket;
      const fail = (error) => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        this.state = "closed";
        this.releaseConnection();
        reject(error instanceof TransportError ? error : new TransportError("connect_failed", "The device connection could not be opened."));
      };
      const ready = () => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        this.state = "open";
        resolve(this);
      };
      socket.on("data", (chunk) => this.handleData(chunk));
      socket.once("error", (error) => {
        if (!settled) fail(new TransportError("connect_failed", "The device connection failed.", { name: error?.code || "socket_error" }));
        else this.failPending(new TransportError("socket_error", "The device connection failed."));
      });
      socket.once("close", () => {
        if (!settled) fail(new TransportError("connect_closed", "The device closed before the connection was ready."));
        else this.handleClosed();
      });
      socket.once("connect", ready);
      timer = setTimeout(() => fail(new TransportError("connect_timeout", "The device connection timed out.")), this.connectionTimeoutMs);
    }).finally(() => { this.openPromise = null; });
    return this.openPromise;
  }

  async request(method, params, { timeoutMs = this.commandTimeoutMs, signal, validate = true, support } = {}) {
    await this.open();
    if (!this.quota.consume() || !this.globalQuota.consume()) throw new TransportError("quota_exhausted", "The LAN command quota is temporarily exhausted.");
    const id = this.allocateRequestId();
    const frame = encodeCommand(id, method, params, { validate, support, maxFrameBytes: this.maxFrameBytes });
    return new Promise((resolve, reject) => {
      let settled = false;
      const timer = setTimeout(() => finish(new TransportError("request_timeout", "The device did not respond before the request deadline.")), timeoutMs);
      const finish = (error, result) => {
        if (settled) return;
        settled = true;
        clearTimeout(timer);
        this.pending.delete(id);
        if (signal) signal.removeEventListener("abort", onAbort);
        if (error) reject(error); else resolve(result);
      };
      const onAbort = () => finish(new TransportError("request_aborted", "The device request was cancelled."));
      this.pending.set(id, { resolve: (result) => finish(null, result), reject: finish });
      if (signal) {
        if (signal.aborted) return onAbort();
        signal.addEventListener("abort", onAbort, { once: true });
      }
      try { this.socket.write(frame); } catch { finish(new TransportError("write_failed", "The device command could not be written.")); }
    });
  }

  onProps(handler) {
    if (typeof handler !== "function") throw new TypeError("notification handler must be a function");
    this.notificationHandlers.add(handler);
    return () => this.notificationHandlers.delete(handler);
  }

  async collectNotifications({ durationMs = 1000, maxNotifications = 32, signal } = {}) {
    await this.open();
    if (!Number.isInteger(durationMs) || durationMs < 1 || durationMs > 60000) throw new TransportError("watch_duration_invalid", "The notification watch duration is outside its bound.");
    const rows = [];
    return new Promise((resolve) => {
      let timer;
      const off = this.onProps((notification) => { if (rows.length < maxNotifications) rows.push(notification); if (rows.length >= maxNotifications) finish(); });
      const abort = () => finish();
      const finish = () => { clearTimeout(timer); off(); if (signal) signal.removeEventListener("abort", abort); resolve(rows); };
      timer = setTimeout(finish, durationMs);
      if (signal) {
        if (signal.aborted) finish();
        else signal.addEventListener("abort", abort, { once: true });
      }
    });
  }

  async executeBatch(commands, { pacingMs = 100, signal } = {}) {
    if (!Array.isArray(commands) || commands.length > 32) throw new TransportError("batch_limit", "The command batch exceeds its safety bound.");
    const results = [];
    try {
      for (const command of commands) {
        if (signal?.aborted) throw new TransportError("request_aborted", "The command batch was cancelled.");
        results.push(await this.request(command.method, command.params, { signal, support: command.support }));
        if (pacingMs > 0 && command !== commands.at(-1)) await new Promise((resolve) => setTimeout(resolve, pacingMs));
      }
      return results;
    } finally {
      if (signal?.aborted) this.close();
    }
  }

  close() {
    if (this.state === "closed" || this.state === "idle") return;
    this.state = "closed";
    this.failPending(new TransportError("connection_closed", "The device connection was closed."));
    try { this.parser.finish(); } catch {}
    try { this.socket?.end?.(); } catch {}
    try { this.socket?.destroy?.(); } catch {}
    this.releaseConnection();
    this.socket = null;
  }

  handleData(chunk) {
    try {
      for (const frame of this.parser.push(chunk)) this.handleFrame(frame);
    } catch (error) {
      this.warnings.push(error?.code || "frame_invalid");
      this.failPending(error instanceof TransportError ? error : new TransportError("frame_invalid", "The device frame was invalid."));
      this.close();
    }
  }

  handleFrame(frame) {
    let message;
    try { message = parseProtocolFrame(frame, { maxFrameBytes: this.maxFrameBytes }); } catch (error) {
      this.warnings.push(error?.code || "protocol_invalid");
      return;
    }
    if (message.kind === "notification") {
      for (const handler of this.notificationHandlers) { try { handler(message.props); } catch {} }
      return;
    }
    if (message.kind === "result") {
      const pending = this.pending.get(message.id);
      if (pending) pending.resolve(message.result);
      else this.warnings.push("orphan_result");
      return;
    }
    if (message.kind === "error") {
      const pending = this.pending.get(message.id);
      if (pending) pending.reject(new TransportError("device_error", message.error.message, { deviceCode: message.error.code }));
      else this.warnings.push("orphan_error");
      return;
    }
    this.warnings.push("unknown_message");
  }

  handleClosed() {
    if (this.state !== "closed") this.state = "closed";
    this.failPending(new TransportError("connection_closed", "The device connection was closed."));
    this.releaseConnection();
  }

  failPending(error) {
    for (const pending of this.pending.values()) pending.reject(error);
    this.pending.clear();
  }

  allocateRequestId() {
    this.requestId = nextRequestId(this.requestId);
    while (this.pending.has(this.requestId)) this.requestId = nextRequestId(this.requestId);
    return this.requestId;
  }

  releaseConnection() {
    if (!this.connectionRegistered) return;
    this.connectionRegistered = false;
    const key = `${this.endpoint.host}:${this.endpoint.port}`;
    const count = ACTIVE_CONNECTIONS.get(key) || 0;
    if (count <= 1) ACTIVE_CONNECTIONS.delete(key); else ACTIVE_CONNECTIONS.set(key, count - 1);
  }
}

export const TcpTransport = YeelightTransport;
export const FrameParser = CRLFFrameParser;
export const createTransport = (options) => new YeelightTransport(options);
export const createFrameParser = (options) => new CRLFFrameParser(options);

function sanitize(details) {
  const output = {};
  for (const [key, value] of Object.entries(details).slice(0, 8)) if (typeof value === "string" || typeof value === "number" || typeof value === "boolean") output[key] = typeof value === "string" ? value.slice(0, 120) : value;
  return output;
}
