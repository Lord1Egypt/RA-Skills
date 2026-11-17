import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const root = fs.mkdtempSync(path.join(os.tmpdir(), 'sis-observe-'));
const script = fileURLToPath(new URL('./heartbeat_observe.mjs', import.meta.url));
const write = (file, value) => fs.writeFileSync(file, JSON.stringify(value));
function fixture(name) {
  const workspace = path.join(root, name);
  fs.mkdirSync(path.join(workspace, 'memory'), {recursive: true});
  const heartbeat = path.join(workspace, 'memory/heartbeat-state.json');
  const mirror = path.join(workspace, 'memory/now-state.json');
  const observation = path.join(workspace, 'observation.json');
  write(heartbeat, {unrelated: {keep: true}, lastSnapshotAt: 17,
    evidence_references: {retained: 'existing source'}});
  write(mirror, {updated_at: '2026-10-05T00:00:00Z', stress: 0, state_id: 'historical'});
  write(observation, {result: 'no_change', reason: 'Grounded fixture observation.',
    evidence_references: {context: 'fixture source'}});
  return {workspace, heartbeat, mirror, observation};
}
function run(f, ...args) {
  return spawnSync(process.execPath, [script, '--workspace', f.workspace,
    '--observation-file', f.observation, ...args], {encoding: 'utf8', cwd: os.tmpdir()});
}

test('preview is default and apply merges only the observation without refreshing the snapshot', () => {
  const f = fixture('workspace with spaces');
  const before = fs.readFileSync(f.heartbeat, 'utf8');
  const mirror = fs.readFileSync(f.mirror, 'utf8');
  for (const args of [[], ['--dry-run']]) {
    const r = run(f, ...args);
    assert.equal(r.status, 0, r.stderr);
    assert.equal(JSON.parse(r.stdout).applied, false);
    assert.equal(fs.readFileSync(f.heartbeat, 'utf8'), before);
  }
  const r = run(f, '--apply');
  assert.equal(r.status, 0, r.stderr);
  const result = JSON.parse(r.stdout);
  const saved = JSON.parse(fs.readFileSync(f.heartbeat, 'utf8'));
  assert.equal(result.applied, true);
  assert.deepEqual(saved.unrelated, {keep: true});
  assert.equal(saved.lastSnapshotAt, 17);
  assert.equal(saved.last_soul_result, 'no_change');
  assert.deepEqual(saved.evidence_references, {retained: 'existing source', context: 'fixture source'});
  assert.equal(saved.last_soul_check, result.last_soul_check);
  assert.match(saved.last_soul_check, /T.*Z$/);
  assert.equal(fs.readFileSync(f.mirror, 'utf8'), mirror);
});

test('invalid observation and malformed prior state cannot overwrite existing data', () => {
  const f = fixture('invalid');
  const before = fs.readFileSync(f.heartbeat, 'utf8');
  for (const observation of [
    {result: 'success', reason: 'fixture', evidence_references: {}},
    {result: 'no_change', reason: ' ', evidence_references: {}},
    {result: 'no_change', reason: 'fixture', evidence_references: []},
    {result: 'no_change', reason: 'fixture', evidence_references: {source: 4}},
    {result: 'no_change', reason: 'fixture', evidence_references: {state_id: 'invented'}},
  ]) {
    write(f.observation, observation);
    assert.notEqual(run(f, '--apply').status, 0);
    assert.equal(fs.readFileSync(f.heartbeat, 'utf8'), before);
  }
  write(f.observation, {result: 'failed', reason: 'Fixture evidence unavailable.', evidence_references: {}});
  for (const malformed of ['{broken', '[]', '{"evidence_references":[]}']) {
    fs.writeFileSync(f.heartbeat, malformed);
    assert.notEqual(run(f, '--apply').status, 0);
    assert.equal(fs.readFileSync(f.heartbeat, 'utf8'), malformed);
  }
});

test('changed requires a completed, non-pending receipt and obtains IDs only from it', () => {
  const f = fixture('changed');
  write(f.observation, {result: 'changed', reason: 'A completed fixture tick.', evidence_references: {}});
  const before = fs.readFileSync(f.heartbeat, 'utf8');
  assert.notEqual(run(f, '--apply').status, 0);
  const receipt = path.join(f.workspace, 'receipt.json');
  for (const value of [
    {complete: false, event: {id: 'event'}, state: {id: 'state'}},
    {complete: true, pending: 'state', event: {id: 'event'}, state: {id: 'state'}},
    {complete: true, event: {id: 'event'}, state: {id: 2}},
  ]) {
    write(receipt, value);
    assert.notEqual(run(f, '--receipt-file', receipt, '--apply').status, 0);
    assert.equal(fs.readFileSync(f.heartbeat, 'utf8'), before);
  }
  write(receipt, {complete: true, pending: null, event: {id: 'fixture-event'}, state: {id: 'fixture-state'}});
  const r = run(f, '--receipt-file', receipt, '--apply');
  assert.equal(r.status, 0, r.stderr);
  assert.deepEqual(JSON.parse(r.stdout).evidence_references,
    {retained: 'existing source', event_id: 'fixture-event', state_id: 'fixture-state'});
});

test('missing heartbeat state can be initialized without creating a snapshot or changing inputs', () => {
  const workspace = path.join(root, 'new-workspace');
  const observation = path.join(root, 'new-observation.json');
  write(observation, {result: 'unavailable', reason: 'Fixture has no evidence yet.', evidence_references: {}});
  const input = fs.readFileSync(observation, 'utf8');
  const f = {workspace, observation};
  const preview = run(f);
  assert.equal(preview.status, 0, preview.stderr);
  assert.equal(fs.existsSync(workspace), false);
  const applied = run(f, '--apply');
  assert.equal(applied.status, 0, applied.stderr);
  assert.equal(JSON.parse(fs.readFileSync(path.join(workspace, 'memory/heartbeat-state.json'))).last_soul_result, 'unavailable');
  assert.equal(fs.existsSync(path.join(workspace, 'memory/now-state.json')), false);
  assert.equal(fs.readFileSync(observation, 'utf8'), input);
});

test('workspace is explicit and conflicting write modes fail before mutation', () => {
  const f = fixture('arguments');
  const before = fs.readFileSync(f.heartbeat, 'utf8');
  assert.notEqual(run(f, '--apply', '--dry-run').status, 0);
  const missingWorkspace = spawnSync(process.execPath, [script, '--observation-file', f.observation, '--apply'], {encoding: 'utf8'});
  assert.notEqual(missingWorkspace.status, 0);
  assert.match(missingWorkspace.stderr, /workspace is required/);
  assert.equal(fs.readFileSync(f.heartbeat, 'utf8'), before);
});
