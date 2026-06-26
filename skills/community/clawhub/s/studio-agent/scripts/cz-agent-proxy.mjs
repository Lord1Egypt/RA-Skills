#!/usr/bin/env node

import path from "node:path";
import { createInterface } from "node:readline";
import process, { env as hostEnv } from "node:process";
import { fileURLToPath } from "node:url";
import { discoverStudioEnv, resolveAutoDiscoveryInput } from "./clickzetta-discovery.mjs";
import {
  isRecord,
  extractTokenFromWsUrl,
  parseTokenClaims,
} from "./utils.mjs";

const PROXY_VERSION = "v1";
const DEFAULT_SESSION_ID = "openclaw-session";
const UNKNOWN_ID = "unknown";
const STARTUP_ID = "startup";
const DEFAULT_CONVERSATION_TITLE = "OpenClaw Session";

const SUPPORTED_OPS = new Set(["user_input", "stop"]);
const ALLOWED_IDENTITY_STRING_KEYS = [
  "user_id",
  "tenant_id",
  "instance_id",
  "session_id",
  "token",
  "instance_name",
  "workspace",
  "workspace_id",
  "env",
  "region_id",
  "region_code",
  "base_url",
  "login_url",
  "project_id",
  "project_name",
  "username",
];

const CODE_PROTOCOL_ERROR = "PROTOCOL_ERROR";
const CODE_NETWORK_ERROR = "NETWORK_ERROR";
const CODE_REMOTE_ERROR = "REMOTE_ERROR";
const CODE_REMOTE_TIMEOUT = "REMOTE_TIMEOUT";

function nowMs() {
  return Date.now();
}

// proxy uses a stricter asTrimmedString that only accepts string type
function asTrimmedString(value) {
  if (typeof value !== "string") {
    return undefined;
  }
  const trimmed = value.trim();
  return trimmed ? trimmed : undefined;
}

function asIdentityFieldValue(value) {
  const text = asTrimmedString(value);
  if (text !== undefined) {
    return text;
  }
  if (typeof value === "number" && Number.isFinite(value)) {
    return String(Math.trunc(value));
  }
  return undefined;
}

function asObjectOrUndefined(value) {
  if (!isRecord(value)) {
    return undefined;
  }
  return value;
}

function asMetadata(value) {
  if (value === undefined || value === null) {
    return {};
  }
  if (!isRecord(value)) {
    return null;
  }
  return { ...value };
}

function readStringListEnv(name, env = hostEnv) {
  const raw = asTrimmedString(env[name]);
  if (!raw) {
    return [];
  }
  const values = raw
    .split(",")
    .map((item) => item.trim())
    .filter((item) => item.length > 0);
  return [...new Set(values)];
}

function normalizeUserInputMetadata(metadata, userInput, alwaysAllowTools = []) {
  const next = { ...metadata };
  if (!asTrimmedString(next.source)) {
    next.source = "openclaw";
  }

  const hasConfigs = Array.isArray(next.configs) && next.configs.length > 0;
  if (!hasConfigs) {
    // Frontend clients send a text config segment by default.
    // Mirror that shape for closer backend behavior parity in CLI mode.
    next.configs = [{ type: "text", value: userInput }];
  }

  const hasAlwaysAllowTools =
    Array.isArray(next.always_allow_tools) && next.always_allow_tools.length > 0;
  if (!hasAlwaysAllowTools && alwaysAllowTools.length > 0) {
    next.always_allow_tools = [...alwaysAllowTools];
  }

  return next;
}

function readIntEnv(name, fallback, min = 1, env = hostEnv) {
  const value = env[name];
  if (value === undefined) {
    return fallback;
  }
  const parsed = Number.parseInt(String(value).trim(), 10);
  if (!Number.isFinite(parsed) || parsed < min) {
    return fallback;
  }
  return parsed;
}

function readBoolEnv(name, fallback, env = hostEnv) {
  const value = asTrimmedString(env[name]);
  if (value === undefined) {
    return fallback;
  }
  const normalized = value.toLowerCase();
  if (["1", "true", "yes", "on"].includes(normalized)) {
    return true;
  }
  if (["0", "false", "no", "off"].includes(normalized)) {
    return false;
  }
  return fallback;
}

function readInterruptDecisionModeEnv(name, fallback, env = hostEnv) {
  const value = asTrimmedString(env[name]);
  if (!value) {
    return fallback;
  }
  const normalized = value.toLowerCase();
  if (["auto_approve", "approve", "auto-approve"].includes(normalized)) {
    return "auto_approve";
  }
  if (["auto_reject", "reject", "auto-reject"].includes(normalized)) {
    return "auto_reject";
  }
  if (["off", "manual", "disabled"].includes(normalized)) {
    return "off";
  }
  return fallback;
}

function createEvent({
  event,
  requestId,
  conversationId,
  opType,
  delta = null,
  content = null,
  complete,
  metadata = {},
  error = null,
}) {
  return {
    version: PROXY_VERSION,
    event,
    request_id: requestId,
    conversation_id: conversationId,
    op_type: opType,
    delta,
    content,
    complete,
    metadata,
    error,
  };
}

