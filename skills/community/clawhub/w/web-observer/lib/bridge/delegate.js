/**
 * Finding and running another OpenClaw skill.
 *
 * Web Observer reimplements neither Vercel nor GA4 access. It runs the two
 * skills that already do that, which makes this module the seam between them and
 * the only place that knows how a skill is laid out on disk.
 *
 * OpenClaw offers nothing to declare a dependency on another skill: the complete
 * `metadata.openclaw` field set carries `requires.bins`, `requires.anyBins`,
 * `requires.env` and `requires.config`, and `install` specs that install
 * binaries. None of them names a sibling skill, and there is no manifest field
 * that pins one to a git ref. So a dependency here is a runtime discovery, and
 * absence has to be a clear sentence rather than a stack trace.
 *
 * Two rules:
 *
 * - **Argument vectors, never shell strings.** Everything spawned goes through
 *   `spawn(file, argv)` with no shell, so a project name or a route pattern
 *   cannot become a command.
 * - **Output is bounded.** A delegate that prints without end must not exhaust
 *   memory in a monitor that runs every few minutes.
 */
import { spawn } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { homedir } from "node:os";
import path from "node:path";
import { openclawStateDir } from "../paths.js";
/** Read `version:` out of a SKILL.md without a YAML parser. */
export function readSkillVersion(skillFile) {
    let text;
    try {
        text = readFileSync(skillFile, "utf8");
    }
    catch {
        return null;
    }
    // Only the frontmatter is considered: a `version:` in prose further down is
    // not the skill's version, and matching it would report a wrong number
    // confidently.
    const end = text.indexOf("\n---", 3);
    const frontmatter = text.startsWith("---") && end > 0 ? text.slice(0, end) : "";
    const match = /^version:\s*(.+)$/m.exec(frontmatter);
    return match?.[1]?.trim() ?? null;
}
/**
 * The directories a skill can be installed in, most specific first.
 *
 * Mirrors OpenClaw's own precedence: the agent workspace, then the
 * per-workspace agent directory, then the shared agent profile, then the shared
 * state directory. The workspace is read from `openclaw.json` when it is
 * configured there, because it need not be `<state>/workspace`.
 */
export function skillSearchDirs(env) {
    const state = openclawStateDir(env);
    const dirs = [];
    const workspace = configuredWorkspace(state);
    if (workspace !== null) {
        dirs.push(path.join(workspace, "skills"));
        dirs.push(path.join(workspace, ".agents", "skills"));
    }
    dirs.push(path.join(state, "workspace", "skills"));
    dirs.push(path.join(state, "workspace", ".agents", "skills"));
    dirs.push(path.join(homedir(), ".agents", "skills"));
    dirs.push(path.join(state, "skills"));
    return [...new Set(dirs)];
}
/**
 * `agents.defaults.workspace` from openclaw.json, or null.
 *
 * Best effort by design: a missing or unreadable config is not this tool's
 * problem, and the search continues with the conventional locations.
 */
function configuredWorkspace(stateDir) {
    try {
        const document = JSON.parse(readFileSync(path.join(stateDir, "openclaw.json"), "utf8"));
        const workspace = document.agents?.defaults?.workspace;
        return typeof workspace === "string" && workspace.trim() !== "" ? workspace : null;
    }
    catch {
        return null;
    }
}
/**
 * Find an installed skill by slug.
 *
 * @param slug The directory name the skill is installed under.
 * @param env Process environment, for the override and the state directory.
 * @param overrideVar The environment variable that names a directory outright.
 * @returns Where it is, or null when no candidate holds a SKILL.md.
 */
export function findSkill(slug, env, overrideVar) {
    const override = env[overrideVar];
    if (override !== undefined && override.trim() !== "") {
        const skillFile = path.join(override, "SKILL.md");
        // An override that is wrong is reported as not found rather than silently
        // falling back to a different copy: somebody who set it wants that copy.
        if (!existsSync(skillFile))
            return null;
        return { slug, dir: override, source: `${overrideVar}`, version: readSkillVersion(skillFile) };
    }
    for (const dir of skillSearchDirs(env)) {
        const candidate = path.join(dir, slug);
        const skillFile = path.join(candidate, "SKILL.md");
        if (existsSync(skillFile)) {
            return { slug, dir: candidate, source: dir, version: readSkillVersion(skillFile) };
        }
    }
    return null;
}
/** How much of a delegate's output is kept. Beyond this it is truncated. */
export const MAX_OUTPUT_BYTES = 4_194_304;
/**
 * Run a program and collect its output.
 *
 * @param file The executable. Never a shell.
 * @param argv Its arguments, already separated.
 * @returns The exit code and captured output. A failure to spawn is reported in
 *   the result rather than thrown, because "the interpreter is missing" is a
 *   diagnosis to print, not an exception to propagate.
 */
export async function run(file, argv, options = {}) {
    return await new Promise((resolve) => {
        const child = spawn(file, [...argv], {
            cwd: options.cwd,
            env: options.env,
            stdio: ["pipe", "pipe", "pipe"],
            // No shell, ever. Every argument reaches the program as written.
            shell: false,
        });
        const out = [];
        const err = [];
        let outBytes = 0;
        let errBytes = 0;
        let timedOut = false;
        let settled = false;
        const timer = options.timeoutMs === undefined
            ? null
            : setTimeout(() => {
                timedOut = true;
                child.kill("SIGKILL");
            }, options.timeoutMs);
        const finish = (result) => {
            if (settled)
                return;
            settled = true;
            if (timer)
                clearTimeout(timer);
            resolve(result);
        };
        child.stdout.on("data", (chunk) => {
            if (outBytes < MAX_OUTPUT_BYTES) {
                out.push(chunk);
                outBytes += chunk.byteLength;
            }
        });
        child.stderr.on("data", (chunk) => {
            if (errBytes < MAX_OUTPUT_BYTES) {
                err.push(chunk);
                errBytes += chunk.byteLength;
            }
        });
        child.on("error", (error) => {
            finish({
                code: 127,
                stdout: "",
                stderr: error instanceof Error ? error.message : String(error),
                timedOut: false,
                spawnFailed: true,
            });
        });
        child.on("close", (code) => {
            finish({
                code: code ?? 1,
                stdout: Buffer.concat(out).toString("utf8"),
                stderr: Buffer.concat(err).toString("utf8"),
                timedOut,
                spawnFailed: false,
            });
        });
        if (options.input !== undefined)
            child.stdin.write(options.input);
        child.stdin.end();
    });
}
/** Whether a path exists, exposed so the bridges can test for a feature file. */
export function fileExists(candidate) {
    return existsSync(candidate);
}
