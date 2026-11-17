/**
 * SPM v4 — Configuration validation schema.
 *
 * Validates a parsed configuration object against the expected shape.
 * Returns a list of validation errors, or an empty array if valid.
 *
 * @module config/schema
 */

/**
 * @typedef {Object} ValidatedConfig
 * @property {EngineConfig} engine
 * @property {EventStoreConfig} event_store
 * @property {SecurityConfig} security
 * @property {WBSConfig} wbs
 */

/**
 * @typedef {Object} EngineConfig
 * @property {EngineLifecycleConfig} lifecycle
 * @property {Array<{from: string, to: string, condition: string}>} transitions
 */
/**
 * @typedef {Object} EngineLifecycleConfig
 * @property {Array<{id: number, name: string, description: string}>} phases
 * @property {number} default_phase
 */
/**
 * @typedef {Object} EventStoreConfig
 * @property {Object<string, DomainConfig>} domains
 */
/**
 * @typedef {Object} DomainConfig
 * @property {string} retention
 * @property {number} schema_version
 */
/**
 * @typedef {Object} SecurityConfig
 * @property {string} policy_file
 * @property {string} default_action
 */
/**
 * @typedef {Object} WBSConfig
 * @property {string} ledger_path
 * @property {string} hash_separate_path
 * @property {boolean} merkle_enabled
 */

// ──────────────────────────────────────────────
// Validation helpers
// ──────────────────────────────────────────────

/**
 * @param {*} value
 * @returns {boolean}
 */
function isString(value) {
  return typeof value === 'string';
}

/**
 * @param {*} value
 * @returns {boolean}
 */
function isNumber(value) {
  return typeof value === 'number' && !Number.isNaN(value);
}

/**
 * @param {*} value
 * @returns {boolean}
 */
function isBoolean(value) {
  return typeof value === 'boolean';
}

/**
 * @param {*} value
 * @returns {boolean}
 */
function isPlainObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

// ──────────────────────────────────────────────
// Validators
// ──────────────────────────────────────────────

/**
 * Validate the engine configuration section.
 *
 * @param {*} section — The engine config value
 * @param {string} prefix — Dot-separated path prefix for error messages
 * @returns {string[]} Validation errors
 */
function validateEngineConfig(section, prefix) {
  const errors = [];

  if (!isPlainObject(section)) {
    errors.push(`${prefix}: must be a plain object`);
    return errors;
  }

  if (section.lifecycle !== undefined) {
    const lp = `${prefix}.lifecycle`;
    if (!isPlainObject(section.lifecycle)) {
      errors.push(`${lp}: must be a plain object`);
    } else {
      // Validate phases
      if (section.lifecycle.phases !== undefined) {
        if (!Array.isArray(section.lifecycle.phases)) {
          errors.push(`${lp}.phases: must be an array`);
        } else {
          for (let i = 0; i < section.lifecycle.phases.length; i++) {
            const phase = section.lifecycle.phases[i];
            if (!isPlainObject(phase)) {
              errors.push(`${lp}.phases[${i}]: must be a plain object`);
              continue;
            }
            if (!isNumber(phase.id)) {
              errors.push(`${lp}.phases[${i}].id: must be a number`);
            }
            if (!isString(phase.name)) {
              errors.push(`${lp}.phases[${i}].name: must be a string`);
            }
            if (phase.description !== undefined && !isString(phase.description)) {
              errors.push(`${lp}.phases[${i}].description: must be a string`);
            }
          }
        }
      }

      // Validate default_phase
      if (section.lifecycle.default_phase !== undefined && !isNumber(section.lifecycle.default_phase)) {
        errors.push(`${lp}.default_phase: must be a number`);
      }
    }
  }

  // Validate transitions
  if (section.transitions !== undefined) {
    if (!Array.isArray(section.transitions)) {
      errors.push(`${prefix}.transitions: must be an array`);
    } else {
      for (let i = 0; i < section.transitions.length; i++) {
        const t = section.transitions[i];
        if (!isPlainObject(t)) {
          errors.push(`${prefix}.transitions[${i}]: must be a plain object`);
          continue;
        }
        if (!isString(t.from)) {
          errors.push(`${prefix}.transitions[${i}].from: must be a string`);
        }
        if (!isString(t.to)) {
          errors.push(`${prefix}.transitions[${i}].to: must be a string`);
        }
        if (t.condition !== undefined && !isString(t.condition)) {
          errors.push(`${prefix}.transitions[${i}].condition: must be a string`);
        }
      }
    }
  }

  return errors;
}

