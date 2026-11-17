/**
 * SPM v4 — Configuration loader.
 *
 * Loads YAML configuration from a file path (default: `src/config/default.yaml`),
 * validates it against the schema, and merges with built-in defaults for any
 * missing keys.
 *
 * @module config/loader
 */

import { readFileSync, existsSync } from 'node:fs';
import { resolve as resolvePath, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parse as parseYaml } from 'yaml';
import { validateConfig } from './schema.js';

// ──────────────────────────────────────────────
// Constants
// ──────────────────────────────────────────────

/** @type {string} */
const __filename = fileURLToPath(import.meta.url);
/** @type {string} */
const __dirname = dirname(__filename);

/**
 * Default configuration object used when no config file is found or
 * when loaded config is missing keys.
 *
 * @type {import('./schema.js').ValidatedConfig}
 */
export const DEFAULT_CONFIG = Object.freeze({
  engine: Object.freeze({
    lifecycle: Object.freeze({
      phases: Object.freeze([
        { id: 0, name: 'context-init', description: 'Deep context initialization' },
        { id: 1, name: 'requirement', description: 'Requirement gathering and design' },
        { id: 2, name: 'planning', description: 'WBS planning and task breakdown' },
        { id: 3, name: 'execution', description: 'Task execution via subagents' },
        { id: 4, name: 'quality', description: 'Quality gates and verification' },
        { id: 5, name: 'delivery', description: 'Deployment and delivery summary' },
      ]),
      default_phase: 3,
    }),
    transitions: Object.freeze([
      { from: '*', to: '*', condition: 'always' },
    ]),
  }),
  event_store: Object.freeze({
    domains: Object.freeze({
      audit: Object.freeze({ retention: '90d', schema_version: 1 }),
      integrity: Object.freeze({ retention: '180d', schema_version: 1 }),
      quality: Object.freeze({ retention: '30d', schema_version: 1 }),
    }),
  }),
  security: Object.freeze({
    policy_file: 'config/security-policy.yaml',
    default_action: 'block',
  }),
  wbs: Object.freeze({
    ledger_path: 'docs/spm/ledger.md',
    hash_separate_path: '.spm/wbs-attestation',
    merkle_enabled: true,
  }),
});

/**
 * Default config file path: `src/config/default.yaml` relative to this file.
 *
 * @type {string}
 */
export const DEFAULT_CONFIG_PATH = resolvePath(__dirname, 'default.yaml');

// ──────────────────────────────────────────────
// Deep merge
// ──────────────────────────────────────────────

/**
 * Deep-merge two objects. Returns a new object.
 * For any key where both values are plain objects, recurse.
 * Otherwise, the override wins.
 *
 * @param {object} defaults — Base/default values
 * @param {object} overrides — Override values (takes precedence)
 * @returns {object} Merged result
 */
function deepMerge(defaults, overrides) {
  const result = { ...defaults };

  for (const key of Object.keys(overrides)) {
    const dVal = defaults[key];
    const oVal = overrides[key];

    if (isPlainObject(dVal) && isPlainObject(oVal)) {
      result[key] = deepMerge(dVal, oVal);
    } else {
      result[key] = oVal;
    }
  }

  return result;
}

/**
 * Check if a value is a plain (non-array, non-null) object.
 *
 * @param {*} value
 * @returns {boolean}
 */
function isPlainObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

// ──────────────────────────────────────────────
// Loader
// ──────────────────────────────────────────────

/**
 * Valid configuration result.
 *
 * @typedef {Object} ConfigResult
 * @property {boolean} valid — Always `true` when this type is returned
 * @property {import('./schema.js').ValidatedConfig} config — The validated, merged config object
 * @property {string} source — The file path the config was loaded from (or "defaults")
 */

/**
 * Invalid configuration result.
 *
 * @typedef {Object} ConfigError
 * @property {boolean} valid — Always `false` when this type is returned
 * @property {string[]} errors — List of validation error messages
 * @property {import('./schema.js').ValidatedConfig | null} config — The raw config (may be partial)
 * @property {string} source — The file path attempted
 */

/**
 * @typedef {ConfigResult | ConfigError} LoadResult
 */

/**
 * Load and validate the SPM configuration.
 *
 * Reads a YAML config file (defaults to `src/config/default.yaml`),
 * parses it, validates against the schema, and merges with built-in
 * defaults for any missing keys.
 *
 * If the file does not exist, the built-in defaults are returned.
 * If the file exists but fails validation, errors are returned and
 * the caller should decide whether to continue with defaults.
 *
 * @param {string} [configPath] — Custom path to a YAML config file.
 *        Falls back to the default bundled config.
 * @returns {LoadResult} Either valid config or error info
 *
 * @example
 * ```js
 * const result = loadConfig();
 * if (result.valid) {
 *   console.log('Using config:', result.config.engine.lifecycle.default_phase);
 * } else {
 *   console.error('Config errors:', result.errors);
 * }
 *
 * // Custom path
 * const custom = loadConfig('/path/to/spm-config.yaml');
 * ```
 */
export function loadConfig(configPath) {
  const path = configPath || DEFAULT_CONFIG_PATH;
  const resolved = resolvePath(path);

  // If the file doesn't exist, return defaults
  if (!existsSync(resolved)) {
    return {
      valid: true,
      config: deepMerge({}, DEFAULT_CONFIG),
      source: 'defaults',
    };
  }

  // Read and parse
  let raw;
  try {
    const content = readFileSync(resolved, 'utf-8');
    raw = parseYaml(content);
  } catch (err) {
    return {
      valid: false,
      errors: [`Failed to read or parse config file "${resolved}": ${err.message}`],
      config: null,
      source: resolved,
    };
  }

  // Validate
  const errors = validateConfig(raw);
  if (errors.length > 0) {
    return {
      valid: false,
      errors,
      config: raw,
      source: resolved,
    };
  }

  // Merge with defaults
  const merged = deepMerge(DEFAULT_CONFIG, raw);

  return {
    valid: true,
    config: merged,
    source: resolved,
  };
}

/**
 * Convenience: load config and throw on validation errors.
 *
 * Useful when the caller wants a simple, fail-fast interface.
 *
 * @param {string} [configPath] — Custom config file path
 * @returns {import('./schema.js').ValidatedConfig} The validated, merged config
 * @throws {Error} If the config file has validation errors
 *
 * @example
 * ```js
 * const config = requireConfig();
 * // config is guaranteed valid
 * ```
 */
export function requireConfig(configPath) {
  const result = loadConfig(configPath);
  if (!result.valid) {
    const msgs = result.errors.join('; ');
    throw new Error(`Configuration validation failed: ${msgs}`);
  }
  return result.config;
}