import { describe, it, before, after } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'fs';
import path from 'path';
import os from 'os';
import { DEFAULT_CONFIG, ClawDoctorConfig } from '../config.js';
import { GatewayWatcher } from '../watchers/gateway.js';
import { CronWatcher } from '../watchers/cron.js';
import { SessionWatcher } from '../watchers/session.js';
import { CostWatcher } from '../watchers/cost.js';

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'clawdoctor-watchers-test-'));

function makeConfig(openclawPath = tmpDir): ClawDoctorConfig {
  return { ...DEFAULT_CONFIG, openclawPath };
}

describe('GatewayWatcher', () => {
  it('returns a WatchResult array', async () => {
    const watcher = new GatewayWatcher(makeConfig());
    const results = await watcher.check();
    assert.ok(Array.isArray(results));
    assert.ok(results.length >= 1);
    assert.ok('ok' in results[0]);
    assert.ok('severity' in results[0]);
    assert.ok('message' in results[0]);
  });

  it('result severity is valid', async () => {
    const watcher = new GatewayWatcher(makeConfig());
    const results = await watcher.check();
    const validSeverities = ['info', 'warning', 'error', 'critical'];
    for (const result of results) {
      assert.ok(validSeverities.includes(result.severity), `Invalid severity: ${result.severity}`);
    }
  });
});

describe('CronWatcher', () => {
  before(() => {
    fs.mkdirSync(path.join(tmpDir, 'cron'), { recursive: true });
  });

  it('returns ok when no cron files exist', async () => {
    const watcher = new CronWatcher(makeConfig());
    const results = await watcher.check();
    assert.ok(results.length >= 1);
    assert.ok(results.some(r => r.event_type === 'cron_no_file' || r.event_type === 'cron_none_enabled' || r.ok));
  });

  it('detects cron error state', async () => {
    const jobsFile = path.join(tmpDir, 'cron', 'jobs.json');
    fs.writeFileSync(jobsFile, JSON.stringify({
      version: 1,
      jobs: [{
        id: 'test-1',
        name: 'test-cron',
        enabled: true,
        schedule: { kind: 'cron', expr: '* * * * *' },
        state: {
          lastRunAtMs: Date.now(),
          lastRunStatus: 'error',
          consecutiveErrors: 3,
        },
      }],
    }));

    const watcher = new CronWatcher(makeConfig());
    const results = await watcher.check();
    const errorResult = results.find(r => r.event_type === 'cron_consecutive_errors');
    assert.ok(errorResult, `Expected cron_consecutive_errors, got: ${results.map(r => r.event_type).join(', ')}`);
    assert.equal(errorResult.severity, 'error');

    fs.unlinkSync(jobsFile);
  });

  it('detects overdue cron', async () => {
    const jobsFile = path.join(tmpDir, 'cron', 'jobs.json');
    const twoHoursAgo = Date.now() - 2 * 3600 * 1000;
    fs.writeFileSync(jobsFile, JSON.stringify({
      version: 1,
      jobs: [{
        id: 'test-2',
        name: 'overdue-cron',
        enabled: true,
        schedule: { kind: 'cron', expr: '*/5 * * * *' },
        state: {
          nextRunAtMs: twoHoursAgo,
          lastRunAtMs: twoHoursAgo - 300000,
          lastRunStatus: 'ok',
          consecutiveErrors: 0,
        },
      }],
    }));

    const watcher = new CronWatcher(makeConfig());
    const results = await watcher.check();
    const overdueResult = results.find(r => r.event_type === 'cron_overdue');
    assert.ok(overdueResult, `Expected cron_overdue, got: ${results.map(r => r.event_type).join(', ')}`);

    fs.unlinkSync(jobsFile);
  });

  it('passes healthy cron', async () => {
    const jobsFile = path.join(tmpDir, 'cron', 'jobs.json');
    fs.writeFileSync(jobsFile, JSON.stringify({
      version: 1,
      jobs: [{
        id: 'test-3',
        name: 'healthy-cron',
        enabled: true,
        schedule: { kind: 'cron', expr: '0 * * * *' },
        state: {
          nextRunAtMs: Date.now() + 3600000,
          lastRunAtMs: Date.now() - 1800000,
          lastRunStatus: 'ok',
          consecutiveErrors: 0,
          lastDeliveryStatus: 'delivered',
        },
      }],
    }));

    const watcher = new CronWatcher(makeConfig());
    const results = await watcher.check();
    const okResult = results.find(r => r.event_type === 'cron_all_ok');
    assert.ok(okResult, `Expected cron_all_ok, got: ${results.map(r => r.event_type + ':' + r.message).join(', ')}`);

    fs.unlinkSync(jobsFile);
  });
});

