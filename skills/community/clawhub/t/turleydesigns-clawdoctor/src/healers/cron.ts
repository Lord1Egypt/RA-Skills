import { BaseHealer, HealResult } from './base.js';
import { runCommand } from '../utils.js';

const TRANSIENT_ERROR_PATTERNS = [
  /network/i,
  /timeout/i,
  /ECONNRESET/i,
  /ECONNREFUSED/i,
  /ETIMEDOUT/i,
  /rate.?limit/i,
  /503/,
  /504/,
  /temporarily unavailable/i,
];

function isTransientError(errorMsg: string): boolean {
  return TRANSIENT_ERROR_PATTERNS.some(p => p.test(errorMsg));
}

export class CronHealer extends BaseHealer {
  readonly name = 'CronHealer';

  // Track our own consecutive failure count per cron (independent of OpenClaw's counter)
  private failureCounts: Map<string, number> = new Map();
  private lastRetryTime: Map<string, number> = new Map();

  private static readonly RETRY_COOLDOWN_MS = 10 * 60 * 1000; // 10 min between retries
  private static readonly AUTO_RETRY_THRESHOLD = 3; // retry after 3 consecutive detections
  private static readonly APPROVAL_THRESHOLD = 6; // ask user after 6 consecutive detections

  async heal(context: Record<string, unknown>): Promise<HealResult> {
    const cronName = (context.cronName as string | undefined) ?? 'unknown';
    const openclawConsecutive = (context.consecutiveErrors as number | undefined) ?? 0;
    const lastError = (context.lastError as string | undefined) ?? '';
    const lastRunStatus = (context.lastRunStatus as string | undefined) ?? '';
    const lastRun = (context.lastRun as string | undefined) ?? 'unknown';
    const dryRun = this.isEffectiveDryRun(this.config.healers.cronRetry.dryRun);

    // Reset our count if OpenClaw reports the cron recovered (consecutiveErrors back to 0)
    if (openclawConsecutive === 0) {
      this.failureCounts.delete(cronName);
      this.lastRetryTime.delete(cronName);
    }

    // Track our own failure count
    const currentCount = (this.failureCounts.get(cronName) ?? 0) + 1;
    this.failureCounts.set(cronName, currentCount);

    // Use the higher of OpenClaw's count or our own
    const consecutiveErrors = Math.max(openclawConsecutive, currentCount);

    // Yellow tier: persistent failures, ask via Telegram
    if (consecutiveErrors >= CronHealer.APPROVAL_THRESHOLD) {
      if (dryRun) {
        this.writeAudit('cron-ask', cronName, 'yellow', 'dry-run');
        return {
          success: true,
          action: `dry-run: would send Telegram approval for '${cronName}'`,
          message: `[DRY RUN] Would request approval for cron '${cronName}' (${consecutiveErrors} failures detected)`,
          tier: 'yellow',
        };
      }
      this.writeAudit('cron-ask', cronName, 'yellow', 'pending');
      const result: HealResult = {
        success: true,
        action: `requested approval for cron '${cronName}'`,
        message: `Cron '${cronName}' has failed ${consecutiveErrors} times. Approval requested.`,
        details: { cronName, consecutiveErrors, lastError, lastRun },
        tier: 'yellow',
        requiresApproval: true,
        approvalOptions: [
          { text: 'Retry Now', callbackData: `cron:retry:${cronName}` },
          { text: 'Disable', callbackData: `cron:disable:${cronName}` },
          { text: 'Ignore', callbackData: `cron:ignore:${cronName}` },
        ],
      };
      await this.recordHeal('CronWatcher', result, 'cron_approval_requested');
      return result;
    }

    // Green tier: auto-retry after threshold, with cooldown
    if (consecutiveErrors >= CronHealer.AUTO_RETRY_THRESHOLD) {
      const lastRetry = this.lastRetryTime.get(cronName) ?? 0;
      const now = Date.now();

      if (now - lastRetry < CronHealer.RETRY_COOLDOWN_MS) {
        // Still in cooldown, just log
        this.writeAudit('cron-log', cronName, 'green', 'pending');
        return {
          success: true,
          action: `retry cooldown for '${cronName}'`,
          message: `Cron '${cronName}' still failing (${consecutiveErrors}x). Next retry in ${Math.round((CronHealer.RETRY_COOLDOWN_MS - (now - lastRetry)) / 60000)}m.`,
          tier: 'green',
        };
      }

      if (dryRun) {
        this.writeAudit('cron-retry', cronName, 'green', 'dry-run');
        return {
          success: true,
          action: `dry-run: would retry '${cronName}'`,
          message: `[DRY RUN] Would retry cron '${cronName}' (${consecutiveErrors} failures)`,
          tier: 'green',
        };
      }

      // Take snapshot and retry
      const snapshotId = this.takeSnapshot(
        'cron-retry',
        cronName,
        { consecutiveErrors, lastError, lastRun, lastRunStatus },
        `openclaw cron disable ${cronName}`
      );

      const retryResult = runCommand('openclaw', ['cron', 'run', cronName]);
      this.lastRetryTime.set(cronName, now);

      if (retryResult.ok) {
        // Reset failure count on successful retry dispatch
        this.failureCounts.set(cronName, 0);
        const result: HealResult = {
          success: true,
          action: `openclaw cron run ${cronName}`,
          message: `Cron '${cronName}' retried after ${consecutiveErrors} failures`,
          details: { cronName, consecutiveErrors, lastError, snapshotId },
          tier: 'green',
          snapshotId,
        };
        await this.recordHeal('CronWatcher', result, 'cron_retried');
        this.writeAudit('cron-retry', cronName, 'green', 'success', snapshotId);
        return result;
      }

      const result: HealResult = {
        success: false,
        action: `openclaw cron run ${cronName}`,
        message: `Failed to retry cron '${cronName}': ${retryResult.stderr.slice(0, 200)}`,
        details: { cronName, consecutiveErrors, lastError, snapshotId },
        tier: 'green',
        snapshotId,
      };
      await this.recordHeal('CronWatcher', result, 'cron_retry_failed');
      this.writeAudit('cron-retry', cronName, 'green', 'failed', snapshotId);
      return result;
    }

    // Below threshold: just log with manual rerun command
    const manualCommand = cronName !== 'unknown'
      ? `openclaw cron run ${cronName}`
      : 'openclaw cron run <cron-name>';

    const result: HealResult = {
      success: true,
      action: `logged cron failure for '${cronName}'`,
      message: `Cron '${cronName}' failed (${consecutiveErrors}/${CronHealer.AUTO_RETRY_THRESHOLD} before auto-retry)${lastError ? `: ${lastError}` : ''}. Manual: \`${manualCommand}\``,
      details: { cronName, lastRun, lastError, manualCommand, consecutiveErrors },
      tier: 'green',
    };
    await this.recordHeal('CronWatcher', result, 'cron_failure_logged');
    this.writeAudit('cron-log', cronName, 'green', 'success');
    return result;
  }

  // Reset count when a cron starts passing again (called externally if needed)
  resetFailureCount(cronName: string): void {
    this.failureCounts.delete(cronName);
    this.lastRetryTime.delete(cronName);
  }
}
