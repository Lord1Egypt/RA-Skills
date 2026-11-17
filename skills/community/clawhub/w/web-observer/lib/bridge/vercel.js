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
import path from "node:path";
import { VERCEL_ENV_VARS } from "../env.js";
import { collectCredentials, childEnv } from "./credentials.js";
import { fileExists, findSkill, run } from "./delegate.js";
/** The slug the skill is installed under. */
export const VERCEL_SLUG = "vercel-insights";
/** The environment variable that points at a copy directly. */
export const VERCEL_DIR_VAR = "WEB_OBSERVER_VERCEL_SKILL_DIR";
export const VERCEL_REPO = "https://github.com/anatoli-iliev/openclaw-vercel-insights";
/**
 * The git ref that carries the request-logs surface.
 *
 * See the TODO in this file's header: this becomes "main" or a tag once the
 * branch merges, and that is the whole of the change.
 */
export const REQUIRED_LOGS_REF = "logs-surface";
/** The version that first carried the logs surface. */
export const REQUIRED_LOGS_VERSION = "1.1.0";
/** What to tell somebody whose copy predates the logs surface. */
export const LOGS_INSTALL_HINT = `openclaw skills install "git:${VERCEL_REPO}#${REQUIRED_LOGS_REF}" --as ${VERCEL_SLUG} --force`;
/** Presets this bridge will forward, by surface. */
export const VERCEL_LOG_PRESETS = ["logs", "errors", "error-summary"];
export const VERCEL_PRESETS = [
    "overview",
    "trend",
    "top-pages",
    "top-routes",
    "referrers",
    "countries",
    "devices",
    "browsers",
    "operating-systems",
    "campaigns",
    "events",
    "total",
    "vitals",
    "slowest-pages",
    "fastest-pages",
    "vitals-by-country",
    "vitals-by-device",
    "vitals-trend",
    "data-points",
    ...VERCEL_LOG_PRESETS,
];
/**
 * The variables the delegated skill reads, forwarded when configured.
 *
 * Drawn from the canonical list in env.ts rather than written out again, so the
 * frontmatter test cannot pass while this spec quietly reads something else.
 */
