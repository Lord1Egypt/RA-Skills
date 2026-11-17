/**
 * @file Policy engine for the SPM security gate.
 * Loads YAML policy rules from a file (default: config/security-policy.yaml)
 * and exposes them for command classification.
 *
 * @module security/policy
 */

import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import yaml from 'yaml';

/** @typedef {'safe'|'risky'|'dangerous'} Level */
/** @typedef {'allow'|'warn'|'block'} Action */

/**
 * @typedef {Object} PolicyRule
 * @property {string}   pattern  - Regex pattern to match against a command.
 * @property {Level}    level    - Severity classification.
 * @property {Action}   action   - Recommended action when matched.
 * @property {string}   reason   - Human-readable explanation.
 */

const __filename = fileURLToPath(import.meta.url);
const __dirname   = dirname(__filename);

// ---------------------------------------------------------------------------
// Built-in default rules (used when no policy file is found)
// ---------------------------------------------------------------------------

/**
 * Default policy rules that ship with the module.
 * These provide reasonable baseline protection even without a config file.
 * @type {PolicyRule[]}
 */
const DEFAULT_RULES = Object.freeze([
  {
    pattern: '^rm -rf /',
    level: 'dangerous',
    action: 'block',
    reason: 'Destructive filesystem operation',
  },
  {
    pattern: '^rm -rf \\*',
    level: 'dangerous',
    action: 'block',
    reason: 'Destructive filesystem operation',
  },
  {
    pattern: '^dd if=',
    level: 'dangerous',
    action: 'block',
    reason: 'Potential disk overwrite',
  },
  {
    pattern: '^mkfs\\..+ /dev/',
    level: 'dangerous',
    action: 'block',
    reason: 'Filesystem creation may destroy data',
  },
  {
    pattern: '^:(){ :\\|:& };:',
    level: 'dangerous',
    action: 'block',
    reason: 'Fork bomb denial-of-service',
  },
  {
    pattern: '^curl .*\\| sh$',
    level: 'risky',
    action: 'warn',
    reason: 'Remote code execution via pipe to shell',
  },
  {
    pattern: '^bash <\\(curl ',
    level: 'risky',
    action: 'warn',
    reason: 'Remote code execution via process substitution',
  },
  {
    pattern: '^git push --force',
    level: 'risky',
    action: 'warn',
    reason: 'Force push may overwrite remote history',
  },
  {
    pattern: '^chmod -R 777',
    level: 'risky',
    action: 'warn',
    reason: 'Overly permissive file permissions',
  },
  {
    pattern: '^wget .* -O - \\| sh$',
    level: 'risky',
    action: 'warn',
    reason: 'Remote code execution via pipe to shell',
  },
  {
    pattern: '^sudo rm',
    level: 'risky',
    action: 'warn',
    reason: 'Sudo delete may remove protected system files',
  },
  {
    pattern: '^> /dev/sda',
    level: 'dangerous',
    action: 'block',
    reason: 'Direct block device write',
  },
  {
    pattern: '^pv$|^pv \\d',
    level: 'risky',
    action: 'warn',
    reason: 'Potential LVM physical volume operation',
  },
  {
    pattern: '^eval \\$\\(',
    level: 'risky',
    action: 'warn',
    reason: 'Dynamic command evaluation may be unsafe',
  },
]);

// ---------------------------------------------------------------------------
// Policy class
// ---------------------------------------------------------------------------

/**
 * Policy engine that reads YAML rules from a file or falls back to built-ins.
 *
 * @example
 * ```js
 * const policy = new Policy();
 * policy.load();                  // loads config/security-policy.yaml
 * policy.load('/custom/path.yaml');
 * ```
 */
export class Policy {
  /** @type {PolicyRule[]} */
  #rules = [];

  /** @type {string|null} */
  #sourcePath = null;

  /**
   * Create a Policy instance.
   *
   * @param {object}        [options]             - Options.
   * @param {string|null}   [options.policyPath]  - Explicit path to YAML policy file.
   *                                                If null, the default location is used:
   *                                                `<package-root>/config/security-policy.yaml`.
   */
  constructor(options = {}) {
    this.#sourcePath = options.policyPath ?? null;
  }

  /**
   * Resolve the absolute path to the policy file.
   *
   * The default path is computed relative to the package root
   * (two levels up from `src/security/`).
   *
   * @returns {string} Absolute policy file path.
   */
  getDefaultPolicyPath() {
    return resolve(__dirname, '..', '..', 'config', 'security-policy.yaml');
  }

  /**
   * Load policy rules from a YAML file.
   *
   * If the file does not exist or cannot be parsed, the engine falls back
   * to the built-in {@link DEFAULT_RULES}.  The `policyPath` parameter
   * overrides any path passed in the constructor.
   *
   * @param {string} [policyPath] - Override path for this load call.
   * @returns {PolicyRule[]} The loaded (or fallback) rules.
   */
  load(policyPath) {
    const targetPath = policyPath ?? this.#sourcePath ?? this.getDefaultPolicyPath();

    if (!existsSync(targetPath)) {
      this.#rules = [...DEFAULT_RULES];
      this.#sourcePath = null;
      return this.#rules;
    }

    try {
      const raw = readFileSync(targetPath, 'utf-8');
      const doc = yaml.parse(raw);

      if (!doc || !Array.isArray(doc.rules)) {
        throw new Error('Policy file must contain a top-level "rules" array');
      }

      /** @type {PolicyRule[]} */
      const parsed = doc.rules.map((r, i) => {
        if (!r.pattern || !r.level || !r.action) {
          throw new Error(
            `Rule at index ${i} is missing required fields (pattern, level, action)`,
          );
        }
        return {
          pattern: String(r.pattern),
          level: /** @type {Level} */ (r.level),
          action: /** @type {Action} */ (r.action),
          reason: r.reason ?? 'No reason provided',
        };
      });

      this.#rules = parsed;
      this.#sourcePath = targetPath;
      return this.#rules;
    } catch (err) {
      console.warn(
        `[spm:security] Failed to load policy from "${targetPath}": ${err.message}`,
      );
      console.warn('[spm:security] Falling back to built-in default rules.');
      this.#rules = [...DEFAULT_RULES];
      this.#sourcePath = null;
      return this.#rules;
    }
  }

  /**
   * Return the currently loaded policy rules.
   *
   * @returns {PolicyRule[]} A shallow copy of the in-memory rules.
   */
  getRules() {
    return [...this.#rules];
  }

  /**
   * Return metadata about the policy source.
   *
   * @returns {{ source: string|null, ruleCount: number }}
   */
  getInfo() {
    return {
      source: this.#sourcePath,
      ruleCount: this.#rules.length,
    };
  }
}

// ---------------------------------------------------------------------------
// Convenience singleton
// ---------------------------------------------------------------------------

/**
 * Pre-configured Policy instance using the default policy path.
 *
 * @type {Policy}
 */
export const defaultPolicy = new Policy();
defaultPolicy.load();