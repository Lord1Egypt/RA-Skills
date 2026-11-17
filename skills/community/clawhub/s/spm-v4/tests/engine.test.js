/**
 * Tests for the Engine state machine (src/engine/).
 *
 * Covers: phase transitions, event hooks, error states, context
 * management, history, precondition guards, and the full phase lifecycle.
 *
 * @module tests/engine.test
 */

import { describe, it, expect, beforeEach, jest } from '@jest/globals';
import { Engine, EngineError } from '../src/engine/index.js';
import {
  buildPhaseDefinitions,
  PHASE_INDEX,
  PHASE_NAMES,
  isTransitionAllowed,
  getDefaultTransitions,
} from '../src/engine/phases.js';
import {
  Workflow,
  registerWorkflow,
  getWorkflow,
  listWorkflows,
  unregisterWorkflow,
  clearWorkflowRegistry,
} from '../src/engine/workflow.js';
import {
  ENGINE_CONTEXT_REQUIREMENT,
  ENGINE_FULL_CONTEXT,
} from './setup.js';

// ──────────────────────────────────────────────
// Engine — Construction & Initialization
// ──────────────────────────────────────────────

describe('Engine', () => {
  let engine;

  beforeEach(() => {
    engine = new Engine(ENGINE_FULL_CONTEXT);
  });

  describe('construction', () => {
    it('starts in context-init phase', () => {
      const phase = engine.currentPhase();
      expect(phase.name).toBe('context-init');
      expect(phase.index).toBe(0);
    });

    it('throws if config has no phases object (edge: undefined)', () => {
      // Engine handles missing config gracefully
      const e = new Engine();
      expect(e.currentPhase().name).toBe('context-init');
    });

    it('accepts custom phase overrides', () => {
      const customPre = jest.fn(() => true);
      const customPost = jest.fn();
      const e = new Engine({
        phases: {
          execution: { pre: customPre, post: customPost },
        },
        context: ENGINE_FULL_CONTEXT,
      });
      e.phase('execution');
      expect(customPre).toHaveBeenCalled();
      expect(customPost).toHaveBeenCalled();
    });

    it('initialises context from config', () => {
      const e = new Engine({
        context: { projectName: 'hello', goal: 'world' },
      });
      expect(e.getContext()).toMatchObject({ projectName: 'hello', goal: 'world' });
    });

    it('records context-init in history on construction', () => {
      const history = engine.getHistory();
      expect(history).toHaveLength(1);
      expect(history[0].phase).toBe('context-init');
    });
  });

  // ────────────────────────────────────────────
  // Phase entry & precondition guards
  // ────────────────────────────────────────────

  describe('phase entry', () => {
    it('enters requirement phase with valid context', () => {
      const p = engine.phase('requirement', {
        projectName: 'p1',
        goal: 'g1',
      });
      expect(p.name).toBe('requirement');
      expect(p.index).toBe(1);
    });

    it('throws EngineError when entering unknown phase', () => {
      expect(() => engine.phase('nonexistent')).toThrow(EngineError);
    });

    it('throws EngineError when precondition fails', () => {
      // requirement requires projectName and goal
      expect(() => engine.phase('requirement')).toThrow(EngineError);
    });

    it('emits "enter" event on successful phase entry', () => {
      const handler = jest.fn();
      engine.on('enter', handler);
      engine.phase('requirement', ENGINE_CONTEXT_REQUIREMENT);
      expect(handler).toHaveBeenCalledTimes(1);
      expect(handler.mock.calls[0][0].phase).toBe('requirement');
    });

    it('emits "error" event on precondition failure', () => {
      const handler = jest.fn();
      engine.on('error', handler);
      try { engine.phase('requirement'); } catch { /* expected */ }
      expect(handler).toHaveBeenCalledTimes(1);
      expect(handler.mock.calls[0][0].error).toBeInstanceOf(EngineError);
    });

    it('merges context on phase entry', () => {
      engine.phase('requirement', ENGINE_CONTEXT_REQUIREMENT);
      expect(engine.getContext()).toMatchObject(ENGINE_CONTEXT_REQUIREMENT);
    });

    it('appends to history on each phase entry', () => {
      engine.phase('requirement', ENGINE_CONTEXT_REQUIREMENT);
      expect(engine.getHistory()).toHaveLength(2);
      expect(engine.getHistory()[1].phase).toBe('requirement');
    });

    it('calls post-condition hook on entry', () => {
      const post = jest.fn();
      const e = new Engine({
        phases: { requirement: { post } },
        context: ENGINE_CONTEXT_REQUIREMENT,
      });
      e.phase('requirement');
      expect(post).toHaveBeenCalled();
    });
  });

  // ────────────────────────────────────────────
  // Transitions
  // ────────────────────────────────────────────

  describe('transitions', () => {
    function fullPhaseEngine() {
      const e = new Engine({ context: { ...ENGINE_FULL_CONTEXT } });
      return e;
    }

    it('allows context-init → requirement', () => {
      const e = fullPhaseEngine();
      const p = e.transition('requirement');
      expect(p.name).toBe('requirement');
    });

    it('throws EngineError on invalid transition', () => {
      const e = fullPhaseEngine();
      e.transition('requirement'); // now in requirement
      // requirement → delivery is NOT allowed
      expect(() => e.transition('delivery')).toThrow(EngineError);
    });

    it('throws when target phase is unknown', () => {
      const e = fullPhaseEngine();
      expect(() => e.transition('moon-phase')).toThrow(EngineError);
    });

    it('emits "transition" event (closest is enter)', () => {
      const handler = jest.fn();
      const e = fullPhaseEngine();
      e.on('enter', handler);
      e.transition('requirement');
      // transition calls phase() internally which emits 'enter'
      expect(handler).toHaveBeenCalled();
    });

    it('transitions through the full lifecycle', () => {
      const e = fullPhaseEngine();
      expect(e.transition('requirement').name).toBe('requirement');
      expect(e.transition('planning').name).toBe('planning');
      expect(e.transition('execution').name).toBe('execution');
      expect(e.transition('quality').name).toBe('quality');
      expect(e.transition('delivery').name).toBe('delivery');
    });

    it('supports limited backtrack from quality → planning', () => {
      const e = fullPhaseEngine();
      e.transition('requirement');
      e.transition('planning');
      e.transition('execution');
      e.transition('quality');
      expect(e.transition('planning').name).toBe('planning');
    });

    it('supports revision cycle: delivery → quality', () => {
      const e = fullPhaseEngine();
      e.transition('requirement');
      e.transition('planning');
      e.transition('execution');
      e.transition('quality');
      e.transition('delivery');
      expect(e.transition('quality').name).toBe('quality');
    });

    it('merges context during transition', () => {
      const e = fullPhaseEngine();
      e.transition('requirement', { extra: 'value' });
      expect(e.getContext().extra).toBe('value');
    });
  });

  // ────────────────────────────────────────────
  // Event listeners (on/off/emit)
  // ────────────────────────────────────────────

  describe('event listeners', () => {
    it('registers and fires on "enter"', () => {
      const handler = jest.fn();
      engine.on('enter', handler);
      engine.phase('requirement', ENGINE_CONTEXT_REQUIREMENT);
      expect(handler).toHaveBeenCalled();
    });

    it('registers and fires on "error"', () => {
      const handler = jest.fn();
      engine.on('error', handler);
      try { engine.phase('nope'); } catch { /* */ }
      expect(handler).toHaveBeenCalled();
    });

    it('removes listener with off()', () => {
      const handler = jest.fn();
      engine.on('enter', handler);
      engine.off('enter', handler);
      engine.phase('requirement', ENGINE_CONTEXT_REQUIREMENT);
      expect(handler).not.toHaveBeenCalled();
    });

    it('swallows handler exceptions without affecting other handlers', () => {
      const badHandler = jest.fn(() => { throw new Error('boom'); });
      const goodHandler = jest.fn();
      engine.on('enter', badHandler);
      engine.on('enter', goodHandler);
      expect(() => {
        engine.phase('requirement', ENGINE_CONTEXT_REQUIREMENT);
      }).not.toThrow();
      expect(goodHandler).toHaveBeenCalled();
    });

    it('off() on unregistered event is safe (no-op)', () => {
      expect(() => engine.off('enter', jest.fn())).not.toThrow();
    });
  });

  // ────────────────────────────────────────────
  // Context management
  // ────────────────────────────────────────────

  describe('context management', () => {
    it('updateContext merges data', () => {
      engine.updateContext({ foo: 'bar' });
      expect(engine.getContext().foo).toBe('bar');
    });

    it('updateContext does not clear existing context', () => {
      engine.updateContext({ foo: 'bar' });
      engine.updateContext({ baz: 'qux' });
      expect(engine.getContext().foo).toBe('bar');
      expect(engine.getContext().baz).toBe('qux');
    });

    it('getContext returns a shallow copy', () => {
      const ctx = engine.getContext();
      ctx.tamper = 'yup';
      expect(engine.getContext().tamper).toBeUndefined();
    });
  });

  // ────────────────────────────────────────────
  // Query helpers
  // ────────────────────────────────────────────

  describe('query helpers', () => {
    it('isInPhase returns true for current phase', () => {
      expect(engine.isInPhase('context-init')).toBe(true);
      expect(engine.isInPhase('requirement')).toBe(false);
    });

    it('allowedTransitions returns valid targets', () => {
      const allowed = engine.allowedTransitions();
      expect(allowed).toEqual(['requirement']);
    });

    it('allowedTransitions changes after phase change', () => {
      const e = new Engine({ context: ENGINE_FULL_CONTEXT });
      e.transition('requirement');
      const allowed = e.allowedTransitions();
      expect(allowed).toContain('planning');
      expect(allowed).toContain('context-init');
    });
  });

  // ────────────────────────────────────────────
  // History
  // ────────────────────────────────────────────

  describe('history', () => {
    it('getHistory returns a copy of history entries', () => {
      const hist = engine.getHistory();
      hist.push({ phase: 'tampered', enteredAt: 0, context: {} });
      expect(engine.getHistory()).toHaveLength(1);
    });

    it('each history entry has phase, enteredAt, and context', () => {
      engine.phase('requirement', ENGINE_CONTEXT_REQUIREMENT);
      const entry = engine.getHistory()[1];
      expect(entry).toHaveProperty('phase', 'requirement');
      expect(entry).toHaveProperty('enteredAt');
      expect(typeof entry.enteredAt).toBe('number');
      expect(entry).toHaveProperty('context');
    });
  });
});

