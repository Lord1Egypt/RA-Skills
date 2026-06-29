import { promises as fs, constants as fsConstants, readFileSync, readdirSync, existsSync } from 'node:fs';
import { homedir } from 'node:os';
import { join, dirname } from 'node:path';
// Owner-side state lives under ~/.siobac/. On a platform that runs MULTIPLE
// agents under one home, a single shared ~/.siobac/auth.json would let one
// agent's login OVERWRITE another's — silently re-binding it to the wrong
// account (and then it never sees its own connect requests / messages).
//
// PER-AGENT ISOLATION via a LOCAL BINDING FILE. Every agent platform runs its
// agents in their OWN working directory, so we scope state by a `.siobac.json`
// file in that working dir (found by walking cwd → up to $HOME). It holds only
// a NON-SECRET pointer { agent_key } — never tokens — and selects the private
// folder ~/.siobac/agents/<agent_key>/ where auth/agent/sessions live. `login`
// and `connect` auto-create the file on first use, so two agents in two working
// dirs get two folders and can never touch each other's login. An explicit
// SIOBAC_AGENT_KEY env var overrides the file; with NEITHER, we fall back to
// the shared ~/.siobac default (single-agent installs, unchanged).
//
// PERSISTENCE OVERRIDE (#16). Some platforms (e.g. Doubao) run the skill in an
// EPHEMERAL workspace that is wiped between runs — so a login written to
// ~/.siobac/auth.json is gone next run, forcing a re-login every time. If the
// platform exposes ANY directory that SURVIVES the wipe, point the state base
// at it with `SIOBAC_STATE_DIR=/that/persistent/path` and the login persists
// there instead of under the wiped home. Empty/unset → the normal ~/.siobac.
function resolveStateBase() {
    const override = (process.env.SIOBAC_STATE_DIR ?? process.env.OVOCLAW_STATE_DIR ?? '').trim();
    return override || join(homedir(), '.siobac');
}
export const STATE_BASE = resolveStateBase();
// Where state lived before the rename to Siobac (ovoclaw → siobac).
// migrateLegacyState() copies an existing login over on first run so users
// don't have to log in again after the rename.
export const LEGACY_STATE_BASE = join(homedir(), '.ovoclaw');
// The local per-working-directory pointer file (no secrets — just agent_key).
// Legacy `.ovoclaw.json` bindings are still honored (read-only) so existing
// working dirs don't lose their agent after the rename.
export const BINDING_FILENAME = '.siobac.json';
export const LEGACY_BINDING_FILENAME = '.ovoclaw.json';
function sanitizeKey(k) {
    return k.replace(/[^a-zA-Z0-9_.-]/g, '_').slice(0, 64);
}
// Nearest .siobac.json (or legacy .ovoclaw.json) carrying a usable agent_key,
// walking cwd up to $HOME. The new filename wins at each level; the legacy name
// is honored so existing bindings survive the rename.
function findBindingFile() {
    const home = homedir();
    let d = process.cwd();
    for (let i = 0; i < 40; i++) {
        for (const name of [BINDING_FILENAME, LEGACY_BINDING_FILENAME]) {
            const candidate = join(d, name);
            try {
                const parsed = JSON.parse(readFileSync(candidate, 'utf8'));
                const key = sanitizeKey(String(parsed?.agent_key ?? '').trim());
                if (key)
                    return { path: candidate, key };
            }
            catch { /* missing or malformed — try the next name / walk up */ }
        }
        if (d === home)
            break;
        const parent = dirname(d);
        if (parent === d)
            break;
        d = parent;
    }
    return null;
}
// FALLBACK when there's no env key and no .siobac.json binding: a command may run
// from a DIFFERENT working directory than `login` did, so the binding walk finds
// nothing and we'd otherwise read the EMPTY shared dir → a false "session expired"
// / re-login even though the login is fine, just saved under a per-agent folder. So
// auto-discover an existing login: if EXACTLY ONE ~/.siobac/agents/<key>/ holds an
// auth.json (logout deletes it, so this = exactly one logged-in agent), use that key.
// Zero or several (ambiguous) → caller's normal fallback; explicit env/binding always wins.
function findSingleLoggedInAgent() {
    try {
        const agentsDir = join(STATE_BASE, 'agents');
        if (!existsSync(agentsDir))
            return null;
        const keys = readdirSync(agentsDir, { withFileTypes: true })
            .filter((e) => e.isDirectory() && existsSync(join(agentsDir, e.name, 'auth.json')))
            .map((e) => e.name);
        return keys.length === 1 ? sanitizeKey(keys[0]) : null;
    }
    catch {
        return null;
    }
}
// Is there a login at the SHARED base (~/.siobac/auth.json)? That's the single-user home.
function sharedBaseHasAuth() {
    try {
        return existsSync(join(STATE_BASE, 'auth.json'));
    }
    catch {
        return false;
    }
}
// Once resolved (or created) within a process the key is PINNED, so every
// command in the same run reads/writes the SAME folder.
let _pinnedKey = null;
function resolveAgentKey() {
    if (_pinnedKey !== null)
        return _pinnedKey;
    const env = (process.env.SIOBAC_AGENT_KEY ?? process.env.OVOCLAW_AGENT_KEY ?? '').trim();
    if (env)
        return sanitizeKey(env);
    const bf = findBindingFile();
    if (bf)
        return bf.key;
    // UNBOUND = single-user mode → the SHARED ~/.siobac base (stable across cwds). Migration
    // bridge: if the shared base has no login yet but exactly one keyed login exists (minted
    // by an older build), use that one so the user isn't logged out.
    if (!sharedBaseHasAuth())
        return findSingleLoggedInAgent() ?? '';
    return '';
}
function stateDirFor(key) {
    return key ? join(STATE_BASE, 'agents', key) : STATE_BASE;
}
// State dir for the current run (env key > local binding file > shared default).
export function stateDir() { return stateDirFor(resolveAgentKey()); }
// The agent-state key resolved for THIS run. `login` records it in the pending
// handshake; `login --finish` pins it back so the token lands in the same
// per-agent folder even when finish runs from a different working directory.
export function resolvedAgentKey() { return resolveAgentKey(); }
export function pinAgentKey(key) { _pinnedKey = sanitizeKey(key); }
// Resolve the per-agent binding. Default is the SHARED ~/.siobac home (single-user);
// a per-agent folder is used ONLY when the platform opts in explicitly — SIOBAC_AGENT_KEY
// env, or a .siobac.json it created. `_create` is accepted for signature compatibility but
// no longer mints a folder (see the unbound branch).
export async function ensureAgentBinding(_create) {
    const env = (process.env.SIOBAC_AGENT_KEY ?? process.env.OVOCLAW_AGENT_KEY ?? '').trim();
    if (env) {
        const key = sanitizeKey(env);
        _pinnedKey = key;
        return { key, source: 'env', binding_file: null, state_dir: stateDirFor(key), created: false };
    }
    const found = findBindingFile();
    if (found) {
        _pinnedKey = found.key;
        return { key: found.key, source: 'local-file', binding_file: found.path, state_dir: stateDirFor(found.key), created: false };
    }
    // UNBOUND (no env, no .siobac.json) = SINGLE-USER mode → the SHARED ~/.siobac base.
    // We DON'T mint a per-cwd folder anymore: on a platform with an unstable/ephemeral cwd,
    // that made every `login` land in a NEW folder, so later commands (different cwd) couldn't
    // find the login → endless re-login churn (the "auth expired" loop). The shared base is
    // ONE stable home regardless of cwd. Multi-agent must opt in via SIOBAC_AGENT_KEY (or a
    // .siobac.json it creates). Migration bridge: if the shared base has no login yet but
    // exactly one keyed login exists (from an older build), reuse it — no forced re-login.
    if (!sharedBaseHasAuth()) {
        const single = findSingleLoggedInAgent();
        if (single) {
            _pinnedKey = single;
            return { key: single, source: 'auto-discovered', binding_file: null, state_dir: stateDirFor(single), created: false };
        }
    }
    _pinnedKey = '';
    return { key: '', source: 'default-shared', binding_file: null, state_dir: STATE_BASE, created: false };
}
// Lazy per-run paths — each resolves the keyed dir fresh (honoring a pinned key)
// so a binding created mid-run (by `login`) takes effect immediately.
function dir() { return stateDir(); }
function authFile() { return join(dir(), 'auth.json'); }
// A mirror of auth.json written on every save. If auth.json is later lost or
// corrupted (e.g. an interrupted write, or a clumsy skill update), loadAuth
// transparently restores from this backup — so the user keeps their login.
function authBackupFile() { return join(dir(), 'auth.json.bak'); }
// Which agent this skill last shared. Kept SEPARATE from auth.json so it
// survives logout / token expiry: on the next `login` we pass this id to the
// approval page as agent_hint, and it auto-confirms the same agent.
function agentFile() { return join(dir(), 'agent.json'); }
// Exposed for diagnostics (doctor) + logout messaging.
export function authFilePath() { return authFile(); }
async function ensureDir() {
    await fs.mkdir(dir(), { recursive: true, mode: 0o700 });
    try {
        await fs.chmod(dir(), 0o700);
    }
    catch { }
}
// Atomic write: temp file + rename (atomic on POSIX), so a reader never sees a
// half-written file and concurrent writers can't interleave bytes. Guards
// auth.json against corruption from an interrupted/parallel write — corruption
// there reads as "logged out" and forces a needless re-login.
async function writeFileAtomic(path, data) {
    const tmp = `${path}.tmp-${process.pid}-${Date.now()}`;
    await fs.writeFile(tmp, data, { mode: 0o600 });
    try {
        await fs.chmod(tmp, 0o600);
    }
    catch { }
    try {
        await fs.rename(tmp, path);
    }
    catch {
        await fs.writeFile(path, data, { mode: 0o600 });
        try {
            await fs.chmod(path, 0o600);
        }
        catch { }
        try {
            await fs.unlink(tmp);
        }
        catch { }
    }
}
// Read + validate an auth file. Returns null for missing (ENOENT) or corrupt /
// malformed contents; rethrows only unexpected fs errors (e.g. permissions).
async function readAuthFrom(path) {
    let raw;
    try {
        raw = await fs.readFile(path, 'utf8');
    }
    catch (e) {
        if (e.code === 'ENOENT')
            return null;
        throw e;
    }
    try {
        const parsed = JSON.parse(raw);
        if (typeof parsed === 'object' && parsed !== null && typeof parsed.accessToken === 'string') {
            return parsed;
        }
    }
    catch {
        // corrupt JSON — fall through to null so the caller can try the backup
    }
    return null;
}
export async function loadAuth() {
    const primary = await readAuthFrom(authFile());
    if (primary)
        return primary;
    // Primary missing or corrupt — recover from the backup and restore it so the
    // user stays logged in without re-running `login`.
    const backup = await readAuthFrom(authBackupFile());
    if (backup) {
        try {
            await saveAuth(backup);
        }
        catch { /* restore is best-effort */ }
        return backup;
    }
    return null;
}
export async function saveAuth(auth) {
    await ensureDir();
    const json = JSON.stringify(auth, null, 2);
    // Atomic so a refresh's rotated token always lands intact.
    await writeFileAtomic(authFile(), json);
    // Mirror to the backup so a lost/corrupt auth.json can self-heal on next load.
    try {
        await writeFileAtomic(authBackupFile(), json);
    }
    catch { /* backup is best-effort; never fail a login over it */ }
}
export async function clearAuth() {
    // Remove BOTH files — otherwise loadAuth would restore the login from the
    // backup and logout wouldn't stick.
    for (const f of [authFile(), authBackupFile()]) {
        try {
            await fs.unlink(f);
        }
        catch (e) {
            if (e.code !== 'ENOENT')
                throw e;
        }
    }
}
// Mark the bound agent's NAME as confirmed (idempotent; no-op if no binding yet).
// Called when the owner sets the name via `set-profile --name`, and on login --finish
// for an already-designed (non-new) agent so a fresh state dir on another machine
// doesn't re-prompt the name for an agent that's clearly already set up.
// `name`, when given, also refreshes the remembered display name (it goes stale when
// the profile is renamed, which made re-login pre-select / show the wrong name).
export async function markNameConfirmed(name) {
    const bound = await loadBoundAgent();
    if (!bound)
        return;
    const next = { ...bound };
    let changed = false;
    if (!bound.nameConfirmedAt) {
        next.nameConfirmedAt = new Date().toISOString();
        changed = true;
    }
    const trimmed = name?.trim();
    if (trimmed && bound.agentName !== trimmed) {
        next.agentName = trimmed;
        changed = true;
    }
    if (changed)
        await saveBoundAgent(next);
}
export async function loadBoundAgent() {
    try {
        const raw = await fs.readFile(agentFile(), 'utf8');
        const parsed = JSON.parse(raw);
        if (typeof parsed === 'object' && parsed !== null && typeof parsed.agentId === 'string') {
            return parsed;
        }
        return null;
    }
    catch (e) {
        if (e.code === 'ENOENT')
            return null;
        throw e;
    }
}
export async function saveBoundAgent(agent) {
    await ensureDir();
    const f = agentFile();
    await fs.writeFile(f, JSON.stringify(agent, null, 2), { mode: 0o600 });
    try {
        await fs.chmod(f, 0o600);
    }
    catch { }
}
// ── Pending device-flow login (two-step) ─────────────────────────────
// `login` requests a device code and stashes it here, then returns the
// approval URL immediately WITHOUT polling. `login --finish` — run only after
// the user says they approved — reads this back and polls once for the token.
// Kept in the SAME per-agent state dir so the finished token lands in the right
// folder. This is what stops the agent from silently looping `login`.
// A stable env-provided key isolates state AND is cwd-independent, so the pending
// handshake can live in the per-agent dir. WITHOUT one, the keyed dir comes from a
// cwd-relative .siobac.json that `login` and `login --finish` (separate processes)
// can resolve DIFFERENTLY if the host shifts cwd between calls — the pending would
// vanish and the agent would loop `login`. In that case park the transient
// handshake at the STABLE shared base where finish always finds it, and record the
// resolved agentKey inside so finish still writes auth.json to the right folder.
function hasStableEnvKey() {
    return !!(process.env.SIOBAC_AGENT_KEY ?? process.env.OVOCLAW_AGENT_KEY ?? '').trim();
}
function pendingLoginFile() {
    return hasStableEnvKey() ? join(dir(), 'login-pending.json') : join(STATE_BASE, 'login-pending.json');
}
export async function savePendingLogin(p) {
    const f = pendingLoginFile();
    await fs.mkdir(dirname(f), { recursive: true, mode: 0o700 });
    await fs.writeFile(f, JSON.stringify(p, null, 2), { mode: 0o600 });
    try {
        await fs.chmod(f, 0o600);
    }
    catch { }
}
export async function loadPendingLogin() {
    try {
        const raw = await fs.readFile(pendingLoginFile(), 'utf8');
        const parsed = JSON.parse(raw);
        if (typeof parsed === 'object' && parsed !== null && typeof parsed.deviceCode === 'string') {
            return parsed;
        }
        return null;
    }
    catch (e) {
        if (e.code === 'ENOENT')
            return null;
        throw e;
    }
}
export async function clearPendingLogin() {
    try {
        await fs.unlink(pendingLoginFile());
    }
    catch (e) {
        if (e.code !== 'ENOENT')
            throw e;
    }
}
// ── Login-mint lock ──────────────────────────────────────────────────────────
// The pending-login guard (load → mint → save) has a TOCTOU window: if a second
// `login` runs after the first's load but before its save, BOTH mint a device
// code, and the second's save OVERWRITES the first's record — orphaning one code
// and leaving the user with two links (the "fail to login" we saw in prod). This
// lock makes the claim atomic: it's acquired with O_EXCL BEFORE the network mint
// and released after the pending record is written, so a concurrent `login` sees
// the claim and reuses the in-flight link instead of minting a rival code. It
// lives next to the pending file so its scope matches (shared base when unbound,
// per-agent folder under a stable env key).
function loginLockFile() {
    return pendingLoginFile() + '.lock';
}
// Returns true if WE claimed the lock; false if a FRESH claim is already held by
// a concurrent login. A stale claim (older than ttlMs — a mint that never
// finished) is taken over so a crashed login can't wedge the flow forever.
export async function claimLoginLock(ttlMs = 60_000) {
    const f = loginLockFile();
    await fs.mkdir(dirname(f), { recursive: true, mode: 0o700 });
    try {
        const fh = await fs.open(f, 'wx', 0o600); // O_EXCL — fails if it already exists
        try {
            await fh.writeFile(String(Date.now()));
        }
        finally {
            await fh.close();
        }
        return true;
    }
    catch (e) {
        if (e.code !== 'EEXIST')
            throw e;
        let fresh = false;
        try {
            const ts = parseInt(await fs.readFile(f, 'utf8'), 10);
            fresh = Number.isFinite(ts) && Date.now() - ts < ttlMs;
        }
        catch { /* unreadable → treat as stale and take over */ }
        if (fresh)
            return false;
        await fs.writeFile(f, String(Date.now()), { mode: 0o600 }); // take over the stale lock
        return true;
    }
}
export async function releaseLoginLock() {
    try {
        await fs.unlink(loginLockFile());
    }
    catch (e) {
        if (e.code !== 'ENOENT')
            throw e;
    }
}
// ── Discovery: consecutive-skip counter ─────────────────────────────────
// Counts how many times in a row the owner hit `discover --next` (skip). When the
// owner skips repeatedly it usually means the recommendations aren't landing — NOT
// that they want to page to the end — so at a threshold the discover flow pauses to
// check satisfaction and refine the purpose instead of serving yet another card. Any
// other discovery action (viewing a match, refining the purpose, connecting, off)
// RESETS it. Lives in the per-agent state dir; on an ephemeral host it just resets
// after a recycle, which is harmless (the streak is a within-session signal anyway).
function discoverSkipsFile() { return join(dir(), 'discover-skips.json'); }
export async function bumpDiscoverSkips() {
    let count = 0;
    try {
        const raw = await fs.readFile(discoverSkipsFile(), 'utf8');
        const n = JSON.parse(raw)?.count;
        if (typeof n === 'number' && n >= 0)
            count = n;
    }
    catch { /* missing/corrupt — start from 0 */ }
    count += 1;
    try {
        await ensureDir();
        await fs.writeFile(discoverSkipsFile(), JSON.stringify({ count }), { mode: 0o600 });
    }
    catch { /* best-effort — the streak signal is non-critical */ }
    return count;
}
export async function resetDiscoverSkips() {
    try {
        await fs.unlink(discoverSkipsFile());
    }
    catch (e) {
        if (e.code !== 'ENOENT') { /* ignore — non-critical */ }
    }
}
export async function isAuthFileWriteable() {
    try {
        await ensureDir();
        await fs.access(dir(), fsConstants.W_OK);
        return { ok: true };
    }
    catch (e) {
        return { ok: false, reason: e.message };
    }
}
// ── Reach-out sessions: REMOVED ──────────────────────────────────────────
// Reach-out (outbound) conversations used to be stored here as local sessions
// (a per-connection xext_ bearer + client_secret in sessions.json). Login-only
// made that vestigial: outbound conversations are now served server-side under
// the owner's OAuth login, keyed by connection_id (see agents/outbound.service on
// the server, and api.listOutbound/readOutbound/sendOutbound). No local session
// state, no rotating token, no silent reauth — which removes the false
// "session/conversation expired" churn. Legacy sessions.json (if present) is left
// untouched; it's simply no longer read, and is cleaned up with the rest of the
// state dir on logout/clear.
// One-time migration after the ovoclaw → siobac rename: if the new ~/.siobac
// state dir has no auth yet but the legacy ~/.ovoclaw equivalent does, copy the
// login (auth/agent/sessions) over so the user stays logged in (no re-login
// after the rename). No-op once migrated, for fresh users, or nothing to copy.
export async function migrateLegacyState() {
    const target = dir();
    try {
        await fs.access(authFile());
        return;
    }
    catch { /* new dir has no auth — maybe migrate */ }
    const legacyDir = target.replace(STATE_BASE, LEGACY_STATE_BASE);
    if (legacyDir === target)
        return;
    try {
        await fs.access(join(legacyDir, 'auth.json'));
    }
    catch {
        return;
    } // nothing legacy
    await fs.mkdir(target, { recursive: true, mode: 0o700 });
    try {
        await fs.chmod(target, 0o700);
    }
    catch { }
    for (const f of ['auth.json', 'auth.json.bak', 'agent.json', 'sessions.json']) {
        try {
            const buf = await fs.readFile(join(legacyDir, f));
            await fs.writeFile(join(target, f), buf, { mode: 0o600 });
            try {
                await fs.chmod(join(target, f), 0o600);
            }
            catch { }
        }
        catch { /* that file didn't exist in legacy — skip */ }
    }
}
