// wip-bridge/core.ts: Pure logic. Zero framework deps.
// Handles messaging, memory search, and workspace access for OpenClaw agents.

import { execSync, exec } from "node:child_process";
import { readdirSync, readFileSync, writeFileSync, existsSync, statSync, mkdirSync, renameSync, unlinkSync } from "node:fs";
import { join, relative, resolve } from "node:path";
import { homedir } from "node:os";
import { promisify } from "node:util";
import { randomUUID } from "node:crypto";

const execAsync = promisify(exec);

// ── Settings ─────────────────────────────────────────────────────────
// All tunable constants in one place. No magic numbers below this block.

const GATEWAY_HOST = "127.0.0.1";
const DEFAULT_GATEWAY_PORT = 18_789;         // openclaw.json gateway.port fallback
const DEFAULT_INBOX_PORT = 18_790;           // env LESA_BRIDGE_INBOX_PORT fallback
const GATEWAY_TIMEOUT_MS = 120_000;          // max wait for gateway chat response (2 min, agent turns can be long)
const OP_CLI_TIMEOUT_MS = 10_000;            // max wait for 1Password CLI
const EMBEDDING_API_URL = "https://api.openai.com/v1/embeddings";
const DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small";
const DEFAULT_EMBEDDING_DIMS = 1_536;
const VECTOR_SEARCH_ROW_LIMIT = 1_000;       // max rows scanned for cosine ranking
const RECENCY_DECAY_RATE = 0.01;             // per-day decay multiplier
const RECENCY_FLOOR = 0.5;                   // minimum recency weight
const FRESHNESS_FRESH_DAYS = 3;
const FRESHNESS_RECENT_DAYS = 7;
const FRESHNESS_AGING_DAYS = 14;
const DEFAULT_SEARCH_LIMIT = 5;              // default results for searchConversations
const WORKSPACE_MAX_DEPTH = 4;               // findMarkdownFiles recursion limit
const WORKSPACE_MAX_EXCERPTS = 5;            // max excerpts per file in search
const WORKSPACE_MAX_RESULTS = 10;            // max files returned from workspace search
const SKILL_EXEC_TIMEOUT_MS = 120_000;       // max wait for skill script execution
const SKILL_EXEC_MAX_BUFFER = 10 * 1024 * 1024; // 10 MB stdout/stderr cap
const MS_PER_DAY = 1_000 * 60 * 60 * 24;

// ── Constants ─────────────────────────────────────────────────────────

const HOME = process.env.HOME || homedir();
export const LDM_ROOT = process.env.LDM_ROOT || join(HOME, ".ldm");

// ── Types ────────────────────────────────────────────────────────────

export interface BridgeConfig {
  openclawDir: string;
  workspaceDir: string;
  dbPath: string;
  inboxPort: number;
  embeddingModel: string;
  embeddingDimensions: number;
}

export interface GatewayConfig {
  token: string;
  port: number;
}

export interface InboxMessage {
  id: string;
  type: string;
  from: string;
  to: string;
  body: string;
  message?: string; // legacy compat: alias for body
  timestamp: string;
  read: boolean;
  // Optional: id of the message this is a reply to. When present on a
  // pushInbox call and `to` is missing or agent-only, the bridge looks up
  // the referenced message and copies its `from` into this message's `to`
  // so replies land at the specific session that sent the original, not
  // broadcast to every session of the agent.
  inReplyTo?: string;
}

export interface ConversationResult {
  text: string;
  role: string;
  sessionKey: string;
  date: string;
  similarity?: number;
  recencyScore?: number;
  freshness?: "fresh" | "recent" | "aging" | "stale";
}

export interface WorkspaceSearchResult {
  path: string;
  excerpts: string[];
  score: number;
}

// ── Config resolution ────────────────────────────────────────────────

export function resolveConfig(overrides?: Partial<BridgeConfig>): BridgeConfig {
  const openclawDir = overrides?.openclawDir || process.env.OPENCLAW_DIR || join(process.env.HOME || "~", ".openclaw");
  return {
    openclawDir,
    workspaceDir: overrides?.workspaceDir || join(openclawDir, "workspace"),
    dbPath: overrides?.dbPath || join(openclawDir, "memory", "context-embeddings.sqlite"),
    inboxPort: overrides?.inboxPort || parseInt(process.env.LESA_BRIDGE_INBOX_PORT || String(DEFAULT_INBOX_PORT), 10),
    embeddingModel: overrides?.embeddingModel || DEFAULT_EMBEDDING_MODEL,
    embeddingDimensions: overrides?.embeddingDimensions || DEFAULT_EMBEDDING_DIMS,
  };
}

