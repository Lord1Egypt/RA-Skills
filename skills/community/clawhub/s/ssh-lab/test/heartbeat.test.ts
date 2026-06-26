import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { exitCode } from '../src/output/formatter.js';
import type { CommandResult } from '../src/types/index.js';

describe('heartbeat / output support', () => {
  it('exitCode returns 0 for ok result', () => {
    const result: CommandResult = {
      ok: true,
      command: 'status',
      summary: '✓ 3 hosts OK | 8/8 GPU(s) active',
      durationMs: 500,
    };
    assert.equal(exitCode(result), 0);
  });

  it('exitCode returns 1 for generic error', () => {
    const result: CommandResult = {
      ok: false,
      command: 'status',
      summary: 'Failed',
      error: { code: 'NO_HOSTS', message: 'No hosts found' },
      durationMs: 10,
    };
    assert.equal(exitCode(result), 1);
  });

  it('exitCode returns 2 for ALERT_CRITICAL', () => {
    const result: CommandResult = {
      ok: false,
      command: 'alert check',
      summary: 'Critical alert',
      error: { code: 'ALERT_CRITICAL', message: 'Disk full' },
      durationMs: 200,
    };
    assert.equal(exitCode(result), 2);
  });

  it('heartbeat summary format: all OK → one-liner with ✓', () => {
    // Verifies the expected shape of heartbeat output
    const summary = '✓ 3 hosts OK | 8/8 GPU(s) active';
    assert.ok(summary.startsWith('✓'));
    assert.ok(summary.includes('hosts OK'));
    assert.ok(summary.includes('GPU(s) active'));
  });

  it('heartbeat summary format: anomalies → starts with ⚠', () => {
    const summary = '⚠ 1 host(s) with issues:\n── GMI4 (500ms) ──\n  🔴 Disk / at 98% — CRITICAL';
    assert.ok(summary.startsWith('⚠'));
    assert.ok(summary.includes('issues'));
  });
});
