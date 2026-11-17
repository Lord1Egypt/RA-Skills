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
import { appendFileSync, mkdirSync, renameSync, statSync } from "node:fs";
import path from "node:path";
/** Rotate the log past this size, keeping one previous file. */
export const RUN_LOG_LIMIT = 1_000_000;
/** The run log's location: beside the state file. */
export function runLogPath(stateFile) {
    return path.join(path.dirname(stateFile), "web-observer.log");
}
/** Streams whose stderr is held back until the outcome is known. */
export function deferErr(streams) {
    const held = [];
    return { out: streams.out, err: (text) => held.push(text), held: () => held.join("") };
}
/**
 * Send held diagnostics where they belong for this outcome.
 *
 * @param code The run's exit code. Zero sends them to the run log, anything
 *   else to stderr.
 */
export function releaseErr(streams, held, code, logFile, label, atMs) {
    if (held === "")
        return;
    if (code !== 0) {
        streams.err(held);
        return;
    }
    try {
        mkdirSync(path.dirname(logFile), { recursive: true });
        try {
            if (statSync(logFile).size > RUN_LOG_LIMIT)
                renameSync(logFile, `${logFile}.1`);
        }
        catch {
            // Absent is the usual case on a first run.
        }
        const stamp = new Date(atMs).toISOString();
        const body = held
            .trimEnd()
            .split("\n")
            .map((line) => `${stamp} ${label} ${line}`)
            .join("\n");
        appendFileSync(logFile, `${body}\n`, { mode: 0o600 });
    }
    catch {
        // Losing a note is better than turning a quiet run into a chat message.
    }
}
