// `ssh-lab doctor <host>` — connectivity & health diagnostics

import { resolveHost } from '../ssh/config.js';
import { execSsh } from '../ssh/exec.js';
import type { CommandResult, DoctorResult, DoctorCheck, HostConfig } from '../types/index.js';

async function runCheck(
  name: string,
  fn: () => Promise<{ status: DoctorCheck['status']; message: string }>,
): Promise<DoctorCheck> {
  const start = Date.now();
  try {
    const { status, message } = await fn();
    return { name, status, message, durationMs: Date.now() - start };
  } catch (err) {
    return {
      name,
      status: 'fail',
      message: err instanceof Error ? err.message : String(err),
      durationMs: Date.now() - start,
    };
  }
}

export async function doctorCommand(hostAlias: string, timeoutMs: number = 15000): Promise<CommandResult<DoctorResult>> {
  const start = Date.now();
  const host = resolveHost(hostAlias);

  if (!host) {
    return {
      ok: false,
      command: 'doctor',
      host: hostAlias,
      summary: `❌ Host '${hostAlias}' not found`,
      error: { code: 'HOST_NOT_FOUND', message: `Cannot resolve host '${hostAlias}'` },
      durationMs: Date.now() - start,
    };
  }

  const checks: DoctorCheck[] = [];

  // 1. SSH connectivity
  checks.push(await runCheck('SSH connectivity', async () => {
    const r = await execSsh(host, 'echo ok', { timeoutMs: Math.min(timeoutMs, 5000) });
    if (r.exitCode === 0 && r.stdout.includes('ok')) {
      return { status: 'pass', message: `Connected in ${r.durationMs}ms` };
    }
    if (r.timedOut) {
      return { status: 'fail', message: `Timed out after ${r.durationMs}ms` };
    }
    return { status: 'fail', message: r.stderr || 'SSH connection failed' };
  }));

  // If SSH failed, skip remote checks
  if (checks[0]!.status === 'fail') {
    const skipMsg = 'Skipped (SSH failed)';
    checks.push(
      { name: 'nvidia-smi', status: 'skip', message: skipMsg, durationMs: 0 },
      { name: 'Disk writable', status: 'skip', message: skipMsg, durationMs: 0 },
      { name: 'Python', status: 'skip', message: skipMsg, durationMs: 0 },
      { name: 'System memory', status: 'skip', message: skipMsg, durationMs: 0 },
    );
  } else {
    // 2. nvidia-smi
    checks.push(await runCheck('nvidia-smi', async () => {
      const r = await execSsh(host, 'nvidia-smi --query-gpu=count --format=csv,noheader,nounits 2>/dev/null', { timeoutMs });
      if (r.exitCode === 0 && r.stdout.trim()) {
        const count = r.stdout.trim().split('\n').length;
        return { status: 'pass', message: `${count} GPU(s) detected` };
      }
      return { status: 'warn', message: 'nvidia-smi not found — no GPU monitoring' };
    }));

    // 3. Disk writable
    checks.push(await runCheck('Disk writable', async () => {
      const r = await execSsh(host, 'touch /tmp/.ssh-lab-probe && rm /tmp/.ssh-lab-probe && echo writable', { timeoutMs });
      if (r.exitCode === 0 && r.stdout.includes('writable')) {
        return { status: 'pass', message: '/tmp is writable' };
      }
      return { status: 'fail', message: 'Cannot write to /tmp' };
    }));

    // 4. Python
    checks.push(await runCheck('Python', async () => {
      const r = await execSsh(host, 'python3 --version 2>/dev/null || python --version 2>/dev/null', { timeoutMs });
      if (r.exitCode === 0 && r.stdout.trim()) {
        return { status: 'pass', message: r.stdout.trim() };
      }
      return { status: 'warn', message: 'Python not found in PATH' };
    }));

    // 5. System memory
    checks.push(await runCheck('System memory', async () => {
      const r = await execSsh(host, 'free -h 2>/dev/null | head -2', { timeoutMs });
      if (r.exitCode === 0 && r.stdout.trim()) {
        const lines = r.stdout.trim().split('\n');
        const memLine = lines[1];
        if (memLine) {
          const parts = memLine.split(/\s+/);
          return { status: 'pass', message: `Total: ${parts[1]}, Used: ${parts[2]}, Free: ${parts[3]}` };
        }
      }
      return { status: 'warn', message: 'Could not parse memory info' };
    }));
  }

  const failCount = checks.filter((c) => c.status === 'fail').length;
  const warnCount = checks.filter((c) => c.status === 'warn').length;
  const passCount = checks.filter((c) => c.status === 'pass').length;
  const overallStatus = failCount > 0 ? 'unhealthy' as const : warnCount > 0 ? 'degraded' as const : 'healthy' as const;
  const icon = { healthy: '✅', degraded: '🟡', unhealthy: '🔴' }[overallStatus];

  const lines = [`${icon} ${hostAlias}: ${overallStatus} (${passCount}/${checks.length} passed)`];
  for (const c of checks) {
    const ci = { pass: '✅', fail: '🔴', warn: '🟡', skip: '⏭️' }[c.status];
    lines.push(`  ${ci} ${c.name}: ${c.message} [${c.durationMs}ms]`);
  }

  return {
    ok: failCount === 0,
    command: 'doctor',
    host: hostAlias,
    data: { host: hostAlias, checks, overallStatus },
    summary: lines.join('\n'),
    durationMs: Date.now() - start,
  };
}
