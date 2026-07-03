import { resolve } from "node:path";
import { ActionGate, FileStore, loadConfig } from "../../../src/core/index.ts";
import { beforeDispatch, messageSending, messageSent } from "../../../src/adapters/openclaw/index.ts";

let definePluginEntry = (entry) => entry;
try {
  ({ definePluginEntry } = await import("openclaw/plugin-sdk/plugin-entry"));
} catch {
  // OpenClaw is an optional peer dependency so package tests and static inspection
  // can run outside an OpenClaw runtime. The real runtime provides definePluginEntry.
}

const PLUGIN_ID = "openclaw-action-gate";
const DEFAULT_PLUGIN_CONFIG = {
  enabled: false,
  modeDefault: "observe",
  serviceUrl: undefined,
  failClosedProtectedPublicSends: true
};

const configSchema = {
  jsonSchema: {
    type: "object",
    additionalProperties: false,
    properties: {
      enabled: { type: "boolean", default: false },
      modeDefault: { type: "string", enum: ["disabled", "observe", "enforce", "public_frozen"], default: "observe" },
      serviceUrl: { type: "string" },
      failClosedProtectedPublicSends: { type: "boolean", default: true }
    }
  },
  parse(value) {
    return normalizePluginConfig(value);
  },
  validate(value) {
    try {
      return { ok: true, value: normalizePluginConfig(value) };
    } catch (error) {
      return { ok: false, errors: [String(error instanceof Error ? error.message : error)] };
    }
  }
};

let pluginConfig = { ...DEFAULT_PLUGIN_CONFIG };
let pluginRootDir = resolve(import.meta.dirname, "..");
let gatePromise;
let gateFactory = createDefaultGate;
const pendingDedupeByMessage = new Map();

export async function beforeDispatchHandler(event, ctx = {}) {
  if (!isRuntimeEnabled()) return undefined;
  const gate = await gateFactory();
  const result = await beforeDispatch(gate, toClaimInboundRequest(event, ctx));
  if (result.handled) return { handled: true, text: "" };
  return { handled: false };
}

export async function messageSendingHandler(event, ctx = {}) {
  if (!isRuntimeEnabled()) return undefined;
  const gate = await gateFactory();
  const request = toReserveOutboxRequest(event, ctx);
  const result = await messageSending(gate, request);
  pendingDedupeByMessage.set(outboundFingerprint(event, ctx), result.dedupe_key);

  const metadata = {
    ...asRecord(event.metadata),
    actionGate: {
      ...asRecord(asRecord(event.metadata).actionGate),
      pluginId: PLUGIN_ID,
      decision: result.decision,
      dedupeKey: result.dedupe_key,
      ownerAgent: result.owner_agent
    }
  };

  if (!result.policy.send_allowed) {
    return {
      cancel: true,
      cancelReason: result.reason ?? result.decision,
      metadata
    };
  }

  return { metadata };
}

export async function messageSentHandler(event, ctx = {}) {
  if (!isRuntimeEnabled()) return undefined;
  const dedupeKey = readActionGateString(event, "dedupeKey")
    ?? readActionGateString(event, "dedupe_key")
    ?? pendingDedupeByMessage.get(outboundFingerprint(event, ctx));
  if (!dedupeKey) return undefined;

  const gate = await gateFactory();
  await messageSent(gate, {
    dedupe_key: dedupeKey,
    discord_message_id: typeof event.messageId === "string" ? event.messageId : undefined,
    result: event.success === false ? "failed" : "sent",
    metadata: {
      pluginId: PLUGIN_ID,
      to: event.to,
      sessionKey: event.sessionKey ?? ctx.sessionKey,
      runId: event.runId ?? ctx.runId,
      error: event.error
    }
  });
  pendingDedupeByMessage.delete(outboundFingerprint(event, ctx));
  return undefined;
}

