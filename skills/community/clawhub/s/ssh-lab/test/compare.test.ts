import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { getProbe, defaultProbes } from '../src/probes/index.js';

describe('compare support: probe registry', () => {
  it('defaultProbes contains gpu, disk, process', () => {
    const names = defaultProbes.map((p) => p.name);
    assert.ok(names.includes('gpu'), 'should include gpu probe');
    assert.ok(names.includes('disk'), 'should include disk probe');
    assert.ok(names.includes('process'), 'should include process probe');
  });

  it('getProbe returns probe by name', () => {
    const gpu = getProbe('gpu');
    assert.ok(gpu);
    assert.equal(gpu.name, 'gpu');
  });

  it('getProbe returns undefined for unknown probe', () => {
    const unknown = getProbe('nonexistent');
    assert.equal(unknown, undefined);
  });
});

describe('compare support: gpu probe parser', () => {
  const gpuProbe = getProbe('gpu')!;

  it('parses nvidia-smi CSV output', () => {
    const stdout = [
      '0, GPU-uuid-0, NVIDIA H100 80GB HBM3, 85, 40960, 81920, 72, 650, 535.183.06',
      '1, GPU-uuid-1, NVIDIA H100 80GB HBM3, 10, 1024, 81920, 55, 200, 535.183.06',
    ].join('\n');
    const data = gpuProbe.parse(stdout);
    assert.equal(data.probe, 'gpu');
    if (data.probe !== 'gpu') return;
    assert.equal(data.available, true);
    assert.equal(data.gpus.length, 2);
    assert.equal(data.gpus[0].utilizationPct, 85);
    assert.equal(data.gpus[1].temperatureC, 55);
  });

  it('marks unavailable when no output', () => {
    const data = gpuProbe.parse('');
    assert.equal(data.probe, 'gpu');
    if (data.probe !== 'gpu') return;
    assert.equal(data.available, false);
    assert.equal(data.gpus.length, 0);
  });
});

describe('compare support: disk probe parser', () => {
  const diskProbe = getProbe('disk')!;

  it('parses df output (sorted by usedPct desc)', () => {
    const stdout = [
      'Filesystem      Size  Used Avail Use% Mounted on',
      '/dev/sda1       916G  442G  428G  51% /',
      '/dev/nvme0n1    3.5T  2.1T  1.3T  62% /data',
    ].join('\n');
    const data = diskProbe.parse(stdout);
    assert.equal(data.probe, 'disk');
    if (data.probe !== 'disk') return;
    assert.equal(data.disks.length, 2);
    // Sorted descending by usedPct: 62% first, 51% second
    assert.equal(data.disks[0].usedPct, 62);
    assert.equal(data.disks[0].mountpoint, '/data');
    assert.equal(data.disks[1].usedPct, 51);
    assert.equal(data.disks[1].mountpoint, '/');
  });
});

describe('compare support: process probe parser', () => {
  const processProbe = getProbe('process')!;

  it('parses ps aux output and filters interesting processes', () => {
    // ps aux format: USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND
    const stdout = [
      'USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND',
      'root      1234 95.0  8.0 123456 78900 ?        Ssl  Jan01 100:00 python train.py',
      'user1     5678 50.0  4.0  99999 44444 ?        Sl   Jan01  50:00 torchrun --nproc 4',
      'root         1  0.0  0.0   1234   567 ?        Ss   Jan01   0:05 /sbin/init',
    ].join('\n');
    const data = processProbe.parse(stdout);
    assert.equal(data.probe, 'process');
    if (data.probe !== 'process') return;
    // python and torchrun match interesting patterns; init doesn't (0% CPU, no pattern match)
    assert.equal(data.processes.length, 2);
    assert.equal(data.processes[0].pid, 1234);
    assert.equal(data.processes[1].pid, 5678);
  });

  it('returns empty for non-matching processes', () => {
    const stdout = [
      'USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND',
      'root         1  0.0  0.0   1234   567 ?        Ss   Jan01   0:05 /sbin/init',
    ].join('\n');
    const data = processProbe.parse(stdout);
    assert.equal(data.probe, 'process');
    if (data.probe !== 'process') return;
    assert.equal(data.processes.length, 0);
  });
});
