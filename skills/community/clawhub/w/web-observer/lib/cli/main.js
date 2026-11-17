/**
 * Dispatch: parse a command line, load what the command needs, run it.
 *
 * `main` returns an exit code instead of calling `process.exit`, and the built
 * shim sets `process.exitCode` from it. That is not a style preference:
 * `process.exit` truncates asynchronous writes to a pipe, and a cron job capturing
 * stdout is exactly a pipe. A truncated alert delivered with exit code 0 would be
 * the worst failure this tool could have, because it would look like it worked.
 */
import { readFileSync } from "node:fs";
import { collectCredentials } from "../bridge/credentials.js";
import { run as runProcess } from "../bridge/delegate.js";
import { ga4Status, runGa4 } from "../bridge/ga4.js";
import { prepare as prepareVercel, runVercel } from "../bridge/vercel.js";
import { ConfigError, emptyConfig, parseConfig } from "../config.js";
import { cliEntry, configPath, statePath } from "../paths.js";
import { liveDeps } from "../uptime/check.js";
import { VERSION } from "../version.js";
import { GA4_CREDENTIAL_SPEC, runDigestCommand, runGa4Command, runVercelCommand, } from "../commands/delegate.js";
import { diagnose, renderDoctor } from "../commands/doctor.js";
import { runScheduleCommand } from "../commands/schedule.js";
import { runCheckCommand, runWatchCommand } from "../commands/uptime.js";
import { runVercelWatch } from "../commands/vercelWatch.js";
import { parseArgs, USAGE } from "./args.js";
import { EXIT_CONFIG, EXIT_FAILURE, EXIT_OK } from "./exit.js";
import { line, note } from "./render.js";
import { deferErr, releaseErr, runLogPath } from "./runlog.js";
function loadConfig(file) {
    let text;
    try {
        text = readFileSync(file, "utf8");
    }
    catch (error) {
        const code = error.code;
        if (code === "ENOENT")
            return { config: null, error: null, exists: false };
        return {
            config: null,
            error: `${file} could not be read: ${error.message}`,
            exists: true,
        };
    }
    let document;
    try {
        document = JSON.parse(text);
    }
    catch (error) {
        return {
            config: null,
            // The parser's own position is the most useful thing about a JSON error,
            // so it is passed through rather than summarised.
            error: `${file} is not valid JSON: ${error.message}`,
            exists: true,
        };
    }
    try {
        return { config: parseConfig(document), error: null, exists: true };
    }
    catch (error) {
        if (error instanceof ConfigError)
            return { config: null, error: error.message, exists: true };
        throw error;
    }
}
/** List existing OpenClaw cron job names, or null when they cannot be listed. */
async function listCronJobNames() {
    const result = await runProcess("openclaw", ["cron", "list", "--json"], { timeoutMs: 30_000 });
    if (result.spawnFailed || result.code !== 0)
        return null;
    try {
        const document = JSON.parse(result.stdout);
        const rows = Array.isArray(document)
            ? document
            : document.jobs;
        if (!Array.isArray(rows))
            return null;
        return rows
            .map((row) => typeof row === "object" && row !== null ? row.name : undefined)
            .filter((name) => typeof name === "string");
    }
    catch {
        return null;
    }
}
/**
 * Run one command.
 *
 * @param argv Arguments after the program name.
 * @param env The process environment.
 * @param streams Where output goes.
 * @returns The exit code. Never throws for an expected failure.
 */
