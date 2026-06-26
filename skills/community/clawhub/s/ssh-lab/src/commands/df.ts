// `ssh-lab df <host> [path]` — standalone disk usage command

import { execSsh } from '../ssh/exec.js';
import { resolveHosts } from '../ssh/config.js';
import type { CommandResult, DiskInfo, DiskProbeData } from '../types/index.js';
import { diskProbe } from '../probes/disk.js';

interface DfData {
  host: string;
  disks: DiskInfo[];
  /** Optional: du -sh output for a specific path */
  pathUsage?: string;
}

export async function dfCommand(
  target: string,
  path?: string,
  timeoutMs: number = 15000
): Promise<CommandResult<DfData | DfData[]>> {
  const start = Date.now();
  const hosts = resolveHosts(target);

  if (hosts.length === 0) {
    return {
      ok: false, command: 'df',
      summary: `No hosts found for '${target}'`,
      error: { code: 'NO_HOSTS', message: `No hosts match '${target}'` },
      durationMs: Date.now() - start,
    };
  }

  const results = await Promise.allSettled(
    hosts.map(async (host): Promise<DfData> => {
      // Always get df output
      const dfResult = await execSsh(host, diskProbe.command, { timeoutMs });
      const diskData = diskProbe.parse(dfResult.stdout) as DiskProbeData;

      let pathUsage: string | undefined;
      if (path) {
        const duResult = await execSsh(host, `du -sh ${shellEscape(path)} 2>&1`, { timeoutMs });
        pathUsage = duResult.stdout;
      }

      return {
        host: host.alias,
        disks: diskData.disks,
        pathUsage,
      };
    })
  );

  const data: DfData[] = [];
  const errors: string[] = [];

  for (const r of results) {
    if (r.status === 'fulfilled') data.push(r.value);
    else errors.push(String(r.reason));
  }

  const summaryLines = data.flatMap((d) => {
    const lines = [`── ${d.host} ──`];
    for (const disk of d.disks) {
      const bar = makeBar(disk.usedPct);
      const warn = disk.usedPct >= 90 ? ' ⚠️' : '';
      lines.push(`  ${disk.mountpoint.padEnd(20)} ${bar} ${disk.usedPct}% | ${disk.used}/${disk.size} (${disk.available} free)${warn}`);
    }
    if (d.pathUsage) {
      lines.push(`  Path: ${d.pathUsage}`);
    }
    return lines;
  });

  return {
    ok: errors.length === 0,
    command: 'df',
    data: data.length === 1 ? data[0] : data,
    summary: summaryLines.join('\n'),
    durationMs: Date.now() - start,
  };
}

function makeBar(pct: number, width = 10): string {
  const filled = Math.round((pct / 100) * width);
  return '█'.repeat(filled) + '░'.repeat(width - filled);
}

function shellEscape(s: string): string {
  return "'" + s.replace(/'/g, "'\\''") + "'";
}
