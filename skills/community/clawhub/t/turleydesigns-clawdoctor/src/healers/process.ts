import { BaseHealer, HealResult } from './base.js';
import { runShell, sleep } from '../utils.js';

export class ProcessHealer extends BaseHealer {
  readonly name = 'ProcessHealer';

  async heal(_context: Record<string, unknown>): Promise<HealResult> {
    const dryRun = this.isEffectiveDryRun(this.config.healers.processRestart.dryRun);

    if (dryRun) {
      this.writeAudit('restart-gateway', 'openclaw-gateway', 'green', 'dry-run');
      return {
        success: true,
        action: 'dry-run: would restart gateway',
        message: '[DRY RUN] Would restart openclaw gateway',
        tier: 'green',
      };
    }

    // Snapshot current state before acting
    const statusBefore = runShell('openclaw gateway status 2>/dev/null || echo "unknown"');
    const snapshotId = this.takeSnapshot(
      'gateway-restart',
      'openclaw-gateway',
      { statusBefore: statusBefore.stdout.trim() },
      'openclaw gateway stop'
    );

    // Try systemctl first
    const systemctlStatus = runShell('systemctl is-enabled openclaw-gateway 2>/dev/null');
    if (systemctlStatus.ok && systemctlStatus.stdout.trim() === 'enabled') {
      const restartResult = runShell('systemctl restart openclaw-gateway');
      if (restartResult.ok) {
        await sleep(10000);
        const verifyResult = runShell('systemctl is-active openclaw-gateway 2>/dev/null');
        if (verifyResult.ok && verifyResult.stdout.trim() === 'active') {
          const result: HealResult = {
            success: true,
            action: 'systemctl restart openclaw-gateway',
            message: 'Gateway restarted via systemd and verified running',
            tier: 'green',
            snapshotId,
          };
          await this.recordHeal('GatewayWatcher', result, 'gateway_restarted');
          this.writeAudit('restart-gateway', 'openclaw-gateway', 'green', 'success', snapshotId);
          return result;
        }
        const result: HealResult = {
          success: false,
          action: 'systemctl restart openclaw-gateway',
          message: 'Gateway restarted via systemd but failed to verify running after 10s',
          tier: 'green',
          snapshotId,
        };
        await this.recordHeal('GatewayWatcher', result, 'gateway_restart_failed');
        this.writeAudit('restart-gateway', 'openclaw-gateway', 'green', 'failed', snapshotId);
        return result;
      }
    }

    // Try openclaw gateway restart
    const openclaw = runShell('openclaw gateway restart');
    if (openclaw.ok) {
      await sleep(10000);
      const verify = runShell('pgrep -f "openclaw"');
      if (verify.ok && verify.stdout.trim().length > 0) {
        const result: HealResult = {
          success: true,
          action: 'openclaw gateway restart',
          message: 'Gateway restarted via openclaw CLI and verified running',
          tier: 'green',
          snapshotId,
        };
        await this.recordHeal('GatewayWatcher', result, 'gateway_restarted');
        this.writeAudit('restart-gateway', 'openclaw-gateway', 'green', 'success', snapshotId);
        return result;
      }
    }

    const result: HealResult = {
      success: false,
      action: 'attempted restart',
      message: `Failed to restart gateway. stdout: ${openclaw.stdout.slice(0, 200)} stderr: ${openclaw.stderr.slice(0, 200)}`,
      details: { stdout: openclaw.stdout, stderr: openclaw.stderr },
      tier: 'green',
      snapshotId,
    };
    await this.recordHeal('GatewayWatcher', result, 'gateway_restart_failed');
    this.writeAudit('restart-gateway', 'openclaw-gateway', 'green', 'failed', snapshotId);
    return result;
  }
}
