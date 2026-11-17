/**
 * SPM v4 — Phase definitions with pre/post conditions.
 *
 * Defines the 6 standard SPM phases and their transition rules.
 * Each phase carries metadata, allowed next phases, and optional
 * pre/post hooks that the engine evaluates before/after entering.
 *
 * @module engine/phases
 */

// ──────────────────────────────────────────────
// Phase index map (0‑based for internal ordering)
// ──────────────────────────────────────────────

export const PHASE_NAMES = Object.freeze({
  0: 'context-init',
  1: 'requirement',
  2: 'planning',
  3: 'execution',
  4: 'quality',
  5: 'delivery',
});

export const PHASE_INDEX = Object.freeze({
  'context-init': 0,
  requirement:    1,
  planning:       2,
  execution:      3,
  quality:        4,
  delivery:       5,
});

// ──────────────────────────────────────────────
// Allowed transitions — ordered graph
// Supports skip-ahead and limited backtrack
// ──────────────────────────────────────────────

const DEFAULT_TRANSITIONS = Object.freeze({
  'context-init': Object.freeze([
    'requirement',
  ]),
  requirement: Object.freeze([
    'planning',
    'context-init',            // revise requirements
  ]),
  planning: Object.freeze([
    'execution',
    'requirement',             // re-plan from requirement changes
  ]),
  execution: Object.freeze([
    'quality',
    'planning',                // re-scope mid execution
  ]),
  quality: Object.freeze([
    'delivery',
    'execution',               // fix defects → re-execute
    'planning',                // major re-scope
    'requirement',             // fundamental redefinition
  ]),
  delivery: Object.freeze([
    'quality',                 // re-certify after delivery issues
  ]),
});

// ──────────────────────────────────────────────
// Default pre‑condition / post‑condition hooks
// ──────────────────────────────────────────────

/** @type {Object<string, { pre: function, post: function }>} */
const DEFAULT_CONDITIONS = Object.freeze({
  'context-init': Object.freeze({
    pre:  () => true,
    post: () => true,
  }),
  requirement: Object.freeze({
    pre:  (ctx) => ctx?.projectName && ctx?.goal,
    post: () => true,
  }),
  planning: Object.freeze({
    pre:  (ctx) => ctx?.requirements?.length > 0,
    post: () => true,
  }),
  execution: Object.freeze({
    pre:  (ctx) => ctx?.plan?.steps?.length > 0,
    post: () => true,
  }),
  quality: Object.freeze({
    pre:  (ctx) => ctx?.execution?.output != null,
    post: () => true,
  }),
  delivery: Object.freeze({
    pre:  (ctx) => ctx?.quality?.passed === true,
    post: () => true,
  }),
});

/**
 * @typedef {Object} PhaseDefinition
 * @property {string} name         — Phase name (e.g. "planning")
 * @property {number} index        — 0‑based ordinal
 * @property {string[]} transitions — Allowed target phase names
 * @property {function} pre        — Pre‑condition check (ctx => boolean)
 * @property {function} post       — Post‑condition hook (ctx => void)
 */

/**
 * Build the full set of phase definitions, merging user overrides
 * with default conditions and transitions.
 *
 * @param {object} [overrides={}] — Optional config overrides keyed by phase name
 * @returns {Object<string, PhaseDefinition>} Map of phase name → definition
 */
export function buildPhaseDefinitions(overrides = {}) {
  /** @type {Object<string, PhaseDefinition>} */
  const defs = {};

  for (const name of Object.values(PHASE_NAMES)) {
    const index = PHASE_INDEX[name];
    const defaults = {
      transitions: DEFAULT_TRANSITIONS[name] ?? [],
      pre:   DEFAULT_CONDITIONS[name]?.pre  ?? (() => true),
      post:  DEFAULT_CONDITIONS[name]?.post ?? (() => true),
    };

    const user = overrides[name] ?? {};
    defs[name] = {
      name,
      index,
      transitions: Object.freeze(user.transitions ?? defaults.transitions),
      pre:   user.pre   ?? defaults.pre,
      post:  user.post  ?? defaults.post,
    };
  }

  return defs;
}

/**
 * Validate that a transition from `from` → `to` is allowed.
 *
 * @param {PhaseDefinition} from — Current phase definition
 * @param {PhaseDefinition} to   — Target phase definition
 * @returns {boolean} true if allowed
 */
export function isTransitionAllowed(from, to) {
  return from.transitions.includes(to.name);
}

/**
 * Return the default transition map for reference / testing.
 * @returns {Object<string, string[]>}
 */
export function getDefaultTransitions() {
  return structuredClone(DEFAULT_TRANSITIONS);
}