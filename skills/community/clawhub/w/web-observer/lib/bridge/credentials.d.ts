/**
 * Handing a delegated skill the credentials it is already configured with.
 *
 * This module exists because of a verified fact about OpenClaw: a cron job with a
 * `command` payload runs with the **Gateway's** environment, not a skill's. A
 * probe job on OpenClaw 2026.7.1-2 printed `VERCEL_TOKEN set= len=0`, so the
 * `skills.entries.<slug>.env` and `apiKey` values that reach a skill during a
 * chat turn are simply absent from a scheduled run.
 *
 * That leaves three ways to give a scheduled poll a token, and the choice
 * matters:
 *
 * 1. Put it in the cron job with `--command-env`. Refused: that copies a secret
 *    into a second file, in plaintext, where nobody will remember it lives.
 * 2. Ask the user to configure the same token twice, once for each skill.
 *    Supported, but not required, because a duplicated secret is a secret that
 *    gets rotated in one place only.
 * 3. Read what the delegated skill is already configured with, from
 *    `openclaw.json`, and pass it to that same skill in its own environment.
 *    This is the default: the secret keeps living in exactly one place.
 *
 * The rules that make (3) defensible, and each is a test:
 *
 * - A value read here is passed to the child process's environment and nowhere
 *   else. It is never put on a command line (a flag is visible to a model and to
 *   `ps`), never printed, and never written to a file.
 * - A `SecretRef` cannot be resolved here, and is reported as such rather than
 *   guessed at or silently dropped.
 * - A `"${VAR}"` interpolation that has nothing to interpolate is reported, not
 *   passed on as an empty string. An empty token produces a confusing 403; a
 *   named missing variable produces a fix.
 */
import { type Env } from "../paths.js";
/** What went wrong, or what was found, for one skill's credentials. */
export type CredentialResult = {
    /** Variables to overlay on the child's environment. Never logged. */
    env: Record<string, string>;
    /**
     * Problems that stop a credential being resolved, as whole sentences.
     *
     * Reported rather than thrown: a missing team id is worth saying while the
     * token still works, and `doctor` shows all of them at once.
     */
    problems: string[];
    /** Where each variable came from, for `doctor`. Values are never included. */
    sources: Record<string, string>;
};
/** The `skills.entries.<slug>` shape this module reads. */
type SkillEntry = {
    enabled?: unknown;
    apiKey?: unknown;
    env?: unknown;
};
/** `skills.entries.<slug>` from openclaw.json, or null. */
export declare function skillEntry(slug: string, env: Env): SkillEntry | null;
/** Whether a skill is explicitly disabled in the config. */
export declare function skillDisabled(slug: string, env: Env): boolean;
export type CredentialSpec = {
    /** The delegated skill's slug in openclaw.json. */
    slug: string;
    /** The variable its `apiKey` maps to, its `primaryEnv`. */
    primaryEnv: string;
    /** Other variables worth forwarding when configured. */
    optional: readonly string[];
};
/**
 * Collect the environment a delegated skill needs.
 *
 * Precedence, most specific first:
 *
 * 1. The variable already present in this process's environment. A manual run in
 *    a terminal that has the token should use it, and so should a Web Observer
 *    given its own copy through `skills.entries.web-observer.env`.
 * 2. `skills.entries.<slug>.apiKey` for the primary variable.
 * 3. `skills.entries.<slug>.env.<name>` for anything else.
 *
 * @returns The overlay, and any problems. An empty overlay with no problems
 *   means nothing was configured anywhere.
 */
export declare function collectCredentials(spec: CredentialSpec, env: Env): CredentialResult;
/**
 * The environment to hand a child process.
 *
 * Starts from this process's environment so a delegate keeps its PATH, HOME and
 * locale, then overlays the resolved credentials.
 */
export declare function childEnv(base: Env, overlay: Record<string, string>): Record<string, string | undefined>;
export {};
