// `ssh-lab status [host|all]` — GPU + disk + process overview via probes

import { execSsh } from '../ssh/exec.js';
import { withPool } from '../ssh/pool.js';
import { resolveHosts } from '../ssh/config.js';
import { defaultProbes } from '../probes/index.js';
import type { CommandResult, HostConfig, HostStatus, Alert, GpuProbeData, DiskProbeData, ProcessProbeData } from '../types/index.js';

/** Run all probes on a single host */
async function probeHost(host: HostConfig, timeoutMs: number): Promise<HostStatus> {
  const start = Date.now();
  const alerts: Alert[] = [];

  // Run all probes in parallel on the same host
  const probeResults = await Promise.allSettled(
    defaultProbes.map(async (probe) => {
      const result = await execSsh(host, probe.command, { timeoutMs });
      if (result.timedOut) {
        alerts.push({ level: 'error', host: host.alias, message: `Probe '${probe.name}' timed out` });
        return probe.parse('');
      }
      if (result.exitCode !== 0 && probe.name === 'gpu') {
        // GPU not available is normal (no NVIDIA GPU)
        return probe.parse('');
      }
      return probe.parse(result.stdout);
    })
  );

  const getData = (idx: number) => {
    const r = probeResults[idx];
    return r.status === 'fulfilled' ? r.value : null;
  };

  const gpu = (getData(0) as GpuProbeData) || { probe: 'gpu' as const, available: false, gpus: [], processes: [] };
  const disk = (getData(1) as DiskProbeData) || { probe: 'disk' as const, disks: [] };
  const proc = (getData(2) as ProcessProbeData) || { probe: 'process' as const, processes: [] };

  // Generate alerts from structured data
  if (gpu.available) {
    const allIdle = gpu.gpus.every((g) => g.utilizationPct < 5);
    if (allIdle && gpu.gpus.length > 0) {
      alerts.push({ level: 'info', host: host.alias, message: `All ${gpu.gpus.length} GPU(s) idle (<5% util)` });
    }

    for (const g of gpu.gpus) {
      if (g.temperatureC > 85) {
        alerts.push({ level: 'warn', host: host.alias, message: `GPU ${g.index} temp ${g.temperatureC}°C (>85°C)` });
      }
    }
  }

  for (const d of disk.disks) {
    if (d.usedPct >= 95) {
      alerts.push({ level: 'error', host: host.alias, message: `Disk ${d.mountpoint} at ${d.usedPct}% — CRITICAL` });
    } else if (d.usedPct >= 90) {
      alerts.push({ level: 'warn', host: host.alias, message: `Disk ${d.mountpoint} at ${d.usedPct}%` });
    }
  }

  return { host, gpu, disk, process: proc, alerts, durationMs: Date.now() - start };
}

/** Format a single host status into summary text */
function formatHostSummary(s: HostStatus): string {
  const lines: string[] = [`── ${s.host.alias} (${s.durationMs}ms) ──`];

  // GPU section
  if (s.gpu.available && s.gpu.gpus.length > 0) {
    for (const g of s.gpu.gpus) {
      const bar = makeBar(g.utilizationPct);
      lines.push(`  GPU ${g.index}: ${g.name} | ${bar} ${g.utilizationPct}% | VRAM ${g.memoryUsedMiB}/${g.memoryTotalMiB} MiB (${g.memoryPct}%) | ${g.temperatureC}°C | ${g.powerW}W`);
    }
    if (s.gpu.processes.length > 0) {
      for (const p of s.gpu.processes) {
        const cmd = p.cmdline || p.name;
        lines.push(`    └─ PID ${p.pid}: ${cmd} (${p.memoryMiB} MiB)`);
      }
    }
  } else {
    lines.push('  GPU: not available');
  }

  // Disk section
  if (s.disk.disks.length > 0) {
    const top = s.disk.disks.slice(0, 3); // Show top 3 by usage
    for (const d of top) {
      const warn = d.usedPct >= 90 ? ' ⚠️' : '';
      lines.push(`  Disk ${d.mountpoint}: ${d.used}/${d.size} (${d.usedPct}%) ${d.available} free${warn}`);
    }
  }

  // Process section
  if (s.process.processes.length > 0) {
    const top = s.process.processes.slice(0, 5);
    lines.push(`  Processes (${s.process.processes.length} active):`);
    for (const p of top) {
      lines.push(`    ${p.user} PID ${p.pid}: CPU ${p.cpuPct}% MEM ${p.memPct}% — ${truncate(p.command, 60)}`);
    }
  }

  // Alerts
  for (const a of s.alerts) {
    const icon = a.level === 'error' ? '🔴' : a.level === 'warn' ? '🟡' : '🔵';
    lines.push(`  ${icon} ${a.message}`);
  }

  return lines.join('\n');
}

