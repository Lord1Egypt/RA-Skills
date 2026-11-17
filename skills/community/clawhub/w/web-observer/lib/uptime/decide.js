/**
 * When a human gets woken up, and when they do not.
 *
 * Every function here is pure: state and a check result go in, new state and at
 * most one event come out. Nothing here performs I/O, reads a clock or formats
 * a message, which is what makes the alerting rules testable without a network
 * or a filesystem, and is why this file rather than the network code carries the
 * tests that matter most.
 *
 * The rules, in the order they bite:
 *
 * 1. A watch is checked only when it is due, so per-URL intervals work from a
 *    single scheduled job. Due times are served by the nearest round rather than
 *    the next one after them, or an interval equal to the tick would slip a
 *    whole tick every time.
 * 2. A watch alerts once it has failed `failureThreshold` consecutive checks,
 *    and not before, so one dropped connection is not an alert.
 * 3. It then stays silent for as long as it remains down. An alert repeated
 *    every interval is what teaches people to mute the monitor that was right.
 * 4. It sends exactly one recovery message when it passes again.
 */
/** Every reason, for documentation tests and for rendering a legend. */
export const FAILURE_REASONS = [
    "timeout",
    "dns",
    "connection-refused",
    "tls",
    "status-mismatch",
    "body-mismatch",
    "redirect-off-allowlist",
    "network",
];
/** How each reason reads in an alert. */
export const REASON_TEXT = {
    timeout: "timed out",
    dns: "DNS lookup failed",
    "connection-refused": "connection refused",
    tls: "TLS error",
    "status-mismatch": "unexpected status",
    "body-mismatch": "body did not match",
    "redirect-off-allowlist": "redirected off the allowlist",
    network: "network error",
};
/**
 * How early a round may take a watch that is not quite due, in milliseconds.
 *
 * Checks happen only when the scheduled job fires, so a watch that comes due
 * between two rounds is either taken by one of them or waits a whole tick. Half
 * a tick puts each due time with the nearer round.
 *
 * Without this, a watch whose interval equals the tick runs at half its
 * configured rate, permanently. The next due time is stamped when a check
 * finishes, so it lands a fraction of a second after the following round
 * arrives; that round finds it not due, and the check falls to the round after.
 * Measured on a live install: a five-minute watch on a five-minute tick was
 * checked every ten minutes, which doubled how long an outage took to report.
 *
 * @param tickMinutes How often the scheduled job runs.
 */
export function dueToleranceMs(tickMinutes) {
    return (tickMinutes * 60_000) / 2;
}
/**
 * Whether a watch should be checked now.
 *
 * A watch never checked before is due immediately, which is what makes a first
 * run report on everything rather than waiting an interval to say anything.
 *
 * @param state That watch's saved state.
 * @param nowMs The current time.
 * @param toleranceMs How early this round may take it. See
 *   {@link dueToleranceMs}: zero means "not before the due time, ever".
 */
export function isDue(state, nowMs, toleranceMs) {
    return state.nextDueAtMs === null || nowMs + toleranceMs >= state.nextDueAtMs;
}
/**
 * Which of a set of watches a tick should check.
 *
 * Disabled watches are skipped here rather than filtered by the caller, so
 * there is one place that decides what a tick does.
 */
export function dueWatches(watches, states, nowMs, toleranceMs) {
    return watches.filter((watch) => watch.enabled && isDue(states(watch), nowMs, toleranceMs));
}
/**
 * Fold one check result into a watch's state.
 *
 * @param watch The watch that was checked, for its thresholds and interval.
 * @param previous Its state before this check.
 * @param result What the check found.
 * @param nowMs The time the check completed.
 * @returns The new state, and the event this check caused, if any. At most one
 *   event: a single check cannot both break and fix a site.
 */
export function applyResult(watch, previous, result, nowMs) {
    const next = {
        ...previous,
        lastCheckAtMs: nowMs,
        nextDueAtMs: nowMs + watch.intervalMinutes * 60_000,
    };
    if (result.ok) {
        next.consecutiveSuccesses = previous.consecutiveSuccesses + 1;
        next.consecutiveFailures = 0;
        next.lastReason = null;
        // The run of failures is over, so the time it began is no longer wanted,
        // but it is needed for this very message, so it is read before clearing.
        const downSinceMs = previous.firstFailureAtMs;
        next.firstFailureAtMs = null;
        if (previous.down && next.consecutiveSuccesses >= watch.recoveryThreshold) {
            next.down = false;
            return { state: next, event: { kind: "recovered", watch, result, atMs: nowMs, downSinceMs } };
        }
        return { state: next, event: null };
    }
    next.consecutiveFailures = previous.consecutiveFailures + 1;
    next.consecutiveSuccesses = 0;
    next.lastReason = result.reason;
    // Stamped when the run of failures starts, not when it crosses the
    // threshold, so a recovery message reports the outage the user experienced
    // rather than the part of it this tool was already certain about.
    next.firstFailureAtMs = previous.firstFailureAtMs ?? nowMs;
    if (!previous.down && next.consecutiveFailures >= watch.failureThreshold) {
        next.down = true;
        return { state: next, event: { kind: "down", watch, result, atMs: nowMs } };
    }
    return { state: next, event: null };
}
