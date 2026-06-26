/**
 * WTT Channel Plugin for OpenClaw.
 *
 * Scope of this module (P0/P1 foundation):
 * - Register WTT as a first-class channel plugin
 * - Manage per-account WS clients
 * - Provide outbound text/media delivery through WTT publish/p2p
 *
 * Command parity status:
 * - Core @wtt topic/message commands routed in src/commands/* (P2 first batch)
 * - task/pipeline/delegate command scaffolding available via HTTP API in src/commands/*
 */

import type {
  WTTAccountConfig,
  ResolvedWTTAccount,
  WsNewMessage,
  WsTaskStatus,
  WsMessagePayload,
} from "./types.js";
import type { WTTCommandProcessResult } from "./commands/router.js";
import type {
  WTTCommandAccountContext,
  WTTCommandRuntimeHooks,
  WTTTaskInferenceRuntimeRequest,
  WTTTaskInferenceUsage,
  WTTSessionRuntimeMetrics,
} from "./commands/types.js";
import { createWTTCommandRouter } from "./commands/router.js";
import { normalizeAccountContext } from "./commands/account.js";
import { executeTaskRunById } from "./commands/task.js";
import { createTaskStatusEventHandler } from "./runtime/task-status-handler.js";
import { WTTCloudClient } from "./ws-client.js";
import { mkdir, readFile, rename, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import os from "node:os";
import { dirname, extname, join as joinPath } from "node:path";
import { randomBytes } from "node:crypto";
import { pathToFileURL } from "node:url";

const DEFAULT_ACCOUNT_ID = "default";
const DEFAULT_CLOUD_URL = "https://www.waxbyte.com";
const CHANNEL_ID = "wtt";
const DEFAULT_INBOUND_POLL_INTERVAL_MS = 0;
const DEFAULT_INBOUND_POLL_LIMIT = 20;
const DEFAULT_INBOUND_DEDUP_WINDOW_MS = 5 * 60_000;
const DEFAULT_INBOUND_DEDUP_MAX_ENTRIES = 2000;
const DEFAULT_TASK_RECOVERY_INTERVAL_MS = 60_000;
const DEFAULT_TASK_RECOVERY_LOOKBACK_MS = 6 * 60 * 60_000;
const DEFAULT_SLASH_COMPAT_ENABLED = false;
const DEFAULT_SLASH_COMPAT_WTT_PREFIX_ONLY = true;
const DEFAULT_SLASH_BYPASS_MENTION_GATE = false;
const DEFAULT_NATURAL_BRIDGE_MIN_DOING_MS = 2500;
const DEFAULT_INBOUND_MEDIA_MAX_BYTES = 15 * 1024 * 1024;
const DEFAULT_INBOUND_MEDIA_MAX_PER_MESSAGE = 4;
const DEFAULT_INBOUND_MEDIA_FETCH_TIMEOUT_MS = 20_000;
const DEFAULT_DISCUSSION_CONTEXT_FETCH_LIMIT = 200;
const DEFAULT_DISCUSSION_CONTEXT_WINDOW = 100;
const DEFAULT_DISCUSSION_CONTEXT_MAX_CHARS = 24_000;

type OpenClawConfig = {
  session?: {
    store?: string;
  };
  channels?: {
    wtt?: {
      accounts?: Record<string, WTTAccountConfig>;
    } & WTTAccountConfig;
  };
};

type HookFn = (ctx: {
  tool: string;
  args: Record<string, unknown>;
  result?: unknown;
}) => void | Promise<void>;

type ChannelLogSink = {
  info?: (msg: string) => void;
  warn?: (msg: string) => void;
  error?: (msg: string) => void;
  debug?: (msg: string) => void;
};

type MsgContextLike = Record<string, unknown>;

type ChannelRuntimeLike = {
  routing: {
    resolveAgentRoute: (params: {
      cfg: OpenClawConfig;
      channel: string;
      accountId?: string | null;
      peer?: { kind: "direct" | "group" | "channel"; id: string } | null;
    }) => { agentId: string; accountId: string; sessionKey: string };
  };
  session: {
    resolveStorePath: (storePath: string | undefined, params: { agentId: string }) => string;
    readSessionUpdatedAt: (params: { storePath: string; sessionKey: string }) => string | number | null | undefined;
    recordInboundSession: (params: {
      storePath: string;
      sessionKey: string;
      ctx: MsgContextLike;
      updateLastRoute?: {
        sessionKey: string;
        channel: string;
        to: string;
        accountId?: string;
      };
      onRecordError: (err: unknown) => void;
    }) => Promise<void>;
  };
  reply: {
    resolveEnvelopeFormatOptions: (cfg: OpenClawConfig) => unknown;
    formatAgentEnvelope: (params: {
      channel: string;
      from: string;
      timestamp: string;
      previousTimestamp?: string | number | null;
      envelope?: unknown;
      body: string;
    }) => string;
    finalizeInboundContext: (ctx: MsgContextLike) => MsgContextLike;
    dispatchReplyWithBufferedBlockDispatcher: (params: {
      ctx: MsgContextLike;
      cfg: OpenClawConfig;
      dispatcherOptions: {
        deliver: (payload: Record<string, unknown>) => Promise<void>;
        onError?: (err: unknown, info: { kind: string }) => void;
      };
      replyOptions?: Record<string, unknown>;
    }) => Promise<unknown>;
  };
};

type GatewayStartContext = {
  cfg: OpenClawConfig;
  accountId: string;
  account: ResolvedWTTAccount;
  abortSignal: AbortSignal;
  log?: ChannelLogSink;
  channelRuntime?: ChannelRuntimeLike;
};

const hooks: { before: HookFn[]; after: HookFn[] } = { before: [], after: [] };
const clients = new Map<string, WTTCloudClient>();
const topicTypeCache = new Map<string, string>();
const recentTopicMediaCache = new Map<string, {
  at: number;
  mediaUrls: string[];
  mediaTypes: string[];
}>();
const DEFAULT_P2P_E2E_ENABLED = false;
const RECENT_TOPIC_MEDIA_TTL_MS = 10 * 60_000;

function registerHook(phase: "before_tool_call" | "after_tool_call", fn: HookFn): void {
  if (phase === "before_tool_call") hooks.before.push(fn);
  else hooks.after.push(fn);
}

async function runHooks(phase: "before" | "after", ctx: Parameters<HookFn>[0]): Promise<void> {
  for (const fn of hooks[phase]) await fn(ctx);
}

function listAccountIds(cfg: OpenClawConfig): string[] {
  const section = cfg.channels?.wtt;
  if (!section) return [];

  const ids = Object.keys(section.accounts ?? {});
  if (ids.length > 0) return ids;

  // Backward compatibility with flat single-account config under channels.wtt
  if (section.agentId || section.token || section.cloudUrl || section.name) return [DEFAULT_ACCOUNT_ID];
  return [];
}

function resolveRawAccountConfig(cfg: OpenClawConfig, accountId?: string): WTTAccountConfig {
  const section = cfg.channels?.wtt ?? {};
  const id = accountId ?? DEFAULT_ACCOUNT_ID;

  if (section.accounts?.[id]) return section.accounts[id];
  if (id === DEFAULT_ACCOUNT_ID) {
    const { accounts: _accounts, ...flat } = section;
    return flat;
  }
  return {};
}

function resolveAccount(cfg: OpenClawConfig, accountId?: string): ResolvedWTTAccount {
  const id = accountId ?? DEFAULT_ACCOUNT_ID;
  const raw = resolveRawAccountConfig(cfg, id);
  const enabled = raw.enabled !== false;
  const configured = Boolean(raw.agentId?.trim() && raw.token?.trim());

  return {
    accountId: id,
    name: raw.name ?? id,
    enabled,
    configured,
    cloudUrl: raw.cloudUrl ?? DEFAULT_CLOUD_URL,
    agentId: raw.agentId ?? "",
    token: raw.token ?? "",
    config: raw,
  };
}

function openclawConfigPath(): string {
  const fromEnv = process.env.OPENCLAW_CONFIG_PATH?.trim();
  if (fromEnv) return fromEnv;
  return joinPath(os.homedir(), ".openclaw", "openclaw.json");
}

function generateE2EPassword(): string {
  return randomBytes(24).toString("base64url");
}

async function ensureAccountE2EPassword(accountId: string, account: ResolvedWTTAccount, log: (level: "debug" | "info" | "warn" | "error", msg: string, data?: unknown) => void): Promise<void> {
  if (account.config.e2ePassword?.trim()) return;

  const password = generateE2EPassword();
  const configPath = openclawConfigPath();

  try {
    let cfgRaw: Record<string, unknown> = {};
    try {
      const text = await readFile(configPath, "utf8");
      cfgRaw = JSON.parse(text) as Record<string, unknown>;
    } catch (err) {
      const code = (err as NodeJS.ErrnoException | undefined)?.code;
      if (code !== "ENOENT") throw err;
    }

    const channels = ((cfgRaw.channels as Record<string, unknown> | undefined) ?? {});
    const wtt = ((channels.wtt as Record<string, unknown> | undefined) ?? {});
    const accounts = ((wtt.accounts as Record<string, unknown> | undefined) ?? {});

    const accountKey = accountId || DEFAULT_ACCOUNT_ID;
    const currentAccount = ((accounts[accountKey] as Record<string, unknown> | undefined) ?? {});

    const existing = typeof currentAccount.e2ePassword === "string" ? currentAccount.e2ePassword.trim() : "";
    if (existing) {
      account.config.e2ePassword = existing;
      return;
    }

    const mergedAccount = {
      ...currentAccount,
      e2ePassword: password,
    };

    const next = {
      ...cfgRaw,
      channels: {
        ...channels,
        wtt: {
          ...wtt,
          accounts: {
            ...accounts,
            [accountKey]: mergedAccount,
          },
        },
      },
    };

    await mkdir(dirname(configPath), { recursive: true });
    const tempPath = `${configPath}.tmp-${Date.now()}`;
    await writeFile(tempPath, `${JSON.stringify(next, null, 2)}\n`, "utf8");
    await rename(tempPath, configPath);

    account.config.e2ePassword = password;
    log("info", `[${accountId}] auto-generated e2ePassword and persisted to openclaw.json`);
  } catch (err) {
    log("warn", `[${accountId}] failed to auto-generate e2ePassword`, err);
  }
}

function rememberTopicType(topicId: string | undefined, topicType: string | undefined): void {
  const id = (topicId ?? "").trim();
  if (!id) return;
  const type = (topicType ?? "").trim().toLowerCase();
  if (!type) return;
  topicTypeCache.set(id, type);
  while (topicTypeCache.size > 5000) {
    const oldest = topicTypeCache.keys().next().value;
    if (!oldest) break;
    topicTypeCache.delete(oldest);
  }
}

function recentTopicMediaKey(topicId: string, senderId: string): string {
  return `${topicId.trim()}::${senderId.trim()}`;
}

function rememberRecentTopicMedia(topicId: string, senderId: string, mediaUrls: string[], mediaTypes: string[]): void {
  const topic = topicId.trim();
  const sender = senderId.trim();
  if (!topic || !sender || mediaUrls.length === 0) return;

  const dedupUrls = Array.from(new Set(mediaUrls.map((item) => String(item || "").trim()).filter(Boolean)));
  const dedupTypes = mediaTypes.slice(0, dedupUrls.length);
  if (dedupUrls.length === 0) return;

  recentTopicMediaCache.set(recentTopicMediaKey(topic, sender), {
    at: Date.now(),
    mediaUrls: dedupUrls,
    mediaTypes: dedupTypes.length > 0 ? dedupTypes : new Array(dedupUrls.length).fill("image/png"),
  });

  while (recentTopicMediaCache.size > 5000) {
    const oldest = recentTopicMediaCache.keys().next().value;
    if (!oldest) break;
    recentTopicMediaCache.delete(oldest);
  }
}

function readRecentTopicMedia(topicId: string, senderId: string): { mediaUrls: string[]; mediaTypes: string[] } | null {
  const now = Date.now();
  const key = recentTopicMediaKey(topicId, senderId);
  const direct = recentTopicMediaCache.get(key);
  if (direct) {
    if (now - direct.at <= RECENT_TOPIC_MEDIA_TTL_MS) {
      return {
        mediaUrls: direct.mediaUrls.slice(),
        mediaTypes: direct.mediaTypes.slice(),
      };
    }
    recentTopicMediaCache.delete(key);
  }

  // Fallback: some environments may surface a changing sender_id for HUMAN
  // messages. In that case, use latest recent media within the same topic.
  const prefix = `${topicId.trim()}::`;
  let best: { at: number; mediaUrls: string[]; mediaTypes: string[] } | null = null;
  for (const [entryKey, value] of recentTopicMediaCache.entries()) {
    if (!entryKey.startsWith(prefix)) continue;
    if (now - value.at > RECENT_TOPIC_MEDIA_TTL_MS) {
      recentTopicMediaCache.delete(entryKey);
      continue;
    }
    if (!best || value.at > best.at) best = value;
  }

  if (!best) return null;
  return {
    mediaUrls: best.mediaUrls.slice(),
    mediaTypes: best.mediaTypes.slice(),
  };
}

function looksLikeImageFollowupText(text: string): boolean {
  const raw = String(text || "").trim();
  if (!raw) return true;

  const compact = raw.replace(/\s+/g, "");
  if (compact.length <= 24) return true;

  return /(图片|图里|看图|识别|这是啥|这是什么|什么狗|啥狗|what\s+is\s+this|what\s+dog|identify)/i.test(raw);
}

function isP2PTopicId(topicId: string): boolean {
  const type = topicTypeCache.get(topicId.trim());
  return type === "p2p";
}

function isDiscussionTopicMessage(raw: WsMessagePayload & Record<string, unknown>, topicId: string): boolean {
  const topicType = String(raw.topic_type ?? "").trim().toLowerCase();
  if (topicType === "discussion") return true;
  if (topicType === "p2p" || topicType === "broadcast" || topicType === "collaborative") return false;

  const cached = topicTypeCache.get(topicId.trim());
  if (cached === "discussion") return true;
  if (cached === "p2p" || cached === "broadcast" || cached === "collaborative") return false;

  const metadata = parseInboundMetadata(raw);
  const metadataType = String(metadata?.topic_type ?? metadata?.topicType ?? "").trim().toLowerCase();
  if (metadataType === "discussion") return true;
  if (metadataType === "p2p" || metadataType === "broadcast" || metadataType === "collaborative") return false;

  const metadataChatType = String(metadata?.chat_type ?? metadata?.chatType ?? "").trim().toLowerCase();
  const metadataIsForum = metadata?.is_forum;
  if (metadataChatType === "group" || metadataChatType === "supergroup") return true;
  if (metadataIsForum === true || String(metadataIsForum).toLowerCase() === "true") return true;

  // Heuristic fallback: most non-p2p group threads are discussion-like and
  // should keep a local topic-memory file for retrieval.
  return Boolean(topicId && !isLikelyP2PMessage(raw));
}

function isP2PE2EEnabled(account: ResolvedWTTAccount): boolean {
  const raw = account.config.p2pE2EEnabled;
  return raw === undefined ? DEFAULT_P2P_E2E_ENABLED : raw !== false;
}

function getClient(accountId: string): WTTCloudClient | undefined {
  return clients.get(accountId);
}

function hasMeaningfulAccountConfig(raw: WTTAccountConfig): boolean {
  return Boolean(raw.agentId || raw.token || raw.cloudUrl || raw.name || raw.enabled !== undefined);
}

function detectAccountSource(cfg: OpenClawConfig | undefined, accountId: string): string {
  const section = cfg?.channels?.wtt;
  if (!section) return "runtime";
  if (section.accounts?.[accountId]) return `channels.wtt.accounts.${accountId}`;
  if (accountId === DEFAULT_ACCOUNT_ID) {
    const { accounts: _accounts, ...flat } = section;
    if (hasMeaningfulAccountConfig(flat)) return "channels.wtt";
  }
  return "runtime";
}

function resolveCommandAccountContext(accountId: string, cfg?: OpenClawConfig): WTTCommandAccountContext | undefined {
  if (cfg?.channels?.wtt) {
    const account = resolveAccount(cfg, accountId);
    return {
      accountId: account.accountId,
      name: account.name,
      source: detectAccountSource(cfg, accountId),
      cloudUrl: account.cloudUrl,
      agentId: account.agentId,
      token: account.token,
      enabled: account.enabled,
      configured: account.configured,
    };
  }

  const client = getClient(accountId);
  if (!client) return undefined;

  const runtime = client.getAccount();
  return {
    accountId: runtime.accountId,
    name: runtime.name,
    source: "runtime.client",
    cloudUrl: runtime.cloudUrl,
    agentId: runtime.agentId,
    token: runtime.token,
    enabled: runtime.enabled,
    configured: runtime.configured,
  };
}

const commandRouter = createWTTCommandRouter({
  getClient,
  getAccount: (accountId) => resolveCommandAccountContext(accountId),
  defaultAccountId: DEFAULT_ACCOUNT_ID,
});

function extractDispatchText(payload: unknown): string {
  if (!payload || typeof payload !== "object") return "";
  const data = payload as Record<string, unknown>;

  if (typeof data.text === "string" && data.text.trim()) {
    return data.text.trim();
  }

  const lines: string[] = [];
  const blocks = Array.isArray(data.blocks) ? data.blocks : [];
  for (const block of blocks) {
    if (!block || typeof block !== "object") continue;
    const piece = (block as Record<string, unknown>).text;
    if (typeof piece === "string" && piece.trim()) lines.push(piece.trim());
  }

  if (lines.length > 0) return lines.join("\n\n");
  return "";
}

function toNumberOrZero(raw: unknown): number {
  const n = Number(raw);
  if (!Number.isFinite(n) || n < 0) return 0;
  return Math.floor(n);
}

function toTimestampMs(raw: unknown): number | undefined {
  if (typeof raw === "number" && Number.isFinite(raw)) {
    if (raw > 1_000_000_000_000) return Math.floor(raw);
    if (raw > 1_000_000_000) return Math.floor(raw * 1000);
    return undefined;
  }

  if (typeof raw === "string" && raw.trim()) {
    const parsed = Date.parse(raw);
    if (Number.isFinite(parsed)) return parsed;
  }

  return undefined;
}

async function collectSessionUsageDelta(params: {
  storePath: string;
  sessionKey: string;
  sinceMs: number;
  untilMs?: number;
}): Promise<WTTTaskInferenceUsage | undefined> {
  const filePath = joinPath(params.storePath, `${params.sessionKey}.jsonl`);

  let content: string;
  try {
    content = await readFile(filePath, "utf8");
  } catch {
    return undefined;
  }

  const lines = content.split("\n");
  if (lines.length === 0) return undefined;

  const untilMs = Number.isFinite(params.untilMs) ? (params.untilMs as number) : Date.now();

  let promptTokens = 0;
  let completionTokens = 0;
  let cacheReadTokens = 0;
  let cacheWriteTokens = 0;
  let totalTokens = 0;
  let matched = 0;
  let provider: string | undefined;
  let model: string | undefined;

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    let entry: Record<string, unknown> | undefined;
    try {
      const parsed = JSON.parse(trimmed) as unknown;
      if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) continue;
      entry = parsed as Record<string, unknown>;
    } catch {
      continue;
    }

    if (entry.type !== "message") continue;

    const message = asRecord(entry.message);
    if (!message || message.role !== "assistant") continue;

    const ts = toTimestampMs(entry.timestamp ?? message.timestamp);
    if (typeof ts !== "number") continue;
    if (ts < params.sinceMs || ts > untilMs + 2_000) continue;

    const usage = asRecord(message.usage);
    if (!usage) continue;

    matched += 1;
    const input = toNumberOrZero(usage.input);
    const output = toNumberOrZero(usage.output);
    const cacheRead = toNumberOrZero(usage.cacheRead);
    const cacheWrite = toNumberOrZero(usage.cacheWrite);
    const total = toNumberOrZero(usage.totalTokens);

    promptTokens += input;
    completionTokens += output;
    cacheReadTokens += cacheRead;
    cacheWriteTokens += cacheWrite;
    totalTokens += total > 0 ? total : (input + output + cacheRead + cacheWrite);

    const msgProvider = typeof message.provider === "string" ? message.provider.trim() : "";
    const msgModel = typeof message.model === "string" ? message.model.trim() : "";
    if (msgProvider) provider = msgProvider;
    if (msgModel) model = msgModel;
  }

  if (matched <= 0) return undefined;

  return {
    promptTokens,
    completionTokens,
    cacheReadTokens,
    cacheWriteTokens,
    totalTokens,
    source: "openclaw_session_usage_delta",
    provider,
    model,
  };
}

