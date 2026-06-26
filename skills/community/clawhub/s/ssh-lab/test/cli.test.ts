import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { parseArgs, getOutputMode } from '../src/cli.js';
import { TIMEOUT_TIERS } from '../src/ssh/exec.js';

describe('parseArgs', () => {
  const p = (args: string[]) => parseArgs(['node', 'ssh-lab', ...args]);

  it('parses empty args', () => {
    const r = p([]);
    assert.equal(r.command, '');
    assert.deepEqual(r.positional, []);
    assert.deepEqual(r.flags, {});
  });

  it('parses command only', () => {
    const r = p(['hosts']);
    assert.equal(r.command, 'hosts');
  });

  it('parses command with positionals', () => {
    const r = p(['run', 'GMI4', 'nvidia-smi']);
    assert.equal(r.command, 'run');
    assert.deepEqual(r.positional, ['GMI4', 'nvidia-smi']);
  });

  it('parses --flag value', () => {
    const r = p(['status', '--timeout', '5000']);
    assert.equal(r.flags.timeout, '5000');
  });

  it('parses --flag=value', () => {
    const r = p(['ls', 'GMI4', '/data', '--sort=size']);
    assert.equal(r.flags.sort, 'size');
  });

  it('parses boolean flags', () => {
    const r = p(['status', '--json', '--heartbeat']);
    assert.equal(r.flags.json, true);
    assert.equal(r.flags.heartbeat, true);
  });

  it('parses short flags -j -r -q', () => {
    assert.equal(p(['-j']).flags.json, true);
    assert.equal(p(['-r']).flags.raw, true);
    assert.equal(p(['-q']).flags.quiet, true);
  });

  it('parses -n with value', () => {
    const r = p(['tail', 'GMI4', '/log', '-n', '100']);
    assert.equal(r.flags.n, '100');
  });

  it('parses --help flag', () => {
    const r = p(['--help']);
    assert.equal(r.flags.help, true);
  });

  it('handles mixed flags and positionals', () => {
    const r = p(['compare', 'GMI4', 'GMI5', '--json', '--probes', 'gpu,disk']);
    assert.equal(r.command, 'compare');
    assert.deepEqual(r.positional, ['GMI4', 'GMI5']);
    assert.equal(r.flags.json, true);
    assert.equal(r.flags.probes, 'gpu,disk');
  });

  it('handles --flag at end as boolean', () => {
    const r = p(['df', 'all', '--json']);
    assert.equal(r.flags.json, true);
    assert.equal(r.command, 'df');
    assert.deepEqual(r.positional, ['all']);
  });
});

describe('getOutputMode', () => {
  it('returns json for --json flag', () => {
    assert.equal(getOutputMode({ json: true }), 'json');
  });

  it('returns raw for --raw flag', () => {
    assert.equal(getOutputMode({ raw: true }), 'raw');
  });

  it('returns summary by default', () => {
    assert.equal(getOutputMode({}), 'summary');
  });

  it('respects --output flag', () => {
    assert.equal(getOutputMode({ output: 'json' }), 'json');
  });
});

describe('TIMEOUT_TIERS', () => {
  it('has correct tier values', () => {
    assert.equal(TIMEOUT_TIERS.quick, 5_000);
    assert.equal(TIMEOUT_TIERS.standard, 15_000);
    assert.equal(TIMEOUT_TIERS.stream, 30_000);
    assert.equal(TIMEOUT_TIERS.transfer, 60_000);
  });

  it('covers all four expected tiers', () => {
    const keys = Object.keys(TIMEOUT_TIERS).sort();
    assert.deepEqual(keys, ['quick', 'standard', 'stream', 'transfer']);
  });
});
