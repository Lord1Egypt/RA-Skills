import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { gpuProbe } from '../src/probes/gpu.js';
import type { GpuProbeData } from '../src/types/index.js';

function parse(s: string): GpuProbeData {
  return gpuProbe.parse(s) as GpuProbeData;
}

describe('gpuProbe.parse', () => {
  it('returns available:false for empty output', () => {
    const data = parse('');
    assert.equal(data.probe, 'gpu');
    assert.equal(data.available, false);
    assert.deepEqual(data.gpus, []);
    assert.deepEqual(data.processes, []);
  });

  it('parses single GPU line', () => {
    const output = [
      '0, GPU-uuid-0, NVIDIA H100 80GB HBM3, 95, 70000, 81920, 72, 650, 535.183.06',
      '---SEPARATOR---',
      '',
      '---SEPARATOR---',
      '',
    ].join('\n');

    const data = parse(output);
    assert.equal(data.available, true);
    assert.equal(data.gpus.length, 1);

    const gpu = data.gpus[0]!;
    assert.equal(gpu.index, 0);
    assert.equal(gpu.name, 'NVIDIA H100 80GB HBM3');
    assert.equal(gpu.utilizationPct, 95);
    assert.equal(gpu.memoryUsedMiB, 70000);
    assert.equal(gpu.memoryTotalMiB, 81920);
    assert.equal(gpu.temperatureC, 72);
    assert.equal(gpu.powerW, 650);
  });

  it('parses multi-GPU output', () => {
    const output = [
      '0, GPU-uuid-0, NVIDIA A100, 80, 30000, 40960, 65, 250, 535.183.06',
      '1, GPU-uuid-1, NVIDIA A100, 10, 5000, 40960, 55, 100, 535.183.06',
      '2, GPU-uuid-2, NVIDIA A100, 0, 0, 40960, 40, 60, 535.183.06',
      '---SEPARATOR---',
      '',
      '---SEPARATOR---',
      '',
    ].join('\n');

    const data = parse(output);
    assert.equal(data.gpus.length, 3);
    assert.equal(data.gpus[0]!.utilizationPct, 80);
    assert.equal(data.gpus[1]!.utilizationPct, 10);
    assert.equal(data.gpus[2]!.utilizationPct, 0);
  });

  it('parses GPU processes with correct gpuIndex from UUID mapping', () => {
    const output = [
      '0, GPU-uuid-0, NVIDIA H100, 50, 20000, 81920, 60, 300, 535.183.06',
      '1, GPU-uuid-1, NVIDIA H100, 30, 10000, 81920, 55, 250, 535.183.06',
      '---SEPARATOR---',
      '1234, GPU-uuid-0, 15000, python',
      '5678, GPU-uuid-1, 8000, torchrun',
      '---SEPARATOR---',
      '1234|python /data/train.py --epochs 100',
      '5678|torchrun --nproc 8 train.py',
    ].join('\n');

    const data = parse(output);
    assert.equal(data.processes.length, 2);
    assert.equal(data.processes[0]!.pid, 1234);
    assert.equal(data.processes[0]!.gpuIndex, 0);
    assert.equal(data.processes[0]!.memoryMiB, 15000);
    assert.equal(data.processes[0]!.cmdline, 'python /data/train.py --epochs 100');
    assert.equal(data.processes[1]!.pid, 5678);
    assert.equal(data.processes[1]!.gpuIndex, 1);
    assert.equal(data.processes[1]!.cmdline, 'torchrun --nproc 8 train.py');
  });

  it('falls back to gpuIndex 0 for unknown UUID', () => {
    const output = [
      '0, GPU-uuid-0, NVIDIA H100, 50, 20000, 81920, 60, 300, 535.183.06',
      '---SEPARATOR---',
      '9999, UNKNOWN-UUID, 5000, mystery',
      '---SEPARATOR---',
      '',
    ].join('\n');

    const data = parse(output);
    assert.equal(data.processes.length, 1);
    assert.equal(data.processes[0]!.gpuIndex, 0); // fallback
  });

  it('computes memoryPct correctly', () => {
    const output = [
      '0, GPU-uuid-0, GPU, 50, 4096, 8192, 60, 100, 535.0',
      '---SEPARATOR---',
      '',
      '---SEPARATOR---',
      '',
    ].join('\n');

    const data = parse(output);
    assert.equal(data.gpus[0]!.memoryPct, 50); // 4096/8192 = 50%
  });

  it('handles malformed lines gracefully', () => {
    const output = [
      'some random text',
      '0, GPU-uuid-0, GPU, 50, 4000, 8000, 60, 100, 535.0',
      'incomplete, line',
      '---SEPARATOR---',
      'bad process line',
      '---SEPARATOR---',
      '',
    ].join('\n');

    const data = parse(output);
    assert.equal(data.available, true);
    assert.equal(data.gpus.length, 1);
  });
});
