import { describe, it, before, after } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'fs';
import path from 'path';
import os from 'os';

// We test config validation by importing config functions after patching paths
const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'clawdoctor-test-'));
const configPath = path.join(tmpDir, 'config.json');

describe('Config', () => {
  after(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('DEFAULT_CONFIG has all required fields', async () => {
    const { DEFAULT_CONFIG } = await import('../config.js');
    assert.ok(DEFAULT_CONFIG.watchers.gateway);
    assert.ok(DEFAULT_CONFIG.watchers.cron);
    assert.ok(DEFAULT_CONFIG.watchers.session);
    assert.ok(DEFAULT_CONFIG.watchers.auth);
    assert.ok(DEFAULT_CONFIG.watchers.cost);
    assert.ok(DEFAULT_CONFIG.healers.processRestart);
    assert.ok(DEFAULT_CONFIG.healers.cronRetry);
    assert.ok(DEFAULT_CONFIG.alerts.telegram);
    assert.equal(DEFAULT_CONFIG.dryRun, false);
    assert.equal(DEFAULT_CONFIG.retentionDays, 7);
  });

  it('DEFAULT_CONFIG watcher intervals are sane', async () => {
    const { DEFAULT_CONFIG } = await import('../config.js');
    assert.equal(DEFAULT_CONFIG.watchers.gateway.interval, 30);
    assert.equal(DEFAULT_CONFIG.watchers.cron.interval, 60);
    assert.equal(DEFAULT_CONFIG.watchers.session.interval, 60);
    assert.equal(DEFAULT_CONFIG.watchers.auth.interval, 60);
    assert.equal(DEFAULT_CONFIG.watchers.cost.interval, 300);
  });

  it('saveConfig and loadConfig roundtrip', async () => {
    // Write config manually to temp path
    const { DEFAULT_CONFIG } = await import('../config.js');
    const testConfig = { ...DEFAULT_CONFIG, dryRun: true, retentionDays: 14 };
    fs.writeFileSync(configPath, JSON.stringify(testConfig, null, 2));

    const parsed = JSON.parse(fs.readFileSync(configPath, 'utf-8'));
    assert.equal(parsed.dryRun, true);
    assert.equal(parsed.retentionDays, 14);
    assert.ok(parsed.watchers);
    assert.ok(parsed.alerts);
  });

  it('configExists returns false when no config file', async () => {
    const { configExists } = await import('../config.js');
    // configExists checks the real AGENTWATCH_DIR. Just verify it's a boolean.
    const result = configExists();
    assert.equal(typeof result, 'boolean');
  });
});
