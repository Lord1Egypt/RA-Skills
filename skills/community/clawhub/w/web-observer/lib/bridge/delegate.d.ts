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
import { type Env } from "../paths.js";
/** Where a skill was found, so `doctor` can say which copy it is using. */
export type SkillLocation = {
    slug: string;
    dir: string;
    /** How it was found: an override, or the directory it was discovered in. */
    source: string;
    /** `version:` from its SKILL.md frontmatter, when it has one. */
    version: string | null;
};
/** Read `version:` out of a SKILL.md without a YAML parser. */
export declare function readSkillVersion(skillFile: string): string | null;
/**
 * The directories a skill can be installed in, most specific first.
 *
 * Mirrors OpenClaw's own precedence: the agent workspace, then the
 * per-workspace agent directory, then the shared agent profile, then the shared
 * state directory. The workspace is read from `openclaw.json` when it is
 * configured there, because it need not be `<state>/workspace`.
 */
export declare function skillSearchDirs(env: Env): string[];
/**
 * Find an installed skill by slug.
 *
 * @param slug The directory name the skill is installed under.
 * @param env Process environment, for the override and the state directory.
 * @param overrideVar The environment variable that names a directory outright.
 * @returns Where it is, or null when no candidate holds a SKILL.md.
 */
export declare function findSkill(slug: string, env: Env, overrideVar: string): SkillLocation | null;
export type RunResult = {
    code: number;
    stdout: string;
    stderr: string;
    /** True when the process was killed for exceeding its time budget. */
    timedOut: boolean;
    /** True when the executable could not be started at all. */
    spawnFailed: boolean;
};
/** How much of a delegate's output is kept. Beyond this it is truncated. */
export declare const MAX_OUTPUT_BYTES = 4194304;
export type SpawnOptions = {
    cwd?: string;
    env?: Record<string, string | undefined>;
    timeoutMs?: number;
    input?: string;
};
/**
 * Run a program and collect its output.
 *
 * @param file The executable. Never a shell.
 * @param argv Its arguments, already separated.
 * @returns The exit code and captured output. A failure to spawn is reported in
 *   the result rather than thrown, because "the interpreter is missing" is a
 *   diagnosis to print, not an exception to propagate.
 */
export declare function run(file: string, argv: readonly string[], options?: SpawnOptions): Promise<RunResult>;
/** Whether a path exists, exposed so the bridges can test for a feature file. */
export declare function fileExists(candidate: string): boolean;
