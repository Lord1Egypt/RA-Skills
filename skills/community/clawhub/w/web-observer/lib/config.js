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
/**
 * A configuration or usage problem, reported as exit code 2.
 *
 * Carries the path it was found at so every message can name the offending
 * key rather than describing it.
 */
export class ConfigError extends Error {
    path;
    constructor(path, message) {
        super(`${path}: ${message}`);
        this.name = "ConfigError";
        this.path = path;
    }
}
export const WATCH_DEFAULTS = {
    intervalMinutes: 5,
    method: "GET",
    expectStatus: [200],
    expectBody: null,
    expectBodyRegex: null,
    timeoutMs: 10_000,
    attempts: 2,
    retryDelayMs: 10_000,
    failureThreshold: 2,
    recoveryThreshold: 1,
    followRedirects: 0,
    headers: {},
    enabled: true,
};
/** Methods a check may use. All are reads: this skill never changes anything. */
export const SAFE_METHODS = ["GET", "HEAD", "OPTIONS"];
const WATCH_KEYS = [
    "id",
    "url",
    "intervalMinutes",
    "method",
    "expectStatus",
    "expectBody",
    "expectBodyRegex",
    "timeoutMs",
    "attempts",
    "retryDelayMs",
    "failureThreshold",
    "recoveryThreshold",
    "followRedirects",
    "headers",
    "enabled",
];
const STATUS_CLASS = /^[1-5]xx$/;
function isPlainObject(value) {
    return typeof value === "object" && value !== null && !Array.isArray(value);
}
/**
 * Edit distance between two strings, capped by early exit at `limit`.
 *
 * Exists only to turn a refused key into a suggestion. A missing plural on
 * `intervalMinutes` and a wrong case on `timeoutMs` are the two typos this
 * file invites, and neither is caught by an equality check.
 */
function editDistance(a, b, limit) {
    if (Math.abs(a.length - b.length) > limit)
        return limit + 1;
    let previous = Array.from({ length: b.length + 1 }, (_unused, index) => index);
    for (let i = 1; i <= a.length; i += 1) {
        const current = [i];
        for (let j = 1; j <= b.length; j += 1) {
            const substitution = previous[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1);
            current[j] = Math.min(substitution, previous[j] + 1, current[j - 1] + 1);
        }
        previous = current;
    }
    return previous[b.length];
}
/**
 * The accepted key a misspelling most likely meant, or undefined.
 *
 * Case-insensitive equality first, then the nearest key within two edits, which
 * covers a dropped letter, an extra one and a transposition.
 */
function nearestKey(key, known) {
    const lowered = key.toLowerCase();
    const exact = known.find((candidate) => candidate.toLowerCase() === lowered);
    if (exact)
        return exact;
    let best;
    for (const candidate of known) {
        const distance = editDistance(lowered, candidate.toLowerCase(), 2);
        if (distance <= 2 && (best === undefined || distance < best.distance)) {
            best = { key: candidate, distance };
        }
    }
    return best?.key;
}
/**
 * Refuse a key the schema does not name.
 *
 * @param path Dotted path of the containing object, for the message.
 * @param value The object to check.
 * @param known Every key this object may carry.
 * @throws ConfigError naming the offending key and listing what is accepted.
 */
