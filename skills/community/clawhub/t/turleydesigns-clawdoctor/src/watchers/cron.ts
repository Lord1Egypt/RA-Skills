import fs from 'fs';
import path from 'path';
import { BaseWatcher, WatchResult } from './base.js';

interface CronJobState {
  nextRunAtMs?: number;
  lastRunAtMs?: number;
  lastRunStatus?: string;
  lastStatus?: string;
  lastDurationMs?: number;
  consecutiveErrors?: number;
  lastDelivered?: boolean;
  lastDeliveryStatus?: string;
}

interface CronJob {
  id: string;
  name: string;
  enabled: boolean;
  schedule: { kind: string; expr?: string };
  state: CronJobState;
  delivery?: { mode?: string };
  agentId?: string;
}

interface CronJobsFile {
  version?: number;
  jobs: CronJob[];
}

export class CronWatcher extends BaseWatcher {
  readonly name = 'CronWatcher';
  readonly defaultInterval = 60;

  async check(): Promise<WatchResult[]> {
    const jobsFile = path.join(this.config.openclawPath, 'cron', 'jobs.json');
    const results: WatchResult[] = [];

    if (!fs.existsSync(jobsFile)) {
      results.push(this.ok('No cron jobs file found', 'cron_no_file'));
      return results;
    }

    let data: CronJobsFile;
    try {
      const raw = fs.readFileSync(jobsFile, 'utf-8');
      data = JSON.parse(raw) as CronJobsFile;
    } catch {
      results.push(this.warn(`Cannot parse cron jobs file: ${jobsFile}`, 'cron_parse_error'));
      return results;
    }

    const jobs = data.jobs ?? [];
    const enabledJobs = jobs.filter(j => j.enabled);

    if (enabledJobs.length === 0) {
      results.push(this.ok('No enabled cron jobs', 'cron_none_enabled'));
      return results;
    }

    let healthy = 0;
    let errored = 0;
    let overdue = 0;

    for (const job of enabledJobs) {
      const state = job.state ?? {};
      const name = job.name ?? job.id;

      // Check consecutive errors — but skip if last run was ok (cron recovered)
      if ((state.consecutiveErrors ?? 0) >= 3 && state.lastRunStatus !== 'ok') {
        results.push(
          this.error(
            `Cron '${name}' has ${state.consecutiveErrors} consecutive errors`,
            'cron_consecutive_errors',
            { cronName: name, jobId: job.id, consecutiveErrors: state.consecutiveErrors, lastStatus: state.lastRunStatus }
          )
        );
        errored++;
        continue;
      }

      // Check last run status — explicit error states only, skip if ok or absent
      if (state.lastRunStatus && state.lastRunStatus !== 'ok') {
        results.push(
          this.warn(
            `Cron '${name}' last run status: ${state.lastRunStatus}`,
            'cron_last_error',
            { cronName: name, jobId: job.id, lastRunStatus: state.lastRunStatus }
          )
        );
        errored++;
        continue;
      }

      // Check if overdue (should have run but nextRunAtMs is in the past by >2x the expected interval)
      if (state.nextRunAtMs) {
        const now = Date.now();
        const overdueMs = now - state.nextRunAtMs;
        // Consider overdue if more than 30 minutes past expected next run
        if (overdueMs > 30 * 60 * 1000) {
          results.push(
            this.warn(
              `Cron '${name}' overdue, was expected ${Math.round(overdueMs / 60000)}m ago`,
              'cron_overdue',
              { cronName: name, jobId: job.id, nextRunAtMs: state.nextRunAtMs, overdueMs }
            )
          );
          overdue++;
          continue;
        }
      }

      // Check delivery status — only flag actual error states, not idle/skipped states
      const deliveryMode = job.delivery?.mode ?? 'announce';
      const deliveryErrorStates = ['failed', 'error', 'timeout'];
      if (deliveryMode !== 'none' && state.lastDeliveryStatus && deliveryErrorStates.includes(state.lastDeliveryStatus)) {
        results.push(
          this.warn(
            `Cron '${name}' last delivery failed: ${state.lastDeliveryStatus}`,
            'cron_delivery_failed',
            { cronName: name, jobId: job.id, lastDeliveryStatus: state.lastDeliveryStatus }
          )
        );
        continue;
      }

      healthy++;
    }

    // Summary result
    if (errored === 0 && overdue === 0) {
      results.push(this.ok(`${healthy} cron job(s) healthy`, 'cron_all_ok'));
    }

    return results;
  }
}
