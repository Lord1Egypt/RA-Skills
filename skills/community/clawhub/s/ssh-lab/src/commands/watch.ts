// `ssh-lab watch <host> <path>` — periodic tail with change detection

import { execSsh } from '../ssh/exec.js';
import { resolveHost } from '../ssh/config.js';
import type { CommandResult } from '../types/index.js';

interface WatchSnapshot {
  host: string;
  path: string;
  content: string;
  lineCount: number;
  lastModified: string;
  sizeBytes: number;
  changed: boolean;
  /** Content hash for change detection — pass back as --prev-hash */
  hash: string;
}

/**
 * Single-shot watch: captures current file state with metadata.
 * For continuous watching, the caller (agent/cron) invokes this repeatedly.
 *
 * This is intentionally NOT a long-running process — the LLM agent
 * manages the polling loop via cron/heartbeat, not us.
 */
export async function watchCommand(
  hostAlias: string,
  remotePath: string,
  options: {
    lines?: number;
    /** Previous content hash to detect changes */
    prevHash?: string;
    timeoutMs?: number;
  } = {}
): Promise<CommandResult<WatchSnapshot>> {
  const start = Date.now();
  const host = resolveHost(hostAlias);
  const lines = options.lines || 30;

  if (!host) {
    return {
      ok: false, command: 'watch',
      summary: `Host '${hostAlias}' not found`,
      error: { code: 'NO_HOST', message: `Unknown host: ${hostAlias}` },
      durationMs: Date.now() - start,
    };
  }

  // Get tail + file metadata in one SSH call
  const cmd = [
    `stat -c '%Y %s' ${shellEscape(remotePath)} 2>/dev/null || stat -f '%m %z' ${shellEscape(remotePath)} 2>/dev/null`,
    `echo '---WATCH-SEP---'`,
    `tail -n ${lines} ${shellEscape(remotePath)} 2>&1`,
  ].join('; ');

  const result = await execSsh(host, cmd, { timeoutMs: options.timeoutMs || 15000 });

  if (result.timedOut) {
    return {
      ok: false, host: hostAlias, command: 'watch',
      summary: `Timed out watching ${remotePath} on ${hostAlias}`,
      error: { code: 'TIMEOUT', message: 'SSH command timed out' },
      durationMs: Date.now() - start,
    };
  }

  const sepIdx = result.stdout.indexOf('---WATCH-SEP---');
  const statLine = sepIdx >= 0 ? result.stdout.slice(0, sepIdx).trim() : '';
  const content = sepIdx >= 0 ? result.stdout.slice(sepIdx + 15).trim() : result.stdout;

  const [modTime, sizeStr] = statLine.split(' ');
  const sizeBytes = parseInt(sizeStr || '0', 10) || 0;
  const lastModified = modTime ? new Date(parseInt(modTime, 10) * 1000).toISOString() : 'unknown';

  // Simple change detection via content hash
  const currentHash = simpleHash(content);
  const changed = options.prevHash ? currentHash !== options.prevHash : true;

  const ok = result.exitCode === 0;

  return {
    ok, host: hostAlias, command: 'watch',
    data: {
      host: hostAlias,
      path: remotePath,
      content,
      lineCount: content.split('\n').length,
      lastModified,
      sizeBytes,
      changed,
      hash: currentHash,
    },
    summary: ok
      ? `${remotePath} on ${hostAlias} | ${sizeBytes} bytes | modified ${lastModified} | ${changed ? '🔄 CHANGED' : '✓ unchanged'}\n${content}`
      : `Failed to watch ${remotePath}: ${result.stderr || result.stdout}`,
    raw: content,
    error: !ok ? { code: 'WATCH_FAILED', message: result.stderr || result.stdout } : undefined,
    durationMs: Date.now() - start,
  };
}

/** Simple FNV-1a hash for change detection */
function simpleHash(s: string): string {
  let hash = 0x811c9dc5;
  for (let i = 0; i < s.length; i++) {
    hash ^= s.charCodeAt(i);
    hash = (hash * 0x01000193) >>> 0;
  }
  return hash.toString(16);
}

function shellEscape(s: string): string {
  return "'" + s.replace(/'/g, "'\\''") + "'";
}
