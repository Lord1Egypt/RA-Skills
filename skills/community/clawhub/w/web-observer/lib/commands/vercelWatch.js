/**
 * The scheduled Vercel poll: error logs, and the performance budget.
 *
 * Two watches share one command because two cron jobs call it, each on its own
 * interval, and each run does whichever parts are due. That keeps the alert-once
 * and recover-once rules in one place, and it means an error poll and a budget
 * check never disagree about what has already been reported.
 *
 * The three decisions worth knowing about:
 *
 * **The window widens to cover a gap.** Each poll asks for `windowMinutes`, or
 * for however long it has been since the last successful poll plus the
 * configured overlap, whichever is longer. If the Gateway was off for two hours,
 * the next poll looks back over those two hours instead of the usual twenty
 * minutes. This is safe only because the end of the window is never specified:
 * a window ending in the past is refused by the API with HTTP 400, while any
 * `--since` with the end left at now succeeds. Both facts were measured.
 *
 * **Deduplication is by request id.** Overlapping windows re-report the same
 * errors by construction, so an id already alerted about is not alerted about
 * again. That is what makes the overlap free.
 *
 * **An empty answer is not proof of health.** Runtime logs are retained for one
 * hour on Hobby, so a window longer than that can come back empty because the
 * logs aged out. The underlying skill says so in its notes, and those notes are
 * passed on rather than dropped.
 */
import { EXIT_CONFIG, EXIT_FAILURE, EXIT_OK } from "../cli/exit.js";
import { line, note } from "../cli/render.js";
import { loadState, pruneSeenIds, vercelStateOf, } from "../state.js";
import { SILENT_TOKEN, stamp } from "../uptime/format.js";
import { budgetArgv, errorsArgv, groupErrors, mainDomain, toSafeEntries, } from "../bridge/vercel.js";
/** The longest window one poll will ask for. */
export const MAX_WINDOW_MINUTES = 1_440;
/**
 * How far back this poll should look.
 *
 * @param windowMinutes The configured window.
 * @param intervalMinutes The configured interval; the difference between the two
 *   is the overlap the user asked for.
 * @param sinceLastPollMinutes Minutes since the last successful poll, or null
 *   when there has never been one.
 * @returns Minutes to ask for, never below the configured window and never above
 *   {@link MAX_WINDOW_MINUTES}.
 */
export function windowFor(windowMinutes, intervalMinutes, sinceLastPollMinutes) {
    const overlap = Math.max(1, windowMinutes - intervalMinutes);
    const needed = sinceLastPollMinutes === null ? windowMinutes : Math.ceil(sinceLastPollMinutes) + overlap;
    return Math.min(MAX_WINDOW_MINUTES, Math.max(windowMinutes, needed));
}
/** Whether enough time has passed for a part of this watch to run again. */
function isDue(lastAtMs, intervalMinutes, nowMs) {
    if (lastAtMs === null)
        return true;
    // A minute of slack, because a cron job fires a moment early as often as late,
    // and a poll skipped for being two seconds early would halve the cadence.
    return nowMs - lastAtMs >= intervalMinutes * 60_000 - 60_000;
}
/** Split a poll's entries into those already reported and those not. */
export function partitionNew(entries, seen) {
    const fresh = [];
    let repeated = 0;
    let withoutId = 0;
    for (const entry of entries) {
        if (entry.requestId === "") {
            // Nothing to deduplicate on. Counted and reported rather than dropped: a
            // failing request is not less real for lacking an id, and silently
            // ignoring it would undercount an incident.
            withoutId += 1;
            fresh.push(entry);
            continue;
        }
        if (Object.hasOwn(seen, entry.requestId)) {
            repeated += 1;
            continue;
        }
        fresh.push(entry);
    }
    return { fresh, repeated, withoutId };
}
/** How many distinct errors an alert lists before summarising the rest. */
export const MAX_GROUPS = 5;
function plural(count, word) {
    return `${count} ${word}${count === 1 ? "" : "s"}`;
}
function listed(pairs, limit) {
    const shown = pairs.slice(0, limit).map(([name, count]) => (pairs.length > 1 ? `${name} (${count})` : name));
    return shown.join(", ") + (pairs.length > limit ? ` and ${pairs.length - limit} more` : "");
}
/**
 * The alert text for a batch of new errors.
 *
 * Leads with the project and its domain, so the reader knows which site it is
 * before anything else, then lists each distinct error once with how often it
 * happened, where, and with what outcome. A flood of one error therefore reads
 * as one line with a count, not as a pile of routes.
 */
