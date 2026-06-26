/**
 * @wtt/plugin — WTT Channel Plugin for OpenClaw
 *
 * Adds WTT as a first-class communication channel with:
 *   - Persistent WebSocket to WTT cloud
 *   - E2E encryption (AES-256-CTR with PBKDF2 key derivation)
 *   - A2UI interactive messages (buttons, selects, confirms)
 *   - Lifecycle hooks (before/after tool calls)
 *   - Multi-account support
 */

// Plugin
export { wttPlugin, processWTTCommandText } from "./channel.js";

// Commands (@wtt ...)
export { createWTTCommandRouter, parseWTTCommandText } from "./commands/index.js";
export type { ParsedWTTCommand, WTTCommandProcessResult } from "./commands/index.js";

// WebSocket Client
export { WTTCloudClient } from "./ws-client.js";
export type { WTTCloudClientOptions } from "./ws-client.js";

// E2E Crypto
export {
  deriveKey,
  encryptText,
  decryptText,
  encryptBytes,
  decryptBytes,
  toBase64,
  fromBase64,
} from "./e2e-crypto.js";

// Runtime scaffolding (P3-prep)
export {
  createSessionBindingPlaceholder,
  describeSessionBindingNextAction,
  buildProgressHeartbeat,
  validateTaskTransition,
  createTaskRunExecutorLoop,
  getSharedTaskRunExecutor,
} from "./runtime/index.js";

export type {
  SessionBindingPlaceholder,
  ProgressHeartbeatPayload,
  RuntimeReviewAction,
  RuntimeTransitionIntent,
  RuntimeTransitionResult,
  TaskRunDetailPayload,
  TaskRunExecutionResult,
  TaskRunExecutorLoop,
  TaskRunExecutorLoopOptions,
  TaskRunExecutorRequest,
  TaskRunExecutorSnapshot,
  TaskRunInferenceRequest,
  TaskRunInferenceResult,
  TaskRunPersistenceAck,
  TaskRunSummaryPayload,
} from "./runtime/index.js";

// Types
export type {
  WTTAccountConfig,
  ResolvedWTTAccount,
  WsAction,
  WsActionMessage,
  WsAuthMessage,
  WsActionResult,
  WsNewMessage,
  WsTaskStatus,
  WsServerMessage,
  WsMessagePayload,
  WsTopicPayload,
  ActionPayloads,
  E2EConfig,
  EncryptedContent,
} from "./types.js";
