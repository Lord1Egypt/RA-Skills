// SSH execution engine — spawns native `ssh` process
// Zero dependencies: uses child_process only

import { spawn, execFileSync } from 'node:child_process';
import { unlinkSync, existsSync } from 'node:fs';
import type { SshExecResult, SshExecOptions, HostConfig, SshError, SshErrorCode } from '../types/index.js';

const DEFAULT_TIMEOUT_MS = 15_000;

// ── Timeout tiers by command type ───────────────────────────
// Quick checks (connectivity, config): 5s
// Standard probes (status, run, ls, df, alert, compare): 15s
// Streaming / log tailing (tail, watch): 30s
// Bulk transfer (sync / rsync): 60s
export const TIMEOUT_TIERS = {
  quick: 5_000,      // hosts, add, doctor
  standard: 15_000,  // status, run, ls, df, alert, compare
  stream: 30_000,    // tail, watch
  transfer: 60_000,  // sync (rsync)
} as const;

// ── Error classification ────────────────────────────────────

/** Classify an SSH execution result into a typed error (or null if success). */
export function classifySshError(result: SshExecResult): SshError | null {
  if (result.exitCode === 0 && !result.timedOut) return null;

  const stderr = result.stderr.toLowerCase();

  if (result.timedOut) {
    return { code: 'TIMEOUT', message: `SSH command timed out after ${result.durationMs}ms`, retryable: true };
  }

  // SSH exit code 255 = SSH-level failure
  if (result.exitCode === 255) {
    if (stderr.includes('permission denied') || stderr.includes('publickey')) {
      return { code: 'AUTH_FAILED', message: 'Authentication failed (permission denied)', retryable: false };
    }
    if (stderr.includes('host key verification failed') || stderr.includes('host key has changed') || stderr.includes('offending') ) {
      return { code: 'AUTH_FAILED', message: 'Host key verification failed — remove stale key from known_hosts', retryable: false };
    }
    if (stderr.includes('connection refused')) {
      return { code: 'CONNECTION_REFUSED', message: 'Connection refused by remote host', retryable: true };
    }
    if (stderr.includes('no route to host') || stderr.includes('network is unreachable') || stderr.includes('could not resolve')) {
      return { code: 'HOST_UNREACHABLE', message: 'Host unreachable or DNS resolution failed', retryable: true };
    }
    if (stderr.includes('connection reset') || stderr.includes('broken pipe') || stderr.includes('connection timed out')) {
      return { code: 'TIMEOUT', message: 'Connection reset or timed out', retryable: true };
    }
    return { code: 'UNKNOWN', message: result.stderr || 'SSH connection failed (exit 255)', retryable: true };
  }

  // Non-zero exit from the remote command itself
  return { code: 'COMMAND_FAILED', message: result.stderr || `Command exited with code ${result.exitCode}`, retryable: false };
}

// ── ControlMaster socket management ─────────────────────────

const CONTROL_PATH_TEMPLATE = '/tmp/ssh-lab-%r@%h:%p';

/** Resolve the ControlMaster socket path for a given host config. */
export function controlSocketPath(host: HostConfig): string {
  const user = host.user || process.env.USER || 'unknown';
  const hostname = host.source === 'ssh-config' ? host.alias : host.hostname;
  const port = host.port || 22;
  return CONTROL_PATH_TEMPLATE
    .replace('%r', user)
    .replace('%h', hostname)
    .replace('%p', String(port));
}

/**
 * Check if the ControlMaster socket is alive.
 * Returns true if healthy, false if stale/missing.
 */
export function isControlMasterAlive(host: HostConfig): boolean {
  const target = host.source === 'ssh-config' ? host.alias : (host.user ? `${host.user}@${host.hostname}` : host.hostname);
  try {
    execFileSync('ssh', [
      '-O', 'check',
      '-o', `ControlPath=${CONTROL_PATH_TEMPLATE}`,
      target,
    ], { timeout: 3000, stdio: 'pipe' });
    return true;
  } catch {
    return false;
  }
}

/**
 * Clean up a stale ControlMaster socket.
 * Tries graceful `ssh -O exit` first, then removes the socket file.
 */
export function cleanControlSocket(host: HostConfig): void {
  const target = host.source === 'ssh-config' ? host.alias : (host.user ? `${host.user}@${host.hostname}` : host.hostname);

  // Try graceful exit first
  try {
    execFileSync('ssh', [
      '-O', 'exit',
      '-o', `ControlPath=${CONTROL_PATH_TEMPLATE}`,
      target,
    ], { timeout: 3000, stdio: 'pipe' });
  } catch {
    // Graceful exit failed — remove socket file directly
    const socketPath = controlSocketPath(host);
    if (existsSync(socketPath)) {
      try { unlinkSync(socketPath); } catch { /* already gone */ }
    }
  }
}