// ──────────────────────────────────────────────
// Phase Definitions
// ──────────────────────────────────────────────

describe('buildPhaseDefinitions', () => {
  it('returns definitions for all 6 phases', () => {
    const defs = buildPhaseDefinitions();
    expect(Object.keys(defs)).toHaveLength(6);
    expect(defs['context-init'].index).toBe(0);
    expect(defs.delivery.index).toBe(5);
  });

  it('allows overriding transitions', () => {
    const defs = buildPhaseDefinitions({
      execution: { transitions: ['delivery'] },
    });
    expect(defs.execution.transitions).toEqual(['delivery']);
  });

  it('allows overriding pre/post conditions', () => {
    const pre = () => false;
    const defs = buildPhaseDefinitions({
      delivery: { pre },
    });
    expect(defs.delivery.pre).toBe(pre);
  });

  it('freezes transitions array', () => {
    const defs = buildPhaseDefinitions();
    expect(Object.isFrozen(defs['context-init'].transitions)).toBe(true);
  });
});

describe('PHASE_INDEX and PHASE_NAMES', () => {
  it('maps names to indices correctly', () => {
    expect(PHASE_INDEX['context-init']).toBe(0);
    expect(PHASE_INDEX.requirement).toBe(1);
    expect(PHASE_INDEX.planning).toBe(2);
    expect(PHASE_INDEX.execution).toBe(3);
    expect(PHASE_INDEX.quality).toBe(4);
    expect(PHASE_INDEX.delivery).toBe(5);
  });

  it('PHASE_NAMES maps indices to names', () => {
    expect(PHASE_NAMES[0]).toBe('context-init');
    expect(PHASE_NAMES[5]).toBe('delivery');
  });
});

