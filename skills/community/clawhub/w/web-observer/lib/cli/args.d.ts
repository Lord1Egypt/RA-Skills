/**
 * Argument parsing.
 *
 * Every flag a command accepts is declared, and an undeclared flag is a usage
 * error naming what the command does accept. The alternative, ignoring it, is
 * how somebody comes to believe they ran a dry run when they did not: the flag
 * would be dropped, the alert would be sent, and nothing in the output would
 * mention it.
 */
/** Commands, with the flags each one accepts. */
export declare const COMMANDS: {
    readonly check: readonly ["--json", "--strict", "--only", "--dry-run"];
    readonly watch: readonly ["--dry-run"];
    readonly "vercel-watch": readonly ["--dry-run"];
    readonly digest: readonly ["--dry-run"];
    readonly vercel: readonly [];
    readonly ga4: readonly [];
    readonly doctor: readonly ["--json"];
    readonly schedule: readonly ["--apply", "--json"];
    readonly help: readonly [];
    readonly version: readonly [];
};
export type CommandName = keyof typeof COMMANDS;
export type Args = {
    command: CommandName;
    json: boolean;
    strict: boolean;
    dryRun: boolean;
    apply: boolean;
    /** Watch ids from `--only`, comma separated or repeated. */
    only: string[];
    /** Everything after the command, for the two delegating commands. */
    passthrough: string[];
};
/**
 * Parse a command line.
 *
 * @param argv Arguments after the program name.
 * @returns The parsed arguments.
 * @throws ConfigError for an unknown command, an unknown flag, or a value flag
 *   with nothing after it.
 */
export declare function parseArgs(argv: readonly string[]): Args;
export declare const USAGE = "web-observer <command> [flags]\n\nWatching\n  check [--json] [--strict] [--only ID] [--dry-run]\n                        Check every watch once, now, and print the results.\n                        --strict exits 3 when anything is down.\n  watch [--dry-run]     Scheduled uptime round. Checks what is due, alerts on a\n                        change, prints NO_REPLY when there is nothing to say.\n\nDelegating\n  vercel <preset> ...   Ask the vercel-insights skill (traffic, speed, errors).\n  ga4 <preset> ...      Ask the open-ga4 skill (traffic).\n  vercel-watch [--dry-run]\n                        Scheduled Vercel error-log and performance-budget poll.\n  digest [--dry-run]    Scheduled GA4 traffic digest.\n\nSetting up\n  doctor [--json]       Check the configuration, the two optional skills, and\n                        whether the scheduled jobs exist.\n  schedule [--apply]    Print the openclaw cron add commands for this config.\n                        --apply creates them.\n\nA scheduled command prints its message to stdout, which is what an OpenClaw cron\njob with --announce delivers to your chat. Printing exactly NO_REPLY is what\nkeeps it quiet, so a quiet run is a silent one.";
