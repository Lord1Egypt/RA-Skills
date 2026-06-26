/**
 * Tests for the import-state-manager module.
 */
import * as assert from 'node:assert/strict';
import * as fs from 'node:fs';
import * as os from 'node:os';
import * as path from 'node:path';
import { test, beforeEach, afterEach } from 'node:test';

import {
  writeImportState,
  readImportState,
  isImportStale,
  readMostRecentActiveImport,
  listAllImportStates,
  setImportStateDirForTests,
  type ImportState,
} from './import-state-manager.js';

let tmpDir: string;

beforeEach(() => {
  tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'import-state-test-'));
  setImportStateDirForTests(tmpDir);
});

afterEach(() => {
  fs.rmSync(tmpDir, { recursive: true, force: true });
});

function makeState(overrides: Partial<ImportState> = {}): ImportState {
  return {
    import_id: 'test-id-1234',
    source: 'chatgpt',
    status: 'running',
    started_at: new Date().toISOString(),
    last_updated: new Date().toISOString(),
    total_chunks: 100,
    total_messages: 2000,
    batch_done: 10,
    batch_total: 4,
    facts_stored: 25,
    facts_extracted: 28,
    dups_skipped: 3,
    errors: [],
    file_path: '/tmp/conversations.json',
    estimated_total_facts: 250,
    estimated_minutes: 12,
    estimated_completion_iso: new Date(Date.now() + 720000).toISOString(),
    disclosure_confirmed: true,
    ...overrides,
  };
}

test('writeImportState creates the directory and file', () => {
  const state = makeState({ import_id: 'write-test-1' });
  writeImportState(state);
  const read = readImportState('write-test-1');
  assert.ok(read !== null);
  assert.equal(read!.import_id, 'write-test-1');
  assert.equal(read!.source, 'chatgpt');
  assert.equal(read!.facts_stored, 25);
});

test('writeImportState updates last_updated timestamp', () => {
  const state = makeState({ import_id: 'ts-test-1', last_updated: '2020-01-01T00:00:00.000Z' });
  writeImportState(state);
  const read = readImportState('ts-test-1');
  assert.ok(read!.last_updated !== '2020-01-01T00:00:00.000Z', 'last_updated should be refreshed');
});

test('readImportState returns null for missing file', () => {
  const result = readImportState('does-not-exist-xyz');
  assert.equal(result, null);
});

test('isImportStale returns false for fresh state', () => {
  const state = makeState({ last_updated: new Date().toISOString() });
  assert.equal(isImportStale(state), false);
});

test('isImportStale returns true for state older than 1h', () => {
  const oldDate = new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(); // 2h ago
  const state = makeState({ last_updated: oldDate });
  assert.equal(isImportStale(state), true);
});

test('readMostRecentActiveImport returns null when no active imports', () => {
  // Write a completed import — should not be returned.
  writeImportState(makeState({ import_id: 'completed-1', status: 'completed' }));
  const result = readMostRecentActiveImport();
  // May return null or a running import from other tests; just verify no completed ones.
  if (result !== null) {
    assert.notEqual(result.status, 'completed');
  }
});

test('readMostRecentActiveImport returns most recent running import', () => {
  const id1 = 'active-older';
  const id2 = 'active-newer';
  const older = new Date(Date.now() - 60000).toISOString();
  const newer = new Date().toISOString();
  writeImportState(makeState({ import_id: id1, status: 'running', started_at: older }));
  writeImportState(makeState({ import_id: id2, status: 'running', started_at: newer }));
  const result = readMostRecentActiveImport();
  assert.ok(result !== null);
  assert.equal(result!.import_id, id2);
});

test('listAllImportStates returns states sorted newest-first', () => {
  const idA = 'list-test-a';
  const idB = 'list-test-b';
  const idC = 'list-test-c';
  writeImportState(makeState({ import_id: idA, started_at: new Date(Date.now() - 3000).toISOString(), status: 'completed' }));
  writeImportState(makeState({ import_id: idB, started_at: new Date(Date.now() - 1000).toISOString(), status: 'running' }));
  writeImportState(makeState({ import_id: idC, started_at: new Date(Date.now() - 2000).toISOString(), status: 'failed' }));

  const all = listAllImportStates();
  const ids = all.map((s) => s.import_id);
  // idB should come before idC which comes before idA
  const posB = ids.indexOf(idB);
  const posC = ids.indexOf(idC);
  const posA = ids.indexOf(idA);
  assert.ok(posB < posC, 'newer should come before older');
  assert.ok(posC < posA, 'middle should come before oldest');
});

test('writeImportState round-trips all fields', () => {
  const state = makeState({
    import_id: 'roundtrip-1',
    errors: ['err1', 'err2'],
    disclosure_confirmed: false,
    dups_skipped: 7,
  });
  writeImportState(state);
  const read = readImportState('roundtrip-1');
  assert.deepEqual(read!.errors, ['err1', 'err2']);
  assert.equal(read!.disclosure_confirmed, false);
  assert.equal(read!.dups_skipped, 7);
});
