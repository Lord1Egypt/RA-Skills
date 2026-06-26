import { execFileSync } from 'child_process';
import { ClawDoctorConfig, loadLicense, refreshEnvKeyCache, Plan } from './config.js';
import { BaseWatcher, WatchResult } from './watchers/base.js';
import { GatewayWatcher } from './watchers/gateway.js';
import { CronWatcher } from './watchers/cron.js';
import { SessionWatcher } from './watchers/session.js';
import { AuthWatcher } from './watchers/auth.js';
import { CostWatcher } from './watchers/cost.js';
import { BudgetWatcher } from './watchers/budget.js';
import { ProcessHealer } from './healers/process.js';
import { CronHealer } from './healers/cron.js';
import { AuthHealer } from './healers/auth.js';
import { SessionHealer } from './healers/session.js';
import { BudgetHealer } from './healers/budget.js';
import { HealResult } from './healers/base.js';
import { TelegramAlerter } from './alerters/telegram.js';
import { pruneOldEvents, getDedupTimestamp, setDedupTimestamp, pruneDedup } from './store.js';
import { nowIso } from './utils.js';

interface WatcherEntry {
  watcher: BaseWatcher;
  intervalMs: number;
  lastRun: number;
}

// Max monitors per plan
const PLAN_MONITOR_LIMITS: Record<Plan, number> = {
  free: 5,
  diagnose: 20,
  heal: Infinity,
};

// Plans that allow auto-fix
const AUTO_FIX_PLANS: Plan[] = ['heal'];

// Retention days per plan
const PLAN_RETENTION_DAYS: Record<Plan, number> = {
  free: 7,
  diagnose: 30,
  heal: 90,
};

export class Daemon {
  private config: ClawDoctorConfig;
  private watchers: WatcherEntry[] = [];
  private alerter: TelegramAlerter;
  private processHealer: ProcessHealer;
  private cronHealer: CronHealer;
  private authHealer: AuthHealer;
  private sessionHealer: SessionHealer;
  private budgetHealer: BudgetHealer;
  private running = false;
  private tickInterval: NodeJS.Timeout | null = null;
  private plan: Plan = 'free';
  private licenseCheckInterval: NodeJS.Timeout | null = null;
  private callbackPollInterval: NodeJS.Timeout | null = null;
  private callbackRateLimit = new Map<string, number>();
  private readonly CALLBACK_DEBOUNCE_MS = 10_000;

  constructor(config: ClawDoctorConfig) {
    this.config = config;
    this.alerter = new TelegramAlerter(config);
    this.processHealer = new ProcessHealer(config);
    this.cronHealer = new CronHealer(config);
    this.authHealer = new AuthHealer(config);
    this.sessionHealer = new SessionHealer(config);
    this.budgetHealer = new BudgetHealer(config);
    this.plan = loadLicense()?.plan ?? 'free';
    // Enforce tier-appropriate retention; override any manual config
    this.config.retentionDays = PLAN_RETENTION_DAYS[this.plan];
    // Heal plan: ensure healers are active (dryRun=false); non-heal: force dryRun=true
    const healPlanActive = this.plan === 'heal';
    for (const key of Object.keys(this.config.healers) as Array<keyof typeof this.config.healers>) {
      this.config.healers[key].dryRun = !healPlanActive;
    }
    this.setupWatchers();
  }

  private setupWatchers(): void {
    const { watchers } = this.config;
    const maxMonitors = PLAN_MONITOR_LIMITS[this.plan];

    // Build candidate list; free plan gets gateway + first 4 crons/others
    const candidates: WatcherEntry[] = [];

    if (watchers.gateway.enabled) {
      candidates.push({
        watcher: new GatewayWatcher(this.config),
        intervalMs: watchers.gateway.interval * 1000,
        lastRun: 0,
      });
    }
    if (watchers.cron.enabled) {
      candidates.push({
        watcher: new CronWatcher(this.config),
        intervalMs: watchers.cron.interval * 1000,
        lastRun: 0,
      });
    }
    if (watchers.session.enabled) {
      candidates.push({
        watcher: new SessionWatcher(this.config),
        intervalMs: watchers.session.interval * 1000,
        lastRun: 0,
      });
    }
    if (watchers.auth.enabled) {
      candidates.push({
        watcher: new AuthWatcher(this.config),
        intervalMs: watchers.auth.interval * 1000,
        lastRun: 0,
      });
    }
    if (watchers.cost.enabled) {
      candidates.push({
        watcher: new CostWatcher(this.config),
        intervalMs: watchers.cost.interval * 1000,
        lastRun: 0,
      });
    }
    if (this.config.budget?.enabled) {
      candidates.push({
        watcher: new BudgetWatcher(this.config),
        intervalMs: 300 * 1000,
        lastRun: 0,
      });
    }

    // Apply monitor limit
    this.watchers = candidates.slice(0, maxMonitors);

    if (candidates.length > this.watchers.length) {
      console.log(`[tier] Free plan: limited to ${maxMonitors} monitors. Upgrade at https://clawdoctor.dev/#pricing`);
    }
  }

