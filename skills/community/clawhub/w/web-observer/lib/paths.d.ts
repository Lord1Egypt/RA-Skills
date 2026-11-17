/**
 * Where the configuration and the state live.
 *
 * Both sit under OpenClaw's state directory rather than inside the skill
 * directory, because every install route replaces the skill directory outright:
 * ClawHub copies files over it, `openclaw skills install` clones into it, and a
 * local path install is a directory copy. Anything durable kept there would be
 * lost on the first update, and losing state means re-alerting every site that
 * was already known to be down.
 *
 * `OPENCLAW_STATE_DIR` is honoured because `openclaw --profile <name>` and
 * `--dev` set it. A profile that shared one monitor's state with another would
 * have them overwrite each other's memory of what is down.
 */
export type Env = Record<string, string | undefined>;
/** OpenClaw's state directory, honouring a profile override. */
export declare function openclawStateDir(env: Env): string;
/** The directory holding this skill's configuration and state. */
export declare function dataDir(env: Env): string;
/**
 * The configuration file.
 *
 * `WEB_OBSERVER_CONFIG` overrides it outright, which is what makes a second
 * configuration testable and lets one machine watch two unrelated sets of URLs.
 */
export declare function configPath(env: Env): string;
/**
 * The state file.
 *
 * Follows `WEB_OBSERVER_CONFIG` when that names a file in another directory, so
 * a second configuration keeps its own state instead of quietly sharing the
 * first one's memory of what is down.
 */
export declare function statePath(env: Env): string;
/**
 * The skill's own root directory, derived from this module's location.
 *
 * An agent invokes a skill from its own working directory with whatever PATH the
 * gateway has, so neither a relative path nor a lookup on PATH can be trusted.
 * Resolving from `import.meta.url` is the only thing that holds wherever the
 * skill is installed, which is also why the generated cron commands embed an
 * absolute path rather than expecting a particular working directory.
 */
export declare function skillRoot(moduleUrl: string): string;
/** The command line a scheduled job runs: `node <root>/lib/cli.js`. */
export declare function cliEntry(moduleUrl: string): string;