describe('isTransitionAllowed', () => {
  it('returns true for valid transition', () => {
    const from = { name: 'planning', transitions: ['execution', 'requirement'] };
    const to = { name: 'execution' };
    expect(isTransitionAllowed(from, to)).toBe(true);
  });

  it('returns false for invalid transition', () => {
    const from = { name: 'planning', transitions: ['execution', 'requirement'] };
    const to = { name: 'delivery' };
    expect(isTransitionAllowed(from, to)).toBe(false);
  });
});

describe('getDefaultTransitions', () => {
  it('returns a deep clone', () => {
    const t1 = getDefaultTransitions();
    const t2 = getDefaultTransitions();
    expect(t1).toEqual(t2);
    // mutation shouldn't affect subsequent calls
    t1.planning = [];
    expect(getDefaultTransitions().planning).toEqual(['execution', 'requirement']);
  });
});

// ──────────────────────────────────────────────
// Workflow
// ──────────────────────────────────────────────

describe('Workflow', () => {
  beforeEach(() => {
    clearWorkflowRegistry();
  });

  const simpleDef = {
    id: 'test-workflow',
    description: 'A simple test workflow',
    phases: [
      { name: 'requirement' },
      { name: 'planning' },
    ],
  };

  describe('construction and validation', () => {
    it('creates a Workflow from a valid definition', () => {
      const wf = new Workflow(simpleDef);
      expect(wf.id).toBe('test-workflow');
      expect(wf.description).toBe('A simple test workflow');
      expect(wf.phases).toHaveLength(2);
    });

    it('throws on null definition', () => {
      expect(() => new Workflow(null)).toThrow(EngineError);
    });

    it('throws on empty id', () => {
      expect(() => new Workflow({ id: '', phases: [] })).toThrow(EngineError);
    });

    it('throws on empty phases', () => {
      expect(() => new Workflow({ id: 'x', phases: [] })).toThrow(EngineError);
    });

    it('throws on phase without string name', () => {
      expect(() => new Workflow({ id: 'x', phases: [{ name: 42 }] })).toThrow(EngineError);
    });

    it('is not complete initially', () => {
      const wf = new Workflow(simpleDef);
      expect(wf.isComplete).toBe(false);
      expect(wf.currentStep).toBe(0);
    });
  });

  describe('execution', () => {
    it('start calls engine.phase for the first step', () => {
      const engine = new Engine({ context: ENGINE_FULL_CONTEXT });
      const wf = new Workflow({
        id: 'exec-test',
        phases: [{ name: 'requirement' }],
      });

      wf.start(engine, ENGINE_CONTEXT_REQUIREMENT);
      expect(engine.isInPhase('requirement')).toBe(true);
    });

    it('next advances to the next phase', async () => {
      const engine = new Engine({ context: ENGINE_FULL_CONTEXT });
      const wf = new Workflow(simpleDef);
      await wf.start(engine, ENGINE_CONTEXT_REQUIREMENT);
      expect(engine.isInPhase('requirement')).toBe(true);

      await wf.next({ ...ENGINE_FULL_CONTEXT, plan: { steps: ['x'] } });
      expect(engine.isInPhase('planning')).toBe(true);
    });

    it('next returns false when workflow is complete', async () => {
      const engine = new Engine({ context: ENGINE_FULL_CONTEXT });
      const wf = new Workflow({
        id: 'one-step',
        phases: [{ name: 'requirement' }],
      });
      await wf.start(engine, ENGINE_CONTEXT_REQUIREMENT);
      const result = await wf.next();
      expect(result).toBe(false);
      expect(wf.isComplete).toBe(true);
    });

    it('run executes all phases', async () => {
      const engine = new Engine({ context: ENGINE_FULL_CONTEXT });
      const wf = new Workflow({
        id: 'run-test',
        phases: [
          { name: 'requirement' },
          { name: 'planning' },
          { name: 'execution' },
        ],
      });
      await wf.run(engine, ENGINE_CONTEXT_REQUIREMENT);
      expect(wf.isComplete).toBe(true);
      expect(engine.isInPhase('execution')).toBe(true);
    });

    it('throws if start called twice', async () => {
      const engine = new Engine({ context: ENGINE_FULL_CONTEXT });
      const wf = new Workflow(simpleDef);
      await wf.start(engine, ENGINE_CONTEXT_REQUIREMENT);
      await expect(wf.start(engine)).rejects.toThrow(EngineError);
    });

    it('throws if next called before start', async () => {
      const wf = new Workflow(simpleDef);
      await expect(wf.next()).rejects.toThrow(EngineError);
    });

    it('start throws on non-Engine argument', async () => {
      const wf = new Workflow(simpleDef);
      await expect(wf.start({})).rejects.toThrow(EngineError);
    });
  });

  describe('triggers and conditions', () => {
    it('calls trigger handlers on phase enter', async () => {
      const handler = jest.fn();
      const engine = new Engine({ context: ENGINE_FULL_CONTEXT });
      const wf = new Workflow({
        id: 'trigger-test',
        phases: [{ name: 'requirement' }],
        triggers: [
          { event: 'enter', hook: 'enter', handler },
        ],
      });
      await wf.start(engine, ENGINE_CONTEXT_REQUIREMENT);
      expect(handler).toHaveBeenCalled();
    });

    it('evaluates function-valued conditions via triggers', async () => {
      const condition = jest.fn(() => true);
      const engine = new Engine({ context: ENGINE_FULL_CONTEXT });
      const wf = new Workflow({
        id: 'cond-test',
        phases: [{ name: 'requirement' }],
        triggers: [{ event: 'enter', hook: 'enter' }],
        conditions: { myCondition: condition },
      });
      await wf.start(engine, ENGINE_CONTEXT_REQUIREMENT);
      expect(condition).toHaveBeenCalled();
    });
  });

  describe('registry', () => {
    it('registerWorkflow and getWorkflow', () => {
      const wf = registerWorkflow(simpleDef);
      expect(getWorkflow('test-workflow')).toBe(wf);
    });

    it('registerWorkflow throws on duplicate id', () => {
      registerWorkflow(simpleDef);
      expect(() => registerWorkflow(simpleDef)).toThrow(EngineError);
    });

    it('listWorkflows returns registered workflows', () => {
      registerWorkflow(simpleDef);
      const list = listWorkflows();
      expect(list).toHaveLength(1);
      expect(list[0].id).toBe('test-workflow');
    });

    it('unregisterWorkflow removes from registry', () => {
      registerWorkflow(simpleDef);
      expect(unregisterWorkflow('test-workflow')).toBe(true);
      expect(getWorkflow('test-workflow')).toBeUndefined();
    });

    it('unregisterWorkflow returns false for unknown id', () => {
      expect(unregisterWorkflow('nope')).toBe(false);
    });

    it('clearWorkflowRegistry empties all workflows', () => {
      registerWorkflow(simpleDef);
      registerWorkflow({ id: 'wf2', phases: [{ name: 'requirement' }] });
      clearWorkflowRegistry();
      expect(listWorkflows()).toHaveLength(0);
    });
  });

  describe('serialization', () => {
    it('serialize returns a plain object snapshot', () => {
      const wf = new Workflow(simpleDef);
      const s = wf.serialize();
      expect(s.id).toBe('test-workflow');
      expect(s.currentStep).toBe(0);
      expect(s.isComplete).toBe(false);
      expect(s.phases).toHaveLength(2);
      // handler should be stripped from triggers
      expect(s.triggers).toBeDefined();
    });

    it('fromDefinition convenience', () => {
      const wf = Workflow.fromDefinition(simpleDef);
      expect(wf).toBeInstanceOf(Workflow);
      expect(wf.id).toBe('test-workflow');
    });
  });
});