  start(): void {
    if (this.running) return;
    this.running = true;

    console.log(`[${nowIso()}] ClawDoctor daemon started`);
    console.log(`[${nowIso()}] Plan: ${this.plan.toUpperCase()}`);
    console.log(`[${nowIso()}] Monitoring ${this.watchers.length} watcher(s)`);

    // Refresh env key plan cache in background (updates plan on next restart if changed)
    const envKey = process.env.CLAWDOCTOR_KEY;
    if (envKey) {
      refreshEnvKeyCache(envKey).then(() => {
        const refreshedPlan = loadLicense()?.plan ?? 'free';
        if (refreshedPlan !== this.plan) {
          console.log(`[${nowIso()}] Plan updated from env key validation: ${this.plan} -> ${refreshedPlan}`);
          this.plan = refreshedPlan;
          this.config.retentionDays = PLAN_RETENTION_DAYS[this.plan];
          this.watchers = [];
          this.setupWatchers();
        }
      }).catch(() => {
        // Non-fatal: keep current plan
      });
    }

    if (this.config.dryRun) {
      console.log(`[${nowIso()}] DRY RUN mode - healers will not take action`);
    }

    // Run all watchers immediately on start
    this.tick();

    // Tick every 5 seconds to check if any watcher is due
    this.tickInterval = setInterval(() => this.tick(), 5000);

    // Poll Telegram callback queries every 10 seconds
    this.callbackPollInterval = setInterval(() => {
      this.alerter.pollCallbacks().catch(err => {
        console.error(`[${nowIso()}] Callback poll error:`, err);
      });
    }, 10000);

    // Prune old events daily
    setInterval(() => {
      const pruned = pruneOldEvents(this.config.retentionDays);
      if (pruned > 0) {
        console.log(`[${nowIso()}] Pruned ${pruned} old event(s)`);
      }
    }, 24 * 3600 * 1000);

    // Re-check license weekly
    this.licenseCheckInterval = setInterval(() => {
      const updatedPlan = loadLicense()?.plan ?? 'free';
      if (updatedPlan !== this.plan) {
        console.log(`[${nowIso()}] Plan changed: ${this.plan} -> ${updatedPlan}. Reloading watchers.`);
        this.plan = updatedPlan;
        this.config.retentionDays = PLAN_RETENTION_DAYS[this.plan];
        this.watchers = [];
        this.setupWatchers();
      }
    }, 7 * 24 * 3600 * 1000);
  }

  stop(): void {
    if (!this.running) return;
    this.running = false;
    if (this.tickInterval) {
      clearInterval(this.tickInterval);
      this.tickInterval = null;
    }
    if (this.licenseCheckInterval) {
      clearInterval(this.licenseCheckInterval);
      this.licenseCheckInterval = null;
    }
    if (this.callbackPollInterval) {
      clearInterval(this.callbackPollInterval);
      this.callbackPollInterval = null;
    }
    console.log(`[${nowIso()}] ClawDoctor daemon stopped`);
  }

  private tick(): void {
    const now = Date.now();
    for (const entry of this.watchers) {
      if (now - entry.lastRun >= entry.intervalMs) {
        entry.lastRun = now;
        this.runWatcher(entry.watcher).catch(err => {
          console.error(`[${nowIso()}] Error in ${entry.watcher.name}:`, err);
        });
      }
    }
  }

