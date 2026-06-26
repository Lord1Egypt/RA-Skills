// `ssh-lab run <host> <cmd>` — execute arbitrary command on remote host(s)

import { execSsh } from '../ssh/exec.js';
import { withPool } from '../ssh/pool.js';
import { resolveHosts } from '../ssh/config.js';
import type { CommandResult, SshExecResult } from '../types/index.js';

export async function runCommand(
  target: string,
  remoteCmd: string,
  timeoutMs: number = 30000,
  options: { concurrency?: number } = {},
): Promise<CommandResult<SshExecResult | SshExecResult[]>> {
  const start = Date.now();
  const hosts = resolveHosts(target);

  if (hosts.length === 0) {
    return {
      ok: false,
      command: 'run',
      summary: `No hosts found for '${target}'`,
      error: { code: 'NO_HOSTS', message: `No hosts match '${target}'` },
      durationMs: Date.now() - start,
    };
  }

  if (hosts.length === 1) {
    const result = await execSsh(hosts[0], remoteCmd, { timeoutMs });
    const ok = result.exitCode === 0 && !result.timedOut;

    return {
      ok,
      host: result.host,
      command: 'run',
      data: result,
      summary: formatSingleResult(result),
      raw: result.stdout,
      error: !ok
        ? { code: result.timedOut ? 'TIMEOUT' : 'EXIT_CODE', message: result.stderr || `exit ${result.exitCode}` }
        : undefined,
      durationMs: Date.now() - start,
    };
  }

  // Multiple hosts — parallel execution via bounded pool
  const tasks = hosts.map((host) => () => execSsh(host, remoteCmd, { timeoutMs }));
  const settled = await withPool(tasks, options.concurrency ?? 5);
  const results: SshExecResult[] = [];
  for (const r of settled) {
    if (r.status === 'fulfilled') results.push(r.value);
  }
  const allOk = results.every((r) => r.exitCode === 0 && !r.timedOut);
  const summary = results.map(formatSingleResult).join('\n\n');

  return {
    ok: allOk,
    command: 'run',
    data: results,
    summary,
    durationMs: Date.now() - start,
  };
}

function formatSingleResult(r: SshExecResult): string {
  const status = r.timedOut ? '⏱ TIMEOUT' : r.exitCode === 0 ? '✓' : `✗ exit=${r.exitCode}`;
  const lines = [`[${r.host}] ${status} (${r.durationMs}ms)`];

  if (r.stdout) lines.push(r.stdout);
  if (r.stderr) lines.push(`stderr: ${r.stderr}`);

  return lines.join('\n');
}