function createErrorEvent({ requestId, conversationId, code, message, metadata = {} }) {
  return createEvent({
    event: "error",
    requestId,
    conversationId,
    opType: "error",
    delta: null,
    content: null,
    complete: true,
    metadata,
    error: {
      code,
      message,
    },
  });
}

function writeEvent(event) {
  process.stdout.write(`${JSON.stringify(event)}\n`);
}

function resolveIdentity(rawIdentity, token, env = hostEnv) {
  const raw = asObjectOrUndefined(rawIdentity);
  const envIdentity = {
    user_id: asTrimmedString(env.CZ_USER_ID),
    tenant_id: asTrimmedString(env.CZ_TENANT_ID),
    instance_id: asTrimmedString(env.CZ_INSTANCE_ID),
    instance_name: asTrimmedString(env.CZ_INSTANCE_NAME),
    project_id: asTrimmedString(env.CZ_PROJECT_ID),
    project_name: asTrimmedString(env.CZ_PROJECT_NAME),
    workspace: asTrimmedString(env.CZ_WORKSPACE),
    workspace_id: asTrimmedString(env.CZ_WORKSPACE_ID),
    username: asTrimmedString(env.CZ_USERNAME),
    session_id: asTrimmedString(env.CZ_SESSION_ID) ?? DEFAULT_SESSION_ID,
    token,
  };

  const identity = { ...envIdentity };

  if (raw) {
    for (const key of ALLOWED_IDENTITY_STRING_KEYS) {
      const value = asIdentityFieldValue(raw[key]);
      if (value !== undefined) {
        identity[key] = value;
      }
    }
  }

  if (!identity.token && token) {
    identity.token = token;
  }

  // Some deployments only provide token + minimal IDs.
  // Derive user/tenant/username from JWT payload when possible.
  const tokenClaims = parseTokenClaims(identity.token);
  if (tokenClaims) {
    if (!identity.user_id) {
      identity.user_id =
        asIdentityFieldValue(tokenClaims.userId) ?? asIdentityFieldValue(tokenClaims.user_id);
    }
    if (!identity.tenant_id) {
      identity.tenant_id =
        asIdentityFieldValue(tokenClaims.tenantId) ??
        asIdentityFieldValue(tokenClaims.tenant_id) ??
        asIdentityFieldValue(tokenClaims.accountId) ??
        asIdentityFieldValue(tokenClaims.account_id);
    }
    if (!identity.username) {
      identity.username =
        asIdentityFieldValue(tokenClaims.userName) ??
        asIdentityFieldValue(tokenClaims.username);
    }
  }

  if (!identity.user_id || !identity.tenant_id || !identity.instance_id) {
    return {
      ok: false,
      message:
        "identity requires non-empty user_id, tenant_id, instance_id (from stdin.identity or env CZ_USER_ID/CZ_TENANT_ID/CZ_INSTANCE_ID)",
    };
  }

  if (!identity.session_id) {
    identity.session_id = DEFAULT_SESSION_ID;
  }

  return {
    ok: true,
    identity,
  };
}

function parseInboundLine(raw, token, defaultConversationId, env = hostEnv) {
  if (!isRecord(raw)) {
    return {
      ok: false,
      event: createErrorEvent({
        requestId: UNKNOWN_ID,
        conversationId: UNKNOWN_ID,
        code: CODE_PROTOCOL_ERROR,
        message: "stdin line must be a JSON object",
      }),
    };
  }

  const requestId = asTrimmedString(raw.request_id) ?? UNKNOWN_ID;
  const conversationId = asTrimmedString(raw.conversation_id) ?? defaultConversationId ?? UNKNOWN_ID;
  const version = asTrimmedString(raw.version);

  if (version !== PROXY_VERSION) {
    return {
      ok: false,
      event: createErrorEvent({
        requestId,
        conversationId,
        code: CODE_PROTOCOL_ERROR,
        message: `unsupported version: ${version ?? "<missing>"}`,
      }),
    };
  }

  const op = asTrimmedString(raw.op);
  if (!op || !SUPPORTED_OPS.has(op)) {
    return {
      ok: false,
      event: createErrorEvent({
        requestId,
        conversationId,
        code: CODE_PROTOCOL_ERROR,
        message: `unsupported op: ${op ?? "<missing>"}`,
      }),
    };
  }

  if (requestId === UNKNOWN_ID || conversationId === UNKNOWN_ID) {
    return {
      ok: false,
      event: createErrorEvent({
        requestId,
        conversationId,
        code: CODE_PROTOCOL_ERROR,
        message:
          "request_id and conversation_id are required (conversation_id can come from stdin, CZ_CONVERSATION_ID, or CZ_AUTO_CREATE_CONVERSATION bootstrap)",
      }),
    };
  }

  const identityResult = resolveIdentity(raw.identity, token, env);
  if (!identityResult.ok) {
    return {
      ok: false,
      event: createErrorEvent({
        requestId,
        conversationId,
        code: CODE_PROTOCOL_ERROR,
        message: identityResult.message,
      }),
    };
  }

  const metadata = asMetadata(raw.metadata);
  if (metadata === null) {
    return {
      ok: false,
      event: createErrorEvent({
        requestId,
        conversationId,
        code: CODE_PROTOCOL_ERROR,
        message: "metadata must be an object when provided",
      }),
    };
  }

  let userInput;
  if (op === "user_input") {
    userInput = asTrimmedString(raw.user_input);
    if (!userInput) {
      return {
        ok: false,
        event: createErrorEvent({
          requestId,
          conversationId,
          code: CODE_PROTOCOL_ERROR,
          message: "user_input is required for op=user_input",
        }),
      };
    }
  }

  const normalizedMetadata =
    op === "user_input" && userInput
      ? normalizeUserInputMetadata(metadata, userInput, readStringListEnv("CZ_ALWAYS_ALLOW_TOOLS", env))
      : metadata;

  const studioMessage = {
    op_type: op,
    identity: identityResult.identity,
    request_id: requestId,
    conversation_id: conversationId,
    timestamp: nowMs(),
    ...(userInput ? { user_input: userInput } : {}),
    metadata: normalizedMetadata,
  };

  return {
    ok: true,
    requestId,
    conversationId,
    op,
    studioMessage,
  };
}

