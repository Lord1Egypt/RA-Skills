/**
 * Turning a configuration into OpenClaw cron jobs.
 *
 * OpenClaw's skill manifest has no way to declare a schedule: the complete set
 * of `metadata.openclaw` fields is `always`, `emoji`, `homepage`, `os`,
 * `requires`, `primaryEnv` and `install`, and none of them schedules anything.
 * Scheduling is `openclaw cron`, which is a separate, imperative step.
 *
 * So this command prints the exact commands, and `--apply` runs them. Printing is
 * the default because creating background jobs that message somebody is not
 * something a tool should do as a side effect of being asked what it would do.
 *
 * Three details here are load-bearing, and all three were established against a
 * live OpenClaw 2026.7.1-2:
 *
 * - `--command` is the payload kind whose **stdout is delivered** by
 *   `--announce`. That is the whole notification mechanism.
 * - An absolute path to `lib/cli.js` is embedded, because a cron job runs with
 *   the gateway's working directory and PATH, neither of which is the skill's.
 * - `--timeout-seconds` is set explicitly. The default is 30 seconds, and one
 *   watch allowed two ten-second attempts with a ten-second pause between them
 *   already reaches exactly that, so the default would kill real rounds.
 */
import { type Streams } from "../cli/render.js";
import type { Config } from "../config.js";
/** One cron job this configuration calls for. */
export type PlannedJob = {
    /** The `--name`, and the identity `--apply` looks for before creating it. */
    name: string;
    /** Which module asked for it, for the printed explanation. */
    module: "uptime" | "vercel-errors" | "vercel-budget" | "ga4-digest";
    /** The `web-observer` subcommand the job runs. */
    command: string;
    /** Either an `--every` duration or a `--cron` expression. */
    schedule: {
        kind: "every";
        value: string;
    } | {
        kind: "cron";
        value: string;
    };
    timeoutSeconds: number;
    why: string;
};
/**
 * Quote a string for `sh -lc`.
 *
 * Single quotes, with any embedded single quote closed and reopened. A skill can
 * be installed under a path with a space in it, and an unquoted path would then
 * be two arguments.
 */
export declare function shellQuote(value: string): string;
/** "1 minute", "5 minutes": a count with its noun agreeing. */
export declare function plural(count: number, noun: string): string;
/**
 * Every job the configuration calls for, in a stable order.
 *
 * A module that is switched off contributes nothing, which is what makes the
 * three modules independently installable: someone using uptime alone gets one
 * job and is never asked about a Vercel token.
 */
export declare function plannedJobs(config: Config): PlannedJob[];
/**
 * The `openclaw cron add` argument vector for one job.
 *
 * Returned as a vector rather than a string so `--apply` can spawn it without a
 * shell. The printed form is the same vector, quoted.
 */
export declare function cronAddArgv(job: PlannedJob, config: Config, cliPath: string): string[];
export type ScheduleDeps = {
    /** Runs `openclaw` with an argument vector. No shell. */
    runOpenclaw: (argv: readonly string[]) => Promise<{
        code: number;
        stdout: string;
        stderr: string;
    }>;
    /** Names of cron jobs that already exist. */
    existingJobNames: () => Promise<string[]>;
};
export declare function runScheduleCommand(context: {
    config: Config;
    configFile: string;
    streams: Streams;
    cliPath: string;
}, options: {
    apply: boolean;
    json: boolean;
}, deps: ScheduleDeps): Promise<number>;
