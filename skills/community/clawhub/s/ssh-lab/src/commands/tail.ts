// `ssh-lab tail <host> <path>` — remote log tail with smart truncation

import { execSsh } from '../ssh/exec.js';
import { resolveHost } from '../ssh/config.js';
import type { CommandResult } from '../types/index.js';

interface TailData {
  host: string;
  path: string;
  lines: number;
  content: string;
  truncated: boolean;
}

const MAX_OUTPUT_CHARS = 50_000;

export async function tailCommand(
  hostAlias: string,
  remotePath: string,
  lines: number = 50,
  timeoutMs: number = 15000
): Promise<CommandResult<TailData>> {
  const start = Date.now();
  const host = resolveHost(hostAlias);

  if (!host) {
    return {
      ok: false,
      command: 'tail',
      summary: `Host '${hostAlias}' not found`,
      error: { code: 'NO_HOST', message: `Unknown host: ${hostAlias}` },
      durationMs: Date.now() - start,
    };
  }

  const cmd = `tail -n ${lines} ${shellEscape(remotePath)} 2>&1`;
  const result = await execSsh(host, cmd, { timeoutMs });

  if (result.timedOut) {
    return {
      ok: false,
      host: hostAlias,
      command: 'tail',
      summary: `Timed out reading ${remotePath} on ${hostAlias}`,
      error: { code: 'TIMEOUT', message: 'SSH command timed out' },
      durationMs: Date.now() - start,
    };
  }

  let content = result.stdout;
  let truncated = false;

  if (content.length > MAX_OUTPUT_CHARS) {
    content = content.slice(-MAX_OUTPUT_CHARS);
    truncated = true;
  }

  const ok = result.exitCode === 0;

  return {
    ok,
    host: hostAlias,
    command: 'tail',
    data: {
      host: hostAlias,
      path: remotePath,
      lines,
      content,
      truncated,
    },
    summary: ok
      ? `${remotePath} (last ${lines} lines${truncated ? ', truncated' : ''}):\n${content}`
      : `Failed to tail ${remotePath}: ${result.stdout || result.stderr}`,
    raw: content,
    error: !ok
      ? { code: 'TAIL_FAILED', message: result.stderr || result.stdout }
      : undefined,
    durationMs: Date.now() - start,
  };
}

/** Basic shell escaping for paths */
function shellEscape(s: string): string {
  // Wrap in single quotes, escaping existing single quotes
  return "'" + s.replace(/'/g, "'\\''") + "'";
}
