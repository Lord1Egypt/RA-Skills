/**
 * SPM v4 — Main exports.
 *
 * Re-exports all public modules: engine, event-store, security,
 * wbs, hooks, session, and config.
 *
 * @example
 * ```js
 * import { Engine, EventStore, SecurityGate, WBS } from 'openclaw-spm';
 *
 * const engine = new Engine({ context: { projectName: 'my-project' } });
 * const store = new EventStore();
 * const gate = new SecurityGate();
 * const wbs = new WBS();
 * ```
 *
 * @module index
 */

// ── Engine ────────────────────────────────────
export { Engine, EngineError } from './engine/index.js';
export {
  buildPhaseDefinitions,
  PHASE_INDEX,
  PHASE_NAMES,
  isTransitionAllowed,
  getDefaultTransitions,
} from './engine/phases.js';
export {
  Workflow,
  registerWorkflow,
  getWorkflow,
  listWorkflows,
  unregisterWorkflow,
  clearWorkflowRegistry,
} from './engine/workflow.js';

// ── Event Store ───────────────────────────────
export { EventStore, buildDomainConfigs } from './event-store/index.js';
export {
  readAll,
  readRange,
  readRecent,
  append,
  appendBatch,
  rotate,
  prune,
} from './event-store/storage.js';

// ── Security ──────────────────────────────────
export {
  SecurityGate,
  defaultGate,
  Policy,
  Classifier,
} from './security/index.js';

// ── WBS ──────────────────────────────────────
export { WBS, WBSError, parseLedger, STATUSES, STATUS_TRANSITIONS } from './wbs/index.js';
export { attest, verify, hashContent, loadAttestation, checkAttestation } from './wbs/attest.js';
export { MerkleTree, MerkleWBS, hashTask } from './wbs/merkle.js';

// ── Hooks ────────────────────────────────────
export {
  register as registerHook,
  unregister as unregisterHook,
  run as runHooks,
  list as listHooks,
  clear as clearHooks,
} from './hooks/index.js';

// ── Session ──────────────────────────────────
export { generateRecoveryReport, getCheckpoint } from './session/index.js';

// ── Config ───────────────────────────────────
export { loadConfig, requireConfig, DEFAULT_CONFIG, DEFAULT_CONFIG_PATH } from './config/loader.js';
export { validateConfig } from './config/schema.js';

// ── CLI (for programmatic use) ───────────────
export { register as registerCommand, getCommands, get as getCommand, printHelp } from './cli/commands.js';
export { initCommand } from './cli/init.js';
export { attestCommand } from './cli/attest.js';
export { verifyCommand } from './cli/verify.js';
export { qualityCommand } from './cli/quality.js';
export { statusCommand } from './cli/status.js';
export { doctorCommand } from './cli/doctor.js';