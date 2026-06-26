// memory-crystal/cloud/types.ts — Shared types for the cloud MCP server.

// ── Cloudflare Worker Environment ──

export interface Env {
  DB: D1Database;
  RELAY: R2Bucket;
  // VECTORS: VectorizeIndex;  // Tier 2 (future)
  OPENAI_API_KEY: string;
  OPENAI_EMBEDDING_MODEL: string;
  CRYSTAL_RELAY_KEY: string;
  OAUTH_SIGNING_SECRET: string;
  MCP_SERVER_NAME: string;
  MCP_SERVER_VERSION: string;
}

// ── Memory Types (subset of core.ts) ──

export type MemoryCategory = 'fact' | 'preference' | 'event' | 'opinion' | 'skill' | 'user' | 'feedback' | 'project' | 'reference';

// ── Encrypted Relay Payload (matches crypto.ts from memory-crystal) ──

export interface EncryptedPayload {
  v: 1;
  nonce: string;       // 12 bytes, base64
  ciphertext: string;  // base64
  tag: string;         // 16 bytes, base64
  hmac: string;        // 32 bytes, hex
}

// ── Relay Drop Metadata ──

export interface RelayDrop {
  type: 'remember' | 'forget' | 'conversation' | 'attachment';
  agent_id: string;
  user_id: string;
  timestamp: string;
  data: RememberData | ForgetData | ConversationData | AttachmentData;
}

export interface RememberData {
  text: string;
  category: MemoryCategory;
  source: 'chatgpt' | 'claude';
  surface: 'macos' | 'ios' | 'web';
}

export interface ForgetData {
  memory_id: number;
  reason?: string;
}

// Raw conversation turn ... gets chunked + embedded on the Mini.
// This mirrors what context-embeddings captures locally.
// The goal: the Mini has the same data it would have if this was a local session.
export interface ConversationData {
  role: 'user' | 'assistant' | 'system';
  content: string;
  source: 'chatgpt' | 'claude';
  surface: 'macos' | 'ios' | 'web';
  session_id?: string;       // groups turns in one conversation
  turn_index?: number;       // ordering within a session
  model?: string;            // e.g. 'gpt-4o', 'claude-sonnet-4-6'
  raw_json?: string;         // full raw message JSON (the complete message object)
  tool_calls?: ToolCallRecord[];  // tool calls made in this turn
  attachments?: InlineAttachment[]; // inline images/files referenced in this turn
}

// Tool call within a conversation turn (for full reconstruction)
export interface ToolCallRecord {
  tool_name: string;
  arguments: string;       // JSON string of tool args
  result?: string;         // tool result text
}

// Inline attachment reference (image URL, file reference from the conversation)
export interface InlineAttachment {
  type: 'image_url' | 'file' | 'audio';
  url?: string;            // URL if available (e.g. ChatGPT image URLs)
  filename?: string;
  mime_type?: string;
  data_base64?: string;    // inline binary data if small enough
}

// Binary attachment ... stored as separate R2 object, metadata in the drop
export interface AttachmentData {
  filename: string;
  mime_type: string;      // e.g. 'image/png', 'audio/mp4', 'video/mp4'
  size_bytes: number;
  r2_key: string;         // key of the binary blob in R2 (set by relay.ts)
  source: 'chatgpt' | 'claude';
  surface: 'macos' | 'ios' | 'web';
  context?: string;       // what the attachment relates to
  session_id?: string;
}

// ── OAuth Types ──

export interface OAuthClient {
  client_id: string;
  redirect_uris: string;
  client_name: string | null;
  created_at: string;
  last_used_at: string | null;
}

export interface TokenRow {
  token_hash: string;
  client_id: string;
  user_id: string;
  scope: string | null;
  tier: string;
  expires_at: string;
  created_at: string;
}

export interface UserRow {
  user_id: string;
  email: string;
  tier: string;
  relay_token: string | null;
  created_at: string;
}
