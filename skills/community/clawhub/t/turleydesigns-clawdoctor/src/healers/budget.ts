import fs from 'fs';
import path from 'path';
import { BaseHealer, HealResult } from './base.js';
import { runCommand } from '../utils.js';

export class BudgetHealer extends BaseHealer {
  readonly name = 'BudgetHealer';

  async heal(context: Record<string, unknown>): Promise<HealResult> {
    const dailySpend = (context.dailySpend as number | undefined) ?? 0;
    const limit = (context.limit as number | undefined) ?? 50;
    const dryRun = this.isEffectiveDryRun(false);

    if (dryRun) {
      this.writeAudit('budget-emergency-stop', 'all-sessions', 'yellow', 'dry-run');
      return {
        success: true,
        action: 'dry-run: would kill all non-essential sessions',
        message: `[DRY RUN] Would kill all sessions (budget $${dailySpend.toFixed(2)} exceeded $${limit.toFixed(2)} limit)`,
        tier: 'yellow',
      };
    }

    const increaseAmount = Math.ceil(limit * 1.5 / 10) * 10;
    const result: HealResult = {
      success: true,
      action: 'requested budget approval',
      message: `Daily budget exceeded: $${dailySpend.toFixed(2)} of $${limit.toFixed(2)}. Emergency action required.`,
      details: { dailySpend, limit },
      tier: 'yellow',
      requiresApproval: true,
      approvalOptions: [
        { text: `Kill All Sessions ($${dailySpend.toFixed(2)} spent)`, callbackData: 'budget:kill_all' },
        { text: `Increase to $${increaseAmount}`, callbackData: `budget:increase:${increaseAmount}` },
        { text: 'Ignore', callbackData: 'budget:ignore' },
      ],
    };
    await this.recordHeal('BudgetWatcher', result, 'budget_approval_requested');
    this.writeAudit('budget-emergency-stop', 'all-sessions', 'yellow', 'pending');
    return result;
  }

  async killAllSessions(): Promise<{ killed: number; failed: number }> {
    const agentsDir = path.join(this.config.openclawPath, 'agents');
    let killed = 0;
    let failed = 0;

    if (!fs.existsSync(agentsDir)) return { killed, failed };

    let agentDirs: string[];
    try {
      agentDirs = fs.readdirSync(agentsDir).filter(d => {
        try { return fs.statSync(path.join(agentsDir, d)).isDirectory(); }
        catch { return false; }
      });
    } catch { return { killed, failed }; }

    for (const agentDir of agentDirs) {
      const sessionsDir = path.join(agentsDir, agentDir, 'sessions');
      if (!fs.existsSync(sessionsDir)) continue;

      let sessionFiles: string[];
      try {
        sessionFiles = fs.readdirSync(sessionsDir)
          .filter(f => f.endsWith('.jsonl'))
          .map(f => f.replace('.jsonl', ''));
      } catch { continue; }

      for (const session of sessionFiles) {
        const killResult = runCommand('openclaw', ['session', 'kill', agentDir, session]);
        if (killResult.ok) {
          killed++;
        } else {
          failed++;
        }
      }
    }

    this.writeAudit('budget-kill-all', `${killed} sessions killed`, 'yellow', killed > 0 ? 'success' : 'failed');
    return { killed, failed };
  }
}
