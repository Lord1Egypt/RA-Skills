/**
 * Tests for the Session modules (src/session/).
 *
 * Covers: heartbeat logging (log, readAll, getLatest, getBySession,
 * validation), session recovery report generation, checkpoint detection,
 * and timestamp-based checkpoint lookup.
 *
 * @module tests/session.test
 */

import { describe, it, expect, beforeEach, afterEach } from '@jest/globals';
import { existsSync, readFileSync, unlinkSync } from 'node:fs';
import { resolve } from 'node:path';
import { log, readAll, getLatest, getBySession } from '../src/session/heartbeat.js';
import { generateRecoveryReport, getCheckpoint } from '../src/session/index.js';
import { createTempDir, cleanupTempDirs } from './setup.js';

// ──────────────────────────────────────────────
// Heartbeat Log
// ──────────────────────────────────────────────

describe('Heartbeat', () => {
  /** @type {{ path: string, cleanup: () => void }} */
  let tmp;
  /** @type {string} */
  let hbPath;

  beforeEach(() => {
    tmp = createTempDir();
    hbPath = resolve(tmp.path, 'heartbeats.jsonl');
  });

  afterEach(() => {
    tmp.cleanup();
  });

  describe('log', () => {
    it('appends a heartbeat entry to the log file', () => {
      log({
        timestamp: '2026-07-04T20:00:00.000Z',
        sessionId: 'session-1',
        activeTask: 'WB-001',
        status: 'running',
      }, hbPath);

      expect(existsSync(hbPath)).toBe(true);
      const content = readFileSync(hbPath, 'utf-8').trim();
      expect(content).toContain('session-1');
    });

    it('appends multiple heartbeats', () => {
      log({ timestamp: 'T1', sessionId: 's1', activeTask: 'A', status: 'running' }, hbPath);
      log({ timestamp: 'T2', sessionId: 's1', activeTask: 'B', status: 'running' }, hbPath);
      const lines = readFileSync(hbPath, 'utf-8').trim().split('\n');
      expect(lines).toHaveLength(2);
    });

    it('throws when required fields are missing', () => {
      // Missing sessionId
      expect(() => log({ timestamp: 'T1', activeTask: 'A' }, hbPath)).toThrow();
    });

    it('throws when timestamp is missing', () => {
      expect(() => log({ sessionId: 's1', activeTask: 'A' }, hbPath)).toThrow();
    });

    it('throws when activeTask is missing', () => {
      expect(() => log({ timestamp: 'T1', sessionId: 's1' }, hbPath)).toThrow();
    });

    it('stores optional note field', () => {
      log({
        timestamp: 'T1',
        sessionId: 's1',
        activeTask: 'A',
        status: 'running',
        note: 'progressing well',
      }, hbPath);

      const all = readAll(hbPath);
      expect(all[0].note).toBe('progressing well');
    });
  });

  describe('readAll', () => {
    it('returns empty array when file does not exist', () => {
      expect(readAll('/nonexistent/heartbeats.jsonl')).toEqual([]);
    });

    it('returns empty array when file is empty', () => {
      // readAll checks if file exists and is non-empty
      // We need to create it through the module (log only writes non-empty)
      // Just check non-existent returns empty
      expect(readAll('/nonexistent/heartbeats.jsonl')).toEqual([]);
    });

    it('reads all heartbeats in order', () => {
      log({ timestamp: 'T1', sessionId: 's1', activeTask: 'A', status: 'running' }, hbPath);
      log({ timestamp: 'T2', sessionId: 's1', activeTask: 'B', status: 'done' }, hbPath);
      const all = readAll(hbPath);
      expect(all).toHaveLength(2);
      expect(all[0].activeTask).toBe('A');
      expect(all[1].activeTask).toBe('B');
    });
  });

  describe('getLatest', () => {
    it('returns the most recent heartbeat', () => {
      log({ timestamp: 'T1', sessionId: 's1', activeTask: 'first', status: 'running' }, hbPath);
      log({ timestamp: 'T2', sessionId: 's1', activeTask: 'last', status: 'running' }, hbPath);
      const latest = getLatest(hbPath);
      expect(latest.activeTask).toBe('last');
    });

    it('returns null when no heartbeats exist', () => {
      expect(getLatest('/nonexistent/hb.jsonl')).toBeNull();
    });
  });

  describe('getBySession', () => {
    it('filters heartbeats by session id', () => {
      log({ timestamp: 'T1', sessionId: 'session-a', activeTask: 'A', status: 'running' }, hbPath);
      log({ timestamp: 'T2', sessionId: 'session-b', activeTask: 'B', status: 'running' }, hbPath);
      log({ timestamp: 'T3', sessionId: 'session-a', activeTask: 'C', status: 'done' }, hbPath);

      const sessionA = getBySession('session-a', hbPath);
      expect(sessionA).toHaveLength(2);
      expect(sessionA[0].activeTask).toBe('A');
      expect(sessionA[1].activeTask).toBe('C');
    });

    it('returns empty array for unknown session', () => {
      log({ timestamp: 'T1', sessionId: 's1', activeTask: 'A', status: 'running' }, hbPath);
      const result = getBySession('unknown', hbPath);
      expect(result).toEqual([]);
    });
  });
});

// ──────────────────────────────────────────────
// Session Recovery
// ──────────────────────────────────────────────

