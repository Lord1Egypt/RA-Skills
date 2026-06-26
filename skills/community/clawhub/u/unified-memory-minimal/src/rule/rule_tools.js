import { z } from 'zod';
/**
 * Rule Memory Tools
 *
 * Tool wrappers for rule memory operations.
 */

import {
  loadRules,
  addRule,
  checkRule as storeCheckRule,
  deleteRule,
  recordViolation,
} from './rule_store.js';

/**
 * Add a new rule
 * @param {string} rule - rule text
 * @param {string} context - why this rule exists
 * @param {'explicit'|'implicit'} source
 * @returns {object} result
 */
export function memory_rule_add({ rule, context, source }) {
  try {
    const entry = addRule(rule, context, source);
    return { ok: true, rule: entry };
  } catch (err) {
    return { ok: false, error: err.message };
  }
}

/**
 * List all rules
 * @returns {object} result
 */
export function memory_rule_list() {
  try {
    const rules = loadRules();
    return { ok: true, rules, count: rules.length };
  } catch (err) {
    return { ok: false, error: err.message };
  }
}

/**
 * Check if an action violates any rules
 * @param {string} action
 * @returns {object} result with violations
 */
export function memory_rule_check({ action }) {
  try {
    return storeCheckRule(action);
  } catch (err) {
    return { ok: false, error: err.message };
  }
}

/**
 * Delete a rule by id
 * @param {string} id
 * @returns {object} result
 */
export function memory_rule_delete({ id }) {
  try {
    const deleted = deleteRule(id);
    return { ok: deleted, deleted: id };
  } catch (err) {
    return { ok: false, error: err.message };
  }
}

/**
 * Record that a rule was violated
 * @param {string} id
 */
export function memory_rule_violate({ id }) {
  try {
    recordViolation(id);
    return { ok: true };
  } catch (err) {
    return { ok: false, error: err.message };
  }
}

export function registerRuleTools(server) {
  server.registerTool('memory_rule_add', {
    description: 'Add a new rule memory (hard constraint or inviolable preference).',
    inputSchema: z.object({
      rule: z.string().describe('Rule text (what to enforce)'),
      context: z.string().optional().describe('Why this rule exists'),
      source: z.enum(['explicit', 'implicit']).optional().default('explicit').describe('How the rule was learned'),
    }),
  }, memory_rule_add);

  server.registerTool('memory_rule_list', {
    description: 'List all stored rule memories.',
    inputSchema: z.object({}),
  }, memory_rule_list);

  server.registerTool('memory_rule_check', {
    description: 'Check if an action or text violates any stored rules.',
    inputSchema: z.object({
      action: z.string().describe('Action or text to check against rules'),
    }),
  }, memory_rule_check);

  server.registerTool('memory_rule_delete', {
    description: 'Delete a rule memory by ID.',
    inputSchema: z.object({
      id: z.string().describe('Rule ID to delete'),
    }),
  }, memory_rule_delete);

  server.registerTool('memory_rule_violate', {
    description: 'Record that a rule was violated (for tracking and learning).',
    inputSchema: z.object({
      id: z.string().describe('Rule ID that was violated'),
    }),
  }, memory_rule_violate);
}