export function formatErrorAlert(project, fresh, payload, windowMinutes, includeMessages, atMs) {
    const domain = mainDomain(fresh);
    const site = domain !== "" && domain !== project ? `${project} (${domain})` : project;
    const groups = groupErrors(fresh);
    const lines = [
        `🟠 ${site}: ${plural(fresh.length, "new error")} on Vercel in the last ${windowMinutes} minutes, ` +
            `${groups.length === 1 ? "1 distinct" : `${groups.length} distinct`}:`,
    ];
    for (const [index, group] of groups.slice(0, MAX_GROUPS).entries()) {
        const where = `${group.method !== "" ? `${group.method} ` : ""}${listed(group.routes, 3)}`;
        const outcome = group.crashed > 0
            ? `crashed the function${group.crashed < group.count ? ` ${group.crashed} times` : ""}`
            : `status ${listed(group.statuses, 3)}`;
        const head = group.message !== null
            ? `${index + 1}. ${group.count} x "${group.message}"`
            : `${index + 1}. ${group.count} x ${where}`;
        lines.push(head);
        const detail = [group.message !== null ? `on ${where}` : null, outcome];
        if (group.loggedOnly === group.count) {
            detail.push(`not an HTTP failure; counted because it logged at ${group.level ?? "error"} level`);
        }
        lines.push(`   ${detail.filter((part) => part !== null).join("; ")}`);
        if (group.sampleRequestId !== "")
            lines.push(`   e.g. request ${group.sampleRequestId}`);
    }
    if (groups.length > MAX_GROUPS) {
        const rest = groups.slice(MAX_GROUPS).reduce((sum, group) => sum + group.count, 0);
        lines.push(`… and ${plural(groups.length - MAX_GROUPS, "more distinct error")} (${rest} in all)`);
    }
    if (payload.truncated) {
        lines.push("More errors matched than were fetched, so this is a sample rather than a full count.");
    }
    lines.push(`At: ${stamp(atMs)}`);
    if (!includeMessages) {
        lines.push("Log messages are not included (vercel.errors.includeMessages is off). " +
            `See them with: web-observer vercel errors --project ${project} --since ${windowMinutes}m`);
    }
    return lines.join("\n");
}
/** Why a delegated call failed, as a sentence, plus whether it is our fault. */
function describeFailure(result, what) {
    if (result.spawnFailed) {
        return `${what} could not be started: ${result.stderr.trim()}`;
    }
    if (result.timedOut) {
        return `${what} did not finish in time`;
    }
    const detail = (result.stderr.trim() || result.stdout.trim()).split("\n").slice(0, 4).join(" ");
    return `${what} exited ${result.code}: ${detail}`;
}
/**
 * Run whichever parts of the Vercel watch are due.
 *
 * @returns The exit code, and the message that was printed.
 */
