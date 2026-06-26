// `ssh-lab compare <host1> <host2> [--probes gpu,disk,process]`
// Side-by-side comparison of multiple hosts' probe data

import { execSsh } from '../ssh/exec.js';
import { resolveHosts } from '../ssh/config.js';
import { defaultProbes, getProbe } from '../probes/index.js';
import { withPool } from '../ssh/pool.js';
import type {
  CommandResult,
  HostConfig,
  Probe,
  ProbeData,
  GpuProbeData,
  DiskProbeData,
  ProcessProbeData,
} from '../types/index.js';

// ── Types ───────────────────────────────────────────────────

interface HostCompareData {
  host: string;
  reachable: boolean;
  probes: Record<string, ProbeData>;
  durationMs: number;
}

interface CompareResult {
  hosts: HostCompareData[];
  probesUsed: string[];
}

// ── Core ────────────────────────────────────────────────────

async function probeHostForCompare(
  host: HostConfig,
  probes: Probe[],
  timeoutMs: number,
): Promise<HostCompareData> {
  const start = Date.now();
  const probeMap: Record<string, ProbeData> = {};

  const results = await Promise.allSettled(
    probes.map(async (probe) => {
      const result = await execSsh(host, probe.command, { timeoutMs });
      if (result.timedOut || (result.exitCode !== 0 && probe.name !== 'gpu')) {
        return { name: probe.name, data: null };
      }
      return { name: probe.name, data: probe.parse(result.stdout) };
    }),
  );

  let reachable = false;
  for (const r of results) {
    if (r.status === 'fulfilled' && r.value.data) {
      probeMap[r.value.name] = r.value.data;
      reachable = true;
    }
  }

  return { host: host.alias, reachable, probes: probeMap, durationMs: Date.now() - start };
}

// ── Formatting ──────────────────────────────────────────────

function formatGpuRow(alias: string, gpu: GpuProbeData): string {
  if (!gpu.available || gpu.gpus.length === 0) return `  ${alias}: No GPUs`;
  return gpu.gpus
    .map(
      (g) =>
        `  ${alias} GPU${g.index}: ${g.name} | util ${g.utilizationPct}% | VRAM ${g.memoryUsedMiB}/${g.memoryTotalMiB} MiB | ${g.temperatureC}°C`,
    )
    .join('\n');
}

function formatDiskRow(alias: string, disk: DiskProbeData): string {
  if (disk.disks.length === 0) return `  ${alias}: No disk data`;
  return disk.disks
    .slice(0, 3)
    .map((d) => `  ${alias} ${d.mountpoint}: ${d.used}/${d.size} (${d.usedPct}%) ${d.available} free`)
    .join('\n');
}

function formatProcessRow(alias: string, proc: ProcessProbeData): string {
  if (proc.processes.length === 0) return `  ${alias}: No processes`;
  return proc.processes
    .slice(0, 3)
    .map((p) => `  ${alias} PID ${p.pid}: ${p.user} CPU ${p.cpuPct}% MEM ${p.memPct}%`)
    .join('\n');
}

function formatCompare(data: CompareResult): string {
  const lines: string[] = [`Compare — ${data.hosts.length} host(s) | probes: ${data.probesUsed.join(', ')}`];
  lines.push('');

  // Unreachable hosts
  const unreachable = data.hosts.filter((h) => !h.reachable);
  if (unreachable.length > 0) {
    for (const h of unreachable) {
      lines.push(`  ❌ ${h.host} [unreachable]`);
    }
    lines.push('');
  }

  const reachable = data.hosts.filter((h) => h.reachable);
  if (reachable.length === 0) {
    lines.push('  No reachable hosts to compare.');
    return lines.join('\n');
  }

  // Group by probe type for side-by-side comparison
  for (const probeName of data.probesUsed) {
    lines.push(`── ${probeName} ──`);
    for (const h of reachable) {
      const probeData = h.probes[probeName];
      if (!probeData) {
        lines.push(`  ${h.host}: [no data]`);
        continue;
      }
      switch (probeData.probe) {
        case 'gpu':
          lines.push(formatGpuRow(h.host, probeData));
          break;
        case 'disk':
          lines.push(formatDiskRow(h.host, probeData));
          break;
        case 'process':
          lines.push(formatProcessRow(h.host, probeData));
          break;
      }
    }
    lines.push('');
  }

  // Timing
  lines.push(
    `Timing: ${reachable.map((h) => `${h.host}=${h.durationMs}ms`).join(', ')}`,
  );

  return lines.join('\n');
}

// ── Command entry ───────────────────────────────────────────

export async function compareCommand(
  targets: string[],
  options: { probes?: string; timeoutMs?: number; maxConcurrency?: number } = {},
): Promise<CommandResult<CompareResult>> {
  const start = Date.now();

  // Resolve all target hosts
  const allHosts: HostConfig[] = [];
  for (const t of targets) {
    const resolved = resolveHosts(t);
    for (const h of resolved) {
      if (!allHosts.some((x) => x.alias === h.alias)) {
        allHosts.push(h);
      }
    }
  }

  if (allHosts.length < 1) {
    return {
      ok: false,
      command: 'compare',
      summary: 'No hosts found for the given targets',
      error: { code: 'NO_HOSTS', message: 'Specify at least one valid host' },
      durationMs: Date.now() - start,
    };
  }

  // Resolve probes
  const probeNames = options.probes
    ? options.probes.split(',').map((s) => s.trim())
    : defaultProbes.map((p) => p.name);

  const selectedProbes: Probe[] = [];
  for (const name of probeNames) {
    const probe = getProbe(name);
    if (probe) selectedProbes.push(probe);
  }

  if (selectedProbes.length === 0) {
    return {
      ok: false,
      command: 'compare',
      summary: `No valid probes found for: ${options.probes}`,
      error: { code: 'BAD_PROBES', message: `Unknown probe names: ${options.probes}` },
      durationMs: Date.now() - start,
    };
  }

  const timeoutMs = options.timeoutMs ?? 15_000;
  const max = options.maxConcurrency ?? 5;

  // Use pool for bounded concurrency
  const tasks = allHosts.map(
    (host) => () => probeHostForCompare(host, selectedProbes, timeoutMs),
  );
  const settled = await withPool(tasks, max);

  const hosts: HostCompareData[] = [];
  for (const r of settled) {
    if (r.status === 'fulfilled') {
      hosts.push(r.value);
    }
  }

  const result: CompareResult = {
    hosts,
    probesUsed: selectedProbes.map((p) => p.name),
  };

  return {
    ok: true,
    command: 'compare',
    data: result,
    summary: formatCompare(result),
    durationMs: Date.now() - start,
  };
}
