import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import { evaluateAlerts } from '../src/alerts/rules.js';
import { addRule, loadRules, saveRules } from '../src/alerts/state.js';
import type { HostStatusData, HostConfig, GpuInfo, DiskInfo, ProcessInfo } from '../src/types/index.js';

function makeHost(alias = 'test-host'): HostConfig {
  return { alias, hostname: alias, source: 'ssh-config', tags: [] };
}

function makeGpu(overrides: Partial<GpuInfo> = {}): GpuInfo {
  return {
    index: 0, name: 'H100', utilizationPct: 95,
    memoryUsedMiB: 70000, memoryTotalMiB: 81920, memoryPct: 85,
    temperatureC: 65, powerW: 650,
    ...overrides,
  };
}

function makeDisk(overrides: Partial<DiskInfo> = {}): DiskInfo {
  return {
    filesystem: '/dev/sda1', size: '1T', used: '500G',
    available: '500G', usedPct: 50, mountpoint: '/',
    ...overrides,
  };
}

function makeProcess(overrides: Partial<ProcessInfo> = {}): ProcessInfo {
  return {
    pid: 1234, user: 'root', cpuPct: 10, memPct: 5,
    vsz: '1000000', rss: '500000', command: 'python train.py',
    ...overrides,
  };
}

function makeStatus(overrides: Partial<HostStatusData> = {}): HostStatusData {
  return {
    host: makeHost(),
    gpu: [makeGpu()],
    disk: [makeDisk()],
    processes: [makeProcess()],
    collectorErrors: [],
    ...overrides,
  };
}

describe('evaluateAlerts', () => {
  // Save and restore rules around each test
  let originalRules: unknown[];
  beforeEach(() => {
    originalRules = loadRules();
    saveRules([]);
  });
  afterEach(() => {
    saveRules(originalRules as any);
  });

  it('returns empty firings when no rules configured', () => {
    const result = evaluateAlerts(makeStatus());
    assert.equal(result.host, 'test-host');
    assert.equal(result.firings.length, 0);
  });

  it('detects disk_full when threshold exceeded', () => {
    addRule({ kind: 'disk_full', host: 'all', threshold: 90 });
    const status = makeStatus({ disk: [makeDisk({ usedPct: 92 })] });
    const result = evaluateAlerts(status);
    assert.equal(result.firings.length, 1);
    assert.equal(result.firings[0]!.kind, 'disk_full');
    assert.equal(result.firings[0]!.level, 'warning');
  });

  it('detects disk_full critical at 95%+', () => {
    addRule({ kind: 'disk_full', host: 'all', threshold: 90 });
    const status = makeStatus({ disk: [makeDisk({ usedPct: 97 })] });
    const result = evaluateAlerts(status);
    assert.equal(result.firings[0]!.level, 'critical');
  });

  it('detects gpu_idle when VRAM loaded but util low', () => {
    addRule({ kind: 'gpu_idle', host: 'all' });
    const status = makeStatus({
      gpu: [makeGpu({ utilizationPct: 0, memoryUsedMiB: 60000 })],
    });
    const result = evaluateAlerts(status);
    assert.equal(result.firings.length, 1);
    assert.equal(result.firings[0]!.kind, 'gpu_idle');
  });

  it('no gpu_idle when util is active', () => {
    addRule({ kind: 'gpu_idle', host: 'all' });
    const status = makeStatus({
      gpu: [makeGpu({ utilizationPct: 80, memoryUsedMiB: 60000 })],
    });
    const result = evaluateAlerts(status);
    assert.equal(result.firings.length, 0);
  });

  it('detects process_died when pattern not found', () => {
    addRule({ kind: 'process_died', host: 'all', processPattern: 'torchrun' });
    const status = makeStatus({
      processes: [makeProcess({ command: 'sleep 1000' })],
    });
    const result = evaluateAlerts(status);
    assert.equal(result.firings.length, 1);
    assert.equal(result.firings[0]!.level, 'critical');
  });

  it('no process_died when pattern is found', () => {
    addRule({ kind: 'process_died', host: 'all', processPattern: 'torchrun' });
    const status = makeStatus({
      processes: [makeProcess({ command: 'torchrun --nproc 8 train.py' })],
    });
    const result = evaluateAlerts(status);
    assert.equal(result.firings.length, 0);
  });

  it('detects high_temp', () => {
    addRule({ kind: 'high_temp', host: 'all', threshold: 80 });
    const status = makeStatus({
      gpu: [makeGpu({ temperatureC: 88 })],
    });
    const result = evaluateAlerts(status);
    assert.equal(result.firings.length, 1);
    assert.equal(result.firings[0]!.kind, 'high_temp');
  });

  it('respects host-specific rules', () => {
    addRule({ kind: 'disk_full', host: 'other-host', threshold: 50 });
    const status = makeStatus({ disk: [makeDisk({ usedPct: 70 })] });
    const result = evaluateAlerts(status);
    // Rule targets 'other-host', not 'test-host'
    assert.equal(result.firings.length, 0);
  });
});
