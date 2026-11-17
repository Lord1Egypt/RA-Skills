/**
 * The GA4 bridge: everything Web Observer knows about the `open-ga4` skill.
 *
 * That skill answers traffic questions from Google Analytics 4, and nothing here
 * duplicates it. This module locates it, runs it, and turns its absence into a
 * sentence somebody can act on.
 *
 * The whole of the coupling is in this file, which is the point: `open-ga4` is
 * optional, and a Web Observer installed only for uptime watching must never fail
 * because a skill it does not use is not installed.
 */
import path from "node:path";
import { fileExists, findSkill, run } from "./delegate.js";
/** The slug the skill is installed under. */
export const GA4_SLUG = "open-ga4";
/** The environment variable that points at a copy directly. */
export const GA4_DIR_VAR = "WEB_OBSERVER_GA4_SKILL_DIR";
/** Where to send somebody who does not have it. */
export const GA4_REPO = "https://github.com/anatoli-iliev/open-ga4";
/**
 * Presets this bridge will forward.
 *
 * An allowlist rather than a passthrough of anything, so a typo is answered by
 * this tool naming the real presets instead of by the other skill's usage error,
 * and so a future subcommand of that skill cannot be reached through here
 * without somebody deciding it should be.
 */
export const GA4_PRESETS = [
    "report",
    "compare",
    "live",
    "query",
    "fields",
    "properties",
    "doctor",
];
/**
 * Whether the GA4 skill is installed and runnable.
 *
 * Three outcomes rather than a boolean: "not installed" and "installed but its
 * built output is missing" need different advice, and conflating them sends
 * somebody to reinstall when the real fix is to build.
 */
export function ga4Status(env) {
    const location = findSkill(GA4_SLUG, env, GA4_DIR_VAR);
    if (location === null) {
        return {
            kind: "absent",
            message: `the ${GA4_SLUG} skill is not installed, so traffic questions cannot be answered. ` +
                `Install it with: openclaw skills install git:${GA4_REPO} --as ${GA4_SLUG}`,
        };
    }
    const entry = path.join(location.dir, "lib", "cli.js");
    if (!fileExists(entry)) {
        return {
            kind: "unusable",
            location,
            message: `${GA4_SLUG} is installed at ${location.dir} but ${entry} is missing, so it cannot ` +
                "run. That directory ships a built lib/; reinstall it, or run `npm run build` there " +
                "if it is a development checkout",
        };
    }
    return { kind: "ready", location, entry };
}
/**
 * Run a GA4 preset.
 *
 * @param status A `ready` status from {@link ga4Status}.
 * @param argv The preset and its flags, forwarded untouched.
 * @param env The environment to hand the child. Passed through so the skill
 *   reads its own credentials exactly as it would when invoked directly, which
 *   means Web Observer never holds them.
 */
export async function runGa4(status, argv, env, timeoutMs = 120_000) {
    return await run("node", [status.entry, ...argv], {
        cwd: status.location.dir,
        env: env,
        timeoutMs,
    });
}
/**
 * Check a forwarded preset against the allowlist.
 *
 * @returns null when it is acceptable, and a message naming the real presets
 *   when it is not.
 */
export function rejectUnknownPreset(argv) {
    const preset = argv[0];
    if (preset === undefined) {
        return `name a preset. ${GA4_SLUG} offers: ${GA4_PRESETS.join(", ")}`;
    }
    if (preset.startsWith("-")) {
        return (`the first argument must be a preset, not ${preset}. ` +
            `${GA4_SLUG} offers: ${GA4_PRESETS.join(", ")}`);
    }
    if (!GA4_PRESETS.includes(preset)) {
        return `${preset} is not a ${GA4_SLUG} preset. It offers: ${GA4_PRESETS.join(", ")}`;
    }
    return null;
}
/**
 * The arguments a scheduled digest runs with.
 *
 * @param property The property to report on, or null for open-ga4's default.
 */
export function digestArgv(config, property) {
    const argv = [config.ga4.digest.preset, "--since", config.ga4.digest.since];
    if (property !== null)
        argv.push("--property", property);
    return argv;
}
