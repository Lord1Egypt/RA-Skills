// HTTP client for the Siobac owner-side API + OAuth Device Authorization
// endpoints. Every public function here normalizes server errors into the
// same ApiError shape so the CLI layer can emit a stable `code` field for
// agents to branch on.

import type { AuthState } from './state.js'
import { SKILL_VERSION } from './version.js'

export type ApiErrorCode =
  | 'network_error'        // fetch threw (DNS, ECONNREFUSED, TLS, timeout, ...)
  | 'authorization_pending'// device flow: user hasn't approved yet
  | 'slow_down'            // device flow: polling too fast, increase interval
  | 'access_denied'        // device flow: user explicitly denied
  | 'expired_token'        // device flow: device_code expired before approval
  | 'not_authenticated'    // CLI: no auth.json or token expired locally
  | 'session_expired'      // 401: token rejected by server (revoked / expired remotely)
  | 'forbidden'            // 403: token lacks scope, or owner doesn't own this agent
  | 'not_found'            // 404: agent / connection / invite not found
  | 'invalid_request'      // 400: malformed body
  | 'rate_limited'         // 429
  | 'server_error'         // 5xx
  | 'server_not_ready'     // device-flow endpoints not deployed yet (404 on /oauth/*)
  | 'not_implemented_yet'  // CLI: command stubbed pending real implementation
  | 'cli_error'            // local CLI input error
  // ── Reach-out (active connect) codes, from the merged connect transport ──
  | 'invalid_invite'       // 404: unknown slug / invite_not_found (typo / never existed)
  | 'invite_revoked'       // 404 (body invite_revoked): the slug EXISTED but the owner turned it off
  | 'invite_unreachable'   // connect/inspect: the invite's OWN host didn't respond (likely a bad/incomplete link)
  | 'cannot_connect_to_self' // 400: an agent tried to connect to its OWN share
  | 'invalid_client_credentials' // 401 (connect re-auth): stored client_secret is wrong, NOT a login-session issue
  | 'agent_unavailable'    // 409: the shared agent is stopped/unavailable
  | 'agent_busy'           // 409: agent_busy / queue_full (single-user mode)
  | 'blocked_by_owner'     // 403: post-rejection cooldown on the connect side
  | 'auth_blocked'         // 429: per-IP brute-force throttle
  | 'unknown'

export interface ApiError extends Error {
  code: ApiErrorCode
  status?: number
  body?: unknown
}

export function makeApiError(
  code: ApiErrorCode,
  message: string,
  extras: { status?: number; body?: unknown } = {},
): ApiError {
  const err = new Error(message) as ApiError
  err.code = code
  if (extras.status !== undefined) err.status = extras.status
  if (extras.body !== undefined) err.body = extras.body
  return err
}

// The Siobac skill always talks to PRODUCTION. A fresh install (e.g. on an
// outside platform) points at the public server with no env var to set, so it
// "just works" for real users. (The Siobac brand keeps the ovoclaw.com backend
// domain.)
//
// Advanced/self-host escape hatch: set SIOBAC_API_BASE to a full URL to point
// the skill at your own Siobac server. Unset (the normal case) → production.
const PROD_API_BASE = 'https://ovo.ovoclaw.com'

export function getApiBase(): string {
  const explicit = process.env.SIOBAC_API_BASE ?? process.env.OVOCLAW_API_BASE
  return explicit || PROD_API_BASE
}

// Which base getApiBase() resolved to — for diagnostics (doctor).
// 'custom' = an explicit SIOBAC_API_BASE/OVOCLAW_API_BASE URL is set.
export function getApiEnv(): 'prod' | 'custom' {
  return (process.env.SIOBAC_API_BASE ?? process.env.OVOCLAW_API_BASE) ? 'custom' : 'prod'
}

// ── Skill update reminder ─────────────────────────────────────────────
// The server echoes the latest/min skill version on every response (only for
// requests carrying our X-Siobac-Share-Version). We stash the last values
// seen this run; the CLI attaches a `skill_update` block to its output when
// we're behind, so the agent can tell the user to update.

export interface SkillUpdateNotice {
  current: string
  latest: string
  required: boolean        // true when below the server's minimum supported version
  update_url: string | null
  message: string
  // Enriched by the CLI before surfacing (see cli.ts): the exact on-disk skill
  // folder and a concrete, copy-pasteable update instruction.
  skill_path?: string
  how_to_update?: string
}

let seenLatest: string | null = null
let seenMin: string | null = null
let seenUrl: string | null = null

function captureUpdateHeaders(res: Response): void {
  // Prefer the new x-siobac-* headers; fall back to legacy x-ovoclaw-* so the
  // skill still reads update info from an older server that hasn't switched.
  const latest = res.headers.get('x-siobac-share-latest') ?? res.headers.get('x-ovoclaw-share-latest')
  if (!latest) return // old server without the version hook — stay silent
  seenLatest = latest
  seenMin = res.headers.get('x-siobac-share-min') ?? res.headers.get('x-ovoclaw-share-min')
  seenUrl = res.headers.get('x-siobac-share-update-url') ?? res.headers.get('x-ovoclaw-share-update-url')
}