function normalizeOutbound(raw) {
  if (!isRecord(raw)) {
    return null;
  }
  const opType = asTrimmedString(raw.op_type);
  const requestId = asTrimmedString(raw.request_id);
  const conversationId = asTrimmedString(raw.conversation_id);
  if (!opType || !requestId || !conversationId) {
    return null;
  }

  const metadata = asMetadata(raw.metadata);
  return {
    opType,
    requestId,
    conversationId,
    interruptId: asIdentityFieldValue(raw.interrupt_id),
    complete: raw.complete === true,
    delta: typeof raw.delta === "string" ? raw.delta : null,
    content: typeof raw.content === "string" ? raw.content : null,
    metadata: metadata ?? {},
  };
}

function asObjectArray(value) {
  if (!Array.isArray(value)) {
    return [];
  }
  return value.filter((item) => isRecord(item));
}

function buildInterruptDecisions(message, decisionValue) {
  const metadata = asObjectOrUndefined(message.metadata) ?? {};
  const interrupts = asObjectArray(metadata.interrupts);
  const topLevelActionRequests = asObjectArray(metadata.action_requests);
  const decisions = [];

  const pushDecisions = (interruptId, actionRequests, fallbackInterruptId = "decisions") => {
    const resolvedInterruptId =
      asIdentityFieldValue(interruptId) ?? asIdentityFieldValue(fallbackInterruptId) ?? "decisions";
    const actions = asObjectArray(actionRequests);

    if (actions.length === 0) {
      decisions.push({
        interrupt_id: resolvedInterruptId,
        decision: [decisionValue],
      });
      return;
    }

    for (const action of actions) {
      const toolCallId = asIdentityFieldValue(action.id);
      if (toolCallId) {
        decisions.push({
          interrupt_id: resolvedInterruptId,
          decision: [decisionValue],
          tool_call_id: toolCallId,
        });
      } else {
        decisions.push({
          interrupt_id: resolvedInterruptId,
          decision: [decisionValue],
        });
      }
    }
  };

  if (interrupts.length > 0) {
    for (const interrupt of interrupts) {
      pushDecisions(interrupt.interrupt_id, interrupt.action_requests, "interrupt_0");
    }
  } else {
    pushDecisions(message.interruptId ?? "decisions", topLevelActionRequests, "decisions");
  }

  if (decisions.length === 0) {
    decisions.push({
      interrupt_id: "decisions",
      decision: [decisionValue],
    });
  }

  return decisions;
}

function resolveFinalContent(message, accumulatedAgentText) {
  const accumulated = asTrimmedString(accumulatedAgentText);
  if (message.opType !== "agent_message" && accumulated) {
    return accumulated;
  }
  const content = asTrimmedString(message.content);
  if (content) {
    return content;
  }
  if (accumulated) {
    return accumulated;
  }
  const delta = asTrimmedString(message.delta);
  return delta ?? null;
}

