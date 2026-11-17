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
import { EXIT_CONFIG, EXIT_FAILURE, EXIT_OK } from "../cli/exit.js";
import { line, note } from "../cli/render.js";
import { worstCaseRoundMs } from "../uptime/run.js";
/**
 * Quote a string for `sh -lc`.
 *
 * Single quotes, with any embedded single quote closed and reopened. A skill can
 * be installed under a path with a space in it, and an unquoted path would then
 * be two arguments.
 */
export function shellQuote(value) {
    return `'${value.split("'").join(`'\\''`)}'`;
}
/** "1 minute", "5 minutes": a count with its noun agreeing. */
export function plural(count, noun) {
    return `${count} ${noun}${count === 1 ? "" : "s"}`;
}
/** A whole number of seconds, with headroom, from a millisecond worst case. */
function timeoutFor(worstCaseMs, floorSeconds) {
    return Math.max(floorSeconds, Math.ceil((worstCaseMs * 2) / 1_000));
}
/**
 * Every job the configuration calls for, in a stable order.
 *
 * A module that is switched off contributes nothing, which is what makes the
 * three modules independently installable: someone using uptime alone gets one
 * job and is never asked about a Vercel token.
 */
export function plannedJobs(config) {
    const jobs = [];
    if (config.uptime.enabled && config.uptime.watches.length > 0) {
        const intervals = config.uptime.watches
            .filter((watch) => watch.enabled)
            .map((watch) => watch.intervalMinutes);
        jobs.push({
            name: "web-observer-uptime",
            module: "uptime",
            command: "watch",
            schedule: { kind: "every", value: `${config.uptime.tickMinutes}m` },
            timeoutSeconds: timeoutFor(worstCaseRoundMs(config.uptime.watches), 60),
            why: `ticks every ${plural(config.uptime.tickMinutes, "minute")} and checks whichever ` +
                `watches are due; the shortest configured interval is ` +
                `${plural(Math.min(...intervals), "minute")}`,
        });
    }
    if (config.vercel.enabled && config.vercel.errors.enabled) {
        jobs.push({
            name: "web-observer-vercel-errors",
            module: "vercel-errors",
            command: "vercel-watch",
            schedule: { kind: "every", value: `${config.vercel.errors.intervalMinutes}m` },
            // A logs query pages up to four times and a page took up to six seconds
            // against a live account, so the floor is generous rather than tight.
            timeoutSeconds: 180,
            why: `polls the last ${plural(config.vercel.errors.windowMinutes, "minute")} of error logs ` +
                `every ${plural(config.vercel.errors.intervalMinutes, "minute")}, deduplicating by ` +
                "request id",
        });
    }
    if (config.vercel.enabled && config.vercel.budget.enabled) {
        jobs.push({
            name: "web-observer-vercel-budget",
            module: "vercel-budget",
            command: "vercel-watch",
            schedule: { kind: "every", value: `${config.vercel.budget.intervalMinutes}m` },
            timeoutSeconds: 180,
            why: "checks Core Web Vitals against your thresholds every " +
                plural(config.vercel.budget.intervalMinutes, "minute"),
        });
    }
    if (config.ga4.enabled && config.ga4.digest.enabled) {
        jobs.push({
            name: "web-observer-ga4-digest",
            module: "ga4-digest",
            command: "digest",
            schedule: { kind: "cron", value: config.ga4.digest.cron },
            timeoutSeconds: 180,
            why: `sends a ${config.ga4.digest.since} traffic digest on the schedule ${config.ga4.digest.cron}`,
        });
    }
    return jobs;
}
/**
 * The `openclaw cron add` argument vector for one job.
 *
 * Returned as a vector rather than a string so `--apply` can spawn it without a
 * shell. The printed form is the same vector, quoted.
 */
export function cronAddArgv(job, config, cliPath) {
    const argv = ["cron", "add", "--name", job.name];
    if (job.schedule.kind === "every") {
        argv.push("--every", job.schedule.value);
    }
    else {
        argv.push("--cron", job.schedule.value);
    }
    argv.push("--command", `node ${shellQuote(cliPath)} ${job.command}`);
    argv.push("--timeout-seconds", String(job.timeoutSeconds));
    // Announce is what delivers stdout. Without it the job would run, decide
    // correctly that a site is down, and tell nobody.
    argv.push("--announce");
    if (config.notify.channel !== null)
        argv.push("--channel", config.notify.channel);
    if (config.notify.to !== null)
        argv.push("--to", config.notify.to);
    return argv;
}
/** The command as a person would type it, wrapped for readability. */
function printable(argv) {
    const parts = argv.map((part) => (/^[A-Za-z0-9_./:@=-]+$/.test(part) ? part : shellQuote(part)));
    return `openclaw ${parts.join(" ")}`;
}
export async function runScheduleCommand(context, options, deps) {
    const { config, streams, cliPath } = context;
    const jobs = plannedJobs(config);
    if (jobs.length === 0) {
        note(streams, `error: no module in ${context.configFile} is enabled, so there is nothing to schedule. ` +
            "Enable uptime, vercel or ga4 first.");
        return EXIT_CONFIG;
    }
    if (config.notify.channel === null || config.notify.to === null) {
        // A job without a destination still runs and still decides correctly; it
        // just tells nobody. Worth refusing rather than creating quietly.
        note(streams, `error: notify.channel and notify.to are not both set in ${context.configFile}, so a ` +
            "scheduled job would have nowhere to deliver an alert. Set them, for example " +
            '{"notify": {"channel": "telegram", "to": "telegram:123456"}}. ' +
            "Run `openclaw directory self` or check an existing job with `openclaw cron list` " +
            "to find the target you already use.");
        return EXIT_CONFIG;
    }
    if (options.json) {
        line(streams, JSON.stringify({
            jobs: jobs.map((job) => ({
                name: job.name,
                module: job.module,
                schedule: job.schedule,
                timeoutSeconds: job.timeoutSeconds,
                why: job.why,
                argv: cronAddArgv(job, config, cliPath),
            })),
        }, null, 2));
        if (!options.apply)
            return EXIT_OK;
    }
    const existing = new Set(await deps.existingJobNames());
    if (!options.apply) {
        if (!options.json) {
            line(streams, "Web Observer needs these OpenClaw cron jobs.");
            line(streams);
            for (const job of jobs) {
                line(streams, `# ${job.name}: ${job.why}`);
                if (existing.has(job.name)) {
                    line(streams, `# already exists; remove it first with: openclaw cron rm ${job.name}`);
                }
                line(streams, printable(cronAddArgv(job, config, cliPath)));
                line(streams);
            }
            line(streams, "Run `web-observer schedule --apply` to create the ones that are missing.");
        }
        return EXIT_OK;
    }
    let created = 0;
    let failed = 0;
    for (const job of jobs) {
        if (existing.has(job.name)) {
            note(streams, `skipping ${job.name}: a cron job with that name already exists.`);
            continue;
        }
        const result = await deps.runOpenclaw(cronAddArgv(job, config, cliPath));
        if (result.code === 0) {
            created += 1;
            line(streams, `created ${job.name}: ${job.why}`);
        }
        else {
            failed += 1;
            note(streams, `failed to create ${job.name}: ${result.stderr.trim() || result.stdout.trim()}`);
        }
    }
    if (created > 0) {
        line(streams, "");
        line(streams, "Check them with: openclaw cron list");
    }
    return failed > 0 ? EXIT_FAILURE : EXIT_OK;
}