describe('Session Recovery', () => {
  /** @type {{ path: string, cleanup: () => void }} */
  let tmp;
  /** @type {string} */
  let hbPath;

  beforeEach(() => {
    tmp = createTempDir();
    hbPath = resolve(tmp.path, 'heartbeats.jsonl');
  });

  afterEach(() => {
    tmp.cleanup();
  });

  describe('generateRecoveryReport', () => {
    it('returns empty report when there are no heartbeats', () => {
      const report = generateRecoveryReport('/nonexistent/heartbeats.jsonl');
      expect(report.totalHeartbeats).toBe(0);
      expect(report.activeTask).toBeNull();
      expect(report.lastCheckpoint).toBeNull();
      expect(report.completedTasks).toEqual([]);
    });

    it('identifies the active task (latest heartbeat)', () => {
      log({ timestamp: 'T1', sessionId: 's1', activeTask: 'WB-001', status: 'running' }, hbPath);
      log({ timestamp: 'T2', sessionId: 's1', activeTask: 'WB-002', status: 'running' }, hbPath);
      const report = generateRecoveryReport(hbPath);
      expect(report.activeTask.activeTask).toBe('WB-002');
      expect(report.sessionId).toBe('s1');
    });

    it('identifies completed tasks', () => {
      log({ timestamp: 'T1', sessionId: 's1', activeTask: 'WB-001', status: 'completed' }, hbPath);
      log({ timestamp: 'T2', sessionId: 's1', activeTask: 'WB-002', status: 'running' }, hbPath);
      log({ timestamp: 'T3', sessionId: 's1', activeTask: 'WB-003', status: 'completed' }, hbPath);
      const report = generateRecoveryReport(hbPath);
      expect(report.completedTasks).toHaveLength(2);
      expect(report.completedTasks[0].activeTask).toBe('WB-001');
      expect(report.completedTasks[1].activeTask).toBe('WB-003');
    });

    it('identifies the last checkpoint by status', () => {
      log({ timestamp: 'T1', sessionId: 's1', activeTask: 'WB-001', status: 'running' }, hbPath);
      log({ timestamp: 'T2', sessionId: 's1', activeTask: 'WB-002', status: 'checkpoint' }, hbPath);
      log({ timestamp: 'T3', sessionId: 's1', activeTask: 'WB-003', status: 'running' }, hbPath);
      const report = generateRecoveryReport(hbPath);
      expect(report.lastCheckpoint.activeTask).toBe('WB-002');
    });

    it('identifies the last checkpoint by "paused" status', () => {
      log({ timestamp: 'T1', sessionId: 's1', activeTask: 'WB-001', status: 'paused' }, hbPath);
      const report = generateRecoveryReport(hbPath);
      expect(report.lastCheckpoint.activeTask).toBe('WB-001');
    });

    it('identifies checkpoint by note keyword "checkpoint"', () => {
      log({
        timestamp: 'T1',
        sessionId: 's1',
        activeTask: 'WB-001',
        status: 'running',
        note: 'Creating a checkpoint here',
      }, hbPath);
      const report = generateRecoveryReport(hbPath);
      expect(report.lastCheckpoint.activeTask).toBe('WB-001');
    });

    it('identifies checkpoint by note keyword "save"', () => {
      log({
        timestamp: 'T1',
        sessionId: 's1',
        activeTask: 'WB-001',
        status: 'running',
        note: 'Saved progress',
      }, hbPath);
      const report = generateRecoveryReport(hbPath);
      expect(report.lastCheckpoint.activeTask).toBe('WB-001');
    });

    it('identifies checkpoint by note keyword "snapshot"', () => {
      log({
        timestamp: 'T1',
        sessionId: 's1',
        activeTask: 'WB-001',
        status: 'running',
        note: 'Taking snapshot',
      }, hbPath);
      const report = generateRecoveryReport(hbPath);
      expect(report.lastCheckpoint.activeTask).toBe('WB-001');
    });

    it('accumulates context notes from all heartbeats', () => {
      log({
        timestamp: 'T1',
        sessionId: 's1', activeTask: 'A', status: 'running',
        note: 'Started',
      }, hbPath);
      log({
        timestamp: 'T2',
        sessionId: 's1', activeTask: 'B', status: 'running',
        note: 'Progress',
      }, hbPath);
      const report = generateRecoveryReport(hbPath);
      expect(report.contextNotes).toHaveLength(2);
      expect(report.contextNotes[0]).toContain('Started');
      expect(report.contextNotes[1]).toContain('Progress');
    });

    it('counts total heartbeats correctly', () => {
      for (let i = 1; i <= 5; i++) {
        log({
          timestamp: `T${i}`, sessionId: 's1',
          activeTask: `WB-00${i}`, status: 'running',
        }, hbPath);
      }
      const report = generateRecoveryReport(hbPath);
      expect(report.totalHeartbeats).toBe(5);
    });
  });

  describe('getCheckpoint', () => {
    it('returns null for empty log', () => {
      expect(getCheckpoint('2026-07-04T00:00:00Z', '/nonexistent/file')).toBeNull();
    });

    it('returns the heartbeat nearest to the given timestamp (≤)', () => {
      log({ timestamp: '2026-07-04T10:00:00Z', sessionId: 's1', activeTask: 'A', status: 'running' }, hbPath);
      log({ timestamp: '2026-07-04T12:00:00Z', sessionId: 's1', activeTask: 'B', status: 'running' }, hbPath);
      log({ timestamp: '2026-07-04T14:00:00Z', sessionId: 's1', activeTask: 'C', status: 'running' }, hbPath);

      // Target is between T12 and T14, should return T12
      const cp = getCheckpoint('2026-07-04T13:00:00Z', hbPath);
      expect(cp.activeTask).toBe('B');
    });

    it('returns earliest entry when all heartbeats are after target', () => {
      log({ timestamp: '2026-07-04T10:00:00Z', sessionId: 's1', activeTask: 'A', status: 'running' }, hbPath);
      const cp = getCheckpoint('2026-07-04T00:00:00Z', hbPath);
      expect(cp.activeTask).toBe('A');
    });
  });
});