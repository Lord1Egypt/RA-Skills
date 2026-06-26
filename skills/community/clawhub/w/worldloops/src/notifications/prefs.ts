import * as fs from 'node:fs';
import * as path from 'node:path';
import type { NotificationPrefs, MinSeverity } from '../types';

function getWorldLoopsDir(): string {
  return process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
}

export function getPrefsPath(): string {
  return path.join(getWorldLoopsDir(), 'notification_prefs.json');
}

export const VALID_CHANNELS = ['local', 'telegram', 'slack', 'discord', 'sms', 'email'] as const;
export type DeliveryChannel = (typeof VALID_CHANNELS)[number];
export const DEFAULT_BRIEF_CHANNEL: DeliveryChannel = 'local';

export const DEFAULT_PREFS: NotificationPrefs = {
  dailyBrief: {
    enabled: true,
    time: '09:00',
    timezone: 'UTC',
    channel: DEFAULT_BRIEF_CHANNEL,
    minimumSeverity: 'medium',
    sources: ['gmail', 'calendar', 'slack'],
  },
  proactiveDiscovery: {
    enabled: false,
    scanIntervalMinutes: 30,
    minSeverity: 'medium',
  },
  quietHours: {
    enabled: false,
    start: '21:00',
    end: '08:00',
  },
  eventAlerts: {
    enabled: false,
    rules: [],
  },
  channels: {
    cli: true,
  },
};

export function loadPrefs(): NotificationPrefs {
  const prefsPath = getPrefsPath();
  if (!fs.existsSync(prefsPath)) {
    return JSON.parse(JSON.stringify(DEFAULT_PREFS)) as NotificationPrefs;
  }
  return JSON.parse(fs.readFileSync(prefsPath, 'utf8')) as NotificationPrefs;
}

export function savePrefs(prefs: NotificationPrefs): void {
  const prefsPath = getPrefsPath();
  const dir = path.dirname(prefsPath);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  fs.writeFileSync(prefsPath, JSON.stringify(prefs, null, 2) + '\n', 'utf8');
}

export function initPrefs(): boolean {
  const prefsPath = getPrefsPath();
  if (fs.existsSync(prefsPath)) {
    return false;
  }
  savePrefs(DEFAULT_PREFS);
  return true;
}

export function setDotPath(obj: Record<string, unknown>, dotPath: string, value: unknown): void {
  const keys = dotPath.split('.');
  let current = obj;
  for (let i = 0; i < keys.length - 1; i++) {
    const key = keys[i];
    if (typeof current[key] !== 'object' || current[key] === null) {
      current[key] = {};
    }
    current = current[key] as Record<string, unknown>;
  }
  current[keys[keys.length - 1]] = value;
}

export function isInQuietHours(prefs: NotificationPrefs, now: Date = new Date()): boolean {
  if (!prefs.quietHours.enabled) return false;

  const [startH, startM] = prefs.quietHours.start.split(':').map(Number);
  const [endH, endM] = prefs.quietHours.end.split(':').map(Number);

  const currentMinutes = now.getHours() * 60 + now.getMinutes();
  const startMinutes = startH * 60 + startM;
  const endMinutes = endH * 60 + endM;

  // Spans midnight (e.g. 21:00–08:00)
  if (startMinutes > endMinutes) {
    return currentMinutes >= startMinutes || currentMinutes < endMinutes;
  }
  // Same day (e.g. 09:00–17:00)
  return currentMinutes >= startMinutes && currentMinutes < endMinutes;
}

const SEVERITY_RANK: Record<string, number> = {
  low: 0,
  medium: 1,
  high: 2,
  critical: 3,
};

export function meetsSeverity(candidateSeverity: string | undefined, minSeverity: MinSeverity): boolean {
  const candidateRank = SEVERITY_RANK[candidateSeverity ?? 'medium'] ?? 1;
  const minRank = SEVERITY_RANK[minSeverity] ?? 1;
  return candidateRank >= minRank;
}
