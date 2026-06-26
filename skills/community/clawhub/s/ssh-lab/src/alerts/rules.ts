import type {
  AlertRule,
  AlertFiring,
  AlertCheckResult,
  HostStatusData,
  NoticeLevel,
} from '../types/index.js';
import { rulesForHost } from './state.js';

/**
 * Evaluate all applicable alert rules against a host's flattened status data.
 */
export function evaluateAlerts(status: HostStatusData): AlertCheckResult {
  const rules = rulesForHost(status.host.alias);
  const firings: AlertFiring[] = [];
  const errors: string[] = [];

  for (const rule of rules) {
    try {
      const firing = evaluateRule(rule, status);
      if (firing) firings.push(firing);
    } catch (err) {
      errors.push(`Rule ${rule.id} (${rule.kind}): ${err instanceof Error ? err.message : String(err)}`);
    }
  }

  return { host: status.host.alias, firings, errors };
}

function evaluateRule(rule: AlertRule, status: HostStatusData): AlertFiring | null {
  switch (rule.kind) {
    case 'gpu_idle':     return checkGpuIdle(rule, status);
    case 'disk_full':    return checkDiskFull(rule, status);
    case 'process_died': return checkProcessDied(rule, status);
    case 'ssh_unreachable': return checkSshUnreachable(rule, status);
    case 'oom_detected': return checkOom(rule, status);
    case 'high_temp':    return checkHighTemp(rule, status);
    default:             return null;
  }
}

function makeFiring(rule: AlertRule, level: NoticeLevel, message: string, value?: number): AlertFiring {
  return {
    ruleId: rule.id,
    kind: rule.kind,
    host: rule.host,
    level,
    message,
    value,
    threshold: rule.threshold,
    firedAt: new Date().toISOString(),
  };
}

/** GPU idle: all GPUs util < 5% but VRAM loaded (>30%) — wasting money */
function checkGpuIdle(rule: AlertRule, status: HostStatusData): AlertFiring | null {
  if (status.gpu.length === 0) return null;

  const idleLoaded = status.gpu.filter((g) => {
    const memPct = (g.memoryUsedMiB / g.memoryTotalMiB) * 100;
    return g.utilizationPct < 5 && memPct > 30;
  });

  if (idleLoaded.length > 0) {
    return makeFiring(rule, 'warning',
      `${idleLoaded.length}/${status.gpu.length} GPUs idle but loaded (VRAM >30%, util <5%)`,
      idleLoaded.length);
  }
  return null;
}

/** Disk full: any mount exceeds threshold% */
function checkDiskFull(rule: AlertRule, status: HostStatusData): AlertFiring | null {
  const threshold = rule.threshold ?? 90;
  const full = status.disk.filter((d) => d.usedPct >= threshold);

  if (full.length > 0) {
    const worst = full.reduce((a, b) => a.usedPct > b.usedPct ? a : b);
    const level: NoticeLevel = worst.usedPct >= 95 ? 'critical' : 'warning';
    return makeFiring(rule, level,
      `${full.length} disk(s) above ${threshold}%: ${full.map((d) => `${d.mountpoint} ${d.usedPct}%`).join(', ')}`,
      worst.usedPct);
  }
  return null;
}

/** Process died: expected process pattern not found */
function checkProcessDied(rule: AlertRule, status: HostStatusData): AlertFiring | null {
  if (!rule.processPattern) return null;
  const pattern = new RegExp(rule.processPattern, 'i');
  const found = status.processes.some((p) => pattern.test(p.command));

  if (!found) {
    return makeFiring(rule, 'critical',
      `Expected process /${rule.processPattern}/ not found on ${status.host.alias}`);
  }
  return null;
}

/** SSH unreachable: all collectors errored with SSH problems */
function checkSshUnreachable(rule: AlertRule, status: HostStatusData): AlertFiring | null {
  const sshErrors = status.collectorErrors.filter((e) =>
    e.includes('SSH') || e.includes('timeout') || e.includes('Connection refused'));

  if (sshErrors.length > 0 && sshErrors.length === status.collectorErrors.length) {
    return makeFiring(rule, 'critical',
      `All collectors failed with SSH errors: ${sshErrors.join('; ')}`);
  }
  return null;
}

/** OOM risk: any process using >90% system memory (proxy for OOM pressure) */
function checkOom(rule: AlertRule, status: HostStatusData): AlertFiring | null {
  const highMem = status.processes.filter((p) => p.memPct > 90);
  if (highMem.length > 0) {
    return makeFiring(rule, 'warning',
      `${highMem.length} process(es) using >90% memory: ${highMem.map((p) => `PID ${p.pid} (${p.memPct}%)`).join(', ')}`,
      highMem[0]!.memPct);
  }
  return null;
}

/** High temperature: any GPU over threshold°C */
function checkHighTemp(rule: AlertRule, status: HostStatusData): AlertFiring | null {
  const threshold = rule.threshold ?? 85;
  const hot = status.gpu.filter((g) => g.temperatureC >= threshold);

  if (hot.length > 0) {
    const worst = hot.reduce((a, b) => a.temperatureC > b.temperatureC ? a : b);
    const level: NoticeLevel = worst.temperatureC >= 90 ? 'critical' : 'warning';
    return makeFiring(rule, level,
      `${hot.length} GPU(s) above ${threshold}°C: ${hot.map((g) => `GPU ${g.index}: ${g.temperatureC}°C`).join(', ')}`,
      worst.temperatureC);
  }
  return null;
}