// a < b for dotted numeric versions (e.g. '0.2.0' < '0.10.1'). Non-numeric or
// missing parts read as 0, so it degrades gracefully on odd inputs.
function versionLt(a: string, b: string): boolean {
  const pa = a.split('.').map((n) => parseInt(n, 10) || 0)
  const pb = b.split('.').map((n) => parseInt(n, 10) || 0)
  for (let i = 0; i < Math.max(pa.length, pb.length); i++) {
    const x = pa[i] ?? 0, y = pb[i] ?? 0
    if (x < y) return true
    if (x > y) return false
  }
  return false
}

// The update notice to surface, or null when we're current / heard nothing.
export function getSkillUpdateNotice(): SkillUpdateNotice | null {
  if (!seenLatest) return null
  const behind = versionLt(SKILL_VERSION, seenLatest)
  const required = !!seenMin && versionLt(SKILL_VERSION, seenMin)
  if (!behind && !required) return null
  return {
    current: SKILL_VERSION,
    latest: seenLatest,
    required,
    update_url: seenUrl,
    message: required
      ? 'This siobac skill is older than the server\'s minimum supported version and may misbehave — update it before relying on it.'
      : 'A newer siobac skill is available — tell the user they can update when convenient.',
  }
}

// Definitive freshness verdict, ALWAYS returned (never null). Actively probes
// the server — sends our version to /health and captures the reply headers —
// so a fresh process (e.g. `doctor`, which ran no other command) still knows
// whether it's current. Falls back to whatever was already seen this run if the
// probe can't reach the server.
export interface VersionStatus {
  up_to_date: boolean
  current: string
  latest: string | null
  required: boolean        // below the server's MINIMUM supported version
  update_url: string | null
  reachable: boolean       // false → couldn't reach the server to check
}
export async function getVersionStatus(): Promise<VersionStatus> {
  let reachable = false
  try {
    const res = await fetch(`${getApiBase()}/health`, {
      method: 'GET',
      headers: { 'X-Siobac-Share-Version': SKILL_VERSION },
    })
    captureUpdateHeaders(res)
    reachable = true
  } catch {
    /* offline — doctor's own api_reachable check reports the network error */
  }
  const behind = !!seenLatest && versionLt(SKILL_VERSION, seenLatest)
  const required = !!seenMin && versionLt(SKILL_VERSION, seenMin)
  return {
    up_to_date: reachable && !behind && !required,
    current: SKILL_VERSION,
    latest: seenLatest,
    required,
    update_url: seenUrl,
    reachable,
  }
}

// ── Wire helpers ──────────────────────────────────────────────────────

interface FetchOpts {
  method: string
  path: string
  bearer?: string
  body?: unknown
  // Used when /oauth/* returns 404 because the server hasn't been updated
  // yet — mapped to a clearer code than just "not_found".
  oauthEndpoint?: boolean
}

function classifyStatus(
  status: number,
  body: { error?: string } | undefined,
  opts: FetchOpts,
): ApiErrorCode {
  if (opts.oauthEndpoint && status === 404) return 'server_not_ready'
  if (status === 400) return 'invalid_request'
  if (status === 401) {
    const e = body?.error ?? ''
    if (e === 'authorization_pending') return 'authorization_pending'
    if (e === 'slow_down') return 'slow_down'
    if (e === 'access_denied') return 'access_denied'
    if (e === 'expired_token') return 'expired_token'
    return 'session_expired'
  }
  if (status === 403) return 'forbidden'
  if (status === 404) return 'not_found'
  if (status === 429) return 'rate_limited'
  if (status >= 500) return 'server_error'
  return 'unknown'
}

async function jsonFetch<T>(opts: FetchOpts): Promise<T> {
  const url = `${getApiBase()}${opts.path}`
  const headers: Record<string, string> = {
    Accept: 'application/json',
    // Tag every call with our version so the server can tell us (via reply
    // headers) when a newer skill is out — see captureUpdateHeaders below.
    'X-Ovoclaw-Share-Version': SKILL_VERSION,
  }
  if (opts.body !== undefined) headers['Content-Type'] = 'application/json'
  if (opts.bearer) headers['Authorization'] = `Bearer ${opts.bearer}`

  let res: Response
  try {
    res = await fetch(url, {
      method: opts.method,
      headers,
      body: opts.body !== undefined ? JSON.stringify(opts.body) : undefined,
    })
  } catch (e) {
    const cause = (e as Error & { cause?: { code?: string; message?: string } }).cause
    const reason = cause?.code || cause?.message || (e as Error).message || 'fetch failed'
    throw makeApiError('network_error', `network_error: ${reason}`)
  }

  // Record the server's version signal on every response (success OR error).
  captureUpdateHeaders(res)

  const text = await res.text()
  let body: unknown
  try {
    body = text ? JSON.parse(text) : {}
  } catch {
    body = { raw: text }
  }

  if (!res.ok) {
    const b = body as { error?: string; message?: string } | undefined
    const code = classifyStatus(res.status, b, opts)
    const msg = b?.message || b?.error || res.statusText
    throw makeApiError(code, `${code} (HTTP ${res.status}): ${msg}`, { status: res.status, body })
  }

  return body as T
}