function rejectUnknownKeys(path, value, known) {
    for (const key of Object.keys(value)) {
        if (!known.includes(key)) {
            const suggestion = nearestKey(key, known);
            const hint = suggestion ? ` Did you mean ${suggestion}?` : "";
            throw new ConfigError(`${path}.${key}`, `is not a setting Web Observer reads; ${path} accepts ${known.join(", ")}.${hint} ` +
                "An unrecognised key is refused rather than ignored, because a silently " +
                "dropped setting would leave the default in force with nothing in the " +
                "output to say so");
        }
    }
}
function requireObject(path, value) {
    if (!isPlainObject(value)) {
        throw new ConfigError(path, `must be an object, not ${describe(value)}`);
    }
    return value;
}
function describe(value) {
    if (value === null)
        return "null";
    if (Array.isArray(value))
        return "an array";
    return typeof value;
}
function readBoolean(path, value, fallback) {
    if (value === undefined)
        return fallback;
    if (typeof value !== "boolean") {
        throw new ConfigError(path, `must be true or false, not ${describe(value)}`);
    }
    return value;
}
function readString(path, value, fallback) {
    if (value === undefined)
        return fallback;
    if (typeof value !== "string" || value.trim() === "") {
        throw new ConfigError(path, "must be a non-empty string");
    }
    return value;
}
function readNullableString(path, value, fallback) {
    if (value === undefined)
        return fallback;
    if (value === null)
        return null;
    if (typeof value !== "string" || value.trim() === "") {
        throw new ConfigError(path, "must be a non-empty string or null");
    }
    return value;
}
/**
 * A whole number within an inclusive range.
 *
 * Bounds are checked and named rather than clamped: a timeout silently raised
 * from 5 ms to a floor would make the tool report a cadence nobody configured.
 */
function readInteger(path, value, fallback, min, max) {
    if (value === undefined)
        return fallback;
    if (typeof value !== "number" || !Number.isFinite(value) || !Number.isInteger(value)) {
        throw new ConfigError(path, `must be a whole number, not ${describe(value)}`);
    }
    if (value < min || value > max) {
        throw new ConfigError(path, `is ${value}, outside the accepted range ${min} to ${max}`);
    }
    return value;
}
function readHeaders(path, value, fallback) {
    if (value === undefined)
        return fallback;
    const object = requireObject(path, value);
    const headers = {};
    for (const [name, headerValue] of Object.entries(object)) {
        if (typeof headerValue !== "string") {
            throw new ConfigError(`${path}.${name}`, `must be a string, not ${describe(headerValue)}`);
        }
        // A header carrying a newline would let a value continue into a second
        // header. Node refuses it too, but with a message that quotes the value,
        // and a configured header may well be an authorization token.
        if (/[\r\n]/.test(name) || /[\r\n]/.test(headerValue)) {
            throw new ConfigError(`${path}.${name}`, "must not contain a carriage return or newline");
        }
        headers[name] = headerValue;
    }
    return headers;
}
/**
 * Validate one status expectation.
 *
 * @throws ConfigError naming every accepted form, since this is the setting
 *   most likely to be written as a string such as `"200"`.
 */
function readStatusExpectation(path, value) {
    if (typeof value === "number") {
        if (!Number.isInteger(value) || value < 100 || value > 599) {
            throw new ConfigError(path, `is ${value}, which is not an HTTP status between 100 and 599`);
        }
        return value;
    }
    if (typeof value === "string") {
        if (!STATUS_CLASS.test(value)) {
            throw new ConfigError(path, `is ${JSON.stringify(value)}; a string status must be a class such as "2xx" or "5xx". ` +
                "An exact code is written as a number, 200 rather than \"200\"");
        }
        return value;
    }
    if (Array.isArray(value)) {
        if (value.length !== 2) {
            throw new ConfigError(path, `has ${value.length} items; a range is exactly two, [min, max], both inclusive`);
        }
        const [min, max] = value;
        for (const bound of [min, max]) {
            if (typeof bound !== "number" || !Number.isInteger(bound) || bound < 100 || bound > 599) {
                throw new ConfigError(path, "must be a range of two HTTP statuses between 100 and 599, for example [200, 399]");
            }
        }
        if (min > max) {
            throw new ConfigError(path, `is [${min}, ${max}], which is empty because min exceeds max`);
        }
        return [min, max];
    }
    throw new ConfigError(path, `must be a status code (200), a class ("2xx") or a range ([200, 399]), not ${describe(value)}`);
}
function readStatusExpectations(path, value, fallback) {
    if (value === undefined)
        return fallback;
    const items = Array.isArray(value) ? value : [value];
    if (items.length === 0) {
        throw new ConfigError(path, "is empty, so no response could ever pass. Name at least one status, class or range");
    }
    return items.map((item, index) => readStatusExpectation(Array.isArray(value) ? `${path}[${index}]` : path, item));
}
/**
 * Validate a watch URL.
 *
 * @returns The URL as given, once parsed.
 * @throws ConfigError for a scheme other than http or https, for embedded
 *   credentials, and for anything unparseable.
 */
