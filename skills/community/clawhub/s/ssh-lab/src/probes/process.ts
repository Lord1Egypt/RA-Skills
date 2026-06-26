// Process probe — parses `ps aux` output, filters to interesting processes

import type { Probe, ProcessProbeData, ProcessInfo } from '../types/index.js';

// Get processes sorted by CPU usage, filter to interesting ones (python, training, etc)
// Use pipe sort instead of ps --sort for macOS compatibility (macOS ps doesn't support --sort)
const PROCESS_COMMAND = "ps aux | sort -k3 -rn | head -30";

// Patterns that indicate interesting (training/compute) processes
const INTERESTING_PATTERNS = [
  /python/i,
  /torch/i,
  /train/i,
  /deepspeed/i,
  /accelerate/i,
  /nccl/i,
  /ray/i,
  /vllm/i,
  /tgi/i,
  /ollama/i,
  /jupyter/i,
  /tensorboard/i,
  /wandb/i,
  /docker/i,
  /singularity/i,
];

function isInteresting(command: string): boolean {
  return INTERESTING_PATTERNS.some((p) => p.test(command));
}

function parsePsLine(line: string): ProcessInfo | null {
  // ps aux format: USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND
  const parts = line.trim().split(/\s+/);
  if (parts.length < 11) return null;

  const pid = parseInt(parts[1], 10);
  if (isNaN(pid)) return null;

  const cpuPct = parseFloat(parts[2]);
  const memPct = parseFloat(parts[3]);
  const command = parts.slice(10).join(' ');

  return {
    pid,
    user: parts[0],
    cpuPct: isNaN(cpuPct) ? 0 : cpuPct,
    memPct: isNaN(memPct) ? 0 : memPct,
    vsz: parts[4],
    rss: parts[5],
    command,
  };
}

export const processProbe: Probe = {
  name: 'process',
  command: PROCESS_COMMAND,

  parse(stdout: string): ProcessProbeData {
    const processes: ProcessInfo[] = [];

    for (const line of stdout.split('\n')) {
      const proc = parsePsLine(line);
      if (!proc) continue;
      // Include processes using significant CPU, or matching interesting patterns
      if (proc.cpuPct >= 1.0 || isInteresting(proc.command)) {
        processes.push(proc);
      }
    }

    return { probe: 'process', processes };
  },
};