  private async runWatcher(watcher: BaseWatcher): Promise<void> {
    try {
      const results = await watcher.run();
      for (const result of results) {
        await this.handleResult(watcher, result);
      }
    } catch (err) {
      console.error(`[${nowIso()}] ${watcher.name} threw:`, err);
    }
  }

  private async handleResult(watcher: BaseWatcher, result: WatchResult): Promise<void> {
    const prefix = `[${nowIso()}] [${watcher.name}]`;

    if (result.severity !== 'info') {
      console.log(`${prefix} ${result.severity.toUpperCase()}: ${result.message}`);
    }

    // Auto-healing
    if (!result.ok) {
      const healResult = await this.attemptHeal(watcher, result);
      if (healResult) {
        // Yellow tier with approval needed: send inline keyboard
        if (healResult.requiresApproval && healResult.approvalOptions) {
          await this.sendApprovalRequest(watcher.name, healResult);
        } else if (this.alerter.shouldAlert(result)) {
          await this.alerter.sendAlert({ watcher: watcher.name, result, healResult });
        }
      } else if (this.alerter.shouldAlert(result)) {
        await this.alerter.sendAlert({ watcher: watcher.name, result });
      }
    }
  }

  private readonly APPROVAL_DEDUP_MS = 60 * 60 * 1000; // 1 hour

  private async sendApprovalRequest(watcherName: string, healResult: HealResult): Promise<void> {
    // Deduplicate: only send one approval request per watcher per hour.
    // State is persisted to SQLite so restarts don't reset the window.
    const dedupKey = `approval:${watcherName}:${healResult.action}`;
    const lastSent = getDedupTimestamp(dedupKey);
    if (Date.now() - lastSent < this.APPROVAL_DEDUP_MS) {
      return;
    }
    setDedupTimestamp(dedupKey, Date.now());

    const options = healResult.approvalOptions ?? [];
    const { text, buttons, suggestions } = this.alerter.formatApprovalMessage(
      watcherName,
      healResult.message,
      options
    );

    const handlers: Record<string, () => Promise<void>> = {};

    for (const option of options) {
      const cbData = option.callbackData;
      handlers[cbData] = async () => {
        await this.handleCallbackAction(cbData);
      };
    }

    await this.alerter.sendWithButtons(text, buttons, handlers, suggestions);
  }

  private async handleCallbackAction(callbackData: string): Promise<void> {
    const now = Date.now();
    const lastRun = this.callbackRateLimit.get(callbackData) ?? 0;
    if (now - lastRun < this.CALLBACK_DEBOUNCE_MS) {
      console.log(`[${nowIso()}] [Daemon] Callback rate-limited (10s debounce): ${callbackData}`);
      return;
    }
    this.callbackRateLimit.set(callbackData, now);

    console.log(`[${nowIso()}] [Daemon] Handling callback: ${callbackData}`);
    const parts = callbackData.split(':');
    const [resource, action, ...args] = parts;

    if (resource === 'cron') {
      const cronName = args[0] ?? 'unknown';
      if (action === 'retry') {
        try {
          execFileSync('openclaw', ['cron', 'run', cronName]);
          console.log(`[${nowIso()}] [CronHealer] Retry ${cronName}: success`);
        } catch {
          console.log(`[${nowIso()}] [CronHealer] Retry ${cronName}: failed`);
        }
      } else if (action === 'disable') {
        try {
          execFileSync('openclaw', ['cron', 'disable', cronName]);
          console.log(`[${nowIso()}] [CronHealer] Disable ${cronName}: success`);
        } catch {
          console.log(`[${nowIso()}] [CronHealer] Disable ${cronName}: failed`);
        }
      } else if (action === 'ignore') {
        console.log(`[${nowIso()}] [CronHealer] Ignored alert for ${cronName}`);
      }
    } else if (resource === 'budget') {
      if (action === 'kill_all') {
        const { killed, failed } = await this.budgetHealer.killAllSessions();
        console.log(`[${nowIso()}] [BudgetHealer] Emergency stop: ${killed} killed, ${failed} failed`);
      } else if (action === 'increase') {
        const newLimit = parseFloat(args[0] ?? '0');
        if (newLimit > 0) {
          this.config.budget.dailyLimitUsd = newLimit;
          console.log(`[${nowIso()}] [BudgetHealer] Daily limit increased to $${newLimit}`);
        }
      } else if (action === 'ignore') {
        console.log(`[${nowIso()}] [BudgetHealer] Budget alert ignored`);
      }
    } else if (resource === 'session') {
      const agent = args[0] ?? 'unknown';
      const session = args[1] ?? 'unknown';
      if (action === 'kill') {
        try {
          execFileSync('openclaw', ['session', 'kill', agent, session]);
          console.log(`[${nowIso()}] [SessionHealer] Kill ${agent}/${session}: success`);
        } catch {
          console.log(`[${nowIso()}] [SessionHealer] Kill ${agent}/${session}: failed`);
        }
      } else if (action === 'ignore') {
        console.log(`[${nowIso()}] [SessionHealer] Ignored alert for ${agent}/${session}`);
      }
    }
  }

