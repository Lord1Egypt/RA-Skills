/**
 * WTT Cloud WebSocket Client — persistent connection to the WTT cloud service.
 *
 * Features:
 *   - Auto-reconnect with exponential backoff
 *   - In-band JWT auth
 *   - Heartbeat ping/pong (text frames, not WS ping)
 *   - Request/response correlation via request_id
 *   - E2E encryption (optional, per-account)
 *   - Server push handling (new_message, task_status)
 */

import type {
  WsAction,
  WsActionMessage,
  WsActionResult,
  WsServerMessage,
  WsNewMessage,
  WsTaskStatus,
  ActionPayloads,
  ResolvedWTTAccount,
} from "./types.js";
import {
  deriveKey,
  encryptText,
  decryptText,
  toBase64,
  fromBase64,
} from "./e2e-crypto.js";

type MessageHandler = (msg: WsNewMessage) => void;
type TaskStatusHandler = (msg: WsTaskStatus) => void;
type ConnectionHandler = () => void;
type ErrorHandler = (err: Error) => void;
type LogFn = (level: "debug" | "info" | "warn" | "error", msg: string, data?: unknown) => void;

export interface WTTCloudClientOptions {
  /** Fully resolved account */
  account: ResolvedWTTAccount;
  /** Callback for incoming messages */
  onMessage?: MessageHandler;
  /** Callback for task status changes */
  onTaskStatus?: TaskStatusHandler;
  /** Callback for connection open */
  onConnect?: ConnectionHandler;
  /** Callback for connection close */
  onDisconnect?: ConnectionHandler;
  /** Callback for errors */
  onError?: ErrorHandler;
  /** Logger function (defaults to console) */
  log?: LogFn;
  /** Heartbeat interval in ms (default: 30_000) */
  heartbeatInterval?: number;
  /** Max reconnect attempts (default: Infinity) */
  maxReconnectAttempts?: number;
}

interface PendingRequest {
  resolve: (data: unknown) => void;
  reject: (err: Error) => void;
  timer: ReturnType<typeof setTimeout>;
}

export class WTTCloudClient {
  private ws: WebSocket | import("ws").WebSocket | null = null;
  private account: ResolvedWTTAccount;
  private e2eKey: Uint8Array | null = null;
  private pending = new Map<string, PendingRequest>();
  private heartbeatTimer: ReturnType<typeof setInterval> | null = null;
  private reconnectTimer: ReturnType<typeof setTimeout> | null = null;
  private reconnectAttempts = 0;
  private maxReconnectAttempts: number;
  private heartbeatInterval: number;
  private closed = false;
  private reqCounter = 0;
  private wsUrlCursor = 0;

  // Handlers
  private onMessage?: MessageHandler;
  private onTaskStatus?: TaskStatusHandler;
  private onConnect?: ConnectionHandler;
  private onDisconnect?: ConnectionHandler;
  private onError?: ErrorHandler;
  private log: LogFn;

  constructor(opts: WTTCloudClientOptions) {
    this.account = opts.account;
    this.onMessage = opts.onMessage;
    this.onTaskStatus = opts.onTaskStatus;
    this.onConnect = opts.onConnect;
    this.onDisconnect = opts.onDisconnect;
    this.onError = opts.onError;
    this.heartbeatInterval = opts.heartbeatInterval ?? 30_000;
    this.maxReconnectAttempts = opts.maxReconnectAttempts ?? Infinity;
    this.log = opts.log ?? ((level, msg, data) => {
      const fn = level === "error" ? console.error : level === "warn" ? console.warn : console.log;
      fn(`[WTT-WS] ${msg}`, data ?? "");
    });
  }

  // ---------------------------------------------------------------------------
  // Lifecycle
  // ---------------------------------------------------------------------------

