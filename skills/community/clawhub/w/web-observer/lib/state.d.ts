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
/** What one watch's history amounts to. */
export type WatchState = {
    consecutiveFailures: number;
    consecutiveSuccesses: number;
    /** Whether a down alert has been sent and no recovery message has followed. */
    down: boolean;
    /** When the current run of failures began, for the recovery message. */
    firstFailureAtMs: number | null;
    lastCheckAtMs: number | null;
    /** When this watch next comes due. Null means "never checked, check now". */
    nextDueAtMs: number | null;
    /** The last failure reason, for a status table. */
    lastReason: string | null;
};
/**
 * A poller's memory of which items it has already reported.
 *
 * Ids are kept with the time they were seen so the set can be pruned by age
 * rather than growing without limit.
 */
export type SeenIds = Record<string, number>;
export type VercelWatchState = {
    /** Request ids already reported, so an overlapping window cannot re-alert. */
    seenRequestIds: SeenIds;
    /** Whether an error alert is outstanding. */
    alerting: boolean;
    lastPollAtMs: number | null;
    /** Whether a monitor-side failure (not a site failure) is outstanding. */
    failing: boolean;
    /** Whether a budget alert is outstanding. */
    budgetAlerting: boolean;
    lastBudgetPollAtMs: number | null;
};
export type State = {
    version: 1;
    watches: Record<string, WatchState>;
    /**
     * One entry per Vercel project, keyed by the name in the configuration.
     *
     * Releases before multi-project support kept a single unkeyed object here.
     * That is read back under {@link LEGACY_VERCEL_KEY} and handed to the first
     * configured project by {@link vercelStateOf}, so an upgrade neither repeats
     * an alert nor forgets an outstanding one.
     */
    vercel: Record<string, VercelWatchState>;
};
/**
 * Where a pre-multi-project Vercel state is parked until a project claims it.
 * Parentheses and a space cannot occur in a Vercel project name or id.
 */
export declare const LEGACY_VERCEL_KEY = "(single project)";
export declare function freshWatchState(): WatchState;
export declare function freshVercelState(): VercelWatchState;
export declare function freshState(): State;
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
export declare function parseState(document: unknown): State;
/**
 * The Vercel state for one project, creating a blank one on first sight.
 *
 * @param first Whether this is the first configured project, the one that
 *   inherits a state written before projects were keyed.
 */
export declare function vercelStateOf(state: State, project: string, first: boolean): VercelWatchState;
/** The state for one watch, creating a blank one on first sight. */
export declare function watchStateOf(state: State, id: string): WatchState;
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
export declare function pruneSeenIds(seen: SeenIds, nowMs: number, keepMs: number, cap?: number): SeenIds;
/** Read state from disk, returning a blank one when it is absent or unreadable. */
export declare function loadState(file: string): State;
/**
 * Write state atomically: temporary file in the same directory, then rename.
 *
 * Same directory matters, because rename is only atomic within a filesystem.
 * The temporary name carries the process id so two runs cannot collide on it.
 */
export declare function saveState(file: string, state: State): void;
