/**
 * SPM v4 — Workflow orchestration.
 *
 * Loads workflow definitions and orchestrates phase sequences through
 * the state machine engine.  Each workflow describes a named pipeline
 * with an ordered list of phases, optional condition keys, and trigger
 * metadata that the engine evaluates before advancing.
 *
 * @module engine/workflow
 */

import { Engine, EngineError } from './index.js';

// ──────────────────────────────────────────────
// Types (JSDoc)
// ──────────────────────────────────────────────

/**
 * @typedef {Object} WorkflowPhase
 * @property {string} name       — Phase name (matches phases.js)
 * @property {object} [context]  — Context data to merge when entering
 */

/**
 * @typedef {Object} WorkflowTrigger
 * @property {string} event   — Event name that fires the trigger
 * @property {"enter"|"leave"|"before"|"after"} hook — When to evaluate
 * @property {function} [handler] — Optional inline callback
 */

/**
 * @typedef {Object} WorkflowDefinition
 * @property {string} id                   — Unique workflow identifier
 * @property {string} [description]        — Human‑readable description
 * @property {WorkflowPhase[]} phases      — Ordered sequence of phases
 * @property {WorkflowTrigger[]} [triggers]  — Trigger definitions
 * @property {Object<string, *>} [conditions] — Named condition map
 */

// ──────────────────────────────────────────────
// Workflow class
// ──────────────────────────────────────────────

export class Workflow {
  /** @type {string} */
  #id;
  /** @type {string|undefined} */
  #description;
  /** @type {WorkflowPhase[]} */
  #phases;
  /** @type {WorkflowTrigger[]} */
  #triggers;
  /** @type {Object<string, *>} */
  #conditions;
  /** @type {Engine|null} */
  #engine;
  /** @type {number} */
  #currentStep;

  /**
   * Create a new Workflow instance.
   *
   * @param {WorkflowDefinition} definition — Workflow definition object
   * @throws {EngineError} If the definition is invalid
   */
  constructor(definition) {
    this.#validateDefinition(definition);

    this.#id = definition.id;
    this.#description = definition.description;
    this.#phases = definition.phases;
    this.#triggers = definition.triggers ?? [];
    this.#conditions = definition.conditions ?? {};
    this.#engine = null;
    this.#currentStep = 0;
  }

