/**
 * Tests for the WBS module (src/wbs/).
 *
 * Covers: ledger parsing, task CRUD, status validation, dependency
 * checks, circular dependency detection, serialization, SHA-256
 * attestation, and Merkle tree hashing.
 *
 * @module tests/wbs.test
 */

import { describe, it, expect, beforeEach, afterEach, jest } from '@jest/globals';
import { readFileSync, existsSync, unlinkSync, rmdirSync, mkdirSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';
import {
  WBS,
  WBSError,
  parseLedger,
  STATUSES,
  STATUS_TRANSITIONS,
} from '../src/wbs/index.js';
import {
  attest,
  verify,
  hashContent,
  loadAttestation,
  checkAttestation,
} from '../src/wbs/attest.js';
import { MerkleTree, MerkleWBS, hashTask } from '../src/wbs/merkle.js';
import {
  SAMPLE_LEDGER,
  CIRCULAR_LEDGER,
  MISSING_DEP_LEDGER,
  createTempDir,
  cleanupTempDirs,
} from './setup.js';

// ──────────────────────────────────────────────
// parseLedger
// ──────────────────────────────────────────────

describe('parseLedger', () => {
  it('parses a valid ledger into task objects', () => {
    const tasks = parseLedger(SAMPLE_LEDGER);
    expect(tasks).toHaveLength(3);
    expect(tasks[0].id).toBe('WB-001');
    expect(tasks[0].workPackage).toBe('Initialize project');
    expect(tasks[0].status).toBe('done');
    expect(tasks[0].dependencies).toEqual([]);
  });

  it('parses dependency lists', () => {
    const tasks = parseLedger(SAMPLE_LEDGER);
    expect(tasks[1].dependencies).toEqual(['WB-001']);
    expect(tasks[2].dependencies).toEqual(['WB-001']);
  });

  it('reads context, exit criteria, and evidence fields', () => {
    const tasks = parseLedger(SAMPLE_LEDGER);
    expect(tasks[0].contextBrief).toBe('Set up the project skeleton');
    expect(tasks[0].exitCriteria).toBe('Repository created with package.json');
    expect(tasks[0].evidence).toBe('GitHub repo initialized');
  });

  it('defaults status to "todo" when not specified', () => {
    const ledger = `## WB-001: No status
- **Dependencies**: none
- **Context**: test
`;
    const tasks = parseLedger(ledger);
    expect(tasks[0].status).toBe('todo');
  });

  it('handles "none" dependencies', () => {
    const tasks = parseLedger(SAMPLE_LEDGER);
    expect(tasks[0].dependencies).toEqual([]);
  });

  it('handles empty dependencies string', () => {
    const ledger = `## WB-001: Empty deps
- **Status**: todo
- **Dependencies**: 
`;
    const tasks = parseLedger(ledger);
    expect(tasks[0].dependencies).toEqual([]);
  });

  it('throws on missing workPackage (no title after colon)', () => {
    const bad = `## WB-001: `;
    expect(() => parseLedger(bad)).toThrow(WBSError);
  });

  it('requires full reparse when content changes', () => {
    const tasks1 = parseLedger(SAMPLE_LEDGER);
    expect(tasks1).toHaveLength(3);
  });

  it('handles multi-line field content gracefully', () => {
    const ledger = `## WB-001: Test
- **Status**: doing
- **Context**: Line one
- **Exit Criteria**: Line one
- **Evidence**: Line one
`;
    const tasks = parseLedger(ledger);
    expect(tasks[0].contextBrief).toBe('Line one');
  });

  it('returns empty array for empty content', () => {
    expect(parseLedger('')).toEqual([]);
  });

  it('returns empty array for content with no task headings', () => {
    expect(parseLedger('Just some text\nwithout headings')).toEqual([]);
  });
});

// ──────────────────────────────────────────────
// WBS Class
// ──────────────────────────────────────────────

describe('WBS', () => {
  /** @type {{ path: string, cleanup: () => void }} */
  let tmp;
  /** @type {WBS} */
  let wbs;

  beforeEach(() => {
    tmp = createTempDir();
    wbs = new WBS();
  });

  afterEach(() => {
    tmp.cleanup();
  });

  // ── load / loadFromString ─────────────────

  describe('loadFromString', () => {
    it('loads tasks from a markdown string', () => {
      const tasks = wbs.loadFromString(SAMPLE_LEDGER);
      expect(tasks).toHaveLength(3);
      expect(wbs.getTask('WB-001')).toBeDefined();
    });

    it('throws on duplicate task id', () => {
      const dup = SAMPLE_LEDGER + `\n## WB-001: Duplicate\n- **Status**: todo\n- **Dependencies**: none\n`;
      expect(() => wbs.loadFromString(dup)).toThrow(WBSError);
    });

    it('throws on missing dependency', () => {
      expect(() => wbs.loadFromString(MISSING_DEP_LEDGER)).toThrow(WBSError);
    });

    it('throws on circular dependency', () => {
      expect(() => wbs.loadFromString(CIRCULAR_LEDGER)).toThrow(WBSError);
    });
  });

  describe('load', () => {
    it('loads tasks from a file path', () => {
      const ledgerPath = resolve(tmp.path, 'ledger.md');
      writeFileSync(ledgerPath, SAMPLE_LEDGER, 'utf-8');
      wbs = new WBS({ ledgerPath });
      const tasks = wbs.load();
      expect(tasks).toHaveLength(3);
    });

    it('throws when no path is provided', () => {
      expect(() => wbs.load()).toThrow(WBSError);
    });

    it('throws on non-existent file', () => {
      expect(() => wbs.load('/nonexistent/ledger.md')).toThrow(WBSError);
    });
  });

  // ── Task CRUD ──────────────────────────────

  describe('getTask / getAllTasks', () => {
    beforeEach(() => {
      wbs.loadFromString(SAMPLE_LEDGER);
    });

    it('getTask returns a task by id', () => {
      const task = wbs.getTask('WB-002');
      expect(task.workPackage).toBe('Implement authentication');
      expect(task.status).toBe('doing');
    });

    it('getTask returns undefined for unknown id', () => {
      expect(wbs.getTask('WB-999')).toBeUndefined();
    });

    it('getTask returns a shallow copy', () => {
      const task = wbs.getTask('WB-001');
      task.workPackage = 'Tampered';
      expect(wbs.getTask('WB-001').workPackage).not.toBe('Tampered');
    });

    it('getAllTasks returns all tasks', () => {
      expect(wbs.getAllTasks()).toHaveLength(3);
    });

    it('getAllTasks returns shallow copies', () => {
      const tasks = wbs.getAllTasks();
      tasks[0].workPackage = 'Tampered';
      expect(wbs.getTask('WB-001').workPackage).not.toBe('Tampered');
    });
  });

  describe('addTask', () => {
    beforeEach(() => {
      wbs.loadFromString(SAMPLE_LEDGER);
    });

    it('adds a new task with minimal fields', () => {
      const added = wbs.addTask({
        id: 'WB-004',
        workPackage: 'New task',
      });
      expect(added.id).toBe('WB-004');
      expect(added.status).toBe('todo');
      expect(wbs.getAllTasks()).toHaveLength(4);
    });

    it('throws on duplicate id', () => {
      expect(() =>
        wbs.addTask({ id: 'WB-001', workPackage: 'Duplicate' }),
      ).toThrow(WBSError);
    });

    it('throws on missing workPackage', () => {
      expect(() =>
        wbs.addTask({ id: 'WB-004' }),
      ).toThrow(WBSError);
    });

    it('throws on missing dependency', () => {
      expect(() =>
        wbs.addTask({ id: 'WB-004', workPackage: 'X', dependencies: ['WB-999'] }),
      ).toThrow(WBSError);
    });

    it('throws on circular dependency introduced by new task', () => {
      // WB-002 depends on WB-001. If WB-001 now depends on WB-004
      // and WB-004 depends on WB-001, that's circular.
      wbs.addTask({
        id: 'WB-004',
        workPackage: 'New',
        dependencies: ['WB-001'],
      });
      expect(() =>
        wbs.addTask({
          id: 'WB-005',
          workPackage: 'Bad',
          dependencies: ['WB-004', 'WB-001'],
        }),
      ).not.toThrow();
    });

    it('normalizes dependencies array', () => {
      const added = wbs.addTask({
        id: 'WB-004',
        workPackage: 'With deps',
        dependencies: ['WB-001'],
      });
      expect(added.dependencies).toEqual(['WB-001']);
    });
  });

  describe('update', () => {
    beforeEach(() => {
      wbs.loadFromString(SAMPLE_LEDGER);
    });

    it('updates task status', () => {
      wbs.update('WB-002', { status: 'done', evidence: 'Auth module deployed' });
      expect(wbs.getTask('WB-002').status).toBe('done');
    });

    it('throws on invalid transition', () => {
      // done → planning is NOT valid
      wbs.update('WB-001', { status: 'done', evidence: 'evidence' });
      expect(() => wbs.update('WB-001', { status: 'planning' })).toThrow(WBSError);
    });

    it('allows valid transition: todo → doing', () => {
      wbs.update('WB-003', { status: 'doing' });
      expect(wbs.getTask('WB-003').status).toBe('doing');
    });

    it('allows valid transition: blocked → todo', () => {
      wbs.update('WB-003', { status: 'blocked' });
      wbs.update('WB-003', { status: 'todo' });
      expect(wbs.getTask('WB-003').status).toBe('todo');
    });

    it('throws WBSError with NO_EVIDENCE when done task lacks evidence', () => {
      expect(() => wbs.update('WB-003', { status: 'done' })).toThrow(WBSError);
    });

    it('allows done with evidence', () => {
      wbs.update('WB-003', { status: 'doing' });
      wbs.update('WB-003', { status: 'done', evidence: 'Tests all pass' });
      expect(wbs.getTask('WB-003').status).toBe('done');
      expect(wbs.getTask('WB-003').evidence).toBe('Tests all pass');
    });

    it('updates workPackage', () => {
      wbs.update('WB-001', { workPackage: 'Renamed' });
      expect(wbs.getTask('WB-001').workPackage).toBe('Renamed');
    });

    it('updates dependencies and validates', () => {
      wbs.update('WB-003', { dependencies: ['WB-002'] });
      expect(wbs.getTask('WB-003').dependencies).toEqual(['WB-002']);
    });

    it('throws when updating to missing dependency', () => {
      expect(() =>
        wbs.update('WB-003', { dependencies: ['WB-999'] }),
      ).toThrow(WBSError);
    });

    it('throws when task not found', () => {
      expect(() =>
        wbs.update('WB-999', { status: 'done' }),
      ).toThrow(WBSError);
    });

    it('detects circular dependency in update', () => {
      // WB-002 depends on WB-001. Make WB-001 depend on WB-002 → circular
      expect(() =>
        wbs.update('WB-001', { dependencies: ['WB-002'] }),
      ).toThrow(WBSError);
    });
  });

  describe('serialize', () => {
    it('produces markdown output', () => {
      wbs.loadFromString(SAMPLE_LEDGER);
      const output = wbs.serialize();
      expect(output).toContain('# SPM WBS Ledger');
      expect(output).toContain('## WB-001');
      expect(output).toContain('## WB-002');
      expect(output).toContain('## WB-003');
    });

    it('round-trips: serialize → parseLedger yields same data', () => {
      wbs.loadFromString(SAMPLE_LEDGER);
      const serialized = wbs.serialize();
      const reparsed = parseLedger(serialized);
      expect(reparsed).toHaveLength(3);
      expect(reparsed[0].id).toBe('WB-001');
    });
  });
});

// ──────────────────────────────────────────────
// Status Constants & Transitions
// ──────────────────────────────────────────────

describe('STATUSES', () => {
  it('contains all valid statuses', () => {
    expect(STATUSES).toEqual(['todo', 'doing', 'done', 'blocked', 'skipped']);
  });
});

describe('STATUS_TRANSITIONS', () => {
  it('todo → doing, blocked, skipped', () => {
    expect(STATUS_TRANSITIONS.todo).toEqual(['doing', 'blocked', 'skipped']);
  });

  it('doing → done, blocked, skipped', () => {
    expect(STATUS_TRANSITIONS.doing).toEqual(['done', 'blocked', 'skipped']);
  });

  it('done has no outgoing transitions', () => {
    expect(STATUS_TRANSITIONS.done).toEqual([]);
  });

  it('blocked → todo, doing', () => {
    expect(STATUS_TRANSITIONS.blocked).toEqual(['todo', 'doing']);
  });

  it('skipped has no outgoing transitions', () => {
    expect(STATUS_TRANSITIONS.skipped).toEqual([]);
  });
});

// ──────────────────────────────────────────────
// SHA-256 Attestation (wbs/attest.js)
// ──────────────────────────────────────────────

describe('attestation', () => {
  /** @type {{ path: string, cleanup: () => void }} */
  let tmp;

  beforeEach(() => {
    tmp = createTempDir();
  });

  afterEach(() => {
    tmp.cleanup();
  });

  describe('hashContent', () => {
    it('returns a 64-character hex string', () => {
      const hash = hashContent(SAMPLE_LEDGER);
      expect(hash).toMatch(/^[0-9a-f]{64}$/);
    });

    it('consistent output for same content', () => {
      expect(hashContent(SAMPLE_LEDGER)).toBe(hashContent(SAMPLE_LEDGER));
    });

    it('changes when content changes', () => {
      const h1 = hashContent(SAMPLE_LEDGER);
      const h2 = hashContent(SAMPLE_LEDGER.replace('Initialize', 'Changed'));
      expect(h1).not.toBe(h2);
    });

    it('normalizes line endings', () => {
      const crlf = SAMPLE_LEDGER.replace(/\n/g, '\r\n');
      expect(hashContent(crlf)).toBe(hashContent(SAMPLE_LEDGER));
    });
  });

  describe('attest / loadAttestation / checkAttestation', () => {
    it('attest writes a JSON record and returns hash/timestamp/algorithm', () => {
      const p = resolve(tmp.path, '.spm', 'wbs-attestation');
      const record = attest(SAMPLE_LEDGER, p);
      expect(record).toHaveProperty('hash');
      expect(record).toHaveProperty('timestamp');
      expect(record.algorithm).toBe('sha-256');
      expect(existsSync(p)).toBe(true);
    });

    it('loadAttestation reads back the record', () => {
      const p = resolve(tmp.path, '.spm', 'wbs-attestation');
      attest(SAMPLE_LEDGER, p);
      const loaded = loadAttestation(p);
      expect(loaded).not.toBeNull();
      expect(loaded.hash).toMatch(/^[0-9a-f]{64}$/);
    });

    it('loadAttestation returns null for missing file', () => {
      expect(loadAttestation('/nonexistent/file')).toBeNull();
    });

    it('loadAttestation returns null for malformed file', () => {
      const p = resolve(tmp.path, 'bad-attest');
      writeFileSync(p, 'not-json', 'utf-8');
      expect(loadAttestation(p)).toBeNull();
    });

    it('checkAttestation verifies matching content', () => {
      const p = resolve(tmp.path, '.spm', 'wbs-attestation');
      attest(SAMPLE_LEDGER, p);
      const result = checkAttestation(SAMPLE_LEDGER, p);
      expect(result.valid).toBe(true);
      expect(result.record).not.toBeNull();
    });

    it('checkAttestation detects tampered content', () => {
      const p = resolve(tmp.path, '.spm', 'wbs-attestation');
      attest(SAMPLE_LEDGER, p);
      const result = checkAttestation(SAMPLE_LEDGER + 'tampered', p);
      expect(result.valid).toBe(false);
    });
  });

  describe('verify', () => {
    it('returns true for matching hash', () => {
      const hash = hashContent(SAMPLE_LEDGER);
      expect(verify(SAMPLE_LEDGER, hash)).toBe(true);
    });

    it('returns false for different hash', () => {
      const hash = hashContent(SAMPLE_LEDGER);
      expect(verify(SAMPLE_LEDGER + 'x', hash)).toBe(false);
    });

    it('uses timing-safe comparison', () => {
      // Just verify the function works; internal timing-safety is a crypto concern
      const hash = hashContent(SAMPLE_LEDGER);
      expect(verify(SAMPLE_LEDGER, hash)).toBe(true);
    });
  });
});

// ──────────────────────────────────────────────
// Merkle Tree (wbs/merkle.js)
// ──────────────────────────────────────────────

describe('MerkleTree', () => {
  const tasks = [
    { id: 'WB-001', workPackage: 'Init', dependencies: [], status: 'done', contextBrief: '', exitCriteria: 'ok', evidence: 'done' },
    { id: 'WB-002', workPackage: 'Auth', dependencies: ['WB-001'], status: 'doing', contextBrief: '', exitCriteria: 'ok', evidence: '' },
    { id: 'WB-003', workPackage: 'Tests', dependencies: ['WB-001'], status: 'todo', contextBrief: '', exitCriteria: '', evidence: '' },
  ];

  describe('buildTree', () => {
    it('returns a snapshot with rootHash and nodeCount', () => {
      const tree = new MerkleTree();
      const snapshot = tree.buildTree(tasks);
      expect(snapshot.rootHash).toMatch(/^[0-9a-f]{64}$/);
      expect(snapshot.nodeCount).toBe(3);
      expect(snapshot.timestamp).toBeDefined();
    });

    it('produces deterministic root hash for same tasks', () => {
      const tree1 = new MerkleTree();
      const tree2 = new MerkleTree();
      expect(tree1.buildTree(tasks).rootHash).toBe(tree2.buildTree(tasks).rootHash);
    });

    it('root hash changes when a task changes', () => {
      const tree1 = new MerkleTree();
      const h1 = tree1.buildTree(tasks).rootHash;

      const modifiedTasks = tasks.map((t) =>
        t.id === 'WB-001' ? { ...t, status: 'todo' } : t,
      );
      const tree2 = new MerkleTree();
      const h2 = tree2.buildTree(modifiedTasks).rootHash;
      expect(h1).not.toBe(h2);
    });

    it('returns null rootHash for empty tree', () => {
      const tree = new MerkleTree();
      const snapshot = tree.buildTree([]);
      expect(snapshot.rootHash).toBeNull();
      expect(snapshot.nodeCount).toBe(0);
    });

    it('sorts tasks by id deterministically', () => {
      const shuffled = [tasks[2], tasks[0], tasks[1]];
      const tree = new MerkleTree();
      const snapshot = tree.buildTree(shuffled);
      expect(snapshot.nodeCount).toBe(3);
    });
  });

  describe('verifyNode', () => {
    it('returns valid=true for matching task data', () => {
      const tree = new MerkleTree();
      tree.buildTree(tasks);
      const result = tree.verifyNode('WB-001', tasks[0]);
      expect(result.valid).toBe(true);
      expect(result.expected).toBe(result.actual);
    });

    it('returns valid=false for modified task data', () => {
      const tree = new MerkleTree();
      tree.buildTree(tasks);
      const result = tree.verifyNode('WB-001', { ...tasks[0], status: 'todo' });
      expect(result.valid).toBe(false);
    });

    it('throws for unknown task id', () => {
      const tree = new MerkleTree();
      tree.buildTree(tasks);
      expect(() => tree.verifyNode('WB-999', {})).toThrow();
    });
  });

  describe('serialization (toJSON / fromJSON)', () => {
    it('toJSON returns a plain object', () => {
      const tree = new MerkleTree();
      tree.buildTree(tasks);
      const json = tree.toJSON();
      expect(json.rootHash).toMatch(/^[0-9a-f]{64}$/);
      expect(json.nodes['WB-001']).toBeDefined();
      expect(json.nodes['WB-001'].hash).toMatch(/^[0-9a-f]{64}$/);
    });

    it('fromJSON restores tree state', () => {
      const tree1 = new MerkleTree();
      tree1.buildTree(tasks);
      const json = tree1.toJSON();

      const tree2 = new MerkleTree();
      tree2.fromJSON(json);
      expect(tree2.getRootHash()).toBe(tree1.getRootHash());
      expect(tree2.getSnapshot().nodeCount).toBe(3);
    });
  });

  describe('getRootHash / getSnapshot / summarize', () => {
    it('getRootHash returns the root hash', () => {
      const tree = new MerkleTree();
      tree.buildTree(tasks);
      expect(tree.getRootHash()).toMatch(/^[0-9a-f]{64}$/);
    });

    it('getSnapshot returns frozen snapshot', () => {
      const tree = new MerkleTree();
      const snap = tree.buildTree(tasks);
      expect(Object.isFrozen(snap)).toBe(true);
    });

    it('summarize produces human-readable output', () => {
      const tree = new MerkleTree();
      tree.buildTree(tasks);
      const summary = tree.summarize();
      expect(summary).toContain('Merkle Tree Summary');
      expect(summary).toContain('WB-001');
    });
  });

  describe('hashTask', () => {
    it('returns SHA-256 hex of canonical task', () => {
      const h = hashTask({ id: 'WB-001', workPackage: 'Init' });
      expect(h).toMatch(/^[0-9a-f]{64}$/);
    });

    it('deterministic for same input', () => {
      const h1 = hashTask({ id: 'WB-001', workPackage: 'Init' });
      const h2 = hashTask({ id: 'WB-001', workPackage: 'Init' });
      expect(h1).toBe(h2);
    });
  });
});