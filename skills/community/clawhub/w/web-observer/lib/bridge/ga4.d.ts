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
import type { Config } from "../config.js";
import type { Env } from "../paths.js";
import { type RunResult, type SkillLocation } from "./delegate.js";
/** The slug the skill is installed under. */
export declare const GA4_SLUG = "open-ga4";
/** The environment variable that points at a copy directly. */
export declare const GA4_DIR_VAR = "WEB_OBSERVER_GA4_SKILL_DIR";
/** Where to send somebody who does not have it. */
export declare const GA4_REPO = "https://github.com/anatoli-iliev/open-ga4";
/**
 * Presets this bridge will forward.
 *
 * An allowlist rather than a passthrough of anything, so a typo is answered by
 * this tool naming the real presets instead of by the other skill's usage error,
 * and so a future subcommand of that skill cannot be reached through here
 * without somebody deciding it should be.
 */
export declare const GA4_PRESETS: readonly string[];
export type Ga4Status = {
    kind: "absent";
    message: string;
} | {
    kind: "unusable";
    location: SkillLocation;
    message: string;
} | {
    kind: "ready";
    location: SkillLocation;
    entry: string;
};
/**
 * Whether the GA4 skill is installed and runnable.
 *
 * Three outcomes rather than a boolean: "not installed" and "installed but its
 * built output is missing" need different advice, and conflating them sends
 * somebody to reinstall when the real fix is to build.
 */
export declare function ga4Status(env: Env): Ga4Status;
/**
 * Run a GA4 preset.
 *
 * @param status A `ready` status from {@link ga4Status}.
 * @param argv The preset and its flags, forwarded untouched.
 * @param env The environment to hand the child. Passed through so the skill
 *   reads its own credentials exactly as it would when invoked directly, which
 *   means Web Observer never holds them.
 */
export declare function runGa4(status: Extract<Ga4Status, {
    kind: "ready";
}>, argv: readonly string[], env: Env, timeoutMs?: number): Promise<RunResult>;
/**
 * Check a forwarded preset against the allowlist.
 *
 * @returns null when it is acceptable, and a message naming the real presets
 *   when it is not.
 */
export declare function rejectUnknownPreset(argv: readonly string[]): string | null;
/**
 * The arguments a scheduled digest runs with.
 *
 * @param property The property to report on, or null for open-ga4's default.
 */
export declare function digestArgv(config: Config, property: string | null): string[];