// ── OAuth Device Authorization (RFC 8628) ────────────────────────────
// These endpoints don't exist on the Siobac server yet — Phase 2 work.
// Calls will return code:server_not_ready until they're deployed.

export interface DeviceCodeResponse {
  device_code: string
  user_code: string
  verification_uri: string
  verification_uri_complete?: string
  expires_in: number
  interval: number
}

export async function requestDeviceCode(scope?: string, agentHint?: string): Promise<DeviceCodeResponse> {
  const body: Record<string, unknown> = {
    client_id: 'ovoclaw-share-cli',
    // Unified skill: one login both serves (share/respond) AND reaches out as a
    // registered agent (connect). The server gate grants each capability per
    // scope; guest reach-out needs no token at all.
    scope: scope ?? 'agent:share agent:respond agent:connect',
  }
  // Remembered agent from a prior share — the approval page auto-confirms it
  // when the logged-in account still owns a matching agent.
  if (agentHint) body.agent_hint = agentHint
  return jsonFetch<DeviceCodeResponse>({
    method: 'POST',
    path: '/oauth/device/code',
    body,
    oauthEndpoint: true,
  })
}

export interface DeviceTokenResponse {
  access_token: string
  token_type: string
  expires_in: number
  refresh_token?: string
  scope?: string
  account_id?: string
  // Agent this token is scoped to act as (set by the approval page's picker).
  agent_id?: string | null
  // Display name of that agent, so we can surface + remember it by name.
  agent_name?: string | null
}

export async function pollDeviceToken(deviceCode: string): Promise<DeviceTokenResponse> {
  return jsonFetch<DeviceTokenResponse>({
    method: 'POST',
    path: '/oauth/device/token',
    body: {
      grant_type: 'urn:ietf:params:oauth:grant-type:device_code',
      device_code: deviceCode,
      client_id: 'ovoclaw-share-cli',
    },
    oauthEndpoint: true,
  })
}

export async function refreshAccessToken(refreshToken: string): Promise<DeviceTokenResponse> {
  return jsonFetch<DeviceTokenResponse>({
    method: 'POST',
    path: '/oauth/token',
    body: {
      grant_type: 'refresh_token',
      refresh_token: refreshToken,
      client_id: 'ovoclaw-share-cli',
    },
    oauthEndpoint: true,
  })
}

// ── Portable login (#16) — a non-rotating token for ephemeral-workspace hosts ──
export interface PortableTokenResponse {
  portable_token: string
  access_token: string
  expires_in: number
  portable_expires_in: number
  agent_id: string | null
  agent_name?: string | null
  scope: string
}
// Mint a portable token (caller must be logged in — owner bearer).
export async function issuePortableToken(bearer: string): Promise<PortableTokenResponse> {
  return jsonFetch<PortableTokenResponse>({ method: 'POST', path: '/oauth/portable-token', bearer, oauthEndpoint: true })
}
// Revoke all live portable tokens for the bound agent.
export async function revokePortableToken(bearer: string): Promise<{ ok: boolean; revoked: number }> {
  return jsonFetch({ method: 'POST', path: '/oauth/portable-token/revoke', bearer, oauthEndpoint: true })
}

// ── Owner-side API (existing JWT-authed endpoints, to be reused once
//    OAuth-issued tokens are accepted in addition to JWT) ─────────────
//
// Every function takes a `bearer` from the loaded AuthState. The endpoint
// paths mirror what's already implemented in apps/server's agents.routes.ts
// — the Phase 2 server work will add OAuth bearer acceptance to those.

export interface AgentSummary {
  id: string
  name: string
  description?: string
  status?: string
}

export interface ShareInvite {
  id: string
  agent_id: string
  slug: string
  requires_approval: boolean
  created_at: string
  share_url?: string
}

export interface ExternalConnection {
  id: string
  agent_id: string
  status: 'pending' | 'active' | 'paused' | 'rejected' | 'disconnected'
  intro_text?: string
  conversation_id: string
  shadow_user_id: string
  shadow_name?: string
  created_at: string
  accepted_at?: string
  last_seen_at?: string
}

// Who sent it / who's connecting — pulled from the connection's intro_meta.
export interface FriendIdentity {
  agent_name: string | null
  owner_name: string | null
}

export interface InboundMessage {
  id: string
  connection_id: string
  agent_id: string
  agent_name: string
  from?: FriendIdentity
  seq: number
  sender_user_id: string
  content: string
  created_at: string
}

export interface PendingRequest {
  id: string
  agent_id: string
  agent_name: string
  from?: FriendIdentity
  intro_text?: string | null
  intro_meta?: Record<string, unknown> | null
  conversation_id: string | null
  shadow_user_id: string | null
  created_at: string
}

// One thread per friend (connection) — messages still needing a reply, in
// chronological order. The grouped view to DISPLAY to the owner.
export interface InboxThread {
  connection_id: string
  agent_id: string
  agent_name: string
  from: FriendIdentity
  unread_count: number
  latest_at: string
  // held = this thread is awaiting the owner's decision (an open escalation); surface
  // it ONCE as the escalation (resolve via request_id), not also as a "new message."
  held?: boolean
  request_id?: string
  messages: { id: string; seq: number; content: string; created_at: string }[]
}

