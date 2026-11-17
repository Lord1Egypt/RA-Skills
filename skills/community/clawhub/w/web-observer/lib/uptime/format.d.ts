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
import { type UptimeEvent } from "./decide.js";
/**
 * The exact token OpenClaw treats as "deliver nothing".
 *
 * Verified against OpenClaw 2026.7.1-2: matched case-insensitively, it
 * suppresses both the direct outbound delivery and the fallback queued summary.
 * It must be the whole of stdout, so nothing may be printed alongside it.
 */
export declare const SILENT_TOKEN = "NO_REPLY";
/**
 * Whether a duration is precise enough to need no hedge in front of it.
 *
 * "Down for about under a second" is what happens without this: the sub-second
 * case already hedges, so a second "about" reads as a mistake. Everything longer
 * does want the hedge, because an outage is only ever known to within one check
 * interval.
 */
export declare function durationIsHedged(ms: number): boolean;
/** How long an outage lasted, in the units a person would use. */
export declare function humanDuration(ms: number): string;
/** A timestamp as local wall-clock time with its offset, for an alert line. */
export declare function stamp(atMs: number): string;
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
export declare function formatEvents(events: readonly UptimeEvent[]): string;