describe('SessionWatcher', () => {
  before(() => {
    fs.mkdirSync(path.join(tmpDir, 'agents', 'test-agent', 'sessions'), { recursive: true });
  });

  it('returns ok when no recent sessions', async () => {
    const watcher = new SessionWatcher(makeConfig());
    const results = await watcher.check();
    assert.ok(results.length >= 1);
    assert.ok(results.some(r => r.ok));
  });

  it('detects session errors', async () => {
    const sessionFile = path.join(tmpDir, 'agents', 'test-agent', 'sessions', 'session-err.jsonl');
    const entries = [
      { type: 'start', timestamp: new Date().toISOString() },
      { type: 'error', error: 'API rate limit exceeded', timestamp: new Date().toISOString() },
    ];
    fs.writeFileSync(sessionFile, entries.map(e => JSON.stringify(e)).join('\n'));

    const watcher = new SessionWatcher(makeConfig());
    const results = await watcher.check();
    const errorResult = results.find(r => r.event_type === 'session_error');
    assert.ok(errorResult, `Expected session_error, got: ${results.map(r => r.event_type).join(', ')}`);

    fs.unlinkSync(sessionFile);
  });

  it('detects aborted sessions', async () => {
    const sessionFile = path.join(tmpDir, 'agents', 'test-agent', 'sessions', 'session-abort.jsonl');
    const entries = [
      { type: 'start', timestamp: new Date().toISOString() },
      { status: 'aborted', timestamp: new Date().toISOString() },
    ];
    fs.writeFileSync(sessionFile, entries.map(e => JSON.stringify(e)).join('\n'));

    const watcher = new SessionWatcher(makeConfig());
    const results = await watcher.check();
    const abortResult = results.find(r => r.event_type === 'session_aborted');
    assert.ok(abortResult, `Expected session_aborted, got: ${results.map(r => r.event_type).join(', ')}`);

    fs.unlinkSync(sessionFile);
  });
});

describe('CostWatcher', () => {
  before(() => {
    fs.mkdirSync(path.join(tmpDir, 'agents', 'cost-agent', 'sessions'), { recursive: true });
  });

  it('returns ok with no sessions', async () => {
    const watcher = new CostWatcher(makeConfig());
    const results = await watcher.check();
    assert.ok(results.length >= 1);
    assert.ok(results.some(r => r.ok));
  });

  it('detects cost anomaly', async () => {
    const sessionsDir = path.join(tmpDir, 'agents', 'cost-agent', 'sessions');

    // Create 5 cheap historical sessions (mtime well in the past)
    for (let i = 0; i < 5; i++) {
      const file = path.join(sessionsDir, `session-cheap-${i}.jsonl`);
      const entry = { usage: { input_tokens: 100, output_tokens: 50, cost_usd: 0.001 } };
      fs.writeFileSync(file, JSON.stringify(entry));
      // Backdate mtime to 2 hours ago
      const t = new Date(Date.now() - 2 * 3600 * 1000);
      fs.utimesSync(file, t, t);
    }

    // Create one very expensive recent session
    const expensiveFile = path.join(sessionsDir, 'session-expensive.jsonl');
    fs.writeFileSync(expensiveFile, JSON.stringify({ usage: { cost_usd: 10.0 } }));
    // Leave mtime as now (recent)

    const watcher = new CostWatcher(makeConfig());
    const results = await watcher.check();
    const anomaly = results.find(r => r.event_type === 'cost_anomaly');
    assert.ok(anomaly, `Expected cost_anomaly, got: ${results.map(r => r.event_type + ':' + r.message).join(', ')}`);

    // Cleanup
    fs.readdirSync(sessionsDir).forEach(f => fs.unlinkSync(path.join(sessionsDir, f)));
  });
});

after(() => {
  fs.rmSync(tmpDir, { recursive: true, force: true });
});
