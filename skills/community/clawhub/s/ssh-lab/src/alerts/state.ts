import { readFileSync, writeFileSync, renameSync, existsSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import type { AlertRule } from '../types/index.js';

const STATE_DIR = join(process.env['HOME'] ?? '/tmp', '.ssh-lab');
const RULES_PATH = join(STATE_DIR, 'alerts.json');

function ensureDir(): void {
  if (!existsSync(STATE_DIR)) {
    mkdirSync(STATE_DIR, { recursive: true, mode: 0o700 });
  }
}

/**
 * Load alert rules from disk. Returns empty array if no file.
 */
export function loadRules(): AlertRule[] {
  if (!existsSync(RULES_PATH)) return [];
  try {
    const raw = readFileSync(RULES_PATH, 'utf-8');
    return JSON.parse(raw) as AlertRule[];
  } catch {
    return [];
  }
}

/**
 * Save alert rules to disk (atomic write: temp → rename).
 */
export function saveRules(rules: AlertRule[]): void {
  ensureDir();
  const tmp = RULES_PATH + '.tmp';
  writeFileSync(tmp, JSON.stringify(rules, null, 2), 'utf-8');
  renameSync(tmp, RULES_PATH);
}

/**
 * Add a rule. Returns the rule with generated id.
 */
export function addRule(rule: Omit<AlertRule, 'id' | 'createdAt' | 'enabled'>): AlertRule {
  const rules = loadRules();
  const newRule: AlertRule = {
    ...rule,
    id: `rule_${Date.now().toString(36)}_${Math.random().toString(36).slice(2, 6)}`,
    enabled: true,
    createdAt: new Date().toISOString(),
  };
  rules.push(newRule);
  saveRules(rules);
  return newRule;
}

/**
 * Remove a rule by id.
 */
export function removeRule(ruleId: string): boolean {
  const rules = loadRules();
  const idx = rules.findIndex(r => r.id === ruleId);
  if (idx === -1) return false;
  rules.splice(idx, 1);
  saveRules(rules);
  return true;
}

/**
 * Get rules applicable to a specific host (rules targeting the host + 'all' rules).
 */
export function rulesForHost(host: string): AlertRule[] {
  return loadRules().filter(r => r.enabled && (r.host === host || r.host === 'all'));
}
