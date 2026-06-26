// ---------------------------------------------------------------------------
// WTT Protocol Types — mirrors the WebSocket protocol defined in
// wtt_service/api/ws.py and wtt-web/lib/useWebSocket.ts
// ---------------------------------------------------------------------------

/** Per-account config persisted in openclaw.json under channels.wtt */
export type WTTAccountConfig = {
  enabled?: boolean;
  name?: string;
  cloudUrl?: string; // e.g. "https://www.waxbyte.com"
  agentId?: string; // WTT agent_id
  token?: string; // JWT auth token
  e2ePassword?: string; // E2E encryption password (optional)
  inboundPollIntervalMs?: number; // periodic catch-up poll interval (default disabled; set >0 to enable)
  inboundPollLimit?: number; // catch-up poll batch size (default 20)
  inboundDedupWindowMs?: number; // dedup TTL window (default 5 minutes)
  inboundDedupMaxEntries?: number; // max dedup ids retained in memory (default 2000)
  slashCompat?: boolean; // enable slash compatibility bridge in inbound relay
  slashCompatWttPrefixOnly?: boolean; // true => only /wtt maps to WTT command router
  slashBypassMentionGate?: boolean; // true => standalone slash commands bypass mention gate
  taskExecutorScope?: "all" | "pipeline_only"; // task_status auto-run scope
  p2pE2EEnabled?: boolean; // enable P2P-only E2E encryption (default false)
  inboundMediaMaxBytes?: number; // max bytes per inbound media fetch (default 15MB)
  inboundMediaMaxPerMessage?: number; // max downloaded media count per message (default 4)
  inboundMediaFetchTimeoutMs?: number; // per-media fetch timeout (default 20s)
  discussionContextFetchLimit?: number; // fetch count for discuss context hydration (default 120)
  discussionContextWindow?: number; // recent message window sent to model (default 60)
  discussionContextMaxChars?: number; // max chars for hydrated context block (default 12000)
};

/** Resolved account ready for runtime use */
export type ResolvedWTTAccount = {
  accountId: string;
  name?: string;
  enabled: boolean;
  configured: boolean;
  cloudUrl: string;
  agentId: string;
  token: string;
  config: WTTAccountConfig;
};

// ---------------------------------------------------------------------------
// WebSocket Actions (Client → Server)
// ---------------------------------------------------------------------------

export type WsAction =
  | "list"
  | "find"
  | "join"
  | "leave"
  | "subscribed"
  | "publish"
  | "poll"
  | "p2p"
  | "history"
  | "detail"
  | "typing";

/** Base action message shape sent to WTT cloud */
export interface WsActionMessage {
  action: WsAction;
  request_id: string;
  [key: string]: unknown;
}

/** Auth message sent as first message after connect */
export interface WsAuthMessage {
  action: "auth";
  token: string;
  request_id?: string;
}

/** Action payloads by action type */
export interface ActionPayloads {
  list: { limit?: number };
  find: { query: string };
  join: { topic_id: string };
  leave: { topic_id: string };
  subscribed: Record<string, never>;
  publish: {
    topic_id: string;
    content: string;
    content_type?: string;
    semantic_type?: string;
    reply_to?: string;
    encrypted?: boolean;
  };
  poll: { limit?: number };
  p2p: { target_agent_id: string; content: string; encrypted?: boolean };
  history: { topic_id: string; limit?: number; before_id?: string };
  detail: { topic_id: string };
  typing: { topic_id: string; state: "start" | "stop"; ttl_ms?: number };
}

// ---------------------------------------------------------------------------
// WebSocket Messages (Server → Client)
// ---------------------------------------------------------------------------

/** Action result — response to a client action */
export interface WsActionResult {
  type: "action_result";
  request_id: string;
  ok: boolean;
  data?: unknown;
  error?: string;
}

/** New message push — server broadcasts to topic members */
export interface WsNewMessage {
  type: "new_message";
  message: WsMessagePayload;
}

/** Task status change push */
export interface WsTaskStatus {
  type: "task_status";
  task_id: string;
  status: string;
  title?: string;
  description?: string;
  exec_mode?: string;
  task_type?: string;
}

export interface WsTyping {
  type: "typing";
  topic_id: string;
  agent_id: string;
  agent_display_name?: string;
  state: "start" | "stop";
  ttl_ms?: number;
  ts?: number;
}

/** Web asks plugin to provide derived E2E key for owner browser bootstrap. */
export interface WsE2EKeyRequest {
  type: "e2e_key_request";
  request_id: string;
}

/** Union of all server → client messages */
export type WsServerMessage = WsActionResult | WsNewMessage | WsTaskStatus | WsTyping | WsE2EKeyRequest;

// ---------------------------------------------------------------------------
// Data shapes returned in action results and push messages
// ---------------------------------------------------------------------------

export interface WsMessagePayload {
  id: string;
  topic_id: string;
  sender_id: string;
  sender_type?: "human" | "agent";
  content_type?: string;
  semantic_type?: string;
  content: string;
  created_at: string;
  encrypted?: boolean;
  reply_to?: string;
}

export interface WsTopicPayload {
  id: string;
  name: string;
  description: string;
  type: "broadcast" | "discussion" | "p2p" | "collaborative";
  visibility?: "public" | "private";
  join_method?: "open" | "invite_only";
  member_count?: number;
  creator_agent_id?: string;
  my_role?: string;
  created_at: string;
}

// ---------------------------------------------------------------------------
// E2E Encryption types
// ---------------------------------------------------------------------------

export interface E2EConfig {
  enabled: boolean;
  password?: string;
}

/** Encrypted message wrapper */
export interface EncryptedContent {
  ciphertext: string; // base64-encoded
  contextId: string; // messageId used as nonce derivation seed
}
