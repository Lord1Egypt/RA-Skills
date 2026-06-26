import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { classifySshError } from '../src/ssh/exec.js';
import type { SshExecResult } from '../src/types/index.js';

function makeResult(overrides: Partial<SshExecResult>): SshExecResult {
  return {
    host: 'test',
    command: 'echo test',
    stdout: '',
    stderr: '',
    exitCode: 0,
    durationMs: 100,
    timedOut: false,
    ...overrides,
  };
}

describe('classifySshError', () => {
  it('returns null for exit code 0', () => {
    assert.equal(classifySshError(makeResult({ exitCode: 0 })), null);
  });

  it('classifies timeout', () => {
    const err = classifySshError(makeResult({ timedOut: true, exitCode: null }));
    assert.ok(err);
    assert.equal(err.code, 'TIMEOUT');
    assert.equal(err.retryable, true);
  });

  it('classifies auth failure', () => {
    const err = classifySshError(makeResult({ exitCode: 255, stderr: 'Permission denied (publickey).' }));
    assert.ok(err);
    assert.equal(err.code, 'AUTH_FAILED');
    assert.equal(err.retryable, false);
  });

  it('classifies connection refused', () => {
    const err = classifySshError(makeResult({ exitCode: 255, stderr: 'ssh: connect to host: Connection refused' }));
    assert.ok(err);
    assert.equal(err.code, 'CONNECTION_REFUSED');
    assert.equal(err.retryable, true);
  });

  it('classifies unreachable', () => {
    const err = classifySshError(makeResult({ exitCode: 255, stderr: 'No route to host' }));
    assert.ok(err);
    assert.equal(err.code, 'HOST_UNREACHABLE');
    assert.equal(err.retryable, true);
  });

  it('classifies command failure', () => {
    const err = classifySshError(makeResult({ exitCode: 1, stderr: 'some error' }));
    assert.ok(err);
    assert.equal(err.code, 'COMMAND_FAILED');
    assert.equal(err.retryable, false);
  });

  it('classifies unknown SSH error', () => {
    const err = classifySshError(makeResult({ exitCode: 255, stderr: 'some weird SSH error' }));
    assert.ok(err);
    assert.equal(err.code, 'UNKNOWN');
    assert.equal(err.retryable, true);
  });
});
