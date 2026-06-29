// HTTP client for the Siobac owner-side API + OAuth Device Authorization
// endpoints. Every public function here normalizes server errors into the
// same ApiError shape so the CLI layer can emit a stable `code` field for
// agents to branch on.
import { SKILL_VERSION } from './version.js';
export function makeApiError(code, message, extras = {}) {
    const err = new Error(message);
    err.code = code;
    if (extras.status !== undefined)
        err.status = extras.status;
    if (extras.body !== undefined)
        err.body = extras.body;
    return err;
}
// The Siobac skill always talks to PRODUCTION. A fresh install (e.g. on an
// outside platform) points at the public server with no env var to set, so it
// "just works" for real users. (The Siobac brand keeps the ovoclaw.com backend
// domain.)
//
// Advanced/self-host escape hatch: set SIOBAC_API_BASE to a full URL to point
// the skill at your own Siobac server. Unset (the normal case) → production.
const PROD_API_BASE = 'https://ovo.ovoclaw.com';
export function getApiBase() {
    const explicit = process.env.SIOBAC_API_BASE ?? process.env.OVOCLAW_API_BASE;
    return explicit || PROD_API_BASE;
}
// Which base getApiBase() resolved to — for diagnostics (doctor).
// 'custom' = an explicit SIOBAC_API_BASE/OVOCLAW_API_BASE URL is set.
export function getApiEnv() {
    return (process.env.SIOBAC_API_BASE ?? process.env.OVOCLAW_API_BASE) ? 'custom' : 'prod';
}
let seenLatest = null;
let seenMin = null;
let seenUrl = null;
function captureUpdateHeaders(res) {
    // Prefer the new x-siobac-* headers; fall back to legacy x-ovoclaw-* so the
    // skill still reads update info from an older server that hasn't switched.
    const latest = res.headers.get('x-siobac-share-latest') ?? res.headers.get('x-ovoclaw-share-latest');
    if (!latest)
        return; // old server without the version hook — stay silent
    seenLatest = latest;
    seenMin = res.headers.get('x-siobac-share-min') ?? res.headers.get('x-ovoclaw-share-min');
    seenUrl = res.headers.get('x-siobac-share-update-url') ?? res.headers.get('x-ovoclaw-share-update-url');
}
// a < b for dotted numeric versions (e.g. '0.2.0' < '0.10.1'). Non-numeric or
// missing parts read as 0, so it degrades gracefully on odd inputs.
function versionLt(a, b) {
    const pa = a.split('.').map((n) => parseInt(n, 10) || 0);
    const pb = b.split('.').map((n) => parseInt(n, 10) || 0);
    for (let i = 0; i < Math.max(pa.length, pb.length); i++) {
        const x = pa[i] ?? 0, y = pb[i] ?? 0;
        if (x < y)
            return true;
        if (x > y)
            return false;
    }
    return false;
}
// The update notice to surface, or null when we're current / heard nothing.
export function getSkillUpdateNotice() {
    if (!seenLatest)
        return null;
    const behind = versionLt(SKILL_VERSION, seenLatest);
    const required = !!seenMin && versionLt(SKILL_VERSION, seenMin);
    if (!behind && !required)
        return null;
    return {
        current: SKILL_VERSION,
        latest: seenLatest,
        required,
        update_url: seenUrl,
        message: required
            ? 'This siobac skill is older than the server\'s minimum supported version and may misbehave — update it before relying on it.'
            : 'A newer siobac skill is available — tell the user they can update when convenient.',
    };
}
export async function getVersionStatus() {
    let reachable = false;
    try {
        const res = await fetch(`${getApiBase()}/health`, {
            method: 'GET',
            headers: { 'X-Siobac-Share-Version': SKILL_VERSION },
        });
        captureUpdateHeaders(res);
        reachable = true;
    }
    catch {
        /* offline — doctor's own api_reachable check reports the network error */
    }
    const behind = !!seenLatest && versionLt(SKILL_VERSION, seenLatest);
    const required = !!seenMin && versionLt(SKILL_VERSION, seenMin);
    return {
        up_to_date: reachable && !behind && !required,
        current: SKILL_VERSION,
        latest: seenLatest,
        required,
        update_url: seenUrl,
        reachable,
    };
}
function classifyStatus(status, body, opts) {
    if (opts.oauthEndpoint && status === 404)
        return 'server_not_ready';
    if (status === 400)
        return 'invalid_request';
    if (status === 401) {
        const e = body?.error ?? '';
        if (e === 'authorization_pending')
            return 'authorization_pending';
        if (e === 'slow_down')
            return 'slow_down';
        if (e === 'access_denied')
            return 'access_denied';
        if (e === 'expired_token')
            return 'expired_token';
        return 'session_expired';
    }
    if (status === 403)
        return 'forbidden';
    if (status === 404)
        return 'not_found';
    if (status === 429)
        return 'rate_limited';
    if (status >= 500)
        return 'server_error';
    return 'unknown';
}
async function jsonFetch(opts) {
    const url = `${getApiBase()}${opts.path}`;
    const headers = {
        Accept: 'application/json',
        // Tag every call with our version so the server can tell us (via reply
        // headers) when a newer skill is out — see captureUpdateHeaders below.
        'X-Ovoclaw-Share-Version': SKILL_VERSION,
    };
    if (opts.body !== undefined)
        headers['Content-Type'] = 'application/json';
    if (opts.bearer)
        headers['Authorization'] = `Bearer ${opts.bearer}`;
    let res;
    try {
        res = await fetch(url, {
            method: opts.method,
            headers,
            body: opts.body !== undefined ? JSON.stringify(opts.body) : undefined,
        });
    }
    catch (e) {
        const cause = e.cause;
        const reason = cause?.code || cause?.message || e.message || 'fetch failed';
        throw makeApiError('network_error', `network_error: ${reason}`);
    }
    // Record the server's version signal on every response (success OR error).
    captureUpdateHeaders(res);
    const text = await res.text();
    let body;
    try {
        body = text ? JSON.parse(text) : {};
    }
    catch {
        body = { raw: text };
    }
    if (!res.ok) {
        const b = body;
        const code = classifyStatus(res.status, b, opts);
        const msg = b?.message || b?.error || res.statusText;
        throw makeApiError(code, `${code} (HTTP ${res.status}): ${msg}`, { status: res.status, body });
    }
    return body;
}
export async function requestDeviceCode(scope, agentHint) {
    const body = {
        client_id: 'ovoclaw-share-cli',
        // Unified skill: one login both serves (share/respond) AND reaches out as a
        // registered agent (connect). The server gate grants each capability per
        // scope; guest reach-out needs no token at all.
        scope: scope ?? 'agent:share agent:respond agent:connect',
    };
    // Remembered agent from a prior share — the approval page auto-confirms it
    // when the logged-in account still owns a matching agent.
    if (agentHint)
        body.agent_hint = agentHint;
    return jsonFetch({
        method: 'POST',
        path: '/oauth/device/code',
        body,
        oauthEndpoint: true,
    });
}
export async function pollDeviceToken(deviceCode) {
    return jsonFetch({
        method: 'POST',
        path: '/oauth/device/token',
        body: {
            grant_type: 'urn:ietf:params:oauth:grant-type:device_code',
            device_code: deviceCode,
            client_id: 'ovoclaw-share-cli',
        },
        oauthEndpoint: true,
    });
}
export async function refreshAccessToken(refreshToken) {
    return jsonFetch({
        method: 'POST',
        path: '/oauth/token',
        body: {
            grant_type: 'refresh_token',
            refresh_token: refreshToken,
            client_id: 'ovoclaw-share-cli',
        },
        oauthEndpoint: true,
    });
}
// Mint a portable token (caller must be logged in — owner bearer).
export async function issuePortableToken(bearer) {
    return jsonFetch({ method: 'POST', path: '/oauth/portable-token', bearer, oauthEndpoint: true });
}
// Revoke all live portable tokens for the bound agent.
export async function revokePortableToken(bearer) {
    return jsonFetch({ method: 'POST', path: '/oauth/portable-token/revoke', bearer, oauthEndpoint: true });
}
export async function listMyAgents(bearer) {
    return jsonFetch({ method: 'GET', path: '/agents', bearer });
}
export async function createShare(bearer, agentId, options) {
    return jsonFetch({
        method: 'POST',
        path: `/agents/${encodeURIComponent(agentId)}/external-invite`,
        bearer,
        body: options,
    });
}
// Toggle whether new connections need the owner's approval — IN PLACE, keeping
// the SAME slug/QR (PATCH, not regenerate). Returns the unchanged invite with the
// new flag.
export async function updateShareApproval(bearer, agentId, requiresApproval) {
    return jsonFetch({
        method: 'PATCH',
        path: `/agents/${encodeURIComponent(agentId)}/external-invite`,
        bearer,
        body: { requires_approval: requiresApproval },
    });
}
// The agent's current active share invite (or null). Used to know the existing
// connect code before changing it.
export async function getActiveInvite(bearer, agentId) {
    return jsonFetch({
        method: 'GET',
        path: `/agents/${encodeURIComponent(agentId)}/external-invite`,
        bearer,
    });
}
// Set or change the agent's custom connect code (the `<code>@siobac` handle).
// Updated in place — existing connections survive, the old code stops resolving.
// Throws an ApiError; the caller should special-case .status===409 (code_taken)
// and .status===400 (invalid format / reserved) to re-prompt.
export async function setConnectCode(bearer, agentId, code) {
    return jsonFetch({
        method: 'PATCH',
        path: `/agents/${encodeURIComponent(agentId)}/external-invite/code`,
        bearer,
        body: { code },
    });
}
// Vet a custom connect code before committing to it (format + availability).
export async function checkConnectCode(bearer, agentId, code) {
    return jsonFetch({
        method: 'GET',
        path: `/agents/${encodeURIComponent(agentId)}/external-invite/check-code?code=${encodeURIComponent(code)}`,
        bearer,
    });
}
export async function listShares(bearer) {
    // Phase 3: server-side aggregate over every agent the owner owns
    // (GET /agents/external-shares).
    return jsonFetch({ method: 'GET', path: '/agents/external-shares', bearer });
}
export async function revokeShare(bearer, agentId) {
    return jsonFetch({
        method: 'DELETE',
        path: `/agents/${encodeURIComponent(agentId)}/external-invite`,
        bearer,
    });
}
export async function regenerateShare(bearer, agentId, options = {}) {
    return jsonFetch({
        method: 'POST',
        path: `/agents/${encodeURIComponent(agentId)}/external-invite/regenerate`,
        bearer,
        body: options,
    });
}
export async function listConnections(bearer, agentId) {
    return jsonFetch({
        method: 'GET',
        path: `/agents/${encodeURIComponent(agentId)}/external-connections`,
        bearer,
    });
}
export async function actOnConnection(bearer, agentId, connectionId, action) {
    return jsonFetch({
        method: 'POST',
        path: `/agents/${encodeURIComponent(agentId)}/external-connections/${encodeURIComponent(connectionId)}/${action}`,
        bearer,
    });
}
export async function fetchInbox(bearer) {
    // Phase 3: server-side aggregate (GET /agents/external-inbox) — pending
    // requests + unanswered inbound messages + a per-connection seq high-water
    // map, all scoped to the owner's agents.
    return jsonFetch({ method: 'GET', path: '/agents/external-inbox', bearer });
}
export async function postReply(bearer, agentId, connectionId, content) {
    return jsonFetch({
        method: 'POST',
        path: `/agents/${encodeURIComponent(agentId)}/external-connections/${encodeURIComponent(connectionId)}/respond`,
        bearer,
        body: { content },
    });
}
export async function readConversation(bearer, agentId, connectionId, opts = {}) {
    const params = new URLSearchParams();
    if (opts.since !== undefined)
        params.set('since', String(opts.since));
    if (opts.limit !== undefined)
        params.set('limit', String(opts.limit));
    const qs = params.toString();
    return jsonFetch({
        method: 'GET',
        path: `/agents/${encodeURIComponent(agentId)}/external-connections/${encodeURIComponent(connectionId)}/conversation${qs ? `?${qs}` : ''}`,
        bearer,
    });
}
// ── Directive (private, owner-only) ──────────────────────────────────
// The owner's prescriptive instructions to the agent (rules + purpose +
// info-handling standard). Private; only the owner reads/edits it; it is NEVER
// disclosed to a connecting friend.
export async function getDirective(bearer, agentId) {
    return jsonFetch({
        method: 'GET',
        path: `/agents/${encodeURIComponent(agentId)}/directive`,
        bearer,
    });
}
export async function setDirective(bearer, agentId, content, ownerMsgSeq) {
    return jsonFetch({
        method: 'PUT',
        path: `/agents/${encodeURIComponent(agentId)}/directive`,
        bearer,
        body: ownerMsgSeq !== undefined ? { content, owner_msg_seq: ownerMsgSeq } : { content },
    });
}
export async function getAgentProfile(bearer, agentId) {
    return jsonFetch({
        method: 'GET',
        path: `/agents/${encodeURIComponent(agentId)}/profile`,
        bearer,
    });
}
export async function setAgentProfile(bearer, agentId, patch) {
    return jsonFetch({
        method: 'PUT',
        path: `/agents/${encodeURIComponent(agentId)}/profile`,
        bearer,
        body: patch,
    });
}
export async function getTalkContext(bearer, agentId, connectionId) {
    return jsonFetch({
        method: 'GET',
        path: `/agents/${encodeURIComponent(agentId)}/external-connections/${encodeURIComponent(connectionId)}/context`,
        bearer,
    });
}
export async function submitMemory(bearer, agentId, connectionId, deltas) {
    return jsonFetch({
        method: 'POST',
        path: `/agents/${encodeURIComponent(agentId)}/external-connections/${encodeURIComponent(connectionId)}/memory`,
        bearer,
        body: { memory_deltas: deltas },
    });
}
export async function discoverOn(bearer, agentId) {
    return jsonFetch({ method: 'POST', path: `/agents/${encodeURIComponent(agentId)}/discover/on`, bearer });
}
export async function discoverOff(bearer, agentId) {
    return jsonFetch({ method: 'POST', path: `/agents/${encodeURIComponent(agentId)}/discover/off`, bearer });
}
export async function setPurpose(bearer, agentId, text, mustHaves) {
    return jsonFetch({
        method: 'POST', path: `/agents/${encodeURIComponent(agentId)}/discover/purpose`, bearer,
        body: { text, must_haves: mustHaves },
    });
}
export async function getSuggestion(bearer, agentId) {
    return jsonFetch({ method: 'GET', path: `/agents/${encodeURIComponent(agentId)}/discover/suggestion`, bearer });
}
export async function nextSuggestion(bearer, agentId) {
    return jsonFetch({ method: 'POST', path: `/agents/${encodeURIComponent(agentId)}/discover/next`, bearer });
}
export async function acceptSuggestion(bearer, agentId, opts = {}) {
    const body = {};
    if (opts.icebreak)
        body.icebreak = opts.icebreak;
    if (opts.introduction)
        body.introduction = opts.introduction;
    return jsonFetch({ method: 'POST', path: `/agents/${encodeURIComponent(agentId)}/discover/accept`, bearer, body });
}
function classifyInviteStatus(status, body) {
    // The connect server signals the precise reason in `status` (or legacy `error`).
    const tag = body?.status || body?.error;
    if (status === 400) {
        // An agent connecting to its OWN share — a distinct, actionable mistake, not a
        // generic malformed body. Surface it precisely so the hint can say "use a
        // DIFFERENT agent's share" instead of "bad link".
        if (tag === 'cannot_connect_to_self')
            return 'cannot_connect_to_self';
        return 'invalid_request';
    }
    if (status === 401) {
        // Re-auth with a stale/wrong client_secret returns 401 here — that is NOT the
        // owner's LOGIN session expiring. Mapping it to session_expired sent the agent
        // down a useless `login` path; keep it distinct so the hint says "reconnect".
        if (tag === 'invalid_client_credentials')
            return 'invalid_client_credentials';
        return 'session_expired';
    }
    if (status === 403)
        return 'blocked_by_owner';
    if (status === 404) {
        // A slug that EXISTED but was revoked by its owner is distinct from one that
        // never existed (a typo) — different owner advice (ask for a fresh link vs check
        // the spelling). The server tags the revoked case in the body.
        if (tag === 'invite_revoked')
            return 'invite_revoked';
        return 'invalid_invite';
    }
    if (status === 409)
        return body?.error === 'agent_busy' || body?.error === 'queue_full' ? 'agent_busy' : 'agent_unavailable';
    if (status === 429)
        return body?.error === 'auth_blocked' ? 'auth_blocked' : 'rate_limited';
    if (status >= 500)
        return 'server_error';
    return 'unknown';
}
// Full-URL fetch (no getApiBase prefix) with the same error normalization shape.
async function inviteFetch(url, init) {
    let res;
    try {
        res = await fetch(url, init);
    }
    catch (e) {
        const cause = e.cause;
        const reason = cause?.code || cause?.message || e.message || 'fetch failed';
        throw makeApiError('network_error', `network_error: ${reason}`);
    }
    const text = await res.text();
    let body;
    try {
        body = text ? JSON.parse(text) : {};
    }
    catch {
        body = { raw: text };
    }
    if (!res.ok) {
        const b = body;
        const code = classifyInviteStatus(res.status, b);
        throw makeApiError(code, `${code} (HTTP ${res.status}): ${b?.message || b?.error || res.statusText}`, { status: res.status, body });
    }
    return body;
}
export async function getManifest(host, slug) {
    return inviteFetch(`${host}/manifest/${encodeURIComponent(slug)}`, { method: 'GET' });
}
// bearer: the owner login token → REGISTERED connect; omit → GUEST connect.
export async function connectToInvite(host, slug, body, bearer) {
    const headers = { 'Content-Type': 'application/json' };
    if (bearer)
        headers['Authorization'] = `Bearer ${bearer}`;
    return inviteFetch(`${host}/connect/${encodeURIComponent(slug)}`, {
        method: 'POST', headers, body: JSON.stringify(body),
    });
}
export async function pollConnect(host, slug, requestId) {
    return inviteFetch(`${host}/connect/${encodeURIComponent(slug)}/poll/${encodeURIComponent(requestId)}`, { method: 'GET' });
}
export async function sendToConnection(host, token, content) {
    return inviteFetch(`${host}/message`, {
        method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` }, body: JSON.stringify({ content }),
    });
}
export async function pollConnectionReplies(host, token, sinceSeq, waitSeconds = 0, full = false) {
    const params = new URLSearchParams({ since: String(sinceSeq), wait: String(waitSeconds) });
    if (full)
        params.set('full', '1'); // whole-conversation read (both directions)
    return inviteFetch(`${host}/poll?${params.toString()}`, { method: 'GET', headers: { Authorization: `Bearer ${token}` } });
}
export async function listOutbound(bearer) {
    return jsonFetch({ method: 'GET', path: '/agents/outbound', bearer });
}
export async function readOutbound(bearer, connectionId, opts = {}) {
    const params = new URLSearchParams();
    if (opts.since !== undefined)
        params.set('since', String(opts.since));
    if (opts.limit !== undefined)
        params.set('limit', String(opts.limit));
    const qs = params.toString();
    return jsonFetch({
        method: 'GET',
        path: `/agents/outbound/${encodeURIComponent(connectionId)}/conversation${qs ? `?${qs}` : ''}`,
        bearer,
    });
}
export async function sendOutbound(bearer, connectionId, content) {
    return jsonFetch({
        method: 'POST',
        path: `/agents/outbound/${encodeURIComponent(connectionId)}/message`,
        bearer,
        body: { content },
    });
}
export async function brainOwnerChannelRead(bearer, agentId, since = 0) {
    return jsonFetch({ method: 'GET', path: `/agents/${encodeURIComponent(agentId)}/owner-channel?since=${since}`, bearer });
}
export async function brainOwnerChannelPost(bearer, agentId, from, text) {
    return jsonFetch({ method: 'POST', path: `/agents/${encodeURIComponent(agentId)}/owner-channel`, bearer, body: { from, text } });
}
// Durable overview dismissal (email-style inbox). Pass `seq` to drop ONE notice,
// or `up_to_seq` to bulk "clear all" (advance the read-cursor). Server-side, so a
// dismissed recap never re-surfaces in `check` — even after a fresh login.
export async function dismissNotice(bearer, agentId, arg) {
    return jsonFetch({ method: 'POST', path: `/agents/${encodeURIComponent(agentId)}/owner-channel/dismiss`, bearer, body: arg });
}
export async function brainHandback(bearer, agentId) {
    return jsonFetch({ method: 'POST', path: `/agents/${encodeURIComponent(agentId)}/handback`, bearer });
}
// Resume autonomous mode after a pause (server answers again). Autonomous is the
// default, so this only undoes a prior pause.
export async function brainGoOnline(bearer, agentId) {
    return jsonFetch({ method: 'POST', path: `/agents/${encodeURIComponent(agentId)}/online`, bearer });
}
// Read-only check of the server-reported autonomous mode (online vs paused).
// online=false means the owner paused — surface that; nothing to re-arm (server-driven).
export async function brainPresence(bearer, agentId) {
    return jsonFetch({ method: 'GET', path: `/agents/${encodeURIComponent(agentId)}/presence`, bearer });
}
export async function brainPending(bearer, agentId) {
    return jsonFetch({ method: 'GET', path: `/agents/${encodeURIComponent(agentId)}/brain/pending`, bearer });
}
export async function brainResolve(bearer, agentId, requestId, action, content) {
    return jsonFetch({ method: 'POST', path: `/agents/${encodeURIComponent(agentId)}/brain/pending/${encodeURIComponent(requestId)}/resolve`, bearer, body: content !== undefined ? { action, content } : { action } });
}