type OpenClawQueueDepthReader = (key: string) => number;

let openClawQueueDepthReaderPromise: Promise<OpenClawQueueDepthReader | null> | null = null;

async function loadOpenClawQueueDepthReader(): Promise<OpenClawQueueDepthReader | null> {
  if (openClawQueueDepthReaderPromise) return openClawQueueDepthReaderPromise;

  openClawQueueDepthReaderPromise = (async () => {
    try {
      const require = createRequire(import.meta.url);
      const sdkEntry = require.resolve("openclaw/plugin-sdk");
      const enqueuePath = joinPath(dirname(sdkEntry), "auto-reply/reply/queue/enqueue.js");
      const mod = await import(pathToFileURL(enqueuePath).href) as unknown as {
        getFollowupQueueDepth?: (key: string) => number;
      };

      if (typeof mod.getFollowupQueueDepth === "function") {
        return mod.getFollowupQueueDepth;
      }
    } catch {
      // best-effort only
    }

    return null;
  })();

  return openClawQueueDepthReaderPromise;
}

async function resolveOpenClawQueueDepth(sessionKey: string): Promise<number | undefined> {
  if (!sessionKey) return undefined;

  try {
    const reader = await loadOpenClawQueueDepthReader();
    if (!reader) return undefined;
    const raw = reader(sessionKey);
    if (!Number.isFinite(raw)) return undefined;
    return Math.max(0, Math.floor(raw));
  } catch {
    return undefined;
  }
}

async function resolveOpenClawQueueModeFromStore(storePath: string, sessionKey: string): Promise<string | undefined> {
  if (!storePath || !sessionKey) return undefined;

  try {
    const raw = await readFile(storePath, "utf8");
    const parsed = JSON.parse(raw) as unknown;
    if (!parsed || typeof parsed !== "object" || Array.isArray(parsed)) return undefined;

    const entry = (parsed as Record<string, unknown>)[sessionKey];
    if (!entry || typeof entry !== "object" || Array.isArray(entry)) return undefined;

    const mode = (entry as Record<string, unknown>).queueMode;
    return typeof mode === "string" && mode.trim() ? mode.trim() : undefined;
  } catch {
    return undefined;
  }
}

function createTaskInferenceRuntimeHooks(params: {
  cfg: OpenClawConfig;
  accountId: string;
  account?: WTTCommandAccountContext;
  channelRuntime?: ChannelRuntimeLike;
  typingSignal?: (args: { topicId: string; state: "start" | "stop"; ttlMs?: number }) => Promise<void>;
}): WTTCommandRuntimeHooks | undefined {
  const runtime = params.channelRuntime;
  if (!runtime) return undefined;

  return {
    getSessionRuntimeMetrics: async (request): Promise<WTTSessionRuntimeMetrics | undefined> => {
      const topicId = request.topicId?.trim();
      if (!topicId || topicId === "-") return undefined;

      const route = runtime.routing.resolveAgentRoute({
        cfg: params.cfg,
        channel: CHANNEL_ID,
        accountId: params.accountId,
        peer: { kind: "group", id: topicId },
      });

      const storePath = runtime.session.resolveStorePath(params.cfg.session?.store, {
        agentId: route.agentId,
      });

      const [queueDepth, queueMode] = await Promise.all([
        resolveOpenClawQueueDepth(route.sessionKey),
        resolveOpenClawQueueModeFromStore(storePath, route.sessionKey),
      ]);

      return {
        source: (typeof queueDepth === "number" || Boolean(queueMode)) ? "openclaw" : "fallback",
        queueDepth,
        queueMode,
        sessionKey: route.sessionKey,
        inflight: true,
      };
    },

    dispatchTaskInference: async (request: WTTTaskInferenceRuntimeRequest) => {
      let topicId = request.task.topicId?.trim();

      if (!topicId || topicId === "-") {
        const token = params.account?.token?.trim();
        const cloudUrl = params.account?.cloudUrl?.trim();

        if (token && cloudUrl) {
          try {
            const resp = await fetch(`${cloudUrl.replace(/\/$/, "")}/tasks/${encodeURIComponent(request.taskId)}`, {
              method: "GET",
              headers: {
                Accept: "application/json",
                Authorization: `Bearer ${token}`,
                "X-Agent-Token": token,
              },
            });

            if (resp.ok) {
              const detail = await resp.json() as Record<string, unknown>;
              const fromDetail = toOptionalString(detail.topic_id) ?? toOptionalString(detail.topicId);
              if (fromDetail && fromDetail !== "-") {
                topicId = fromDetail;
              }
            }
          } catch {
            // keep fallback below
          }
        }
      }

      if (!topicId || topicId === "-") {
        throw new Error(`task_topic_unresolved:${request.taskId}`);
      }

      const emitTypingSignal = async (state: "start" | "stop"): Promise<void> => {
        if (!params.typingSignal) return;
        try {
          await params.typingSignal({ topicId, state, ttlMs: 6000 });
        } catch {
          // best-effort only
        }
      };

      const route = runtime.routing.resolveAgentRoute({
        cfg: params.cfg,
        channel: CHANNEL_ID,
        accountId: params.accountId,
        peer: { kind: "group", id: topicId },
      });

      const storePath = runtime.session.resolveStorePath(params.cfg.session?.store, {
        agentId: route.agentId,
      });

      const previousTimestamp = runtime.session.readSessionUpdatedAt({
        storePath,
        sessionKey: route.sessionKey,
      });
      const runStartedMs = Date.now();

      const timestamp = new Date().toISOString();
      const from = `wtt:topic:${topicId}`;
      const to = `topic:${topicId}`;
      const chatType = "group";

      const envelopeOptions = runtime.reply.resolveEnvelopeFormatOptions(params.cfg);
      const body = runtime.reply.formatAgentEnvelope({
        channel: "WTT",
        from: "WTT Task Executor",
        timestamp,
        previousTimestamp,
        envelope: envelopeOptions,
        body: request.prompt,
      });

      const ctxPayload = runtime.reply.finalizeInboundContext({
        Body: body,
        BodyForAgent: request.prompt,
        RawBody: request.prompt,
        CommandBody: request.prompt,
        From: from,
        To: to,
        SessionKey: route.sessionKey,
        AccountId: route.accountId,
        ChatType: chatType,
        ConversationLabel: `topic:${topicId}`,
        SenderName: "WTT Task Executor",
        SenderId: params.account?.agentId || "wtt-task-executor",
        GroupSubject: topicId,
        Provider: CHANNEL_ID,
        Surface: CHANNEL_ID,
        MessageSid: `task-run:${request.taskId}:${Date.now()}`,
        Timestamp: timestamp,
        OriginatingChannel: CHANNEL_ID,
        OriginatingTo: to,
      });

      await runtime.session.recordInboundSession({
        storePath,
        sessionKey: route.sessionKey,
        ctx: ctxPayload,
        updateLastRoute: {
          sessionKey: route.sessionKey,
          channel: CHANNEL_ID,
          to,
          accountId: route.accountId,
        },
        onRecordError: () => {
          // keep inference path running even if session recording fails
        },
      });

      const chunks: string[] = [];
      let dispatchResult: unknown;

      await emitTypingSignal("start");
      try {
        dispatchResult = await runtime.reply.dispatchReplyWithBufferedBlockDispatcher({
          ctx: ctxPayload,
          cfg: params.cfg,
          dispatcherOptions: {
            deliver: async (payload) => {
              if (payload.isReasoning) return;
              const text = extractDispatchText(payload);
              if (text) chunks.push(text);
            },
          },
        });
      } finally {
        await emitTypingSignal("stop");
      }

      const fallback = extractDispatchText(dispatchResult);
      const outputText = chunks.join("\n\n").trim() || fallback;

      const usage = await collectSessionUsageDelta({
        storePath,
        sessionKey: route.sessionKey,
        sinceMs: runStartedMs,
        untilMs: Date.now(),
      });

      return {
        outputText,
        provider: "channelRuntime.reply.dispatchReplyWithBufferedBlockDispatcher",
        usage,
        raw: dispatchResult,
      };
    },
  };
}

export async function processWTTCommandText(params: {
  text: string;
  accountId?: string;
  cfg?: OpenClawConfig;
  channelRuntime?: ChannelRuntimeLike;
}): Promise<WTTCommandProcessResult> {
  const accountId = params.accountId ?? DEFAULT_ACCOUNT_ID;
  const account = resolveCommandAccountContext(accountId, params.cfg);

  return commandRouter.processText(params.text, {
    accountId,
    account,
    runtimeHooks: createTaskInferenceRuntimeHooks({
      cfg: params.cfg ?? {},
      accountId,
      account,
      channelRuntime: params.channelRuntime,
    }),
  });
}

type PluginAPI = {
  log: (level: "debug" | "info" | "warn" | "error", msg: string, data?: unknown) => void;
  onMessage?: (accountId: string, msg: WsNewMessage) => void;
  onTaskStatus?: (accountId: string, msg: WsTaskStatus) => void;
};

async function resolveAgentDisplayName(account: ResolvedWTTAccount): Promise<string | undefined> {
  const token = account.token?.trim();
  const agentId = account.agentId?.trim();
  if (!token || !agentId) return undefined;

  const authHeaders = {
    Accept: "application/json",
    Authorization: `Bearer ${token}`,
    "X-Agent-Token": token,
  };

  // Preferred endpoint: lists current user's bound agents including display_name.
  try {
    const myResp = await fetch(`${account.cloudUrl.replace(/\/$/, "")}/agents/my`, {
      method: "GET",
      headers: authHeaders,
    });
    if (myResp.ok) {
      const payload = await myResp.json() as unknown;
      const rows = Array.isArray(payload)
        ? payload
        : (payload && typeof payload === "object" && Array.isArray((payload as Record<string, unknown>).agents))
          ? (payload as Record<string, unknown>).agents as unknown[]
          : [];

      for (const rowRaw of rows) {
        if (!rowRaw || typeof rowRaw !== "object") continue;
        const row = rowRaw as Record<string, unknown>;
        const rowId = typeof row.agent_id === "string" ? row.agent_id.trim() : "";
        if (rowId !== agentId) continue;
        const display = typeof row.display_name === "string" ? row.display_name.trim() : "";
        if (display) return display;
      }
    }
  } catch {
    // ignore and try fallback endpoint
  }

  // Fallback endpoint.
  try {
    const profileResp = await fetch(`${account.cloudUrl.replace(/\/$/, "")}/agents/${encodeURIComponent(agentId)}/profile`, {
      method: "GET",
      headers: authHeaders,
    });
    if (profileResp.ok) {
      const profile = await profileResp.json() as { display_name?: string };
      const display = profile.display_name?.trim();
      if (display) return display;
    }
  } catch {
    // ignore
  }

  return undefined;
}

async function startWsAccount(
  accountId: string,
  account: ResolvedWTTAccount,
  api: PluginAPI,
): Promise<WTTCloudClient | undefined> {
  const existing = clients.get(accountId);
  if (existing) {
    existing.disconnect();
    clients.delete(accountId);
  }

  if (!account.enabled || !account.configured) {
    api.log("info", `WTT account ${accountId} skipped (${!account.enabled ? "disabled" : "not configured"})`);
    return undefined;
  }

  await ensureAccountE2EPassword(accountId, account, api.log);

  const client = new WTTCloudClient({
    account,
    onMessage: (msg) => api.onMessage?.(accountId, msg),
    onTaskStatus: (msg) => api.onTaskStatus?.(accountId, msg),
    onConnect: () => api.log("info", `[${accountId}] connected`),
    onDisconnect: () => api.log("info", `[${accountId}] disconnected`),
    onError: (err) => api.log("error", `[${accountId}] ${err.message}`),
    log: (level, msg, data) => api.log(level, `[${accountId}] ${msg}`, data),
  });

  clients.set(accountId, client);
  await client.connect();

  // Resolve display name from server (supports claimed+renamed agent names).
  try {
    const displayName = await resolveAgentDisplayName(account);
    if (displayName && displayName !== account.agentId) {
      account.name = displayName;
      api.log("info", `[${accountId}] display name resolved: ${displayName}`);
    }
  } catch {
    // Non-critical — inference gating will still match agentId.
  }

  return client;
}

async function stopAccount(accountId: string): Promise<void> {
  const client = clients.get(accountId);
  if (!client) return;
  client.disconnect();
  clients.delete(accountId);
}

function parseWttTarget(rawTarget: string):
  | { mode: "topic"; value: string }
  | { mode: "p2p"; value: string } {
  const target = (rawTarget || "").trim();

  if (target.startsWith("topic:")) return { mode: "topic", value: target.slice("topic:".length).trim() };
  if (target.startsWith("p2p:")) return { mode: "p2p", value: target.slice("p2p:".length).trim() };
  if (target.startsWith("agent:")) return { mode: "p2p", value: target.slice("agent:".length).trim() };

  // default behavior: treat as topic id for compatibility with existing topic-based routing
  return { mode: "topic", value: target };
}

async function sendText(params: {
  to: string;
  text: string;
  replyTo?: string;
  accountId?: string;
  cfg?: OpenClawConfig;
}): Promise<{ channel: "wtt"; messageId: string; conversationId?: string; meta?: Record<string, unknown> }> {
  const accountId = params.accountId ?? DEFAULT_ACCOUNT_ID;
  const client = getClient(accountId);
  if (!client?.connected) throw new Error(`WTT account ${accountId} is not connected`);

  const target = parseWttTarget(params.to);
  await runHooks("before", { tool: "sendText", args: { ...params, target } });

  let response: any;
  const account = client.getAccount();
  const p2pEncryptEnabled = isP2PE2EEnabled(account) && client.hasE2EKey();

  if (target.mode === "p2p") {
    response = await client.p2p(target.value, params.text, p2pEncryptEnabled);
  } else {
    const shouldEncryptTopic = p2pEncryptEnabled && isP2PTopicId(target.value);
    response = await client.publish(target.value, params.text, {
      encrypt: shouldEncryptTopic,
      replyTo: params.replyTo,
    });
  }

  await runHooks("after", { tool: "sendText", args: { ...params, target }, result: response });

  return {
    channel: "wtt",
    messageId: String(response?.id ?? response?.message_id ?? response?.request_id ?? Date.now()),
    conversationId: String(response?.topic_id ?? target.value),
    meta: {
      mode: target.mode,
      raw: response ?? null,
    },
  };
}

async function sendMedia(params: {
  to: string;
  text?: string;
  mediaUrl?: string;
  replyTo?: string;
  accountId?: string;
  cfg?: OpenClawConfig;
}): Promise<{ channel: "wtt"; messageId: string; conversationId?: string; meta?: Record<string, unknown> }> {
  const payload = JSON.stringify({
    type: "media",
    mediaUrl: params.mediaUrl ?? "",
    caption: params.text ?? "",
  });
  return sendText({
    to: params.to,
    text: payload,
    replyTo: params.replyTo,
    accountId: params.accountId,
    cfg: params.cfg,
  });
}

