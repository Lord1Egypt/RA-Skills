import { BaseHealer, HealResult } from './base.js';
import { runShell } from '../utils.js';

export class AuthHealer extends BaseHealer {
  readonly name = 'AuthHealer';

  async heal(context: Record<string, unknown>): Promise<HealResult> {
    const provider = (context.provider as string | undefined) ?? 'unknown';
    const count = (context.count as number | undefined) ?? 1;
    const dryRun = this.isEffectiveDryRun(this.config.healers.auth.dryRun);

    if (dryRun) {
      this.writeAudit('auth-refresh', provider, 'green', 'dry-run');
      return {
        success: true,
        action: 'dry-run: would run openclaw auth refresh',
        message: '[DRY RUN] Would attempt auth refresh',
        tier: 'green',
      };
    }

    // Green tier: attempt openclaw auth refresh
    const refreshResult = runShell('openclaw auth refresh 2>&1');

    if (refreshResult.ok) {
      const result: HealResult = {
        success: true,
        action: 'openclaw auth refresh',
        message: `Auth refresh succeeded (${count} auth failure(s) detected)`,
        details: { provider, count, stdout: refreshResult.stdout.slice(0, 300) },
        tier: 'green',
      };
      await this.recordHeal('AuthWatcher', result, 'auth_refreshed');
      this.writeAudit('auth-refresh', provider, 'green', 'success');
      return result;
    }

    // Yellow tier: refresh failed, request manual re-auth via Telegram
    this.writeAudit('auth-refresh', provider, 'yellow', 'pending');
    const result: HealResult = {
      success: false,
      action: 'openclaw auth refresh',
      message: `Auth refresh failed for provider '${provider}'. Manual re-auth required.`,
      details: {
        provider,
        count,
        stderr: refreshResult.stderr.slice(0, 300),
        stdout: refreshResult.stdout.slice(0, 300),
      },
      tier: 'yellow',
      requiresApproval: false,
    };
    await this.recordHeal('AuthWatcher', result, 'auth_refresh_failed');
    return result;
  }
}