export async function main(argv, env, streams) {
    let args;
    try {
        args = parseArgs(argv);
    }
    catch (error) {
        if (error instanceof ConfigError) {
            note(streams, `error: ${error.message}`);
            note(streams, "");
            note(streams, USAGE);
            return EXIT_CONFIG;
        }
        throw error;
    }
    if (args.command === "help") {
        line(streams, USAGE);
        return EXIT_OK;
    }
    if (args.command === "version") {
        line(streams, VERSION);
        return EXIT_OK;
    }
    const configFile = configPath(env);
    const stateFile = statePath(env);
    const loaded = loadConfig(configFile);
    if (args.command === "doctor") {
        return renderDoctor(diagnose({
            config: loaded.config,
            configError: loaded.error,
            configFile,
            configExists: loaded.exists,
            stateFile,
            env,
            cronJobNames: await listCronJobNames(),
        }), streams, { json: args.json });
    }
    // The two ad hoc delegating commands need no configuration of their own: they
    // exist so somebody can ask a question, and requiring a config file first
    // would make the easy case need setup it does not use.
    if (args.command === "vercel" || args.command === "ga4") {
        const context = { config: loaded.config ?? emptyConfig(), streams, env };
        return args.command === "vercel"
            ? await runVercelCommand(context, args.passthrough)
            : await runGa4Command(context, args.passthrough);
    }
    if (!loaded.exists) {
        note(streams, `error: no configuration at ${configFile}. Copy examples/config.json from this skill's ` +
            "directory, edit it, then run `web-observer doctor` to check it.");
        return EXIT_CONFIG;
    }
    if (loaded.config === null) {
        note(streams, `error: ${loaded.error}`);
        note(streams, "Run `web-observer doctor` for the full picture.");
        return EXIT_CONFIG;
    }
    const config = loaded.config;
    // A scheduled run's stderr is delivered to the chat alongside its stdout, so
    // a successful one keeps its notes for the run log instead. See runlog.ts.
    const scheduled = (args.command === "watch" || args.command === "vercel-watch" || args.command === "digest") &&
        !args.dryRun;
    // Spread so the command keeps the narrowing the checks above gave it.
    const configured = { ...args, command: args.command };
    if (!scheduled)
        return await runConfigured(configured, config, configFile, stateFile, env, streams);
    const quiet = deferErr(streams);
    const code = await runConfigured(configured, config, configFile, stateFile, env, quiet);
    releaseErr(streams, quiet.held(), code, runLogPath(stateFile), args.command, Date.now());
    return code;
}
/** Run a command that needs a valid configuration. */
async function runConfigured(args, config, configFile, stateFile, env, streams) {
    switch (args.command) {
        case "check":
            return await runCheckCommand({ config, configFile, stateFile, streams, deps: liveDeps }, { json: args.json, strict: args.strict, only: args.only, dryRun: args.dryRun });
        case "watch":
            return await runWatchCommand({ config, configFile, stateFile, streams, deps: liveDeps }, { dryRun: args.dryRun });
        case "vercel-watch": {
            const { status, credentials } = prepareVercel(env);
            const outcome = await runVercelWatch({ config, configFile, stateFile, streams, env, now: liveDeps.now }, {
                status,
                credentials,
                invoke: async (delegateArgv) => {
                    if (status.kind === "absent") {
                        return {
                            code: 2,
                            stdout: "",
                            stderr: status.message,
                            timedOut: false,
                            spawnFailed: true,
                        };
                    }
                    return await runVercel({ status, credentials, env }, delegateArgv);
                },
            }, { dryRun: args.dryRun });
            if (!args.dryRun) {
                // Persisted even on a failed poll, so the "could not reach Vercel"
                // notice is not repeated every fifteen minutes. That includes a
                // configuration failure: with several projects, one of them failing
                // must not stop another's alert from being remembered as sent, and a
                // run refused before polling returns the state exactly as loaded.
                const { persist } = await import("../commands/uptime.js");
                persist({ config, configFile, stateFile, streams, deps: liveDeps }, outcome.state);
            }
            return outcome.code;
        }
        case "digest": {
            const status = ga4Status(env);
            const credentials = collectCredentials(GA4_CREDENTIAL_SPEC, env);
            return await runDigestCommand({ config, configFile, streams, env }, {
                status,
                credentials,
                invoke: async (delegateArgv) => {
                    if (status.kind !== "ready") {
                        return {
                            code: 2,
                            stdout: "",
                            stderr: status.message,
                            timedOut: false,
                            spawnFailed: true,
                        };
                    }
                    return await runGa4(status, delegateArgv, { ...env, ...credentials.env });
                },
            }, { dryRun: args.dryRun });
        }
        case "schedule":
            return await runScheduleCommand({ config, configFile, streams, cliPath: cliEntry(import.meta.url) }, { apply: args.apply, json: args.json }, {
                runOpenclaw: async (openclawArgv) => await runProcess("openclaw", openclawArgv, { timeoutMs: 60_000 }),
                existingJobNames: async () => (await listCronJobNames()) ?? [],
            });
        default: {
            // Unreachable: parseArgs only produces known commands. Handled rather than
            // asserted, so a future command added to COMMANDS and forgotten here says
            // so instead of failing obscurely.
            const unknown = args.command;
            note(streams, `error: ${String(unknown)} is not implemented`);
            return EXIT_FAILURE;
        }
    }
}