export interface InboxSnapshot {
  pending_requests: PendingRequest[]
  new_messages: InboundMessage[]
  threads: InboxThread[]
  // True when more unanswered inbound existed than the server returned — the
  // caller should drain via respond/read-conversation rather than assume this
  // is the full set.
  new_messages_truncated: boolean
  last_seq_by_connection: Record<string, number>
}

export async function listMyAgents(bearer: string): Promise<AgentSummary[]> {
  return jsonFetch<AgentSummary[]>({ method: 'GET', path: '/agents', bearer })
}

export async function createShare(
  bearer: string,
  agentId: string,
  options: { requires_approval?: boolean },
): Promise<ShareInvite> {
  return jsonFetch<ShareInvite>({
    method: 'POST',
    path: `/agents/${encodeURIComponent(agentId)}/external-invite`,
    bearer,
    body: options,
  })
}

// Toggle whether new connections need the owner's approval — IN PLACE, keeping
// the SAME slug/QR (PATCH, not regenerate). Returns the unchanged invite with the
// new flag.
export async function updateShareApproval(
  bearer: string,
  agentId: string,
  requiresApproval: boolean,
): Promise<ShareInvite> {
  return jsonFetch<ShareInvite>({
    method: 'PATCH',
    path: `/agents/${encodeURIComponent(agentId)}/external-invite`,
    bearer,
    body: { requires_approval: requiresApproval },
  })
}

// The agent's current active share invite (or null). Used to know the existing
// connect code before changing it.
export async function getActiveInvite(
  bearer: string,
  agentId: string,
): Promise<{ invite: { id: string; slug: string; requires_approval: boolean; created_at: string } | null }> {
  return jsonFetch<{ invite: ShareInvite | null }>({
    method: 'GET',
    path: `/agents/${encodeURIComponent(agentId)}/external-invite`,
    bearer,
  })
}

// Set or change the agent's custom connect code (the `<code>@siobac` handle).
// Updated in place — existing connections survive, the old code stops resolving.
// Throws an ApiError; the caller should special-case .status===409 (code_taken)
// and .status===400 (invalid format / reserved) to re-prompt.
export async function setConnectCode(
  bearer: string,
  agentId: string,
  code: string,
): Promise<ShareInvite> {
  return jsonFetch<ShareInvite>({
    method: 'PATCH',
    path: `/agents/${encodeURIComponent(agentId)}/external-invite/code`,
    bearer,
    body: { code },
  })
}

export interface CodeCheckResult {
  valid: boolean
  available: boolean
  code: string
  error?: 'invalid_format' | 'reserved'
}

// Vet a custom connect code before committing to it (format + availability).
export async function checkConnectCode(
  bearer: string,
  agentId: string,
  code: string,
): Promise<CodeCheckResult> {
  return jsonFetch<CodeCheckResult>({
    method: 'GET',
    path: `/agents/${encodeURIComponent(agentId)}/external-invite/check-code?code=${encodeURIComponent(code)}`,
    bearer,
  })
}

export interface ShareListEntry {
  agent_id: string
  agent_name: string
  invite: {
    id: string
    slug: string
    requires_approval: boolean
    created_at: string
  }
  share_url: string
}

export async function listShares(bearer: string): Promise<ShareListEntry[]> {
  // Phase 3: server-side aggregate over every agent the owner owns
  // (GET /agents/external-shares).
  return jsonFetch<ShareListEntry[]>({ method: 'GET', path: '/agents/external-shares', bearer })
}

export async function revokeShare(bearer: string, agentId: string): Promise<{ ok: true }> {
  return jsonFetch<{ ok: true }>({
    method: 'DELETE',
    path: `/agents/${encodeURIComponent(agentId)}/external-invite`,
    bearer,
  })
}

export async function regenerateShare(
  bearer: string,
  agentId: string,
  options: { requires_approval?: boolean } = {},
): Promise<ShareInvite> {
  return jsonFetch<ShareInvite>({
    method: 'POST',
    path: `/agents/${encodeURIComponent(agentId)}/external-invite/regenerate`,
    bearer,
    body: options,
  })
}

export async function listConnections(
  bearer: string,
  agentId: string,
): Promise<ExternalConnection[]> {
  return jsonFetch<ExternalConnection[]>({
    method: 'GET',
    path: `/agents/${encodeURIComponent(agentId)}/external-connections`,
    bearer,
  })
}

export async function actOnConnection(
  bearer: string,
  agentId: string,
  connectionId: string,
  action: 'accept' | 'reject' | 'disconnect' | 'pause' | 'resume' | 'rotate-token',
): Promise<ExternalConnection | { ok: true }> {
  return jsonFetch<ExternalConnection | { ok: true }>({
    method: 'POST',
    path: `/agents/${encodeURIComponent(agentId)}/external-connections/${encodeURIComponent(connectionId)}/${action}`,
    bearer,
  })
}

