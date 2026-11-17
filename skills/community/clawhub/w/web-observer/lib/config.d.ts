/**
 * Configuration: the shape on disk, how it is validated, and the URL allowlist
 * derived from it.
 *
 * Two rules shape this module.
 *
 * **Nothing is silently ignored.** An unknown key is a configuration error
 * naming it, not a key that is dropped. A watch written with `intervalMinute`
 * instead of `intervalMinutes` would otherwise keep the default cadence
 * forever, and the user would have no way to tell from the output that the
 * number they wrote was never read. The same reasoning applies to every
 * misspelling: this file is edited by hand.
 *
 * **The allowlist has exactly one source.** {@link allowlistOf} derives it from
 * the configured watch URLs and nothing else. There is no flag that extends it
 * and no other constructor for it, so "Web Observer only contacts hosts the
 * user configured" is a property of the code rather than a claim in a document.
 */
/** Where a configuration problem was found, as a dotted path into the file. */
export type ConfigPath = string;
/**
 * A configuration or usage problem, reported as exit code 2.
 *
 * Carries the path it was found at so every message can name the offending
 * key rather than describing it.
 */
export declare class ConfigError extends Error {
    readonly path: ConfigPath;
    constructor(path: ConfigPath, message: string);
}
/**
 * One acceptable response status: an exact code, a class such as `"2xx"`, or an
 * inclusive `[min, max]` range.
 *
 * Three forms rather than one because all three are things people actually
 * mean. A marketing page is `200`. An endpoint behind a redirect is
 * `[200, 399]`. "Any success" is `"2xx"`.
 */
export type StatusExpectation = number | string | [number, number];
/** One URL to watch, with every default already applied. */
export type Watch = {
    /** Stable identifier, used as the state key and in alert text. */
    id: string;
    url: string;
    intervalMinutes: number;
    method: string;
    expectStatus: StatusExpectation[];
    /** Substring the body must contain, or null. */
    expectBody: string | null;
    /** Regular expression source the body must match, or null. */
    expectBodyRegex: string | null;
    timeoutMs: number;
    /**
     * Requests made within one check before the check counts as failed.
     *
     * This is the guard against a single dropped packet, and it is separate from
     * {@link failureThreshold} because the two protect against different things
     * at different speeds: `attempts` retries seconds apart inside one run, while
     * `failureThreshold` waits for the next tick, minutes later. A check succeeds
     * as soon as any attempt succeeds.
     */
    attempts: number;
    /** Pause between attempts within one check. */
    retryDelayMs: number;
    /** Consecutive failed checks required before the first alert. */
    failureThreshold: number;
    /** Consecutive successes required before the recovery message. */
    recoveryThreshold: number;
    /** Redirect hops to follow. Every hop is allowlist-checked. */
    followRedirects: number;
    headers: Record<string, string>;
    enabled: boolean;
};
/** Defaults every watch inherits and may override. */
export type WatchDefaults = Omit<Watch, "id" | "url">;
export type UptimeConfig = {
    enabled: boolean;
    /**
     * How often the cron job runs. A watch is checked on the first tick at or
     * after it comes due, so an interval is honoured to within one tick.
     */
    tickMinutes: number;
    defaults: WatchDefaults;
    watches: Watch[];
};
export type VercelErrorsConfig = {
    enabled: boolean;
    intervalMinutes: number;
    /**
     * How far back each poll looks. Deliberately longer than
     * `intervalMinutes`, so a late cycle cannot let an error fall between two
     * windows; the overlap costs nothing because entries are deduplicated by
     * request id.
     */
    windowMinutes: number;
    /** Alert when the count of new errors in a poll exceeds this. */
    threshold: number;
    /**
     * Whether raw log message text may travel into an alert.
     *
     * Off by default, and enforced in bridge/vercel.ts rather than in the
     * formatter: the underlying skill scrubs only its own Vercel token from log
     * content, so whatever the application printed, which can include secrets
     * and customer data, arrives as-is.
     */
    includeMessages: boolean;
};
export type VercelBudgetConfig = {
    enabled: boolean;
    intervalMinutes: number;
    /** Metric id to threshold, in the units the metric is reported in. */
    metrics: Record<string, number>;
};
export type VercelConfig = {
    enabled: boolean;
    /**
     * Project names or `prj_` ids, in the order they are polled.
     *
     * Written in the file as `project` for one or `projects` for several. Every
     * project shares the error and budget settings below, and keeps its own state,
     * so an outage on one site neither raises nor clears an alert for another.
     */
    projects: string[];
    errors: VercelErrorsConfig;
    budget: VercelBudgetConfig;
};
export type Ga4DigestConfig = {
    enabled: boolean;
    /** A five-field cron expression, since a digest is a wall-clock event. */
    cron: string;
    preset: string;
    since: string;
};
export type Ga4Config = {
    enabled: boolean;
    /**
     * Property ids, one digest section each. Written as `property` for one or
     * `properties` for several. Empty means the open-ga4 skill's own default.
     */
    properties: string[];
    digest: Ga4DigestConfig;
};
/**
 * Where alerts are delivered.
 *
 * Read only by the `schedule` command, which turns it into `--channel` and
 * `--to` on an `openclaw cron add`. Nothing in this skill opens a connection to
 * a chat provider: a cron job announces this tool's stdout, which is what keeps
 * alerting on OpenClaw's own mechanism instead of a second bot token.
 */