/**
 * Multi-config resolver. Checks ~/.ldm/config.json first, falls back to OPENCLAW_DIR.
 * This is the LDM OS native path. resolveConfig() is the legacy OpenClaw path.
 * Both return the same BridgeConfig shape.
 */
export function resolveConfigMulti(overrides?: Partial<BridgeConfig>): BridgeConfig {
  // Check LDM OS config first
  const ldmConfig = join(LDM_ROOT, "config.json");
  if (existsSync(ldmConfig)) {
    try {
      const raw = JSON.parse(readFileSync(ldmConfig, "utf-8"));
      const openclawDir = raw.openclawDir || process.env.OPENCLAW_DIR || join(HOME, ".openclaw");
      return {
        openclawDir,
        workspaceDir: raw.workspaceDir || overrides?.workspaceDir || join(openclawDir, "workspace"),
        dbPath: raw.dbPath || overrides?.dbPath || join(openclawDir, "memory", "context-embeddings.sqlite"),
        inboxPort: raw.inboxPort || overrides?.inboxPort || parseInt(process.env.LESA_BRIDGE_INBOX_PORT || String(DEFAULT_INBOX_PORT), 10),
        embeddingModel: raw.embeddingModel || overrides?.embeddingModel || DEFAULT_EMBEDDING_MODEL,
        embeddingDimensions: raw.embeddingDimensions || overrides?.embeddingDimensions || DEFAULT_EMBEDDING_DIMS,
      };
    } catch {
      // LDM config unreadable, fall through to legacy
    }
  }

  // Fallback to legacy OpenClaw resolution
  return resolveConfig(overrides);
}

// ── API key resolution ───────────────────────────────────────────────

let cachedApiKey: string | null | undefined = undefined;

export function resolveApiKey(openclawDir: string): string | null {
  if (cachedApiKey !== undefined) return cachedApiKey;

  // 1. Environment variable
  if (process.env.OPENAI_API_KEY) {
    cachedApiKey = process.env.OPENAI_API_KEY;
    return cachedApiKey;
  }

  // 2. 1Password via service account token
  const tokenPath = join(openclawDir, "secrets", "op-sa-token");
  if (existsSync(tokenPath)) {
    try {
      const saToken = readFileSync(tokenPath, "utf-8").trim();
      const key = execSync(
        `op read "op://Agent Secrets/OpenAI API/api key" 2>/dev/null`,
        {
          env: { ...process.env, OP_SERVICE_ACCOUNT_TOKEN: saToken },
          timeout: OP_CLI_TIMEOUT_MS,
          encoding: "utf-8",
        }
      ).trim();
      if (key && key.startsWith("sk-")) {
        cachedApiKey = key;
        return cachedApiKey;
      }
    } catch {
      // 1Password not available
    }
  }

  cachedApiKey = null;
  return null;
}

// ── Gateway config ───────────────────────────────────────────────────

let cachedGatewayConfig: GatewayConfig | null = null;

export function resolveGatewayConfig(openclawDir: string): GatewayConfig {
  if (cachedGatewayConfig) return cachedGatewayConfig;

  const configPath = join(openclawDir, "openclaw.json");
  if (!existsSync(configPath)) {
    throw new Error(`OpenClaw config not found: ${configPath}`);
  }

  const config = JSON.parse(readFileSync(configPath, "utf-8"));
  const token = config?.gateway?.auth?.token;
  const port = config?.gateway?.port || DEFAULT_GATEWAY_PORT;

  if (!token) {
    throw new Error("No gateway.auth.token found in openclaw.json");
  }

  cachedGatewayConfig = { token, port };
  return cachedGatewayConfig;
}

// ── Inbox (file-based via ~/.ldm/messages/) ─────────────────────────
//
// Phase 1: Replaces the in-memory queue with JSON files on disk.
// Phase 2: Adds session targeting (agent:session format).
// Phase 4: Cross-agent delivery to any agent via the same directory.
//
// Uses the existing lib/messages.mjs format. Each message is a JSON file
// at ~/.ldm/messages/{uuid}.json. Read means move to _processed/.

const MESSAGES_DIR = join(LDM_ROOT, "messages");
const PROCESSED_DIR = join(MESSAGES_DIR, "_processed");

// Session identity for this bridge process.
// Set via LDM_SESSION_NAME env or defaults to "default".
let _sessionAgentId = "cc-mini";
let _sessionName = process.env.LDM_SESSION_NAME || "default";

export function setSessionIdentity(agentId: string, sessionName: string): void {
  _sessionAgentId = agentId;
  _sessionName = sessionName;
}

