/**
 * The run log: where a scheduled run's diagnostics go when the run succeeded.
 *
 * OpenClaw stays silent for a cron command only when its output is exactly
 * NO_REPLY. If anything was written to stderr as well, it delivers both, headed
 * "stdout:" and "stderr:", so a routine note becomes a chat message. Measured on
 * OpenClaw 2026.7.1-2: eleven such messages in two days from notes alone.
 *
 * So a successful scheduled run writes nothing to stderr. Its notes are
 * appended here instead, next to the state file, where they can still be read.
 * A failed run keeps them on stderr, because then they are the explanation.
 */
import type { Streams } from "./render.js";
/** Rotate the log past this size, keeping one previous file. */
export declare const RUN_LOG_LIMIT = 1000000;
/** The run log's location: beside the state file. */
export declare function runLogPath(stateFile: string): string;
/** Streams whose stderr is held back until the outcome is known. */
export declare function deferErr(streams: Streams): Streams & {
    held: () => string;
};
/**
 * Send held diagnostics where they belong for this outcome.
 *
 * @param code The run's exit code. Zero sends them to the run log, anything
 *   else to stderr.
 */
export declare function releaseErr(streams: Streams, held: string, code: number, logFile: string, label: string, atMs: number): void;