  private async attemptHeal(
    watcher: BaseWatcher,
    result: WatchResult
  ): Promise<HealResult | null> {
    const autoFixAllowed = AUTO_FIX_PLANS.includes(this.plan);

    if (watcher.name === 'GatewayWatcher' && result.event_type === 'gateway_down') {
      if (this.config.healers.processRestart.enabled && autoFixAllowed) {
        console.log(`[${nowIso()}] [ProcessHealer] Attempting to restart gateway...`);
        const healResult = await this.processHealer.heal({});
        console.log(`[${nowIso()}] [ProcessHealer] ${healResult.success ? 'SUCCESS' : 'FAILED'}: ${healResult.message}`);
        return healResult;
      } else if (!autoFixAllowed) {
        console.log(`[${nowIso()}] [ProcessHealer] Auto-fix requires Heal plan. Upgrade at https://clawdoctor.dev/#pricing`);
      }
    }

    if (watcher.name === 'CronWatcher' && (result.event_type === 'cron_consecutive_errors' || result.event_type === 'cron_overdue' || result.event_type === 'cron_last_error')) {
      if (this.config.healers.cronRetry.enabled && autoFixAllowed) {
        const context = result.details ?? {};
        const healResult = await this.cronHealer.heal(context as Record<string, unknown>);
        console.log(`[${nowIso()}] [CronHealer] ${healResult.success ? 'SUCCESS' : 'FAILED'}: ${healResult.message}`);
        return healResult;
      } else if (!autoFixAllowed) {
        // Still log, even on non-heal plans
        const context = result.details ?? {};
        return await this.cronHealer.heal(context as Record<string, unknown>);
      }
    }

    if (watcher.name === 'AuthWatcher' && result.event_type === 'auth_failure') {
      if (this.config.healers.auth.enabled && autoFixAllowed) {
        const context = result.details ?? {};
        const healResult = await this.authHealer.heal(context as Record<string, unknown>);
        console.log(`[${nowIso()}] [AuthHealer] ${healResult.success ? 'SUCCESS' : 'FAILED'}: ${healResult.message}`);
        return healResult;
      }
    }

    if (watcher.name === 'SessionWatcher' && (result.event_type === 'session_stuck' || result.event_type === 'session_error')) {
      if (this.config.healers.session.enabled && autoFixAllowed) {
        const context = result.details ?? {};
        const healResult = await this.sessionHealer.heal(context as Record<string, unknown>);
        console.log(`[${nowIso()}] [SessionHealer] ${healResult.success ? 'SUCCESS' : 'FAILED'}: ${healResult.message}`);
        return healResult;
      }
    }

    if (watcher.name === 'BudgetWatcher' && result.event_type === 'budget_exceeded') {
      if (autoFixAllowed) {
        const context = result.details ?? {};
        const healResult = await this.budgetHealer.heal(context as Record<string, unknown>);
        console.log(`[${nowIso()}] [BudgetHealer] ${healResult.success ? 'SUCCESS' : 'FAILED'}: ${healResult.message}`);
        return healResult;
      }
    }

    return null;
  }

  async runOnce(): Promise<Map<string, WatchResult[]>> {
    const allResults = new Map<string, WatchResult[]>();
    for (const entry of this.watchers) {
      try {
        const results = await entry.watcher.check();
        allResults.set(entry.watcher.name, results);
      } catch (err) {
        allResults.set(entry.watcher.name, [{
          ok: false,
          severity: 'error',
          event_type: 'watcher_error',
          message: `Watcher threw: ${String(err)}`,
        }]);
      }
    }
    return allResults;
  }
}