function parseCreatedConversationId(message) {
  if (message.opType !== "conversation_created") {
    return undefined;
  }
  if (typeof message.content === "string" && message.content.trim()) {
    try {
      const parsed = JSON.parse(message.content);
      const cid = asTrimmedString(parsed?.conversation_id);
      if (cid) {
        return cid;
      }
    } catch {
      // ignore malformed content JSON
    }
  }
  return asTrimmedString(message.conversationId);
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function toWebSocketText(data) {
  if (typeof data === "string") {
    return Promise.resolve(data);
  }
  if (data instanceof ArrayBuffer) {
    return Promise.resolve(Buffer.from(data).toString("utf8"));
  }
  if (ArrayBuffer.isView(data)) {
    return Promise.resolve(
      Buffer.from(data.buffer, data.byteOffset, data.byteLength).toString("utf8"),
    );
  }
  if (typeof Blob !== "undefined" && data instanceof Blob) {
    return data.text();
  }
  return Promise.resolve(String(data));
}

function resolveWsUrl(baseUrl, token) {
  if (!token) {
    return baseUrl;
  }
  try {
    const parsed = new URL(baseUrl);
    if (!parsed.searchParams.has("x-clickzetta-token")) {
      parsed.searchParams.set("x-clickzetta-token", token);
    }
    return parsed.toString();
  } catch {
    return baseUrl;
  }
}

async function connectWebSocket({ url, token, timeoutMs }) {
  if (typeof globalThis.WebSocket === "undefined") {
    throw new Error(
      "WebSocket is not available. Node.js >= 22 is required (or use a WebSocket polyfill).",
    );
  }
  const targetUrl = resolveWsUrl(url, token);
  return await new Promise((resolve, reject) => {
    let settled = false;

    let ws;
    try {
      // Keep browser-compatible WebSocket usage. Node's global WebSocket does not
      // support arbitrary header options in the constructor.
      ws = new WebSocket(targetUrl);
    } catch (error) {
      reject(error instanceof Error ? error : new Error(String(error)));
      return;
    }

    const timer = setTimeout(() => {
      if (settled) {
        return;
      }
      settled = true;
      try {
        ws.close();
      } catch {
        // ignore
      }
      reject(new Error(`WebSocket connect timeout after ${timeoutMs}ms`));
    }, timeoutMs);

    const cleanup = () => {
      clearTimeout(timer);
      ws.removeEventListener("open", onOpen);
      ws.removeEventListener("error", onError);
      ws.removeEventListener("close", onClose);
    };

    const onOpen = () => {
      if (settled) {
        return;
      }
      settled = true;
      cleanup();
      resolve(ws);
    };

    const onError = (event) => {
      if (settled) {
        return;
      }
      settled = true;
      cleanup();
      const message = event?.error?.message || "WebSocket connection error";
      reject(new Error(message));
    };

    const onClose = (event) => {
      if (settled) {
        return;
      }
      settled = true;
      cleanup();
      reject(
        new Error(
          `WebSocket closed before open (code=${event.code}, reason=${event.reason || ""})`,
        ),
      );
    };

    ws.addEventListener("open", onOpen);
    ws.addEventListener("error", onError);
    ws.addEventListener("close", onClose);
  });
}

class CzAgentProxy {
  constructor(options = {}) {
    this.env = isRecord(options.env) ? { ...options.env } : hostEnv;
    this.onEvent = typeof options.onEvent === "function" ? options.onEvent : writeEvent;

    this.wsUrl = asTrimmedString(this.env.CZ_AGENT_WS_URL);
    this.token = asTrimmedString(this.env.CZ_AGENT_TOKEN) ?? extractTokenFromWsUrl(this.wsUrl);
    this.defaultConversationId = asTrimmedString(this.env.CZ_CONVERSATION_ID);
    this.autoCreateConversation = readBoolEnv("CZ_AUTO_CREATE_CONVERSATION", true, this.env);
    this.autoConversationTitle =
      asTrimmedString(this.env.CZ_CONVERSATION_TITLE) ?? DEFAULT_CONVERSATION_TITLE;

    this.requestTimeoutMs = readIntEnv("CZ_REQUEST_TIMEOUT_SECONDS", 120, 1, this.env) * 1000;
    this.stopGraceMs = readIntEnv("CZ_STOP_GRACE_SECONDS", 10, 1, this.env) * 1000;
    this.startupConnectTimeoutMs =
      readIntEnv("CZ_STARTUP_CONNECT_TIMEOUT_SECONDS", 10, 1, this.env) * 1000;
    this.reconnectMaxAttempts = readIntEnv("CZ_RECONNECT_MAX_ATTEMPTS", 3, 1, this.env);
    this.interruptDecisionMode = readInterruptDecisionModeEnv(
      "CZ_INTERRUPT_DECISION_MODE",
      "auto_approve",
      this.env,
    );
    this.emitAssistantDeltas = readBoolEnv("CZ_EMIT_ASSISTANT_DELTAS", false, this.env);

    this.socket = null;
    this.readline = null;
    this.shuttingDown = false;
    this.stdinClosed = false;

    this.reconnectPromise = null;
    this.requestTimeoutTimer = null;
    this.stopGraceTimer = null;

    this.activeRequest = null;
    this.lineChain = Promise.resolve();

    this.doneResolve = null;
    this.done = new Promise((resolve) => {
      this.doneResolve = resolve;
    });

    this.onSigint = () => {
      this.shutdown(0);
    };
    this.onSigterm = () => {
      this.shutdown(0);
    };
  }

  emitEvent(event) {
    this.onEvent(event);
  }

  async start() {
    if (!this.wsUrl) {
      await this.tryRuntimeDiscovery();
    }

    if (!this.wsUrl) {
      this.emitEvent(
        createErrorEvent({
          requestId: STARTUP_ID,
          conversationId: STARTUP_ID,
          code: CODE_PROTOCOL_ERROR,
          message:
            "missing studio runtime connection info; configure CZ_STUDIO_JDBC_URL, or use file-mode CZ_STUDIO_DOMAIN/CZ_STUDIO_USERNAME/CZ_STUDIO_PASSWORD, or provide manual CZ_AGENT_WS_URL",
        }),
      );
      return false;
    }

    const startupConnected = await this.connectAtStartup();
    if (!startupConnected) {
      return false;
    }

    process.on("SIGINT", this.onSigint);
    process.on("SIGTERM", this.onSigterm);
    return true;
  }

  async run() {
    const started = await this.start();
    if (!started) {
      return 1;
    }

    this.readline = createInterface({ input: process.stdin, crlfDelay: Infinity });
    this.readline.on("line", (line) => {
      this.lineChain = this.lineChain
        .then(async () => {
          await this.handleLine(line);
        })
        .catch((error) => {
          this.emitEvent(
            createErrorEvent({
              requestId: UNKNOWN_ID,
              conversationId: UNKNOWN_ID,
              code: CODE_PROTOCOL_ERROR,
              message: `line handler error: ${String(error)}`,
            }),
          );
        });
    });
    this.readline.on("close", () => {
      this.stdinClosed = true;
      if (!this.activeRequest) {
        this.shutdown(0);
      }
    });

    return await this.done;
  }

  async tryRuntimeDiscovery() {
    const autoInput = resolveAutoDiscoveryInput({}, this.env);
    if (!autoInput) {
      return;
    }

    const discovered = await discoverStudioEnv(autoInput);
    for (const [key, value] of Object.entries(discovered.env)) {
      this.env[key] = value;
    }
    this.wsUrl = asTrimmedString(this.env.CZ_AGENT_WS_URL);
    this.token = asTrimmedString(this.env.CZ_AGENT_TOKEN) ?? extractTokenFromWsUrl(this.wsUrl);
  }

  async connectAtStartup() {
    try {
      await this.connectAndBind(this.startupConnectTimeoutMs);
      return true;
    } catch (error) {
      this.emitEvent(
        createErrorEvent({
          requestId: STARTUP_ID,
          conversationId: STARTUP_ID,
          code: CODE_NETWORK_ERROR,
          message: `startup connection failed: ${error instanceof Error ? error.message : String(error)}`,
        }),
      );
      return false;
    }
  }

  async connectAndBind(timeoutMs) {
    const ws = await connectWebSocket({
      url: this.wsUrl,
      token: this.token,
      timeoutMs,
    });

    this.socket = ws;
    await this.bootstrapConversationIfNeeded(ws, timeoutMs);

    ws.addEventListener("message", (event) => {
      void this.onSocketMessage(event.data);
    });
    ws.addEventListener("close", () => {
      if (this.socket === ws) {
        this.socket = null;
      }
      if (!this.shuttingDown) {
        void this.ensureConnected();
      }
    });
    ws.addEventListener("error", () => {
      // close handler handles reconnect
    });
  }

  async bootstrapConversationIfNeeded(ws, timeoutMs) {
    if (this.defaultConversationId || !this.autoCreateConversation) {
      return;
    }

    const identityResult = resolveIdentity(undefined, this.token, this.env);
    if (!identityResult.ok) {
      return;
    }

    const now = nowMs();
    const tempConversationId = `temp-${now}`;
    const createRequestId = `startup-create-${now}`;
    const createMessage = {
      op_type: "create_conversation",
      identity: identityResult.identity,
      request_id: createRequestId,
      conversation_id: tempConversationId,
      timestamp: now,
      metadata: {
        title: this.autoConversationTitle,
        source: "openclaw",
      },
    };

    this.defaultConversationId = await this.sendAndWaitConversationCreated({
      ws,
      message: createMessage,
      timeoutMs,
    });
  }

  async sendAndWaitConversationCreated({ ws, message, timeoutMs }) {
    return await new Promise((resolve, reject) => {
      let settled = false;

      const cleanup = () => {
        ws.removeEventListener("message", onMessage);
        ws.removeEventListener("close", onClose);
        ws.removeEventListener("error", onError);
        clearTimeout(timer);
      };

      const fail = (error) => {
        if (settled) {
          return;
        }
        settled = true;
        cleanup();
        reject(error);
      };

      const succeed = (conversationId) => {
        if (settled) {
          return;
        }
        settled = true;
        cleanup();
        resolve(conversationId);
      };

      const timer = setTimeout(() => {
        fail(new Error(`create_conversation timeout after ${timeoutMs}ms`));
      }, timeoutMs);

      const onClose = (event) => {
        fail(new Error(`WebSocket closed during create_conversation (code=${event.code})`));
      };

      const onError = () => {
        fail(new Error("WebSocket error during create_conversation"));
      };

      const onMessage = (event) => {
        void (async () => {
          const text = await toWebSocketText(event.data);
          let parsed;
          try {
            parsed = JSON.parse(text);
          } catch {
            return;
          }
          const outbound = normalizeOutbound(parsed);
          if (!outbound || outbound.requestId !== message.request_id) {
            return;
          }
          if (outbound.opType === "error") {
            fail(
              new Error(
                `create_conversation rejected: ${outbound.content || outbound.delta || "remote error"}`,
              ),
            );
            return;
          }
          const conversationId = parseCreatedConversationId(outbound);
          if (conversationId) {
            succeed(conversationId);
          }
        })().catch((error) => {
          fail(error instanceof Error ? error : new Error(String(error)));
        });
      };

      ws.addEventListener("message", onMessage);
      ws.addEventListener("close", onClose);
      ws.addEventListener("error", onError);

      try {
        ws.send(JSON.stringify(message));
      } catch (error) {
        fail(error instanceof Error ? error : new Error(String(error)));
      }
    });
  }

  async ensureConnected() {
    if (this.shuttingDown) {
      return false;
    }
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      return true;
    }
    if (this.reconnectPromise) {
      return await this.reconnectPromise;
    }

    this.reconnectPromise = this.reconnectLoop();
    try {
      return await this.reconnectPromise;
    } finally {
      this.reconnectPromise = null;
    }
  }

  async reconnectLoop() {
    for (let attempt = 1; attempt <= this.reconnectMaxAttempts; attempt += 1) {
      if (this.shuttingDown) {
        return false;
      }
      if (attempt > 1) {
        await sleep(500 * (attempt - 1));
      }
      try {
        await this.connectAndBind(this.startupConnectTimeoutMs);
        return true;
      } catch {
        // continue retries
      }
    }

    if (this.activeRequest) {
      this.emitActiveNetworkError("WebSocket reconnect attempts exhausted");
    }

    return false;
  }

  async handleLine(line) {
    if (this.shuttingDown) {
      return;
    }
    const trimmed = line.trim();
    if (!trimmed) {
      return;
    }

    let raw;
    try {
      raw = JSON.parse(trimmed);
    } catch {
      this.emitEvent(
        createErrorEvent({
          requestId: UNKNOWN_ID,
          conversationId: UNKNOWN_ID,
          code: CODE_PROTOCOL_ERROR,
          message: "stdin line is not valid JSON",
        }),
      );
      return;
    }

    const fallbackConversationId =
      this.activeRequest?.conversationId ?? this.defaultConversationId ?? UNKNOWN_ID;
    const parsed = parseInboundLine(raw, this.token, fallbackConversationId, this.env);
    if (!parsed.ok) {
      this.emitEvent(parsed.event);
      return;
    }

    if (parsed.op === "user_input") {
      await this.handleUserInput(parsed);
      return;
    }

    await this.handleStop(parsed);
  }

  async handleUserInput(parsed) {
    if (this.activeRequest) {
      this.emitEvent(
        createErrorEvent({
          requestId: parsed.requestId,
          conversationId: parsed.conversationId,
          code: CODE_PROTOCOL_ERROR,
          message: "CONCURRENT_REQUEST_NOT_SUPPORTED",
        }),
      );
      return;
    }

    const connected = await this.ensureConnected();
    if (!connected) {
      this.emitEvent(
        createErrorEvent({
          requestId: parsed.requestId,
          conversationId: parsed.conversationId,
          code: CODE_NETWORK_ERROR,
          message: "WebSocket is unavailable",
        }),
      );
      return;
    }

    this.activeRequest = {
      requestId: parsed.requestId,
      conversationId: parsed.conversationId,
      accumulatedAgentText: "",
      lastAgentContent: "",
      identity: parsed.studioMessage.identity,
      baseMetadata: parsed.studioMessage.metadata,
      autoInterruptDecisions: 0,
      lastActivityAtMs: nowMs(),
    };
    this.resetRequestTimeoutTimer();

    const sent = await this.sendStudioMessage(parsed.studioMessage);
    if (!sent) {
      this.emitActiveNetworkError("failed to send user_input to Studio WebSocket");
    }
  }

  async handleStop(parsed) {
    if (!this.activeRequest) {
      this.emitEvent(
        createErrorEvent({
          requestId: parsed.requestId,
          conversationId: parsed.conversationId,
          code: CODE_PROTOCOL_ERROR,
          message: "NO_ACTIVE_REQUEST",
        }),
      );
      return;
    }

    const connected = await this.ensureConnected();
    if (!connected) {
      this.emitActiveNetworkError("WebSocket is unavailable while handling stop");
      return;
    }

    const sent = await this.sendStudioMessage(parsed.studioMessage);
    if (!sent) {
      this.emitActiveNetworkError("failed to send stop to Studio WebSocket");
      return;
    }

    this.startStopGraceTimer();
  }

  async sendStudioMessage(message) {
    const ws = this.socket;
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      return false;
    }

    try {
      ws.send(JSON.stringify(message));
      return true;
    } catch {
      return false;
    }
  }

  resolveAgentDelta(message) {
    if (!this.activeRequest || message.opType !== "agent_message") {
      return null;
    }

    let delta = typeof message.delta === "string" ? message.delta : null;
    const content = typeof message.content === "string" ? message.content : null;

    if ((!delta || delta.length === 0) && content !== null) {
      const previous = this.activeRequest.lastAgentContent ?? "";
      if (!previous) {
        delta = content;
      } else if (content.startsWith(previous)) {
        delta = content.slice(previous.length);
      } else {
        delta = content;
      }
    }

    if (content !== null) {
      this.activeRequest.lastAgentContent = content;
    }

    return delta;
  }

  async handleInterruptRequest(message) {
    if (!this.activeRequest) {
      return false;
    }

    if (this.interruptDecisionMode === "off") {
      this.emitEvent(
        createErrorEvent({
          requestId: message.requestId,
          conversationId: message.conversationId,
          code: CODE_PROTOCOL_ERROR,
          message:
            "interrupt_request received but CZ_INTERRUPT_DECISION_MODE=off. Set mode to auto_approve or auto_reject.",
        }),
      );
      this.clearActiveRequest();
      return false;
    }

    const decisionValue = this.interruptDecisionMode === "auto_reject" ? "reject" : "approve";
    const interruptDecisions = buildInterruptDecisions(message, decisionValue);
    const baseMetadata = asObjectOrUndefined(this.activeRequest.baseMetadata) ?? {};
    const decisionMetadata = {
      source: "openclaw",
      auto_interrupt_decision: decisionValue,
    };
    if (
      Array.isArray(baseMetadata.always_allow_tools) &&
      baseMetadata.always_allow_tools.length > 0
    ) {
      decisionMetadata.always_allow_tools = [...baseMetadata.always_allow_tools];
    }

    const decisionMessage = {
      op_type: "interrupt_decision",
      identity: this.activeRequest.identity,
      request_id: message.requestId,
      conversation_id: message.conversationId,
      interrupt_decisions: interruptDecisions,
      timestamp: nowMs(),
      metadata: decisionMetadata,
    };

    const sent = await this.sendStudioMessage(decisionMessage);
    if (!sent) {
      this.emitActiveNetworkError("failed to send interrupt_decision to Studio WebSocket");
      return false;
    }

    this.activeRequest.autoInterruptDecisions += 1;
    if (this.emitAssistantDeltas) {
      this.emitEvent(
        createEvent({
          event: "assistant_delta",
          requestId: message.requestId,
          conversationId: message.conversationId,
          opType: message.opType,
          delta: null,
          content: null,
          complete: false,
          metadata: {
            auto_interrupt_decision: decisionValue,
            auto_interrupt_decision_count: this.activeRequest.autoInterruptDecisions,
          },
          error: null,
        }),
      );
    }

    return true;
  }

  async onSocketMessage(rawData) {
    if (!this.activeRequest) {
      return;
    }

    const text = await toWebSocketText(rawData);
    let parsed;
    try {
      parsed = JSON.parse(text);
    } catch {
      return;
    }

    const message = normalizeOutbound(parsed);
    if (!message) {
      return;
    }

    if (message.requestId !== this.activeRequest.requestId) {
      return;
    }

    this.activeRequest.lastActivityAtMs = nowMs();
    this.resetRequestTimeoutTimer();

    const agentDelta = this.resolveAgentDelta(message);
    if (message.opType === "agent_message" && agentDelta) {
      this.activeRequest.accumulatedAgentText += agentDelta;
    }

    if (message.opType === "interrupt_request") {
      await this.handleInterruptRequest(message);
      return;
    }

    // error with complete=true is a terminal state
    if (message.opType === "error" && message.complete) {
      this.emitEvent(
        createErrorEvent({
          requestId: message.requestId,
          conversationId: message.conversationId,
          code: CODE_REMOTE_ERROR,
          message: message.content || message.delta || "remote error",
          metadata: message.metadata,
        }),
      );
      this.clearActiveRequest();
      return;
    }

    // op_type "end" is the real terminal signal from Studio agent
    if (message.opType === "end") {
      const finalContent = resolveFinalContent(message, this.activeRequest.accumulatedAgentText);
      this.emitEvent(
        createEvent({
          event: "assistant_final",
          requestId: message.requestId,
          conversationId: message.conversationId,
          opType: message.opType,
          delta: null,
          content: finalContent,
          complete: true,
          metadata: {},
          error: null,
        }),
      );
      this.clearActiveRequest();
      return;
    }

    // Everything else (agent_message, etc.) is intermediate — accumulate and optionally emit deltas
    if (this.emitAssistantDeltas) {
      this.emitEvent(
        createEvent({
          event: "assistant_delta",
          requestId: message.requestId,
          conversationId: message.conversationId,
          opType: message.opType,
          delta: message.opType === "agent_message" ? agentDelta : null,
          content: null,
          complete: false,
          metadata: {},
          error: null,
        }),
      );
    }
  }

  resetRequestTimeoutTimer() {
    if (this.requestTimeoutTimer) {
      clearTimeout(this.requestTimeoutTimer);
      this.requestTimeoutTimer = null;
    }

    if (!this.activeRequest) {
      return;
    }

    this.requestTimeoutTimer = setTimeout(() => {
      if (!this.activeRequest) {
        return;
      }
      this.emitEvent(
        createErrorEvent({
          requestId: this.activeRequest.requestId,
          conversationId: this.activeRequest.conversationId,
          code: CODE_REMOTE_TIMEOUT,
          message: `request timed out after ${Math.round(this.requestTimeoutMs / 1000)}s without complete=true`,
        }),
      );
      this.clearActiveRequest();
    }, this.requestTimeoutMs);
  }

  startStopGraceTimer() {
    if (this.stopGraceTimer) {
      clearTimeout(this.stopGraceTimer);
      this.stopGraceTimer = null;
    }
    if (!this.activeRequest) {
      return;
    }

    this.stopGraceTimer = setTimeout(() => {
      if (!this.activeRequest) {
        return;
      }
      this.emitEvent(
        createErrorEvent({
          requestId: this.activeRequest.requestId,
          conversationId: this.activeRequest.conversationId,
          code: CODE_REMOTE_TIMEOUT,
          message: `stop grace window exceeded (${Math.round(this.stopGraceMs / 1000)}s)`,
        }),
      );
      this.clearActiveRequest();
    }, this.stopGraceMs);
  }

  emitActiveNetworkError(reason) {
    if (!this.activeRequest) {
      return;
    }
    this.emitEvent(
      createErrorEvent({
        requestId: this.activeRequest.requestId,
        conversationId: this.activeRequest.conversationId,
        code: CODE_NETWORK_ERROR,
        message: reason,
      }),
    );
    this.clearActiveRequest();
  }

  clearActiveRequest() {
    this.activeRequest = null;

    if (this.requestTimeoutTimer) {
      clearTimeout(this.requestTimeoutTimer);
      this.requestTimeoutTimer = null;
    }
    if (this.stopGraceTimer) {
      clearTimeout(this.stopGraceTimer);
      this.stopGraceTimer = null;
    }

    if (this.stdinClosed) {
      this.shutdown(0);
    }
  }

  shutdown(code) {
    if (this.shuttingDown) {
      return;
    }
    this.shuttingDown = true;

    if (this.requestTimeoutTimer) {
      clearTimeout(this.requestTimeoutTimer);
      this.requestTimeoutTimer = null;
    }
    if (this.stopGraceTimer) {
      clearTimeout(this.stopGraceTimer);
      this.stopGraceTimer = null;
    }

    if (this.readline) {
      try {
        this.readline.close();
      } catch {
        // ignore
      }
      this.readline = null;
    }

    if (this.socket) {
      try {
        this.socket.close();
      } catch {
        // ignore
      }
      this.socket = null;
    }

    process.off("SIGINT", this.onSigint);
    process.off("SIGTERM", this.onSigterm);

    this.doneResolve(code);
  }
}

