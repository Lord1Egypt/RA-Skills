/**
 * Dispatch: parse a command line, load what the command needs, run it.
 *
 * `main` returns an exit code instead of calling `process.exit`, and the built
 * shim sets `process.exitCode` from it. That is not a style preference:
 * `process.exit` truncates asynchronous writes to a pipe, and a cron job capturing
 * stdout is exactly a pipe. A truncated alert delivered with exit code 0 would be
 * the worst failure this tool could have, because it would look like it worked.
 */
import { type Env } from "../paths.js";
import { type Streams } from "./render.js";
/**
 * Run one command.
 *
 * @param argv Arguments after the program name.
 * @param env The process environment.
 * @param streams Where output goes.
 * @returns The exit code. Never throws for an expected failure.
 */
export declare function main(argv: readonly string[], env: Env, streams: Streams): Promise<number>;
