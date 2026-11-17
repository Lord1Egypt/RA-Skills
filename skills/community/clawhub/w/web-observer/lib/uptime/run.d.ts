/**
 * Running a round of checks.
 *
 * Ties the pure decision logic to the network and the state file, and nothing
 * more: the rules live in decide.ts, the requests in check.ts, the wording in
 * format.ts. What this module owns is which watches run, in what order, and what
 * is persisted afterwards.
 *
 * Checks run concurrently, with a small limit. Sequentially, a dozen watches
 * each allowed two ten-second attempts and a pause between them could take six
 * minutes, and a cron command job's default timeout is thirty seconds. Running
 * them together makes the round cost roughly one watch's worst case rather than
 * the sum of all of them.
 */
import type { Config, Watch } from "../config.js";
import { type State } from "../state.js";
import { type CheckDeps } from "./check.js";
import { type CheckResult, type UptimeEvent } from "./decide.js";
/** How many checks are in flight at once. */
export declare const CONCURRENCY = 4;
export type RunOptions = {
    /**
     * Check every enabled watch regardless of when it is next due.
     *
     * What `check` uses: somebody verifying a configuration should not be told to
     * wait four minutes.
     */
    ignoreSchedule: boolean;
    /** Limit the round to these watch ids. Empty means every watch. */
    only: readonly string[];
};
export type WatchOutcome = {
    watch: Watch;
    result: CheckResult;
};
export type RunOutcome = {
    /** Every check that ran, in configuration order. */
    outcomes: WatchOutcome[];
    /** Events worth telling somebody about. */
    events: UptimeEvent[];
    /** The state after the round. The caller decides whether to persist it. */
    state: State;
    /** Watches that were skipped because they were not yet due. */
    skipped: Watch[];
};
/**
 * The longest a round can take, in milliseconds.
 *
 * Used to set an explicit timeout on the generated cron job. A job killed
 * halfway through a round would leave some watches unchecked while looking, in
 * the run log, like a job that failed for its own reasons.
 */
export declare function worstCaseRoundMs(watches: readonly Watch[]): number;
/**
 * Check the watches that are due and fold the outcomes into state.
 *
 * @param config The whole configuration; only `uptime` is read.
 * @param state State as loaded. Not mutated: a new state is returned.
 * @param deps Injected clock, sleep and fetch.
 * @param options Which watches to run.
 * @returns The outcomes, the events, and the new state.
 */
export declare function runRound(config: Config, state: State, deps: CheckDeps, options: RunOptions): Promise<RunOutcome>;