function waitForAbort(signal: AbortSignal): Promise<void> {
  if (signal.aborted) return Promise.resolve();
  return new Promise((resolve) => {
    signal.addEventListener(
      "abort",
      () => {
        resolve();
      },
      { once: true },
    );
  });
}

function toIsoTimestamp(raw: unknown): string {
  if (typeof raw === "string" && raw.trim()) {
    const d = new Date(raw);
    if (!Number.isNaN(d.getTime())) return d.toISOString();
    return raw;
  }
  if (typeof raw === "number" && Number.isFinite(raw)) {
    const d = new Date(raw);
    if (!Number.isNaN(d.getTime())) return d.toISOString();
  }
  return new Date().toISOString();
}

function toOptionalString(value: unknown): string | undefined {
  if (typeof value !== "string") return undefined;
  const trimmed = value.trim();
  return trimmed ? trimmed : undefined;
}

function hasMeaningfulPipelineId(value: unknown): boolean {
  const normalized = String(value ?? "").trim().toLowerCase();
  if (!normalized) return false;
  if (["default", "none", "null", "undefined", "n/a", "na", "-", "0"].includes(normalized)) {
    return false;
  }
  return true;
}

function sanitizeInboundText(raw: string): string {
  let text = raw || "";

  // Strip WTT source marker banner block if present.
  text = text.replace(/┌─ 来源标识[\s\S]*?└[^\n]*\n?/g, "").trim();

  // Remove inline image payload markers from text body.
  // Why: markdown image syntax starts with `!`, which can be interpreted as
  // shell-command prefix by OpenClaw slash command surface.
  text = text.replace(/<img\b[^>]*>/gi, " ");
  text = text.replace(/!\[[^\]]*\]\((https?:\/\/[^\s)]+)\)/gi, " ");
  text = text.replace(/(?:^|\n)\s*https?:\/\/\S+\.(?:jpg|jpeg|png|gif|webp|svg)(?:\?[^\s]*)?\s*(?=\n|$)/gim, "\n");
  text = text.replace(/\n{3,}/g, "\n\n").trim();

  return text;
}

function extractInboundImageMedia(raw: string, rawMsg?: Record<string, unknown>): { mediaUrls: string[]; mediaTypes: string[] } {
  const source = raw || "";
  const mediaUrls: string[] = [];
  const mediaTypes: string[] = [];

  const imageExtRe = /\.(?:jpg|jpeg|png|gif|webp|bmp|svg|heic|heif)(?:\?|$)/i;
  const imageHostHintRe = /(?:^|\/)media\/[0-9a-f-]{16,}(?:\.[a-z0-9]{2,8})?(?:\?|$)/i;

  const pushUrl = (urlRaw: string): void => {
    const url = String(urlRaw || "").trim().replace(/[),.;]+$/, "");
    if (!url) return;
    if (!/^https?:\/\//i.test(url) && !/^\/?.*media\/[0-9a-f-]{16,}/i.test(url)) return;
    if (mediaUrls.includes(url)) return;
    mediaUrls.push(url);
    mediaTypes.push("image/png");
  };

  const scanStringForImageUrls = (input: string): void => {
    const text = String(input || "");
    if (!text) return;

    // HTML <img src="url"> pattern (from rich editor)
    const htmlImgRe = /<img\s[^>]*\bsrc\s*=\s*["']([^"']+)["']/gi;
    let htmlMatch: RegExpExecArray | null;
    while ((htmlMatch = htmlImgRe.exec(text)) !== null) {
      pushUrl(htmlMatch[1]);
    }

    // Markdown ![alt](url) pattern (accept absolute + relative media paths)
    const mdImgRe = /!\[[^\]]*\]\(([^\s)]+)\)/gi;
    let mdMatch: RegExpExecArray | null;
    while ((mdMatch = mdImgRe.exec(text)) !== null) {
      pushUrl(mdMatch[1]);
    }

    // Generic URL scan (covers metadata/url fields and host URLs without explicit image token)
    const genericUrlRe = /https?:\/\/[^\s"'<>\])]+/gi;
    let urlMatch: RegExpExecArray | null;
    while ((urlMatch = genericUrlRe.exec(text)) !== null) {
      const candidate = String(urlMatch[0] || "").replace(/[),.;]+$/, "");
      if (!candidate) continue;
      if (imageExtRe.test(candidate) || imageHostHintRe.test(candidate)) {
        pushUrl(candidate);
      }
    }

    // Relative media URL scan (e.g. /media/<id> from backend metadata)
    const relativeMediaRe = /(?:^|[\s(\["'])(\/?media\/[0-9a-f-]{16,}(?:\.[a-z0-9]{2,8})?(?:\?[^\s)"']*)?)/gi;
    let relMatch: RegExpExecArray | null;
    while ((relMatch = relativeMediaRe.exec(text)) !== null) {
      pushUrl(relMatch[1]);
    }

    // Bare image URLs on their own line (explicit fast path)
    const bareImgRe = /^(https?:\/\/\S+\.(?:jpg|jpeg|png|gif|webp|svg)(?:\?[^\s]*)?)$/gim;
    let bareMatch: RegExpExecArray | null;
    while ((bareMatch = bareImgRe.exec(text)) !== null) {
      pushUrl(bareMatch[1]);
    }
  };

  const walkUnknown = (value: unknown, depth = 0): void => {
    if (depth > 5 || value == null) return;
    if (typeof value === "string") {
      scanStringForImageUrls(value);
      return;
    }
    if (Array.isArray(value)) {
      const upper = Math.min(value.length, 80);
      for (let i = 0; i < upper; i += 1) walkUnknown(value[i], depth + 1);
      return;
    }
    if (typeof value !== "object") return;

    const obj = value as Record<string, unknown>;
    for (const [k, v] of Object.entries(obj)) {
      const key = k.toLowerCase();
      if (typeof v === "string") {
        // Prioritize likely media-related keys.
        if (key.includes("image") || key.includes("media") || key.includes("url") || key.includes("file") || key.includes("asset") || key.includes("attach")) {
          scanStringForImageUrls(v);
        } else if (/https?:\/\//i.test(v)) {
          scanStringForImageUrls(v);
        }
      } else {
        walkUnknown(v, depth + 1);
      }
    }
  };

  scanStringForImageUrls(source);
  if (rawMsg) walkUnknown(rawMsg);

  return { mediaUrls, mediaTypes };
}

function absolutizeInboundMediaUrls(mediaUrls: string[], cloudUrl: string): string[] {
  const base = String(cloudUrl || "").trim().replace(/\/$/, "");
  const originMatch = base.match(/^(https?:\/\/[^/]+)/i);
  const origin = originMatch ? originMatch[1] : base;

  const out: string[] = [];
  for (const raw of mediaUrls) {
    let url = String(raw || "").trim();
    if (!url) continue;

    if (/^\/\//.test(url)) {
      url = `https:${url}`;
    } else if (/^\//.test(url) && origin) {
      url = `${origin}${url}`;
    } else if (/^media\//i.test(url) && origin) {
      url = `${origin}/${url}`;
    }

    if (!/^https?:\/\//i.test(url)) continue;
    if (out.includes(url)) continue;
    out.push(url);
  }

  return out;
}

function toThumbnailVariantUrl(urlRaw: string): string {
  const url = String(urlRaw || "").trim();
  if (!url) return url;
  if (!/\/media\//i.test(url)) return url;

  try {
    const parsed = new URL(url);
    if (!parsed.searchParams.get("variant")) {
      parsed.searchParams.set("variant", "thumb");
    }
    return parsed.toString();
  } catch {
    // best-effort for non-standard URLs
    const sep = url.includes("?") ? "&" : "?";
    if (/([?&])variant=/i.test(url)) return url;
    return `${url}${sep}variant=thumb`;
  }
}

function toThumbnailVariantUrls(urls: string[]): string[] {
  const out: string[] = [];
  for (const item of urls) {
    const normalized = toThumbnailVariantUrl(item);
    if (!normalized) continue;
    if (out.includes(normalized)) continue;
    out.push(normalized);
  }
  return out;
}

function resolveOpenClawHomeDir(): string {
  const fromEnv = process.env.OPENCLAW_HOME?.trim();
  if (fromEnv) return fromEnv;
  return dirname(openclawConfigPath());
}

function resolveInboundMediaDir(): string {
  return joinPath(resolveOpenClawHomeDir(), "media", "inbound");
}

function extensionFromContentType(contentType: string | undefined): string {
  const normalized = String(contentType || "").toLowerCase();
  if (!normalized) return "";
  if (normalized.includes("jpeg") || normalized.includes("jpg")) return ".jpg";
  if (normalized.includes("png")) return ".png";
  if (normalized.includes("gif")) return ".gif";
  if (normalized.includes("webp")) return ".webp";
  if (normalized.includes("bmp")) return ".bmp";
  if (normalized.includes("svg")) return ".svg";
  if (normalized.includes("heic")) return ".heic";
  if (normalized.includes("heif")) return ".heif";
  if (normalized.includes("mp4")) return ".mp4";
  return "";
}

function extensionFromUrl(urlRaw: string): string {
  try {
    const parsed = new URL(urlRaw);
    const ext = extname(parsed.pathname || "").toLowerCase();
    if (!ext) return "";
    if (/^\.[a-z0-9]{1,8}$/.test(ext)) return ext;
    return "";
  } catch {
    const ext = extname(urlRaw).toLowerCase();
    if (!ext) return "";
    return /^\.[a-z0-9]{1,8}$/.test(ext) ? ext : "";
  }
}

async function downloadInboundMediaToLocal(params: {
  url: string;
  account: ResolvedWTTAccount;
  maxBytes: number;
  timeoutMs: number;
}): Promise<{ path: string; contentType?: string; bytes: number }> {
  const headers: Record<string, string> = {
    Accept: "image/*,*/*;q=0.8",
  };
  if (params.account.token) {
    headers.Authorization = `Bearer ${params.account.token}`;
    headers["X-Agent-Token"] = params.account.token;
  }

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), Math.max(1000, params.timeoutMs));

  let response: Response;
  try {
    response = await fetch(params.url, {
      method: "GET",
      headers,
      redirect: "follow",
      signal: controller.signal,
    });
  } finally {
    clearTimeout(timeout);
  }

  if (!response.ok) {
    throw new Error(`http_${response.status}`);
  }

  const chunks: Buffer[] = [];
  let total = 0;

  const reader = response.body?.getReader();
  if (reader) {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      if (!value) continue;
      total += value.byteLength;
      if (total > params.maxBytes) {
        throw new Error(`media_too_large_${total}`);
      }
      chunks.push(Buffer.from(value));
    }
  } else {
    const buf = Buffer.from(await response.arrayBuffer());
    total = buf.length;
    if (total > params.maxBytes) {
      throw new Error(`media_too_large_${total}`);
    }
    chunks.push(buf);
  }

  if (total <= 0) {
    throw new Error("empty_media");
  }

  const contentType = (response.headers.get("content-type") || "").split(";")[0]?.trim().toLowerCase() || undefined;
  const ext = extensionFromContentType(contentType) || extensionFromUrl(params.url) || ".bin";
  const fileName = `wtt-inbound-${Date.now()}-${randomBytes(6).toString("hex")}${ext}`;
  const mediaDir = resolveInboundMediaDir();
  await mkdir(mediaDir, { recursive: true });
  const filePath = joinPath(mediaDir, fileName);
  await writeFile(filePath, Buffer.concat(chunks));

  return {
    path: filePath,
    contentType,
    bytes: total,
  };
}

async function materializeInboundMediaForContext(params: {
  mediaUrls: string[];
  mediaTypes: string[];
  account: ResolvedWTTAccount;
  accountId: string;
  preferThumbnail?: boolean;
  log?: (level: "debug" | "info" | "warn" | "error", msg: string, data?: unknown) => void;
}): Promise<{ mediaPaths: string[]; mediaTypes: string[] }> {
  if (params.mediaUrls.length === 0) {
    return { mediaPaths: [], mediaTypes: [] };
  }

  const maxBytes = toPositiveInt(params.account.config.inboundMediaMaxBytes, DEFAULT_INBOUND_MEDIA_MAX_BYTES);
  const maxPerMessage = toPositiveInt(params.account.config.inboundMediaMaxPerMessage, DEFAULT_INBOUND_MEDIA_MAX_PER_MESSAGE);
  const timeoutMs = toPositiveInt(params.account.config.inboundMediaFetchTimeoutMs, DEFAULT_INBOUND_MEDIA_FETCH_TIMEOUT_MS);
  const sourceUrls = params.mediaUrls
    .slice(0, Math.max(1, maxPerMessage))
    .map((url) => (params.preferThumbnail ? toThumbnailVariantUrl(url) : url));

  const mediaPaths: string[] = [];
  const mediaTypes: string[] = [];

  for (let idx = 0; idx < sourceUrls.length; idx += 1) {
    const url = sourceUrls[idx] || "";
    if (!url) continue;

    try {
      const downloaded = await downloadInboundMediaToLocal({
        url,
        account: params.account,
        maxBytes,
        timeoutMs,
      });
      mediaPaths.push(downloaded.path);
      mediaTypes.push(downloaded.contentType || params.mediaTypes[idx] || "image/png");
      params.log?.("info", `[${params.accountId}] inbound media downloaded url=${url} path=${downloaded.path} bytes=${downloaded.bytes}`);
    } catch (err) {
      params.log?.("warn", `[${params.accountId}] inbound media download failed url=${url}`, err);
    }
  }

  return {
    mediaPaths,
    mediaTypes,
  };
}

type DiscussionHistoryMessage = {
  id: string;
  senderId: string;
  senderDisplayName?: string;
  senderType?: string;
  content: string;
  createdAt?: string;
  replyTo?: string;
  mediaPaths?: string[];
  mediaUrls?: string[];
  replyExcerpt?: string;
};

function resolveTopicMemoryDir(): string {
  return joinPath(resolveOpenClawHomeDir(), "topic-memory");
}

// ── Knowledge Base local cache ──

function resolveKBCacheDir(taskId: string): string {
  return joinPath(resolveOpenClawHomeDir(), "knowledge-base", taskId);
}

async function ensureKBCacheDir(taskId: string): Promise<string> {
  const dir = resolveKBCacheDir(taskId);
  try { await mkdir(dir, { recursive: true }); } catch { /* exists */ }
  return dir;
}

/**
 * Sync KB index from server to local cache.
 * Fetches TOC and writes _index.md for agent reference.
 */
async function syncKBIndex(taskId: string, apiBase: string): Promise<string | null> {
  const dir = await ensureKBCacheDir(taskId);
  const indexPath = joinPath(dir, "_index.md");
  try {
    const resp = await fetch(`${apiBase}/tasks/${taskId}/kb/toc`);
    if (!resp.ok) return null;
    const toc = (await resp.json()) as { article_count?: number; categories?: Record<string, any[]>; index_entries?: any[] };
    const lines: string[] = [`# Knowledge Base Index — ${taskId}\n`];
    lines.push(`Total articles: ${toc.article_count ?? 0}\n`);
    for (const [cat, articles] of Object.entries(toc.categories ?? {})) {
      lines.push(`\n## ${cat}\n`);
      for (const a of articles as any[]) {
        lines.push(`- **${a.title}** (${a.slug}) v${a.version}`);
        if (a.summary) lines.push(`  > ${a.summary}`);
        if (a.tags) lines.push(`  Tags: ${a.tags}`);
      }
    }
    if (toc.index_entries?.length) {
      lines.push(`\n## Concepts & Entities\n`);
      for (const e of toc.index_entries) {
        lines.push(`- [${e.entry_type}] **${e.key}**: ${e.summary || '(no summary)'}`);
      }
    }
    await writeFile(indexPath, lines.join("\n"), "utf-8");
    return indexPath;
  } catch (e) {
    return null;
  }
}

/**
 * Build KB context block for injection into agent inference.
 * Reads local _index.md, extracts relevant summaries based on message content.
 */
async function buildKBContextBlock(taskId: string, messageContent: string): Promise<string> {
  const dir = resolveKBCacheDir(taskId);
  const indexPath = joinPath(dir, "_index.md");
  try {
    const indexContent = await readFile(indexPath, "utf-8");
    if (!indexContent || indexContent.length < 50) return "";

    // Provide index summary + file path for agent to dig deeper
    const truncated = indexContent.length > 8000
      ? indexContent.slice(0, 8000) + "\n...(truncated, read full index file for more)"
      : indexContent;

    return (
      `\n\n[KB_CONTEXT]\n` +
      `This task has a Knowledge Base. Here is the index:\n\n` +
      `${truncated}\n\n` +
      `[KB_INDEX_FILE] ${indexPath}\n` +
      `Use wtt_kb_search and wtt_kb_read MCP tools to access full articles.\n` +
      `[/KB_CONTEXT]`
    );
  } catch {
    return "";
  }
}

function compactDiscussionContent(raw: string): string {
  const source = String(raw || "");
  return source
    .replace(/┌─\s*来源标识[\s\S]*?└[^\n]*\n?/g, "")
    .replace(/\[回复上下文\][\s\S]*?(?:---|$)/g, "")
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<\/p>/gi, "\n")
    .replace(/<[^>]+>/g, "")
    .replace(/!\[[^\]]*\]\(([^)]+)\)/g, (_m, u) => `[image:${toThumbnailVariantUrl(String(u || ""))}]`)
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

/**
 * Read and parse the local topic memory file into DiscussionHistoryMessage[].
 * Returns empty array if the file doesn't exist or is malformed.
 *
 * Compatible formats:
 * - Legacy 2-line entries
 * - Extended multi-line entries with text/media/reply_excerpt blocks
 */
