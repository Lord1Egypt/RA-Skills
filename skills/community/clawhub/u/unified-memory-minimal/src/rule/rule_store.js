/**
 * Rule Store - Persistent storage for rule memories
 *
 * A rule memory stores hard constraints / user preferences as inviolable rules.
 * Distinct from procedural memories (how) or episodic memories (what happened).
 *
 * Storage: ~/.openclaw/workspace/memory/rules.json
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';
import crypto from 'crypto';
import { config } from '../config.js';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const RULES_FILE = join(config.memoryDir, 'rules.json');

// In-memory cache
let cache = null;

// ─── File I/O ────────────────────────────────────────────────────────────────

function ensureDir() {
  const dir = config.memoryDir;
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
}

function loadStore() {
  if (cache) return cache;
  ensureDir();
  if (!existsSync(RULES_FILE)) {
    cache = createEmptyStore();
    return cache;
  }
  try {
    const raw = JSON.parse(readFileSync(RULES_FILE, 'utf-8'));
    cache = {
      rules: Array.isArray(raw.rules) ? raw.rules : [],
      metadata: raw.metadata || { version: '1.0', lastUpdated: Date.now(), count: 0 },
    };
    return cache;
  } catch {
    cache = createEmptyStore();
    return cache;
  }
}

function createEmptyStore() {
  return {
    rules: [],
    metadata: { version: '1.0', lastUpdated: Date.now(), count: 0 },
  };
}

function saveStore(store) {
  ensureDir();
  store.metadata.lastUpdated = Date.now();
  store.metadata.count = store.rules.length;
  writeFileSync(RULES_FILE, JSON.stringify(store, null, 2), 'utf-8');
  cache = store;
}

// ─── Core CRUD ───────────────────────────────────────────────────────────────

/**
 * Load all rules from store
 * @returns {any[]}
 */
export function loadRules() {
  return loadStore().rules;
}

/**
 * Save the full rules array to store
 * @param {any[]} rules
 */
export function saveRules(rules) {
  const store = loadStore();
  store.rules = rules;
  saveStore(store);
}

/**
 * Add a new rule memory
 * @param {string} rule - the rule text
 * @param {string} context - why this rule exists
 * @param {'explicit'|'implicit'} source - how the rule was learned
 * @param {number} [confidence=0.95]
 * @returns {object} the created rule
 */
export function addRule(rule, context, source = 'explicit', confidence = 0.95) {
  const rules = loadRules();
  const id = 'rule_' + crypto.randomUUID().replace(/-/g, '').slice(0, 16);
  const now = new Date().toISOString();
  const entry = {
    id,
    rule,
    context: context || '',
    source: source === 'implicit' ? 'implicit' : 'explicit',
    confidence: Math.min(1, Math.max(0, confidence)),
    created_at: now,
    violation_count: 0,
  };
  rules.push(entry);
  saveRules(rules);
  return entry;
}

/**
 * Check an action/description against all rules
 * Returns a list of violated rules.
 * Handles negation prefixes (不要/不能/不可/不许/禁止) by extracting
 * the forbidden action pattern and checking if the input action matches it.
 *
 * @param {string} action - text describing the planned action
 * @returns {{ ok: boolean, violations: object[], checked: number }}
 */
export function checkRule(action) {
  const rules = loadRules();
  const violations = [];
  const actionLower = action.toLowerCase();

  for (const r of rules) {
    // Strip common negation prefixes to get the forbidden pattern
    // e.g. "不要在群里@刘总" → "在群里@刘总"
    const ruleText = r.rule
      .replace(/^(不要|不能|不可|不许|禁止|切勿|勿|不准|不可以|不该|不应该)\s*/i, '')
      .trim();

    // Split into keywords (min 3 chars for Chinese, 2+ for anything with special chars).
    // Use [...str] spread to correctly count multi-byte (Chinese) chars.
    const ruleKeywords = ruleText.split(/[\s,，、@#]+/).filter(w => {
      const chars = [...w];
      return chars.length >= 3 || w.includes('@') || w.includes('#') || w.includes('http');
    });
    const matched = ruleKeywords.some(kw => actionLower.includes(kw));
    if (matched) {
      violations.push(r);
    }
  }

  return {
    ok: violations.length === 0,
    violations,
    checked: rules.length,
  };
}

/**
 * Increment violation counter for a rule
 * @param {string} id
 */
export function recordViolation(id) {
  const rules = loadRules();
  const rule = rules.find(r => r.id === id);
  if (rule) {
    rule.violation_count = (rule.violation_count || 0) + 1;
    saveRules(rules);
  }
}

/**
 * Delete a rule by id
 * @param {string} id
 * @returns {boolean} true if deleted
 */
export function deleteRule(id) {
  const rules = loadRules();
  const idx = rules.findIndex(r => r.id === id);
  if (idx === -1) return false;
  rules.splice(idx, 1);
  saveRules(rules);
  return true;
}
