import fs from 'fs';
import path from 'path';
import os from 'os';
import https from 'https';

export interface WatcherConfig {
  enabled: boolean;
  interval: number;
}

export interface HealerConfig {
  enabled: boolean;
  dryRun?: boolean;
}

export interface TelegramConfig {
  enabled: boolean;
  botToken: string;
  chatId: string;
  /**
   * Optional: a separate bot token dedicated to receiving callback_query updates
   * (inline button presses). If set, ClawDoctor will poll this bot for callbacks
   * and show inline buttons in alerts. If omitted, alerts fall back to plain text
   * suggestions (e.g. "Run: clawdoctor retry metrics-collector") to avoid
   * conflicts with other processes polling the same bot token (e.g. OpenClaw).
   */
  callbackBotToken?: string;
}

export interface AlertsConfig {
  telegram: TelegramConfig;
}

export interface BudgetConfig {
  enabled: boolean;
  dailyLimitUsd: number;
}

export interface ClawDoctorConfig {
  openclawPath: string;
  watchers: {
    gateway: WatcherConfig;
    cron: WatcherConfig;
    session: WatcherConfig;
    auth: WatcherConfig;
    cost: WatcherConfig;
  };
  healers: {
    processRestart: HealerConfig;
    cronRetry: HealerConfig;
    auth: HealerConfig;
    session: HealerConfig;
  };
  alerts: AlertsConfig;
  budget: BudgetConfig;
  dryRun: boolean;
  retentionDays: number;
}

export const AGENTWATCH_DIR = path.join(os.homedir(), '.clawdoctor');
export const CONFIG_PATH = path.join(AGENTWATCH_DIR, 'config.json');
export const DB_PATH = path.join(AGENTWATCH_DIR, 'events.db');
export const PID_PATH = path.join(AGENTWATCH_DIR, 'clawdoctor.pid');
export const LICENSE_PATH = path.join(AGENTWATCH_DIR, 'license.json');
export const SNAPSHOTS_DIR = path.join(AGENTWATCH_DIR, 'snapshots');
export const AUDIT_PATH = path.join(AGENTWATCH_DIR, 'audit.jsonl');
export const ENV_KEY_CACHE_PATH = path.join(AGENTWATCH_DIR, 'env-key-cache.json');

export type Plan = 'free' | 'diagnose' | 'heal';

export interface LicenseInfo {
  key: string;
  plan: Plan;
  features: string[];
  email?: string;
  createdAt?: string;
  validatedAt: string;
}

const PLAN_FEATURES: Record<Plan, string[]> = {
  free: ['5 monitors', 'Local-only alerts', '7-day event history', 'CLI dashboard'],
  diagnose: [
    'Up to 20 monitors',
    '30-day event history',
    'Smart alerts with root cause',
    'Known-issue pattern matching',
    'Telegram, Slack, and Discord alerts',
  ],
  heal: [
    'Unlimited monitors',
    '90-day event history',
    'Auto-fix (restart, retry)',
    'Approval flow for risky fixes',
    'Full audit trail and rollback',
    'Everything in Diagnose',
  ],
};

export function getPlanFeatures(plan: Plan): string[] {
  return PLAN_FEATURES[plan] ?? PLAN_FEATURES.free;
}

export function loadLicense(): LicenseInfo | null {
  // Env var takes precedence
  const envKey = process.env.CLAWDOCTOR_KEY;
  if (envKey) {
    // Check cache for previously validated plan
    try {
      if (fs.existsSync(ENV_KEY_CACHE_PATH)) {
        const cache = JSON.parse(fs.readFileSync(ENV_KEY_CACHE_PATH, 'utf-8')) as {
          key: string;
          plan: Plan;
          features: string[];
          cachedAt: string;
        };
        const ageMs = Date.now() - new Date(cache.cachedAt).getTime();
        const ONE_DAY_MS = 24 * 60 * 60 * 1000;
        if (cache.key === envKey && ageMs < ONE_DAY_MS) {
          return { key: envKey, plan: cache.plan, features: cache.features, validatedAt: cache.cachedAt };
        }
      }
    } catch {
      // ignore cache errors
    }
    // Fallback to diagnose until cache is refreshed
    return { key: envKey, plan: 'diagnose', features: PLAN_FEATURES.diagnose, validatedAt: new Date().toISOString() };
  }

  try {
    if (fs.existsSync(LICENSE_PATH)) {
      return JSON.parse(fs.readFileSync(LICENSE_PATH, 'utf-8')) as LicenseInfo;
    }
  } catch {
    // ignore
  }
  return null;
}