export async function fetchInbox(bearer: string): Promise<InboxSnapshot> {
  // Phase 3: server-side aggregate (GET /agents/external-inbox) — pending
  // requests + unanswered inbound messages + a per-connection seq high-water
  // map, all scoped to the owner's agents.
  return jsonFetch<InboxSnapshot>({ method: 'GET', path: '/agents/external-inbox', bearer })
}

export async function postReply(
  bearer: string,
  agentId: string,
  connectionId: string,
  content: string,
): Promise<{ ok: true; seq: number; message_id: string; conversation_id: string }> {
  return jsonFetch<{ ok: true; seq: number; message_id: string; conversation_id: string }>({
    method: 'POST',
    path: `/agents/${encodeURIComponent(agentId)}/external-connections/${encodeURIComponent(connectionId)}/respond`,
    bearer,
    body: { content },
  })
}

export interface ConversationMessage {
  id: string
  seq: number
  content: string
  message_type: string
  sender_user_id: string
  sender_name: string | null
  direction: 'inbound' | 'outbound'
  created_at: string
}

export interface ConversationHistory {
  conversation_id: string | null
  shadow_user_id: string | null
  messages: ConversationMessage[]
  last_seq: number
  has_more: boolean
}

export async function readConversation(
  bearer: string,
  agentId: string,
  connectionId: string,
  opts: { since?: number; limit?: number } = {},
): Promise<ConversationHistory> {
  const params = new URLSearchParams()
  if (opts.since !== undefined) params.set('since', String(opts.since))
  if (opts.limit !== undefined) params.set('limit', String(opts.limit))
  const qs = params.toString()
  return jsonFetch<ConversationHistory>({
    method: 'GET',
    path: `/agents/${encodeURIComponent(agentId)}/external-connections/${encodeURIComponent(connectionId)}/conversation${qs ? `?${qs}` : ''}`,
    bearer,
  })
}

// ── Directive (private, owner-only) ──────────────────────────────────
// The owner's prescriptive instructions to the agent (rules + purpose +
// info-handling standard). Private; only the owner reads/edits it; it is NEVER
// disclosed to a connecting friend.
export async function getDirective(bearer: string, agentId: string): Promise<{ content: string }> {
  return jsonFetch<{ content: string }>({
    method: 'GET',
    path: `/agents/${encodeURIComponent(agentId)}/directive`,
    bearer,
  })
}

export async function setDirective(bearer: string, agentId: string, content: string, ownerMsgSeq?: number): Promise<{ ok: true }> {
  return jsonFetch<{ ok: true }>({
    method: 'PUT',
    path: `/agents/${encodeURIComponent(agentId)}/directive`,
    bearer,
    body: ownerMsgSeq !== undefined ? { content, owner_msg_seq: ownerMsgSeq } : { content },
  })
}

// ── Agent profile (public card) — onboarding read + owner edit ───────
export interface AgentProfile {
  name: string
  description: string
  avatar_url: string | null
  directive: string
  profile_complete: boolean
  directive_set: boolean
  is_new: boolean
}
export async function getAgentProfile(bearer: string, agentId: string): Promise<AgentProfile> {
  return jsonFetch<AgentProfile>({
    method: 'GET',
    path: `/agents/${encodeURIComponent(agentId)}/profile`,
    bearer,
  })
}
export async function setAgentProfile(
  bearer: string, agentId: string, patch: { name?: string; description?: string; owner_msg_seq?: number },
): Promise<{ ok: true }> {
  return jsonFetch<{ ok: true }>({
    method: 'PUT',
    path: `/agents/${encodeURIComponent(agentId)}/profile`,
    bearer,
    body: patch,
  })
}

// ── Read-before-talk context + write-after-talk memory ───────────────
export interface FriendMemoryItem {
  id: string
  kind: 'fact' | 'preference' | 'event' | 'summary' | 'authorization'
  content: string
  disclosure: 'private' | 'friend_shared'
  confidence: number | null
  source_seq: number | null
  updated_at: string
}
export interface TalkContext {
  // directive.disclose is always false — it shapes HOW you reply, never shown.
  directive: { content: string; disclose: false }
  profile: { name: string; description: string | null; avatar_url: string | null } | null
  friend_memory: FriendMemoryItem[]
  mode: 'guest' | 'registered'
}
export async function getTalkContext(
  bearer: string, agentId: string, connectionId: string,
): Promise<TalkContext> {
  return jsonFetch<TalkContext>({
    method: 'GET',
    path: `/agents/${encodeURIComponent(agentId)}/external-connections/${encodeURIComponent(connectionId)}/context`,
    bearer,
  })
}

export interface MemoryDelta {
  op: 'add' | 'update' | 'supersede'
  scope: 'friend'
  friend_id: string
  // 'authorization' = a standing owner pre-approval the SERVER brain may act on directly
  // (e.g. an availability window) — confirm inside its scope without re-escalating.
  kind: 'fact' | 'preference' | 'event' | 'summary' | 'authorization'
  content: string
  disclosure?: 'private' | 'friend_shared'
  confidence?: number
  supersedes?: string
  source_seq?: number
}
export async function submitMemory(
  bearer: string, agentId: string, connectionId: string, deltas: MemoryDelta[],
): Promise<{ ok: true; applied: number }> {
  return jsonFetch<{ ok: true; applied: number }>({
    method: 'POST',
    path: `/agents/${encodeURIComponent(agentId)}/external-connections/${encodeURIComponent(connectionId)}/memory`,
    bearer,
    body: { memory_deltas: deltas },
  })
}