export const VERCEL_CREDENTIAL_SPEC = {
    slug: VERCEL_SLUG,
    primaryEnv: VERCEL_ENV_VARS[0],
    optional: VERCEL_ENV_VARS.slice(1),
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
export function pythonFor(dir) {
    const venv = path.join(dir, ".venv", "bin", "python");
    return fileExists(venv) ? venv : "python3";
}
/**
 * Whether an installed copy carries the request-logs surface.
 *
 * Tests for the module that implements it rather than comparing version strings.
 * A feature test keeps working when the branch merges and the version changes,
 * and it cannot be fooled by a version bumped without the feature.
 */
export function hasLogsSurface(dir) {
    return fileExists(path.join(dir, "vercel_insights", "logs.py"));
}
/**
 * Whether the Vercel skill is installed, and whether it can answer about logs.
 *
 * Three outcomes, because they need three different sentences. On this machine
 * the installed copy is 0.2.0 with no logs surface, so `no-logs` is the case a
 * real user hits today, and telling them "not installed" would be wrong.
 */
export function vercelStatus(env) {
    const location = findSkill(VERCEL_SLUG, env, VERCEL_DIR_VAR);
    if (location === null) {
        return {
            kind: "absent",
            message: `the ${VERCEL_SLUG} skill is not installed, so Vercel traffic, speed and error ` +
                `questions cannot be answered. Install it with: ${LOGS_INSTALL_HINT}`,
        };
    }
    const python = pythonFor(location.dir);
    if (!hasLogsSurface(location.dir)) {
        return {
            kind: "no-logs",
            location,
            python,
            message: `${VERCEL_SLUG} ${location.version ?? "(unknown version)"} is installed at ` +
                `${location.dir}, but it has no request-logs surface, so error-log questions and the ` +
                "scheduled error watch cannot work. Traffic and speed presets still work. Request " +
                `logs need ${REQUIRED_LOGS_VERSION} or later, currently the ${REQUIRED_LOGS_REF} ` +
                `branch: ${LOGS_INSTALL_HINT}`,
        };
    }
    return { kind: "ready", location, python, hasLogs: true };
}
/** Check a forwarded preset against the allowlist. */
export function rejectUnknownPreset(argv) {
    const preset = argv[0];
    if (preset === undefined) {
        return `name a preset. ${VERCEL_SLUG} offers: ${VERCEL_PRESETS.join(", ")}`;
    }
    if (preset.startsWith("-")) {
        return `the first argument must be a preset, not ${preset}. Presets: ${VERCEL_PRESETS.join(", ")}`;
    }
    if (!VERCEL_PRESETS.includes(preset)) {
        return `${preset} is not a ${VERCEL_SLUG} preset. It offers: ${VERCEL_PRESETS.join(", ")}`;
    }
    return null;
}
/** Resolve everything needed to run the delegated skill. */
export function prepare(env) {
    return {
        status: vercelStatus(env),
        credentials: collectCredentials(VERCEL_CREDENTIAL_SPEC, env),
    };
}
/**
 * Run the delegated skill.
 *
 * The token travels in the child's environment and nowhere else. `--token` is
 * deliberately never used: a credential on a command line is visible in `ps`, in
 * a process tree, and to a model reading a transcript, and that skill's own
 * documentation refuses the pattern for the same reason.
 */
export async function runVercel(context, argv, timeoutMs = 180_000) {
    return await run(context.status.python, ["-m", "vercel_insights", ...argv], {
        cwd: context.status.location.dir,
        env: childEnv(context.env, context.credentials.env),
        timeoutMs,
    });
}
/**
 * The arguments for one error poll.
 *
 * There is no parameter for the end of the window, and that is deliberate: see
 * this file's header. `--limit` asks for the maximum the surface will fetch,
 * because an alert that undercounts a flood is worse than a slower poll.
 */
export function errorsArgv(project, windowMinutes) {
    return ["errors", "--since", `${windowMinutes}m`, "--json", "--limit", "200", "--project", project];
}
/** The arguments for one performance-budget check of one project. */
export function budgetArgv(config, project) {
    const argv = ["vitals", "--project", project];
    for (const [metric, threshold] of Object.entries(config.vercel.budget.metrics)) {
        argv.push("--budget", `${metric}=${threshold}`);
    }
    return argv;
}
function asString(value) {
    return typeof value === "string" ? value : "";
}
const HOSTNAME = /^[a-z0-9]([a-z0-9-]*[a-z0-9])?(\.[a-z0-9]([a-z0-9-]*[a-z0-9])?)+$/i;
function asHostname(value) {
    const text = asString(value);
    return text.length <= 253 && HOSTNAME.test(text) ? text.toLowerCase() : "";
}
/** The longest message an alert carries, after redaction. */
export const MESSAGE_LIMIT = 200;
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
export function redactMessage(message) {
    const first = (message.split(/\r?\n/).find((line) => line.trim() !== "") ?? "").trim();
    const redacted = first
        .replace(/\b([a-z][a-z0-9+.-]*:\/\/)[^\s/:@]+:[^\s/@]+@/gi, "$1[redacted]@")
        .replace(/\b((?:api[_-]?key|apikey|token|secret|password|passwd|pwd|auth|authorization|session|cookie|signature|sig|key)["']?\s*[:=]\s*)("[^"]*"|'[^']*'|[^\s,;&]+)/gi, "$1[redacted]")
        .replace(/\b(bearer|basic)\s+[A-Za-z0-9._~+/=-]+/gi, "$1 [redacted]")
        .replace(/[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g, "[email]")
        .replace(/\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+/g, "[redacted]")
        .replace(/[A-Za-z0-9_-]{24,}/g, (run) => (/\d/.test(run) ? "[redacted]" : run))
        .replace(/\s+/g, " ");
    return redacted.length > MESSAGE_LIMIT ? `${redacted.slice(0, MESSAGE_LIMIT)}…` : redacted;
}
function asNumberOrNull(value) {
    return typeof value === "number" && Number.isFinite(value) ? value : null;
}
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
export function toSafeEntries(document, includeMessages) {
    if (typeof document !== "object" || document === null || Array.isArray(document)) {
        throw new Error("the errors output was not a JSON object");
    }
    const object = document;
    const rawEntries = object["entries"];
    if (!Array.isArray(rawEntries)) {
        throw new Error("the errors output carried no 'entries' array");
    }
    const query = object["query"];
    const queryObject = typeof query === "object" && query !== null ? query : {};
    const entries = [];
    for (const raw of rawEntries) {
        if (typeof raw !== "object" || raw === null || Array.isArray(raw))
            continue;
        const row = raw;
        const entry = {
            requestId: asString(row["requestId"]),
            timestamp: typeof row["timestamp"] === "string" ? row["timestamp"] : null,
            status: asNumberOrNull(row["status"]),
            method: asString(row["method"]),
            route: asString(row["route"]),
            path: asString(row["path"]),
            // Verified live: this field can be null as well as absent.
            level: typeof row["level"] === "string" ? row["level"] : null,
            crashed: row["crashed"] === true,
            isError: row["isError"] === true,
            domain: asHostname(row["domain"]),
        };
        if (includeMessages) {
            entry.message = redactMessage(asString(row["message"]));
        }
        entries.push(entry);
    }
    const notes = Array.isArray(object["notes"])
        ? object["notes"].filter((note) => typeof note === "string")
        : [];
    return {
        entries,
        truncated: object["truncated"] === true,
        notes,
        since: typeof queryObject["since"] === "string" ? queryObject["since"] : null,
        until: typeof queryObject["until"] === "string" ? queryObject["until"] : null,
    };
}
/** Count new errors by status and by route, most frequent first. */
export function tally(entries) {
    const statuses = new Map();
    const routes = new Map();
    for (const entry of entries) {
        const status = entry.status === null ? "(none)" : String(entry.status);
        statuses.set(status, (statuses.get(status) ?? 0) + 1);
        // The route pattern, never the concrete path. A path is chosen by whoever
        // made the request, and this tally is delivered into a chat, so quoting it
        // would let any stranger write into the alert.
        const route = entry.route !== "" ? entry.route : "(unrouted)";
        routes.set(route, (routes.get(route) ?? 0) + 1);
    }
    const order = (map) => [...map.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
    return { total: entries.length, byStatus: order(statuses), byRoute: order(routes) };
}
/**
 * Group a poll's errors into distinct ones, most frequent first.
 *
 * With messages included, entries sharing a message are one error wherever it
 * was raised, because one bug often fails several routes. Without them, the
 * best available identity is the method, route, status and whether it crashed.
 */
export function groupErrors(entries) {
    const groups = new Map();
    for (const entry of entries) {
        const status = entry.status === null ? "(none)" : String(entry.status);
        const route = entry.route !== "" ? entry.route : "(unrouted)";
        const message = entry.message !== undefined && entry.message !== "" ? entry.message : null;
        const key = message !== null
            ? `m\u0000${message}`
            : `r\u0000${entry.method}\u0000${route}\u0000${status}\u0000${entry.crashed}`;
        let slot = groups.get(key);
        if (slot === undefined) {
            slot = {
                group: {
                    count: 0,
                    message,
                    method: entry.method,
                    statuses: [],
                    routes: [],
                    level: entry.level,
                    crashed: 0,
                    loggedOnly: 0,
                    sampleRequestId: entry.requestId,
                },
                statuses: new Map(),
                routes: new Map(),
            };
            groups.set(key, slot);
        }
        const { group } = slot;
        group.count += 1;
        if (entry.crashed)
            group.crashed += 1;
        if (!entry.crashed && entry.status !== null && entry.status < 500)
            group.loggedOnly += 1;
        if (group.sampleRequestId === "")
            group.sampleRequestId = entry.requestId;
        slot.statuses.set(status, (slot.statuses.get(status) ?? 0) + 1);
        slot.routes.set(route, (slot.routes.get(route) ?? 0) + 1);
    }
    const order = (map) => [...map.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]));
    return [...groups.values()]
        .map(({ group, statuses, routes }) => ({ ...group, statuses: order(statuses), routes: order(routes) }))
        .sort((a, b) => b.count - a.count);
}
/** The hostname most of a poll's errors were served on, or "" when none is known. */
export function mainDomain(entries) {
    const counts = new Map();
    for (const entry of entries) {
        if (entry.domain !== "")
            counts.set(entry.domain, (counts.get(entry.domain) ?? 0) + 1);
    }
    return [...counts.entries()].sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))[0]?.[0] ?? "";
}
