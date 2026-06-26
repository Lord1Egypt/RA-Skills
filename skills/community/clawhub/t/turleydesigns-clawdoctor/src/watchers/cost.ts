import fs from 'fs';
import path from 'path';
import { BaseWatcher, WatchResult } from './base.js';
import { fileAgeSeconds } from '../utils.js';

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

interface SessionCost {
  agent: string;
  session: string;
  cost: number;
  timestamp: Date;
}

const ROLLING_WINDOW = 20;
const ANOMALY_MULTIPLIER = 3;
const RECENT_HOURS = 1;

export class CostWatcher extends BaseWatcher {
  readonly name = 'CostWatcher';
  readonly defaultInterval = 300;

  async check(): Promise<WatchResult[]> {
    const agentsDir = path.join(this.config.openclawPath, 'agents');
    const results: WatchResult[] = [];

    if (!fs.existsSync(agentsDir)) {
      results.push(this.ok('No agents directory found', 'cost_no_agents_dir'));
      return results;
    }

    const sessionCosts = this.collectSessionCosts(agentsDir);

    if (sessionCosts.length < 2) {
      results.push(this.ok('Not enough sessions to calculate cost baseline', 'cost_no_baseline'));
      return results;
    }

    // Sort by timestamp, newest last
    sessionCosts.sort((a, b) => a.timestamp.getTime() - b.timestamp.getTime());

    // Check recent sessions against rolling average
    const recentCutoff = new Date(Date.now() - RECENT_HOURS * 3600 * 1000);
    const recentSessions = sessionCosts.filter(s => s.timestamp > recentCutoff);

    if (recentSessions.length === 0) {
      results.push(this.ok('No recent sessions to check for cost anomalies', 'cost_ok'));
      return results;
    }

    // Calculate rolling average from last ROLLING_WINDOW sessions (excluding recent ones)
    const historicalSessions = sessionCosts
      .filter(s => s.timestamp <= recentCutoff)
      .slice(-ROLLING_WINDOW);

    if (historicalSessions.length === 0) {
      results.push(this.ok('No historical sessions for cost baseline yet', 'cost_no_baseline'));
      return results;
    }

    const avgCost = historicalSessions.reduce((sum, s) => sum + s.cost, 0) / historicalSessions.length;
    const threshold = avgCost * ANOMALY_MULTIPLIER;

    const anomalies = recentSessions.filter(s => s.cost > threshold && s.cost > 0.01);

    if (anomalies.length === 0) {
      results.push(
        this.ok(
          `Cost normal, avg $${avgCost.toFixed(4)}/session, ${recentSessions.length} recent session(s) checked`,
          'cost_ok'
        )
      );
    } else {
      for (const anomaly of anomalies) {
        results.push(
          this.error(
            `Cost anomaly in agent '${anomaly.agent}': $${anomaly.cost.toFixed(4)} (${Math.round(anomaly.cost / avgCost)}x avg of $${avgCost.toFixed(4)})`,
            'cost_anomaly',
            {
              agent: anomaly.agent,
              session: anomaly.session,
              cost: anomaly.cost,
              avgCost,
              multiplier: anomaly.cost / avgCost,
            }
          )
        );
      }
    }

    return results;
  }

  private collectSessionCosts(agentsDir: string): SessionCost[] {
    const costs: SessionCost[] = [];

    let agentDirs: string[];
    try {
      agentDirs = fs.readdirSync(agentsDir).filter(d => {
        try { return fs.statSync(path.join(agentsDir, d)).isDirectory(); }
        catch { return false; }
      });
    } catch { return costs; }

    for (const agentDir of agentDirs) {
      const sessionsDir = path.join(agentsDir, agentDir, 'sessions');
      if (!fs.existsSync(sessionsDir)) continue;

      let sessionFiles: string[];
      try {
        sessionFiles = fs.readdirSync(sessionsDir)
          .filter(f => f.endsWith('.jsonl'))
          .map(f => {
            const stat = fs.statSync(path.join(sessionsDir, f));
            return { name: f, mtime: stat.mtime };
          })
          .filter(f => fileAgeSeconds(f.mtime) < 7 * 24 * 3600) // last 7 days
          .sort((a, b) => a.mtime.getTime() - b.mtime.getTime())
          .map(f => f.name);
      } catch { continue; }

      for (const sessionFile of sessionFiles) {
        const sessionPath = path.join(sessionsDir, sessionFile);
        const cost = this.extractSessionCost(sessionPath);
        if (cost !== null) {
          const stat = fs.statSync(sessionPath);
          costs.push({ agent: agentDir, session: sessionFile, cost, timestamp: stat.mtime });
        }
      }
    }

    return costs;
  }

  private extractSessionCost(filePath: string): number | null {
    try {
      const lines = fs.readFileSync(filePath, 'utf-8').split('\n').filter(l => l.trim());
      let totalCost = 0;
      let found = false;

      for (const line of lines) {
        try {
          const entry = JSON.parse(line) as SessionEntry;

          if (entry.usage?.cost_usd != null) {
            totalCost += entry.usage.cost_usd;
            found = true;
          } else if (entry.cost != null) {
            totalCost = entry.cost; // use last total_cost if available
            found = true;
          } else if (entry.total_cost != null) {
            totalCost = entry.total_cost;
            found = true;
          } else if (entry.usage?.input_tokens != null || entry.usage?.output_tokens != null) {
            // Estimate cost: ~$3/M input, ~$15/M output (Claude Sonnet ballpark)
            const inputTokens = entry.usage.input_tokens ?? 0;
            const outputTokens = entry.usage.output_tokens ?? 0;
            totalCost += (inputTokens * 3 + outputTokens * 15) / 1_000_000;
            found = true;
          }
        } catch { continue; }
      }

      return found ? totalCost : null;
    } catch { return null; }
  }
}