export async function runVercelWatch(context, deps, options) {
    const { config, streams } = context;
    const nowMs = context.now();
    const state = loadState(context.stateFile);
    const blocks = [];
    let code = EXIT_OK;
    if (!config.vercel.enabled) {
        note(streams, `error: the vercel module is switched off in ${context.configFile}. ` +
            "Set vercel.enabled to true, or remove the scheduled job with " +
            "`openclaw cron rm web-observer-vercel-errors`.");
        return { code: EXIT_CONFIG, message: "", state };
    }
    if (deps.status.kind === "absent") {
        note(streams, `error: ${deps.status.message}`);
        return { code: EXIT_CONFIG, message: "", state };
    }
    if (deps.credentials.problems.length > 0) {
        for (const problem of deps.credentials.problems) {
            note(streams, `error: ${problem}`);
        }
        return { code: EXIT_CONFIG, message: "", state };
    }
    if (deps.credentials.env["VERCEL_TOKEN"] === undefined) {
        note(streams, "error: no Vercel token is configured. A scheduled cron job runs with the Gateway's " +
            "environment, so the token has to be readable from openclaw.json: set it with " +
            "`openclaw config set skills.entries.vercel-insights.apiKey YOUR_TOKEN`.");
        return { code: EXIT_CONFIG, message: "", state };
    }
    const nextVercel = {};
    const noLogsReported = { value: false };
    for (const [index, project] of config.vercel.projects.entries()) {
        const previous = vercelStateOf(state, project, index === 0);
        const vercel = { ...previous, seenRequestIds: { ...previous.seenRequestIds } };
        const projectCode = await pollProject(context, deps, project, vercel, nowMs, blocks, noLogsReported);
        // The most serious outcome wins: a configuration problem on one project
        // must not be hidden by another project polling cleanly.
        if (projectCode === EXIT_CONFIG || (projectCode !== EXIT_OK && code === EXIT_OK)) {
            code = projectCode;
        }
        nextVercel[project] = vercel;
    }
    const message = blocks.length === 0 ? SILENT_TOKEN : blocks.join("\n\n");
    // Projects no longer configured are dropped, along with any legacy entry.
    const nextState = { ...state, vercel: nextVercel };
    if (options.dryRun) {
        note(streams, "dry run: the message below would have been delivered.");
        note(streams, message);
        note(streams, "dry run: state was not written, so nothing was consumed.");
        line(streams, SILENT_TOKEN);
        return { code, message, state };
    }
    line(streams, message);
    return { code, message, state: nextState };
}
/**
 * Run whichever parts of the Vercel watch are due for one project.
 *
 * @param vercel This project's state, updated in place.
 * @param blocks Messages to deliver, appended to.
 * @param noLogsReported Shared across projects, so a missing logs surface is
 *   announced once rather than once per site.
 * @returns The exit code for this project alone.
 */