// ── Retry logic ─────────────────────────────────────────────

export interface RetryOptions {
  maxRetries?: number;
  baseDelayMs?: number;
}

/** Execute SSH with retry + exponential backoff for retryable errors. */
export async function execSshWithRetry(
  host: HostConfig,
  remoteCmd: string,
  options: SshExecOptions & RetryOptions = {},
): Promise<SshExecResult & { attempts: number; lastError?: SshError }> {
  const maxRetries = options.maxRetries ?? 2;
  const baseDelayMs = options.baseDelayMs ?? 500;
  let lastResult: SshExecResult | null = null;
  let lastError: SshError | null = null;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    if (attempt > 0) {
      // Clean stale ControlMaster socket before retry (connection errors often mean stale mux)
      if (lastError && lastError.retryable && lastError.code !== 'COMMAND_FAILED') {
        if (!isControlMasterAlive(host)) {
          cleanControlSocket(host);
        }
      }
      // Exponential backoff with jitter
      const delay = baseDelayMs * Math.pow(2, attempt - 1) + Math.random() * 200;
      await new Promise(r => setTimeout(r, delay));
    }

    lastResult = await execSsh(host, remoteCmd, options);
    lastError = classifySshError(lastResult);

    if (!lastError || !lastError.retryable || attempt === maxRetries) {
      return { ...lastResult, attempts: attempt + 1, lastError: lastError ?? undefined };
    }
  }

  // Should not reach here, but TypeScript
  return { ...lastResult!, attempts: maxRetries + 1, lastError: lastError ?? undefined };
}

/** Build SSH target string from host config */
export function sshTarget(host: HostConfig): string {
  // If alias matches an SSH config Host entry, just use the alias
  // (ssh -G will have resolved everything)
  return host.alias;
}

/** Build SSH args array */
function buildArgs(host: HostConfig, remoteCmd: string): string[] {
  const args: string[] = [];

  // Connection options
  args.push('-o', 'BatchMode=yes');
  args.push('-o', 'ConnectTimeout=10');
  args.push('-o', 'StrictHostKeyChecking=accept-new');

  // ControlMaster reuse (if socket exists it reuses, otherwise creates)
  args.push('-o', 'ControlMaster=auto');
  args.push('-o', 'ControlPath=/tmp/ssh-lab-%r@%h:%p');
  args.push('-o', 'ControlPersist=300');

  // For SSH config hosts, use alias directly — inherits ProxyJump, keys, etc.
  // For custom hosts, specify user@hostname explicitly with overrides.
  if (host.source === 'ssh-config') {
    args.push(host.alias);
  } else {
    if (host.port) {
      args.push('-p', String(host.port));
    }
    if (host.identityFile) {
      args.push('-i', host.identityFile);
    }
    const target = host.user ? `${host.user}@${host.hostname}` : host.hostname;
    args.push(target);
  }

  // Remote command
  args.push(remoteCmd);

  return args;
}

/** Execute a command on a remote host via SSH */
export function execSsh(
  host: HostConfig,
  remoteCmd: string,
  options: SshExecOptions = {}
): Promise<SshExecResult> {
  const timeoutMs = options.timeoutMs ?? DEFAULT_TIMEOUT_MS;

  return new Promise((resolve) => {
    const startTime = Date.now();
    const args = buildArgs(host, remoteCmd);
    const child = spawn('ssh', args, { stdio: ['ignore', 'pipe', 'pipe'] });

    let stdout = '';
    let stderr = '';
    let timedOut = false;
    let settled = false;

    const timer = setTimeout(() => {
      timedOut = true;
      child.kill('SIGTERM');
      // Give it a moment then SIGKILL
      setTimeout(() => child.kill('SIGKILL'), 2000);
    }, timeoutMs);

    child.stdout.on('data', (chunk: Buffer) => {
      stdout += chunk.toString();
    });

    child.stderr.on('data', (chunk: Buffer) => {
      stderr += chunk.toString();
    });

    const finish = (exitCode: number | null) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      resolve({
        host: host.alias,
        command: remoteCmd,
        stdout: stdout.trimEnd(),
        stderr: stderr.trimEnd(),
        exitCode,
        durationMs: Date.now() - startTime,
        timedOut,
      });
    };

    child.on('close', (code) => finish(code));
    child.on('error', () => finish(null));
  });
}

// NOTE: For parallel multi-host execution, use withPool from '../ssh/pool.js'
// instead of rolling ad-hoc batching. See run.ts and compare.ts for examples.