// ── Discovery / matchmaking ("find people outside") ──────────────────
// Owner-authed (same bearer as directive/profile). The server runs the whole
// match pipeline; the skill only confirms the purpose, shows ONE match, and
// accepts (which reuses the connect flow honouring the candidate's approval).
export interface MatchSuggestion {
  suggestion_id: string
  candidate_agent_id: string
  candidate_name: string
  candidate_description: string
  mode: 'same' | 'complementary' | 'both'
  score: number
  why_text: string
  matched_dimensions: { shared: string[]; complementary: string[] }
}
export async function discoverOn(bearer: string, agentId: string): Promise<{ ok: true; discoverable: boolean; has_purpose: boolean }> {
  return jsonFetch({ method: 'POST', path: `/agents/${encodeURIComponent(agentId)}/discover/on`, bearer })
}
export async function discoverOff(bearer: string, agentId: string): Promise<{ ok: true; discoverable: boolean }> {
  return jsonFetch({ method: 'POST', path: `/agents/${encodeURIComponent(agentId)}/discover/off`, bearer })
}
export async function setPurpose(
  bearer: string, agentId: string, text: string, mustHaves: string[],
): Promise<{ ok: true; intents: string[]; constraints: Record<string, unknown>; suggestion: MatchSuggestion | null }> {
  return jsonFetch({
    method: 'POST', path: `/agents/${encodeURIComponent(agentId)}/discover/purpose`, bearer,
    body: { text, must_haves: mustHaves },
  })
}
export async function getSuggestion(bearer: string, agentId: string): Promise<{ suggestion: MatchSuggestion | null; looking: boolean }> {
  return jsonFetch({ method: 'GET', path: `/agents/${encodeURIComponent(agentId)}/discover/suggestion`, bearer })
}
export async function nextSuggestion(bearer: string, agentId: string): Promise<{ suggestion: MatchSuggestion | null }> {
  return jsonFetch({ method: 'POST', path: `/agents/${encodeURIComponent(agentId)}/discover/next`, bearer })
}
export interface DiscoverySession {
  token: string; token_expires_at: string; client_secret: string
  your_user_id: string; conversation_id?: string; peer_name?: string
}
export async function acceptSuggestion(
  bearer: string, agentId: string,
  opts: { icebreak?: 'auto' | 'manual'; introduction?: string } = {},
): Promise<{
  ok: boolean; connect_status?: 'active' | 'awaiting_approval'; candidate_name?: string
  slug?: string; request_id?: string; conversation_id?: string
  session?: DiscoverySession; error?: string; reason?: string
}> {
  const body: Record<string, unknown> = {}
  if (opts.icebreak) body.icebreak = opts.icebreak
  if (opts.introduction) body.introduction = opts.introduction
  return jsonFetch({ method: 'POST', path: `/agents/${encodeURIComponent(agentId)}/discover/accept`, bearer, body })
}

// ── Reach-out transport (active connect) ─────────────────────────────
// These talk to a FULL host (resolved from the invite by parseInvite), not
// getApiBase(): an invite can point at any server/prefix. connect/manifest are
// unauthenticated; message/poll use the per-connection bearer (xext_) returned
// at connect. (A logged-in connect ALSO passes the owner login bearer so the
// server makes it a REGISTERED friendship; guest connect passes none.)
export interface Manifest {
  // The PUBLIC manifest deliberately omits the internal agent `id` (unauthenticated
  // endpoint) — verify by `name`, not `id`. `id` stays optional in case a server adds it.
  agent: { id?: string; name: string; description?: string; status?: string }
  ovo_protocol?: string
  requires_approval?: boolean
  [k: string]: unknown
}
export type ConnectStatus =
  | 'active' | 'awaiting_approval' | 'agent_unavailable' | 'agent_busy'
  | 'already_connected' | 'reauthorized' | 'invalid_client_credentials'
  | 'invalid_invite' | 'rate_limited' | 'blocked_by_owner'
export interface ConnectResponse {
  status: ConnectStatus
  token?: string; token_expires_at?: string; client_secret?: string
  your_user_id?: string; request_id?: string; conversation_id?: string
  peer_name?: string; registered?: boolean; retry_after_seconds?: number
  [k: string]: unknown
}
export interface ConnectInput {
  your_agent_name?: string; your_owner_name?: string
  introduction: string; purpose_hint?: string
  icebreak?: 'auto' | 'manual'   // #24: 'manual' = owner breaks the ice themselves (no auto exchange)
  client_user_id?: string; client_secret?: string
}
export interface SendMessageResponse {
  ok: boolean; message: { id: string; seq: number; [k: string]: unknown }
  agent_message?: unknown; reply_status?: 'received' | 'pending'
  conversation_id?: string; your_user_id?: string; delivery?: unknown
}
export interface ReplyMessage {
  id: string; seq: number; sender_user_id?: string; content: string; created_at: string
  direction?: 'inbound' | 'outbound'   // present on a full read (both directions)
  [k: string]: unknown
}
export interface PollRepliesResponse {
  messages: ReplyMessage[]; last_seq: number; conversation_id?: string
  your_user_id?: string; delivery?: unknown
}

