/**
 * Exit codes, and what each one should make an agent say.
 *
 * The distinction that earns its keep is between 1 and 3. A monitor that cannot
 * reach an API and a monitor reporting that a site is down are different events:
 * the first needs the monitor looked at, the second needs the site looked at.
 * Collapsing them would make an outage indistinguishable from a broken token.
 *
 * The subtler rule is that a scheduled run alerting about a real outage exits
 * **0**. An alert is this tool working, not failing. Exiting non-zero would make
 * OpenClaw's own cron failure notification fire alongside the alert already
 * delivered, so a single outage would be reported twice by two mechanisms, and
 * repeated failures would additionally back the job off.
 */
export declare const EXIT_OK = 0;
/** A check or a delegated call failed for a network or API reason. */
export declare const EXIT_FAILURE = 1;
/** Configuration or usage error. Nothing was attempted. */
export declare const EXIT_CONFIG = 2;
/** It worked, and the answer is bad news. Only from `check --strict`. */
export declare const EXIT_BAD_NEWS = 3;
export declare const EXIT_INTERRUPTED = 130;
export declare const EXIT_CODES: readonly [0, 1, 2, 3, 130];
/** One line per code, for the documentation test to compare against SKILL.md. */
export declare const EXIT_MEANINGS: Record<number, string>;
