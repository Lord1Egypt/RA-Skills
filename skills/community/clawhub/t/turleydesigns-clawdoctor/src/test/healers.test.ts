import { describe, it, before, after } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'fs';
import path from 'path';
import os from 'os';
import { DEFAULT_CONFIG, ClawDoctorConfig } from '../config.js';
import { CronHealer } from '../healers/cron.js';
import { AuthHealer } from '../healers/auth.js';
import { SessionHealer } from '../healers/session.js';

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'clawdoctor-healers-test-'));

function makeConfig(overrides: Partial<ClawDoctorConfig> = {}): ClawDoctorConfig {
  return {
    ...DEFAULT_CONFIG,
    openclawPath: tmpDir,
    dryRun: true, // Always dry-run in tests
    ...overrides,
  };
}

// ── Snapshot tests ─────────────────────────────────────────────────────────────

describe('Snapshots', () => {
  const snapshotsDir = path.join(tmpDir, 'snapshots-test');

  before(() => {
    fs.mkdirSync(snapshotsDir, { recursive: true });
  });

  it('creates and reads a snapshot file', async () => {
    const { createSnapshot, getSnapshot, listSnapshots } = await import('../snapshots.js');
    const id = createSnapshot('test-action', 'test-target', { key: 'value' }, 'echo rollback');
    assert.ok(id.includes('test-action'), `Expected id to contain action, got: ${id}`);

    const snap = getSnapshot(id);
    assert.ok(snap, 'Snapshot should exist');
    assert.equal(snap.action, 'test-action');
    assert.equal(snap.target, 'test-target');
    assert.equal(snap.rollbackCommand, 'echo rollback');
    assert.deepEqual(snap.before, { key: 'value' });

    const list = listSnapshots();
    assert.ok(list.some(s => s.id === id), 'Snapshot should appear in list');
  });

  it('returns null for non-existent snapshot', async () => {
    const { getSnapshot } = await import('../snapshots.js');
    const snap = getSnapshot('non-existent-id-xyz');
    assert.equal(snap, null);
  });

  it('executeRollback returns error for missing snapshot', async () => {
    const { executeRollback } = await import('../snapshots.js');
    const result = executeRollback('definitely-does-not-exist');
    assert.equal(result.success, false);
    assert.ok(result.message.includes('not found'));
  });

  it('executeRollback rejects non-allowlisted commands', async () => {
    const { createSnapshot, executeRollback } = await import('../snapshots.js');
    const id = createSnapshot('echo-test', 'test', {}, 'echo hello-rollback');
    const result = executeRollback(id);
    assert.equal(result.success, false, 'Non-allowlisted command should be rejected');
    assert.ok(result.message.includes('allowlist'), `Expected allowlist rejection, got: ${result.message}`);
  });
});

// ── Audit trail tests ──────────────────────────────────────────────────────────

describe('Audit Trail', () => {
  it('writes and reads audit entries', async () => {
    const { appendAudit, getRecentAudit } = await import('../audit.js');

    appendAudit({
      timestamp: new Date().toISOString(),
      healer: 'CronHealer',
      action: 'cron-retry',
      target: 'test-cron',
      tier: 'green',
      result: 'success',
      snapshotId: 'snap-001',
    });

    const entries = getRecentAudit(10);
    const found = entries.find(e => e.healer === 'CronHealer' && e.target === 'test-cron');
    assert.ok(found, 'Audit entry should be found');
    assert.equal(found.action, 'cron-retry');
    assert.equal(found.tier, 'green');
    assert.equal(found.result, 'success');
    assert.equal(found.snapshotId, 'snap-001');
  });

  it('returns empty array when no audit file', async () => {
    const { getRecentAudit } = await import('../audit.js');
    // If audit path does not exist, should return []
    const entries = getRecentAudit(1);
    assert.ok(Array.isArray(entries));
  });
});

// ── CronHealer tests ───────────────────────────────────────────────────────────

