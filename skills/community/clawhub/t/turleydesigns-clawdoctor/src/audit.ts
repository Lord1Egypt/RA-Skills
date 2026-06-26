import fs from 'fs';
import path from 'path';
import { AGENTWATCH_DIR } from './config.js';

export const AUDIT_PATH = path.join(AGENTWATCH_DIR, 'audit.jsonl');

export type AuditTier = 'green' | 'yellow';
export type AuditResult = 'success' | 'failed' | 'dry-run' | 'pending';

export interface AuditEntry {
  timestamp: string;
  healer: string;
  action: string;
  target: string;
  tier: AuditTier;
  result: AuditResult;
  snapshotId?: string;
}

export function appendAudit(entry: AuditEntry): void {
  fs.mkdirSync(path.dirname(AUDIT_PATH), { recursive: true });
  fs.appendFileSync(AUDIT_PATH, JSON.stringify(entry) + '\n', { encoding: 'utf-8', mode: 0o600 });
}

export function getRecentAudit(limit = 50): AuditEntry[] {
  if (!fs.existsSync(AUDIT_PATH)) return [];
  try {
    const lines = fs.readFileSync(AUDIT_PATH, 'utf-8').split('\n').filter(Boolean);
    return lines
      .slice(-limit)
      .map(l => {
        try { return JSON.parse(l) as AuditEntry; } catch { return null; }
      })
      .filter((x): x is AuditEntry => x !== null);
  } catch {
    return [];
  }
}
