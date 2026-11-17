/**
 * The Vercel bridge: everything Web Observer knows about `openclaw-vercel-insights`.
 *
 * Nothing about Vercel is reimplemented here. This module locates that skill,
 * decides whether the copy installed is new enough to answer questions about
 * error logs, runs it, and converts what it returns into a shape that is safe to
 * deliver into a chat.
 *
 * ## The pin
 *
 * Request-log support lives on the `logs-surface` branch, which is version 1.1.0
 * and is expected to merge to `main`. Everything about that pin is in this file
 * and in README.md, and switching to a merged `main` or a tagged release is a
 * change to {@link REQUIRED_LOGS_REF} and the documented install command.
 *
 * TODO(logs-surface): re-pin once
 * https://github.com/anatoli-iliev/openclaw-vercel-insights/tree/logs-surface
 * merges to main. Then {@link REQUIRED_LOGS_REF} becomes the tag or "main", and
 * {@link LOGS_INSTALL_HINT} loses its `#ref`. {@link hasLogsSurface} keeps
 * working either way, because it tests for the feature rather than the version.
 *
 * ## Two rules from the underlying API
 *
 * **Never send `--until`.** Measured against a live account on 2026-08-18: a
 * window whose end is more than about an hour in the past is answered with
 * `HTTP 400 {"name":"ExceedsBillingLimitError"}`, which the skill reports as a
 * failure. With `--until` left at its default of now, every `--since` succeeds,
 * from 30 minutes to 7 days. Varying only `--since` removes that failure mode
 * rather than handling it, so {@link errorsArgv} has no way to express an end.
 *
 * **Empty is not healthy.** An empty result is exit 0, and runtime logs are
 * retained for one hour on Hobby. So "no errors" from a window longer than the
 * retention can mean the logs aged out. That is reported, never smoothed over.
 *
 * ## The redaction boundary
 *
 * The underlying skill scrubs only its own Vercel token out of log content.
 * Whatever the application printed, which can include secrets, tokens and
 * customer data, arrives verbatim. So {@link toSafeEntries} is a boundary, not a
 * formatter: with `includeMessages` off, the message, the log lines and the raw
 * row are **not copied out of this module at all**. Code downstream cannot leak
 * what it was never handed, which makes the guarantee structural.
 */
import type { Config } from "../config.js";
import type { Env } from "../paths.js";
import { type CredentialResult } from "./credentials.js";
import { type RunResult, type SkillLocation } from "./delegate.js";
/** The slug the skill is installed under. */
export declare const VERCEL_SLUG = "vercel-insights";
/** The environment variable that points at a copy directly. */
export declare const VERCEL_DIR_VAR = "WEB_OBSERVER_VERCEL_SKILL_DIR";
export declare const VERCEL_REPO = "https://github.com/anatoli-iliev/openclaw-vercel-insights";
/**
 * The git ref that carries the request-logs surface.
 *
 * See the TODO in this file's header: this becomes "main" or a tag once the
 * branch merges, and that is the whole of the change.
 */
export declare const REQUIRED_LOGS_REF = "logs-surface";
/** The version that first carried the logs surface. */
export declare const REQUIRED_LOGS_VERSION = "1.1.0";
/** What to tell somebody whose copy predates the logs surface. */
export declare const LOGS_INSTALL_HINT = "openclaw skills install \"git:https://github.com/anatoli-iliev/openclaw-vercel-insights#logs-surface\" --as vercel-insights --force";
/** Presets this bridge will forward, by surface. */
export declare const VERCEL_LOG_PRESETS: readonly string[];
export declare const VERCEL_PRESETS: readonly string[];
/**
 * The variables the delegated skill reads, forwarded when configured.
 *
 * Drawn from the canonical list in env.ts rather than written out again, so the
 * frontmatter test cannot pass while this spec quietly reads something else.
 */
export declare const VERCEL_CREDENTIAL_SPEC: {
    readonly slug: "vercel-insights";
    readonly primaryEnv: "VERCEL_TOKEN";
    readonly optional: ("VERCEL_TOKEN" | "VERCEL_PROJECT_ID" | "VERCEL_TEAM_ID" | "VERCEL_TEAM_SLUG" | "VERCEL_ORG_ID" | "VERCEL_OWNER_ID")[];
};
export type VercelStatus = {
    kind: "absent";
    message: string;
} | {
    kind: "no-logs";
    location: SkillLocation;
    python: string;
    message: string;
} | {
    kind: "ready";
    location: SkillLocation;
    python: string;
    hasLogs: true;
};
/**
 * The interpreter to run the delegated skill with.
 *
 * Its own virtual environment first, because that skill depends on `requests` and
 * the system interpreter very often does not have it: on this machine
 * `python3 -c "import requests"` fails. Falling back to `python3` is still right,
 * because a system install may well have it, and the resulting error message from
 * that skill names the interpreter and the fix.
 */
export declare function pythonFor(dir: string): string;
/**
 * Whether an installed copy carries the request-logs surface.
 *
 * Tests for the module that implements it rather than comparing version strings.
 * A feature test keeps working when the branch merges and the version changes,
 * and it cannot be fooled by a version bumped without the feature.
 */
export declare function hasLogsSurface(dir: string): boolean;
/**
 * Whether the Vercel skill is installed, and whether it can answer about logs.
 *
 * Three outcomes, because they need three different sentences. On this machine
 * the installed copy is 0.2.0 with no logs surface, so `no-logs` is the case a
 * real user hits today, and telling them "not installed" would be wrong.
 */
