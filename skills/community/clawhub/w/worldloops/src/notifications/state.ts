import * as fs from 'node:fs';
import * as path from 'node:path';
import type { NotificationState } from '../types';

function getWorldLoopsDir(): string {
  return process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
}

export function getStatePath(): string {
  return path.join(getWorldLoopsDir(), 'notification_state.json');
}

export function loadState(): NotificationState {
  const statePath = getStatePath();
  if (!fs.existsSync(statePath)) {
    return { suppressedKeys: [] };
  }
  return JSON.parse(fs.readFileSync(statePath, 'utf8')) as NotificationState;
}

export function saveState(state: NotificationState): void {
  const statePath = getStatePath();
  const dir = path.dirname(statePath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(statePath, JSON.stringify(state, null, 2) + '\n', 'utf8');
}