  async connect(): Promise<void> {
    this.closed = false;
    this.reconnectAttempts = 0;

    // Derive E2E key if password is configured
    if (this.account.config.e2ePassword) {
      this.log("info", "Deriving E2E key...");
      this.e2eKey = await deriveKey(this.account.config.e2ePassword, this.account.agentId);
      this.log("info", "E2E key derived");
    }

    this.doConnect();
  }

  disconnect(): void {
    this.closed = true;
    this.clearTimers();
    if (this.ws) {
      this.ws.close(1000, "client disconnect");
      this.ws = null;
    }
    // Reject all pending requests
    for (const [id, p] of this.pending) {
      clearTimeout(p.timer);
      p.reject(new Error("Client disconnected"));
    }
    this.pending.clear();
  }

  get connected(): boolean {
    if (!this.ws) return false;
    const state = (this.ws as WebSocket).readyState ?? (this.ws as import("ws").WebSocket).readyState;
    return state === 1; // OPEN
  }

  getAccount(): ResolvedWTTAccount {
    return { ...this.account, config: { ...this.account.config } };
  }

  hasE2EKey(): boolean {
    return Boolean(this.e2eKey && this.e2eKey.length > 0);
  }

  // ---------------------------------------------------------------------------
  // Actions (public API)
  // ---------------------------------------------------------------------------

