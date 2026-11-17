'use strict';

import { resolve, dirname } from 'node:path';
import { mkdirSync } from 'node:fs';

/**
 * @typedef {Object} DomainConfig
 * @property {string}    name            - Domain identifier (e.g. 'audit')
 * @property {number}    schema_version  - Version of the domain schema
 * @property {number}    retention_days  - How long to keep events (in days)
 * @property {string}    file_path       - Absolute path to the JSONL file
 * @property {number}    [max_file_size] - Max file size in bytes before rotation (default 10 MB)
 */

/**
 * Map of known domain keys to their configuration.
 *
 * Three default domains:
 * - **audit**     — immutable log of every action (who did what, when)
 * - **integrity** — hash chains, attestations, Merkle proofs
 * - **quality**   — quality gate results, score snapshots, gate passes/fails
 */
const DEFAULT_DOMAINS = {
  audit: {
    name: 'audit',
    schema_version: 1,
    retention_days: 365,
    file_path: null, // resolved at build time
    max_file_size: 10 * 1024 * 1024, // 10 MB
  },

  integrity: {
    name: 'integrity',
    schema_version: 1,
    retention_days: 730,
    file_path: null,
    max_file_size: 5 * 1024 * 1024, // 5 MB
  },

  quality: {
    name: 'quality',
    schema_version: 1,
    retention_days: 180,
    file_path: null,
    max_file_size: 10 * 1024 * 1024, // 10 MB
  },
};

/**
 * Resolve file_path for each domain relative to a base directory.
 *
 * @param {string}  baseDir  - Absolute directory path where the event-store lives
 * @param {object}  [overrides] - Optional per-domain overrides (name → partial config)
 * @returns {DomainConfig[]} Array of fully-resolved domain configurations
 */
export function buildDomainConfigs(baseDir, overrides = {}) {
  // Ensure the base directory exists
  mkdirSync(baseDir, { recursive: true });

  /** @type {DomainConfig[]} */
  const configs = [];

  for (const [key, domain] of Object.entries(DEFAULT_DOMAINS)) {
    // Start from the default
    /** @type {DomainConfig} */
    const cfg = { ...domain };

    // Apply any user overrides for this domain
    if (overrides[key]) {
      Object.assign(cfg, overrides[key]);
    }

    // Resolve the file path if not explicitly provided in overrides
    if (!cfg.file_path) {
      cfg.file_path = resolve(baseDir, `${key}.jsonl`);
    }

    configs.push(cfg);
  }

  return configs;
}

/**
 * Retrieve the default domain definitions (unresolved).
 *
 * @returns {object} Map of domain key → partial DomainConfig
 */
export function getDomainDefaults() {
  return { ...DEFAULT_DOMAINS };
}