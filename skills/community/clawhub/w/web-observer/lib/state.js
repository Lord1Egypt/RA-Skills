/**
 * Durable state, and the atomic write that keeps it trustworthy.
 *
 * State exists for exactly one reason: to know, across separate runs, whether a
 * URL was already reported as down. Without it every failed check would alert
 * again, which is the behaviour that teaches people to mute a monitor.
 *
 * It is therefore written atomically, to a temporary file in the same directory
 * followed by a rename. A partially written file would fail to parse on the next
 * run, be treated as absent, and re-alert everything that was already down: the
 * exact failure state is designed to prevent.
 */
import { mkdirSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import path from "node:path";
/**
 * Where a pre-multi-project Vercel state is parked until a project claims it.
 * Parentheses and a space cannot occur in a Vercel project name or id.
 */
export const LEGACY_VERCEL_KEY = "(single project)";
export function freshWatchState() {
    return {
        consecutiveFailures: 0,
        consecutiveSuccesses: 0,
        down: false,
        firstFailureAtMs: null,
        lastCheckAtMs: null,
        nextDueAtMs: null,
        lastReason: null,
    };
}
export function freshVercelState() {
    return {
        seenRequestIds: {},
        alerting: false,
        lastPollAtMs: null,
        failing: false,
        budgetAlerting: false,
        lastBudgetPollAtMs: null,
    };
}
export function freshState() {
    return { version: 1, watches: {}, vercel: {} };
}
function readNumberOrNull(value) {
    return typeof value === "number" && Number.isFinite(value) ? value : null;
}
function readCount(value) {
    return typeof value === "number" && Number.isFinite(value) && value >= 0 ? Math.floor(value) : 0;
}
/**
 * Rebuild state from a decoded document, defaulting anything unreadable.
 *
 * Deliberately forgiving, and the opposite of how configuration is treated. A
 * configuration file is written by a person and a surprise in it is a mistake
 * worth reporting; this file is written by this program, and the only thing to
 * do with a corrupt field is carry on from a sane value. Refusing to run
 * because the state file is odd would turn a bookkeeping problem into an
 * outage in the monitoring.
 *
 * The one field that matters to preserve exactly is `down`: getting it wrong in
 * either direction either re-alerts or stays silent about a real outage.
 */
export function parseState(document) {
    if (typeof document !== "object" || document === null || Array.isArray(document)) {
        return freshState();
    }
    const object = document;
    const state = freshState();
    const watches = object["watches"];
    if (typeof watches === "object" && watches !== null && !Array.isArray(watches)) {
        for (const [id, raw] of Object.entries(watches)) {
            if (typeof raw !== "object" || raw === null || Array.isArray(raw))
                continue;
            const entry = raw;
            state.watches[id] = {
                consecutiveFailures: readCount(entry["consecutiveFailures"]),
                consecutiveSuccesses: readCount(entry["consecutiveSuccesses"]),
                down: entry["down"] === true,
                firstFailureAtMs: readNumberOrNull(entry["firstFailureAtMs"]),
                lastCheckAtMs: readNumberOrNull(entry["lastCheckAtMs"]),
                nextDueAtMs: readNumberOrNull(entry["nextDueAtMs"]),
                lastReason: typeof entry["lastReason"] === "string" ? entry["lastReason"] : null,
            };
        }
    }
    const vercel = object["vercel"];
    if (typeof vercel === "object" && vercel !== null && !Array.isArray(vercel)) {
        const entries = vercel;
        if ("seenRequestIds" in entries || "lastPollAtMs" in entries) {
            state.vercel[LEGACY_VERCEL_KEY] = parseVercelState(entries);
        }
        else {
            for (const [project, raw] of Object.entries(entries)) {
                if (typeof raw !== "object" || raw === null || Array.isArray(raw))
                    continue;
                state.vercel[project] = parseVercelState(raw);
            }
        }
    }
    return state;
}
function parseVercelState(entry) {
    const seen = {};
    const rawSeen = entry["seenRequestIds"];
    if (typeof rawSeen === "object" && rawSeen !== null && !Array.isArray(rawSeen)) {
        for (const [id, at] of Object.entries(rawSeen)) {
            const stamp = readNumberOrNull(at);
            if (stamp !== null)
                seen[id] = stamp;
        }
    }
    return {
        seenRequestIds: seen,
        alerting: entry["alerting"] === true,
        lastPollAtMs: readNumberOrNull(entry["lastPollAtMs"]),
        failing: entry["failing"] === true,
        budgetAlerting: entry["budgetAlerting"] === true,
        lastBudgetPollAtMs: readNumberOrNull(entry["lastBudgetPollAtMs"]),
    };
}
/**
 * The Vercel state for one project, creating a blank one on first sight.
 *
 * @param first Whether this is the first configured project, the one that
 *   inherits a state written before projects were keyed.
 */
export function vercelStateOf(state, project, first) {
    return (state.vercel[project] ??
        (first ? state.vercel[LEGACY_VERCEL_KEY] : undefined) ??
        freshVercelState());
}
/** The state for one watch, creating a blank one on first sight. */
export function watchStateOf(state, id) {
    return state.watches[id] ?? freshWatchState();
}
/**
 * Forget request ids older than `keepMs`.
 *
 * The seen set exists to stop an overlapping poll window re-alerting the same
 * error. An id older than the window can never appear again, so keeping it
 * would grow the file without bound.
 *
 * @param cap Hard ceiling on entries, applied after the age prune. A window
 *   wide enough to hold more errors than this is a flood, and forgetting the
 *   oldest of them risks one duplicate alert rather than an unbounded file.
 */
export function pruneSeenIds(seen, nowMs, keepMs, cap = 5_000) {
    const kept = Object.entries(seen).filter(([, at]) => nowMs - at <= keepMs);
    if (kept.length > cap) {
        kept.sort((a, b) => b[1] - a[1]);
        kept.length = cap;
    }
    return Object.fromEntries(kept);
}
/** Read state from disk, returning a blank one when it is absent or unreadable. */
export function loadState(file) {
    let text;
    try {
        text = readFileSync(file, "utf8");
    }
    catch {
        return freshState();
    }
    try {
        return parseState(JSON.parse(text));
    }
    catch {
        // Unparseable is treated as absent, and deliberately not reported as an
        // error: see parseState. The cost is one repeated alert, once.
        return freshState();
    }
}
/**
 * Write state atomically: temporary file in the same directory, then rename.
 *
 * Same directory matters, because rename is only atomic within a filesystem.
 * The temporary name carries the process id so two runs cannot collide on it.
 */
export function saveState(file, state) {
    mkdirSync(path.dirname(file), { recursive: true });
    const temporary = `${file}.${process.pid}.tmp`;
    writeFileSync(temporary, `${JSON.stringify(state, null, 2)}\n`, { mode: 0o600 });
    renameSync(temporary, file);
}