export function getSessionIdentity(): { agentId: string; sessionName: string } {
  return { agentId: _sessionAgentId, sessionName: _sessionName };
}

/**
 * Re-read the session name from CC's session metadata file.
 *
 * CC writes the /rename label to ~/.claude/sessions/<pid>.json. The bridge
 * reads this once on boot, but the name can change at any time via /rename
 * or /resume. Calling this before each inbox check ensures the bridge
 * always uses the current label for message targeting.
 *
 * Cheap: one file read per call. No network. No delay.
 */
export function refreshSessionIdentity(): void {
  try {
    const sessionPath = join(
      process.env.HOME || require("node:os").homedir(),
      ".claude",
      "sessions",
      `${process.ppid}.json`
    );
    const data = JSON.parse(readFileSync(sessionPath, "utf-8"));
    if (data.name && typeof data.name === "string" && data.name !== _sessionName) {
      const oldName = _sessionName;
      _sessionName = data.name;
      // Re-register with the new name so other agents can find us
      try {
        registerBridgeSession();
      } catch {}
      if (oldName !== _sessionName) {
        process.stderr.write(`wip-bridge: session name updated: ${oldName} -> ${_sessionName}\n`);
      }
    }
  } catch {
    // File doesn't exist or can't be read. Keep current name.
  }
}

/**
 * Parse a "to" field into agent and session parts.
 * Formats: "cc-mini" (default session), "cc-mini:brainstorm" (named),
 *          "cc-mini:*" (broadcast to all sessions of agent), "*" (all)
 */
function parseTarget(to: string): { agent: string; session: string } {
  if (to === "*") return { agent: "*", session: "*" };
  const colonIdx = to.indexOf(":");
  // Agent-only address (no colon, e.g. "cc-mini") is a broadcast to all
  // sessions of that agent. Previously this defaulted to session "default"
  // which silently dropped messages for any session with a non-default name.
  // See: ai/product/bugs/bridge/2026-04-10--cc-mini--bridge-reply-addressing-mismatch.md
  if (colonIdx === -1) return { agent: to, session: "*" };
  return { agent: to.slice(0, colonIdx), session: to.slice(colonIdx + 1) };
}

/**
 * Check if a message's "to" field matches this session.
 * Matches: exact agent + session, agent broadcast (agent:*),
 *          global broadcast (*), or agent-only address (no session qualifier).
 */
function messageMatchesSession(msgTo: string, agentId: string, sessionName: string): boolean {
  // Global broadcast
  if (msgTo === "*" || msgTo === "all") return true;

  const target = parseTarget(msgTo);

  // Different agent entirely
  if (target.agent !== "*" && target.agent !== agentId) return false;

  // Agent broadcast (agent:*) or agent-only address
  if (target.session === "*") return true;

  // Exact session match
  return target.session === sessionName;
}

/**
 * Look up a message by id in the inbox or processed dir. Returns null if
 * not found. Used by reply-to-sender routing.
 */
export function findMessageById(id: string): InboxMessage | null {
  if (!id) return null;
  for (const dir of [MESSAGES_DIR, PROCESSED_DIR]) {
    const candidate = join(dir, `${id}.json`);
    if (!existsSync(candidate)) continue;
    try {
      const data = JSON.parse(readFileSync(candidate, "utf-8")) as InboxMessage;
      return data;
    } catch {}
  }
  return null;
}

/**
 * Write a message to the file-based inbox.
 * Creates a JSON file at ~/.ldm/messages/{uuid}.json.
 *
 * Reply-to-sender routing (added 2026-04-20):
 *   If `inReplyTo` is set AND `to` is missing or agent-only (no colon),
 *   the bridge looks up the referenced message and copies its `from` into
 *   this message's `to`. This makes replies land at the specific session
 *   that sent the original, rather than broadcasting to every session of
 *   the agent (which is what Apr 10's Option 1 shipped as a safety net).
 *   Callers that explicitly want broadcast can still use
 *   `to: "<agent>:*"` or `to: "*"`.
 */