async function readLocalTopicMemory(params: {
  topicId: string;
  log?: (level: "debug" | "info" | "warn" | "error", msg: string, data?: unknown) => void;
}): Promise<DiscussionHistoryMessage[]> {
  if (!params.topicId) return [];

  const path = joinPath(resolveTopicMemoryDir(), `topic_id_${params.topicId}.md`);
  let raw: string;
  try {
    raw = await readFile(path, "utf8");
  } catch {
    return []; // file doesn't exist — cold start
  }

  const messages: DiscussionHistoryMessage[] = [];
  const lines = raw.split("\n");
  // Pattern: - [timestamp] type:senderId(displayName) id=xxx [reply_to=xxx] [...]
  const entryRe = /^- \[([^\]]*)\]\s+([\w]+):(\S+?)(?:\(([^)]*)\))?\s+id=(\S+?)(?:\s+reply_to=(\S+))?(?:\s+.*)?$/;

  let i = 0;
  while (i < lines.length) {
    const match = lines[i].match(entryRe);
    if (!match) {
      i += 1;
      continue;
    }

    const [, createdAt, senderType, senderId, displayName, id, replyTo] = match;
    i += 1;

    const bodyLines: string[] = [];
    while (i < lines.length && !entryRe.test(lines[i])) {
      if (lines[i].startsWith("  ")) bodyLines.push(lines[i].slice(2));
      i += 1;
    }

    let content = "";
    const mediaPaths: string[] = [];
    const mediaUrls: string[] = [];
    let replyExcerpt: string | undefined;

    for (const row of bodyLines) {
      const line = row.trim();
      if (!line) continue;

      if (line.startsWith("text:")) {
        content = line.slice("text:".length).trim();
        continue;
      }

      if (line.startsWith("media_paths:")) {
        const payload = line.slice("media_paths:".length).trim();
        for (const part of payload.split("|").map((item) => item.trim()).filter(Boolean)) {
          mediaPaths.push(part);
        }
        continue;
      }

      if (line.startsWith("media_urls:")) {
        const payload = line.slice("media_urls:".length).trim();
        for (const part of payload.split("|").map((item) => item.trim()).filter(Boolean)) {
          mediaUrls.push(part);
        }
        continue;
      }

      if (line.startsWith("reply_excerpt:")) {
        replyExcerpt = line.slice("reply_excerpt:".length).trim() || undefined;
        continue;
      }

      if (!content) {
        content = line;
      } else {
        content += ` ${line}`;
      }
    }

    messages.push({
      id,
      senderId,
      senderDisplayName: displayName || undefined,
      senderType: senderType || undefined,
      content: content.trim(),
      createdAt: createdAt || undefined,
      replyTo: replyTo || undefined,
      mediaPaths,
      mediaUrls,
      replyExcerpt,
    });
  }

  return messages;
}

async function fetchDiscussionTopicMessages(params: {
  account: ResolvedWTTAccount;
  topicId: string;
  limit: number;
  log?: (level: "debug" | "info" | "warn" | "error", msg: string, data?: unknown) => void;
}): Promise<DiscussionHistoryMessage[]> {
  if (!params.account.token || !params.topicId) return [];

  try {
    const base = params.account.cloudUrl.replace(/\/$/, "");
    const resp = await fetch(`${base}/topics/${encodeURIComponent(params.topicId)}/messages?limit=${Math.max(1, params.limit)}`, {
      method: "GET",
      headers: {
        Accept: "application/json",
        "X-Agent-Token": params.account.token,
      },
    });

    if (!resp.ok) {
      params.log?.("warn", `[wtt] discussion context fetch failed topic=${params.topicId} status=${resp.status}`);
      return [];
    }

    const raw = await resp.json() as unknown;
    const source = Array.isArray(raw)
      ? raw
      : (asRecord(raw)?.messages as unknown[] | undefined) ?? (asRecord(raw)?.items as unknown[] | undefined) ?? [];

    const mapped: DiscussionHistoryMessage[] = [];
    for (const item of source) {
      const row = asRecord(item);
      if (!row) continue;

      const id = toOptionalString(row.message_id) ?? toOptionalString(row.id);
      const senderId = toOptionalString(row.sender_id) ?? "unknown";
      const content = String(row.content ?? "").trim();
      if (!id || !content) continue;

      mapped.push({
        id,
        senderId,
        senderDisplayName: toOptionalString(row.sender_display_name),
        senderType: toOptionalString(row.sender_type),
        content,
        createdAt: toOptionalString(row.created_at),
        replyTo: toOptionalString(row.reply_to),
      });
    }

    mapped.sort((a, b) => {
      const ta = a.createdAt ? Date.parse(a.createdAt) : 0;
      const tb = b.createdAt ? Date.parse(b.createdAt) : 0;
      return ta - tb;
    });

    return mapped;
  } catch (err) {
    params.log?.("warn", `[wtt] discussion context fetch error topic=${params.topicId}`, err);
    return [];
  }
}

async function hydrateDiscussionTopicMemoryIfMissing(params: {
  accountId: string;
  account: ResolvedWTTAccount;
  topicId: string;
  topicName?: string;
  limit: number;
  log?: (level: "debug" | "info" | "warn" | "error", msg: string, data?: unknown) => void;
}): Promise<void> {
  if (!params.topicId) return;

  try {
    const path = joinPath(resolveTopicMemoryDir(), `topic_id_${params.topicId}.md`);
    try {
      const existing = await readFile(path, "utf8");
      if (existing.includes("id=")) return;
    } catch {
      // file not found, continue
    }

    let topicName = params.topicName;
    const wsClient = getClient(params.accountId);

    if (!topicName && wsClient) {
      try {
        const detail = await wsClient.detail(params.topicId);
        const row = asRecord(detail);
        topicName = toOptionalString(row?.name) ?? toOptionalString(row?.title) ?? toOptionalString(row?.topic_name);
      } catch {
        // ignore detail failure
      }
    }

    let seeded: DiscussionHistoryMessage[] = [];

    if (wsClient) {
      try {
        const raw = await wsClient.history(params.topicId, Math.max(1, params.limit));
        const source = Array.isArray(raw)
          ? raw
          : (asRecord(raw)?.messages as unknown[] | undefined) ?? (asRecord(raw)?.items as unknown[] | undefined) ?? (asRecord(raw)?.data as unknown[] | undefined) ?? [];

        for (const item of source) {
          const row = asRecord(item);
          if (!row) continue;

          const id = toOptionalString(row.id) ?? toOptionalString(row.message_id);
          const contentRaw = String(row.content ?? "");
          const media = extractInboundImageMedia(contentRaw, row);
          const content = sanitizeInboundText(contentRaw).trim() || (media.mediaUrls.length > 0 ? "[media_only]" : "");
          if (!id || (!content && media.mediaUrls.length === 0)) continue;

          seeded.push({
            id,
            senderId: toOptionalString(row.sender_id) ?? "unknown",
            senderDisplayName: toOptionalString(row.sender_display_name),
            senderType: toOptionalString(row.sender_type),
            content,
            createdAt: toOptionalString(row.created_at),
            replyTo: toOptionalString(row.reply_to),
            mediaUrls: toThumbnailVariantUrls(media.mediaUrls),
          });
        }

        seeded.sort((a, b) => {
          const ta = a.createdAt ? Date.parse(a.createdAt) : 0;
          const tb = b.createdAt ? Date.parse(b.createdAt) : 0;
          return ta - tb;
        });

        if (seeded.length > 0) {
          params.log?.("info", `[wtt] discussion topic memory cold start via ws history topic=${params.topicId} count=${seeded.length}`);
        }
      } catch (err) {
        params.log?.("warn", `[wtt] discussion ws history fetch failed topic=${params.topicId}`, err);
      }
    }

    if (seeded.length === 0) {
      seeded = await fetchDiscussionTopicMessages({
        account: params.account,
        topicId: params.topicId,
        limit: params.limit,
        log: params.log,
      });
      if (seeded.length > 0) {
        params.log?.("info", `[wtt] discussion topic memory cold start via http topic=${params.topicId} count=${seeded.length}`);
      }
    }

    if (seeded.length > 0) {
      await persistDiscussionTopicMemory({
        topicId: params.topicId,
        topicName,
        messages: seeded,
        log: params.log,
      });
    }
  } catch (err) {
    params.log?.("warn", `[wtt] discussion topic memory hydrate failed topic=${params.topicId}`, err);
  }
}

async function persistDiscussionTopicMemory(params: {
  topicId: string;
  topicName?: string;
  messages: DiscussionHistoryMessage[];
  log?: (level: "debug" | "info" | "warn" | "error", msg: string, data?: unknown) => void;
}): Promise<void> {
  if (!params.topicId || params.messages.length === 0) return;

  try {
    const dir = resolveTopicMemoryDir();
    await mkdir(dir, { recursive: true });
    const path = joinPath(dir, `topic_id_${params.topicId}.md`);

    const lines: string[] = [];
    lines.push(`# topic_id_${params.topicId}`);
    if (params.topicName?.trim()) {
      lines.push(`topic_name: ${params.topicName.trim()}`);
    }
    lines.push(`updated_at: ${new Date().toISOString()}`);
    lines.push("");

    for (const msg of params.messages) {
      const ts = msg.createdAt ?? "";
      const nameTag = msg.senderDisplayName ? `(${msg.senderDisplayName})` : "";
      const who = `${msg.senderType || "unknown"}:${msg.senderId}${nameTag}`;
      const content = compactDiscussionContent(msg.content).replace(/\n/g, " ").trim();
      const mediaCount = (msg.mediaPaths?.length ?? 0) + (msg.mediaUrls?.length ?? 0);
      const contentForStore = content || (mediaCount > 0 ? "[media_only]" : "");
      lines.push(`- [${ts}] ${who} id=${msg.id}${msg.replyTo ? ` reply_to=${msg.replyTo}` : ""}${mediaCount > 0 ? ` media_count=${mediaCount}` : ""}`);
      lines.push(`  text: ${contentForStore}`);
      if (msg.mediaPaths && msg.mediaPaths.length > 0) {
        lines.push(`  media_paths: ${msg.mediaPaths.join(" | ")}`);
      }
      if (msg.mediaUrls && msg.mediaUrls.length > 0) {
        lines.push(`  media_urls: ${msg.mediaUrls.join(" | ")}`);
      }
      if (msg.replyExcerpt) {
        lines.push(`  reply_excerpt: ${msg.replyExcerpt}`);
      }
    }

    await writeFile(path, `${lines.join("\n")}\n`, "utf8");
  } catch (err) {
    params.log?.("warn", `[wtt] discussion topic memory persist failed topic=${params.topicId}`, err);
  }
}

/**
 * Append a single message to the topic memory file incrementally.
 * Called for every inbound discussion message (not just @mentions),
 * so the memory file stays up-to-date even without inference triggers.
 */
async function appendDiscussionTopicMemory(params: {
  topicId: string;
  topicName?: string;
  msg: DiscussionHistoryMessage;
  log?: (level: "debug" | "info" | "warn" | "error", msg: string, data?: unknown) => void;
}): Promise<void> {
  if (!params.topicId || !params.msg.id) return;

  try {
    const dir = resolveTopicMemoryDir();
    await mkdir(dir, { recursive: true });
    const path = joinPath(dir, `topic_id_${params.topicId}.md`);

    // Check if message already recorded (idempotent)
    let existing = "";
    try {
      existing = await readFile(path, "utf8");
    } catch {
      // File doesn't exist yet — will create with header
    }

    const idMarker = `id=${params.msg.id}`;
    const history = existing ? await readLocalTopicMemory({ topicId: params.topicId }) : [];
    if (existing.includes(idMarker)) {
      // Upsert path: same message id may arrive first without media (push) and
      // later with richer media URLs (poll). Merge fields instead of dropping.
      const existingIdx = history.findIndex((item) => item.id === params.msg.id);
      if (existingIdx >= 0) {
        const current = history[existingIdx];
        const incomingContent = compactDiscussionContent(params.msg.content).replace(/\n/g, " ").trim();
        const incomingMediaPaths = Array.from(new Set((params.msg.mediaPaths ?? []).map((v) => String(v || "").trim()).filter(Boolean)));
        const incomingMediaUrls = Array.from(
          new Set(
            (params.msg.mediaUrls ?? [])
              .map((v) => toThumbnailVariantUrl(String(v || "").trim()))
              .filter(Boolean),
          ),
        );

        const mergedMediaPaths = Array.from(new Set([...(current.mediaPaths ?? []), ...incomingMediaPaths]));
        const mergedMediaUrls = Array.from(
          new Set(
            [...(current.mediaUrls ?? []), ...incomingMediaUrls]
              .map((v) => toThumbnailVariantUrl(String(v || "").trim()))
              .filter(Boolean),
          ),
        );
        const mergedContent = (current.content && current.content !== "[media_only]")
          ? current.content
          : (incomingContent || current.content || "");

        const changed = mergedMediaPaths.length !== (current.mediaPaths ?? []).length
          || mergedMediaUrls.length !== (current.mediaUrls ?? []).length
          || mergedContent !== current.content;

        if (changed) {
          history[existingIdx] = {
            ...current,
            content: mergedContent,
            mediaPaths: mergedMediaPaths,
            mediaUrls: mergedMediaUrls,
          };
          await persistDiscussionTopicMemory({
            topicId: params.topicId,
            topicName: params.topicName,
            messages: history,
            log: params.log,
          });
        }
      }
      return;
    }

    const replyTarget = params.msg.replyTo
      ? history.find((item) => item.id === params.msg.replyTo)
      : undefined;
    const replyExcerpt = replyTarget
      ? compactDiscussionContent(replyTarget.content).slice(0, 220)
      : undefined;

    const ts = params.msg.createdAt ?? new Date().toISOString();
    const nameTag = params.msg.senderDisplayName ? `(${params.msg.senderDisplayName})` : "";
    const who = `${params.msg.senderType || "unknown"}:${params.msg.senderId}${nameTag}`;
    const content = compactDiscussionContent(params.msg.content).replace(/\n/g, " ").trim();
    const mediaPaths = Array.from(new Set((params.msg.mediaPaths ?? []).map((v) => String(v || "").trim()).filter(Boolean)));
    const mediaUrls = Array.from(
      new Set(
        (params.msg.mediaUrls ?? [])
          .map((v) => toThumbnailVariantUrl(String(v || "").trim()))
          .filter(Boolean),
      ),
    );
    const mediaCount = mediaPaths.length + mediaUrls.length;
    const contentForStore = content || (mediaCount > 0 ? "[media_only]" : "");

    const lines: string[] = [];
    lines.push(`- [${ts}] ${who} ${idMarker}${params.msg.replyTo ? ` reply_to=${params.msg.replyTo}` : ""}${mediaCount > 0 ? ` media_count=${mediaCount}` : ""}`);
    lines.push(`  text: ${contentForStore}`);
    if (mediaPaths.length > 0) {
      lines.push(`  media_paths: ${mediaPaths.join(" | ")}`);
    }
    if (mediaUrls.length > 0) {
      lines.push(`  media_urls: ${mediaUrls.join(" | ")}`);
    }
    if (replyExcerpt) {
      lines.push(`  reply_excerpt: ${replyExcerpt}`);
    }

    if (!existing) {
      // Create file with header
      const headerLines = [`# topic_id_${params.topicId}`];
      if (params.topicName?.trim()) {
        headerLines.push(`topic_name: ${params.topicName.trim()}`);
      }
      headerLines.push(`updated_at: ${new Date().toISOString()}`);
      headerLines.push("");
      await writeFile(path, `${headerLines.join("\n")}\n${lines.join("\n")}\n`, "utf8");
    } else {
      // Append to existing file
      await writeFile(path, `${existing.trimEnd()}\n${lines.join("\n")}\n`, "utf8");
    }
  } catch (err) {
    params.log?.("warn", `[wtt] discussion topic memory append failed topic=${params.topicId}`, err);
  }
}

function extractDiscussionSearchTokens(text: string): string[] {
  const source = compactDiscussionContent(text || "").toLowerCase();
  if (!source) return [];

  const tokens = new Set<string>();

  const latin = source.match(/[a-z0-9_\-]{2,}/g) ?? [];
  for (const token of latin) tokens.add(token);

  const hanBlocks = source.match(/[\u4e00-\u9fff]{2,}/g) ?? [];
  for (const block of hanBlocks) {
    tokens.add(block);
    for (let i = 0; i < block.length - 1; i += 1) {
      tokens.add(block.slice(i, i + 2));
    }
  }

  return Array.from(tokens).slice(0, 24);
}

