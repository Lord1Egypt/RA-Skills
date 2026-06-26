import { execFileSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import { AGENTWATCH_DIR } from './config.js';

export const SNAPSHOTS_DIR = path.join(AGENTWATCH_DIR, 'snapshots');

const ALLOWED_ROLLBACK_PREFIXES = [
  'openclaw gateway',
  'openclaw cron',
  'openclaw session',
  'openclaw auth',
];

export interface Snapshot {
  timestamp: string;
  action: string;
  target: string;
  before: Record<string, unknown>;
  rollbackCommand: string;
}

export function createSnapshot(
  action: string,
  target: string,
  before: Record<string, unknown>,
  rollbackCommand: string
): string {
  fs.mkdirSync(SNAPSHOTS_DIR, { recursive: true, mode: 0o700 });
  const now = new Date();
  const datePart = now.toISOString().slice(0, 10);
  const timePart = now.toISOString().slice(11, 19).replace(/:/g, '');
  const id = `${datePart}-${timePart}-${action}`;
  const snapshot: Snapshot = {
    timestamp: now.toISOString(),
    action,
    target,
    before,
    rollbackCommand,
  };
  fs.writeFileSync(path.join(SNAPSHOTS_DIR, `${id}.json`), JSON.stringify(snapshot, null, 2), { encoding: 'utf-8', mode: 0o600 });
  return id;
}

export function listSnapshots(): Array<{ id: string; snapshot: Snapshot }> {
  if (!fs.existsSync(SNAPSHOTS_DIR)) return [];
  let files: string[];
  try {
    files = fs.readdirSync(SNAPSHOTS_DIR)
      .filter(f => f.endsWith('.json'))
      .sort()
      .reverse();
  } catch {
    return [];
  }
  return files.map(f => {
    const id = f.replace('.json', '');
    try {
      const snapshot = JSON.parse(fs.readFileSync(path.join(SNAPSHOTS_DIR, f), 'utf-8')) as Snapshot;
      return { id, snapshot };
    } catch {
      return null;
    }
  }).filter((x): x is { id: string; snapshot: Snapshot } => x !== null);
}

export function getSnapshot(id: string): Snapshot | null {
  const filePath = path.join(SNAPSHOTS_DIR, `${id}.json`);
  if (!fs.existsSync(filePath)) return null;
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf-8')) as Snapshot;
  } catch {
    return null;
  }
}

export function executeRollback(id: string): { success: boolean; message: string; snapshot?: Snapshot } {
  const snapshot = getSnapshot(id);
  if (!snapshot) {
    return { success: false, message: `Snapshot '${id}' not found` };
  }

  const cmd = snapshot.rollbackCommand;
  const allowed = ALLOWED_ROLLBACK_PREFIXES.some(prefix => cmd.startsWith(prefix));
  if (!allowed) {
    console.error(`[snapshots] Rollback rejected: command not in allowlist: ${cmd}`);
    return { success: false, message: `Rollback rejected: command not in allowlist` };
  }

  const [bin, ...args] = cmd.split(/\s+/);
  try {
    execFileSync(bin, args);
    return { success: true, message: `Rollback successful: ${cmd}`, snapshot };
  } catch (err) {
    return {
      success: false,
      message: `Rollback failed: ${String(err).slice(0, 200)}`,
      snapshot,
    };
  }
}
