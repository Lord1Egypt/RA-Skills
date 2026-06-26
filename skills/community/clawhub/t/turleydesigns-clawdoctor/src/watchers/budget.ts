import fs from 'fs';
import path from 'path';
import { BaseWatcher, WatchResult } from './base.js';

interface SessionEntry {
  type?: string;
  usage?: {
    input_tokens?: number;
    output_tokens?: number;
    cost_usd?: number;
  };
  cost?: number;
  total_cost?: number;
}

export class BudgetWatcher extends BaseWatcher {
  readonly name = 'BudgetWatcher';
  readonly defaultInterval = 300;

  // Track which thresholds have already been alerted (reset at midnight UTC)
  private alertedDate = '';
  private alertedExceeded = false;

  async check(): Promise<WatchResult[]> {
    const { budget } = this.config;
    if (!budget?.enabled) {
      return [this.ok('Budget monitoring disabled', 'budget_disabled')];
    }

    const todayUtc = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
    if (todayUtc !== this.alertedDate) {
      // New day: reset
      this.alertedDate = todayUtc;
      this.alertedExceeded = false;
    }

    const dailySpend = this.calculateDailySpend(todayUtc);
    const limit = budget.dailyLimitUsd;

    if (dailySpend >= limit) {
      if (!this.alertedExceeded) {
        this.alertedExceeded = true;
        return [
          this.critical(
            `Daily budget exceeded: $${dailySpend.toFixed(2)} of $${limit.toFixed(2)} limit`,
            'budget_exceeded',
            { dailySpend, limit, date: todayUtc }
          ),
        ];
      }
      return [this.ok(`Budget exceeded ($${dailySpend.toFixed(2)}/$${limit.toFixed(2)}) - already alerted`, 'budget_exceeded_dedup')];
    }

    return [
      this.ok(
        `Daily spend $${dailySpend.toFixed(2)} of $${limit.toFixed(2)} limit`,
        'budget_ok'
      ),
    ];
  }

  private calculateDailySpend(todayUtc: string): number {
    const agentsDir = path.join(this.config.openclawPath, 'agents');
    if (!fs.existsSync(agentsDir)) return 0;

    let totalSpend = 0;
    const dayStart = new Date(todayUtc + 'T00:00:00.000Z').getTime();

    let agentDirs: string[];
    try {
      agentDirs = fs.readdirSync(agentsDir).filter(d => {
        try { return fs.statSync(path.join(agentsDir, d)).isDirectory(); }
        catch { return false; }
      });
    } catch { return 0; }

    for (const agentDir of agentDirs) {
      const sessionsDir = path.join(agentsDir, agentDir, 'sessions');
      if (!fs.existsSync(sessionsDir)) continue;

      let sessionFiles: string[];
      try {
        sessionFiles = fs.readdirSync(sessionsDir)
          .filter(f => f.endsWith('.jsonl'))
          .map(f => {
            const fp = path.join(sessionsDir, f);
            const stat = fs.statSync(fp);
            return { name: f, mtime: stat.mtime };
          })
          .filter(f => f.mtime.getTime() >= dayStart)
          .map(f => f.name);
      } catch { continue; }

      for (const sessionFile of sessionFiles) {
        const sessionPath = path.join(sessionsDir, sessionFile);
        totalSpend += this.extractSessionCost(sessionPath);
      }
    }

    return totalSpend;
  }

  private extractSessionCost(filePath: string): number {
    try {
      const lines = fs.readFileSync(filePath, 'utf-8').split('\n').filter(l => l.trim());
      let totalCost = 0;

      for (const line of lines) {
        try {
          const entry = JSON.parse(line) as SessionEntry;
          if (entry.usage?.cost_usd != null) {
            totalCost += entry.usage.cost_usd;
          } else if (entry.cost != null) {
            totalCost = entry.cost;
          } else if (entry.total_cost != null) {
            totalCost = entry.total_cost;
          } else if (entry.usage?.input_tokens != null || entry.usage?.output_tokens != null) {
            const inputTokens = entry.usage.input_tokens ?? 0;
            const outputTokens = entry.usage.output_tokens ?? 0;
            totalCost += (inputTokens * 3 + outputTokens * 15) / 1_000_000;
          }
        } catch { continue; }
      }

      return totalCost;
    } catch { return 0; }
  }
}
