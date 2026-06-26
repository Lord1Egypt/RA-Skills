"use strict";
/**
 * Interceptor — the main hook that fires on every intent.
 *
 * Flow:
 * 1. User issues an intent (e.g., "login to GitHub")
 * 2. Interceptor queries ClawMind Cloud for a matching Lobster macro
 * 3. If hit → execute the Lobster workflow directly (skip LLM exploration)
 * 4. If miss → passthrough to normal OpenClaw flow
 * 5. On success → contribute the trace back to the cloud
 * 6. On failure → report failure for circuit breaker tracking
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.interceptIntent = interceptIntent;
exports.onSessionComplete = onSessionComplete;
const cloud_client_js_1 = require("./cloud-client.js");
const intent_parser_js_1 = require("./intent-parser.js");
const trace_compiler_js_1 = require("./trace-compiler.js");
async function interceptIntent(ctx) {
    const { browser, lobster, sessions, gateway, workspace, config, logger } = ctx;
    // Check if skill is enabled
    if (!config.get("enabled")) {
        gateway.passthrough();
        return;
    }
    const cloudEndpoint = config.get("cloud_endpoint");
    const timeoutMs = config.get("timeout_ms");
    const client = new cloud_client_js_1.CloudClient(cloudEndpoint, timeoutMs, logger);
    const sessionId = sessions.getCurrentSessionId();
    const history = await sessions.getHistory(sessionId);
    const intent = history.intent;
    if (!intent) {
        gateway.passthrough();
        return;
    }
    const url = await browser.getCurrentUrl();
    const domHash = await browser.getDomSkeletonHash();
    const nodeId = workspace.getNodeId();
    const parsed = (0, intent_parser_js_1.parseIntent)(intent, url);
    logger.info(`[ClawMind] Intercepting intent: "${parsed.normalized}" on ${parsed.domain}`);
    // Query cloud for a matching macro
    let matchResult = null;
    try {
        matchResult = await client.match({
            intent: parsed.normalized,
            url,
            dom_skeleton_hash: domHash,
            node_id: nodeId,
        });
    }
    catch {
        // Cloud unavailable — graceful degradation, just passthrough
        logger.debug("[ClawMind] Cloud unreachable, passing through");
        gateway.passthrough();
        return;
    }
    // No match — let OpenClaw handle it normally
    if (!matchResult || !matchResult.hit || !matchResult.macro) {
        logger.info("[ClawMind] No macro match, passing through to OpenClaw");
        gateway.passthrough();
        return;
    }
    const macro = matchResult.macro;
    logger.info(`[ClawMind] Match found: ${macro.macro_id} (score: ${matchResult.match_score}, method: ${matchResult.match_method})`);
    // Validate the workflow before execution
    if (!lobster.validate(macro.lobster_workflow)) {
        logger.warn(`[ClawMind] Workflow validation failed for ${macro.macro_id}`);
        gateway.passthrough();
        return;
    }
    // Execute the Lobster workflow
    let execResult;
    try {
        execResult = await lobster.execute(macro.lobster_workflow);
    }
    catch (err) {
        logger.error(`[ClawMind] Lobster execution threw: ${err}`);
        // Report failure to cloud (fire-and-forget)
        client.reportFailure({
            macro_id: macro.macro_id,
            node_id: nodeId,
            error_type: "other",
            error_detail: String(err),
        }).catch(() => { });
        // Fall back to normal OpenClaw flow
        gateway.passthrough();
        return;
    }
    if (execResult.success) {
        logger.info(`[ClawMind] Macro ${macro.macro_id} executed successfully (${execResult.steps_completed}/${execResult.total_steps} steps)`);
        gateway.respond(`✅ Done via ClawMind cached workflow (${macro.macro_id}). ` +
            `${execResult.steps_completed} steps replayed.`);
    }
    else {
        logger.warn(`[ClawMind] Macro ${macro.macro_id} failed at step ${execResult.failed_step_id}: ${execResult.error}`);
        // Map error to error_type
        const errorType = mapErrorType(execResult.error || "");
        client.reportFailure({
            macro_id: macro.macro_id,
            node_id: nodeId,
            error_type: errorType,
            error_detail: execResult.error,
        }).catch(() => { });
        // Fall back to normal OpenClaw flow
        gateway.passthrough();
    }
}
/**
 * Hook: called when a session completes successfully.
 * Compiles the session trace into a Lobster workflow and contributes it.
 */
async function onSessionComplete(ctx) {
    const { browser, sessions, workspace, config, logger } = ctx;
    if (!config.get("enabled") || !config.get("auto_contribute")) {
        return;
    }
    const sessionId = sessions.getCurrentSessionId();
    const history = await sessions.getHistory(sessionId);
    // Only contribute successful sessions with meaningful actions
    if (history.status !== "success")
        return;
    if (history.actions.length < 2)
        return;
    const intent = history.intent;
    if (!intent)
        return;
    const url = await browser.getCurrentUrl();
    const domHash = await browser.getDomSkeletonHash();
    const nodeId = workspace.getNodeId();
    // Compile the trace into a Lobster workflow
    const { workflow, argCount } = (0, trace_compiler_js_1.compileTrace)(intent, history.actions);
    // Skip trivial workflows (single step, no real logic)
    if (workflow.steps.length < 2) {
        logger.debug("[ClawMind] Workflow too trivial to contribute, skipping");
        return;
    }
    logger.info(`[ClawMind] Contributing workflow "${workflow.name}" (${workflow.steps.length} steps, ${argCount} args)`);
    const cloudEndpoint = config.get("cloud_endpoint");
    const client = new cloud_client_js_1.CloudClient(cloudEndpoint, 5000, logger);
    try {
        const result = await client.contribute({
            node_id: nodeId,
            intent,
            url,
            dom_skeleton_hash: domHash,
            lobster_workflow: workflow,
            session_id: sessionId,
        });
        if (result?.accepted) {
            logger.info(`[ClawMind] Contribution accepted: ${result.macro_id}`);
        }
        else {
            logger.debug(`[ClawMind] Contribution not accepted: ${result?.reason}`);
        }
    }
    catch (err) {
        logger.debug(`[ClawMind] Contribution failed: ${err}`);
    }
}
function mapErrorType(error) {
    const lower = error.toLowerCase();
    if (lower.includes("selector") || lower.includes("not found") || lower.includes("no element")) {
        return "selector_not_found";
    }
    if (lower.includes("timeout") || lower.includes("timed out")) {
        return "timeout";
    }
    if (lower.includes("unexpected") || lower.includes("state")) {
        return "unexpected_state";
    }
    return "other";
}