function classifyInviteStatus(status: number, body: { error?: string; status?: string } | undefined): ApiErrorCode {
  // The connect server signals the precise reason in `status` (or legacy `error`).
  const tag = body?.status || body?.error
  if (status === 400) {
    // An agent connecting to its OWN share — a distinct, actionable mistake, not a
    // generic malformed body. Surface it precisely so the hint can say "use a
    // DIFFERENT agent's share" instead of "bad link".
    if (tag === 'cannot_connect_to_self') return 'cannot_connect_to_self'
    return 'invalid_request'
  }
  if (status === 401) {
    // Re-auth with a stale/wrong client_secret returns 401 here — that is NOT the
    // owner's LOGIN session expiring. Mapping it to session_expired sent the agent
    // down a useless `login` path; keep it distinct so the hint says "reconnect".
    if (tag === 'invalid_client_credentials') return 'invalid_client_credentials'
    return 'session_expired'
  }
  if (status === 403) return 'blocked_by_owner'
  if (status === 404) {
    // A slug that EXISTED but was revoked by its owner is distinct from one that
    // never existed (a typo) — different owner advice (ask for a fresh link vs check
    // the spelling). The server tags the revoked case in the body.
    if (tag === 'invite_revoked') return 'invite_revoked'
    return 'invalid_invite'
  }
  if (status === 409) return body?.error === 'agent_busy' || body?.error === 'queue_full' ? 'agent_busy' : 'agent_unavailable'
  if (status === 429) return body?.error === 'auth_blocked' ? 'auth_blocked' : 'rate_limited'
  if (status >= 500) return 'server_error'
  return 'unknown'
}

// Full-URL fetch (no getApiBase prefix) with the same error normalization shape.
async function inviteFetch<T>(url: string, init: RequestInit): Promise<T> {
  let res: Response
  try {
    res = await fetch(url, init)
  } catch (e) {
    const cause = (e as Error & { cause?: { code?: string; message?: string } }).cause
    const reason = cause?.code || cause?.message || (e as Error).message || 'fetch failed'
    throw makeApiError('network_error', `network_error: ${reason}`)
  }
  const text = await res.text()
  let body: unknown
  try { body = text ? JSON.parse(text) : {} } catch { body = { raw: text } }
  if (!res.ok) {
    const b = body as { message?: string; error?: string } | undefined
    const code = classifyInviteStatus(res.status, b)
    throw makeApiError(code, `${code} (HTTP ${res.status}): ${b?.message || b?.error || res.statusText}`, { status: res.status, body })
  }
  return body as T
}

export async function getManifest(host: string, slug: string): Promise<Manifest> {
  return inviteFetch<Manifest>(`${host}/manifest/${encodeURIComponent(slug)}`, { method: 'GET' })
}
// bearer: the owner login token → REGISTERED connect; omit → GUEST connect.
export async function connectToInvite(host: string, slug: string, body: ConnectInput, bearer?: string): Promise<ConnectResponse> {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' }
  if (bearer) headers['Authorization'] = `Bearer ${bearer}`
  return inviteFetch<ConnectResponse>(`${host}/connect/${encodeURIComponent(slug)}`, {
    method: 'POST', headers, body: JSON.stringify(body),
  })
}
export async function pollConnect(host: string, slug: string, requestId: string): Promise<ConnectResponse> {
  return inviteFetch<ConnectResponse>(`${host}/connect/${encodeURIComponent(slug)}/poll/${encodeURIComponent(requestId)}`, { method: 'GET' })
}
export async function sendToConnection(host: string, token: string, content: string): Promise<SendMessageResponse> {
  return inviteFetch<SendMessageResponse>(`${host}/message`, {
    method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }, body: JSON.stringify({ content }),
  })
}
export async function pollConnectionReplies(host: string, token: string, sinceSeq: number, waitSeconds = 0, full = false): Promise<PollRepliesResponse> {
  const params = new URLSearchParams({ since: String(sinceSeq), wait: String(waitSeconds) })
  if (full) params.set('full', '1')   // whole-conversation read (both directions)
  return inviteFetch<PollRepliesResponse>(`${host}/poll?${params.toString()}`, { method: 'GET', headers: { Authorization: `Bearer ${token}` } })
}

