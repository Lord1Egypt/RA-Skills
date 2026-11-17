/**
 * SPM v4 — State machine engine.
 *
 * Event-driven phase state machine for the SPM workflow lifecycle.
 *
 * Phases:
 *   0 — context-init
 *   1 — requirement
 *   2 — planning
 *   3 — execution
 *   4 — quality
 *   5 — delivery
 *
 * @module engine
 */

import {
  buildPhaseDefinitions,
  PHASE_INDEX,
  isTransitionAllowed,
} from './phases.js';

// ──────────────────────────────────────────────
// Errors
// ──────────────────────────────────────────────

/** Error thrown on invalid phase operations. */
export class EngineError extends Error {
  /**
   * @param {string} code    — Machine‑readable error code
   * @param {string} message — Human‑readable description
   */
  constructor(code, message) {
    super(`[${code}] ${message}`);
    this.name = 'EngineError';
    this.code = code;
  }
}

// ──────────────────────────────────────────────
// Engine
// ──────────────────────────────────────────────

export class Engine {
  #phases;
  #current;
  #context;
  #listeners;
  #history;

  /**
   * Create a new SPM state machine engine.
   *
   * @param {object} config               — Configuration object (from config/loader.js).
   * @param {object} [config.phases={}]   — Optional phase condition/transition overrides.
   * @param {object} [config.context={}]  — Initial context payload (project name, goal, …).
   */
  constructor(config = {}) {
    const { phases: phaseOverrides = {}, context: initialContext = {} } = config;

    this.#phases = buildPhaseDefinitions(phaseOverrides);

    const initPhase = this.#phases['context-init'];
    if (!initPhase) {
      throw new EngineError('INIT_FAILED', 'context-init phase definition missing');
    }

    // Validate that all phase names have a definition
    for (const name of Object.keys(PHASE_INDEX)) {
      if (!this.#phases[name]) {
        throw new EngineError('INIT_FAILED', `Phase "${name}" has no definition`);
      }
    }

    this.#current = initPhase;
    this.#context = { ...initialContext };
    this.#listeners = new Map();
    this.#history = [{
      phase: initPhase.name,
      enteredAt: Date.now(),
      context: { ...this.#context },
    }];
  }

  // ── Event listeners ────────────────────────

  /**
   * Register a listener for engine events.
   *
   * @param {'enter' | 'transition' | 'error'} event — Event type
   * @param {function} handler                        — Callback receiving event payload
   * @returns {void}
   */
  on(event, handler) {
    if (!this.#listeners.has(event)) {
      this.#listeners.set(event, new Set());
    }
    this.#listeners.get(event).add(handler);
  }

  /**
   * Remove a previously registered listener.
   *
   * @param {'enter' | 'transition' | 'error'} event — Event type
   * @param {function} handler                        — Handler to remove
   * @returns {void}
   */
  off(event, handler) {
    this.#listeners.get(event)?.delete(handler);
  }

  /**
   * Internal: fire all listeners for a given event.
   * @param {string} event
   * @param {object} payload
   */
  #emit(event, payload) {
    this.#listeners.get(event)?.forEach((fn) => {
      try { fn(payload); } catch { /* swallow listener errors */ }
    });
  }

  // ── Phase API ──────────────────────────────

  /**
   * Enter a named phase directly (used for initial setup or forced entry).
   * Evaluates pre‑conditions, records history, fires 'enter' events.
   *
   * @param {string} phaseName — Target phase name
   * @param {object} [ctx={}]  — Context merge payload
   * @returns {object} — The new current phase definition
   * @throws {EngineError} If phase name is unknown or pre‑condition fails
   */
  phase(phaseName, ctx = {}) {
    const target = this.#phases[phaseName];
    if (!target) {
      const err = new EngineError('UNKNOWN_PHASE', `Unknown phase "${phaseName}"`);
      this.#emit('error', { error: err });
      throw err;
    }

    // Merge context
    this.#context = { ...this.#context, ...ctx };

    // Evaluate pre‑condition
    const preOk = target.pre(this.#context);
    if (!preOk) {
      const err = new EngineError(
        'PRECONDITION_FAILED',
        `Pre‑condition failed for phase "${phaseName}"`,
      );
      this.#emit('error', { error: err, phase: phaseName });
      throw err;
    }

    // Execute post‑condition
    target.post(this.#context);

    // Record the phase entry
    this.#current = target;
    this.#history.push({
      phase: target.name,
      enteredAt: Date.now(),
      context: { ...this.#context },
    });

    this.#emit('enter', {
      phase: target.name,
      index: target.index,
      context: { ...this.#context },
    });

    return target;
  }

  /**
   * Transition from the current phase to a target phase.
   * Validates the transition is allowed before proceeding.
   *
   * @param {string} targetPhase — Name of the phase to transition into
   * @param {object} [ctx={}]    — Optional context merge payload
   * @returns {object} — The new current phase definition
   * @throws {EngineError} If transition is not allowed or phase unknown
   */
  transition(targetPhase, ctx = {}) {
    const from = this.#current;
    const to = this.#phases[targetPhase];

    if (!to) {
      const err = new EngineError('UNKNOWN_PHASE', `Unknown phase "${targetPhase}"`);
      this.#emit('error', { error: err });
      throw err;
    }

    if (!isTransitionAllowed(from, to)) {
      const err = new EngineError(
        'INVALID_TRANSITION',
        `Transition "${from.name}" → "${targetPhase}" is not allowed`,
      );
      this.#emit('error', { error: err, from: from.name, to: targetPhase });
      throw err;
    }

    return this.phase(targetPhase, ctx);
  }

  /**
   * Return the current phase definition.
   *
   * @returns {object} Current phase definition `{ name, index, transitions }`
   */
  currentPhase() {
    return { ...this.#current };
  }

  /**
   * Return a shallow copy of the current context.
   *
   * @returns {object}
   */
  getContext() {
    return { ...this.#context };
  }

  /**
   * Merge additional data into the engine context.
   *
   * @param {object} data — Key/value pairs to merge
   * @returns {void}
   */
  updateContext(data) {
    this.#context = { ...this.#context, ...data };
  }

  /**
   * Return the phase history log.
   *
   * @returns {Array<{ phase: string, enteredAt: number, context: object }>}
   */
  getHistory() {
    return [...this.#history];
  }

  /**
   * Check whether the engine is in a specific phase.
   *
   * @param {string} phaseName
   * @returns {boolean}
   */
  isInPhase(phaseName) {
    return this.#current.name === phaseName;
  }

  /**
   * Return the list of phases the engine can transition into from its
   * current position.
   *
   * @returns {string[]}
   */
  allowedTransitions() {
    return [...this.#current.transitions];
  }
}