export function configureActionGatePluginForTests(options = {}) {
  pluginConfig = { ...DEFAULT_PLUGIN_CONFIG, ...normalizePluginConfig(options.pluginConfig ?? options) };
  if (options.pluginRootDir) pluginRootDir = options.pluginRootDir;
  if (options.gateFactory) gateFactory = options.gateFactory;
  gatePromise = undefined;
  pendingDedupeByMessage.clear();
}

export function resetActionGatePluginForTests() {
  pluginConfig = { ...DEFAULT_PLUGIN_CONFIG };
  pluginRootDir = resolve(import.meta.dirname, "..");
  gateFactory = createDefaultGate;
  gatePromise = undefined;
  pendingDedupeByMessage.clear();
}

export function normalizePluginConfig(value) {
  const raw = asRecord(value);
  const modeDefault = typeof raw.modeDefault === "string" ? raw.modeDefault : DEFAULT_PLUGIN_CONFIG.modeDefault;
  if (!["disabled", "observe", "enforce", "public_frozen"].includes(modeDefault)) {
    throw new Error(`invalid modeDefault: ${modeDefault}`);
  }
  return {
    enabled: typeof raw.enabled === "boolean" ? raw.enabled : DEFAULT_PLUGIN_CONFIG.enabled,
    modeDefault,
    serviceUrl: typeof raw.serviceUrl === "string" && raw.serviceUrl.length > 0 ? raw.serviceUrl : undefined,
    failClosedProtectedPublicSends:
      typeof raw.failClosedProtectedPublicSends === "boolean"
        ? raw.failClosedProtectedPublicSends
        : DEFAULT_PLUGIN_CONFIG.failClosedProtectedPublicSends
  };
}

function configureRuntime(api) {
  pluginConfig = normalizePluginConfig(api.pluginConfig);
  pluginRootDir = typeof api.rootDir === "string" ? api.rootDir : pluginRootDir;
  gateFactory = createDefaultGate;
  gatePromise = undefined;
}

function isRuntimeEnabled() {
  if (process.env.ACTION_GATE_ENABLED === "false") return false;
  return pluginConfig.enabled === true;
}

async function createDefaultGate() {
  gatePromise ??= (async () => {
    const configPath = process.env.ACTION_GATE_CONFIG || resolve(pluginRootDir, "../../config/scopes.yaml");
    const config = await loadConfig(configPath);
    config.enabled = true;
    config.mode_default = pluginConfig.modeDefault;
    config.fail_closed_protected_public_sends = pluginConfig.failClosedProtectedPublicSends;
    config.service_url = pluginConfig.serviceUrl ?? "embedded://openclaw-plugin";
    if (pluginConfig.serviceUrl) {
      return new RemoteActionGate(pluginConfig.serviceUrl);
    }
    const storePath = process.env.ACTION_GATE_STORE || resolve(pluginRootDir, "../../.action-gate/state.json");
    const gate = new ActionGate(config, new FileStore(storePath));
    await gate.init();
    return gate;
  })();
  return gatePromise;
}

class RemoteActionGate {
  constructor(serviceUrl) {
    this.serviceUrl = serviceUrl.replace(/\/+$/, "");
  }

  async claimInbound(request) {
    return this.post("/claim-inbound", request);
  }

  async reserveOutbox(request) {
    return this.post("/reserve-outbox", request);
  }

  async completeOutbox(request) {
    return this.post("/complete-outbox", request);
  }

  async post(path, payload) {
    const response = await fetch(this.serviceUrl + path, {
      method: "POST",
      headers: { "content-type": "application/json", "user-agent": `${PLUGIN_ID}/0.1.0` },
      body: JSON.stringify(payload)
    });
    const text = await response.text();
    const data = text ? JSON.parse(text) : {};
    if (!response.ok) throw new Error(`Action Gate service ${path} failed: ${response.status} ${data.error ?? text}`);
    return data;
  }
}

