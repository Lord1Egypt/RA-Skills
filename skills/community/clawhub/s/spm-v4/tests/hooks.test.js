/**
 * Tests for the Hook middleware module (src/hooks/).
 *
 * Covers: register/unregister/run, event-type specific hooks,
 * context mutation, duplicate detection, error handling, listing,
 * clearing, and WBS context injection.
 *
 * @module tests/hooks.test
 */

import { describe, it, expect, beforeEach, afterEach, jest } from '@jest/globals';
import {
  register,
  unregister,
  run,
  list,
  clear,
} from '../src/hooks/index.js';
import {
  install,
  uninstall,
} from '../src/hooks/inject.js';

// ──────────────────────────────────────────────
// Hook Registry — register / unregister
// ──────────────────────────────────────────────

describe('Hook Registry', () => {
  beforeEach(() => {
    clear();
  });

  afterEach(() => {
    clear();
  });

  describe('register', () => {
    it('registers a hook handler for preToolUse (default)', () => {
      const handler = jest.fn();
      register('test-hook', handler);
      const all = list();
      expect(all.preToolUse).toContain('test-hook');
    });

    it('registers for postToolUse', () => {
      register('post-hook', jest.fn(), 'postToolUse');
      const all = list();
      expect(all.postToolUse).toContain('post-hook');
    });

    it('registers for onPhaseEnter', () => {
      register('enter-hook', jest.fn(), 'onPhaseEnter');
      const all = list();
      expect(all.onPhaseEnter).toContain('enter-hook');
    });

    it('registers for onPhaseExit', () => {
      register('exit-hook', jest.fn(), 'onPhaseExit');
      const all = list();
      expect(all.onPhaseExit).toContain('exit-hook');
    });

    it('throws for unknown event type', () => {
      expect(() => register('bad', jest.fn(), 'unknownEvent')).toThrow();
    });

    it('throws for duplicate hook name across event types', () => {
      register('unique-name', jest.fn(), 'preToolUse');
      expect(() => register('unique-name', jest.fn(), 'postToolUse')).toThrow();
    });

    it('allows same name for different handlers with different names', () => {
      register('hook-a', jest.fn(), 'preToolUse');
      register('hook-b', jest.fn(), 'preToolUse');
      const all = list();
      expect(all.preToolUse).toHaveLength(2);
    });
  });

  describe('unregister', () => {
    it('removes a registered hook by name', () => {
      register('remove-me', jest.fn(), 'preToolUse');
      unregister('remove-me');
      const all = list();
      expect(all.preToolUse).not.toContain('remove-me');
    });

    it('is a no-op for unknown name', () => {
      expect(() => unregister('not-there')).not.toThrow();
    });

    it('only removes the named hook, not others', () => {
      register('keep', jest.fn(), 'preToolUse');
      register('remove', jest.fn(), 'preToolUse');
      unregister('remove');
      const all = list();
      expect(all.preToolUse).toEqual(['keep']);
    });
  });

  // ────────────────────────────────────────────
  // Run
  // ────────────────────────────────────────────

  describe('run', () => {
    it('executes handlers in registration order', async () => {
      const order = [];
      register('first', async () => { order.push('first'); }, 'preToolUse');
      register('second', async () => { order.push('second'); }, 'preToolUse');

      await run('preToolUse', {});
      expect(order).toEqual(['first', 'second']);
    });

    it('passes context to each handler', async () => {
      const handler = jest.fn();
      register('ctx-test', handler, 'preToolUse');
      await run('preToolUse', { foo: 'bar' });
      expect(handler).toHaveBeenCalledWith({ foo: 'bar' });
    });

    it('handlers can mutate context', async () => {
      register('mutator', async (ctx) => {
        ctx.added = 'yes';
      }, 'preToolUse');

      const ctx = {};
      await run('preToolUse', ctx);
      expect(ctx.added).toBe('yes');
    });

    it('handler exceptions propagate up and abort the chain', async () => {
      const good = jest.fn();
      register('bad', async () => { throw new Error('oops'); }, 'preToolUse');
      register('good', good, 'preToolUse');

      await expect(run('preToolUse', {})).rejects.toThrow('oops');
      expect(good).not.toHaveBeenCalled();
    });

    it('no-ops when no hooks registered for event type', async () => {
      clear();
      await expect(run('preToolUse', {})).resolves.not.toThrow();
    });
  });

  // ────────────────────────────────────────────
  // List / Clear
  // ────────────────────────────────────────────

  describe('list', () => {
    it('returns empty object when no hooks registered', () => {
      clear();
      const all = list();
      expect(all.preToolUse).toEqual([]);
      expect(all.postToolUse).toEqual([]);
      expect(all.onPhaseEnter).toEqual([]);
      expect(all.onPhaseExit).toEqual([]);
    });

    it('lists hooks grouped by event type', () => {
      register('pre-a', jest.fn(), 'preToolUse');
      register('post-a', jest.fn(), 'postToolUse');
      register('enter-a', jest.fn(), 'onPhaseEnter');
      register('exit-a', jest.fn(), 'onPhaseExit');

      const all = list();
      expect(all.preToolUse).toEqual(['pre-a']);
      expect(all.postToolUse).toEqual(['post-a']);
      expect(all.onPhaseEnter).toEqual(['enter-a']);
      expect(all.onPhaseExit).toEqual(['exit-a']);
    });
  });

  describe('clear', () => {
    it('removes all hooks', () => {
      register('h1', jest.fn(), 'preToolUse');
      register('h2', jest.fn(), 'postToolUse');
      clear();
      const all = list();
      expect(all.preToolUse).toHaveLength(0);
      expect(all.postToolUse).toHaveLength(0);
    });
  });
});