function makeBar(pct: number, width = 10): string {
  const filled = Math.round((pct / 100) * width);
  return '█'.repeat(filled) + '░'.repeat(width - filled);
}

function truncate(s: string, max: number): string {
  return s.length > max ? s.slice(0, max - 3) + '...' : s;
}

export async function statusCommand(target: string, timeoutMs: number = 15000, options: { heartbeat?: boolean; quiet?: boolean; concurrency?: number } = {}): Promise<CommandResult<HostStatus[]>> {
  const start = Date.now();
  const hosts = resolveHosts(target);

  if (hosts.length === 0) {
    return {
      ok: false,
      command: 'status',
      summary: `No hosts found for target '${target}'`,
      error: { code: 'NO_HOSTS', message: `No hosts match '${target}'` },
      durationMs: Date.now() - start,
    };
  }

  // Probe all hosts with bounded concurrency
  const tasks = hosts.map((h) => () => probeHost(h, timeoutMs));
  const results = await withPool(tasks, options.concurrency ?? 5);

  const statuses: HostStatus[] = [];
  const errors: string[] = [];

  for (const r of results) {
    if (r.status === 'fulfilled') {
      statuses.push(r.value);
    } else {
      errors.push(String(r.reason));
    }
  }

  // Build aggregate summary
  const allAlerts = statuses.flatMap((s) => s.alerts);
  const totalGpus = statuses.reduce((n, s) => n + s.gpu.gpus.length, 0);
  const activeGpus = statuses.reduce((n, s) => n + s.gpu.gpus.filter((g) => g.utilizationPct >= 5).length, 0);

  const headerParts = [
    `${statuses.length}/${hosts.length} host(s) reachable`,
    totalGpus > 0 ? `${activeGpus}/${totalGpus} GPU(s) active` : null,
    allAlerts.length > 0 ? `${allAlerts.length} alert(s)` : null,
  ].filter(Boolean);

  // Heartbeat mode: one-liner if all OK, only expand anomalies
  let summary: string;
  if (options.heartbeat) {
    const anomalies = statuses.filter(
      (s) => s.alerts.some((a) => a.level === 'warn' || a.level === 'error'),
    );
    if (anomalies.length === 0 && errors.length === 0) {
      summary = `✓ ${statuses.length} hosts OK | ${activeGpus}/${totalGpus} GPU(s) active`;
    } else {
      const lines = [`⚠ ${anomalies.length} host(s) with issues:`];
      for (const s of anomalies) {
        lines.push(formatHostSummary(s));
      }
      for (const e of errors) {
        lines.push(`ERROR: ${e}`);
      }
      summary = lines.join('\n');
    }
  } else {
    summary = [
      headerParts.join(' | '),
      '',
      ...statuses.map(formatHostSummary),
      ...errors.map((e) => `ERROR: ${e}`),
    ].join('\n');
  }

  return {
    ok: errors.length === 0,
    command: 'status',
    data: statuses,
    summary,
    durationMs: Date.now() - start,
  };
}