export function pushInbox(msg: { from: string; message?: string; body?: string; to?: string; type?: string; inReplyTo?: string }): number {
  try {
    mkdirSync(MESSAGES_DIR, { recursive: true });
    const id = randomUUID();

    // Resolve reply target from inReplyTo if applicable.
    let resolvedTo = msg.to;
    const explicitBroadcast = resolvedTo === "*" || resolvedTo === "all" || (resolvedTo && resolvedTo.endsWith(":*"));
    const agentOnly = resolvedTo && !resolvedTo.includes(":") && !explicitBroadcast;
    if (msg.inReplyTo && (!resolvedTo || agentOnly)) {
      const original = findMessageById(msg.inReplyTo);
      if (original && original.from) {
        resolvedTo = original.from;
      }
    }

    const data: InboxMessage = {
      id,
      type: msg.type || "chat",
      from: msg.from || "unknown",
      to: resolvedTo || `${_sessionAgentId}:${_sessionName}`,
      body: msg.body || msg.message || "",
      timestamp: new Date().toISOString(),
      read: false,
      ...(msg.inReplyTo ? { inReplyTo: msg.inReplyTo } : {}),
    };
    writeFileSync(join(MESSAGES_DIR, `${id}.json`), JSON.stringify(data, null, 2) + "\n");

    // Return count of pending messages for this session
    return inboxCount();
  } catch {
    return 0;
  }
}

/**
 * Read and drain all messages for this session from the inbox.
 * Moves processed messages to ~/.ldm/messages/_processed/.
 */
export function drainInbox(): InboxMessage[] {
  // Re-read session name from CC metadata before filtering.
  // Handles /rename and /resume happening after bridge boot.
  refreshSessionIdentity();

  try {
    if (!existsSync(MESSAGES_DIR)) return [];

    const files = readdirSync(MESSAGES_DIR).filter(f => f.endsWith(".json"));
    const messages: InboxMessage[] = [];

    for (const file of files) {
      const filePath = join(MESSAGES_DIR, file);
      try {
        const data = JSON.parse(readFileSync(filePath, "utf-8")) as InboxMessage;

        // Check if this message is addressed to us
        if (!messageMatchesSession(data.to, _sessionAgentId, _sessionName)) continue;

        // Normalize: ensure body is populated (legacy compat)
        if (!data.body && data.message) data.body = data.message;

        messages.push(data);

        // Move to processed
        try {
          mkdirSync(PROCESSED_DIR, { recursive: true });
          renameSync(filePath, join(PROCESSED_DIR, file));
        } catch {
          // If rename fails, try to delete
          try { unlinkSync(filePath); } catch {}
        }
      } catch {
        // Skip malformed files
      }
    }

    // Sort by timestamp (oldest first)
    messages.sort((a, b) => (a.timestamp || "").localeCompare(b.timestamp || ""));
    return messages;
  } catch {
    return [];
  }
}

/**
 * Count pending messages for this session without draining.
 */
export function inboxCount(): number {
  refreshSessionIdentity();
  try {
    if (!existsSync(MESSAGES_DIR)) return 0;

    const files = readdirSync(MESSAGES_DIR).filter(f => f.endsWith(".json"));
    let count = 0;

    for (const file of files) {
      try {
        const data = JSON.parse(readFileSync(join(MESSAGES_DIR, file), "utf-8"));
        if (messageMatchesSession(data.to, _sessionAgentId, _sessionName)) count++;
      } catch {
        // Skip malformed
      }
    }

    return count;
  } catch {
    return 0;
  }
}

/**
 * Get pending message counts broken down by session.
 * Used by GET /status to show per-session counts.
 */
export function inboxCountBySession(): Record<string, number> {
  const counts: Record<string, number> = {};
  try {
    if (!existsSync(MESSAGES_DIR)) return counts;

    const files = readdirSync(MESSAGES_DIR).filter(f => f.endsWith(".json"));
    for (const file of files) {
      try {
        const data = JSON.parse(readFileSync(join(MESSAGES_DIR, file), "utf-8"));
        const to = data.to || "unknown";
        counts[to] = (counts[to] || 0) + 1;
      } catch {}
    }
  } catch {}
  return counts;
}

/**
 * Send a message to another agent or session via the file-based inbox.
 * Phase 4: Cross-agent messaging. Works for any agent, any session.
 * This is the file-based path. For OpenClaw agents, use sendMessage() (gateway).
 */
