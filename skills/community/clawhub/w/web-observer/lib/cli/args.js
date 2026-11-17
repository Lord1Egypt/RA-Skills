/**
 * Argument parsing.
 *
 * Every flag a command accepts is declared, and an undeclared flag is a usage
 * error naming what the command does accept. The alternative, ignoring it, is
 * how somebody comes to believe they ran a dry run when they did not: the flag
 * would be dropped, the alert would be sent, and nothing in the output would
 * mention it.
 */
import { ConfigError } from "../config.js";
/** Commands, with the flags each one accepts. */
export const COMMANDS = {
    check: ["--json", "--strict", "--only", "--dry-run"],
    watch: ["--dry-run"],
    "vercel-watch": ["--dry-run"],
    digest: ["--dry-run"],
    vercel: [],
    ga4: [],
    doctor: ["--json"],
    schedule: ["--apply", "--json"],
    help: [],
    version: [],
};
/** Flags that take a value rather than standing alone. */
const VALUE_FLAGS = new Set(["--only"]);
function emptyArgs(command) {
    return {
        command,
        json: false,
        strict: false,
        dryRun: false,
        apply: false,
        only: [],
        passthrough: [],
    };
}
function isCommand(value) {
    return Object.hasOwn(COMMANDS, value);
}
/**
 * Parse a command line.
 *
 * @param argv Arguments after the program name.
 * @returns The parsed arguments.
 * @throws ConfigError for an unknown command, an unknown flag, or a value flag
 *   with nothing after it.
 */
export function parseArgs(argv) {
    const first = argv[0];
    if (first === undefined || first === "--help" || first === "-h")
        return emptyArgs("help");
    if (first === "--version" || first === "-V")
        return emptyArgs("version");
    if (!isCommand(first)) {
        const names = Object.keys(COMMANDS)
            .filter((name) => name !== "help" && name !== "version")
            .join(", ");
        throw new ConfigError("command", `${JSON.stringify(first)} is not a Web Observer command. Available: ${names}`);
    }
    const args = emptyArgs(first);
    const rest = argv.slice(1);
    // The two delegating commands forward their arguments untouched: the flags
    // belong to the other skill's command line, and this one has no business
    // holding an opinion about them. They are forwarded as an argument vector, so
    // no shell ever sees them.
    if (first === "vercel" || first === "ga4") {
        args.passthrough = [...rest];
        return args;
    }
    const accepted = COMMANDS[first];
    for (let index = 0; index < rest.length; index += 1) {
        const token = rest[index];
        if (!token.startsWith("-")) {
            throw new ConfigError("command", `${JSON.stringify(token)} is not expected after ${first}. ` +
                (accepted.length > 0
                    ? `It accepts ${accepted.join(", ")}`
                    : "It takes no arguments"));
        }
        const [name, inlineValue] = token.includes("=")
            ? [token.slice(0, token.indexOf("=")), token.slice(token.indexOf("=") + 1)]
            : [token, undefined];
        if (!accepted.includes(name)) {
            throw new ConfigError("command", `${name} is not a flag ${first} accepts. ` +
                (accepted.length > 0
                    ? `It accepts ${accepted.join(", ")}`
                    : "It takes no flags") +
                ". An unrecognised flag is refused rather than ignored, so a run can " +
                "never quietly differ from the one that was asked for");
        }
        if (VALUE_FLAGS.has(name)) {
            const value = inlineValue ?? rest[index + 1];
            if (value === undefined || value.startsWith("-")) {
                throw new ConfigError("command", `${name} needs a value, for example ${name} my-site`);
            }
            if (inlineValue === undefined)
                index += 1;
            if (name === "--only") {
                args.only.push(...value.split(",").map((part) => part.trim()).filter((part) => part !== ""));
            }
            continue;
        }
        if (inlineValue !== undefined) {
            throw new ConfigError("command", `${name} does not take a value`);
        }
        if (name === "--json")
            args.json = true;
        if (name === "--strict")
            args.strict = true;
        if (name === "--dry-run")
            args.dryRun = true;
        if (name === "--apply")
            args.apply = true;
    }
    return args;
}
export const USAGE = `web-observer <command> [flags]

Watching
  check [--json] [--strict] [--only ID] [--dry-run]
                        Check every watch once, now, and print the results.
                        --strict exits 3 when anything is down.
  watch [--dry-run]     Scheduled uptime round. Checks what is due, alerts on a
                        change, prints NO_REPLY when there is nothing to say.

Delegating
  vercel <preset> ...   Ask the vercel-insights skill (traffic, speed, errors).
  ga4 <preset> ...      Ask the open-ga4 skill (traffic).
  vercel-watch [--dry-run]
                        Scheduled Vercel error-log and performance-budget poll.
  digest [--dry-run]    Scheduled GA4 traffic digest.

Setting up
  doctor [--json]       Check the configuration, the two optional skills, and
                        whether the scheduled jobs exist.
  schedule [--apply]    Print the openclaw cron add commands for this config.
                        --apply creates them.

A scheduled command prints its message to stdout, which is what an OpenClaw cron
job with --announce delivers to your chat. Printing exactly NO_REPLY is what
keeps it quiet, so a quiet run is a silent one.`;