export declare function vercelStatus(env: Env): VercelStatus;
/** Check a forwarded preset against the allowlist. */
export declare function rejectUnknownPreset(argv: readonly string[]): string | null;
export type VercelRunContext = {
    status: Extract<VercelStatus, {
        kind: "ready" | "no-logs";
    }>;
    credentials: CredentialResult;
    env: Env;
};
/** Resolve everything needed to run the delegated skill. */
export declare function prepare(env: Env): {
    status: VercelStatus;
    credentials: CredentialResult;
};
/**
 * Run the delegated skill.
 *
 * The token travels in the child's environment and nowhere else. `--token` is
 * deliberately never used: a credential on a command line is visible in `ps`, in
 * a process tree, and to a model reading a transcript, and that skill's own
 * documentation refuses the pattern for the same reason.
 */
export declare function runVercel(context: VercelRunContext, argv: readonly string[], timeoutMs?: number): Promise<RunResult>;
/**
 * The arguments for one error poll.
 *
 * There is no parameter for the end of the window, and that is deliberate: see
 * this file's header. `--limit` asks for the maximum the surface will fetch,
 * because an alert that undercounts a flood is worse than a slower poll.
 */
export declare function errorsArgv(project: string, windowMinutes: number): string[];
/** The arguments for one performance-budget check of one project. */
export declare function budgetArgv(config: Config, project: string): string[];
/**
 * One error, reduced to fields that are safe to put in a chat message.
 *
 * Every field here is either produced by Vercel's infrastructure or chosen by
 * the site's own routing. None of it is free text an application wrote, with the
 * single exception of `message`, which is present only when the user has
 * explicitly opted in.
 */
export type SafeErrorEntry = {
    requestId: string;
    timestamp: string | null;
    status: number | null;
    method: string;
    route: string;
    path: string;
    level: string | null;
    crashed: boolean;
    isError: boolean;
    /**
     * The site's hostname, or "" when absent or not a plain hostname. Vercel only
     * routes a request to a project through that project's own domains, so this
     * names the site rather than repeating what a visitor typed.
     */
    domain: string;
    /**
     * Present only when `vercel.errors.includeMessages` is true, and even then
     * only as {@link redactMessage} leaves it.
     */
    message?: string;
};
export type ErrorsPayload = {
    entries: SafeErrorEntry[];
    truncated: boolean;
    /** The skill's own notes, including the retention caveat on an empty result. */
    notes: string[];
    /** The window the skill actually queried, as it reported it. */
    since: string | null;
    until: string | null;
};
/** The longest message an alert carries, after redaction. */
export declare const MESSAGE_LIMIT = 200;
/**
 * Reduce an application's log message to a line that is reasonable to send to
 * a chat the user opted into.
 *
 * The underlying skill scrubs only its own Vercel token, so this is the second
 * line of defence for the user who turned `includeMessages` on: the first line
 * of the message only, with the shapes secrets usually take replaced. It is
 * pattern-based and cannot catch everything, which is why the opt-in exists.
 *
 * - `key=value` and `key: value` pairs whose key names a secret
 * - `Bearer ...` and `Basic ...` credentials
 * - email addresses
 * - JWTs, and any unbroken run of 24 or more letters, digits, `_` or `-`
 *   containing a digit, which is what API keys and session ids look like
 * - credentials embedded in a URL
 */
export declare function redactMessage(message: string): string;
/**
 * Parse `errors --json` into the safe subset.
 *
 * This is the redaction boundary. When `includeMessages` is false the message,
 * the individual log lines and the raw row are not read into the result at all,
 * so no downstream formatting mistake can put them in an alert.
 *
 * @param document The decoded `--json` document.
 * @param includeMessages Whether the user opted into raw log text.
 * @throws Error when the document is not the expected shape, because a silently
 *   empty parse would report a healthy site.
 */
export declare function toSafeEntries(document: unknown, includeMessages: boolean): ErrorsPayload;
/** A tally of one poll's new errors, for the alert text. */
export type ErrorTally = {
    total: number;
    byStatus: Array<[string, number]>;
    byRoute: Array<[string, number]>;
};
/** Count new errors by status and by route, most frequent first. */
export declare function tally(entries: readonly SafeErrorEntry[]): ErrorTally;
/** One distinct error in a poll: every entry that shares its cause. */
export type ErrorGroup = {
    count: number;
    /** The redacted message, or null when messages are not included. */
    message: string | null;
    method: string;
    /** Statuses seen, most frequent first. */
    statuses: Array<[string, number]>;
    /** Route patterns seen, most frequent first. Never concrete paths. */
    routes: Array<[string, number]>;
    level: string | null;
    crashed: number;
    /** Entries that responded below 500 without crashing. */
    loggedOnly: number;
    /** A request id to look up in the Vercel dashboard. */
    sampleRequestId: string;
};
/**
 * Group a poll's errors into distinct ones, most frequent first.
 *
 * With messages included, entries sharing a message are one error wherever it
 * was raised, because one bug often fails several routes. Without them, the
 * best available identity is the method, route, status and whether it crashed.
 */
export declare function groupErrors(entries: readonly SafeErrorEntry[]): ErrorGroup[];
/** The hostname most of a poll's errors were served on, or "" when none is known. */
export declare function mainDomain(entries: readonly SafeErrorEntry[]): string;
