/**
 * Turning events into the text a person reads on their phone.
 *
 * The single most important thing here is {@link SILENT_TOKEN}. A cron job with
 * `--announce` delivers this tool's stdout to the chat channel, and OpenClaw
 * suppresses that delivery when the output is exactly the silent token. So
 * "print an alert" and "say nothing" are the same mechanism, and no code in this
 * project opens a connection to a chat provider.
 *
 * The consequence to keep in mind while editing: **anything printed to stdout on
 * a scheduled run is sent to the user.** A stray progress line turns a quiet
 * monitor into a source of noise every five minutes.
 */
import { REASON_TEXT } from "./decide.js";
/**
 * The exact token OpenClaw treats as "deliver nothing".
 *
 * Verified against OpenClaw 2026.7.1-2: matched case-insensitively, it
 * suppresses both the direct outbound delivery and the fallback queued summary.
 * It must be the whole of stdout, so nothing may be printed alongside it.
 */
export const SILENT_TOKEN = "NO_REPLY";
/**
 * Whether a duration is precise enough to need no hedge in front of it.
 *
 * "Down for about under a second" is what happens without this: the sub-second
 * case already hedges, so a second "about" reads as a mistake. Everything longer
 * does want the hedge, because an outage is only ever known to within one check
 * interval.
 */
export function durationIsHedged(ms) {
    return ms < 1_000;
}
/** How long an outage lasted, in the units a person would use. */
export function humanDuration(ms) {
    if (ms < 1_000)
        return "under a second";
    const seconds = Math.round(ms / 1_000);
    if (seconds < 60)
        return `${seconds} second${seconds === 1 ? "" : "s"}`;
    const minutes = Math.round(seconds / 60);
    if (minutes < 60)
        return `${minutes} minute${minutes === 1 ? "" : "s"}`;
    const hours = ms / 3_600_000;
    if (hours < 48) {
        const rounded = Math.round(hours * 10) / 10;
        return `${rounded} hour${rounded === 1 ? "" : "s"}`;
    }
    const days = Math.round(hours / 24);
    return `${days} day${days === 1 ? "" : "s"}`;
}
/** A timestamp as local wall-clock time with its offset, for an alert line. */
export function stamp(atMs) {
    const date = new Date(atMs);
    const offsetMinutes = -date.getTimezoneOffset();
    const sign = offsetMinutes < 0 ? "-" : "+";
    const absolute = Math.abs(offsetMinutes);
    const offset = `${sign}${String(Math.floor(absolute / 60)).padStart(2, "0")}:${String(absolute % 60).padStart(2, "0")}`;
    const pad = (value) => String(value).padStart(2, "0");
    return (`${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ` +
        `${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())} ${offset}`);
}
/** One event as the lines it contributes to a message. */
function eventLines(event) {
    if (event.kind === "down") {
        const { watch, result } = event;
        const lines = [`🔴 ${watch.id} is DOWN: ${watch.url}`];
        lines.push(`- Reason: ${REASON_TEXT[result.reason]} (${result.detail})`);
        lines.push(`- Confirmed over ${watch.failureThreshold} consecutive check${watch.failureThreshold === 1 ? "" : "s"}, ${result.attemptsUsed} request${result.attemptsUsed === 1 ? "" : "s"} on the last one`);
        lines.push(`- At: ${stamp(event.atMs)}`);
        return lines;
    }
    const { watch, result } = event;
    const lines = [`🟢 ${watch.id} is back up: ${watch.url}`];
    if (event.downSinceMs !== null) {
        const outage = event.atMs - event.downSinceMs;
        const hedge = durationIsHedged(outage) ? "" : "about ";
        lines.push(`- Down for ${hedge}${humanDuration(outage)}, since ${stamp(event.downSinceMs)}`);
    }
    lines.push(`- Now returning ${result.status} in ${result.durationMs} ms`);
    lines.push(`- At: ${stamp(event.atMs)}`);
    return lines;
}
/**
 * The message for a scheduled run, or the silent token.
 *
 * Several events become one message rather than several, because a cron run
 * produces exactly one delivery: printing two alerts would still be one chat
 * message, and formatting them as though they were separate reads as a mistake.
 *
 * @param events Every event this run produced, in the order the watches ran.
 * @returns Text to print. Exactly {@link SILENT_TOKEN} when there is nothing to
 *   say, which is what suppresses delivery.
 */
export function formatEvents(events) {
    if (events.length === 0)
        return SILENT_TOKEN;
    const down = events.filter((event) => event.kind === "down");
    const recovered = events.filter((event) => event.kind === "recovered");
    const blocks = events.map((event) => eventLines(event).join("\n"));
    if (events.length === 1)
        return blocks[0];
    // A heading only when there is more than one event, so the common case of a
    // single site failing is not padded with a summary of itself.
    const summary = [
        down.length > 0 ? `${down.length} down` : null,
        recovered.length > 0 ? `${recovered.length} recovered` : null,
    ]
        .filter((part) => part !== null)
        .join(", ");
    // Blocks are separated by a blank line. Joined by a single newline, two
    // stacked alerts run together into one wall of text, which is how it reads on
    // a phone: the second site's name lands directly under the first one's
    // timestamp and neither is easy to pick out.
    return `Web Observer: ${summary}\n\n${blocks.join("\n\n")}`;
}
