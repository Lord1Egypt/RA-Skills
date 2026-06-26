// GPU probe — parses nvidia-smi CSV output + compute process list

import type { Probe, GpuProbeData, GpuInfo, GpuProcess } from '../types/index.js';

const GPU_QUERY_FIELDS = [
  'index',
  'uuid',
  'name',
  'utilization.gpu',
  'memory.used',
  'memory.total',
  'temperature.gpu',
  'power.draw',
  'driver_version',
].join(',');

// Two commands in one: GPU stats + compute processes with full cmdline
// Use ; instead of && so partial failures don't kill subsequent commands
const GPU_COMMAND = [
  `nvidia-smi --query-gpu=${GPU_QUERY_FIELDS} --format=csv,noheader,nounits 2>/dev/null`,
  `echo "---SEPARATOR---"`,
  `nvidia-smi --query-compute-apps=pid,gpu_uuid,used_gpu_memory,process_name --format=csv,noheader,nounits 2>/dev/null`,
  `echo "---SEPARATOR---"`,
  // Get full cmdline for running GPU processes
  `nvidia-smi --query-compute-apps=pid --format=csv,noheader,nounits 2>/dev/null | xargs -I{} sh -c 'echo "{}|$(cat /proc/{}/cmdline 2>/dev/null | tr "\\0" " " || ps -p {} -o args= 2>/dev/null)"'`,
].join('; ');

function parseNum(s: string): number {
  const n = parseFloat(s.trim());
  return isNaN(n) ? 0 : n;
}

function parseGpuLines(output: string): { gpus: GpuInfo[]; uuidToIndex: Map<string, number>; driverVersion: string } {
  const gpus: GpuInfo[] = [];
  const uuidToIndex = new Map<string, number>();
  let driverVersion = '';

  for (const line of output.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    const parts = trimmed.split(',').map((s) => s.trim());
    if (parts.length < 8) continue;

    const index = parseInt(parts[0], 10);
    const uuid = parts[1];
    const memUsed = parseNum(parts[4]);
    const memTotal = parseNum(parts[5]);
    driverVersion = parts[8] || driverVersion;

    if (uuid) uuidToIndex.set(uuid, index);

    gpus.push({
      index,
      name: parts[2],
      utilizationPct: parseNum(parts[3]),
      memoryUsedMiB: memUsed,
      memoryTotalMiB: memTotal,
      memoryPct: memTotal > 0 ? Math.round((memUsed / memTotal) * 1000) / 10 : 0,
      temperatureC: parseNum(parts[6]),
      powerW: parseNum(parts[7]),
    });
  }

  return { gpus, uuidToIndex, driverVersion };
}

function parseProcessLines(processOutput: string, cmdlineOutput: string, uuidToIndex: Map<string, number>): GpuProcess[] {
  const processes: GpuProcess[] = [];
  const cmdlineMap = new Map<number, string>();

  // Parse cmdline output: "pid|full command line"
  for (const line of cmdlineOutput.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    const pipeIdx = trimmed.indexOf('|');
    if (pipeIdx > 0) {
      const pid = parseInt(trimmed.slice(0, pipeIdx), 10);
      const cmdline = trimmed.slice(pipeIdx + 1).trim();
      if (!isNaN(pid) && cmdline) cmdlineMap.set(pid, cmdline);
    }
  }

  for (const line of processOutput.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    const parts = trimmed.split(',').map((s) => s.trim());
    if (parts.length < 4) continue;

    const pid = parseInt(parts[0], 10);
    if (isNaN(pid)) continue;

    const gpuUuid = parts[1];
    const gpuIndex = uuidToIndex.get(gpuUuid) ?? 0;

    processes.push({
      pid,
      gpuIndex,
      memoryMiB: parseNum(parts[2]),
      name: parts[3],
      cmdline: cmdlineMap.get(pid),
    });
  }

  return processes;
}

export const gpuProbe: Probe = {
  name: 'gpu',
  command: GPU_COMMAND,

  parse(stdout: string): GpuProbeData {
    const sections = stdout.split('---SEPARATOR---');

    if (!sections[0] || sections[0].trim() === '') {
      return { probe: 'gpu', available: false, gpus: [], processes: [] };
    }

    const { gpus, uuidToIndex, driverVersion } = parseGpuLines(sections[0]);
    const processes = parseProcessLines(sections[1] || '', sections[2] || '', uuidToIndex);

    return {
      probe: 'gpu',
      available: true,
      driverVersion,
      gpus,
      processes,
    };
  },
};