async function pollProject(context, deps, project, vercel, nowMs, blocks, noLogsReported) {
    const { config, streams } = context;
    const { errors, budget } = config.vercel;
    let code = EXIT_OK;
    // ---- error logs -------------------------------------------------------
    if (errors.enabled && isDue(vercel.lastPollAtMs, errors.intervalMinutes, nowMs)) {
        if (deps.status.kind === "no-logs") {
            // Reported once rather than every poll: an installed copy without the
            // logs surface will not fix itself, and a message every fifteen minutes
            // about it would be worse than the missing feature.
            if (!vercel.failing && !noLogsReported.value) {
                blocks.push(`⚠️ Vercel error watch cannot run: ${deps.status.message}`);
                noLogsReported.value = true;
            }
            if (!vercel.failing) {
                vercel.failing = true;
            }
            else {
                note(streams, `error: ${deps.status.message}`);
            }
            code = EXIT_CONFIG;
        }
        else {
            const sinceLastPoll = vercel.lastPollAtMs === null ? null : (nowMs - vercel.lastPollAtMs) / 60_000;
            const windowMinutes = windowFor(errors.windowMinutes, errors.intervalMinutes, sinceLastPoll);
            const result = await deps.invoke(errorsArgv(project, windowMinutes));
            if (result.code !== 0) {
                const failure = describeFailure(result, "the Vercel errors query");
                if (!vercel.failing) {
                    vercel.failing = true;
                    // A monitor problem, distinguished from a site problem in the text: the
                    // thing to look at is the token or the network, not the application.
                    blocks.push(`⚠️ Web Observer could not check Vercel errors for ${project}: ${failure}. ` +
                        "This is a problem with the check, not necessarily with the site.");
                }
                else {
                    note(streams, `error: ${failure}`);
                }
                code = result.code === 2 ? EXIT_CONFIG : EXIT_FAILURE;
            }
            else {
                let payload;
                try {
                    payload = toSafeEntries(JSON.parse(result.stdout), errors.includeMessages);
                }
                catch (error) {
                    const reason = error instanceof Error ? error.message : String(error);
                    note(streams, `error: could not read the Vercel errors output for ${project}: ${reason}`);
                    return EXIT_FAILURE;
                }
                if (vercel.failing) {
                    blocks.push(`✅ Web Observer can reach Vercel logs for ${project} again.`);
                    vercel.failing = false;
                }
                const { fresh, repeated } = partitionNew(payload.entries, vercel.seenRequestIds);
                vercel.lastPollAtMs = nowMs;
                if (fresh.length > errors.threshold) {
                    if (!vercel.alerting)
                        vercel.alerting = true;
                    // Ids are remembered only once they have actually been reported. A
                    // batch that stayed under the threshold is deliberately left
                    // unremembered, so it is counted again next time and a slow trickle
                    // still adds up to an alert. Marking everything seen on every poll
                    // would make any threshold above zero unreachable by a steady drip:
                    // two errors per poll would each be new once and never again.
                    for (const entry of fresh) {
                        if (entry.requestId !== "")
                            vercel.seenRequestIds[entry.requestId] = nowMs;
                    }
                    blocks.push(formatErrorAlert(project, fresh, payload, windowMinutes, errors.includeMessages, nowMs));
                }
                else if (vercel.alerting && payload.entries.length === 0) {
                    // Recovery needs the whole window clean, not merely free of anything
                    // new. Errors already reported are still in an overlapping window, and
                    // announcing "no errors in the last 20 minutes" while 20 minutes still
                    // holds two of them would be a false statement.
                    vercel.alerting = false;
                    blocks.push(`✅ ${project}: no Vercel errors in the last ${windowMinutes} minutes.` +
                        (payload.notes.some((note_) => note_.includes("retention"))
                            ? " Note: the window is longer than this plan's log retention, so this is " +
                                "not proof that nothing failed."
                            : ""));
                }
                // Kept for twice the window: an id cannot reappear in a window that no
                // longer reaches it, and holding them forever would grow the file.
                vercel.seenRequestIds = pruneSeenIds(vercel.seenRequestIds, nowMs, windowMinutes * 2 * 60_000);
                if (repeated > 0) {
                    note(streams, `note: ${repeated} error(s) in this window were already reported and were skipped.`);
                }
                for (const payloadNote of payload.notes) {
                    note(streams, `note: ${payloadNote}`);
                }
            }
        }
    }
    // ---- performance budget ----------------------------------------------
    if (budget.enabled &&
        isDue(vercel.lastBudgetPollAtMs, budget.intervalMinutes, nowMs)) {
        const result = await deps.invoke(budgetArgv(config, project));
        // Exit 3 is that skill's "the query worked and a threshold was exceeded",
        // which is the whole reason it exists and is not a failure.
        if (result.code === 3) {
            vercel.lastBudgetPollAtMs = nowMs;
            if (!vercel.budgetAlerting) {
                vercel.budgetAlerting = true;
                const thresholds = Object.entries(budget.metrics)
                    .map(([metric, value]) => `${metric} ${value}`)
                    .join(", ");
                blocks.push([
                    `🟠 ${project}: Core Web Vitals are over budget (${thresholds}).`,
                    // Speed Insights percentiles only. No part of this output is text a
                    // visitor or an application wrote, so it is safe to pass on whole.
                    ...result.stdout.trimEnd().split("\n").slice(0, 14),
                    `- At: ${stamp(nowMs)}`,
                ].join("\n"));
            }
        }
        else if (result.code === 0) {
            vercel.lastBudgetPollAtMs = nowMs;
            if (vercel.budgetAlerting) {
                vercel.budgetAlerting = false;
                blocks.push(`✅ ${project}: Core Web Vitals are back within budget.`);
            }
        }
        else {
            const failure = describeFailure(result, "the Vercel speed query");
            note(streams, `error: ${failure}`);
            code = result.code === 2 ? EXIT_CONFIG : EXIT_FAILURE;
        }
    }
    return code;
}
