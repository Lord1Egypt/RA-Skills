/**
 * The scheduled Vercel poll: error logs, and the performance budget.
 *
 * Two watches share one command because two cron jobs call it, each on its own
 * interval, and each run does whichever parts are due. That keeps the alert-once
 * and recover-once rules in one place, and it means an error poll and a budget
 * check never disagree about what has already been reported.
 *
 * The three decisions worth knowing about:
 *
 * **The window widens to cover a gap.** Each poll asks for `windowMinutes`, or
 * for however long it has been since the last successful poll plus the
 * configured overlap, whichever is longer. If the Gateway was off for two hours,
 * the next poll looks back over those two hours instead of the usual twenty
 * minutes. This is safe only because the end of the window is never specified:
 * a window ending in the past is refused by the API with HTTP 400, while any
 * `--since` with the end left at now succeeds. Both facts were measured.
 *
 * **Deduplication is by request id.** Overlapping windows re-report the same
 * errors by construction, so an id already alerted about is not alerted about
 * again. That is what makes the overlap free.
 *
 * **An empty answer is not proof of health.** Runtime logs are retained for one
 * hour on Hobby, so a window longer than that can come back empty because the
 * logs aged out. The underlying skill says so in its notes, and those notes are
 * passed on rather than dropped.
 */
import { type Streams } from "../cli/render.js";
import type { Config } from "../config.js";
import type { Env } from "../paths.js";
import { type State } from "../state.js";
import { type ErrorsPayload, type SafeErrorEntry, type VercelStatus } from "../bridge/vercel.js";
import type { CredentialResult } from "../bridge/credentials.js";
import type { RunResult } from "../bridge/delegate.js";
/** The longest window one poll will ask for. */
export declare const MAX_WINDOW_MINUTES = 1440;
export type VercelWatchContext = {
    config: Config;
    configFile: string;
    stateFile: string;
    streams: Streams;
    env: Env;
    now: () => number;
};
export type VercelWatchDeps = {
    /** Runs the delegated skill. Injected so tests need no Python. */
    invoke: (argv: readonly string[]) => Promise<RunResult>;
    status: VercelStatus;
    credentials: CredentialResult;
};
/**
 * How far back this poll should look.
 *
 * @param windowMinutes The configured window.
 * @param intervalMinutes The configured interval; the difference between the two
 *   is the overlap the user asked for.
 * @param sinceLastPollMinutes Minutes since the last successful poll, or null
 *   when there has never been one.
 * @returns Minutes to ask for, never below the configured window and never above
 *   {@link MAX_WINDOW_MINUTES}.
 */
export declare function windowFor(windowMinutes: number, intervalMinutes: number, sinceLastPollMinutes: number | null): number;
/** Split a poll's entries into those already reported and those not. */
export declare function partitionNew(entries: readonly SafeErrorEntry[], seen: Readonly<Record<string, number>>): {
    fresh: SafeErrorEntry[];
    repeated: number;
    withoutId: number;
};
/** How many distinct errors an alert lists before summarising the rest. */
export declare const MAX_GROUPS = 5;
/**
 * The alert text for a batch of new errors.
 *
 * Leads with the project and its domain, so the reader knows which site it is
 * before anything else, then lists each distinct error once with how often it
 * happened, where, and with what outcome. A flood of one error therefore reads
 * as one line with a count, not as a pile of routes.
 */
export declare function formatErrorAlert(project: string, fresh: readonly SafeErrorEntry[], payload: ErrorsPayload, windowMinutes: number, includeMessages: boolean, atMs: number): string;
/**
 * Run whichever parts of the Vercel watch are due.
 *
 * @returns The exit code, and the message that was printed.
 */
export declare function runVercelWatch(context: VercelWatchContext, deps: VercelWatchDeps, options: {
    dryRun: boolean;
}): Promise<{
    code: number;
    message: string;
    state: State;
}>;