function toClaimInboundRequest(event, ctx) {
  return {
    scope_key: resolveScopeKey(event, ctx),
    source_message_id: stringValue(event.messageId ?? ctx.messageId ?? event.timestamp) ?? "unknown-message",
    action_class: readActionGateString(event, "actionClass") ?? readActionGateString(event, "action_class") ?? "discord_ingress",
    runtime: "openclaw",
    agent: resolveAgent(event, ctx)
  };
}

function toReserveOutboxRequest(event, ctx) {
  return {
    scope_key: resolveScopeKey(event, ctx),
    logical_action_key:
      readActionGateString(event, "logicalActionKey")
      ?? readActionGateString(event, "logical_action_key")
      ?? outboundFingerprint(event, ctx),
    action_type: readActionGateString(event, "actionType") ?? readActionGateString(event, "action_type") ?? "message_send",
    runtime: "openclaw",
    agent: resolveAgent(event, ctx),
    content: typeof event.content === "string" ? event.content : undefined,
    metadata: {
      pluginId: PLUGIN_ID,
      to: event.to,
      threadId: event.threadId,
      replyToId: event.replyToId,
      sessionKey: ctx.sessionKey,
      runId: ctx.runId
    }
  };
}

function resolveScopeKey(event, ctx) {
  const explicit = readActionGateString(event, "scopeKey") ?? readActionGateString(event, "scope_key");
  if (explicit) return explicit;

  const metadata = asRecord(event.metadata);
  const accountId = stringValue(
    ctx.accountId
    ?? event.accountId
    ?? metadata.accountId
    ?? metadata.guildId
    ?? metadata.groupId
  ) ?? "unknown";

  const candidate = [
    event.threadId,
    metadata.threadId,
    event.messageThreadId,
    metadata.messageThreadId,
    event.to,
    metadata.to,
    ctx.conversationId,
    event.conversationId,
    metadata.conversationId,
    ctx.parentConversationId,
    event.channelId,
    metadata.channelId,
    event.channel,
    ctx.channelId
  ].map((value) => normalizeDiscordConversationId(value)).find(Boolean);

  return `discord:${accountId}:${candidate ?? "unknown"}`;
}

function normalizeDiscordConversationId(value) {
  const raw = stringValue(value);
  if (!raw) return undefined;
  for (const prefix of ["channel:", "chat:", "thread:", "discord:"]) {
    if (raw.startsWith(prefix)) return normalizeDiscordConversationId(raw.slice(prefix.length));
  }
  if (/^\d{8,}$/.test(raw)) return raw;
  return undefined;
}

function resolveAgent(event, ctx) {
  return readActionGateString(event, "agent")
    ?? stringValue(ctx.agentId ?? event.agentId ?? ctx.agent ?? event.agent)
    ?? stringValue(process.env.ACTION_GATE_AGENT)
    ?? "ada";
}

function outboundFingerprint(event, ctx) {
  return [
    resolveScopeKey(event, ctx),
    stringValue(event.to) ?? "",
    stringValue(event.threadId) ?? "",
    stringValue(event.replyToId) ?? "",
    typeof event.content === "string" ? event.content : ""
  ].join("|");
}

function readActionGateString(event, key) {
  const metadata = asRecord(event.metadata);
  const actionGate = asRecord(metadata.actionGate);
  return stringValue(actionGate[key] ?? metadata[key]);
}

function stringValue(value) {
  if (typeof value === "string" && value.length > 0) return value;
  if (typeof value === "number" || typeof value === "bigint") return String(value);
  return undefined;
}

function asRecord(value) {
  return value && typeof value === "object" && !Array.isArray(value) ? value : {};
}

export default definePluginEntry({
  id: "openclaw-action-gate",
  name: "OpenClaw Action Gate",
  description: "Scope-owned Discord ingress/egress gate",
  configSchema,
  register(api) {
    configureRuntime(api);
    api.on("before_dispatch", beforeDispatchHandler, { priority: 100 });
    api.on("message_sending", messageSendingHandler, { priority: 100 });
    api.on("message_sent", messageSentHandler, { priority: 100 });
  },
});
