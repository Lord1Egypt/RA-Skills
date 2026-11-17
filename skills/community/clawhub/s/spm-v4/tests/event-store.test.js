/**
 * Tests for the Event Store module (src/event-store/).
 *
 * Covers: push/query operations, domain configuration, JSONL append
 * and read, file rotation, retention cleanup, error handling.
 *
 * @module tests/event-store.test
 */

import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import { existsSync, readFileSync, writeFileSync, unlinkSync, statSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { EventStore, buildDomainConfigs } from '../src/event-store/index.js';
import {
  append,
  appendBatch,
  readAll,
  readRange,
  readRecent,
  rotate,
  prune,
  parseLines,
} from '../src/event-store/storage.js';
import { createTempDir, cleanupTempDirs } from './setup.js';

// ──────────────────────────────────────────────
// parseLines (internal helper)
// ──────────────────────────────────────────────

describe('parseLines', () => {
  it('parses valid JSON lines', () => {
    const raw = '{"id":"1"}\n{"id":"2"}\n';
    const events = parseLines(raw);
    expect(events).toHaveLength(2);
    expect(events[0].id).toBe('1');
  });

  it('skips empty lines', () => {
    const raw = '{"id":"1"}\n\n\n{"id":"2"}\n';
    const events = parseLines(raw);
    expect(events).toHaveLength(2);
  });

  it('skips malformed JSON silently', () => {
    const raw = '{"id":"1"}\nnot-json\n{"id":"2"}\n';
    const events = parseLines(raw);
    expect(events).toHaveLength(2);
  });

  it('returns empty array for empty input', () => {
    expect(parseLines('')).toEqual([]);
  });

  it('returns empty array for whitespace-only input', () => {
    expect(parseLines('   \n\n  ')).toEqual([]);
  });
});

// ──────────────────────────────────────────────
// Storage: append/read
// ──────────────────────────────────────────────

describe('storage', () => {
  /** @type {{ path: string, cleanup: () => void }} */
  let tmp;

  beforeEach(() => {
    tmp = createTempDir();
  });

  afterEach(() => {
    tmp.cleanup();
  });

  describe('append / readAll', () => {
    it('append creates file and writes JSON line', () => {
      const file = resolve(tmp.path, 'test.jsonl');
      append(file, { id: 'evt-1', type: 'test', payload: { x: 1 } });
      expect(existsSync(file)).toBe(true);
      const events = readAll(file);
      expect(events).toHaveLength(1);
      expect(events[0].id).toBe('evt-1');
    });

    it('append multiple events', () => {
      const file = resolve(tmp.path, 'multi.jsonl');
      append(file, { id: '1' });
      append(file, { id: '2' });
      append(file, { id: '3' });
      expect(readAll(file)).toHaveLength(3);
    });

    it('readAll throws for missing file', () => {
      expect(() => readAll('/nonexistent/file.jsonl')).toThrow();
    });
  });

  describe('appendBatch', () => {
    it('writes all events atomically', () => {
      const file = resolve(tmp.path, 'batch.jsonl');
      const events = [
        { id: 'a', type: 'test' },
        { id: 'b', type: 'test' },
      ];
      appendBatch(file, events);
      const loaded = readAll(file);
      expect(loaded).toHaveLength(2);
      expect(loaded[0].id).toBe('a');
      expect(loaded[1].id).toBe('b');
    });
  });

  describe('readRange', () => {
    it('filters events by time range', () => {
      const file = resolve(tmp.path, 'range.jsonl');
      append(file, { id: 'early', timestamp: 1000 });
      append(file, { id: 'mid', timestamp: 2000 });
      append(file, { id: 'late', timestamp: 3000 });

      const mid = readRange(file, 1500, 2500);
      expect(mid).toHaveLength(1);
      expect(mid[0].id).toBe('mid');
    });

    it('returns all events when range covers everything', () => {
      const file = resolve(tmp.path, 'all-range.jsonl');
      append(file, { id: 'a', timestamp: 100 });
      append(file, { id: 'b', timestamp: 200 });
      expect(readRange(file, 0, 999)).toHaveLength(2);
    });

    it('returns empty when range matches nothing', () => {
      const file = resolve(tmp.path, 'no-match.jsonl');
      append(file, { id: 'a', timestamp: 500 });
      expect(readRange(file, 1000, 2000)).toHaveLength(0);
    });
  });

  describe('readRecent', () => {
    it('returns last N events', () => {
      const file = resolve(tmp.path, 'recent.jsonl');
      for (let i = 1; i <= 10; i++) {
        append(file, { id: `evt-${i}` });
      }
      const recent = readRecent(file, 3);
      expect(recent).toHaveLength(3);
      expect(recent[0].id).toBe('evt-8');
      expect(recent[2].id).toBe('evt-10');
    });

    it('returns all events when N exceeds total', () => {
      const file = resolve(tmp.path, 'few.jsonl');
      append(file, { id: 'a' });
      append(file, { id: 'b' });
      expect(readRecent(file, 10)).toHaveLength(2);
    });
  });

  describe('rotate', () => {
    it('rotates file when size exceeds maxBytes', () => {
      const file = resolve(tmp.path, 'rotate.jsonl');
      // Write enough data to trigger rotation
      const bigPayload = { id: 'big', data: 'x'.repeat(500) };
      append(file, bigPayload);
      const result = rotate(file, 50); // small threshold
      expect(result).not.toBeNull(); // archive path
      expect(result).toContain('rotate.');
    });

    it('returns null when rotation is not needed', () => {
      const file = resolve(tmp.path, 'no-rotate.jsonl');
      append(file, { id: 'small' });
      expect(rotate(file, 999999)).toBeNull();
    });
  });

  describe('prune', () => {
    it('deletes old domain files', () => {
      const file = resolve(tmp.path, 'audit.old.jsonl');
      writeFileSync(file, '{"id":"old"}');
      const deleted = prune(tmp.path, 'audit', Date.now() + 999999); // all files are "old"
      expect(deleted.length).toBeGreaterThan(0);
      expect(existsSync(file)).toBe(false);
    });

    it('does not delete temp files', () => {
      const temp = resolve(tmp.path, '.audit.tmp');
      writeFileSync(temp, 'data');
      const deleted = prune(tmp.path, 'audit', Date.now() + 999999);
      expect(deleted).not.toContain(temp);
    });

    it('returns empty for non-existent directory', () => {
      expect(prune('/nonexistent', 'audit', Date.now())).toEqual([]);
    });

    it('skips files with different prefix', () => {
      const other = resolve(tmp.path, 'other.jsonl');
      writeFileSync(other, 'data');
      const deleted = prune(tmp.path, 'audit', Date.now() + 999999);
      expect(deleted).toEqual([]);
    });
  });
});

// ──────────────────────────────────────────────
// Domain Configs
// ──────────────────────────────────────────────

describe('buildDomainConfigs', () => {
  /** @type {{ path: string, cleanup: () => void }} */
  let tmp;

  beforeEach(() => {
    tmp = createTempDir();
  });

  afterEach(() => {
    tmp.cleanup();
  });

  it('builds configs for audit, integrity, and quality', () => {
    const configs = buildDomainConfigs(tmp.path);
    expect(configs).toHaveLength(3);
    const names = configs.map((c) => c.name).sort();
    expect(names).toEqual(['audit', 'integrity', 'quality']);
  });

  it('resolves file paths relative to baseDir', () => {
    const configs = buildDomainConfigs(tmp.path);
    for (const cfg of configs) {
      expect(cfg.file_path.startsWith(tmp.path)).toBe(true);
      expect(cfg.file_path.endsWith(`${cfg.name}.jsonl`)).toBe(true);
    }
  });

  it('applies per-domain overrides', () => {
    const configs = buildDomainConfigs(tmp.path, {
      audit: { retention_days: 30 },
    });
    const audit = configs.find((c) => c.name === 'audit');
    expect(audit.retention_days).toBe(30);
  });

  it('sets default retention values', () => {
    const configs = buildDomainConfigs(tmp.path);
    const audit = configs.find((c) => c.name === 'audit');
    expect(audit.retention_days).toBe(365);
  });

  it('sets default max_file_size values', () => {
    const configs = buildDomainConfigs(tmp.path);
    const q = configs.find((c) => c.name === 'quality');
    expect(q.max_file_size).toBe(10 * 1024 * 1024);
  });
});

// ──────────────────────────────────────────────
// EventStore Class
// ──────────────────────────────────────────────

describe('EventStore', () => {
  /** @type {{ path: string, cleanup: () => void }} */
  let tmp;
  /** @type {EventStore} */
  let store;

  beforeEach(() => {
    tmp = createTempDir();
    store = new EventStore(tmp.path);
  });

  afterEach(() => {
    tmp.cleanup();
  });

  describe('constructor', () => {
    it('creates the base directory', () => {
      expect(existsSync(tmp.path)).toBe(true);
    });

    it('registers all three domains', () => {
      const names = store.domainNames();
      expect(names.sort()).toEqual(['audit', 'integrity', 'quality']);
    });

    it('accepts domain overrides', () => {
      const s = new EventStore(tmp.path, { audit: { retention_days: 10 } });
      const cfg = s.getByDomain('audit');
      expect(cfg.retention_days).toBe(10);
    });
  });

  describe('push', () => {
    it('enriches event with id, domain, and timestamp', () => {
      const ev = store.push('audit', { type: 'test', payload: { msg: 'hello' } });
      expect(ev.id).toBeDefined();
      expect(ev.domain).toBe('audit');
      expect(ev.timestamp).toBeDefined();
      expect(typeof ev.timestamp).toBe('number');
    });

    it('preserves provided id and timestamp', () => {
      const ev = store.push('audit', {
        id: 'my-custom-id',
        timestamp: 123456789,
        type: 'test',
        payload: {},
      });
      expect(ev.id).toBe('my-custom-id');
      expect(ev.timestamp).toBe(123456789);
    });

    it('writes event to the JSONL file', () => {
      store.push('audit', { type: 'command.run', payload: { cmd: 'ls' } });
      const evts = readAll(resolve(tmp.path, 'audit.jsonl'));
      expect(evts).toHaveLength(1);
      expect(evts[0].type).toBe('command.run');
    });

    it('throws for unknown domain', () => {
      expect(() => store.push('unknown', {})).toThrow();
    });

    it('allows push to integrity and quality domains', () => {
      store.push('integrity', { type: 'attest', payload: { hash: 'abc' } });
      store.push('quality', { type: 'gate.passed', payload: { score: 95 } });
      expect(store.query('integrity')).toHaveLength(1);
      expect(store.query('quality')).toHaveLength(1);
    });
  });

  describe('pushBatch', () => {
    it('enriches and persists multiple events', () => {
      const events = store.pushBatch('audit', [
        { type: 'a', payload: { i: 1 } },
        { type: 'b', payload: { i: 2 } },
      ]);
      expect(events).toHaveLength(2);
      expect(store.query('audit')).toHaveLength(2);
    });
  });

  describe('query', () => {
    beforeEach(() => {
      for (let i = 1; i <= 5; i++) {
        store.push('audit', { type: 'progress', payload: { step: i } });
      }
      store.push('audit', { type: 'error', payload: { msg: 'boom' } });
    });

    it('returns all events without filters', () => {
      expect(store.query('audit')).toHaveLength(6);
    });

    it('filters by type', () => {
      const errors = store.query('audit', { type: 'error' });
      expect(errors).toHaveLength(1);
      expect(errors[0].type).toBe('error');
    });

    it('filters by limit (returns last N events)', () => {
      const limited = store.query('audit', { limit: 2 });
      expect(limited).toHaveLength(2);
      // slice(-2) returns the last 2 events: progress step 5 and error
      expect(limited[0].payload.step).toBe(5);
      expect(limited[1].type).toBe('error');
    });

    it('filters by recent (N most recent)', () => {
      const recent = store.query('audit', { recent: 2 });
      expect(recent).toHaveLength(2);
    });

    it('filters by after/before timestamp', () => {
      // Push events with controlled timestamps
      const store2 = new EventStore(resolve(tmp.path, 'ts-test'));
      const t0 = 1000;
      const t1 = 2000;
      const t2 = 3000;
      store2.push('audit', { type: 'early', timestamp: t0, payload: {} });
      store2.push('audit', { type: 'mid', timestamp: t1, payload: {} });
      store2.push('audit', { type: 'late', timestamp: t2, payload: {} });
      const mid = store2.query('audit', { after: 1500, before: 2500 });
      expect(mid).toHaveLength(1);
      expect(mid[0].type).toBe('mid');
    });

    it('combines type and limit filters', () => {
      store.push('audit', { type: 'error', payload: { msg: 'err2' } });
      const errors = store.query('audit', { type: 'error', limit: 1 });
      expect(errors).toHaveLength(1);
    });

    it('throws for unknown domain', () => {
      expect(() => store.query('nope')).toThrow();
    });
  });

  describe('getByDomain', () => {
    it('returns domain config', () => {
      const cfg = store.getByDomain('quality');
      expect(cfg.name).toBe('quality');
      expect(cfg.retention_days).toBe(180);
    });

    it('returns a shallow copy (mutation-safe)', () => {
      const cfg = store.getByDomain('audit');
      cfg.retention_days = 999;
      expect(store.getByDomain('audit').retention_days).toBe(365);
    });

    it('throws for unknown domain', () => {
      expect(() => store.getByDomain('void')).toThrow();
    });
  });

  describe('rotateDomain', () => {
    it('rotates the active file for a domain', () => {
      store.push('audit', { type: 'test', payload: {} });
      const archive = store.rotateDomain('audit');
      expect(archive).not.toBeNull();
      expect(typeof archive).toBe('string');
    });

    it('throws for unknown domain', () => {
      expect(() => store.rotateDomain('nope')).toThrow();
    });
  });

  describe('cleanup', () => {
    it('returns pruned files per domain', () => {
      const result = store.cleanup();
      expect(result).toHaveProperty('audit');
      expect(result).toHaveProperty('integrity');
      expect(result).toHaveProperty('quality');
      // Initially there are no old files
      expect(result.audit).toEqual([]);
    });
  });

  describe('domainNames', () => {
    it('returns registered domain names', () => {
      const names = store.domainNames().sort();
      expect(names).toEqual(['audit', 'integrity', 'quality']);
    });
  });
});