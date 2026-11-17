/**
 * The commands that hand a question to another skill.
 *
 * `vercel` and `ga4` are for questions asked in conversation. `digest` is the
 * scheduled GA4 summary. All three exist so that Web Observer is one surface for
 * "how is my site doing", rather than three skills a person has to remember the
 * names of.
 *
 * Output is relayed rather than reformatted. Both delegated skills already lay
 * their answers out for a person to read, and re-typesetting a table is how a
 * number comes to differ between two tools that queried the same thing once.
 */
import { EXIT_CONFIG, EXIT_FAILURE, EXIT_OK } from "../cli/exit.js";
import { line, note } from "../cli/render.js";
import { GA4_ENV_VARS } from "../env.js";
import { childEnv, collectCredentials } from "../bridge/credentials.js";
import { digestArgv, ga4Status, GA4_SLUG, rejectUnknownPreset as rejectGa4Preset, runGa4, } from "../bridge/ga4.js";
import { prepare as prepareVercel, rejectUnknownPreset as rejectVercelPreset, runVercel, VERCEL_LOG_PRESETS, } from "../bridge/vercel.js";
import { SILENT_TOKEN } from "../uptime/format.js";
/** The variables open-ga4 reads, forwarded when configured. Canonical list in env.ts. */
export const GA4_CREDENTIAL_SPEC = {
    slug: GA4_SLUG,
    primaryEnv: GA4_ENV_VARS[0],
    optional: GA4_ENV_VARS.slice(1),
};
/** Relay a delegated run's output and translate its exit code. */
function relay(streams, result, what) {
    if (result.spawnFailed) {
        note(streams, `error: ${what} could not be started: ${result.stderr.trim()}`);
        return EXIT_FAILURE;
    }
    if (result.timedOut) {
        note(streams, `error: ${what} did not finish in time.`);
        return EXIT_FAILURE;
    }
    if (result.stdout !== "")
        streams.out(result.stdout);
    if (result.stderr !== "")
        streams.err(result.stderr);
    // The delegate's own code is passed through, so `--budget`'s exit 3 and an
    // empty-but-successful result keep the meanings its documentation gives them.
    return result.code;
}
/** `web-observer vercel <preset> ...` */
export async function runVercelCommand(context, passthrough) {
    const rejection = rejectVercelPreset(passthrough);
    if (rejection !== null) {
        note(context.streams, `error: ${rejection}`);
        return EXIT_CONFIG;
    }
    const { status, credentials } = prepareVercel(context.env);
    if (status.kind === "absent") {
        note(context.streams, `error: ${status.message}`);
        return EXIT_CONFIG;
    }
    const preset = passthrough[0];
    if (status.kind === "no-logs" && VERCEL_LOG_PRESETS.includes(preset)) {
        note(context.streams, `error: ${status.message}`);
        return EXIT_CONFIG;
    }
    for (const problem of credentials.problems) {
        note(context.streams, `warning: ${problem}`);
    }
    const result = await runVercel({ status, credentials, env: context.env }, passthrough);
    return relay(context.streams, result, "vercel-insights");
}
/** `web-observer ga4 <preset> ...` */
export async function runGa4Command(context, passthrough) {
    const rejection = rejectGa4Preset(passthrough);
    if (rejection !== null) {
        note(context.streams, `error: ${rejection}`);
        return EXIT_CONFIG;
    }
    const status = ga4Status(context.env);
    if (status.kind !== "ready") {
        note(context.streams, `error: ${status.message}`);
        return EXIT_CONFIG;
    }
    const credentials = collectCredentials(GA4_CREDENTIAL_SPEC, context.env);
    for (const problem of credentials.problems) {
        note(context.streams, `warning: ${problem}`);
    }
    const result = await runGa4(status, passthrough, childEnv(context.env, credentials.env));
    return relay(context.streams, result, GA4_SLUG);
}
/**
 * `digest`: the scheduled traffic summary.
 *
 * Unlike the ad hoc commands, this one runs unattended and its stdout is
 * delivered to a chat, so a failure must not become a message: printing the
 * silent token and exiting non-zero puts the problem in the run log and lets
 * cron's own failure notification handle it, instead of sending somebody a
 * stack trace at nine in the morning every Monday.
 */
export async function runDigestCommand(context, deps, options) {
    if (!context.config.ga4.enabled) {
        note(context.streams, `error: the ga4 module is switched off in ${context.configFile}. Set ga4.enabled to ` +
            "true, or remove the job with `openclaw cron rm web-observer-ga4-digest`.");
        return EXIT_CONFIG;
    }
    if (deps.status.kind !== "ready") {
        note(context.streams, `error: ${deps.status.message}`);
        return EXIT_CONFIG;
    }
    if (deps.credentials.problems.length > 0) {
        for (const problem of deps.credentials.problems) {
            note(context.streams, `error: ${problem}`);
        }
        return EXIT_CONFIG;
    }
    // One section per property. A property that fails is reported in the run log
    // and the others are still delivered: one broken credential should not cost
    // every other site its digest.
    const properties = context.config.ga4.properties;
    const targets = properties.length === 0 ? [null] : properties;
    const since = context.config.ga4.digest.since;
    const sections = [];
    let code = EXIT_OK;
    for (const property of targets) {
        const result = await deps.invoke(digestArgv(context.config, property));
        if (result.code !== 0 || result.stdout.trim() === "") {
            const detail = result.spawnFailed
                ? result.stderr.trim()
                : result.timedOut
                    ? "it did not finish in time"
                    : (result.stderr.trim() || result.stdout.trim()).split("\n").slice(0, 4).join(" ");
            const which = property === null ? "" : ` for property ${property}`;
            note(context.streams, `error: the GA4 digest${which} failed: ${detail}`);
            if (code !== EXIT_CONFIG)
                code = result.code === 2 ? EXIT_CONFIG : EXIT_FAILURE;
            continue;
        }
        const heading = targets.length > 1
            ? `📈 Traffic digest for property ${property}, last ${since}`
            : `📈 Traffic digest, last ${since}`;
        sections.push(`${heading}\n\n${result.stdout.trimEnd()}`);
    }
    if (sections.length === 0)
        return code;
    const message = sections.join("\n\n");
    if (options.dryRun) {
        note(context.streams, "dry run: the message below would have been delivered.");
        note(context.streams, message);
        line(context.streams, SILENT_TOKEN);
        return code;
    }
    line(context.streams, message);
    return code;
}
