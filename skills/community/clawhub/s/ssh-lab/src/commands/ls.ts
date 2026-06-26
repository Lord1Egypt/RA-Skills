// `ssh-lab ls <host> <path>` — remote directory listing with sorting

import { execSsh } from '../ssh/exec.js';
import { resolveHost } from '../ssh/config.js';
import type { CommandResult } from '../types/index.js';

export interface RemoteFileEntry {
  name: string;
  size: string;
  sizeBytes: number;
  modified: string;
  permissions: string;
  owner: string;
  isDirectory: boolean;
}

interface LsData {
  host: string;
  path: string;
  entries: RemoteFileEntry[];
}

/** Parse `ls -lh --time-style=long-iso` output into structured entries */
function parseLsLine(line: string): RemoteFileEntry | null {
  // Format: drwxr-xr-x 2 user group 4.0K 2026-03-10 12:00 dirname
  const trimmed = line.trim();
  if (!trimmed || trimmed.startsWith('total ')) return null;

  const parts = trimmed.split(/\s+/);
  if (parts.length < 8) return null;

  const permissions = parts[0];
  const owner = parts[2];
  const size = parts[4];
  // With --time-style=long-iso: date is parts[5], time is parts[6], name is parts[7+]
  const modified = `${parts[5]} ${parts[6]}`;
  const name = parts.slice(7).join(' ');

  if (!name) return null;

  return {
    name,
    size,
    sizeBytes: parseSizeToBytes(size),
    modified,
    permissions,
    owner,
    isDirectory: permissions.startsWith('d'),
  };
}

function parseSizeToBytes(size: string): number {
  const match = size.match(/^([\d.]+)([KMGTP]?)$/i);
  if (!match) return 0;
  const num = parseFloat(match[1]);
  const unit = match[2].toUpperCase();
  const multipliers: Record<string, number> = { '': 1, K: 1024, M: 1048576, G: 1073741824, T: 1099511627776 };
  return Math.round(num * (multipliers[unit] || 1));
}

export async function lsCommand(
  hostAlias: string,
  remotePath: string,
  sort: 'time' | 'size' | 'name' = 'time',
  timeoutMs: number = 15000
): Promise<CommandResult<LsData>> {
  const start = Date.now();
  const host = resolveHost(hostAlias);

  if (!host) {
    return {
      ok: false,
      command: 'ls',
      summary: `Host '${hostAlias}' not found`,
      error: { code: 'NO_HOST', message: `Unknown host: ${hostAlias}` },
      durationMs: Date.now() - start,
    };
  }

  // Use --time-style=long-iso for parseable dates, fall back to basic ls -lh
  const sortFlag = sort === 'time' ? 't' : sort === 'size' ? 'S' : '';
  const cmd = `ls -lh${sortFlag} --time-style=long-iso ${shellEscape(remotePath)} 2>/dev/null || ls -lh${sortFlag} ${shellEscape(remotePath)} 2>&1`;

  const result = await execSsh(host, cmd, { timeoutMs });

  if (result.timedOut) {
    return {
      ok: false, host: hostAlias, command: 'ls',
      summary: `Timed out listing ${remotePath} on ${hostAlias}`,
      error: { code: 'TIMEOUT', message: 'SSH command timed out' },
      durationMs: Date.now() - start,
    };
  }

  const entries: RemoteFileEntry[] = [];
  for (const line of result.stdout.split('\n')) {
    const entry = parseLsLine(line);
    if (entry) entries.push(entry);
  }

  const ok = result.exitCode === 0;
  const summary = ok
    ? `${remotePath} on ${hostAlias} (${entries.length} entries):\n` +
      entries.map((e) => {
        const icon = e.isDirectory ? '📁' : '📄';
        return `  ${icon} ${e.name.padEnd(40)} ${e.size.padStart(8)} ${e.modified}`;
      }).join('\n')
    : `Failed to list ${remotePath}: ${result.stdout || result.stderr}`;

  return {
    ok, host: hostAlias, command: 'ls',
    data: { host: hostAlias, path: remotePath, entries },
    summary,
    raw: result.stdout,
    error: !ok ? { code: 'LS_FAILED', message: result.stderr || result.stdout } : undefined,
    durationMs: Date.now() - start,
  };
}

function shellEscape(s: string): string {
  return "'" + s.replace(/'/g, "'\\''") + "'";
}