// ──────────────────────────────────────────────
// WBS Context Injection (hooks/inject.js)
// ──────────────────────────────────────────────

describe('WBS Context Injection', () => {
  beforeEach(() => {
    clear();
  });

  afterEach(() => {
    uninstall();
    clear();
  });

  it('install registers the wbs-context-inject hook', () => {
    install({
      reader: async () => ({
        ledgerPath: 'docs/spm/ledger.md',
        activeTask: 'WB-001',
        completed: ['WB-000'],
        pending: ['WB-002'],
      }),
    });
    const all = list();
    expect(all.preToolUse).toContain('wbs-context-inject');
  });

  it('injects wbsContext into context on preToolUse', async () => {
    install({
      reader: async () => ({
        ledgerPath: 'docs/spm/ledger.md',
        activeTask: 'WB-001',
        completed: ['WB-000'],
        pending: ['WB-002'],
      }),
    });

    const ctx = {};
    await run('preToolUse', ctx);

    expect(ctx.wbsContext).toBeDefined();
    expect(ctx.wbsContext).toContain('SPM WBS Context');
    expect(ctx.wbsContext).toContain('WB-001');
    expect(ctx.wbsContext).toContain('docs/spm/ledger.md');
  });

  it('uninstall removes the hook', () => {
    install({ reader: async () => ({ ledgerPath: 'x' }) });
    uninstall();
    const all = list();
    expect(all.preToolUse).not.toContain('wbs-context-inject');
  });

  it('handles empty WBS state gracefully', async () => {
    install({
      reader: async () => ({
        ledgerPath: 'docs/spm/ledger.md',
      }),
    });

    const ctx = {};
    await run('preToolUse', ctx);
    expect(ctx.wbsContext).toBeDefined();
    expect(ctx.wbsContext).toContain('SPM WBS Context');
  });

  it('respects maxChars limit', async () => {
    install({
      maxChars: 50,
      reader: async () => ({
        ledgerPath: 'x.md',
        activeTask: 'A very long task description that should be truncated',
      }),
    });

    const ctx = {};
    await run('preToolUse', ctx);
    expect(ctx.wbsContext.length).toBeLessThanOrEqual(53); // 50 + '…'
  });
});