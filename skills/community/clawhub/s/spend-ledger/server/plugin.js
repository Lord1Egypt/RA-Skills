/**
 * spend-ledger OpenClaw plugin entry point.
 *
 * Registers two hooks:
 *
 * 1. before_tool_call — enforcement layer.
 *    Blocks a payment if an identical call (same input_hash) already
 *    succeeded in the current session. Stops duplicate payments before
 *    money moves.
 *
 * 2. tool_result_persist — observation layer.
 *    Detects completed payments and appends them to the transaction log.
 *    Runs after the tool has executed, synchronously.
 *
 * The two hooks share state via pendingCalls (keyed by toolCallId) so that
 * tool_result_persist has access to the original params even if the framework
 * doesn't include them in that event.
 */

import { detectPayment, hasPaymentArgs } from "./detectors.js";
import { readAllTransactions, appendTransaction, hashInput } from "./transactions.js";
import { syncPatterns, loadConfig } from "./patterns-sync.js";

// Bridge: before_tool_call stores params here so tool_result_persist can read them.
// Keyed by toolCallId. Cleaned up after each tool_result_persist fires.
const pendingCalls = new Map();

export function register(api) {

  // Sync community patterns on load, then refresh every 24 hours.
  // Runs in the background — never blocks registration.
  // Download-only (no payment data sent). Disable with sync_community_patterns: false in config.
  const cfg = loadConfig();
  if (cfg.sync_community_patterns !== false) {
    syncPatterns();
    setInterval(syncPatterns, 24 * 60 * 60 * 1000);
  }

  // ── Enforcement ─────────────────────────────────────────────────────────────
  // Fires before the tool executes. Blocks duplicate payments within a session.

  api.on("before_tool_call", async (event, ctx) => {
    const { toolName, params, toolCallId } = event;
    const sessionKey = ctx?.sessionKey ?? null;

    // Quick pre-check: is this even a payment tool?
    // Use hasPaymentArgs as a broader stash trigger — detectPayment can't confirm
    // without a result, but if args look monetary we want to capture them so
    // tool_result_persist can make a proper decision with the full result.
    const argsStr = typeof params === "object" ? JSON.stringify(params || {}) : String(params || "");
    const likelyPayment = detectPayment(toolName, params, "") || hasPaymentArgs(argsStr);
    if (!likelyPayment) return { params };

    // Stash params for tool_result_persist to pick up later.
    if (toolCallId) {
      pendingCalls.set(toolCallId, {
        toolName,
        params,
        inputHash: hashInput(params),
        sessionKey,
      });
    }

    // Without a session key we can't scope deduplication — allow through.
    if (!sessionKey) return { params };

    const inputHash = hashInput(params);
    const txns = readAllTransactions();

    const duplicate = txns.find(
      (t) =>
        t.context?.input_hash === inputHash &&
        t.context?.session_key === sessionKey &&
        t.status === "confirmed"
    );

    if (duplicate) {
      return {
        block: true,
        blockReason:
          `Duplicate payment blocked — identical payment to ` +
          `${duplicate.service?.name || "this service"} ` +
          `already executed at ${duplicate.timestamp} in this session`,
      };
    }

    return { params };
  });

  // ── Observation ──────────────────────────────────────────────────────────────
  // Fires after the tool completes. Logs detected payments to the ledger.
  // Must be synchronous.

  api.on("tool_result_persist", (event, ctx) => {
    const { toolName, toolCallId, message } = event;

    // Retrieve params stashed by before_tool_call, fall back to event.params.
    const pending = toolCallId ? pendingCalls.get(toolCallId) : null;
    const params = pending?.params ?? event.params ?? {};
    const sessionKey = pending?.sessionKey ?? ctx?.sessionKey ?? null;

    // Clean up the bridge entry.
    if (toolCallId) pendingCalls.delete(toolCallId);

    // Normalize tool result from the message content.
    const toolResult =
      typeof message?.content === "string"
        ? message.content
        : Array.isArray(message?.content)
        ? message.content.map((b) => b.text ?? b.content ?? "").join("")
        : JSON.stringify(message?.content ?? "");

    const payment = detectPayment(toolName, params, toolResult);
    if (!payment) return;

    appendTransaction({
      ...payment,
      context: {
        ...payment.context,
        input_hash: pending?.inputHash ?? hashInput(params),
        session_key: sessionKey,
        tool_name: toolName,
      },
    });
  });
}