export async function refreshEnvKeyCache(key: string): Promise<void> {
  const result = await validateKeyRemote(key);
  if (!result.valid || !result.plan) return;
  ensureAgentwatchDir();
  const cache = {
    key,
    plan: result.plan,
    features: result.features ?? PLAN_FEATURES[result.plan],
    cachedAt: new Date().toISOString(),
  };
  fs.writeFileSync(ENV_KEY_CACHE_PATH, JSON.stringify(cache, null, 2), { encoding: 'utf-8', mode: 0o600 });
}

export function saveLicense(info: LicenseInfo): void {
  ensureAgentwatchDir();
  fs.writeFileSync(LICENSE_PATH, JSON.stringify(info, null, 2), { encoding: 'utf-8', mode: 0o600 });
}

export async function validateKeyRemote(key: string): Promise<{ valid: boolean; plan?: Plan; features?: string[]; email?: string; createdAt?: string }> {
  return new Promise((resolve) => {
    const body = JSON.stringify({ key });
    const options = {
      hostname: 'clawdoctor.dev',
      port: 443,
      path: '/api/license/validate',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(body),
      },
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch {
          resolve({ valid: false });
        }
      });
    });

    req.on('error', () => resolve({ valid: false }));
    req.setTimeout(8000, () => { req.destroy(); resolve({ valid: false }); });
    req.write(body);
    req.end();
  });
}

export function getActivePlan(cmdKey?: string): Plan {
  const key = cmdKey ?? process.env.CLAWDOCTOR_KEY;
  if (key) {
    const license = loadLicense();
    if (license && license.key === key) return license.plan;
  }
  const license = loadLicense();
  return license?.plan ?? 'free';
}

export const DEFAULT_CONFIG: ClawDoctorConfig = {
  openclawPath: path.join(os.homedir(), '.openclaw'),
  watchers: {
    gateway: { enabled: true, interval: 30 },
    cron: { enabled: true, interval: 60 },
    session: { enabled: true, interval: 60 },
    auth: { enabled: true, interval: 60 },
    cost: { enabled: true, interval: 300 },
  },
  healers: {
    processRestart: { enabled: true, dryRun: false },
    cronRetry: { enabled: true, dryRun: false },
    auth: { enabled: true, dryRun: false },
    session: { enabled: true, dryRun: false },
  },
  alerts: {
    telegram: {
      enabled: false,
      botToken: '',
      chatId: '',
    },
  },
  budget: {
    enabled: true,
    dailyLimitUsd: 50,
  },
  dryRun: false,
  retentionDays: 7,
};

export function loadConfig(): ClawDoctorConfig {
  if (!fs.existsSync(CONFIG_PATH)) {
    throw new Error(`Config not found at ${CONFIG_PATH}. Run 'clawdoctor init' first.`);
  }
  const raw = fs.readFileSync(CONFIG_PATH, 'utf-8');
  const parsed = JSON.parse(raw) as Partial<ClawDoctorConfig>;
  return mergeConfig(DEFAULT_CONFIG, parsed);
}

function mergeConfig(defaults: ClawDoctorConfig, overrides: Partial<ClawDoctorConfig>): ClawDoctorConfig {
  const overrideHealers = (overrides.healers ?? {}) as Partial<ClawDoctorConfig['healers']>;
  return {
    ...defaults,
    ...overrides,
    watchers: { ...defaults.watchers, ...(overrides.watchers ?? {}) },
    healers: {
      processRestart: { ...defaults.healers.processRestart, ...(overrideHealers.processRestart ?? {}) },
      cronRetry: { ...defaults.healers.cronRetry, ...(overrideHealers.cronRetry ?? {}) },
      auth: { ...defaults.healers.auth, ...(overrideHealers.auth ?? {}) },
      session: { ...defaults.healers.session, ...(overrideHealers.session ?? {}) },
    },
    alerts: {
      ...defaults.alerts,
      ...(overrides.alerts ?? {}),
      telegram: {
        ...defaults.alerts.telegram,
        ...(overrides.alerts?.telegram ?? {}),
      },
    },
    budget: { ...defaults.budget, ...(overrides.budget ?? {}) },
  };
}

export function saveConfig(config: ClawDoctorConfig): void {
  ensureAgentwatchDir();
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2), { encoding: 'utf-8', mode: 0o600 });
}

export function ensureAgentwatchDir(): void {
  if (!fs.existsSync(AGENTWATCH_DIR)) {
    fs.mkdirSync(AGENTWATCH_DIR, { recursive: true, mode: 0o700 });
  }
}

export function configExists(): boolean {
  return fs.existsSync(CONFIG_PATH);
}