/**
 * Validate the event_store configuration section.
 *
 * @param {*} section
 * @param {string} prefix
 * @returns {string[]}
 */
function validateEventStoreConfig(section, prefix) {
  const errors = [];

  if (!isPlainObject(section)) {
    errors.push(`${prefix}: must be a plain object`);
    return errors;
  }

  if (section.domains !== undefined) {
    if (!isPlainObject(section.domains)) {
      errors.push(`${prefix}.domains: must be a plain object`);
    } else {
      for (const [domainName, domain] of Object.entries(section.domains)) {
        const dp = `${prefix}.domains.${domainName}`;
        if (!isPlainObject(domain)) {
          errors.push(`${dp}: must be a plain object`);
          continue;
        }
        if (domain.retention !== undefined && !isString(domain.retention)) {
          errors.push(`${dp}.retention: must be a string (e.g. "90d")`);
        }
        if (domain.schema_version !== undefined && !isNumber(domain.schema_version)) {
          errors.push(`${dp}.schema_version: must be a number`);
        }
      }
    }
  }

  return errors;
}

/**
 * Validate the security configuration section.
 *
 * @param {*} section
 * @param {string} prefix
 * @returns {string[]}
 */
function validateSecurityConfig(section, prefix) {
  const errors = [];

  if (!isPlainObject(section)) {
    errors.push(`${prefix}: must be a plain object`);
    return errors;
  }

  if (section.policy_file !== undefined && !isString(section.policy_file)) {
    errors.push(`${prefix}.policy_file: must be a string`);
  }
  if (
    section.default_action !== undefined &&
    !['allow', 'warn', 'block'].includes(section.default_action)
  ) {
    errors.push(`${prefix}.default_action: must be one of "allow", "warn", "block"`);
  }

  return errors;
}

/**
 * Validate the wbs configuration section.
 *
 * @param {*} section
 * @param {string} prefix
 * @returns {string[]}
 */
function validateWBSConfig(section, prefix) {
  const errors = [];

  if (!isPlainObject(section)) {
    errors.push(`${prefix}: must be a plain object`);
    return errors;
  }

  if (section.ledger_path !== undefined && !isString(section.ledger_path)) {
    errors.push(`${prefix}.ledger_path: must be a string`);
  }
  if (section.hash_separate_path !== undefined && !isString(section.hash_separate_path)) {
    errors.push(`${prefix}.hash_separate_path: must be a string`);
  }
  if (section.merkle_enabled !== undefined && !isBoolean(section.merkle_enabled)) {
    errors.push(`${prefix}.merkle_enabled: must be a boolean`);
  }

  return errors;
}

// ──────────────────────────────────────────────
// Main validation
// ──────────────────────────────────────────────

/**
 * Validate a parsed configuration object.
 *
 * Checks the shape of each section (engine, event_store, security, wbs)
 * and returns a list of all validation errors found. An empty array
 * means the config is valid.
 *
 * @param {*} config — Parsed configuration object (from YAML)
 * @returns {string[]} Array of error messages (empty = valid)
 *
 * @example
 * ```js
 * const errors = validateConfig(parsedYaml);
 * if (errors.length > 0) {
 *   console.error('Config validation failed:');
 *   errors.forEach(e => console.error(`  - ${e}`));
 * }
 * ```
 */
export function validateConfig(config) {
  const errors = [];

  if (!isPlainObject(config)) {
    errors.push('root: configuration must be a plain object');
    return errors;
  }

  if (config.engine !== undefined) {
    errors.push(...validateEngineConfig(config.engine, 'engine'));
  }

  if (config.event_store !== undefined) {
    errors.push(...validateEventStoreConfig(config.event_store, 'event_store'));
  }

  if (config.security !== undefined) {
    errors.push(...validateSecurityConfig(config.security, 'security'));
  }

  if (config.wbs !== undefined) {
    errors.push(...validateWBSConfig(config.wbs, 'wbs'));
  }

  return errors;
}