export type NotifyConfig = {
    channel: string | null;
    to: string | null;
};
export type Config = {
    notify: NotifyConfig;
    uptime: UptimeConfig;
    vercel: VercelConfig;
    ga4: Ga4Config;
};
export declare const WATCH_DEFAULTS: WatchDefaults;
/** Methods a check may use. All are reads: this skill never changes anything. */
export declare const SAFE_METHODS: readonly string[];
/**
 * Validate a watch URL.
 *
 * @returns The URL as given, once parsed.
 * @throws ConfigError for a scheme other than http or https, for embedded
 *   credentials, and for anything unparseable.
 */
export declare function readWatchUrl(path: ConfigPath, value: unknown): string;
/**
 * Validate a decoded configuration document.
 *
 * @param document Anything `JSON.parse` produced.
 * @returns The configuration with every default applied, so no consumer needs
 *   to know which values were written down and which were inferred.
 * @throws ConfigError naming the path and the offending value.
 */
export declare function parseConfig(document: unknown): Config;
/** A configuration with every module off, used when no file exists yet. */
export declare function emptyConfig(): Config;
/**
 * The set of hosts Web Observer may contact, derived from the watch URLs.
 *
 * This is the only constructor for an allowlist, and its only input is the
 * configuration. There is no flag that adds to it, which is what makes
 * "only user-configured hosts are contacted" a property of the code.
 *
 * A host includes its port when one is given, so `example.com:8443` does not
 * authorise `example.com:443`.
 *
 * @param watches Every configured watch, enabled or not. A disabled watch still
 *   contributes: enabling it must not need a second edit elsewhere.
 */
export declare function allowlistOf(watches: readonly Watch[]): ReadonlySet<string>;
/**
 * Whether a URL may be contacted.
 *
 * Used for the initial request and again for every redirect hop, so a redirect
 * cannot carry a request to a host the user never configured.
 *
 * @param url The absolute URL about to be requested.
 * @param allowlist The set from {@link allowlistOf}.
 * @returns The parsed URL when it is allowed, and null when it is not or cannot
 *   be parsed. Null rather than a throw because a redirect to an unparseable
 *   Location is a check failure, not a crash.
 */
export declare function allowedUrl(url: string, allowlist: ReadonlySet<string>): URL | null;
/** Whether a response status satisfies any of a watch's expectations. */
export declare function statusMatches(status: number, expectations: readonly StatusExpectation[]): boolean;
/** How an expectation list reads in an alert, for example `200, 2xx, 200-399`. */
export declare function describeStatusExpectations(expectations: readonly StatusExpectation[]): string;
