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
import { readFileSync } from "node:fs";
import path from "node:path";
import { openclawStateDir } from "../paths.js";
function readOpenclawConfig(env) {
    try {
        const file = path.join(openclawStateDir(env), "openclaw.json");
        return JSON.parse(readFileSync(file, "utf8"));
    }
    catch {
        return null;
    }
}
/** `skills.entries.<slug>` from openclaw.json, or null. */
export function skillEntry(slug, env) {
    const document = readOpenclawConfig(env);
    const skills = document?.["skills"];
    if (typeof skills !== "object" || skills === null)
        return null;
    const entries = skills["entries"];
    if (typeof entries !== "object" || entries === null)
        return null;
    const entry = entries[slug];
    if (typeof entry !== "object" || entry === null || Array.isArray(entry))
        return null;
    return entry;
}
/** Whether a skill is explicitly disabled in the config. */
export function skillDisabled(slug, env) {
    return skillEntry(slug, env)?.enabled === false;
}
const INTERPOLATION = /^\$\{([A-Za-z_][A-Za-z0-9_]*)\}$/;
/**
 * Resolve one configured value.
 *
 * @returns The value, or a problem sentence naming what could not be resolved.
 */
function resolveValue(name, raw, env, slug) {
    if (typeof raw === "string") {
        const match = INTERPOLATION.exec(raw.trim());
        if (match) {
            const variable = match[1];
            const value = env[variable];
            if (value === undefined || value === "") {
                return {
                    problem: `skills.entries.${slug}.env.${name} is "\${${variable}}", but ${variable} is not ` +
                        "set in the environment this ran in. A scheduled cron job runs with the " +
                        "Gateway's environment, which is not your shell's, so an interpolation that " +
                        "works in a terminal can be empty here. Set a literal value, or set " +
                        `${variable} where the Gateway can see it`,
                };
            }
            return { value };
        }
        if (raw.trim() === "") {
            return { problem: `skills.entries.${slug}.env.${name} is empty` };
        }
        return { value: raw };
    }
    if (typeof raw === "object" && raw !== null) {
        // A SecretRef. Resolving one needs the Gateway's secret providers, which are
        // not reachable from here, so this is reported rather than attempted.
        return {
            problem: `skills.entries.${slug}.${name} is a secret reference, which only the Gateway can ` +
                "resolve, so a scheduled run cannot read it. Either give Web Observer its own copy " +
                `(openclaw config set skills.entries.web-observer.env.${name} ...) or set ${name} ` +
                "where the Gateway process can see it",
        };
    }
    return { problem: `skills.entries.${slug}.${name} is not a string` };
}
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
export function collectCredentials(spec, env) {
    const result = { env: {}, problems: [], sources: {} };
    const entry = skillEntry(spec.slug, env);
    const inherited = env[spec.primaryEnv];
    if (inherited !== undefined && inherited !== "") {
        result.env[spec.primaryEnv] = inherited;
        result.sources[spec.primaryEnv] = "inherited from the environment";
    }
    else if (entry?.apiKey !== undefined) {
        const resolved = resolveValue(spec.primaryEnv, entry.apiKey, env, spec.slug);
        if ("value" in resolved) {
            result.env[spec.primaryEnv] = resolved.value;
            result.sources[spec.primaryEnv] = `skills.entries.${spec.slug}.apiKey`;
        }
        else {
            result.problems.push(resolved.problem);
        }
    }
    const configured = typeof entry?.env === "object" && entry.env !== null && !Array.isArray(entry.env)
        ? entry.env
        : {};
    for (const name of [spec.primaryEnv, ...spec.optional]) {
        if (result.env[name] !== undefined)
            continue;
        const inheritedOptional = env[name];
        if (inheritedOptional !== undefined && inheritedOptional !== "") {
            result.env[name] = inheritedOptional;
            result.sources[name] = "inherited from the environment";
            continue;
        }
        if (!Object.hasOwn(configured, name))
            continue;
        const resolved = resolveValue(name, configured[name], env, spec.slug);
        if ("value" in resolved) {
            result.env[name] = resolved.value;
            result.sources[name] = `skills.entries.${spec.slug}.env.${name}`;
        }
        else {
            result.problems.push(resolved.problem);
        }
    }
    return result;
}
/**
 * The environment to hand a child process.
 *
 * Starts from this process's environment so a delegate keeps its PATH, HOME and
 * locale, then overlays the resolved credentials.
 */
export function childEnv(base, overlay) {
    return { ...base, ...overlay };
}