export function sendLdmMessage(opts: {
  from?: string;
  to?: string;
  body: string;
  type?: string;
  // Reply-to-sender routing (added 2026-04-20). If provided and `to` is
  // missing or agent-only (no session suffix), `to` is auto-resolved from
  // the referenced message's `from`, so the reply lands at exactly the
  // session that sent the original. See
  // ai/product/bugs/bridge/2026-04-20--cc-mini--bridge-reply-to-sender-routing.md
  inReplyTo?: string;
}): string | null {
  try {
    mkdirSync(MESSAGES_DIR, { recursive: true });
    const id = randomUUID();

    // Resolve reply target from inReplyTo when applicable.
    let resolvedTo = opts.to;
    const explicitBroadcast = resolvedTo === "*" || resolvedTo === "all" || (resolvedTo && resolvedTo.endsWith(":*"));
    const agentOnly = resolvedTo && !resolvedTo.includes(":") && !explicitBroadcast;
    if (opts.inReplyTo && (!resolvedTo || agentOnly)) {
      const original = findMessageById(opts.inReplyTo);
      if (original && original.from) {
        resolvedTo = original.from;
      }
    }
    if (!resolvedTo) {
      // No target and no inReplyTo to resolve from. Nothing safe to do
      // except a no-op. Caller is at fault; return null to signal.
      return null;
    }

    const data: InboxMessage = {
      id,
      type: opts.type || "chat",
      from: opts.from || `${_sessionAgentId}:${_sessionName}`,
      to: resolvedTo,
      body: opts.body,
      timestamp: new Date().toISOString(),
      read: false,
      ...(opts.inReplyTo ? { inReplyTo: opts.inReplyTo } : {}),
    };
    writeFileSync(join(MESSAGES_DIR, `${id}.json`), JSON.stringify(data, null, 2) + "\n");
    return id;
  } catch {
    return null;
  }
}

// ── Session management (Phase 2) ────────────────────────────────────

const SESSIONS_DIR = join(LDM_ROOT, "sessions");

export interface SessionInfo {
  name: string;
  agentId: string;
  pid: number;
  startTime: string;
  cwd: string;
  alive: boolean;
  meta?: Record<string, unknown>;
}

/**
 * Register this bridge session in ~/.ldm/sessions/.
 * Uses the agent--session naming convention.
 */
export function registerBridgeSession(): SessionInfo | null {
  try {
    mkdirSync(SESSIONS_DIR, { recursive: true });
    const fileName = `${_sessionAgentId}--${_sessionName}.json`;
    const data: SessionInfo = {
      name: _sessionName,
      agentId: _sessionAgentId,
      pid: process.pid,
      startTime: new Date().toISOString(),
      cwd: process.cwd(),
      alive: true,
    };
    writeFileSync(join(SESSIONS_DIR, fileName), JSON.stringify(data, null, 2) + "\n");
    return data;
  } catch {
    return null;
  }
}

/**
 * List active sessions. Validates PID liveness and cleans stale entries.
 */
export function listActiveSessions(agentFilter?: string): SessionInfo[] {
  try {
    if (!existsSync(SESSIONS_DIR)) return [];

    const files = readdirSync(SESSIONS_DIR).filter(f => f.endsWith(".json"));
    const sessions: SessionInfo[] = [];

    for (const file of files) {
      try {
        const filePath = join(SESSIONS_DIR, file);
        const data = JSON.parse(readFileSync(filePath, "utf-8")) as SessionInfo;

        // PID liveness check
        let alive = false;
        try {
          process.kill(data.pid, 0);
          alive = true;
        } catch {
          // Dead PID. Clean up.
          try { unlinkSync(filePath); } catch {}
          continue;
        }

        if (agentFilter && data.agentId !== agentFilter) continue;

        sessions.push({ ...data, alive });
      } catch {}
    }

    return sessions;
  } catch {
    return [];
  }
}

// ── Send message to OpenClaw agent ───────────────────────────────────

export async function sendMessage(
  openclawDir: string,
  message: string,
  options?: { agentId?: string; user?: string; senderLabel?: string; fireAndForget?: boolean }
): Promise<string> {
  const { token, port } = resolveGatewayConfig(openclawDir);
  const agentId = options?.agentId || "main";
  const senderLabel = options?.senderLabel || "Claude Code";
  const fireAndForget = options?.fireAndForget ?? false;

  // Send user: "main" to route to the main session (agent:main:main).
  // This ensures Parker sees CC's messages in the same stream as iMessage.
  // The OpenClaw gateway treats user: "main" as "use the default session."
  const requestBody = JSON.stringify({
    model: `openclaw/${agentId}`,
    messages: [
      {
        role: "user",
        content: `[${senderLabel}]: ${message}`,
      },
    ],
  });

  const requestHeaders: Record<string, string> = {
    Authorization: `Bearer ${token}`,
    "Content-Type": "application/json",
    "x-openclaw-scopes": "operator.read,operator.write",
    "x-openclaw-session-key": `agent:${agentId}:main`,
  };

  const url = `http://${GATEWAY_HOST}:${port}/v1/chat/completions`;

  // Fire-and-forget: send the request and return immediately.
  // The message is queued in the gateway. Lēsa processes it when she's ready.
  // No timeout. No waiting. Like dropping a letter in a mailbox.
  if (fireAndForget) {
    fetch(url, {
      method: "POST",
      headers: requestHeaders,
      body: requestBody,
    }).catch(() => {}); // Ignore errors silently
    return "Message sent (queued). Response will arrive in the TUI.";
  }

  // Synchronous: wait for the full response.
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), GATEWAY_TIMEOUT_MS);

  try {
    const response = await fetch(url, {
      method: "POST",
      headers: requestHeaders,
      body: requestBody,
      signal: controller.signal,
    });
    clearTimeout(timeoutId);

    if (!response.ok) {
      const body = await response.text();
      throw new Error(`Gateway returned ${response.status}: ${body}`);
    }

    const data = (await response.json()) as {
      choices: Array<{ message: { content: string } }>;
    };

    const reply = data.choices?.[0]?.message?.content;
    if (!reply) {
      throw new Error("No response content from gateway");
    }

    return reply;
  } catch (err: any) {
    clearTimeout(timeoutId);
    if (err.name === "AbortError") {
      throw new Error(
        "Gateway timeout: Lesa may be busy or the gateway is processing another request. Try again in a moment."
      );
    }
    throw err;
  }
}