function buildDiscussionContextBlock(params: {
  messages: DiscussionHistoryMessage[];
  currentMessageId: string;
  windowSize: number;
  maxChars: number;
  replyTo?: string;
}): string {
  if (params.messages.length === 0) return "";

  const currentIdx = Math.max(0, params.messages.findIndex((m) => m.id === params.currentMessageId));
  const start = Math.max(0, currentIdx - Math.max(1, params.windowSize));
  const focus = params.messages.slice(start, currentIdx + 1);

  const lines: string[] = [];
  lines.push("[TOPIC_CONTEXT]");
  lines.push("以下为当前讨论话题最近消息（按时间顺序）。回答时请结合这些上下文，不要只看 @ 内容。\n");

  if (params.replyTo) {
    const target = params.messages.find((m) => m.id === params.replyTo);
    if (target) {
      const targetName = target.senderDisplayName ? `(${target.senderDisplayName})` : "";
      lines.push(`[被回复消息] id=${target.id} sender=${target.senderId}${targetName}`);
      lines.push(compactDiscussionContent(target.content).slice(0, 1200));
      if (target.mediaPaths && target.mediaPaths.length > 0) {
        lines.push(`media_paths: ${target.mediaPaths.join(" | ")}`);
      }
      if (target.mediaUrls && target.mediaUrls.length > 0) {
        lines.push(`media_urls: ${target.mediaUrls.join(" | ")}`);
      }
      lines.push("");
    }
  }

  for (const msg of focus) {
    const compact = compactDiscussionContent(msg.content);
    const hasMedia = Boolean((msg.mediaPaths && msg.mediaPaths.length > 0) || (msg.mediaUrls && msg.mediaUrls.length > 0));
    if (!compact && !hasMedia) continue;
    const nameTag = msg.senderDisplayName ? `(${msg.senderDisplayName})` : "";
    const mediaTag = (msg.mediaPaths && msg.mediaPaths.length > 0)
      ? ` media_paths=${msg.mediaPaths.join("|")}`
      : ((msg.mediaUrls && msg.mediaUrls.length > 0) ? ` media_urls=${msg.mediaUrls.join("|")}` : "");
    const replyExcerptTag = msg.replyExcerpt ? ` reply_excerpt=${msg.replyExcerpt}` : "";
    lines.push(`- id=${msg.id} sender=${msg.senderId}${nameTag}${msg.replyTo ? ` reply_to=${msg.replyTo}` : ""}${mediaTag}${replyExcerptTag}: ${compact || "[media_message]"}`);
  }

  // Precision retrieval for long discussion topics:
  // lexical+reply aware hit selection across full topic memory.
  const currentMessage = params.messages[currentIdx];
  const queryTokens = extractDiscussionSearchTokens(currentMessage?.content ?? "");
  if (queryTokens.length > 0 && params.messages.length > Math.max(40, focus.length + 10)) {
    const focusIds = new Set(focus.map((m) => m.id));
    const scored = params.messages
      .filter((m) => !focusIds.has(m.id))
      .map((m) => {
        const hay = [
          compactDiscussionContent(m.content || ""),
          m.replyExcerpt || "",
          ...(m.mediaUrls ?? []),
          ...(m.mediaPaths ?? []),
        ].join(" ").toLowerCase();
        let score = 0;
        for (const tk of queryTokens) {
          if (tk && hay.includes(tk)) score += tk.length >= 4 ? 3 : 1;
        }
        if (params.replyTo && m.id === params.replyTo) score += 8;
        if (params.replyTo && m.replyTo === params.replyTo) score += 4;
        if (currentMessage?.replyTo && m.id === currentMessage.replyTo) score += 6;
        return { m, score };
      })
      .filter((item) => item.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 8);

    if (scored.length > 0) {
      lines.push("");
      lines.push("[检索命中]");
      for (const { m, score } of scored) {
        const compact = compactDiscussionContent(m.content || "") || "[media_message]";
        const mediaTag = (m.mediaPaths && m.mediaPaths.length > 0)
          ? ` media_paths=${m.mediaPaths.join("|")}`
          : ((m.mediaUrls && m.mediaUrls.length > 0) ? ` media_urls=${m.mediaUrls.join("|")}` : "");
        lines.push(`- score=${score} id=${m.id} sender=${m.senderId}${m.replyTo ? ` reply_to=${m.replyTo}` : ""}${mediaTag}: ${compact.slice(0, 240)}`);
      }
    }
  }

  let block = lines.join("\n").trim();
  if (block.length > params.maxChars) {
    block = block.slice(block.length - params.maxChars);
    block = `[TOPIC_CONTEXT-TRUNCATED]\n${block}`;
  }
  return block;
}

function isMeaningfulUserText(text: string): boolean {
  const t = (text || "").trim();
  if (!t) return false;

  // Drop visual-only box characters/separators.
  const visualOnly = t.replace(/[\s│┌┐└┘─\-_=]+/g, "").trim();
  if (!visualOnly) return false;

  // Drop status heartbeat style lines from execution stream.
  if (/^\[\d{4}-\d{2}-\d{2}T[^\]]+\]\s*状态=/.test(t)) return false;
  if (/^状态=.+\|\s*动作=.+\|\s*心跳=\d+s$/i.test(t)) return false;

  return true;
}

function isSystemLikeInbound(raw: WsMessagePayload & Record<string, unknown>, text: string): boolean {
  const semanticType = String(raw.semantic_type ?? "").toLowerCase();
  const senderType = String(raw.sender_type ?? "").toLowerCase();
  const contentType = String(raw.content_type ?? "").toLowerCase();

  if (senderType === "system") return true;
  if (semanticType.startsWith("system") || semanticType === "task_progress") return true;
  if (["task_request", "task_run", "task_status", "task_summary", "task_blocked", "task_review", "notification"].includes(semanticType)) {
    return true;
  }
  if (contentType === "system") return true;
  if (text.startsWith("[system:")) return true;

  return false;
}

function isTaskBootstrapPlaceholderText(text: string): boolean {
  const t = (text || "").trim().toLowerCase();
  if (!t) return true;
  return t === "new task" || t === "新任务" || t === "(无描述)" || t === "无描述";
}

function isBlockedDiscussModelCommand(raw: WsMessagePayload & Record<string, unknown>, text: string): boolean {
  const topicType = String(raw.topic_type ?? "").toLowerCase();
  if (topicType !== "discussion") return false;

  // Task-linked discussion topics must keep model selection available.
  const taskId = toOptionalString(raw.task_id);
  const topicName = String(raw.topic_name ?? "");
  const isTaskLinked = Boolean(taskId || topicName.startsWith("TASK-"));
  if (isTaskLinked) return false;

  const normalized = (text || "").trim().toLowerCase();
  return /^\/models?(\s|$)/.test(normalized);
}

function normalizeMentionToken(raw: string): string {
  const lowered = (raw || "")
    .normalize("NFKC")
    .trim()
    .replace(/^@+/, "")
    .toLowerCase();

  return lowered.replace(/[^\p{L}\p{N}]+/gu, "");
}

function extractMentionHandles(content: string): string[] {
  const handles = new Set<string>();

  // Parse @mentions as agent-like handles using ASCII-safe token rules.
  // Why:
  // - Discuss topics often contain CJK text immediately after mention, e.g. "@lyz_agent看看"
  // - Unicode-wide token regex may swallow trailing CJK and produce "lyzagent看看"
  // - We need strict/precise handle extraction for routing gate.
  const regex = /(^|[^A-Za-z0-9_])@([A-Za-z0-9][A-Za-z0-9._-]{0,63})/g;
  let match: RegExpExecArray | null;

  while ((match = regex.exec(content)) !== null) {
    const token = normalizeMentionToken(match[2] || "");
    if (token) handles.add(token);
  }

  return Array.from(handles);
}

function buildAgentMentionAliases(agentId: string, agentName?: string): Set<string> {
  const aliases = new Set<string>();

  const addAlias = (candidate?: string): void => {
    if (!candidate) return;
    const normalized = normalizeMentionToken(candidate);
    if (normalized) aliases.add(normalized);
  };

  addAlias(agentId);

  if (agentName) {
    addAlias(agentName);
    addAlias(agentName.replace(/\s+/g, "_"));
    addAlias(agentName.replace(/\s+/g, "-"));
  }

  return aliases;
}

function resolveMentionMatch(content: string, agentId: string, agentName?: string): {
  hasMentions: boolean;
  matchesAgent: boolean;
} {
  const mentions = extractMentionHandles(content || "");
  if (mentions.length === 0) {
    return { hasMentions: false, matchesAgent: false };
  }

  const aliases = buildAgentMentionAliases(agentId, agentName);
  const matchesAgent = mentions.some((mention) => aliases.has(mention));

  return {
    hasMentions: true,
    matchesAgent,
  };
}

function matchesAgentIdentity(candidate: string | undefined, agentId: string, agentName?: string): boolean {
  const normalized = normalizeMentionToken(candidate ?? "");
  if (!normalized) return false;

  const aliases = buildAgentMentionAliases(agentId, agentName);
  return aliases.has(normalized);
}

function isStandaloneSlashCommandText(text: string): boolean {
  const trimmed = text.trim();
  if (!trimmed.startsWith("/")) return false;
  if (trimmed.includes("\n")) return false;
  return /^\/[a-z][a-z0-9_:-]*(?:\s+[\s\S]*)?$/i.test(trimmed);
}

function normalizeSlashForWttCommandRouter(text: string, account: ResolvedWTTAccount): string {
  const trimmed = text.trim();
  if (!trimmed.startsWith("/")) return text;

  const prefixOnly = account.config.slashCompatWttPrefixOnly ?? DEFAULT_SLASH_COMPAT_WTT_PREFIX_ONLY;
  if (prefixOnly) return text;

  const aliasMap: Record<string, string> = {
    task: "task",
    pipeline: "pipeline",
    pipe: "pipeline",
    delegate: "delegate",
    list: "list",
    find: "find",
    join: "join",
    leave: "leave",
    publish: "publish",
    poll: "poll",
    history: "history",
    p2p: "p2p",
    detail: "detail",
    subscribed: "subscribed",
    config: "config",
    cfg: "config",
    bind: "bind",
    whoami: "whoami",
    help: "help",
    update: "update",
    upgrade: "update",
  };

  const match = trimmed.match(/^\/([a-z][a-z0-9_:-]*)(?:\s+([\s\S]*))?$/i);
  if (!match) return text;

  const verb = match[1].toLowerCase();
  if (verb === "wtt") return text;
  const mapped = aliasMap[verb];
  if (!mapped) return text;

  const args = (match[2] ?? "").trim();
  return args ? `/wtt ${mapped} ${args}` : `/wtt ${mapped}`;
}

/**
 * Inference gating: decide if this inbound message should trigger LLM reasoning.
 *
 * Rules:
 * - Broadcast topics never trigger.
 * - Task-linked topics do not require @mention; runner_agent_id/name is used when available.
 * - Discussion topics require explicit @mention for this agent.
 * - P2P topics never require @mention.
 */
function shouldTriggerInference(
  raw: WsMessagePayload & Record<string, unknown>,
  agentId: string,
  agentName?: string,
): { trigger: boolean; reason?: string } {
  const topicType = String(raw.topic_type ?? "").toLowerCase();

  // Broadcast topics — never auto-infer.
  if (topicType === "broadcast") {
    return { trigger: false, reason: "broadcast_no_infer" };
  }

  const taskId = toOptionalString(raw.task_id);
  const topicName = String(raw.topic_name ?? "");
  const isTaskLinked = Boolean(taskId || topicName.startsWith("TASK-"));

  if (isTaskLinked) {
    const senderType = String(raw.sender_type ?? "").toLowerCase();
    if (senderType && senderType !== "human" && senderType !== "user") {
      return { trigger: false, reason: "task_non_human_sender" };
    }
    const runnerAgentId = toOptionalString(raw.runner_agent_id) ?? toOptionalString(raw.runnerAgentId);
    const runnerAgentName = toOptionalString(raw.runner_agent_name) ?? toOptionalString(raw.runnerAgentName);
    if (runnerAgentId || runnerAgentName) {
      if (
        matchesAgentIdentity(runnerAgentId, agentId, agentName)
        || matchesAgentIdentity(runnerAgentName, agentId, agentName)
      ) {
        return { trigger: true, reason: "task_linked_runner_match" };
      }
      return { trigger: false, reason: "task_runner_mismatch" };
    }

    return { trigger: true, reason: "task_linked" };
  }

  // Only discuss topics require explicit mention.
  // Fallback: accept backend-resolved runner targeting for renamed agent names.
  if (topicType === "discussion") {
    const content = String(raw.content ?? "");
    const mentionMatch = resolveMentionMatch(content, agentId, agentName);
    if (mentionMatch.matchesAgent) {
      return { trigger: true };
    }

    const runnerAgentId = toOptionalString(raw.runner_agent_id) ?? toOptionalString(raw.runnerAgentId);
    const runnerAgentName = toOptionalString(raw.runner_agent_name) ?? toOptionalString(raw.runnerAgentName);
    if (
      matchesAgentIdentity(runnerAgentId, agentId, agentName)
      || matchesAgentIdentity(runnerAgentName, agentId, agentName)
    ) {
      return { trigger: true, reason: "discussion_runner_match" };
    }

    return { trigger: false, reason: "discussion_no_mention" };
  }

  // p2p / collaborative / unknown — infer by default.
  return { trigger: true };
}

function toPositiveInt(raw: unknown, fallback: number): number {
  const n = Number(raw);
  if (!Number.isFinite(n) || n <= 0) return fallback;
  return Math.floor(n);
}

function asRecord(value: unknown): Record<string, unknown> | undefined {
  if (!value || typeof value !== "object") return undefined;
  return value as Record<string, unknown>;
}

function parseInboundMetadata(raw: WsMessagePayload & Record<string, unknown>): Record<string, unknown> | undefined {
  const direct = raw.metadata;
  if (direct && typeof direct === "object") return direct as Record<string, unknown>;
  if (typeof direct === "string") {
    try {
      const parsed = JSON.parse(direct) as unknown;
      return parsed && typeof parsed === "object" ? parsed as Record<string, unknown> : undefined;
    } catch {
      return undefined;
    }
  }
  return undefined;
}

function coerceWsNewMessage(raw: unknown): WsNewMessage | undefined {
  const record = asRecord(raw);
  if (!record) return undefined;

  const wrapped = asRecord(record.message);
  if (record.type === "new_message" && wrapped) {
    return {
      type: "new_message",
      message: wrapped as unknown as WsMessagePayload,
    };
  }

  if (wrapped && toOptionalString(wrapped.id)) {
    return {
      type: "new_message",
      message: wrapped as unknown as WsMessagePayload,
    };
  }

  if (toOptionalString(record.id) && resolveInboundTopicId(record as unknown as WsMessagePayload & Record<string, unknown>) && toOptionalString(record.sender_id)) {
    return {
      type: "new_message",
      message: record as unknown as WsMessagePayload,
    };
  }

  return undefined;
}

export function extractPolledInboundMessages(raw: unknown): WsNewMessage[] {
  let candidates: unknown[] = [];

  if (Array.isArray(raw)) {
    candidates = raw;
  } else {
    const record = asRecord(raw);
    const nested = asRecord(record?.data);
    if (Array.isArray(record?.messages)) candidates = record!.messages as unknown[];
    else if (Array.isArray(record?.data)) candidates = record!.data as unknown[];
    else if (Array.isArray(nested?.messages)) candidates = nested!.messages as unknown[];
    else if (Array.isArray(nested?.items)) candidates = nested!.items as unknown[];
  }

  const parsed: WsNewMessage[] = [];
  for (const item of candidates) {
    const msg = coerceWsNewMessage(item);
    if (msg) parsed.push(msg);
  }

  return parsed;
}

function resolveInboundTopicId(msg: WsMessagePayload & Record<string, unknown>): string {
  const direct = toOptionalString(msg.topic_id) ?? toOptionalString(msg.topicId) ?? toOptionalString(msg.p2p_topic_id);
  if (direct) return direct;

  const nestedTopic = asRecord(msg.topic);
  const nestedId = nestedTopic ? toOptionalString(nestedTopic.id) : undefined;
  if (nestedId) return nestedId;

  return "";
}

function resolveInboundDedupKey(msg: WsNewMessage): string {
  const payload = msg.message as WsMessagePayload & Record<string, unknown>;
  const { mediaUrls } = extractInboundImageMedia(String(payload.content ?? ""), payload);
  const mediaSig = mediaUrls.slice(0, 4).join("|") || "no-media";
  const contentSig = String(payload.content ?? "").slice(0, 48);
  const directId = toOptionalString(payload.id);
  if (directId) return `${directId}:${mediaSig}:${contentSig}`;

  const topicId = resolveInboundTopicId(payload) || "no-topic";
  const senderId = toOptionalString(payload.sender_id) ?? "unknown";
  const createdAt = toOptionalString(payload.created_at) ?? "";
  const content = String(payload.content ?? "").slice(0, 96);
  return `${topicId}:${senderId}:${createdAt}:${mediaSig}:${content}`;
}

function isLikelyP2PMessage(msg: WsMessagePayload & Record<string, unknown>): boolean {
  const topicType = String(msg.topic_type ?? "").toLowerCase();
  if (topicType === "p2p") return true;

  const topicId = resolveInboundTopicId(msg);

  // Legacy p2p push payloads only contain id/topic_id/sender_id/content/created_at/encrypted.
  // If type hints are absent and we still have a topic+sender, treat as p2p.
  if (!topicType && topicId && msg.sender_id && !msg.content_type && !msg.semantic_type && !msg.sender_type) {
    return true;
  }

  // Current deployment only enables encryption on P2P; if we observe encrypted payload
  // without explicit topic_type (e.g. poll fallback), treat as P2P for routing/encryption cache.
  if (!topicType && topicId && Boolean(msg.encrypted)) {
    return true;
  }

  return false;
}

export type NormalizedInboundWsMessage = {
  text: string;
  senderId: string;
  senderName?: string;
  topicId: string;
  topicName?: string;
  messageId: string;
  timestamp: string;
  chatType: "direct" | "group";
  routePeerId: string;
  to: string;
  from: string;
  conversationLabel: string;
  /** Image URLs extracted from message content (HTML <img> or markdown ![](url)) */
  mediaUrls: string[];
  mediaTypes: string[];
};

