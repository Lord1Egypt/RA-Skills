// `ssh-lab alert list|add|remove|check` — declarative alert rule engine

import { statusCommand } from './status.js';
import { evaluateAlerts } from '../alerts/rules.js';
import { loadRules, addRule, removeRule } from '../alerts/state.js';
import type {
  CommandResult,
  AlertRule,
  AlertRuleKind,
  AlertCheckResult,
  HostStatus,
  HostStatusData,
} from '../types/index.js';

/** Convert probe-based HostStatus to flattened HostStatusData for alert evaluation */
function flattenStatus(s: HostStatus): HostStatusData {
  const collectorErrors: string[] = [];
  // Collect alerts that indicate probe failures
  for (const a of s.alerts) {
    if (a.message.includes('timed out') || a.message.includes('failed')) {
      collectorErrors.push(a.message);
    }
  }
  return {
    host: s.host,
    gpu: s.gpu.gpus,
    disk: s.disk.disks,
    processes: s.process.processes,
    collectorErrors,
  };
}

/** ssh-lab alert list */
export function alertListCommand(): CommandResult<AlertRule[]> {
  const start = Date.now();
  const rules = loadRules();

  const lines = ['Alert Rules:'];
  if (rules.length === 0) {
    lines.push('  No rules configured. Use `ssh-lab alert add` to create one.');
  } else {
    for (const r of rules) {
      const thresh = r.threshold !== undefined ? ` threshold=${r.threshold}` : '';
      const pat = r.processPattern ? ` pattern=/${r.processPattern}/` : '';
      const icon = r.enabled ? '✅' : '⏸️';
      lines.push(`  ${icon} ${r.id}: ${r.kind} on ${r.host}${thresh}${pat}`);
    }
  }

  return {
    ok: true,
    command: 'alert-list',
    data: rules,
    summary: lines.join('\n'),
    durationMs: Date.now() - start,
  };
}

/** ssh-lab alert add <kind> <host> [--threshold N] [--pattern P] */
export function alertAddCommand(
  kind: AlertRuleKind,
  host: string,
  options: { threshold?: number; processPattern?: string } = {},
): CommandResult<AlertRule> {
  const start = Date.now();
  const rule = addRule({ kind, host, threshold: options.threshold, processPattern: options.processPattern });

  return {
    ok: true,
    command: 'alert-add',
    host,
    data: rule,
    summary: `✅ Alert rule added: ${kind} on ${host} (id: ${rule.id})`,
    durationMs: Date.now() - start,
  };
}

/** ssh-lab alert remove <rule-id> */
export function alertRemoveCommand(ruleId: string): CommandResult<{ removed: boolean }> {
  const start = Date.now();
  const removed = removeRule(ruleId);

  return {
    ok: removed,
    command: 'alert-remove',
    data: { removed },
    summary: removed ? `✅ Rule ${ruleId} removed` : `❌ Rule ${ruleId} not found`,
    error: removed ? undefined : { code: 'NOT_FOUND', message: `No rule with id "${ruleId}"` },
    durationMs: Date.now() - start,
  };
}

/** ssh-lab alert check [host|all] — evaluate rules against live status */
export async function alertCheckCommand(target: string, timeoutMs?: number): Promise<CommandResult<AlertCheckResult[]>> {
  const start = Date.now();

  const statusResult = await statusCommand(target, timeoutMs);
  if (!statusResult.ok || !statusResult.data) {
    return {
      ok: false,
      command: 'alert-check',
      summary: `Cannot check alerts: status collection failed`,
      error: statusResult.error,
      durationMs: Date.now() - start,
    };
  }

  const results = statusResult.data.map((s) => evaluateAlerts(flattenStatus(s)));
  const totalFirings = results.reduce((n, r) => n + r.firings.length, 0);
  const criticals = results.flatMap((r) => r.firings.filter((f) => f.level === 'critical'));
  const warnings = results.flatMap((r) => r.firings.filter((f) => f.level === 'warning'));

  const lines = [`Alert Check — ${results.length} host(s)`];
  if (totalFirings === 0) {
    lines.push('  All clear ✅');
  } else {
    for (const r of results) {
      for (const f of r.firings) {
        const icon = f.level === 'critical' ? '🔴' : f.level === 'warning' ? '🟡' : '🔵';
        lines.push(`  ${icon} [${r.host}] ${f.kind}: ${f.message}`);
      }
      for (const e of r.errors) {
        lines.push(`  ❌ [${r.host}] ${e}`);
      }
    }
  }

  if (criticals.length > 0) lines.push(`\n  🔴 ${criticals.length} critical alert(s)`);
  if (warnings.length > 0) lines.push(`  🟡 ${warnings.length} warning(s)`);

  // Exit code: 0=clear, 1=warning, 2=critical
  // Store level in error code so CLI can use differentiated exit codes
  const alertLevel = criticals.length > 0 ? 'critical' : warnings.length > 0 ? 'warning' : 'clear';

  return {
    ok: alertLevel === 'clear',
    command: 'alert-check',
    data: results,
    summary: lines.join('\n'),
    error: alertLevel !== 'clear'
      ? { code: alertLevel === 'critical' ? 'ALERT_CRITICAL' : 'ALERT_WARNING', message: `${totalFirings} alert(s) firing` }
      : undefined,
    durationMs: Date.now() - start,
  };
}
