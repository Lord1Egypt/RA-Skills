/**
 * @file Command classifier for the SPM security gate.
 * Matches a shell command string against a set of policy rules and
 * returns a classification verdict.
 *
 * @module security/classifier
 */

/**
 * @typedef {'safe'|'risky'|'dangerous'} Level
 * @typedef {'allow'|'warn'|'block'}     Action
 */

/**
 * @typedef {Object} Classification
 * @property {Level}  level   - Severity level.
 * @property {Action} action  - Recommended action.
 * @property {string} reason  - Reason for the classification.
 * @property {string} [match] - The specific rule pattern that matched.
 */

/**
 * @typedef {import('./policy.js').PolicyRule} PolicyRule
 */

// ---------------------------------------------------------------------------
// Classifier
// ---------------------------------------------------------------------------

/**
 * Classify shell commands against a list of policy rules.
 *
 * Rules are checked in order.  The **first** matching rule determines
 * the classification.  If no rule matches, the command is considered
 * **safe** (`{ level: 'safe', action: 'allow' }`).
 *
 * @example
 * ```js
 * const classifier = new Classifier(rules);
 * const result = classifier.classify('rm -rf /');
 * // → { level: 'dangerous', action: 'block', reason: '...', match: '^rm -rf /' }
 * ```
 */
export class Classifier {
  /** @type {PolicyRule[]} */
  #rules;

  /**
   * @param {PolicyRule[]} rules - Ordered array of policy rules.
   */
  constructor(rules) {
    this.#rules = rules;
  }

  /**
   * Classify a shell command by matching it against all loaded rules.
   *
   * @param {string} command - The shell command string to classify.
   * @returns {Classification} Verdict with level, action, and reason.
   */
  classify(command) {
    for (const rule of this.#rules) {
      try {
        const re = new RegExp(rule.pattern);
        if (re.test(command.trim())) {
          return {
            level: rule.level,
            action: rule.action,
            reason: rule.reason,
            match: rule.pattern,
          };
        }
      } catch {
        // Skip rules with invalid regex patterns and continue
        continue;
      }
    }

    return {
      level: 'safe',
      action: 'allow',
      reason: 'Command does not match any policy rule',
    };
  }
}

// ---------------------------------------------------------------------------
// Convenience runner
// ---------------------------------------------------------------------------

/**
 * One-shot classification using the default policy.
 *
 * @param {string}          command - Shell command to classify.
 * @param {PolicyRule[]}    rules   - Policy rules to match against.
 * @returns {Classification}
 */
export function classifyCommand(command, rules) {
  const classifier = new Classifier(rules);
  return classifier.classify(command);
}