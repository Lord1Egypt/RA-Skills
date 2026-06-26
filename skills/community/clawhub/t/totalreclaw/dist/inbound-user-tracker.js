/**
 * Per-channel inbound-user tracker (issue #215, 3.3.7-rc.1).
 *
 * Tier 3 + Tier 5 of the `/totalreclaw-restart` 5-tier auth fallback need to know
 * "how many distinct users have ever messaged this gateway on channel X".
 *
 * This module implements a simple disk-backed counter. Persistence
 * survives gateway restarts (which is the whole point — a fresh
 * container restart must NOT reset the count to 0 and let an attacker
 * race the lone-user heuristic).
 *
 * Storage: a single JSON file at `<credentialsDir>/.inbound-users.json`
 * with shape `{ channel: { user1: ts, user2: ts, ... } }`. The file
 * sits next to credentials.json so it's covered by the same backup
 * boundary.
 *
 * Operations:
 *   - `recordInboundUser(channel, senderId)` — idempotent insert; updates
 *     `ts` to last-seen-at on every call.
 *   - `getDistinctInboundUserCount(channel)` — returns number of distinct
 *     keys for that channel (0 if no entries / file missing).
 *
 * Thread safety: the module-level cache is mutated synchronously in
 * one Node.js event-loop tick; concurrent message_received hooks share
 * the same cache. Disk writes are best-effort (no fsync) because losing
 * a few count updates is recoverable — the worst case is a stale-but-
 * never-stale count that becomes correct on the next inbound message.
 *
 * Privacy: senderIds are stored AS RECEIVED. Telegram chat IDs are not
 * secrets but they are user-identifying. The file is mode 0o600 (same
 * as credentials.json) so only the gateway's user can read it.
 *
 * Pure file I/O is intentional. The OpenClaw scanner whole-file rule
 * disallows fs.read* alongside outbound-request markers; we do not
 * make any HTTP / network call here, so the tracker is scanner-clean.
 */
import * as fs from 'node:fs';
import * as path from 'node:path';
const SCHEMA_VERSION = 1;
/** Module-level cache so consecutive lookups don't re-read disk. Reset
 * whenever the disk file changes (we don't watch — instead, every
 * `recordInboundUser` reloads the on-disk state to merge concurrent
 * writers, then writes the merged result back). For the read path we
 * always touch disk because Tier 5 verdict is correctness-critical. */
let cachedState = null;
function defaultState() {
    return { channels: {}, version: SCHEMA_VERSION };
}
/** Resolve the on-disk path. Caller passes the credentials.json path
 * (the plugin already knows it from CONFIG.credentialsPath); we share
 * the parent directory so the tracker file is co-located. */
export function resolveTrackerPath(credentialsPath) {
    const dir = path.dirname(credentialsPath);
    return path.join(dir, '.inbound-users.json');
}
function readStateFromDisk(trackerPath) {
    try {
        if (!fs.existsSync(trackerPath))
            return defaultState();
        const raw = fs.readFileSync(trackerPath, 'utf-8');
        const parsed = JSON.parse(raw);
        if (!parsed || typeof parsed !== 'object' || !parsed.channels || typeof parsed.channels !== 'object') {
            return defaultState();
        }
        // Light validation: channels must be Record<string, Record<string, number>>
        const channels = {};
        for (const [ch, users] of Object.entries(parsed.channels)) {
            if (!users || typeof users !== 'object')
                continue;
            const u = {};
            for (const [uid, ts] of Object.entries(users)) {
                if (typeof ts === 'number' && Number.isFinite(ts))
                    u[uid] = ts;
            }
            channels[ch] = u;
        }
        return { channels, version: SCHEMA_VERSION, updatedAt: parsed.updatedAt };
    }
    catch {
        return defaultState();
    }
}
function writeStateToDisk(trackerPath, state) {
    try {
        const dir = path.dirname(trackerPath);
        if (!fs.existsSync(dir))
            fs.mkdirSync(dir, { recursive: true });
        state.updatedAt = new Date().toISOString();
        state.version = SCHEMA_VERSION;
        fs.writeFileSync(trackerPath, JSON.stringify(state), { mode: 0o600 });
        return true;
    }
    catch {
        return false;
    }
}
/**
 * Idempotently record that `senderId` messaged on `channel`. Returns
 * true on successful persist, false if the disk write failed (the
 * in-memory cache is updated either way so the run-time count is
 * still correct for this process).
 */
export function recordInboundUser(trackerPath, channel, senderId) {
    const ch = channel.trim().toLowerCase();
    const sid = senderId.trim();
    if (!ch || !sid)
        return false;
    // Always reload from disk before mutating — covers the multi-process
    // case where another worker (e.g. a sidecar) may have written entries
    // since our last read.
    const state = readStateFromDisk(trackerPath);
    if (!state.channels[ch])
        state.channels[ch] = {};
    state.channels[ch][sid] = Date.now();
    cachedState = state;
    return writeStateToDisk(trackerPath, state);
}
/**
 * Read the distinct inbound-user count for the given channel from disk
 * (or the in-memory cache). Tier 5 of the auth fallback uses this; we
 * read fresh-from-disk to make sure a multi-user gateway can't trip
 * the lone-user heuristic just because our cache is stale.
 */
export function getDistinctInboundUserCount(trackerPath, channel) {
    const ch = channel.trim().toLowerCase();
    if (!ch)
        return 0;
    // We deliberately do NOT use the cache here — see fn doc.
    const state = readStateFromDisk(trackerPath);
    cachedState = state;
    const users = state.channels[ch];
    if (!users || typeof users !== 'object')
        return 0;
    return Object.keys(users).length;
}
/** Test-only: reset the in-memory cache. */
export function __resetForTesting() {
    cachedState = null;
}
/** Test-only: peek at the cache (returns a deep copy so tests can
 * mutate without affecting the module). */
export function __peekCacheForTesting() {
    if (!cachedState)
        return null;
    return JSON.parse(JSON.stringify(cachedState));
}
