import { ClawDoctorConfig } from '../config.js';
import { insertEvent } from '../store.js';
import { nowIso } from '../utils.js';
import { createSnapshot } from '../snapshots.js';
import { appendAudit, AuditTier, AuditResult } from '../audit.js';

export interface HealResult {
  success: boolean;
  action: string;
  message: string;
  details?: Record<string, unknown>;
  tier?: AuditTier;
  requiresApproval?: boolean;
  approvalOptions?: Array<{ text: string; callbackData: string }>;
  snapshotId?: string;
}

export abstract class BaseHealer {
  abstract readonly name: string;

  protected config: ClawDoctorConfig;

  constructor(config: ClawDoctorConfig) {
    this.config = config;
  }

  abstract heal(context: Record<string, unknown>): Promise<HealResult>;

  protected async recordHeal(
    watcherName: string,
    result: HealResult,
    eventType: string
  ): Promise<void> {
    insertEvent({
      timestamp: nowIso(),
      watcher: watcherName,
      severity: result.success ? 'info' : 'error',
      event_type: eventType,
      message: result.message,
      details: result.details ? JSON.stringify(result.details) : undefined,
      action_taken: result.action,
      action_result: result.success ? 'success' : 'failed',
    });
  }

  protected takeSnapshot(
    action: string,
    target: string,
    before: Record<string, unknown>,
    rollbackCommand: string
  ): string {
    return createSnapshot(action, target, before, rollbackCommand);
  }

  protected writeAudit(
    action: string,
    target: string,
    tier: AuditTier,
    result: AuditResult,
    snapshotId?: string
  ): void {
    appendAudit({
      timestamp: nowIso(),
      healer: this.name,
      action,
      target,
      tier,
      result,
      snapshotId,
    });
  }

  protected isEffectiveDryRun(healerDryRun?: boolean): boolean {
    return this.config.dryRun || (healerDryRun ?? false);
  }
}
