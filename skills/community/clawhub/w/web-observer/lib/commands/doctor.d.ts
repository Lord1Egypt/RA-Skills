/**
 * `doctor`: what is wrong, and the one thing to do next.
 *
 * Two audiences, two shapes. The checklist is for a person in a terminal and
 * lists everything. `--json` is for an agent walking somebody through setup, and
 * names exactly one next step: somebody handed five simultaneous problems does
 * nothing, somebody handed one does it.
 *
 * Ordering is by what blocks what. There is no point advising somebody to install
 * the Vercel skill while their configuration file does not parse.
 */
import { type Streams } from "../cli/render.js";
import type { Config } from "../config.js";
import type { Env } from "../paths.js";
/** What is stopping Web Observer, as a machine-readable value. */
export type BlockedOn = "ok" | "no_config" | "bad_config" | "nothing_enabled" | "no_watches" | "no_notify_target" | "no_cron_jobs" | "vercel_skill_missing" | "vercel_logs_missing" | "vercel_credentials" | "ga4_skill_missing" | "ga4_credentials" | "interval_shorter_than_tick";
export declare const BLOCKED_ON_VALUES: readonly BlockedOn[];
export type Finding = {
    /** Short label for the checklist. */
    check: string;
    ok: boolean;
    /** Whether this stops something working, as opposed to being worth knowing. */
    blocking: boolean;
    detail: string;
    blockedOn?: BlockedOn;
};
export type DoctorReport = {
    ok: boolean;
    blocked_on: BlockedOn;
    next: string | null;
    configFile: string;
    stateFile: string;
    findings: Finding[];
};
export type DoctorInput = {
    config: Config | null;
    /** The error from loading the configuration, when it failed. */
    configError: string | null;
    configFile: string;
    configExists: boolean;
    stateFile: string;
    env: Env;
    /** Names of existing cron jobs, or null when they could not be listed. */
    cronJobNames: string[] | null;
};
/**
 * Examine everything and produce findings in blocking order.
 *
 * Pure, so the whole diagnosis is testable without a filesystem: the inputs are
 * gathered by the caller.
 */
export declare function diagnose(input: DoctorInput): DoctorReport;
/** Render a report, and return the exit code it implies. */
export declare function renderDoctor(report: DoctorReport, streams: Streams, options: {
    json: boolean;
}): number;