// ── Embedding helpers ────────────────────────────────────────────────

export async function getQueryEmbedding(
  text: string,
  apiKey: string,
  model = DEFAULT_EMBEDDING_MODEL,
  dimensions = DEFAULT_EMBEDDING_DIMS
): Promise<number[]> {
  const response = await fetch(EMBEDDING_API_URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      input: [text],
      model,
      dimensions,
    }),
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`OpenAI embeddings failed (${response.status}): ${body}`);
  }

  const data = (await response.json()) as { data: Array<{ embedding: number[] }> };
  return data.data[0].embedding;
}

export function blobToEmbedding(blob: Buffer): number[] {
  const floats: number[] = [];
  for (let i = 0; i < blob.length; i += 4) {
    floats.push(blob.readFloatLE(i));
  }
  return floats;
}

export function cosineSimilarity(a: number[], b: number[]): number {
  let dot = 0;
  let normA = 0;
  let normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  const denom = Math.sqrt(normA) * Math.sqrt(normB);
  return denom === 0 ? 0 : dot / denom;
}

// ── Recency scoring ─────────────────────────────────────────────────

function recencyWeight(ageDays: number): number {
  // Linear decay with floor. Old stuff never fully disappears
  // but fresh context wins ties. ~50 days to hit the floor.
  return Math.max(RECENCY_FLOOR, 1.0 - ageDays * RECENCY_DECAY_RATE);
}

function freshnessLabel(ageDays: number): "fresh" | "recent" | "aging" | "stale" {
  if (ageDays < FRESHNESS_FRESH_DAYS) return "fresh";
  if (ageDays < FRESHNESS_RECENT_DAYS) return "recent";
  if (ageDays < FRESHNESS_AGING_DAYS) return "aging";
  return "stale";
}

// ── Conversation search ──────────────────────────────────────────────

export async function searchConversations(
  config: BridgeConfig,
  query: string,
  limit = DEFAULT_SEARCH_LIMIT
): Promise<ConversationResult[]> {
  // Lazy import to avoid requiring better-sqlite3 if not needed
  const Database = (await import("better-sqlite3")).default;

  if (!existsSync(config.dbPath)) {
    throw new Error(`Database not found: ${config.dbPath}`);
  }

  const db = new Database(config.dbPath, { readonly: true });
  db.pragma("journal_mode = WAL");

  try {
    const apiKey = resolveApiKey(config.openclawDir);

    if (apiKey) {
      // Vector search
      const queryEmbedding = await getQueryEmbedding(
        query, apiKey, config.embeddingModel, config.embeddingDimensions
      );

      const rows = db
        .prepare(
          `SELECT chunk_text, role, session_key, timestamp, embedding
           FROM conversation_chunks
           WHERE embedding IS NOT NULL
           ORDER BY timestamp DESC
           LIMIT ${VECTOR_SEARCH_ROW_LIMIT}`
        )
        .all() as Array<{
        chunk_text: string;
        role: string;
        session_key: string;
        timestamp: number;
        embedding: Buffer;
      }>;

      const now = Date.now();
      return rows
        .map((row) => {
          const cosine = cosineSimilarity(queryEmbedding, blobToEmbedding(row.embedding));
          const ageDays = (now - row.timestamp) / MS_PER_DAY;
          const weight = recencyWeight(ageDays);
          return {
            text: row.chunk_text,
            role: row.role,
            sessionKey: row.session_key,
            date: new Date(row.timestamp).toISOString().split("T")[0],
            similarity: cosine * weight,
            recencyScore: weight,
            freshness: freshnessLabel(ageDays),
          };
        })
        .sort((a, b) => (b.similarity || 0) - (a.similarity || 0))
        .slice(0, limit);
    } else {
      // Fallback: text search
      const rows = db
        .prepare(
          `SELECT chunk_text, role, session_key, timestamp
           FROM conversation_chunks
           WHERE chunk_text LIKE ?
           ORDER BY timestamp DESC
           LIMIT ?`
        )
        .all(`%${query}%`, limit) as Array<{
        chunk_text: string;
        role: string;
        session_key: string;
        timestamp: number;
      }>;

      return rows.map((row) => ({
        text: row.chunk_text,
        role: row.role,
        sessionKey: row.session_key,
        date: new Date(row.timestamp).toISOString().split("T")[0],
      }));
    }
  } finally {
    db.close();
  }
}

