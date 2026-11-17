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
import { existsSync } from "node:fs";
import { homedir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
/** OpenClaw's state directory, honouring a profile override. */
export function openclawStateDir(env) {
    const override = env["OPENCLAW_STATE_DIR"];
    if (override !== undefined && override.trim() !== "")
        return override;
    return path.join(homedir(), ".openclaw");
}
/** The directory holding this skill's configuration and state. */
export function dataDir(env) {
    return path.join(openclawStateDir(env), "web-observer");
}
/**
 * The configuration file.
 *
 * `WEB_OBSERVER_CONFIG` overrides it outright, which is what makes a second
 * configuration testable and lets one machine watch two unrelated sets of URLs.
 */
export function configPath(env) {
    const override = env["WEB_OBSERVER_CONFIG"];
    if (override !== undefined && override.trim() !== "")
        return override;
    return path.join(dataDir(env), "config.json");
}
/**
 * The state file.
 *
 * Follows `WEB_OBSERVER_CONFIG` when that names a file in another directory, so
 * a second configuration keeps its own state instead of quietly sharing the
 * first one's memory of what is down.
 */
export function statePath(env) {
    const override = env["WEB_OBSERVER_STATE"];
    if (override !== undefined && override.trim() !== "")
        return override;
    const config = env["WEB_OBSERVER_CONFIG"];
    if (config !== undefined && config.trim() !== "") {
        return path.join(path.dirname(config), "state.json");
    }
    return path.join(dataDir(env), "state.json");
}
/**
 * The skill's own root directory, derived from this module's location.
 *
 * An agent invokes a skill from its own working directory with whatever PATH the
 * gateway has, so neither a relative path nor a lookup on PATH can be trusted.
 * Resolving from `import.meta.url` is the only thing that holds wherever the
 * skill is installed, which is also why the generated cron commands embed an
 * absolute path rather than expecting a particular working directory.
 */
export function skillRoot(moduleUrl) {
    // Walk up to the directory that marks the skill's root, rather than assuming a
    // depth. A depth is wrong as soon as a module moves into a subdirectory, which
    // is exactly how this first produced `<root>/lib/lib/cli.js`: the caller had
    // moved from lib/ to lib/cli/ and the arithmetic did not.
    let current = path.dirname(fileURLToPath(moduleUrl));
    for (let up = 0; up < 6; up += 1) {
        if (existsSync(path.join(current, "SKILL.md")) || existsSync(path.join(current, "package.json"))) {
            return current;
        }
        const parent = path.dirname(current);
        if (parent === current)
            break;
        current = parent;
    }
    // Nothing marked a root. Returning the module's own directory keeps the result
    // absolute and obviously wrong in a message, rather than silently plausible.
    return path.dirname(fileURLToPath(moduleUrl));
}
/** The command line a scheduled job runs: `node <root>/lib/cli.js`. */
export function cliEntry(moduleUrl) {
    return path.join(skillRoot(moduleUrl), "lib", "cli.js");
}