export function readWatchUrl(path, value) {
    if (typeof value !== "string" || value.trim() === "") {
        throw new ConfigError(path, "must be a URL string");
    }
    let parsed;
    try {
        parsed = new URL(value);
    }
    catch {
        throw new ConfigError(path, `is not a URL: ${JSON.stringify(value)}. Include the scheme, as in https://example.com`);
    }
    if (parsed.protocol !== "http:" && parsed.protocol !== "https:") {
        throw new ConfigError(path, `has scheme ${parsed.protocol.replace(":", "")}; Web Observer checks http and https only`);
    }
    if (parsed.username !== "" || parsed.password !== "") {
        throw new ConfigError(path, "carries credentials in the URL. Put them in a header instead, so the secret " +
            "cannot be echoed back in an alert that names the URL");
    }
    return value;
}
/**
 * Validate a regular expression at load time rather than at check time.
 *
 * An invalid pattern found during a check would look exactly like a site
 * failure, and would alert as one.
 */
function readBodyRegex(path, value, fallback) {
    const source = readNullableString(path, value, fallback);
    if (source === null)
        return null;
    try {
        new RegExp(source);
    }
    catch (error) {
        const reason = error instanceof Error ? error.message : String(error);
        throw new ConfigError(path, `is not a valid regular expression: ${reason}`);
    }
    return source;
}
function readWatchDefaults(path, value, base) {
    if (value === undefined)
        return base;
    const object = requireObject(path, value);
    rejectUnknownKeys(path, object, WATCH_KEYS.filter((key) => key !== "id" && key !== "url"));
    const method = readString(`${path}.method`, object["method"], base.method).toUpperCase();
    if (!SAFE_METHODS.includes(method)) {
        throw new ConfigError(`${path}.method`, `is ${method}; Web Observer only issues ${SAFE_METHODS.join(", ")}, because a health ` +
            "check must not be able to change anything it is checking");
    }
    return {
        intervalMinutes: readInteger(`${path}.intervalMinutes`, object["intervalMinutes"], base.intervalMinutes, 1, 10_080),
        method,
        expectStatus: readStatusExpectations(`${path}.expectStatus`, object["expectStatus"], base.expectStatus),
        expectBody: readNullableString(`${path}.expectBody`, object["expectBody"], base.expectBody),
        expectBodyRegex: readBodyRegex(`${path}.expectBodyRegex`, object["expectBodyRegex"], base.expectBodyRegex),
        timeoutMs: readInteger(`${path}.timeoutMs`, object["timeoutMs"], base.timeoutMs, 100, 120_000),
        attempts: readInteger(`${path}.attempts`, object["attempts"], base.attempts, 1, 10),
        retryDelayMs: readInteger(`${path}.retryDelayMs`, object["retryDelayMs"], base.retryDelayMs, 0, 60_000),
        failureThreshold: readInteger(`${path}.failureThreshold`, object["failureThreshold"], base.failureThreshold, 1, 100),
        recoveryThreshold: readInteger(`${path}.recoveryThreshold`, object["recoveryThreshold"], base.recoveryThreshold, 1, 100),
        followRedirects: readInteger(`${path}.followRedirects`, object["followRedirects"], base.followRedirects, 0, 10),
        headers: readHeaders(`${path}.headers`, object["headers"], base.headers),
        enabled: readBoolean(`${path}.enabled`, object["enabled"], base.enabled),
    };
}
const ID_SHAPE = /^[a-z0-9][a-z0-9._-]*$/i;
function readWatch(path, value, defaults) {
    const object = requireObject(path, value);
    rejectUnknownKeys(path, object, WATCH_KEYS);
    const url = readWatchUrl(`${path}.url`, object["url"]);
    const id = readString(`${path}.id`, object["id"], "");
    if (id === "") {
        throw new ConfigError(`${path}.id`, "is required. It keys this watch's saved state, so renaming it forgets whether " +
            "the URL was already down, and two watches sharing one would overwrite each other");
    }
    if (!ID_SHAPE.test(id)) {
        throw new ConfigError(`${path}.id`, `is ${JSON.stringify(id)}; an id may hold letters, digits, dot, dash and underscore, ` +
            "and must start with a letter or digit");
    }
    // `id` and `url` are this watch's own, not overridable defaults, so they are
    // removed before the shared reader runs. Deleted rather than set to
    // undefined: Object.keys still reports a key whose value is undefined, and
    // rejectUnknownKeys would refuse the very keys just validated above.
    const overrides = { ...object };
    delete overrides["id"];
    delete overrides["url"];
    const resolved = readWatchDefaults(path, overrides, defaults);
    if (resolved.expectBody !== null && resolved.expectBodyRegex !== null) {
        throw new ConfigError(`${path}.expectBodyRegex`, "is set alongside expectBody. Use one: a substring or a pattern, not both, " +
            "since two body tests would make a failure ambiguous to report");
    }
    if (resolved.method === "HEAD" && (resolved.expectBody !== null || resolved.expectBodyRegex !== null)) {
        throw new ConfigError(`${path}.method`, "is HEAD, which returns no body, but a body expectation is configured. " +
            "A HEAD check can only test the status");
    }
    return { id, url, ...resolved };
}
function readUptime(path, value) {
    if (value === undefined) {
        return { enabled: false, tickMinutes: 5, defaults: WATCH_DEFAULTS, watches: [] };
    }
    const object = requireObject(path, value);
    rejectUnknownKeys(path, object, ["enabled", "tickMinutes", "defaults", "watches"]);
    const defaults = readWatchDefaults(`${path}.defaults`, object["defaults"], WATCH_DEFAULTS);
    const rawWatches = object["watches"];
    let watches = [];
    if (rawWatches !== undefined) {
        if (!Array.isArray(rawWatches)) {
            throw new ConfigError(`${path}.watches`, `must be an array, not ${describe(rawWatches)}`);
        }
        watches = rawWatches.map((watch, index) => readWatch(`${path}.watches[${index}]`, watch, defaults));
    }
    const seen = new Map();
    for (const [index, watch] of watches.entries()) {
        const previous = seen.get(watch.id);
        if (previous !== undefined) {
            throw new ConfigError(`${path}.watches[${index}].id`, `repeats the id ${JSON.stringify(watch.id)} already used by watches[${previous}]. ` +
                "Ids key saved state, so a duplicate would make two URLs share one memory of " +
                "being up or down");
        }
        seen.set(watch.id, index);
    }
    const enabled = readBoolean(`${path}.enabled`, object["enabled"], watches.length > 0);
    if (enabled && watches.length === 0) {
        throw new ConfigError(`${path}.watches`, "is empty while uptime is enabled, so there is nothing to check. Add a watch, " +
            "or set uptime.enabled to false");
    }
    return {
        enabled,
        tickMinutes: readInteger(`${path}.tickMinutes`, object["tickMinutes"], 5, 1, 1_440),
        defaults,
        watches,
    };
}
function readMetrics(path, value) {
    if (value === undefined)
        return {};
    const object = requireObject(path, value);
    const metrics = {};
    for (const [name, threshold] of Object.entries(object)) {
        if (typeof threshold !== "number" || !Number.isFinite(threshold) || threshold < 0) {
            throw new ConfigError(`${path}.${name}`, `must be a non-negative number, not ${describe(threshold)}`);
        }
        if (!/^[a-z][a-z0-9_-]*$/i.test(name)) {
            throw new ConfigError(`${path}.${name}`, "is not a metric id");
        }
        metrics[name] = threshold;
    }
    return metrics;
}
/**
 * A list of names written either as one string under `singular` or as an array
 * under `plural`.
 *
 * Both spellings are accepted because a single site is the common case and the
 * plural is what a second site needs; both at once is refused, since which one
 * won would be invisible from the output.
 */