// ── Workspace search ─────────────────────────────────────────────────

export function findMarkdownFiles(dir: string, maxDepth = WORKSPACE_MAX_DEPTH, depth = 0): string[] {
  if (depth > maxDepth || !existsSync(dir)) return [];

  const files: string[] = [];
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    if (entry.name.startsWith(".") || entry.name === "node_modules") continue;
    const fullPath = join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...findMarkdownFiles(fullPath, maxDepth, depth + 1));
    } else if (entry.name.endsWith(".md")) {
      files.push(fullPath);
    }
  }
  return files;
}

export function searchWorkspace(workspaceDir: string, query: string): WorkspaceSearchResult[] {
  const files = findMarkdownFiles(workspaceDir);
  const queryLower = query.toLowerCase();
  const words = queryLower.split(/\s+/).filter((w) => w.length > 2);
  const results: WorkspaceSearchResult[] = [];

  for (const filePath of files) {
    try {
      const content = readFileSync(filePath, "utf-8");
      const contentLower = content.toLowerCase();

      let score = 0;
      for (const word of words) {
        if (contentLower.indexOf(word) !== -1) score++;
      }
      if (score === 0) continue;

      const lines = content.split("\n");
      const excerpts: string[] = [];
      for (let i = 0; i < lines.length && excerpts.length < WORKSPACE_MAX_EXCERPTS; i++) {
        const lineLower = lines[i].toLowerCase();
        if (words.some((w) => lineLower.includes(w))) {
          const start = Math.max(0, i - 1);
          const end = Math.min(lines.length, i + 2);
          excerpts.push(lines.slice(start, end).join("\n"));
        }
      }

      results.push({ path: relative(workspaceDir, filePath), excerpts, score });
    } catch {
      // Skip unreadable files
    }
  }

  return results.sort((a, b) => b.score - a.score).slice(0, WORKSPACE_MAX_RESULTS);
}

// ── Read workspace file ──────────────────────────────────────────────

export interface WorkspaceFileResult {
  content: string;
  relativePath: string;
}

// ── Skill types ─────────────────────────────────────────────────────

export interface SkillInfo {
  name: string;
  description: string;
  skillDir: string;
  hasScripts: boolean;
  scripts: string[];
  source: "builtin" | "custom";
  emoji?: string;
  requires?: Record<string, string[]>;
}

// ── Skill discovery ─────────────────────────────────────────────────

function parseSkillFrontmatter(content: string): { name?: string; description?: string; emoji?: string; requires?: Record<string, string[]> } {
  const match = content.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return {};

  const yaml = match[1];
  const name = yaml.match(/^name:\s*(.+)$/m)?.[1]?.trim();
  const description = yaml.match(/^description:\s*(.+)$/m)?.[1]?.trim();

  // Extract emoji from metadata block (handles both YAML and JSON-in-YAML formats)
  let emoji: string | undefined;
  const emojiMatch = yaml.match(/"emoji":\s*"([^"]+)"/);
  if (emojiMatch) emoji = emojiMatch[1];

  // Extract requires
  let requires: Record<string, string[]> | undefined;
  const requiresMatch = yaml.match(/"requires":\s*\{([^}]+)\}/);
  if (requiresMatch) {
    requires = {};
    const pairs = requiresMatch[1].matchAll(/"(\w+)":\s*\[([^\]]*)\]/g);
    for (const pair of pairs) {
      const values = pair[2].match(/"([^"]+)"/g)?.map(v => v.replace(/"/g, "")) || [];
      requires[pair[1]] = values;
    }
  }

  return { name, description, emoji, requires };
}

