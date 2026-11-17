/**
 * @file Security Gate — the main entry point for the SPM security module.
 *
 * Provides a 3-level classification (safe / risky / dangerous) for shell
 * commands using a YAML-based policy engine.
 *
 * @example
 * ```js
 * import { SecurityGate } from './security/index.js';
 *
 * const gate = new SecurityGate();
 * await gate.ready();               // ensure policy is loaded
 *
 * gate.check('rm -rf /');           // { action: 'block', level: 'dangerous', reason: '...' }
 * gate.classify('echo hello');      // { level: 'safe', action: 'allow' }
 * gate.getCurrentPolicy();          // PolicyRule[]
 * ```
 *
 * @module security/index
 */

import { Policy } from './policy.js';
import { Classifier } from './classifier.js';

/**
 * @typedef {'safe'|'risky'|'dangerous'} Level
 * @typedef {'allow'|'warn'|'block'}     Action
 */

/**
 * @typedef {import('./policy.js').PolicyRule} PolicyRule
 */

/**
 * @typedef {Object} Classification
 * @property {Level}   level   - Severity level.
 * @property {Action}  action  - Recommended action.
 * @property {string}  reason  - Explanation.
 * @property {string}  [match] - The regex pattern that matched.
 */

// ---------------------------------------------------------------------------
// SecurityGate
// ---------------------------------------------------------------------------

/**
 * Security gate that classifies shell commands and enforces policy rules.
 *
 * **3-level classification:**
 * - `safe` –     allowed without intervention (action: `allow`)
 * - `risky` –    allowed with a warning (action: `warn`)
 * - `dangerous` – blocked outright (action: `block`)
 *
 * @example
 * ```js
 * const gate = new SecurityGate();
 * const result = gate.check('rm -rf /important');
 * if (result.action === 'block') {
 *   console.error(`🔒 Blocked: ${result.reason}`);
 * }
 * ```
 */
export class SecurityGate {
  /** @type {Policy} */
  #policy;

  /** @type {Classifier} */
  #classifier;

  /** @type {boolean} */
  #loaded = false;

  /**
   * @param {object}      [options]             - Options.
   * @param {string|null} [options.policyPath]  - Path to YAML policy file.
   * @param {Policy}      [options.policy]      - Pre-configured Policy instance.
   */
  constructor(options = {}) {
    if (options.policy) {
      this.#policy = options.policy;
    } else {
      this.#policy = new Policy({ policyPath: options.policyPath ?? null });
    }

    this.#classifier = new Classifier(this.#policy.getRules());
    this.#loaded = this.#policy.getRules().length > 0;
  }

  /**
   * Ensure the policy is loaded.
   *
   * Call this before querying the gate if you want to guarantee the
   * policy file has been read.  If the policy was already loaded (e.g.
   * via constructor or a previous call), this is a no-op.
   *
   * @returns {this}
   */
  ready() {
    if (!this.#loaded) {
      this.#policy.load();
      this.#classifier = new Classifier(this.#policy.getRules());
      this.#loaded = true;
    }
    return this;
  }

  /**
   * Classify a command and return the full classification object.
   *
   * Alias for {@link SecurityGate#classify}.
   *
   * @param {string} command - Shell command to evaluate.
   * @returns {Classification}
   */
  check(command) {
    this.ready();
    return this.#classifier.classify(command);
  }

  /**
   * Classify a command and return the full classification object.
   *
   * @param {string} command - Shell command to evaluate.
   * @returns {Classification}
   */
  classify(command) {
    this.ready();
    return this.#classifier.classify(command);
  }

  /**
   * Return a snapshot of the currently loaded policy rules.
   *
   * @returns {PolicyRule[]} Shallow copy of the active rules.
   */
  getCurrentPolicy() {
    this.ready();
    return this.#policy.getRules();
  }

  /**
   * Reload the policy from disk (or fall back to built-in defaults).
   *
   * @param {string} [policyPath] - Optional override path.
   * @returns {PolicyRule[]}
   */
  reloadPolicy(policyPath) {
    this.#policy.load(policyPath);
    this.#classifier = new Classifier(this.#policy.getRules());
    return this.#policy.getRules();
  }

  /**
   * Return metadata about the active policy (source file, rule count).
   *
   * @returns {{ source: string|null, ruleCount: number }}
   */
  policyInfo() {
    this.ready();
    return this.#policy.getInfo();
  }
}

// ---------------------------------------------------------------------------
// Convenience exports
// ---------------------------------------------------------------------------

/**
 * Pre-initialized default security gate singleton.
 *
 * @type {SecurityGate}
 */
export const defaultGate = new SecurityGate();
defaultGate.ready();

export { Policy } from './policy.js';
export { Classifier } from './classifier.js';