// ── Outbound (reach-out) conversations under the OWNER's login ──────────────
// Replaces the old guest `xext_` sessions: a logged-in agent lists / reads / sends on
// its OWN reach-out conversations via OAuth, keyed by connection_id (server:
// agents/outbound.service). No per-conversation token, no local session, no reauth.
export interface OutboundConnection {
  connection_id: string
  status: string
  conversation_id: string | null
  peer_name: string | null
  peer_description: string | null
  ice_break_closed: boolean
  new_count: number
  created_at: string
  last_seen_at: string | null
}
export async function listOutbound(bearer: string): Promise<{ connections: OutboundConnection[] }> {
  return jsonFetch<{ connections: OutboundConnection[] }>({ method: 'GET', path: '/agents/outbound', bearer })
}
export async function readOutbound(
  bearer: string,
  connectionId: string,
  opts: { since?: number; limit?: number } = {},
): Promise<ConversationHistory & { your_user_id: string | null }> {
  const params = new URLSearchParams()
  if (opts.since !== undefined) params.set('since', String(opts.since))
  if (opts.limit !== undefined) params.set('limit', String(opts.limit))
  const qs = params.toString()
  return jsonFetch<ConversationHistory & { your_user_id: string | null }>({
    method: 'GET',
    path: `/agents/outbound/${encodeURIComponent(connectionId)}/conversation${qs ? `?${qs}` : ''}`,
    bearer,
  })
}
export async function sendOutbound(
  bearer: string,
  connectionId: string,
  content: string,
): Promise<{ ok?: boolean; status?: string; kind?: string; message?: { id?: string; seq?: number }; reply_status?: string }> {
  return jsonFetch({
    method: 'POST',
    path: `/agents/outbound/${encodeURIComponent(connectionId)}/message`,
    bearer,
    body: { content },
  })
}

// Re-export the AuthState type for convenience in cli.ts.
export type { AuthState }

// ── Agent Brain — owner surface (the brain itself runs on the SERVER) ──
// docs/agent-brain-api-contract.md. Owner-authed (acts as the agent's owner).
// Owner-channel, presence (online/paused), and escalation handling
// (pending/resolve) — no client tick/loop/slice; the server is the responder.
export interface OwnerChannelMsg { seq: number; from: 'owner' | 'agent'; text: string; ts: string; kind?: 'note' | 'operational' }
export async function brainOwnerChannelRead(bearer: string, agentId: string, since = 0): Promise<{ messages: OwnerChannelMsg[]; cursor: number | null }> {
  return jsonFetch({ method: 'GET', path: `/agents/${encodeURIComponent(agentId)}/owner-channel?since=${since}`, bearer })
}
export async function brainOwnerChannelPost(bearer: string, agentId: string, from: 'owner' | 'agent', text: string): Promise<{ seq: number }> {
  return jsonFetch({ method: 'POST', path: `/agents/${encodeURIComponent(agentId)}/owner-channel`, bearer, body: { from, text } })
}
// Durable overview dismissal (email-style inbox). Pass `seq` to drop ONE notice,
// or `up_to_seq` to bulk "clear all" (advance the read-cursor). Server-side, so a
// dismissed recap never re-surfaces in `check` — even after a fresh login.
export async function dismissNotice(
  bearer: string,
  agentId: string,
  arg: { seq: number } | { up_to_seq: number },
): Promise<{ dismissed: boolean } | { seen_seq: number }> {
  return jsonFetch({ method: 'POST', path: `/agents/${encodeURIComponent(agentId)}/owner-channel/dismiss`, bearer, body: arg })
}
export async function brainHandback(bearer: string, agentId: string): Promise<{ mode: 'paused' }> {
  return jsonFetch({ method: 'POST', path: `/agents/${encodeURIComponent(agentId)}/handback`, bearer })
}
// Resume autonomous mode after a pause (server answers again). Autonomous is the
// default, so this only undoes a prior pause.
export async function brainGoOnline(bearer: string, agentId: string): Promise<{ mode: 'auto' }> {
  return jsonFetch({ method: 'POST', path: `/agents/${encodeURIComponent(agentId)}/online`, bearer })
}
// mode + online only. (Earlier builds also carried last_tick_at/seconds_since_tick/
// offline_after_ms — vestiges of a client-scheduled brain that never shipped; online is
// purely !paused, so they were dead/misleading and the server no longer returns them.)
export interface BrainPresence { mode: 'auto' | 'paused'; online: boolean }
// Read-only check of the server-reported autonomous mode (online vs paused).
// online=false means the owner paused — surface that; nothing to re-arm (server-driven).
export async function brainPresence(bearer: string, agentId: string): Promise<BrainPresence> {
  return jsonFetch({ method: 'GET', path: `/agents/${encodeURIComponent(agentId)}/presence`, bearer })
}
export interface BrainPendingReq { request_id: string; connId: string; reason: string; proposed_draft?: string; friend?: string; purpose?: string; created_at: string }
export async function brainPending(bearer: string, agentId: string): Promise<{ pending: BrainPendingReq[] }> {
  return jsonFetch({ method: 'GET', path: `/agents/${encodeURIComponent(agentId)}/brain/pending`, bearer })
}
export async function brainResolve(bearer: string, agentId: string, requestId: string, action: 'sent' | 'handed_off' | 'declined', content?: string): Promise<{ ok: boolean; sent?: boolean; outcome?: 'done' | 'updated'; update?: { reason: string; draft: string; friend?: string } }> {
  return jsonFetch({ method: 'POST', path: `/agents/${encodeURIComponent(agentId)}/brain/pending/${encodeURIComponent(requestId)}/resolve`, bearer, body: content !== undefined ? { action, content } : { action } })
}