  async sendAction<A extends WsAction>(
    action: A,
    payload: ActionPayloads[A],
    timeoutMs = 15_000,
  ): Promise<unknown> {
    if (!this.connected) throw new Error("Not connected to WTT cloud");

    const requestId = `${action}-${++this.reqCounter}-${Date.now().toString(36)}`;
    const msg: WsActionMessage = { action, request_id: requestId, ...payload };

    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this.pending.delete(requestId);
        reject(new Error(`Action ${action} timed out after ${timeoutMs}ms`));
      }, timeoutMs);

      this.pending.set(requestId, { resolve, reject, timer });
      this.send(JSON.stringify(msg));
    });
  }

  // Convenience methods
  async list(limit?: number) {
    return this.sendAction("list", { limit });
  }

  async find(query: string) {
    return this.sendAction("find", { query });
  }

  async join(topicId: string) {
    return this.sendAction("join", { topic_id: topicId });
  }

  async leave(topicId: string) {
    return this.sendAction("leave", { topic_id: topicId });
  }

  async subscribed() {
    return this.sendAction("subscribed", {} as Record<string, never>);
  }

  async publish(
    topicId: string,
    content: string,
    opts?: { contentType?: string; semanticType?: string; encrypt?: boolean; replyTo?: string },
  ) {
    let finalContent = content;
    let encrypted = false;

    if (opts?.encrypt && this.e2eKey) {
      const contextId = crypto.randomUUID();
      const ciphertext = await encryptText(this.e2eKey, content, contextId);
      finalContent = JSON.stringify({ c: toBase64(ciphertext), ctx: contextId });
      encrypted = true;
    }

    return this.sendAction("publish", {
      topic_id: topicId,
      content: finalContent,
      content_type: opts?.contentType,
      semantic_type: opts?.semanticType,
      reply_to: opts?.replyTo,
      encrypted,
    });
  }

  async poll(limit?: number) {
    return this.sendAction("poll", { limit });
  }

  async p2p(targetAgentId: string, content: string, encrypt = false) {
    let finalContent = content;
    let encrypted = false;

    if (encrypt && this.e2eKey) {
      const contextId = crypto.randomUUID();
      const ciphertext = await encryptText(this.e2eKey, content, contextId);
      finalContent = JSON.stringify({ c: toBase64(ciphertext), ctx: contextId });
      encrypted = true;
    }

    return this.sendAction("p2p", {
      target_agent_id: targetAgentId,
      content: finalContent,
      encrypted,
    });
  }

  async history(topicId: string, limit?: number, beforeId?: string) {
    return this.sendAction("history", {
      topic_id: topicId,
      limit,
      before_id: beforeId,
    });
  }

  async detail(topicId: string) {
    return this.sendAction("detail", { topic_id: topicId });
  }

  async typing(topicId: string, state: "start" | "stop", ttlMs = 6000) {
    return this.sendAction("typing", {
      topic_id: topicId,
      state,
      ttl_ms: ttlMs,
    });
  }

  // ---------------------------------------------------------------------------
  // E2E decryption helper (for consumers)
  // ---------------------------------------------------------------------------

  async decryptMessage(content: string): Promise<string> {
    if (!this.e2eKey) return content;
    try {
      const { c, ctx } = JSON.parse(content) as { c: string; ctx: string };
      if (!c || !ctx) return content;
      const ciphertext = fromBase64(c);
      return await decryptText(this.e2eKey, ciphertext, ctx);
    } catch {
      return content; // not encrypted or failed to decrypt
    }
  }

  // ---------------------------------------------------------------------------
  // Connection internals
  // ---------------------------------------------------------------------------

  private resolveWsUrls(): string[] {
    const raw = this.account.cloudUrl.replace(/\/$/, "");
    const direct = `${raw.replace(/^http/, "ws")}/ws/${this.account.agentId}`;

    const strippedRaw = raw.replace(/\/api\/v1\/?$/i, "");
    const stripped = `${strippedRaw.replace(/^http/, "ws")}/ws/${this.account.agentId}`;

    const urls = [stripped, direct].filter(Boolean);
    return Array.from(new Set(urls));
  }

  private async doConnect(): Promise<void> {
    const wsUrls = this.resolveWsUrls();
    const wsUrl = wsUrls[this.wsUrlCursor % wsUrls.length];

    this.log("info", `Connecting to ${wsUrl}`);

    try {
      if (typeof globalThis.WebSocket !== "undefined") {
        // Browser / Deno / CF Workers
        this.ws = new WebSocket(wsUrl);
      } else {
        // Node.js — use ws package
        const { default: WS } = await import("ws");
        this.ws = new WS(wsUrl) as unknown as WebSocket;
      }
    } catch (err) {
      this.log("error", "Failed to create WebSocket", err);
      this.scheduleReconnect();
      return;
    }

    const ws = this.ws;

    const onOpen = () => {
      this.log("info", "WebSocket connected, authenticating...");
      this.reconnectAttempts = 0;
      // Send auth as first message
      this.send(JSON.stringify({ action: "auth", token: this.account.token }));
      this.startHeartbeat();
      this.onConnect?.();
    };

    const onMessage = (event: MessageEvent | { data: unknown }) => {
      const raw = typeof event === "object" && "data" in event ? String(event.data) : String(event);
      if (raw === "pong") return; // heartbeat response

      try {
        const msg = JSON.parse(raw) as WsServerMessage;
        if (msg.type === "action_result") {
          this.log("debug", `WS action_result received: ok=${(msg as any).ok} keys=${Object.keys((msg as any).data ?? {}).join(",")}`);
        }
        this.handleServerMessage(msg);
      } catch {
        this.log("warn", "Non-JSON message received", raw);
      }
    };

    const onClose = (event: { code?: number; reason?: string }) => {
      const code = "code" in event ? event.code : undefined;
      const reason = "reason" in event ? event.reason : "";
      this.log("info", `WebSocket closed: ${code} ${reason}`);
      this.clearTimers();
      this.onDisconnect?.();

      if (!this.closed) {
        const wsUrls = this.resolveWsUrls();
        if (wsUrls.length > 1) {
          this.wsUrlCursor = (this.wsUrlCursor + 1) % wsUrls.length;
          this.log("info", `Switching WS endpoint candidate -> ${wsUrls[this.wsUrlCursor]}`);
        }
        this.scheduleReconnect();
      }
    };

    const onError = (err: Event | Error) => {
      const error = err instanceof Error ? err : new Error("WebSocket error");
      this.log("error", "WebSocket error", error);
      this.onError?.(error);
    };

    // Attach listeners (works for both browser WebSocket and ws package)
    if ("addEventListener" in ws) {
      ws.addEventListener("open", onOpen);
      ws.addEventListener("message", onMessage);
      ws.addEventListener("close", onClose);
      ws.addEventListener("error", onError);
    } else {
      const nodeWs = ws as unknown as import("ws").WebSocket;
      nodeWs.on("open", onOpen);
      nodeWs.on("message", (data) => onMessage({ data: data.toString() }));
      nodeWs.on("close", (code, reason) => onClose({ code, reason: reason?.toString() }));
      nodeWs.on("error", onError);
    }
  }

  private handleServerMessage(msg: WsServerMessage): void {
    if (msg.type === "action_result") {
      const result = msg as WsActionResult;
      // Capture agent display name from auth response
      if (result.ok && result.data && typeof result.data === "object") {
        const data = result.data as Record<string, unknown>;
        if (data.authenticated && data.agent_display_name) {
          this.account = { ...this.account, name: String(data.agent_display_name) };
          this.log("info", `Agent display name resolved: ${this.account.name}`);
        }
      }
      const p = this.pending.get(result.request_id);
      if (p) {
        clearTimeout(p.timer);
        this.pending.delete(result.request_id);
        if (result.ok) {
          p.resolve(result.data);
        } else {
          p.reject(new Error(result.error ?? "Action failed"));
        }
      }
      return;
    }

    if (msg.type === "new_message") {
      this.onMessage?.(msg as WsNewMessage);
      return;
    }

    if (msg.type === "task_status") {
      this.onTaskStatus?.(msg as WsTaskStatus);
      return;
    }

    if (msg.type === "e2e_key_request") {
      const requestId = String((msg as { request_id?: unknown }).request_id ?? "").trim();
      if (!requestId) return;
      this.log("info", `e2e_key_request received rid=${requestId}`);
      if (!this.e2eKey) {
        this.log("warn", `e2e_key_request rid=${requestId} failed: e2e_not_configured`);
        this.send(JSON.stringify({
          type: "e2e_key_response",
          request_id: requestId,
          ok: false,
          error: "e2e_not_configured",
        }));
        return;
      }

      this.send(JSON.stringify({
        type: "e2e_key_response",
        request_id: requestId,
        ok: true,
        key_b64: toBase64(this.e2eKey),
      }));
      this.log("info", `e2e_key_response sent rid=${requestId}`);
      return;
    }

    this.log("debug", "Unknown message type", msg);
  }

  // ---------------------------------------------------------------------------
  // Heartbeat & reconnect
  // ---------------------------------------------------------------------------

  private startHeartbeat(): void {
    this.stopHeartbeat();
    this.heartbeatTimer = setInterval(() => {
      if (this.connected) {
        this.send("ping"); // WTT uses text "ping", not WS ping frames
      }
    }, this.heartbeatInterval);
  }

  private stopHeartbeat(): void {
    if (this.heartbeatTimer) {
      clearInterval(this.heartbeatTimer);
      this.heartbeatTimer = null;
    }
  }

  private scheduleReconnect(): void {
    if (this.closed || this.reconnectAttempts >= this.maxReconnectAttempts) {
      this.log("warn", "Max reconnect attempts reached, giving up");
      return;
    }

    const delay = Math.min(1000 * 2 ** this.reconnectAttempts, 30_000);
    this.reconnectAttempts++;
    this.log("info", `Reconnecting in ${delay}ms (attempt ${this.reconnectAttempts})`);

    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null;
      this.doConnect();
    }, delay);
  }

  private clearTimers(): void {
    this.stopHeartbeat();
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }
  }

  private send(data: string): void {
    try {
      if (this.ws && this.connected) {
        (this.ws as WebSocket).send(data);
      }
    } catch (err) {
      this.log("error", "Send failed", err);
    }
  }
}
