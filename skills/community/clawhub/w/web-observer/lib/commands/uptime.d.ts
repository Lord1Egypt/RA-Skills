/**
 * The two uptime commands: `check` and `watch`.
 *
 * They run the same round and differ in three ways. `check` ignores the
 * schedule, prints a table of everything it found, and never changes whether a
 * site is considered down. `watch` runs only what is due, prints an alert or
 * nothing at all, and persists what it learned.
 *
 * `--dry-run` deserves its own note. On a scheduled run, printing to stdout *is*
 * sending: cron delivers stdout to the chat. So a dry run cannot simply "not
 * send" while still printing the message. It writes the message it would have
 * delivered to **stderr**, where cron records it in the run log without
 * delivering it, and prints the silent token to stdout. State is left untouched,
 * so a dry run can be repeated and cannot consume the one alert an outage gets.
 */
import { type Streams } from "../cli/render.js";
import type { Config } from "../config.js";
import { type State } from "../state.js";
import type { CheckDeps } from "../uptime/check.js";
export type CommandContext = {
    config: Config;
    configFile: string;
    stateFile: string;
    streams: Streams;
    deps: CheckDeps;
};
/** `check`: run everything once and report, without changing any alert state. */
export declare function runCheckCommand(context: CommandContext, options: {
    json: boolean;
    strict: boolean;
    only: readonly string[];
    dryRun: boolean;
}): Promise<number>;
/** `watch`: the scheduled round. Alerts on a change, otherwise says nothing. */
export declare function runWatchCommand(context: CommandContext, options: {
    dryRun: boolean;
}): Promise<number>;
/**
 * Write state, reporting a failure to stderr rather than throwing.
 *
 * A state file that cannot be written is a real problem worth naming, and it is
 * not a reason to discard an alert that has already been formatted: the next run
 * will re-alert, which is the right way to fail here.
 */
export declare function persist(context: CommandContext, state: State): void;