export async function runProxyOneShot({
  env,
  requestId,
  conversationId,
  userInput,
  hardTimeoutMs,
}) {
  const events = [];
  let finalEvent = null;
  let errorEvent = null;

  let resolveDone;
  let rejectDone;
  const done = new Promise((resolve, reject) => {
    resolveDone = resolve;
    rejectDone = reject;
  });

  const proxy = new CzAgentProxy({
    env,
    onEvent(event) {
      events.push(event);
      const eventRequestId = asTrimmedString(event?.request_id);
      const eventName = asTrimmedString(event?.event);
      if (eventName === "error" && (eventRequestId === STARTUP_ID || eventRequestId === requestId)) {
        errorEvent = event;
        resolveDone();
      }
      if (eventName === "assistant_final" && eventRequestId === requestId && event?.complete === true) {
        finalEvent = event;
        resolveDone();
      }
    },
  });

  let hardTimer = null;
  if (hardTimeoutMs > 0) {
    hardTimer = setTimeout(() => {
      rejectDone(new Error(`one-shot hard timeout after ${Math.round(hardTimeoutMs / 1000)}s`));
      proxy.shutdown(0);
    }, hardTimeoutMs);
  }

  try {
    const started = await proxy.start();
    if (!started) {
      return { events, finalEvent, errorEvent };
    }

    const outbound = {
      version: PROXY_VERSION,
      op: "user_input",
      request_id: requestId,
      conversation_id: conversationId,
      user_input: userInput,
      metadata: {
        source: "openclaw",
        configs: [{ type: "text", value: userInput }],
      },
    };

    const fallbackConversationId = proxy.defaultConversationId ?? conversationId ?? UNKNOWN_ID;
    const parsed = parseInboundLine(outbound, proxy.token, fallbackConversationId, proxy.env);
    if (!parsed.ok) {
      proxy.emitEvent(parsed.event);
      return { events, finalEvent, errorEvent: parsed.event };
    }

    await proxy.handleUserInput(parsed);
    await done;
    return { events, finalEvent, errorEvent };
  } finally {
    if (hardTimer) {
      clearTimeout(hardTimer);
    }
    proxy.shutdown(0);
  }
}

async function main() {
  const proxy = new CzAgentProxy();
  const code = await proxy.run();
  if (code !== 0) {
    process.exitCode = code;
  }
}

function isDirectExecution() {
  const entryPath = process.argv[1];
  if (!entryPath) {
    return false;
  }
  return path.resolve(entryPath) === path.resolve(fileURLToPath(import.meta.url));
}

if (isDirectExecution()) {
  void main().catch((error) => {
    writeEvent(
      createErrorEvent({
        requestId: STARTUP_ID,
        conversationId: STARTUP_ID,
        code: CODE_PROTOCOL_ERROR,
        message: `startup failed: ${error instanceof Error ? error.message : String(error)}`,
      }),
    );
    process.exitCode = 1;
  });
}
