/**
 * pair-pending-injection — `before_agent_start` hook that surfaces the
 * pending pair URL + PIN to the chat agent verbatim, so the agent can NOT
 * hallucinate either value.
 *
 * Background
 * ----------
 * Companion to `auto-pair-on-load.ts`. When the plugin loads without
 * credentials, the auto-pair flow writes `~/.totalreclaw/.pair-pending.json`
 * with the exact URL + PIN the user must use. This hook reads that file on
 * every agent start and, when present, prepends a context block that tells
 * the agent EXACTLY what to say.
 *
 * No agent-generated string ever appears in the URL or PIN that reaches
 * the user.
 *
 * Phrase safety
 * -------------
 * The sentinel does NOT contain the recovery phrase. The injected context
 * deliberately warns the agent NOT to attempt to display, generate, or
 * relay any phrase. That instruction is reinforced via the staging-banner
 * hook + the SKILL.md phrase-safety section.
 *
 * Scanner scope
 * -------------
 * Pure-logic file — no `node:fs` imports, no `process.env` reads, no
 * subprocess module usage. Disk I/O is delegated to `fs-helpers.ts`.
 */
import { defaultPairPendingPath, deletePairPendingFile, loadPairPendingFile, } from './fs-helpers.js';
import { maybeStartAutoPair } from './auto-pair-on-load.js';
// ---------------------------------------------------------------------------
// Hook body (exposed for unit tests)
// ---------------------------------------------------------------------------
/**
 * Pure-async body of the hook. Test-callable.
 *
 * - sentinel missing -> no-op (return `undefined`)
 * - sentinel valid + non-expired -> return `{ prependContext: <block> }`
 * - sentinel expired -> delete + try re-create via maybeStartAutoPair; if
 *   re-create returns a fresh `pending`, inject context for the NEW URL/PIN;
 *   else return `undefined`
 */
export async function runPairPendingInjection(deps, logger) {
    const now = deps.now ?? Date.now;
    const pendingPath = deps.pendingPath ?? defaultPairPendingPath(deps.credentialsPath);
    const existing = loadPairPendingFile(pendingPath);
    // No sentinel — nothing to inject.
    if (!existing)
        return undefined;
    // Valid + non-expired sentinel — inject context with verbatim values.
    if (existing.expires_at_ms > now()) {
        return { prependContext: buildPrependContext(existing) };
    }
    // Expired sentinel. Clean it up and optionally re-create.
    logger.info('pair-pending-injection: sentinel expired, cleaning up');
    deletePairPendingFile(pendingPath);
    const apFactory = deps.autoPairDepsFactory;
    if (!apFactory)
        return undefined;
    const apDeps = apFactory();
    if (!apDeps)
        return undefined;
    try {
        const runner = deps.startAutoPair ?? maybeStartAutoPair;
        const result = (await runner(apDeps));
        if (result
            && typeof result === 'object'
            && (result.status === 'started' || result.status === 'pending_reused')) {
            return { prependContext: buildPrependContext(result.pending) };
        }
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        logger.warn(`pair-pending-injection: re-create failed: ${msg}`);
    }
    return undefined;
}
// ---------------------------------------------------------------------------
// Wire-up
// ---------------------------------------------------------------------------
/**
 * Register the before_agent_start hook on the OpenClaw plugin API. Wraps
 * the hook body in try/catch so any error path returns `undefined` (i.e.
 * silently skip the injection — never block session start).
 */
export function installBeforeAgentStartHook(api, deps) {
    api.on('before_agent_start', async (_event) => {
        try {
            return await runPairPendingInjection(deps, api.logger);
        }
        catch (err) {
            const msg = err instanceof Error ? err.message : String(err);
            api.logger.warn(`pair-pending-injection: hook failed: ${msg}`);
            return undefined;
        }
    }, 
    // Priority chosen lower than the staging-banner / memory-recall hook
    // (which uses default priority) so the pair-pending block lands BEFORE
    // those — the URL + PIN is the highest-priority action for a fresh user.
    { priority: 100 });
}
// ---------------------------------------------------------------------------
// Context-block builder (exported for tests)
// ---------------------------------------------------------------------------
/**
 * Build the prepend block. URL + PIN are inlined VERBATIM from the
 * sentinel — there is no template substitution or string manipulation on
 * either value. The agent is told explicitly to read the file as the
 * source of truth.
 */
export function buildPrependContext(pending) {
    return ('[TotalReclaw setup pending — read this carefully]\n\n'
        + 'The user has TotalReclaw installed but no recovery phrase yet. To complete setup, '
        + 'tell the user EXACTLY these two values (do NOT invent or modify them — read directly '
        + 'from ~/.totalreclaw/.pair-pending.json):\n\n'
        + `Open this URL in your browser: ${pending.url}\n`
        + `Enter this 6-digit PIN: ${pending.pin}\n\n`
        + 'The browser page lets the user either generate a fresh 12-word recovery phrase or '
        + 'import an existing one. The phrase is delivered to the gateway end-to-end encrypted; '
        + 'it never touches you (the agent) or any server in plaintext.\n\n'
        + 'After the user confirms "done", check ~/.totalreclaw/credentials.json — if present, '
        + 'setup is complete.\n\n'
        + 'CRITICAL: do NOT make up these values. The file ~/.totalreclaw/.pair-pending.json IS '
        + 'the source of truth. If the file is missing, run `tr pair --json` instead.\n\n');
}
