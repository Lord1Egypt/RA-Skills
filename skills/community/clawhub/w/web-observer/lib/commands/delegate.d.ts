/**
 * The commands that hand a question to another skill.
 *
 * `vercel` and `ga4` are for questions asked in conversation. `digest` is the
 * scheduled GA4 summary. All three exist so that Web Observer is one surface for
 * "how is my site doing", rather than three skills a person has to remember the
 * names of.
 *
 * Output is relayed rather than reformatted. Both delegated skills already lay
 * their answers out for a person to read, and re-typesetting a table is how a
 * number comes to differ between two tools that queried the same thing once.
 */
import { type Streams } from "../cli/render.js";
import type { Config } from "../config.js";
import type { Env } from "../paths.js";
import { type CredentialResult } from "../bridge/credentials.js";
import type { RunResult } from "../bridge/delegate.js";
import { type Ga4Status } from "../bridge/ga4.js";
/** The variables open-ga4 reads, forwarded when configured. Canonical list in env.ts. */
export declare const GA4_CREDENTIAL_SPEC: {
    readonly slug: "open-ga4";
    readonly primaryEnv: "GA4_CREDENTIALS";
    readonly optional: ("GA4_CREDENTIALS" | "GA4_PROPERTY_ID" | "GOOGLE_APPLICATION_CREDENTIALS")[];
};
export type DelegateContext = {
    config: Config;
    streams: Streams;
    env: Env;
};
/** `web-observer vercel <preset> ...` */
export declare function runVercelCommand(context: DelegateContext, passthrough: readonly string[]): Promise<number>;
/** `web-observer ga4 <preset> ...` */
export declare function runGa4Command(context: DelegateContext, passthrough: readonly string[]): Promise<number>;
export type DigestDeps = {
    status: Ga4Status;
    credentials: CredentialResult;
    invoke: (argv: readonly string[]) => Promise<RunResult>;
};
/**
 * `digest`: the scheduled traffic summary.
 *
 * Unlike the ad hoc commands, this one runs unattended and its stdout is
 * delivered to a chat, so a failure must not become a message: printing the
 * silent token and exiting non-zero puts the problem in the run log and lets
 * cron's own failure notification handle it, instead of sending somebody a
 * stack trace at nine in the morning every Monday.
 */
export declare function runDigestCommand(context: DelegateContext & {
    configFile: string;
}, deps: DigestDeps, options: {
    dryRun: boolean;
}): Promise<number>;