function readNameList(path, object, singular, plural) {
    const one = object[singular];
    const many = object[plural];
    if (one !== undefined && one !== null && many !== undefined) {
        throw new ConfigError(`${path}.${plural}`, `is set alongside ${singular}. Use ${singular} for one or ${plural} for several, not both`);
    }
    if (many === undefined) {
        const name = readNullableString(`${path}.${singular}`, one, null);
        return name === null ? [] : [name];
    }
    if (!Array.isArray(many)) {
        throw new ConfigError(`${path}.${plural}`, `must be an array, not ${describe(many)}`);
    }
    const names = many.map((item, index) => readString(`${path}.${plural}[${index}]`, item, ""));
    for (const [index, name] of names.entries()) {
        const previous = names.indexOf(name);
        if (previous !== index) {
            throw new ConfigError(`${path}.${plural}[${index}]`, `repeats ${JSON.stringify(name)}, already listed at ${plural}[${previous}]`);
        }
    }
    return names;
}
function readVercel(path, value) {
    const disabled = {
        enabled: false,
        projects: [],
        errors: {
            enabled: false,
            intervalMinutes: 15,
            windowMinutes: 20,
            threshold: 0,
            includeMessages: false,
        },
        budget: { enabled: false, intervalMinutes: 360, metrics: {} },
    };
    if (value === undefined)
        return disabled;
    const object = requireObject(path, value);
    rejectUnknownKeys(path, object, ["enabled", "project", "projects", "errors", "budget"]);
    const enabled = readBoolean(`${path}.enabled`, object["enabled"], false);
    const projects = readNameList(path, object, "project", "projects");
    const errorsRaw = object["errors"];
    let errors = disabled.errors;
    if (errorsRaw !== undefined) {
        const errorsObject = requireObject(`${path}.errors`, errorsRaw);
        rejectUnknownKeys(`${path}.errors`, errorsObject, [
            "enabled",
            "intervalMinutes",
            "windowMinutes",
            "threshold",
            "includeMessages",
        ]);
        const intervalMinutes = readInteger(`${path}.errors.intervalMinutes`, errorsObject["intervalMinutes"], 15, 1, 1_440);
        const windowMinutes = readInteger(`${path}.errors.windowMinutes`, errorsObject["windowMinutes"], Math.max(intervalMinutes + 5, 20), 1, 1_440);
        if (windowMinutes <= intervalMinutes) {
            throw new ConfigError(`${path}.errors.windowMinutes`, `is ${windowMinutes}, which does not exceed intervalMinutes of ${intervalMinutes}. ` +
                "The window must overlap the interval, or an error arriving while a poll is in " +
                "flight falls into the gap between two windows and is never reported. Entries " +
                "are deduplicated by request id, so the overlap costs nothing");
        }
        errors = {
            enabled: readBoolean(`${path}.errors.enabled`, errorsObject["enabled"], true),
            intervalMinutes,
            windowMinutes,
            threshold: readInteger(`${path}.errors.threshold`, errorsObject["threshold"], 0, 0, 10_000),
            includeMessages: readBoolean(`${path}.errors.includeMessages`, errorsObject["includeMessages"], false),
        };
    }
    const budgetRaw = object["budget"];
    let budget = disabled.budget;
    if (budgetRaw !== undefined) {
        const budgetObject = requireObject(`${path}.budget`, budgetRaw);
        rejectUnknownKeys(`${path}.budget`, budgetObject, ["enabled", "intervalMinutes", "metrics"]);
        const metrics = readMetrics(`${path}.budget.metrics`, budgetObject["metrics"]);
        const budgetEnabled = readBoolean(`${path}.budget.enabled`, budgetObject["enabled"], Object.keys(metrics).length > 0);
        if (budgetEnabled && Object.keys(metrics).length === 0) {
            throw new ConfigError(`${path}.budget.metrics`, "is empty while the budget check is enabled, so there is no threshold to test. " +
                'Name at least one, for example {"lcp": 2500}');
        }
        budget = {
            enabled: budgetEnabled,
            intervalMinutes: readInteger(`${path}.budget.intervalMinutes`, budgetObject["intervalMinutes"], 360, 1, 10_080),
            metrics,
        };
    }
    if (enabled && projects.length === 0) {
        throw new ConfigError(`${path}.project`, "is required when the Vercel module is enabled: every query names exactly one " +
            "project. Set project for one site or projects for several. Run the " +
            "vercel-insights skill's --list-projects to see the names");
    }
    return { enabled, projects, errors, budget };
}
function readGa4(path, value) {
    const disabled = {
        enabled: false,
        properties: [],
        digest: { enabled: false, cron: "0 9 * * 1", preset: "report", since: "7d" },
    };
    if (value === undefined)
        return disabled;
    const object = requireObject(path, value);
    rejectUnknownKeys(path, object, ["enabled", "property", "properties", "digest"]);
    const enabled = readBoolean(`${path}.enabled`, object["enabled"], false);
    const properties = readNameList(path, object, "property", "properties");
    const digestRaw = object["digest"];
    let digest = disabled.digest;
    if (digestRaw !== undefined) {
        const digestObject = requireObject(`${path}.digest`, digestRaw);
        rejectUnknownKeys(`${path}.digest`, digestObject, ["enabled", "cron", "preset", "since"]);
        const cron = readString(`${path}.digest.cron`, digestObject["cron"], disabled.digest.cron);
        const fields = cron.trim().split(/\s+/);
        if (fields.length !== 5) {
            throw new ConfigError(`${path}.digest.cron`, `has ${fields.length} fields; a schedule is five, as in "0 9 * * 1" for 09:00 on Mondays`);
        }
        digest = {
            enabled: readBoolean(`${path}.digest.enabled`, digestObject["enabled"], true),
            cron,
            preset: readString(`${path}.digest.preset`, digestObject["preset"], disabled.digest.preset),
            since: readString(`${path}.digest.since`, digestObject["since"], disabled.digest.since),
        };
    }
    return { enabled, properties, digest };
}
function readNotify(path, value) {
    if (value === undefined)
        return { channel: null, to: null };
    const object = requireObject(path, value);
    rejectUnknownKeys(path, object, ["channel", "to"]);
    return {
        channel: readNullableString(`${path}.channel`, object["channel"], null),
        to: readNullableString(`${path}.to`, object["to"], null),
    };
}
/**
 * Validate a decoded configuration document.
 *
 * @param document Anything `JSON.parse` produced.
 * @returns The configuration with every default applied, so no consumer needs
 *   to know which values were written down and which were inferred.
 * @throws ConfigError naming the path and the offending value.
 */