export function discoverSkills(openclawDir: string): SkillInfo[] {
  const skills: SkillInfo[] = [];
  const seen = new Set<string>();

  // Two places skills live:
  // 1. Built-in: extensions/*/node_modules/openclaw/skills/
  // 2. Custom: extensions/*/skills/
  const extensionsDir = join(openclawDir, "extensions");
  if (!existsSync(extensionsDir)) return skills;

  for (const ext of readdirSync(extensionsDir, { withFileTypes: true })) {
    if (!ext.isDirectory() || ext.name.startsWith(".")) continue;
    const extDir = join(extensionsDir, ext.name);

    const searchDirs: Array<{ dir: string; source: "builtin" | "custom" }> = [
      { dir: join(extDir, "node_modules", "openclaw", "skills"), source: "builtin" },
      { dir: join(extDir, "skills"), source: "custom" },
    ];

    for (const { dir, source } of searchDirs) {
      if (!existsSync(dir)) continue;

      for (const entry of readdirSync(dir, { withFileTypes: true })) {
        if (!entry.isDirectory() || entry.name.startsWith(".")) continue;

        const skillDir = join(dir, entry.name);
        const skillMd = join(skillDir, "SKILL.md");
        if (!existsSync(skillMd)) continue;

        // Deduplicate by skill name (same skill may appear in multiple extensions)
        if (seen.has(entry.name)) continue;
        seen.add(entry.name);

        try {
          const content = readFileSync(skillMd, "utf-8");
          const frontmatter = parseSkillFrontmatter(content);

          const scriptsDir = join(skillDir, "scripts");
          let scripts: string[] = [];
          let hasScripts = false;

          if (existsSync(scriptsDir) && statSync(scriptsDir).isDirectory()) {
            scripts = readdirSync(scriptsDir).filter(f =>
              f.endsWith(".sh") || f.endsWith(".py")
            );
            hasScripts = scripts.length > 0;
          }

          skills.push({
            name: frontmatter.name || entry.name,
            description: frontmatter.description || `OpenClaw skill: ${entry.name}`,
            skillDir,
            hasScripts,
            scripts,
            source,
            emoji: frontmatter.emoji,
            requires: frontmatter.requires,
          });
        } catch {
          // Skip unreadable skills
        }
      }
    }
  }

  return skills.sort((a, b) => a.name.localeCompare(b.name));
}

// ── Skill execution ─────────────────────────────────────────────────

export async function executeSkillScript(
  skillDir: string,
  scripts: string[],
  scriptName: string | undefined,
  args: string
): Promise<string> {
  const scriptsDir = join(skillDir, "scripts");

  // Find the script to run
  let script: string;
  if (scriptName) {
    if (!scripts.includes(scriptName)) {
      throw new Error(`Script "${scriptName}" not found. Available: ${scripts.join(", ")}`);
    }
    script = scriptName;
  } else if (scripts.length === 1) {
    script = scripts[0];
  } else {
    // Default: prefer .sh over .py, take the first
    const sh = scripts.find(s => s.endsWith(".sh"));
    script = sh || scripts[0];
  }

  const scriptPath = join(scriptsDir, script);

  // Determine interpreter
  const interpreter = script.endsWith(".py") ? "python3" : "bash";

  try {
    const { stdout, stderr } = await execAsync(
      `${interpreter} "${scriptPath}" ${args}`,
      {
        env: { ...process.env },
        timeout: SKILL_EXEC_TIMEOUT_MS,
        maxBuffer: SKILL_EXEC_MAX_BUFFER,
      }
    );
    return stdout || stderr || "(no output)";
  } catch (err: any) {
    // exec errors include stdout/stderr on the error object
    const output = err.stdout || err.stderr || err.message;
    throw new Error(`Script failed (exit ${err.code || "?"}): ${output}`);
  }
}

export function readWorkspaceFile(workspaceDir: string, filePath: string): WorkspaceFileResult {
  const resolved = resolve(workspaceDir, filePath);
  if (!resolved.startsWith(resolve(workspaceDir))) {
    throw new Error("Path must be within workspace/");
  }

  if (!existsSync(resolved)) {
    // List available files at the requested directory level
    const dir = resolved.endsWith(".md") ? join(resolved, "..") : resolved;
    if (existsSync(dir) && statSync(dir).isDirectory()) {
      const files = findMarkdownFiles(dir, 1);
      const listing = files.map((f) => relative(workspaceDir, f)).join("\n");
      throw new Error(`File not found: ${filePath}\n\nAvailable files:\n${listing}`);
    }
    throw new Error(`File not found: ${filePath}`);
  }

  return {
    content: readFileSync(resolved, "utf-8"),
    relativePath: relative(workspaceDir, resolved),
  };
}
