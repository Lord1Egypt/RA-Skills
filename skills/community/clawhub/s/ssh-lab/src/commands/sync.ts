// `ssh-lab sync <host> <src> <dst>` — rsync wrapper for file transfer

import { spawn } from 'node:child_process';
import { resolveHost } from '../ssh/config.js';
import type { CommandResult } from '../types/index.js';

interface SyncData {
  host: string;
  direction: 'up' | 'down';
  src: string;
  dst: string;
  output: string;
  exitCode: number | null;
}

export async function syncCommand(
  hostAlias: string,
  src: string,
  dst: string,
  options: {
    direction?: 'up' | 'down';
    dryRun?: boolean;
    delete?: boolean;
    exclude?: string[];
    timeoutMs?: number;
  } = {}
): Promise<CommandResult<SyncData>> {
  const start = Date.now();
  const host = resolveHost(hostAlias);
  const direction = options.direction || 'down';

  if (!host) {
    return {
      ok: false, command: 'sync',
      summary: `Host '${hostAlias}' not found`,
      error: { code: 'NO_HOST', message: `Unknown host: ${hostAlias}` },
      durationMs: Date.now() - start,
    };
  }

  // Build rsync command
  const rsyncArgs: string[] = ['-avz', '--progress'];

  if (options.dryRun) rsyncArgs.push('--dry-run');
  if (options.delete) rsyncArgs.push('--delete');
  if (options.exclude) {
    for (const pattern of options.exclude) {
      rsyncArgs.push('--exclude', pattern);
    }
  }

  // Build SSH options for rsync (port, identity)
  const sshOpts: string[] = [];
  if (host.source === 'ssh-config') {
    // Use alias-based config — SSH will resolve everything
    // But rsync needs user@hostname, so we pass -e ssh with config
  }
  if (host.port) sshOpts.push(`-p ${host.port}`);
  if (host.identityFile) sshOpts.push(`-i ${host.identityFile}`);
  if (sshOpts.length > 0) {
    rsyncArgs.push('-e', `ssh ${sshOpts.join(' ')}`);
  }

  // Build remote path
  const remotePrefix = host.source === 'ssh-config'
    ? host.alias  // Use SSH alias for config-based hosts
    : (host.user ? `${host.user}@${host.hostname}` : host.hostname);

  if (direction === 'up') {
    rsyncArgs.push(src, `${remotePrefix}:${dst}`);
  } else {
    rsyncArgs.push(`${remotePrefix}:${src}`, dst);
  }

  return new Promise((resolve) => {
    let output = '';
    const child = spawn('rsync', rsyncArgs, { stdio: ['ignore', 'pipe', 'pipe'] });

    const timer = options.timeoutMs
      ? setTimeout(() => child.kill('SIGTERM'), options.timeoutMs)
      : null;

    child.stdout.on('data', (chunk: Buffer) => { output += chunk.toString(); });
    child.stderr.on('data', (chunk: Buffer) => { output += chunk.toString(); });

    child.on('close', (code) => {
      if (timer) clearTimeout(timer);
      const ok = code === 0;
      resolve({
        ok, host: hostAlias, command: 'sync',
        data: { host: hostAlias, direction, src, dst, output: output.trimEnd(), exitCode: code },
        summary: ok
          ? `Synced ${direction === 'up' ? 'local→remote' : 'remote→local'}: ${src} → ${dst}${options.dryRun ? ' (dry run)' : ''}\n${output.trimEnd()}`
          : `Sync failed (exit ${code}): ${output.trimEnd()}`,
        raw: output.trimEnd(),
        error: !ok ? { code: 'SYNC_FAILED', message: `rsync exit ${code}` } : undefined,
        durationMs: Date.now() - start,
      });
    });

    child.on('error', (err) => {
      if (timer) clearTimeout(timer);
      resolve({
        ok: false, host: hostAlias, command: 'sync',
        data: { host: hostAlias, direction, src, dst, output: '', exitCode: null },
        summary: `Sync error: ${err.message}`,
        error: { code: 'SPAWN_ERROR', message: err.message },
        durationMs: Date.now() - start,
      });
    });
  });
}