export function parseConfig(document) {
    const object = requireObject("config", document);
    rejectUnknownKeys("config", object, ["notify", "uptime", "vercel", "ga4", "$schema"]);
    return {
        notify: readNotify("notify", object["notify"]),
        uptime: readUptime("uptime", object["uptime"]),
        vercel: readVercel("vercel", object["vercel"]),
        ga4: readGa4("ga4", object["ga4"]),
    };
}
/** A configuration with every module off, used when no file exists yet. */
export function emptyConfig() {
    return parseConfig({});
}
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
export function allowlistOf(watches) {
    const hosts = new Set();
    for (const watch of watches) {
        hosts.add(new URL(watch.url).host.toLowerCase());
    }
    return hosts;
}
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
export function allowedUrl(url, allowlist) {
    let parsed;
    try {
        parsed = new URL(url);
    }
    catch {
        return null;
    }
    if (parsed.protocol !== "http:" && parsed.protocol !== "https:")
        return null;
    return allowlist.has(parsed.host.toLowerCase()) ? parsed : null;
}
/** Whether a response status satisfies one expectation. */
function statusMatchesOne(status, expectation) {
    if (typeof expectation === "number")
        return status === expectation;
    if (typeof expectation === "string") {
        return Math.floor(status / 100) === Number(expectation[0]);
    }
    return status >= expectation[0] && status <= expectation[1];
}
/** Whether a response status satisfies any of a watch's expectations. */
export function statusMatches(status, expectations) {
    return expectations.some((expectation) => statusMatchesOne(status, expectation));
}
/** How an expectation list reads in an alert, for example `200, 2xx, 200-399`. */
export function describeStatusExpectations(expectations) {
    return expectations
        .map((expectation) => Array.isArray(expectation) ? `${expectation[0]}-${expectation[1]}` : String(expectation))
        .join(", ");
}
