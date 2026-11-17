/**
 * Performing one uptime check.
 *
 * This is the only module in Web Observer that makes an outbound request of its
 * own, and every request it makes is checked against the allowlist first, on the
 * initial URL and again on every redirect hop. The allowlist is derived from the
 * user's configured watch URLs and nothing else, so a redirect cannot take a
 * request, or a configured header, to a host the user never named.
 *
 * Nothing a server sends is copied into a failure detail. A body is measured,
 * never quoted, and a header is never echoed: a check runs against a site that
 * may be compromised or simply misconfigured, its output is delivered straight
 * into a chat, and a detail line has no business carrying whatever a stranger
 * put in a response.
 */
import { type Watch } from "../config.js";
import type { CheckResult, FailureReason } from "./decide.js";
/** The subset of `fetch` this module uses, injected so tests need no network. */
export type Fetcher = (url: string, init: RequestInit) => Promise<Response>;
export type CheckDeps = {
    fetch: Fetcher;
    /** Milliseconds since the epoch. Injected to keep durations deterministic. */
    now: () => number;
    sleep: (ms: number) => Promise<void>;
};
/**
 * How much of a body is read when a body expectation exists.
 *
 * A health endpoint's answer is small; a home page is not, and an unbounded read
 * of a page being served by a broken origin is a way to run out of memory. A
 * match beyond this point is reported as a mismatch, and the detail says the
 * body was truncated so the number is never mistaken for a verdict on the whole
 * document.
 */
export declare const MAX_BODY_BYTES = 1048576;
/**
 * Turn a thrown request error into one of the fixed reasons.
 *
 * Node's fetch wraps the real cause, so the chain is walked rather than the
 * outer message read: the outer message is the useless `fetch failed`.
 *
 * @returns The reason, and one line naming what happened. The line is built from
 *   the error's own code and message, both of which describe the transport, not
 *   the response body.
 */
export declare function classifyError(error: unknown): {
    reason: FailureReason;
    detail: string;
};
/**
 * Check one watch, retrying within the check as configured.
 *
 * A check succeeds as soon as any attempt succeeds, so `attempts` is the guard
 * against a single dropped packet. The reason reported on failure is the last
 * attempt's: an intermittent failure that changes character between attempts is
 * best described by the most recent one, and the count of attempts spent is
 * reported alongside so a reader knows it was not a one-off.
 *
 * @param watch The watch to check, with defaults already applied.
 * @param allowlist From `allowlistOf`, enforced on every request.
 * @param deps Injected clock, sleep and fetch.
 */
export declare function performCheck(watch: Watch, allowlist: ReadonlySet<string>, deps: CheckDeps): Promise<CheckResult>;
/** The real dependencies, used by the CLI. */
export declare const liveDeps: CheckDeps;