  /**
   * Validate a raw workflow definition.
   *
   * @param {*} def — Incoming definition
   * @returns {void}
   * @throws {EngineError}
   */
  #validateDefinition(def) {
    if (!def || typeof def !== 'object') {
      throw new EngineError('INVALID_WORKFLOW', 'Workflow definition must be a non‑null object');
    }
    if (typeof def.id !== 'string' || def.id.length === 0) {
      throw new EngineError('INVALID_WORKFLOW', 'Workflow definition must have a non‑empty "id"');
    }
    if (!Array.isArray(def.phases) || def.phases.length === 0) {
      throw new EngineError('INVALID_WORKFLOW', 'Workflow definition must have a non‑empty "phases" array');
    }
    for (let i = 0; i < def.phases.length; i++) {
      const p = def.phases[i];
      if (!p || typeof p.name !== 'string') {
        throw new EngineError(
          'INVALID_WORKFLOW',
          `Workflow phase at index ${i} must have a string "name"`,
        );
      }
    }
    if (def.triggers && !Array.isArray(def.triggers)) {
      throw new EngineError('INVALID_WORKFLOW', 'Workflow "triggers" must be an array');
    }
    if (def.conditions && (typeof def.conditions !== 'object' || Array.isArray(def.conditions))) {
      throw new EngineError('INVALID_WORKFLOW', 'Workflow "conditions" must be a plain object');
    }
  }

  // ── Accessors ──────────────────────────────

  /** @returns {string} */
  get id() {
    return this.#id;
  }

  /** @returns {string|undefined} */
  get description() {
    return this.#description;
  }

  /** @returns {WorkflowPhase[]} */
  get phases() {
    return this.#phases.map((p) => ({ ...p }));
  }

  /** @returns {WorkflowTrigger[]} */
  get triggers() {
    return this.#triggers.map((t) => ({ ...t }));
  }

  /** @returns {Object<string, *>} */
  get conditions() {
    return { ...this.#conditions };
  }

  /** @returns {boolean} — true when the workflow has run to completion */
  get isComplete() {
    return this.#currentStep >= this.#phases.length;
  }

  /** @returns {number} — 0‑based index of the current step */
  get currentStep() {
    return this.#currentStep;
  }

  // ── Execution ──────────────────────────────

  /**
   * Bind this workflow to an engine and begin execution from phase 0.
   *
   * @param {Engine} engine    — An already‑initialised SPM engine
   * @param {object} [ctx={}]  — Initial context to merge into the engine
   * @returns {Promise<void>}
   * @throws {EngineError} If already started or engine argument is invalid
   */
  async start(engine, ctx = {}) {
    if (!(engine instanceof Engine)) {
      throw new EngineError('INVALID_ENGINE', 'start() requires an Engine instance');
    }
    if (this.#engine) {
      throw new EngineError('ALREADY_STARTED', `Workflow "${this.#id}" has already been started`);
    }

    this.#engine = engine;
    this.#currentStep = 0;

    // Register triggers as event listeners
    this.#registerTriggers(engine);

    // Execute the first phase
    await this.#executeCurrentStep(ctx);
  }

  /**
   * Register workflow triggers as engine event listeners.
   *
   * @param {Engine} engine
   */
  #registerTriggers(engine) {
    for (const trigger of this.#triggers) {
      const eventName = trigger.hook === 'enter' ? 'enter'
        : trigger.hook === 'leave' ? 'transition'
        : trigger.hook;
      // If the event name is unknown, skip silently
      if (!['enter', 'transition', 'error'].includes(eventName)) continue;

      engine.on(eventName, (payload) => {
        trigger.handler?.(payload, this);
        this.#evaluateConditionTriggers(payload);
      });
    }
  }

  /**
   * After every phase enter, check if any condition‑based trigger should fire.
   * Condition triggers are defined as function-valued entries in #conditions.
   *
   * @param {object} payload — Event payload
   */
  #evaluateConditionTriggers(payload) {
    for (const [key, condition] of Object.entries(this.#conditions)) {
      if (typeof condition === 'function') {
        try {
          const result = condition(payload, this);
          if (result === true) {
            this.#engine?.updateContext({ [`trigger_${key}`]: true });
          }
        } catch {
          // condition evaluation errors are non‑fatal
        }
      }
    }
  }

  /**
   * Advance the workflow to the next phase.
   *
   * @param {object} [ctx={}] — Context merge payload
   * @returns {Promise<boolean>} — true if another phase was entered
   * @throws {EngineError} If the workflow is not started or already complete
   */
  async next(ctx = {}) {
    if (!this.#engine) {
      throw new EngineError('NOT_STARTED', `Workflow "${this.#id}" has not been started`);
    }
    if (this.isComplete) {
      throw new EngineError('WORKFLOW_COMPLETE', `Workflow "${this.#id}" is already complete`);
    }

    this.#currentStep++;
    if (this.isComplete) {
      return false;
    }

    await this.#executeCurrentStep(ctx);
    return true;
  }

  /**
   * Execute the phase at the current step index.
   *
   * @param {object} ctx — Context merge payload
   */
  async #executeCurrentStep(ctx = {}) {
    const step = this.#phases[this.#currentStep];
    const engine = /** @type {Engine} */ (this.#engine);

    engine.phase(step.name, { ...(step.context ?? {}), ...ctx });
  }

  /**
   * Run the entire workflow from start to finish without manual stepping.
   *
   * @param {Engine} engine     — SPM engine
   * @param {object} [ctx={}]   — Initial context
   * @returns {Promise<void>}
   */
  async run(engine, ctx = {}) {
    await this.start(engine, ctx);

    while (!this.isComplete) {
      const hasNext = await this.next();
      if (!hasNext) break;
    }
  }

  /**
   * Create a Workflow from a plain definition object.
   *
   * @param {WorkflowDefinition} def
   * @returns {Workflow}
   */
  static fromDefinition(def) {
    return new Workflow(def);
  }

  /**
   * Return a serialisable snapshot of the workflow state.
   *
   * @returns {object}
   */
  serialize() {
    return {
      id: this.#id,
      description: this.#description,
      phases: this.#phases.map((p) => ({ ...p })),
      triggers: this.#triggers.map((t) => ({ ...t, handler: undefined })),
      conditions: Object.keys(this.#conditions),
      currentStep: this.#currentStep,
      isComplete: this.isComplete,
    };
  }
}

// ──────────────────────────────────────────────
// Workflow registry
// ──────────────────────────────────────────────

/** @type {Map<string, Workflow>} */
const registry = new Map();

/**
 * Register a workflow definition so it can be looked up by id.
 *
 * @param {WorkflowDefinition} def
 * @returns {Workflow}
 * @throws {EngineError} If a workflow with the same id already exists
 */
export function registerWorkflow(def) {
  if (registry.has(def.id)) {
    throw new EngineError(
      'WORKFLOW_EXISTS',
      `A workflow with id "${def.id}" is already registered`,
    );
  }
  const wf = new Workflow(def);
  registry.set(def.id, wf);
  return wf;
}

/**
 * Retrieve a previously registered workflow by id.
 *
 * @param {string} id
 * @returns {Workflow|undefined}
 */
export function getWorkflow(id) {
  return registry.get(id);
}

/**
 * List all registered workflow ids and descriptions.
 *
 * @returns {Array<{ id: string, description?: string }>}
 */
export function listWorkflows() {
  return Array.from(registry.values()).map((wf) => ({
    id: wf.id,
    description: wf.description,
  }));
}

/**
 * Remove a workflow from the registry.
 *
 * @param {string} id
 * @returns {boolean} — Whether a workflow was removed
 */
export function unregisterWorkflow(id) {
  return registry.delete(id);
}

/**
 * Clear all registered workflows.
 * @returns {void}
 */
export function clearWorkflowRegistry() {
  registry.clear();
}