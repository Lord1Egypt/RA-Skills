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
import { allowlistOf } from "../config.js";
import { freshWatchState, watchStateOf } from "../state.js";
import { performCheck } from "./check.js";
import { applyResult, dueToleranceMs, isDue } from "./decide.js";
/** How many checks are in flight at once. */
export const CONCURRENCY = 4;
/**
 * The longest a round can take, in milliseconds.
 *
 * Used to set an explicit timeout on the generated cron job. A job killed
 * halfway through a round would leave some watches unchecked while looking, in
 * the run log, like a job that failed for its own reasons.
 */
export function worstCaseRoundMs(watches) {
    const perWatch = watches
        .filter((watch) => watch.enabled)
        .map((watch) => watch.attempts * watch.timeoutMs + (watch.attempts - 1) * watch.retryDelayMs);
    if (perWatch.length === 0)
        return 0;
    // Ceiling rather than maximum: with a concurrency limit, a long queue of slow
    // watches still has to drain in batches.
    const batches = Math.ceil(perWatch.length / CONCURRENCY);
    const slowest = Math.max(...perWatch);
    return batches * slowest;
}
/** Run `tasks` with at most `limit` in flight, preserving input order. */
async function mapWithLimit(items, limit, run) {
    const results = new Array(items.length);
    let next = 0;
    const workers = Array.from({ length: Math.min(limit, items.length) }, async () => {
        for (;;) {
            const index = next;
            next += 1;
            if (index >= items.length)
                return;
            results[index] = await run(items[index], index);
        }
    });
    await Promise.all(workers);
    return results;
}
/**
 * Check the watches that are due and fold the outcomes into state.
 *
 * @param config The whole configuration; only `uptime` is read.
 * @param state State as loaded. Not mutated: a new state is returned.
 * @param deps Injected clock, sleep and fetch.
 * @param options Which watches to run.
 * @returns The outcomes, the events, and the new state.
 */
export async function runRound(config, state, deps, options) {
    const allowlist = allowlistOf(config.uptime.watches);
    const requested = options.only.length === 0
        ? config.uptime.watches
        : config.uptime.watches.filter((watch) => options.only.includes(watch.id));
    const runnable = [];
    const skipped = [];
    for (const watch of requested) {
        // A disabled watch is skipped even when named explicitly: `enabled: false`
        // is a statement about the watch, not a default to be overridden by asking.
        if (!watch.enabled) {
            skipped.push(watch);
            continue;
        }
        if (options.ignoreSchedule ||
            isDue(watchStateOf(state, watch.id), deps.now(), dueToleranceMs(config.uptime.tickMinutes))) {
            runnable.push(watch);
        }
        else {
            skipped.push(watch);
        }
    }
    const results = await mapWithLimit(runnable, CONCURRENCY, (watch) => performCheck(watch, allowlist, deps));
    const watches = { ...state.watches };
    const events = [];
    const outcomes = [];
    runnable.forEach((watch, index) => {
        const result = results[index];
        outcomes.push({ watch, result });
        // The completion time is read once per watch, after its own check, so a
        // long round does not stamp every watch with the moment the round started.
        const applied = applyResult(watch, watches[watch.id] ?? freshWatchState(), result, deps.now());
        watches[watch.id] = applied.state;
        if (applied.event)
            events.push(applied.event);
    });
    return { outcomes, events, state: { ...state, watches }, skipped };
}