export function normalizeInboundWsMessage(params: {
  msg: WsNewMessage;
  decryptedContent?: string;
}): NormalizedInboundWsMessage {
  const raw = params.msg.message as WsMessagePayload & Record<string, unknown>;
  const senderId = String(raw.sender_id || "unknown");
  const topicId = resolveInboundTopicId(raw);
  const senderName = toOptionalString(raw.sender_display_name);
  const topicName = toOptionalString(raw.topic_name);

  const rawContent = params.decryptedContent ?? String(raw.content ?? "");
  let content = sanitizeInboundText(rawContent);
  const messageId = toOptionalString(raw.id) ?? `${topicId || "no-topic"}:${senderId}:${Date.now()}`;
  const timestamp = toIsoTimestamp(raw.created_at);

  // Extract image URLs from original message body for OpenClaw media-understanding pipeline.
  const { mediaUrls, mediaTypes } = extractInboundImageMedia(rawContent, raw);

  // If message is image-only after sanitization, keep a minimal prompt so it
  // won't be dropped by empty-message gating.
  if (!content.trim() && mediaUrls.length > 0) {
    content = "请结合这张图片内容进行识别并回复。";
  }

  const isP2P = isLikelyP2PMessage(raw);
  const hasTopicId = Boolean(topicId);
  const chatType: "direct" | "group" = isP2P ? "direct" : "group";
  const routePeerId = isP2P
    ? (hasTopicId ? topicId : senderId)
    : topicId || senderId;
  // Always publish to the specific topic_id so responses land in the correct
  // P2P topic (e.g. worker topics vs default P2P between the same two parties).
  const to = hasTopicId ? `topic:${topicId}` : `p2p:${senderId}`;
  const from = `wtt:${senderId}`;

  const conversationLabel = isP2P
    ? `p2p:${topicName ?? senderName ?? (hasTopicId ? topicId : senderId)}`
    : `topic:${topicName ?? (topicId || "unknown")}`;

  return {
    text: content,
    senderId,
    senderName,
    topicId,
    topicName,
    messageId,
    timestamp,
    chatType,
    routePeerId,
    to,
    from,
    conversationLabel,
    mediaUrls,
    mediaTypes,
  };
}

export type InboundRoutingResult = {
  routed: boolean;
  reason?: "runtime_unavailable" | "self_echo" | "empty_message" | "system_message" | "agent_no_mention" | "broadcast_no_infer" | "discussion_no_mention" | "task_runner_mismatch" | "task_non_human_sender";
};

export type InboundRelayStats = {
  pushReceivedCount: number;
  pollFetchedCount: number;
  routedCount: number;
  dedupDroppedCount: number;
};

export function createInboundMessageRelay(params: {
  cfg: OpenClawConfig;
  accountId: string;
  account: ResolvedWTTAccount;
  getLatestAccount?: () => ResolvedWTTAccount;
  channelRuntime?: ChannelRuntimeLike;
  decryptContent?: (content: string) => Promise<string>;
  deliver?: (params: { to: string; payload: Record<string, unknown> }) => Promise<void>;
  typingSignal?: (params: { topicId: string; state: "start" | "stop"; ttlMs?: number }) => Promise<void>;
  log?: (level: "debug" | "info" | "warn" | "error", msg: string, data?: unknown) => void;
  dedupWindowMs?: number;
  dedupMaxEntries?: number;
}): {
  stats: InboundRelayStats;
  handlePush: (msg: WsNewMessage) => Promise<InboundRoutingResult>;
  handlePollResult: (rawPollResult: unknown) => Promise<{ fetched: number; routed: number; dedupDropped: number }>;
} {
  const dedupWindowMs = toPositiveInt(params.dedupWindowMs, DEFAULT_INBOUND_DEDUP_WINDOW_MS);
  const dedupMaxEntries = toPositiveInt(params.dedupMaxEntries, DEFAULT_INBOUND_DEDUP_MAX_ENTRIES);
  const dedupSeenAt = new Map<string, number>();

  const stats: InboundRelayStats = {
    pushReceivedCount: 0,
    pollFetchedCount: 0,
    routedCount: 0,
    dedupDroppedCount: 0,
  };

  const pruneDedup = (nowMs: number): void => {
    const ttlCutoff = nowMs - dedupWindowMs;
    for (const [id, seenAt] of dedupSeenAt) {
      if (seenAt >= ttlCutoff) break;
      dedupSeenAt.delete(id);
    }

    while (dedupSeenAt.size > dedupMaxEntries) {
      const oldest = dedupSeenAt.keys().next().value;
      if (!oldest) break;
      dedupSeenAt.delete(oldest);
    }
  };

  const isDuplicate = (msg: WsNewMessage): boolean => {
    const key = resolveInboundDedupKey(msg);
    const nowMs = Date.now();
    pruneDedup(nowMs);
    const seenAt = dedupSeenAt.get(key);
    if (typeof seenAt === "number" && nowMs - seenAt <= dedupWindowMs) {
      return true;
    }

    dedupSeenAt.set(key, nowMs);
    return false;
  };

  const routeOne = async (msg: WsNewMessage, source: "push" | "poll"): Promise<InboundRoutingResult> => {
    if (isDuplicate(msg)) {
      stats.dedupDroppedCount += 1;
      params.log?.(
        "debug",
        `[${params.accountId}] inbound dedup dropped source=${source} dedup_dropped=${stats.dedupDroppedCount}`,
      );
      return { routed: false };
    }

    const result = await routeInboundWsMessage({
      cfg: params.cfg,
      accountId: params.accountId,
      account: params.getLatestAccount?.() ?? params.account,
      msg,
      channelRuntime: params.channelRuntime,
      decryptContent: params.decryptContent,
      deliver: params.deliver,
      typingSignal: params.typingSignal,
      log: params.log,
    });

    if (result.routed) stats.routedCount += 1;

    params.log?.(
      "debug",
      `[${params.accountId}] inbound counters push_received=${stats.pushReceivedCount} poll_fetched=${stats.pollFetchedCount} routed=${stats.routedCount} dedup_dropped=${stats.dedupDroppedCount}`,
    );

    return result;
  };

  return {
    stats,
    async handlePush(msg: WsNewMessage): Promise<InboundRoutingResult> {
      stats.pushReceivedCount += 1;
      return routeOne(msg, "push");
    },
    async handlePollResult(rawPollResult: unknown): Promise<{ fetched: number; routed: number; dedupDropped: number }> {
      const messages = extractPolledInboundMessages(rawPollResult);
      stats.pollFetchedCount += messages.length;

      const beforeRouted = stats.routedCount;
      const beforeDedup = stats.dedupDroppedCount;

      for (const msg of messages) {
        await routeOne(msg, "poll");
      }

      const routed = stats.routedCount - beforeRouted;
      const dedupDropped = stats.dedupDroppedCount - beforeDedup;
      params.log?.(
        "info",
        `[${params.accountId}] inbound poll fetched=${messages.length} routed=${routed} dedup_dropped=${dedupDropped} totals(push=${stats.pushReceivedCount},poll=${stats.pollFetchedCount},routed=${stats.routedCount},dedup=${stats.dedupDroppedCount})`,
      );

      return {
        fetched: messages.length,
        routed,
        dedupDropped,
      };
    },
  };
}

async function deliverReplyPayload(params: {
  to: string;
  payload: Record<string, unknown>;
  replyTo?: string;
  accountId: string;
  cfg: OpenClawConfig;
}): Promise<void> {
  const text = typeof params.payload.text === "string" ? params.payload.text : "";
  const isReasoning = Boolean(params.payload.isReasoning);
  if (isReasoning) return;

  const mediaUrls = Array.isArray(params.payload.mediaUrls)
    ? params.payload.mediaUrls.filter((item): item is string => typeof item === "string" && item.trim().length > 0)
    : [];

  const mediaUrl = typeof params.payload.mediaUrl === "string" ? params.payload.mediaUrl.trim() : "";
  if (mediaUrl) mediaUrls.push(mediaUrl);

  if (mediaUrls.length > 0) {
    let first = true;
    for (const media of mediaUrls) {
      await sendMedia({
        to: params.to,
        text: first ? text : "",
        mediaUrl: media,
        replyTo: params.replyTo,
        accountId: params.accountId,
        cfg: params.cfg,
      });
      first = false;
    }
    return;
  }

  if (!text) return;

  await sendText({
    to: params.to,
    text,
    replyTo: params.replyTo,
    accountId: params.accountId,
    cfg: params.cfg,
  });
}