describe('CronHealer', () => {
  it('returns dry-run result in dry-run mode (low errors)', async () => {
    const healer = new CronHealer(makeConfig());
    const result = await healer.heal({
      cronName: 'my-cron',
      consecutiveErrors: 2,
      lastError: 'some error',
      lastRun: new Date().toISOString(),
    });
    assert.ok(result.success);
    assert.ok(result.message.includes('my-cron'));
  });

  it('requests approval for 5+ consecutive errors (dry-run)', async () => {
    const healer = new CronHealer(makeConfig());
    const result = await healer.heal({
      cronName: 'bad-cron',
      consecutiveErrors: 6,
      lastError: 'persistent failure',
    });
    assert.ok(result.success);
    assert.equal(result.tier, 'yellow');
    assert.ok(result.message.includes('[DRY RUN]'));
  });

  it('requests approval with approvalOptions when not dry-run', async () => {
    const config = makeConfig({ dryRun: false });
    config.healers.cronRetry.dryRun = false;
    const healer = new CronHealer(config);
    const result = await healer.heal({
      cronName: 'bad-cron',
      consecutiveErrors: 7,
      lastError: 'network error',
    });
    assert.equal(result.tier, 'yellow');
    assert.equal(result.requiresApproval, true);
    assert.ok(Array.isArray(result.approvalOptions));
    assert.ok(result.approvalOptions!.length >= 3);
    const cbDatas = result.approvalOptions!.map(o => o.callbackData);
    assert.ok(cbDatas.some(d => d.startsWith('cron:retry')));
    assert.ok(cbDatas.some(d => d.startsWith('cron:disable')));
    assert.ok(cbDatas.some(d => d.startsWith('cron:ignore')));
  });

  it('uses green tier for transient errors below threshold (dry-run)', async () => {
    const healer = new CronHealer(makeConfig());
    const result = await healer.heal({
      cronName: 'network-cron',
      consecutiveErrors: 4,
      lastError: 'network timeout',
    });
    assert.equal(result.tier, 'green');
    assert.ok(result.message.includes('[DRY RUN]'));
  });
});

// ── AuthHealer tests ───────────────────────────────────────────────────────────

describe('AuthHealer', () => {
  it('returns dry-run result in dry-run mode', async () => {
    const healer = new AuthHealer(makeConfig());
    const result = await healer.heal({ provider: 'anthropic', count: 3 });
    assert.ok(result.success);
    assert.equal(result.tier, 'green');
    assert.ok(result.message.includes('[DRY RUN]'));
  });

  it('has correct healer name', () => {
    const healer = new AuthHealer(makeConfig());
    assert.equal(healer.name, 'AuthHealer');
  });
});

// ── SessionHealer tests ────────────────────────────────────────────────────────

describe('SessionHealer', () => {
  it('returns dry-run result for stuck session', async () => {
    const healer = new SessionHealer(makeConfig());
    const result = await healer.heal({
      agent: 'test-agent',
      session: 'session-001.jsonl',
      ageSec: 3 * 3600, // 3 hours = stuck
      sessionPath: '',
    });
    assert.ok(result.success);
    assert.equal(result.tier, 'green');
    assert.ok(result.message.includes('[DRY RUN]'));
    assert.ok(result.message.includes('stuck') || result.message.includes('180m') || result.message.includes('kill'));
  });

  it('requests approval for high-cost session (dry-run)', async () => {
    const healer = new SessionHealer(makeConfig());
    const result = await healer.heal({
      agent: 'expensive-agent',
      session: 'session-big.jsonl',
      ageSec: 1800,
      costUsd: 15.50,
    });
    assert.ok(result.success);
    assert.equal(result.tier, 'yellow');
    assert.ok(result.message.includes('[DRY RUN]'));
    assert.ok(result.message.includes('$15.50'));
  });

  it('requests approval with buttons when not dry-run for high cost', async () => {
    const config = makeConfig({ dryRun: false });
    config.healers.session.dryRun = false;
    const healer = new SessionHealer(config);
    const result = await healer.heal({
      agent: 'costly-agent',
      session: 'session-x.jsonl',
      ageSec: 600,
      costUsd: 12.00,
    });
    assert.equal(result.tier, 'yellow');
    assert.equal(result.requiresApproval, true);
    assert.ok(Array.isArray(result.approvalOptions));
    const cbDatas = result.approvalOptions!.map(o => o.callbackData);
    assert.ok(cbDatas.some(d => d.startsWith('session:kill')));
    assert.ok(cbDatas.some(d => d.startsWith('session:ignore')));
  });

  it('has correct healer name', () => {
    const healer = new SessionHealer(makeConfig());
    assert.equal(healer.name, 'SessionHealer');
  });
});

// ── TelegramAlerter inline keyboard tests ─────────────────────────────────────

describe('TelegramAlerter inline keyboard', () => {
  it('formatApprovalMessage returns correct structure', async () => {
    const { TelegramAlerter } = await import('../alerters/telegram.js');
    const config = makeConfig();
    const alerter = new TelegramAlerter(config);

    const options = [
      { text: 'Retry', callbackData: 'cron:retry:test' },
      { text: 'Disable', callbackData: 'cron:disable:test' },
    ];

    const { text, buttons } = alerter.formatApprovalMessage('CronWatcher', 'test issue', options);
    assert.ok(text.includes('CronWatcher'));
    assert.ok(text.includes('test issue'));
    assert.ok(Array.isArray(buttons));
    assert.equal(buttons.length, 1);
    assert.equal(buttons[0].length, 2);
    assert.equal(buttons[0][0].text, 'Retry');
    assert.equal(buttons[0][0].callback_data, 'cron:retry:test');
  });
});

after(() => {
  fs.rmSync(tmpDir, { recursive: true, force: true });
});
