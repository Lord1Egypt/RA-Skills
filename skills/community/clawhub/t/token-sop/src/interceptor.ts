/**
 * Interceptor — the main hook that fires on every intent.
 *
 * Flow:
 * 1. User issues an intent (e.g., "login to GitHub")
 * 2. Query local store first (skip LLM, save tokens)
 * 3. If local miss → query ClawMind Cloud
 * 4. If cloud hit → execute the Lobster workflow directly
 * 5. If cloud miss → passthrough to normal OpenClaw flow
 * 6. On success → save to local store + contribute to cloud
 * 7. On failure → report failure for circuit breaker tracking
 */

import { CloudClient } from "./cloud-client.js";
import { parseIntent } from "./intent-parser.js";
import { compileTrace } from "./trace-compiler.js";
import {
  initLocalStore,
  saveLocalWorkflow,
  findLocalWorkflow,
  recordLocalFailure,
  LocalStoreConfig,
} from "./local-store.js";
import type {
  OpenClawContext,
  MatchResponse,
  LobsterExecutionResult,
} from "./types.js";

export async function interceptIntent(ctx: OpenClawContext): Promise<void> {
  const { browser, lobster, sessions, gateway, workspace, config, logger } = ctx;

  // Check if skill is enabled
  if (!config.get<boolean>("enabled")) {
    gateway.passthrough();
    return;
  }

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
  const parsed = parseIntent(intent, url);

  logger.info(`[ClawMind] Intercepting intent: "${parsed.normalized}" on ${parsed.domain}`);

  // ===== Step 1: Query local store first (save tokens!) =====
  const localWorkflow = findLocalWorkflow(
    { storageDir: "", enabled: true }, // 使用默认配置
    parsed.normalized,
    url
  );

  if (localWorkflow) {
    logger.info(`[ClawMind] Local workflow found, executing directly (saves tokens!)`);

    // Validate and execute local workflow
    if (!lobster.validate(localWorkflow)) {
      logger.warn(`[ClawMind] Local workflow validation failed, falling back`);
    } else {
      try {
        const execResult = await lobster.execute(localWorkflow);
        if (execResult.success) {
          logger.info(`[ClawMind] Local workflow executed successfully`);
          gateway.respond(
            `✅ Done via local cached workflow. ${execResult.steps_completed} steps replayed.`
          );
          return;
        } else {
          logger.warn(`[ClawMind] Local workflow failed: ${execResult.error}`);
          recordLocalFailure({ storageDir: "", enabled: true }, parsed.normalized, url);
        }
      } catch (err) {
        logger.error(`[ClawMind] Local workflow execution error: ${err}`);
      }
    }
  }

  // ===== Step 2: Query cloud if local miss =====
  const cloudEndpoint = config.get<string>("cloud_endpoint");
  const timeoutMs = config.get<number>("timeout_ms");
  const client = new CloudClient(cloudEndpoint, timeoutMs, logger);

  let matchResult: MatchResponse | null = null;
  try {
    matchResult = await client.match({
      intent: parsed.normalized,
      url,
      dom_skeleton_hash: domHash,
      node_id: nodeId,
    });
  } catch {
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
  logger.info(
    `[ClawMind] Cloud match found: ${macro.macro_id} (score: ${matchResult.match_score}, method: ${matchResult.match_method})`
  );

  // Validate the workflow before execution
  if (!lobster.validate(macro.lobster_workflow)) {
    logger.warn(`[ClawMind] Workflow validation failed for ${macro.macro_id}`);
    gateway.passthrough();
    return;
  }

  // Execute the Lobster workflow
  let execResult: LobsterExecutionResult;
  try {
    execResult = await lobster.execute(macro.lobster_workflow);
  } catch (err) {
    logger.error(`[ClawMind] Lobster execution threw: ${err}`);

    // Report failure to cloud (fire-and-forget)
    client.reportFailure({
      macro_id: macro.macro_id,
      node_id: nodeId,
      error_type: "other",
      error_detail: String(err),
    }).catch(() => {});

    // Fall back to normal OpenClaw flow
    gateway.passthrough();
    return;
  }

  if (execResult.success) {
    logger.info(
      `[ClawMind] Macro ${macro.macro_id} executed successfully (${execResult.steps_completed}/${execResult.total_steps} steps)`
    );
    gateway.respond(
      `✅ Done via ClawMind cached workflow (${macro.macro_id}). ` +
      `${execResult.steps_completed} steps replayed.`
    );
  } else {
    logger.warn(
      `[ClawMind] Macro ${macro.macro_id} failed at step ${execResult.failed_step_id}: ${execResult.error}`
    );

    // Map error to error_type
    const errorType = mapErrorType(execResult.error || "");

    client.reportFailure({
      macro_id: macro.macro_id,
      node_id: nodeId,
      error_type: errorType,
      error_detail: execResult.error,
    }).catch(() => {});

    // Fall back to normal OpenClaw flow
    gateway.passthrough();
  }
}

/**
 * Hook: called when a session completes successfully.
 * Compiles the session trace into a Lobster workflow and:
 * 1. Saves to local store (for faster retrieval next time)
 * 2. Contributes to cloud (for sharing with other nodes)
 */
export async function onSessionComplete(ctx: OpenClawContext): Promise<void> {
  const { browser, sessions, workspace, config, logger } = ctx;

  if (!config.get<boolean>("enabled") || !config.get<boolean>("auto_contribute")) {
    return;
  }

  const sessionId = sessions.getCurrentSessionId();
  const history = await sessions.getHistory(sessionId);

  // Only contribute successful sessions with meaningful actions
  if (history.status !== "success") return;
  if (history.actions.length < 2) return;

  const intent = history.intent;
  if (!intent) return;

  const url = await browser.getCurrentUrl();
  const domHash = await browser.getDomSkeletonHash();
  const nodeId = workspace.getNodeId();

  // Compile the trace into a Lobster workflow
  const { workflow, argCount } = compileTrace(intent, history.actions);

  // Skip trivial workflows (single step, no real logic)
  if (workflow.steps.length < 2) {
    logger.debug("[ClawMind] Workflow too trivial to contribute, skipping");
    return;
  }

  logger.info(
    `[ClawMind] Saving workflow "${workflow.name}" (${workflow.steps.length} steps, ${argCount} args)`
  );

  // ===== Step 1: Save to local store =====
  try {
    saveLocalWorkflow(
      { storageDir: "", enabled: true },
      intent,
      url,
      workflow
    );
    logger.info("[ClawMind] Workflow saved to local store");
  } catch (err) {
    logger.warn(`[ClawMind] Failed to save local workflow: ${err}`);
  }

  // ===== Step 2: Contribute to cloud =====
  const cloudEndpoint = config.get<string>("cloud_endpoint");
  const client = new CloudClient(cloudEndpoint, 5000, logger);

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
      logger.info(`[ClawMind] Cloud contribution accepted: ${result.macro_id}`);
    } else {
      logger.debug(`[ClawMind] Cloud contribution not accepted: ${result?.reason}`);
    }
  } catch (err) {
    logger.debug(`[ClawMind] Cloud contribution failed: ${err}`);
  }
}

function mapErrorType(
  error: string
): "selector_not_found" | "timeout" | "unexpected_state" | "other" {
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