export async function routeInboundWsMessage(params: {
  cfg: OpenClawConfig;
  accountId: string;
  account: ResolvedWTTAccount;
  msg: WsNewMessage;
  channelRuntime?: ChannelRuntimeLike;
  decryptContent?: (content: string) => Promise<string>;
  deliver?: (params: { to: string; payload: Record<string, unknown> }) => Promise<void>;
  typingSignal?: (params: { topicId: string; state: "start" | "stop"; ttlMs?: number }) => Promise<void>;
  log?: (level: "debug" | "info" | "warn" | "error", msg: string, data?: unknown) => void;
}): Promise<InboundRoutingResult> {
  const runtime = params.channelRuntime;
  if (!runtime) {
    params.log?.("warn", `[${params.accountId}] channelRuntime unavailable; inbound message skipped`);
    return { routed: false, reason: "runtime_unavailable" };
  }

  const rawContent = String(params.msg.message.content ?? "");
  let decryptedContent = rawContent;
  if (params.msg.message.encrypted && params.decryptContent) {
    try {
      decryptedContent = await params.decryptContent(rawContent);
    } catch (err) {
      params.log?.("warn", `[${params.accountId}] Failed to decrypt inbound content, using raw`, err);
      decryptedContent = rawContent;
    }
  }

  let normalized = normalizeInboundWsMessage({
    msg: params.msg,
    decryptedContent,
  });

  const rawMsg = params.msg.message as WsMessagePayload & Record<string, unknown>;
  if (normalized.mediaUrls.length > 0) {
    const absMediaUrls = absolutizeInboundMediaUrls(normalized.mediaUrls, params.account.cloudUrl);
    normalized = {
      ...normalized,
      mediaUrls: absMediaUrls,
      mediaTypes: absMediaUrls.map(() => "image/png"),
    };
  }
  const inboundTaskId = toOptionalString(rawMsg.task_id);
  const inferredTopicType = String(rawMsg.topic_type ?? "").toLowerCase();
  if (normalized.topicId) {
    if (inferredTopicType) {
      rememberTopicType(normalized.topicId, inferredTopicType);
    } else if (isLikelyP2PMessage(rawMsg)) {
      rememberTopicType(normalized.topicId, "p2p");
    }
  }
  const typingTopicId = normalized.topicId?.trim() || "";
  const mentionMatch = resolveMentionMatch(String(rawMsg.content ?? ""), params.account.agentId, params.account.name);
  const originalMediaUrls = normalized.mediaUrls.slice();
  const originalMediaTypes = normalized.mediaTypes.slice();

  // Remember recent media from this sender/topic even when the message itself
  // does not trigger inference (for example: image first, @mention second).
  if (typingTopicId && originalMediaUrls.length > 0) {
    rememberRecentTopicMedia(typingTopicId, normalized.senderId, originalMediaUrls, originalMediaTypes);
    params.log?.("info", `[${params.accountId}] inbound media captured topic=${typingTopicId} sender=${normalized.senderId} count=${originalMediaUrls.length}`);
  }

  // If current @mention message carries no media, try to reuse sender's latest
  // media in the same topic so "image + @mention" split messages still work.
  if (
    typingTopicId
    && normalized.mediaUrls.length === 0
    && mentionMatch.matchesAgent
    && looksLikeImageFollowupText(normalized.text)
  ) {
    const recentMedia = readRecentTopicMedia(typingTopicId, normalized.senderId);
    if (recentMedia && recentMedia.mediaUrls.length > 0) {
      normalized = {
        ...normalized,
        mediaUrls: recentMedia.mediaUrls,
        mediaTypes: recentMedia.mediaTypes,
      };
      params.log?.("info", `[${params.accountId}] inbound media hydrated from recent cache topic=${typingTopicId} sender=${normalized.senderId} count=${recentMedia.mediaUrls.length}`);
    } else {
      const rawKeys = Object.keys(rawMsg || {}).slice(0, 40).join(",");
      const md = parseInboundMetadata(rawMsg);
      const metadataKeys = md ? Object.keys(md).slice(0, 30).join(",") : "";
      const contentPreview = String(rawMsg.content ?? "").slice(0, 120).replace(/\s+/g, " ");
      params.log?.("info", `[${params.accountId}] inbound media cache_miss topic=${typingTopicId} sender=${normalized.senderId} raw_keys=${rawKeys} metadata_keys=${metadataKeys} content_preview=${contentPreview}`);
    }
  }


  const emitTypingSignal = async (state: "start" | "stop"): Promise<void> => {
    if (!typingTopicId || !params.typingSignal) return;
    try {
      await params.typingSignal({ topicId: typingTopicId, state, ttlMs: 6000 });
    } catch (err) {
      params.log?.("debug", `[${params.accountId}] typing signal ${state} failed topic=${typingTopicId}`, err);
    }
  };

  const patchTaskStatus = async (taskId: string, status: string, notes?: string): Promise<boolean> => {
    if (!params.account.token) return false;

    try {
      const body: Record<string, unknown> = {
        status,
        runner_agent_id: params.account.agentId || undefined,
      };
      if (notes && notes.trim()) {
        body.notes = notes.trim();
      }

      const resp = await fetch(`${params.account.cloudUrl.replace(/\/$/, "")}/tasks/${encodeURIComponent(taskId)}`, {
        method: "PATCH",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
          Authorization: `Bearer ${params.account.token}`,
          "X-Agent-Token": params.account.token,
        },
        body: JSON.stringify(body),
      });
      return resp.ok;
    } catch {
      return false;
    }
  };

  if (isSystemLikeInbound(rawMsg, normalized.text)) {
    // Ignore transport/system chatter in user-facing conversation flow.
    return { routed: false, reason: "system_message" };
  }

  if (normalized.senderId === params.account.agentId) {
    // Ignore own echo to avoid self-reply loops.
    return { routed: false, reason: "self_echo" };
  }

  if (inboundTaskId && isTaskBootstrapPlaceholderText(normalized.text)) {
    // Ignore placeholder bootstrap text in task topics (e.g. default "New Task").
    return { routed: false, reason: "empty_message" };
  }

  if (isBlockedDiscussModelCommand(rawMsg, normalized.text)) {
    // In discussion topics, block model switching commands to avoid all agents
    // responding to the same slash command.
    return { routed: false, reason: "system_message" };
  }

  const slashCompatEnabled = params.account.config.slashCompat ?? DEFAULT_SLASH_COMPAT_ENABLED;
  const slashBypassMentionGate = params.account.config.slashBypassMentionGate ?? DEFAULT_SLASH_BYPASS_MENTION_GATE;

  const topicType = String(rawMsg.topic_type ?? "").toLowerCase();
  const topicName = String(rawMsg.topic_name ?? "");
  const isDiscussionTopic = isDiscussionTopicMessage(rawMsg, typingTopicId);
  const isTaskLinkedTopic = Boolean(inboundTaskId || topicName.startsWith("TASK-"));
  const isSlashLike = /^\/\S+/.test((normalized.text || "").trim());
  const inboundMetadata = parseInboundMetadata(rawMsg);
  const mentionTargetedDiscussion = isDiscussionTopic && mentionMatch.matchesAgent;

  const hasMeaningfulText = isMeaningfulUserText(normalized.text);
  const allowVisualOnlyDiscussionMessage = isDiscussionTopic && originalMediaUrls.length > 0;
  if (!hasMeaningfulText && !allowVisualOnlyDiscussionMessage) {
    // Ignore empty/status payloads to avoid creating empty task requests.
    // Exception: discussion image/video-only messages must still enter topic memory.
    return { routed: false, reason: "empty_message" };
  }

  // For discussion topics, keep local topic memory complete even when inference
  // is not triggered. Download image media and index local paths/urls.
  let indexedTopicMedia: { mediaPaths: string[]; mediaTypes: string[] } = { mediaPaths: [], mediaTypes: [] };
  if (isDiscussionTopic && typingTopicId && (normalized.text.trim() || originalMediaUrls.length > 0)) {
    await hydrateDiscussionTopicMemoryIfMissing({
      accountId: params.accountId,
      account: params.account,
      topicId: typingTopicId,
      topicName: normalized.topicName ?? topicName,
      limit: 60,
      log: params.log,
    });

    if (originalMediaUrls.length > 0) {
      indexedTopicMedia = await materializeInboundMediaForContext({
        mediaUrls: originalMediaUrls,
        mediaTypes: originalMediaTypes,
        account: params.account,
        accountId: params.accountId,
        preferThumbnail: true,
        log: params.log,
      });
    }

    await appendDiscussionTopicMemory({
      topicId: typingTopicId,
      topicName: normalized.topicName ?? topicName,
      msg: {
        id: normalized.messageId,
        senderId: normalized.senderId,
        senderDisplayName: normalized.senderName ?? toOptionalString(rawMsg.sender_display_name),
        senderType: String(rawMsg.sender_type ?? "unknown"),
        content: normalized.text,
        createdAt: normalized.timestamp,
        replyTo: toOptionalString(rawMsg.reply_to),
        mediaPaths: indexedTopicMedia.mediaPaths,
        mediaUrls: toThumbnailVariantUrls(originalMediaUrls),
      },
      log: params.log,
    });
  }

  if (slashCompatEnabled) {
    if (isDiscussionTopic && !isTaskLinkedTopic && isSlashLike) {
      const targetAgentId = toOptionalString(inboundMetadata?.command_target_agent_id)
        ?? toOptionalString(inboundMetadata?.commandTargetAgentId);

      // For non-task discuss slash commands: execute only on explicitly targeted agent.
      if (!targetAgentId || !matchesAgentIdentity(targetAgentId, params.account.agentId, params.account.name)) {
        return { routed: false, reason: "agent_no_mention" };
      }
    }

    const wttCommandText = normalizeSlashForWttCommandRouter(normalized.text, params.account);
    const commandResult = await processWTTCommandText({
      text: wttCommandText,
      accountId: params.accountId,
      cfg: params.cfg,
      channelRuntime: runtime,
    });

    if (commandResult.handled) {
      const responseText = (commandResult.response ?? "").trim();
      if (responseText) {
        const payload = { text: responseText };
        if (params.deliver) {
          await params.deliver({
            to: normalized.to,
            payload,
          });
        } else {
          await deliverReplyPayload({
            to: normalized.to,
            payload,
            accountId: params.accountId,
            cfg: params.cfg,
          });
        }
      }

      params.log?.("info", `[${params.accountId}] command_router handled command=${commandResult.command ?? "unknown"}`);
      return { routed: true };
    }
  }

  const standaloneSlash = isStandaloneSlashCommandText(normalized.text);
  const bypassInferenceGate = slashCompatEnabled && slashBypassMentionGate && standaloneSlash;
  let inferDecision: { trigger: boolean; reason?: string } | undefined;

  // Inference gating: skip messages that shouldn't trigger reasoning
  if (!bypassInferenceGate) {
    inferDecision = shouldTriggerInference(rawMsg, params.account.agentId, params.account.name);
    params.log?.("info", `[${params.accountId}] inference_gate topic_type=${String(rawMsg.topic_type)} task_id=${String(rawMsg.task_id ?? "")} trigger=${inferDecision.trigger} reason=${inferDecision.reason ?? "ok"} content_preview=${String(rawMsg.content ?? "").slice(0, 60)} agentName=${params.account.name}`);
    if (!inferDecision.trigger) {
      return { routed: false, reason: inferDecision.reason as InboundRoutingResult["reason"] };
    }
  } else {
    params.log?.("info", `[${params.accountId}] inference_gate bypassed reason=slash_command topic_type=${String(rawMsg.topic_type)}`);
  }

  // Telegram-style media handling: download inbound media first, then pass
  // local file paths into MediaPath/MediaPaths for stable vision pipeline input.
  // Reuse files already downloaded for topic-memory indexing when available.
  const downloadedInboundMedia = indexedTopicMedia.mediaPaths.length > 0
    ? indexedTopicMedia
    : await materializeInboundMediaForContext({
        mediaUrls: normalized.mediaUrls,
        mediaTypes: normalized.mediaTypes,
        account: params.account,
        accountId: params.accountId,
        log: params.log,
      });

  const contextMediaPaths = downloadedInboundMedia.mediaPaths.length > 0
    ? downloadedInboundMedia.mediaPaths
    : normalized.mediaUrls;
  const contextMediaTypes = downloadedInboundMedia.mediaTypes.length > 0
    ? downloadedInboundMedia.mediaTypes
    : normalized.mediaTypes;

  const route = runtime.routing.resolveAgentRoute({
    cfg: params.cfg,
    channel: CHANNEL_ID,
    accountId: params.accountId,
    peer: {
      kind: normalized.chatType,
      id: normalized.routePeerId,
    },
  });

  const storePath = runtime.session.resolveStorePath(params.cfg.session?.store, {
    agentId: route.agentId,
  });

  const previousTimestamp = runtime.session.readSessionUpdatedAt({
    storePath,
    sessionKey: route.sessionKey,
  });

  const envelopeOptions = runtime.reply.resolveEnvelopeFormatOptions(params.cfg);
  const fromLabel = normalized.chatType === "direct"
    ? normalized.senderName ?? normalized.senderId
    : `${normalized.senderName ?? normalized.senderId} @ ${normalized.topicName ?? (normalized.topicId || "topic")}`;

  const body = runtime.reply.formatAgentEnvelope({
    channel: "WTT",
    from: fromLabel,
    timestamp: normalized.timestamp,
    previousTimestamp,
    envelope: envelopeOptions,
    body: normalized.text,
  });

  const taskTitleCandidate =
    toOptionalString(rawMsg.task_title)
    ?? toOptionalString(rawMsg.taskTitle)
    ?? toOptionalString(rawMsg.title)
    ?? (normalized.topicName && !normalized.topicName.startsWith("TASK-") ? normalized.topicName : undefined);

  const mentionDirective = (isDiscussionTopic && mentionTargetedDiscussion)
    ? "注意：这是讨论话题中明确 @ 你的消息，必须直接回应用户问题，禁止输出 NO_REPLY。\n\n"
    : "";

  const replyToId = toOptionalString(rawMsg.reply_to);
  let discussionContextBlock = "";
  if (isDiscussionTopic && normalized.topicId && (mentionTargetedDiscussion || Boolean(replyToId))) {
    const contextWindow = toPositiveInt(
      params.account.config.discussionContextWindow,
      DEFAULT_DISCUSSION_CONTEXT_WINDOW,
    );
    const contextMaxChars = toPositiveInt(
      params.account.config.discussionContextMaxChars,
      DEFAULT_DISCUSSION_CONTEXT_MAX_CHARS,
    );

    // Local-first: read from local memory file (kept up-to-date by incremental append).
    // Only fall back to HTTP if local file is empty (cold start / first encounter).
    let discussionMessages = await readLocalTopicMemory({
      topicId: normalized.topicId,
      log: params.log,
    });

    if (discussionMessages.length === 0) {
      // Cold start: HTTP fetch to bootstrap the local memory file
      params.log?.("info", `[wtt] topic memory cold start, fetching via HTTP topic=${normalized.topicId}`);
      const contextFetchLimit = toPositiveInt(
        params.account.config.discussionContextFetchLimit,
        DEFAULT_DISCUSSION_CONTEXT_FETCH_LIMIT,
      );
      discussionMessages = await fetchDiscussionTopicMessages({
        account: params.account,
        topicId: normalized.topicId,
        limit: contextFetchLimit,
        log: params.log,
      });
      if (discussionMessages.length > 0) {
        await persistDiscussionTopicMemory({
          topicId: normalized.topicId,
          topicName: normalized.topicName,
          messages: discussionMessages,
          log: params.log,
        });
      }
    }

    if (discussionMessages.length > 0) {
      discussionContextBlock = buildDiscussionContextBlock({
        messages: discussionMessages,
        currentMessageId: normalized.messageId,
        windowSize: contextWindow,
        maxChars: contextMaxChars,
        replyTo: replyToId,
      });

      const memDir = resolveTopicMemoryDir();
      const memFile = `topic_id_${normalized.topicId}.md`;
      discussionContextBlock += `\n\n[TOPIC_MEMORY_FILE] ${memDir}/${memFile}\n如需查看完整讨论历史，请读取上述文件。`;
    }
  }

  const bodyCore = inboundTaskId && taskTitleCandidate
    ? `任务标题: ${taskTitleCandidate}\n\n用户消息: ${normalized.text}`
    : normalized.text;

  // Inject KB context for research tasks (async, best-effort)
  let kbContextBlock = "";
  if (inboundTaskId && params.account.cloudUrl) {
    try {
      const apiBase = params.account.cloudUrl.replace(/\/$/, "");
      // Sync KB index on each inference (lightweight — just TOC)
      await syncKBIndex(inboundTaskId, apiBase);
      kbContextBlock = await buildKBContextBlock(inboundTaskId, normalized.text);
    } catch (e) {
      params.log?.("warn", `[wtt] KB context injection failed task=${inboundTaskId}`, e);
    }
  }

  // Inject project context for local file tasks (async, best-effort)
  let projectContextBlock = "";
  if (inboundTaskId && params.account.cloudUrl) {
    try {
      const apiBase = params.account.cloudUrl.replace(/\/$/, "");
      const pcResp = await fetch(`${apiBase}/tasks/${inboundTaskId}/project-context`);
      if (pcResp.ok) {
        const pc = (await pcResp.json()) as Record<string, any>;
        if (pc && (pc.file_count as number) > 0) {
          const statsStr = Object.entries((pc.language_stats as Record<string, number>) || {}).slice(0, 6).map(([k, v]) => `${k}: ${v}`).join(", ");
          const keysStr = ((pc.key_files as string[]) || []).slice(0, 8).join(", ");
          projectContextBlock =
            `\n\n[PROJECT_CONTEXT]\n` +
            `Local project: ${(pc.project_root as string) || "unknown"}\n` +
            `Files: ${pc.file_count as number} (${statsStr})\n` +
            `Key files: ${keysStr}\n` +
            `Use wtt_local_read(task_id='${inboundTaskId}', file_path='...') to read files.\n` +
            `Use wtt_local_tree(task_id='${inboundTaskId}') for the full file tree.\n` +
            `Use wtt_local_write(task_id='${inboundTaskId}', file_path='...', content='...') to create/edit files.\n` +
            `[/PROJECT_CONTEXT]\n`;
        }
      }
    } catch (e) {
      params.log?.("warn", `[wtt] Project context injection failed task=${inboundTaskId}`, e);
    }
  }

  const bodyForAgent = `${mentionDirective}${discussionContextBlock ? `${discussionContextBlock}\n\n` : ""}${kbContextBlock}${projectContextBlock}${bodyCore}`;

  const ctxPayload = runtime.reply.finalizeInboundContext({
    // Keep Body plain so downstream task/title extraction uses user text directly.
    Body: normalized.text,
    BodyForAgent: bodyForAgent,
    RawBody: normalized.text,
    CommandBody: normalized.text,
    EnvelopeBody: body,
    From: normalized.from,
    To: normalized.to,
    SessionKey: route.sessionKey,
    AccountId: route.accountId,
    ChatType: normalized.chatType,
    ConversationLabel: normalized.conversationLabel,
    SenderName: normalized.senderName,
    SenderId: normalized.senderId,
    GroupSubject: normalized.chatType === "group" ? normalized.topicName ?? normalized.topicId : undefined,
    Provider: CHANNEL_ID,
    Surface: CHANNEL_ID,
    MessageSid: normalized.messageId,
    Timestamp: normalized.timestamp,
    OriginatingChannel: CHANNEL_ID,
    OriginatingTo: normalized.to,
    // Pass media as local paths when available (Telegram parity), fallback to
    // original URLs when download is unavailable.
    ...(contextMediaPaths.length > 0
      ? {
          MediaPath: contextMediaPaths[0],
          MediaPaths: contextMediaPaths,
          MediaUrl: contextMediaPaths[0],
          MediaUrls: contextMediaPaths,
          MediaType: contextMediaTypes[0],
          MediaTypes: contextMediaTypes,
          OriginalMediaUrls: normalized.mediaUrls.length > 0 ? normalized.mediaUrls : undefined,
        }
      : {}),
  });

  const taskExecutorScope = (params.account.config.taskExecutorScope ?? "all").toLowerCase();
  let naturalBridgeTaskStatus = "";
  let naturalBridgeEnabled = false;
  let naturalBridgeDoingAtMs: number | null = null;

  // Natural bridge should work for normal (non-pipeline) tasks regardless of executor scope.
  if (inboundTaskId && params.account.token) {
    try {
      const detailResp = await fetch(`${params.account.cloudUrl.replace(/\/$/, "")}/tasks/${encodeURIComponent(inboundTaskId)}`, {
        method: "GET",
        headers: {
          Accept: "application/json",
          Authorization: `Bearer ${params.account.token}`,
          "X-Agent-Token": params.account.token,
        },
      });

      if (detailResp.ok) {
        const detailPayload = await detailResp.json() as Record<string, unknown>;
        const liveTaskType = String(detailPayload.task_type ?? detailPayload.taskType ?? "").trim().toLowerCase();
        const liveStatus = String(detailPayload.status ?? "").trim().toLowerCase();

        if (liveTaskType && liveTaskType !== "pipeline") {
          naturalBridgeEnabled = true;
          naturalBridgeTaskStatus = ["todo", "doing", "review", "done", "blocked"].includes(liveStatus)
            ? (liveStatus as typeof naturalBridgeTaskStatus)
            : "";

          // Delay todo->doing transition until we confirm meaningful output was delivered.
        }
      }
    } catch (err) {
      params.log?.("warn", `[${params.accountId}] natural task status bridge pre-dispatch failed task=${inboundTaskId}`, err);
    }
  }

  if (naturalBridgeEnabled && inboundTaskId && naturalBridgeTaskStatus === "todo" && isMeaningfulUserText(normalized.text)) {
    const movedDoing = await patchTaskStatus(inboundTaskId, "doing");
    if (movedDoing) {
      naturalBridgeTaskStatus = "doing";
      naturalBridgeDoingAtMs = Date.now();
    }
  }

  await runtime.session.recordInboundSession({
    storePath,
    sessionKey: route.sessionKey,
    ctx: ctxPayload,
    updateLastRoute: {
      sessionKey: route.sessionKey,
      channel: CHANNEL_ID,
      to: normalized.to,
      accountId: route.accountId,
    },
    onRecordError: (err) => {
      params.log?.("warn", `[${params.accountId}] Failed to record inbound session`, err);
    },
  });

  let dispatchProducedOutput = false;

  await emitTypingSignal("start");
  try {
    await runtime.reply.dispatchReplyWithBufferedBlockDispatcher({
      ctx: ctxPayload,
      cfg: params.cfg,
      dispatcherOptions: {
        deliver: async (payload) => {
          const isReasoning = Boolean(payload?.isReasoning);
          const text = typeof payload?.text === "string" ? payload.text.trim() : "";
          const mediaUrl = typeof payload?.mediaUrl === "string" ? payload.mediaUrl.trim() : "";
          const mediaUrls = Array.isArray(payload?.mediaUrls)
            ? payload.mediaUrls.filter((item): item is string => typeof item === "string" && item.trim().length > 0)
            : [];

          if (!isReasoning && (text.length > 0 || mediaUrl.length > 0 || mediaUrls.length > 0)) {
            dispatchProducedOutput = true;
          }

          if (params.deliver) {
            await params.deliver({
              to: normalized.to,
              payload: {
                ...payload,
                replyToMessageId: normalized.messageId,
              },
            });
            return;
          }

          await deliverReplyPayload({
            to: normalized.to,
            payload,
            replyTo: normalized.messageId,
            accountId: params.accountId,
            cfg: params.cfg,
          });
        },
        onError: (err, info) => {
          params.log?.(
            "error",
            `[${params.accountId}] WTT inbound dispatch failed (${String(info?.kind ?? "unknown")})`,
            err,
          );
        },
      },
    });
  } finally {
    await emitTypingSignal("stop");
  }

  const shouldForceMentionAck = isDiscussionTopic
    && Boolean(inferDecision?.trigger)
    && (mentionTargetedDiscussion || inferDecision?.reason === "discussion_runner_match");

  if (!dispatchProducedOutput && shouldForceMentionAck) {
    params.log?.("warn", `[${params.accountId}] discussion mention produced no visible output (model empty/NO_REPLY)`);
  }

  if (naturalBridgeEnabled && inboundTaskId) {
    const terminal = new Set(["review", "done", "cancelled", "blocked"]);
    if (!terminal.has(naturalBridgeTaskStatus)) {
      if (!dispatchProducedOutput) {
        params.log?.("info", `[${params.accountId}] natural task status bridge skipped (no output) task=${inboundTaskId}`);
      } else {
        if (naturalBridgeTaskStatus === "doing") {
          if (typeof naturalBridgeDoingAtMs === "number") {
            const elapsedMs = Date.now() - naturalBridgeDoingAtMs;
            const waitMs = Math.max(0, DEFAULT_NATURAL_BRIDGE_MIN_DOING_MS - elapsedMs);
            if (waitMs > 0) {
              await new Promise((resolve) => setTimeout(resolve, waitMs));
            }
          }

          const movedReview = await patchTaskStatus(inboundTaskId, "review");
          if (!movedReview) {
            params.log?.("warn", `[${params.accountId}] natural task status bridge post-dispatch failed task=${inboundTaskId}`);
          }
        }
      }
    }
  }

  return { routed: true };
}

type RecoveryTaskCandidate = {
  id: string;
  status: string;
  runnerAgentId?: string;
  ownerAgentId?: string;
  updatedAt?: string;
};

function parseRecoveryTaskCandidates(raw: unknown): RecoveryTaskCandidate[] {
  const payload = asRecord(raw);
  const dataCandidate = asRecord(payload?.data);

  const source = Array.isArray(raw)
    ? raw
    : Array.isArray(payload?.tasks)
      ? payload.tasks
      : Array.isArray(payload?.items)
        ? payload.items
        : Array.isArray(dataCandidate?.tasks)
          ? dataCandidate.tasks
          : Array.isArray(dataCandidate?.items)
            ? dataCandidate.items
            : [];

  const parsed: RecoveryTaskCandidate[] = [];
  for (const item of source) {
    const record = asRecord(item);
    if (!record) continue;

    const id = toOptionalString(record.id);
    const status = toOptionalString(record.status);
    if (!id || !status) continue;

    parsed.push({
      id,
      status: status.toLowerCase(),
      runnerAgentId: toOptionalString(record.runner_agent_id),
      ownerAgentId: toOptionalString(record.owner_agent_id),
      updatedAt: toOptionalString(record.updated_at) ?? toOptionalString(record.created_at),
    });
  }

  return parsed;
}

function parseIsoMs(input?: string): number | undefined {
  if (!input) return undefined;
  const t = Date.parse(input);
  return Number.isFinite(t) ? t : undefined;
}

