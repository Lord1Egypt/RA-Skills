import fs from 'fs';
import path from 'path';
import os from 'os';
import { execFileSync } from 'child_process';
import { BaseWatcher, WatchResult } from './base.js';

const AUTH_PATTERNS = [
  /401/,
  /403/,
  /token expired/i,
  /auth failed/i,
  /unauthorized/i,
  /authentication error/i,
  /invalid token/i,
  /permission denied/i,
];

const MAX_LOG_LINES = 200;

// Thresholds for expiry warnings (seconds)
const EXPIRY_THRESHOLDS = [
  { seconds: 60 * 60,      severity: 'critical' as const, label: '1h'  },
  { seconds: 4 * 60 * 60,  severity: 'error'    as const, label: '4h'  },
  { seconds: 24 * 60 * 60, severity: 'warning'  as const, label: '24h' },
];

interface AuthProfile {
  [key: string]: unknown;
}

export class AuthWatcher extends BaseWatcher {
  readonly name = 'AuthWatcher';
  readonly defaultInterval = 60;

  // Track which (token, threshold) pairs have already been alerted
  private alertedTokenThresholds = new Set<string>();

  async check(): Promise<WatchResult[]> {
    const results: WatchResult[] = [];

    // Check for expiring OAuth tokens
    const expiryResults = this.checkTokenExpiry();
    results.push(...expiryResults);

    // Try to read from systemd journal
    const journalLines = this.readJournalLogs();
    if (journalLines !== null) {
      results.push(...this.analyzeLines(journalLines, 'systemd journal'));
      return results;
    }

    // Try to find gateway log files
    const logLines = this.readLogFiles();
    if (logLines !== null) {
      results.push(...this.analyzeLines(logLines, 'log file'));
      return results;
    }

    if (results.length === 0) {
      results.push(this.ok('No gateway logs accessible for auth check', 'auth_no_logs'));
    }
    return results;
  }

  private checkTokenExpiry(): WatchResult[] {
    const results: WatchResult[] = [];
    const agentsDir = path.join(this.config.openclawPath, 'agents');
    if (!fs.existsSync(agentsDir)) return results;

    let agentDirs: string[];
    try {
      agentDirs = fs.readdirSync(agentsDir).filter(d => {
        try { return fs.statSync(path.join(agentsDir, d)).isDirectory(); }
        catch { return false; }
      });
    } catch { return results; }

    const now = Date.now();

    for (const agentDir of agentDirs) {
      const profilePath = path.join(agentsDir, agentDir, 'agent', 'auth-profiles.json');
      if (!fs.existsSync(profilePath)) continue;

      let profiles: AuthProfile;
      try {
        profiles = JSON.parse(fs.readFileSync(profilePath, 'utf-8')) as AuthProfile;
      } catch { continue; }

      this.findExpiryFields(profiles, agentDir, now, results);
    }

    return results;
  }

  private findExpiryFields(
    obj: unknown,
    agentDir: string,
    now: number,
    results: WatchResult[],
    keyPath = ''
  ): void {
    if (obj === null || typeof obj !== 'object') return;

    for (const [key, value] of Object.entries(obj as Record<string, unknown>)) {
      const currentPath = keyPath ? `${keyPath}.${key}` : key;

      if ((key === 'expires_at' || key === 'expiresAt') && (typeof value === 'number' || typeof value === 'string')) {
        const expiresAtMs = typeof value === 'number'
          ? (value > 1e10 ? value : value * 1000) // handle seconds vs ms
          : new Date(value as string).getTime();

        if (isNaN(expiresAtMs)) continue;

        const secsUntilExpiry = (expiresAtMs - now) / 1000;
        if (secsUntilExpiry <= 0) continue; // already expired; handled by regular auth failure detection

        for (const threshold of EXPIRY_THRESHOLDS) {
          if (secsUntilExpiry <= threshold.seconds) {
            const dedupKey = `${agentDir}:${currentPath}:${threshold.label}`;
            if (this.alertedTokenThresholds.has(dedupKey)) continue;
            this.alertedTokenThresholds.add(dedupKey);

            const minsLeft = Math.round(secsUntilExpiry / 60);
            const msg = `Auth token expiring in ${minsLeft}m for agent '${agentDir}' (${currentPath})`;
            const detail = { agent: agentDir, tokenPath: currentPath, secsUntilExpiry, threshold: threshold.label };

            if (threshold.severity === 'critical') {
              results.push(this.critical(msg, 'auth_expiring_soon', detail));
            } else if (threshold.severity === 'error') {
              results.push(this.error(msg, 'auth_expiring_soon', detail));
            } else {
              results.push(this.warn(msg, 'auth_expiring_soon', detail));
            }
            break; // only alert for the most severe applicable threshold
          }
        }
      } else if (typeof value === 'object' && value !== null) {
        this.findExpiryFields(value, agentDir, now, results, currentPath);
      }
    }
  }

  private readJournalLogs(): string[] | null {
    try {
      const output = execFileSync(
        'journalctl',
        ['-u', 'openclaw-gateway', '--since', '5 minutes ago', '--no-pager', '-q'],
        { encoding: 'utf-8', timeout: 5000 }
      );
      return output.split('\n').slice(-MAX_LOG_LINES);
    } catch {
      return null;
    }
  }

  private readLogFiles(): string[] | null {
    const logPaths = [
      `${this.config.openclawPath}/logs/gateway.log`,
      `${this.config.openclawPath}/gateway.log`,
    ];

    for (const logPath of logPaths) {
      try {
        const output = execFileSync('tail', ['-n', String(MAX_LOG_LINES), logPath], {
          encoding: 'utf-8',
          timeout: 3000,
        });
        return output.split('\n');
      } catch {
        continue;
      }
    }
    return null;
  }

  private analyzeLines(lines: string[], source: string): WatchResult[] {
    const matches: string[] = [];

    for (const line of lines) {
      if (AUTH_PATTERNS.some(pattern => pattern.test(line))) {
        matches.push(line.trim());
      }
    }

    if (matches.length === 0) {
      return [this.ok(`No auth failures detected in ${source}`, 'auth_ok')];
    }

    return [
      this.error(
        `${matches.length} auth failure(s) detected in ${source}`,
        'auth_failure',
        { count: matches.length, samples: matches.slice(0, 3) }
      ),
    ];
  }
}
