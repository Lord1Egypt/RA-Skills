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
import { EXIT_CONFIG, EXIT_OK } from "../cli/exit.js";
import { line, table } from "../cli/render.js";
import { collectCredentials } from "../bridge/credentials.js";
import { ga4Status } from "../bridge/ga4.js";
import { prepare as prepareVercel, REQUIRED_LOGS_VERSION } from "../bridge/vercel.js";
import { plannedJobs } from "./schedule.js";
import { GA4_CREDENTIAL_SPEC } from "./delegate.js";
export const BLOCKED_ON_VALUES = [
    "ok",
    "no_config",
    "bad_config",
    "nothing_enabled",
    "no_watches",
    "no_notify_target",
    "no_cron_jobs",
    "vercel_skill_missing",
    "vercel_logs_missing",
    "vercel_credentials",
    "ga4_skill_missing",
    "ga4_credentials",
    "interval_shorter_than_tick",
];
/**
 * Examine everything and produce findings in blocking order.
 *
 * Pure, so the whole diagnosis is testable without a filesystem: the inputs are
 * gathered by the caller.
 */
export function diagnose(input) {
    const findings = [];
    const report = (finding) => findings.push(finding);
    if (!input.configExists) {
        report({
            check: "configuration",
            ok: false,
            blocking: true,
            blockedOn: "no_config",
            detail: `no configuration at ${input.configFile}. Copy the example from the skill's ` +
                "examples/config.json and edit it, then run web-observer check",
        });
        return finish(input, findings);
    }
    if (input.config === null) {
        report({
            check: "configuration",
            ok: false,
            blocking: true,
            blockedOn: "bad_config",
            detail: input.configError ?? `${input.configFile} could not be read`,
        });
        return finish(input, findings);
    }
    const config = input.config;
    report({
        check: "configuration",
        ok: true,
        blocking: false,
        detail: `${input.configFile} parses`,
    });
    const enabled = [
        config.uptime.enabled ? "uptime" : null,
        config.vercel.enabled ? "vercel" : null,
        config.ga4.enabled ? "ga4" : null,
    ].filter((name) => name !== null);
    if (enabled.length === 0) {
        report({
            check: "modules",
            ok: false,
            blocking: true,
            blockedOn: "nothing_enabled",
            detail: "no module is enabled. Set uptime.enabled, vercel.enabled or ga4.enabled to true. " +
                "They are independent: uptime needs no credentials at all",
        });
    }
    else {
        report({
            check: "modules",
            ok: true,
            blocking: false,
            detail: `enabled: ${enabled.join(", ")}`,
        });
    }
    // ---- uptime -----------------------------------------------------------
    if (config.uptime.enabled) {
        if (config.uptime.watches.length === 0) {
            report({
                check: "uptime watches",
                ok: false,
                blocking: true,
                blockedOn: "no_watches",
                detail: "uptime is enabled but no watches are configured",
            });
        }
        else {
            const active = config.uptime.watches.filter((watch) => watch.enabled);
            report({
                check: "uptime watches",
                ok: true,
                blocking: false,
                detail: `${active.length} active watch${active.length === 1 ? "" : "es"}` +
                    (active.length === config.uptime.watches.length
                        ? ""
                        : ` (${config.uptime.watches.length - active.length} disabled)`),
            });
            // A watch that wants checking more often than the job runs is the one
            // misconfiguration whose symptom is a cadence that silently differs from
            // the one written down.
            const tooFast = active.filter((watch) => watch.intervalMinutes < config.uptime.tickMinutes);
            if (tooFast.length > 0) {
                report({
                    check: "uptime cadence",
                    ok: false,
                    blocking: true,
                    blockedOn: "interval_shorter_than_tick",
                    detail: `${tooFast.map((watch) => watch.id).join(", ")} ` +
                        (tooFast.length === 1 ? "asks" : "ask") +
                        ` for an interval below uptime.tickMinutes (${config.uptime.tickMinutes}), so ` +
                        (tooFast.length === 1 ? "it would" : "they would") +
                        ` actually be checked every ${config.uptime.tickMinutes} minutes. Lower ` +
                        "tickMinutes, or raise the interval",
                });
            }
            const notMultiples = active.filter((watch) => watch.intervalMinutes >= config.uptime.tickMinutes &&
                watch.intervalMinutes % config.uptime.tickMinutes !== 0);
            if (notMultiples.length > 0) {
                report({
                    check: "uptime cadence",
                    ok: false,
                    blocking: false,
                    detail: `${notMultiples.map((watch) => watch.id).join(", ")} have intervals that are not ` +
                        `multiples of tickMinutes (${config.uptime.tickMinutes}), so each check lands on ` +
                        "the first tick after it comes due and the effective interval is a little longer " +
                        "than configured",
                });
            }
        }
    }
    // ---- vercel -----------------------------------------------------------
    if (config.vercel.enabled) {
        const { status, credentials } = prepareVercel(input.env);
        if (status.kind === "absent") {
            report({
                check: "vercel-insights skill",
                ok: false,
                blocking: true,
                blockedOn: "vercel_skill_missing",
                detail: status.message,
            });
        }
        else {
            report({
                check: "vercel-insights skill",
                ok: true,
                blocking: false,
                detail: `${status.location.version ?? "unknown version"} at ${status.location.dir}`,
            });
            if (status.kind === "no-logs") {
                report({
                    check: "vercel request logs",
                    ok: false,
                    // Blocking only when something actually needs it.
                    blocking: config.vercel.errors.enabled,
                    blockedOn: "vercel_logs_missing",
                    detail: status.message,
                });
            }
            else {
                report({
                    check: "vercel request logs",
                    ok: true,
                    blocking: false,
                    detail: `present (needs ${REQUIRED_LOGS_VERSION} or later)`,
                });
            }
            if (credentials.env["VERCEL_TOKEN"] === undefined || credentials.problems.length > 0) {
                report({
                    check: "vercel token",
                    ok: false,
                    blocking: true,
                    blockedOn: "vercel_credentials",
                    detail: credentials.problems[0] ??
                        "no Vercel token is readable. Set it with `openclaw config set " +
                            "skills.entries.vercel-insights.apiKey YOUR_TOKEN`, scoped to the account or " +
                            "team rather than one project, because request logs and Speed Insights are " +
                            "account-scoped",
                });
            }
            else {
                report({
                    check: "vercel token",
                    ok: true,
                    blocking: false,
                    // The source, never the value.
                    detail: `from ${credentials.sources["VERCEL_TOKEN"]}`,
                });
            }
            if (config.vercel.errors.includeMessages) {
                report({
                    check: "vercel log messages",
                    ok: true,
                    blocking: false,
                    detail: "includeMessages is on, so raw application log text will be sent to your chat. " +
                        "That text is not redacted by the underlying skill and can contain secrets or " +
                        "customer data",
                });
            }
        }
    }
    // ---- ga4 --------------------------------------------------------------
    if (config.ga4.enabled) {
        const status = ga4Status(input.env);
        if (status.kind !== "ready") {
            report({
                check: "open-ga4 skill",
                ok: false,
                blocking: true,
                blockedOn: "ga4_skill_missing",
                detail: status.message,
            });
        }
        else {
            report({
                check: "open-ga4 skill",
                ok: true,
                blocking: false,
                detail: `${status.location.version ?? "unknown version"} at ${status.location.dir}`,
            });
            const credentials = collectCredentials(GA4_CREDENTIAL_SPEC, input.env);
            const hasCredential = credentials.env["GA4_CREDENTIALS"] !== undefined ||
                credentials.env["GOOGLE_APPLICATION_CREDENTIALS"] !== undefined;
            if (!hasCredential || credentials.problems.length > 0) {
                report({
                    check: "ga4 credentials",
                    ok: false,
                    blocking: true,
                    blockedOn: "ga4_credentials",
                    detail: credentials.problems[0] ??
                        "no GA4 service-account credential is readable. open-ga4's own `doctor --json` " +
                            "walks through setting one up",
                });
            }
            else {
                report({
                    check: "ga4 credentials",
                    ok: true,
                    blocking: false,
                    detail: `from ${credentials.sources["GA4_CREDENTIALS"] ??
                        credentials.sources["GOOGLE_APPLICATION_CREDENTIALS"]}`,
                });
            }
        }
    }
    // ---- delivery and scheduling -----------------------------------------
    if (enabled.length > 0) {
        if (config.notify.channel === null || config.notify.to === null) {
            report({
                check: "alert destination",
                ok: false,
                blocking: true,
                blockedOn: "no_notify_target",
                detail: "notify.channel and notify.to are not both set, so a scheduled job would have " +
                    'nowhere to deliver an alert. For Telegram: {"channel": "telegram", "to": ' +
                    '"telegram:<chat id>"}',
            });
        }
        else {
            report({
                check: "alert destination",
                ok: true,
                blocking: false,
                detail: `${config.notify.channel} -> ${config.notify.to}`,
            });
        }
        const wanted = plannedJobs(config);
        if (input.cronJobNames === null) {
            report({
                check: "scheduled jobs",
                ok: false,
                blocking: false,
                detail: "could not list OpenClaw cron jobs, so whether the schedule exists is unknown. " +
                    "Check `openclaw cron list` and that the Gateway is running",
            });
        }
        else {
            const missing = wanted.filter((job) => !input.cronJobNames?.includes(job.name));
            if (missing.length > 0) {
                report({
                    check: "scheduled jobs",
                    ok: false,
                    blocking: true,
                    blockedOn: "no_cron_jobs",
                    detail: `${missing.map((job) => job.name).join(", ")} ${missing.length === 1 ? "is" : "are"} not scheduled, so nothing runs on its own. Run \`web-observer schedule\` to see ` +
                        "the commands, or `web-observer schedule --apply` to create them",
                });
            }
            else {
                report({
                    check: "scheduled jobs",
                    ok: true,
                    blocking: false,
                    detail: `${wanted.length} job${wanted.length === 1 ? "" : "s"} scheduled`,
                });
            }
        }
    }
    return finish(input, findings);
}
function finish(input, findings) {
    const blocker = findings.find((finding) => finding.blocking && !finding.ok);
    return {
        ok: blocker === undefined,
        blocked_on: blocker?.blockedOn ?? "ok",
        next: blocker?.detail ?? null,
        configFile: input.configFile,
        stateFile: input.stateFile,
        findings,
    };
}
/** Render a report, and return the exit code it implies. */
export function renderDoctor(report, streams, options) {
    if (options.json) {
        line(streams, JSON.stringify(report, null, 2));
        return report.ok ? EXIT_OK : EXIT_CONFIG;
    }
    line(streams, "Web Observer doctor");
    line(streams);
    line(streams, `config  ${report.configFile}`);
    line(streams, `state   ${report.stateFile}`);
    line(streams);
    for (const row of table(["", "check", "detail"], report.findings.map((finding) => [
        finding.ok ? "ok" : finding.blocking ? "FAIL" : "warn",
        finding.check,
        finding.detail,
    ]))) {
        line(streams, row);
    }
    line(streams);
    if (report.ok) {
        line(streams, "Ready. Nothing is blocking.");
    }
    else {
        line(streams, `Blocked on: ${report.blocked_on}`);
        line(streams, `Next: ${report.next ?? ""}`);
    }
    return report.ok ? EXIT_OK : EXIT_CONFIG;
}