async function startGatewayAccount(ctx: GatewayStartContext): Promise<void> {
  const log = (level: "debug" | "info" | "warn" | "error", msg: string, data?: unknown): void => {
    if (level === "debug") ctx.log?.debug?.(msg);
    else if (level === "info") ctx.log?.info?.(msg);
    else if (level === "warn") ctx.log?.warn?.(msg);
    else ctx.log?.error?.(data ? `${msg} ${String(data)}` : msg);
  };

  let activeClient: WTTCloudClient | undefined;
  let pollTimer: ReturnType<typeof setInterval> | undefined;
  let recoveryTimer: ReturnType<typeof setInterval> | undefined;
  let pollInFlight = false;
  let recoveryInFlight = false;

  const pollIntervalMs = toPositiveInt(ctx.account.config.inboundPollIntervalMs, DEFAULT_INBOUND_POLL_INTERVAL_MS);
  const pollLimit = toPositiveInt(ctx.account.config.inboundPollLimit, DEFAULT_INBOUND_POLL_LIMIT);
  const recoveryIntervalMs = DEFAULT_TASK_RECOVERY_INTERVAL_MS;
  const recoveryLookbackMs = DEFAULT_TASK_RECOVERY_LOOKBACK_MS;
  const recoverySeenAt = new Map<string, number>();
  const todoRecheckTimers = new Map<string, ReturnType<typeof setTimeout>>();

  const inboundRelay = createInboundMessageRelay({
    cfg: ctx.cfg,
    accountId: ctx.accountId,
    account: ctx.account,
    getLatestAccount: () => {
      const client = getClient(ctx.accountId);
      return client ? client.getAccount() : ctx.account;
    },
    channelRuntime: ctx.channelRuntime,
    decryptContent: async (content: string) => {
      const runtimeClient = getClient(ctx.accountId);
      if (!runtimeClient) return content;
      return runtimeClient.decryptMessage(content);
    },
    typingSignal: async ({ topicId, state, ttlMs }) => {
      const runtimeClient = getClient(ctx.accountId);
      if (!runtimeClient || !runtimeClient.connected) return;
      await runtimeClient.typing(topicId, state, ttlMs ?? 6000);
    },
    log,
    dedupWindowMs: ctx.account.config.inboundDedupWindowMs,
    dedupMaxEntries: ctx.account.config.inboundDedupMaxEntries,
  });

  const scheduleTodoRecheck = (taskId: string, delayMs = 5000): void => {
    if (todoRecheckTimers.has(taskId)) return;

    const timer = setTimeout(async () => {
      todoRecheckTimers.delete(taskId);
      try {
        if (ctx.abortSignal.aborted || !ctx.channelRuntime) return;

        const accountContext = resolveCommandAccountContext(ctx.accountId, ctx.cfg);
        const account = normalizeAccountContext(ctx.accountId, accountContext);
        if (!account.hasToken || !account.agentId) return;

        const detailResp = await fetch(`${account.cloudUrl.replace(/\/$/, "")}/tasks/${encodeURIComponent(taskId)}`, {
          method: "GET",
          headers: {
            Accept: "application/json",
            Authorization: `Bearer ${account.token}`,
            "X-Agent-Token": account.token,
          },
        });
        if (!detailResp.ok) return;

        const detailPayload = await detailResp.json() as Record<string, unknown>;
        const liveStatus = String(detailPayload.status ?? "").trim().toLowerCase();
        const TERMINAL_STATUSES = new Set(["review", "done", "cancelled", "blocked"]);
        if (TERMINAL_STATUSES.has(liveStatus)) return;

        const taskExecutorScope = (ctx.account.config.taskExecutorScope ?? "all").toLowerCase();
        if (taskExecutorScope === "pipeline_only") {
          const liveTaskType = String(detailPayload.task_type ?? detailPayload.taskType ?? "").trim().toLowerCase();
          const liveExecMode = String(detailPayload.exec_mode ?? detailPayload.execMode ?? "").trim().toLowerCase();
          const liveTaskMode = String(detailPayload.task_mode ?? detailPayload.taskMode ?? "").trim().toLowerCase();
          const livePipelineId = detailPayload.pipeline_id ?? detailPayload.pipelineId ?? "";

          const isPipelineTask = [liveTaskType, liveExecMode, liveTaskMode].includes("pipeline") || hasMeaningfulPipelineId(livePipelineId);
          if (!isPipelineTask) {
            log("info", `[${ctx.accountId}] task_status todo recheck skipped non-pipeline task=${taskId}`);
            return;
          }
        }

        const runtimeHooks = createTaskInferenceRuntimeHooks({
          cfg: ctx.cfg,
          accountId: ctx.accountId,
          account: accountContext,
          channelRuntime: ctx.channelRuntime,
        });

        const runResult = await executeTaskRunById({
          taskId,
          ctx: {
            accountId: ctx.accountId,
            account,
            client: activeClient,
            clientConnected: Boolean(activeClient?.connected),
            fetchImpl: fetch,
            runtimeHooks,
          },
          account,
          note: "triggered by task_status todo recheck",
          heartbeatSeconds: 60,
          publishHeartbeatToStream: true,
        });

        const enqueue = runResult.enqueueResult;
        const detail = enqueue.deduplicated
          ? `idempotency=${enqueue.idempotency.decision} duplicate_state=${enqueue.idempotency.duplicateState ?? "-"}`
          : `idempotency=${enqueue.idempotency.decision} final_status=${enqueue.finalStatus} transition=${enqueue.transitionApplied}`;

        log("info", `[${ctx.accountId}] task_status todo recheck dispatched task=${taskId} ${detail}`);
      } catch (err) {
        log("warn", `[${ctx.accountId}] task_status todo recheck failed task=${taskId}`, err);
      }
    }, delayMs);

    todoRecheckTimers.set(taskId, timer);
  };

  const taskStatusHandler = createTaskStatusEventHandler({
    runTask: async ({ taskId, status, event }) => {
      if (!ctx.channelRuntime) {
        throw new Error("channel_runtime_unavailable");
      }

      const accountContext = resolveCommandAccountContext(ctx.accountId, ctx.cfg);
      const account = normalizeAccountContext(ctx.accountId, accountContext);
      if (!account.hasToken) {
        throw new Error("missing_account_token");
      }

      const taskExecutorScope = (ctx.account.config.taskExecutorScope ?? "all").toLowerCase();
      let liveTaskType = "";
      let liveExecMode = "";
      let liveTaskMode = "";
      let livePipelineId = "";

      // Guard: verify live task status before dispatching run from WS task_status events.
      // - todo: actionable if still todo/doing; terminal statuses are skipped.
      // - doing: only actionable when live status is still doing (avoid stale doing replay after review/done).
      if (status === "todo" || status === "doing") {
        const TERMINAL_STATUSES = new Set(["review", "done", "cancelled", "blocked"]);
        try {
          const detailResp = await fetch(`${account.cloudUrl.replace(/\/$/, "")}/tasks/${encodeURIComponent(taskId)}`, {
            method: "GET",
            headers: {
              Accept: "application/json",
              Authorization: `Bearer ${account.token}`,
              "X-Agent-Token": account.token,
            },
          });

          if (!detailResp.ok) {
            if (status === "todo") {
              scheduleTodoRecheck(taskId);
              return {
                deduplicated: true,
                detail: `skip_todo_detail_fetch_failed:http_${detailResp.status}`,
              };
            }

            return {
              deduplicated: true,
              detail: `skip_doing_detail_fetch_failed:http_${detailResp.status}`,
            };
          }

          const detailPayload = await detailResp.json() as Record<string, unknown>;
          liveTaskType = String(detailPayload.task_type ?? detailPayload.taskType ?? "").trim().toLowerCase();
          liveExecMode = String(detailPayload.exec_mode ?? detailPayload.execMode ?? "").trim().toLowerCase();
          liveTaskMode = String(detailPayload.task_mode ?? detailPayload.taskMode ?? "").trim().toLowerCase();
          livePipelineId = String(detailPayload.pipeline_id ?? detailPayload.pipelineId ?? "").trim();
          const liveStatus = String(detailPayload.status ?? "").trim().toLowerCase();
          if (TERMINAL_STATUSES.has(liveStatus)) {
            // Pipeline task events can briefly replay stale blocked before converging to todo/doing.
            // For TODO events, schedule a delayed recheck to avoid one-shot deadlocks.
            if (status === "todo") {
              scheduleTodoRecheck(taskId, 6000);
              return {
                deduplicated: true,
                detail: `skip_${status}_live_status_terminal:${liveStatus}_recheck_scheduled`,
              };
            }

            return {
              deduplicated: true,
              detail: `skip_${status}_live_status_terminal:${liveStatus}`,
            };
          }

          if (status === "doing" && liveStatus !== "doing") {
            return {
              deduplicated: true,
              detail: `skip_doing_live_status_mismatch:${liveStatus || "unknown"}`,
            };
          }
        } catch (err) {
          // On fetch error, still proceed — executor has its own idempotency guards.
          const msg = err instanceof Error ? err.message : String(err);
          log("warn", `[${ctx.accountId}] task_status ${status} detail fetch error task=${taskId}: ${msg}`);
        }
      }

      if (taskExecutorScope === "pipeline_only") {
        const eventTaskType = String(event.task_type ?? "").trim().toLowerCase();
        const eventExecMode = String(event.exec_mode ?? "").trim().toLowerCase();
        const pipelineHints = [liveTaskType, liveExecMode, liveTaskMode, eventTaskType, eventExecMode];
        const isPipelineTask = pipelineHints.includes("pipeline") || hasMeaningfulPipelineId(livePipelineId);

        if (!isPipelineTask) {
          const hint = (pipelineHints.find(Boolean) || "unknown");
          return {
            deduplicated: true,
            detail: `skip_non_pipeline_task_type:${hint}`,
          };
        }
      }

      const runtimeHooks = createTaskInferenceRuntimeHooks({
        cfg: ctx.cfg,
        accountId: ctx.accountId,
        account: accountContext,
        channelRuntime: ctx.channelRuntime,
        typingSignal: async ({ topicId, state, ttlMs }) => {
          if (!activeClient?.connected) return;
          await activeClient.typing(topicId, state, ttlMs ?? 6000);
        },
      });

      if (!runtimeHooks?.dispatchTaskInference) {
        throw new Error("runtime_hook_unavailable");
      }

      if (!activeClient?.connected) {
        throw new Error("wtt_client_disconnected");
      }

      const runResult = await executeTaskRunById({
        taskId,
        ctx: {
          accountId: ctx.accountId,
          account: accountContext,
          clientConnected: activeClient.connected,
          client: activeClient,
          runtimeHooks,
        },
        account,
        note: `triggered by task_status (${status})`,
        heartbeatSeconds: 60,
        publishHeartbeatToStream: true,
      });

      const enqueue = runResult.enqueueResult;
      const detail = enqueue.deduplicated
        ? `idempotency=${enqueue.idempotency.decision} duplicate_state=${enqueue.idempotency.duplicateState ?? "-"}`
        : `idempotency=${enqueue.idempotency.decision} final_status=${enqueue.finalStatus} transition=${enqueue.transitionApplied}`;

      return {
        deduplicated: enqueue.deduplicated,
        detail,
      };
    },
  });

  const runPollCatchup = async (): Promise<void> => {
    if (ctx.abortSignal.aborted || pollInFlight) return;
    if (!activeClient?.connected) return;

    pollInFlight = true;
    try {
      const raw = await activeClient.poll(pollLimit);
      await inboundRelay.handlePollResult(raw);
    } catch (err) {
      log("warn", `[${ctx.accountId}] inbound poll catch-up failed`, err);
    } finally {
      pollInFlight = false;
    }
  };

  const runTaskRecoverySweep = async (): Promise<void> => {
    if (ctx.abortSignal.aborted || recoveryInFlight) return;
    if (!activeClient?.connected) return;
    if (!ctx.channelRuntime) return;

    const accountContext = resolveCommandAccountContext(ctx.accountId, ctx.cfg);
    const account = normalizeAccountContext(ctx.accountId, accountContext);
    if (!account.hasToken || !account.agentId) return;

    recoveryInFlight = true;
    try {
      const endpoint = `${account.cloudUrl.replace(/\/$/, "")}/tasks`;
      const response = await fetch(endpoint, {
        method: "GET",
        headers: {
          Accept: "application/json",
          Authorization: `Bearer ${account.token}`,
          "X-Agent-Token": account.token,
        },
      });

      if (!response.ok) {
        throw new Error(`tasks list failed: HTTP ${response.status}`);
      }

      const payload = await response.json();
      const tasks = parseRecoveryTaskCandidates(payload);
      const nowMs = Date.now();
      const cutoffMs = nowMs - recoveryLookbackMs;

      for (const [key, seenAt] of recoverySeenAt) {
        if (seenAt < cutoffMs) recoverySeenAt.delete(key);
      }

      let scanned = 0;
      let triggered = 0;
      for (const task of tasks) {
        if (task.status !== "doing") continue;
        if (task.runnerAgentId !== account.agentId) continue;

        const updatedAtMs = parseIsoMs(task.updatedAt);
        if (typeof updatedAtMs === "number" && updatedAtMs < cutoffMs) continue;

        scanned += 1;
        const dedupKey = `${task.id}:${task.status}:${task.updatedAt ?? ""}`;
        if (recoverySeenAt.has(dedupKey)) continue;
        recoverySeenAt.set(dedupKey, nowMs);

        triggered += 1;
        const consume = await taskStatusHandler.handle({
          type: "task_status",
          task_id: task.id,
          status: "doing",
        });
        const dedupSource = consume.dedupSource ? ` dedup_source=${consume.dedupSource}` : "";
        const dispatchDetail = consume.dispatch?.detail ? ` detail=${consume.dispatch.detail}` : "";
        log(
          "info",
          `[${ctx.accountId}] recovery task_status consume decision=${consume.decision} task=${consume.taskId || task.id} status=doing reason=${consume.reason}${dedupSource}${dispatchDetail}`,
        );
      }

      if (scanned > 0 || triggered > 0) {
        log("info", `[${ctx.accountId}] recovery sweep scanned=${scanned} triggered=${triggered}`);
      }
    } catch (err) {
      log("warn", `[${ctx.accountId}] task recovery sweep failed`, err);
    } finally {
      recoveryInFlight = false;
    }
  };

  try {
    activeClient = await startWsAccount(ctx.accountId, ctx.account, {
      log,
      onMessage: (_accountId, msg) => {
        void inboundRelay.handlePush(msg).catch((err) => {
          log("error", `[${ctx.accountId}] inbound routing error`, err);
        });
      },
      onTaskStatus: (_accountId, status) => {
        void taskStatusHandler.handle(status)
          .then((consume) => {
            const dedupSource = consume.dedupSource ? ` dedup_source=${consume.dedupSource}` : "";
            const dispatchDetail = consume.dispatch?.detail ? ` detail=${consume.dispatch.detail}` : "";
            log(
              "info",
              `[${ctx.accountId}] task_status consume decision=${consume.decision} task=${consume.taskId || "-"} status=${consume.status} reason=${consume.reason}${dedupSource}${dispatchDetail}`,
            );
          })
          .catch((err) => {
            log("error", `[${ctx.accountId}] task_status handler failed`, err);
          });
      },
    });

    if (pollIntervalMs > 0) {
      log("info", `[${ctx.accountId}] inbound poll catch-up enabled interval=${pollIntervalMs}ms limit=${pollLimit}`);
      void runPollCatchup();
      pollTimer = setInterval(() => {
        void runPollCatchup();
      }, pollIntervalMs);
    }

    if (recoveryIntervalMs > 0) {
      log(
        "info",
        `[${ctx.accountId}] task recovery sweep enabled interval=${recoveryIntervalMs}ms lookback_ms=${recoveryLookbackMs}`,
      );
      void runTaskRecoverySweep();
      recoveryTimer = setInterval(() => {
        void runTaskRecoverySweep();
      }, recoveryIntervalMs);
    }

    await waitForAbort(ctx.abortSignal);
  } finally {
    if (pollTimer) {
      clearInterval(pollTimer);
      pollTimer = undefined;
    }

    if (recoveryTimer) {
      clearInterval(recoveryTimer);
      recoveryTimer = undefined;
    }

    for (const timer of todoRecheckTimers.values()) {
      clearTimeout(timer);
    }
    todoRecheckTimers.clear();

    log(
      "info",
      `[${ctx.accountId}] inbound summary push_received=${inboundRelay.stats.pushReceivedCount} poll_fetched=${inboundRelay.stats.pollFetchedCount} routed=${inboundRelay.stats.routedCount} dedup_dropped=${inboundRelay.stats.dedupDroppedCount}`,
    );

    await stopAccount(ctx.accountId);
  }
}

const A2UI_MESSAGE_TOOL_HINTS = [
  "WTT supports action fenced code blocks for interactive UI.",
  "Use ```action JSON blocks with kinds: buttons/confirm/select/input.",
  "Prefer compact button choices over long numbered lists.",
].join("\n");

export const wttPlugin = {
  id: "wtt",
  meta: {
    id: "wtt",
    label: "WTT",
    selectionLabel: "WTT (WebSocket)",
    docsPath: "/channels/wtt",
    docsLabel: "wtt",
    blurb: "WTT real-time topic + p2p channel.",
    aliases: ["want-to-talk"],
    order: 95,
  },
  capabilities: {
    chatTypes: ["direct", "group", "thread"],
    threads: true,
    media: true,
  },
  reload: {
    configPrefixes: ["channels.wtt"],
  },
  config: {
    listAccountIds,
    resolveAccount,
    defaultAccountId: () => DEFAULT_ACCOUNT_ID,
    isConfigured: (account: ResolvedWTTAccount) => account.configured,
    describeAccount: (account: ResolvedWTTAccount) => ({
      accountId: account.accountId,
      name: account.name,
      enabled: account.enabled,
      configured: account.configured,
      cloudUrl: account.cloudUrl,
    }),
  },
  gateway: {
    startAccount: startGatewayAccount,
    stopAccount: async (ctx: { accountId: string }) => {
      await stopAccount(ctx.accountId);
    },
  },
  outbound: {
    deliveryMode: "direct",
    textChunkLimit: 4000,
    resolveTarget: ({ to }: { to: string }) => to,
    sendText,
    sendMedia,
  },
  agentPrompt: {
    messageToolHints: () => [A2UI_MESSAGE_TOOL_HINTS],
  },
  hooks: {
    register: registerHook,
    runBefore: (ctx: Parameters<HookFn>[0]) => runHooks("before", ctx),
    runAfter: (ctx: Parameters<HookFn>[0]) => runHooks("after", ctx),
  },
  getClient,
};
