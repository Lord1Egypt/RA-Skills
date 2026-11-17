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
import { EXIT_BAD_NEWS, EXIT_CONFIG, EXIT_OK } from "../cli/exit.js";
import { line, note, table } from "../cli/render.js";
import { loadState, saveState } from "../state.js";
import { REASON_TEXT } from "../uptime/decide.js";
import { formatEvents, SILENT_TOKEN, stamp } from "../uptime/format.js";
import { runRound } from "../uptime/run.js";
/**
 * Why uptime cannot run, as a sentence, or null when it can.
 *
 * Separated from the commands because both need it and because the wording is
 * the whole value: "no watches configured" with the file path beats a stack
 * trace or a silent success.
 */
function uptimeBlocker(context) {
    const { uptime } = context.config;
    if (uptime.watches.length === 0) {
        return (`no watches are configured in ${context.configFile}. Add one under uptime.watches, ` +
            "for example {\"id\": \"site\", \"url\": \"https://example.com\"}, then run " +
            "web-observer check to try it");
    }
    if (!uptime.enabled) {
        return (`uptime is switched off in ${context.configFile}. Set uptime.enabled to true to ` +
            `check the ${uptime.watches.length} configured watch` +
            `${uptime.watches.length === 1 ? "" : "es"}`);
    }
    return null;
}
/** The rows of the `check` table. */
function checkRows(outcome) {
    return outcome.outcomes.map(({ watch, result }) => [
        watch.id,
        result.ok ? "up" : "DOWN",
        result.ok ? String(result.status) : result.status === null ? "-" : String(result.status),
        `${result.durationMs} ms`,
        String(result.attemptsUsed),
        result.ok ? "" : `${REASON_TEXT[result.reason]}: ${result.detail}`,
    ]);
}
/** `check`: run everything once and report, without changing any alert state. */
export async function runCheckCommand(context, options) {
    const blocker = uptimeBlocker(context);
    if (blocker !== null) {
        note(context.streams, `error: ${blocker}`);
        return EXIT_CONFIG;
    }
    if (options.only.length > 0) {
        const known = new Set(context.config.uptime.watches.map((watch) => watch.id));
        const unknown = options.only.filter((id) => !known.has(id));
        if (unknown.length > 0) {
            note(context.streams, `error: --only ${unknown[0]} names no configured watch. Configured: ` +
                `${[...known].join(", ")}`);
            return EXIT_CONFIG;
        }
    }
    const state = loadState(context.stateFile);
    const outcome = await runRound(context.config, state, context.deps, {
        ignoreSchedule: true,
        only: options.only,
    });
    const failures = outcome.outcomes.filter(({ result }) => !result.ok);
    if (options.json) {
        line(context.streams, JSON.stringify({
            checkedAt: new Date(context.deps.now()).toISOString(),
            watches: outcome.outcomes.map(({ watch, result }) => ({
                id: watch.id,
                url: watch.url,
                ok: result.ok,
                status: result.status ?? null,
                durationMs: result.durationMs,
                attemptsUsed: result.attemptsUsed,
                reason: result.ok ? null : result.reason,
                detail: result.ok ? null : result.detail,
            })),
            skipped: outcome.skipped.map((watch) => watch.id),
            upCount: outcome.outcomes.length - failures.length,
            downCount: failures.length,
        }, null, 2));
    }
    else {
        line(context.streams, `Web Observer check at ${stamp(context.deps.now())}`);
        line(context.streams);
        for (const row of table(["watch", "state", "status", "took", "tries", "detail"], checkRows(outcome))) {
            line(context.streams, row);
        }
        line(context.streams);
        line(context.streams, `${outcome.outcomes.length - failures.length} up, ${failures.length} down` +
            (outcome.skipped.length > 0 ? `, ${outcome.skipped.length} skipped (disabled)` : ""));
        if (failures.length === 0 && outcome.outcomes.length > 0) {
            // Said explicitly, because "no news" from a monitoring tool is the one
            // case where silence and success look identical.
            line(context.streams, "Everything configured is responding as expected.");
        }
    }
    // `check` deliberately does not persist. Somebody verifying a configuration
    // should not thereby consume the single alert a real outage is entitled to,
    // nor mark a site as recovered that the scheduled round has not yet seen.
    if (!options.dryRun && outcome.outcomes.length > 0) {
        note(context.streams, "note: check does not update alert state or the schedule; watch does that.");
    }
    if (options.strict && failures.length > 0)
        return EXIT_BAD_NEWS;
    return EXIT_OK;
}
/** `watch`: the scheduled round. Alerts on a change, otherwise says nothing. */
export async function runWatchCommand(context, options) {
    const blocker = uptimeBlocker(context);
    if (blocker !== null) {
        // Nothing on stdout: with cron's announce delivery, stdout is the message,
        // and a configuration problem is for the run log and the failure
        // notification, not for the chat where alerts about sites appear.
        note(context.streams, `error: ${blocker}`);
        return EXIT_CONFIG;
    }
    const state = loadState(context.stateFile);
    const outcome = await runRound(context.config, state, context.deps, {
        ignoreSchedule: false,
        only: [],
    });
    const message = formatEvents(outcome.events);
    if (options.dryRun) {
        note(context.streams, "dry run: the message below would have been delivered.");
        note(context.streams, message);
        note(context.streams, `dry run: state at ${context.stateFile} was not written, so nothing was consumed.`);
        line(context.streams, SILENT_TOKEN);
        return EXIT_OK;
    }
    persist(context, outcome.state);
    line(context.streams, message);
    // Exit 0 even having alerted. An alert is this tool working. A non-zero exit
    // would make cron's own failure notification fire alongside the alert just
    // delivered, and back the job off after a few rounds.
    return EXIT_OK;
}
/**
 * Write state, reporting a failure to stderr rather than throwing.
 *
 * A state file that cannot be written is a real problem worth naming, and it is
 * not a reason to discard an alert that has already been formatted: the next run
 * will re-alert, which is the right way to fail here.
 */
export function persist(context, state) {
    try {
        saveState(context.stateFile, state);
    }
    catch (error) {
        const reason = error instanceof Error ? error.message : String(error);
        note(context.streams, `warning: could not write ${context.stateFile}: ${reason}. ` +
            "Alert state is unchanged, so the next run may repeat this message.");
    }
}
