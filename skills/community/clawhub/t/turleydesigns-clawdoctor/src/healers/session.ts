import fs from 'fs';
import { BaseHealer, HealResult } from './base.js';
import { runCommand } from '../utils.js';

const STUCK_THRESHOLD_SECONDS = 2 * 3600; // 2 hours
const HIGH_COST_THRESHOLD_USD = 10;

export class SessionHealer extends BaseHealer {
  readonly name = 'SessionHealer';

  async heal(context: Record<string, unknown>): Promise<HealResult> {
    const agent = (context.agent as string | undefined) ?? 'unknown';
    const session = (context.session as string | undefined) ?? 'unknown';
    const ageSec = (context.ageSec as number | undefined) ?? 0;
    const sessionPath = (context.sessionPath as string | undefined) ?? '';
    const costUsd = (context.costUsd as number | undefined) ?? 0;
    const dryRun = this.isEffectiveDryRun(this.config.healers.session.dryRun);

    // Yellow tier: high token burn needs approval
    if (costUsd >= HIGH_COST_THRESHOLD_USD) {
      if (dryRun) {
        this.writeAudit('session-cost-alert', agent, 'yellow', 'dry-run');
        return {
          success: true,
          action: `dry-run: would send cost alert for agent '${agent}'`,
          message: `[DRY RUN] Would request approval for high-cost session ($${costUsd.toFixed(2)})`,
          tier: 'yellow',
        };
      }
      this.writeAudit('session-cost-alert', agent, 'yellow', 'pending');
      const result: HealResult = {
        success: true,
        action: `requested approval for high-cost session in agent '${agent}'`,
        message: `Session in agent '${agent}' has spent $${costUsd.toFixed(2)}. Action required.`,
        details: { agent, session, costUsd },
        tier: 'yellow',
        requiresApproval: true,
        approvalOptions: [
          { text: `Kill Session ($${costUsd.toFixed(2)} spent)`, callbackData: `session:kill:${agent}:${session}` },
          { text: 'Let it run', callbackData: `session:ignore:${agent}:${session}` },
        ],
      };
      await this.recordHeal('SessionWatcher', result, 'session_cost_alert');
      return result;
    }

    // Green tier: kill sessions stuck >2 hours
    if (ageSec >= STUCK_THRESHOLD_SECONDS) {
      if (dryRun) {
        this.writeAudit('session-kill', agent, 'green', 'dry-run');
        return {
          success: true,
          action: `dry-run: would kill stuck session in agent '${agent}'`,
          message: `[DRY RUN] Would kill session running for ${Math.round(ageSec / 60)}m`,
          tier: 'green',
        };
      }

      // Snapshot session log before killing
      let sessionLogSample = '';
      if (sessionPath) {
        try {
          const lines = fs.readFileSync(sessionPath, 'utf-8').split('\n').filter(Boolean);
          sessionLogSample = lines.slice(-10).join('\n');
        } catch {
          // ignore
        }
      }

      const snapshotId = this.takeSnapshot(
        'session-kill',
        `${agent}/${session}`,
        { agent, session, ageSec, sessionLogSample },
        `echo "Session ${session} was killed - restore manually if needed"`
      );

      const killResult = runCommand('openclaw', ['session', 'kill', agent, session]);

      if (killResult.ok) {
        const result: HealResult = {
          success: true,
          action: `openclaw session kill ${agent} ${session}`,
          message: `Killed stuck session in agent '${agent}' (running for ${Math.round(ageSec / 60)}m)`,
          details: { agent, session, ageSec, snapshotId },
          tier: 'green',
          snapshotId,
        };
        await this.recordHeal('SessionWatcher', result, 'session_killed');
        this.writeAudit('session-kill', agent, 'green', 'success', snapshotId);
        return result;
      }

      // Kill command not available, just log
      const result: HealResult = {
        success: false,
        action: `openclaw session kill ${agent} ${session}`,
        message: `Could not kill stuck session in agent '${agent}': ${killResult.stderr.slice(0, 200)}`,
        details: { agent, session, ageSec, snapshotId },
        tier: 'green',
        snapshotId,
      };
      await this.recordHeal('SessionWatcher', result, 'session_kill_failed');
      this.writeAudit('session-kill', agent, 'green', 'failed', snapshotId);
      return result;
    }

    // Default: log the issue
    const result: HealResult = {
      success: true,
      action: `logged session issue for agent '${agent}'`,
      message: `Session issue logged for agent '${agent}', session '${session}'`,
      details: { agent, session, ageSec },
      tier: 'green',
    };
    await this.recordHeal('SessionWatcher', result, 'session_issue_logged');
    this.writeAudit('session-log', agent, 'green', 'success');
    return result;
  }
}
