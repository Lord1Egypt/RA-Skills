import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { getStateRoot } from "../config/paths";

export interface HealthCheck {
  ts: number;
  ok: boolean;
}

export interface SourceHealth {
  name: string;
  checks: HealthCheck[];
}

export type HealthStore = Record<string, SourceHealth>;

const SEVEN_DAYS = 7 * 24 * 3_600_000;

function healthPath(env: NodeJS.ProcessEnv): string {
  return path.join(getStateRoot(env), "health.json");
}

export async function loadHealthStore(env: NodeJS.ProcessEnv): Promise<HealthStore> {
  try {
    const content = await readFile(healthPath(env), "utf8");
    return JSON.parse(content) as HealthStore;
  } catch {
    return {};
  }
}

export async function saveHealthStore(store: HealthStore, env: NodeJS.ProcessEnv): Promise<void> {
  const root = getStateRoot(env);
  await mkdir(root, { recursive: true });
  await writeFile(healthPath(env), JSON.stringify(store, null, 2), "utf8");
}

export function recordSourceResult(store: HealthStore, id: string, name: string, ok: boolean, now = Date.now()): void {
  const cutoff = now - SEVEN_DAYS;

  if (!store[id]) {
    store[id] = { name, checks: [] };
  }

  store[id].checks.push({ ts: now, ok });

  // Prune old entries
  store[id].checks = store[id].checks.filter((c) => c.ts >= cutoff);
}

export function getUnhealthySources(store: HealthStore, threshold = 0.5): string[] {
  const unhealthy: string[] = [];

  for (const [, health] of Object.entries(store)) {
    if (health.checks.length < 2) continue;
    const failCount = health.checks.filter((c) => !c.ok).length;
    const failRate = failCount / health.checks.length;
    if (failRate > threshold) {
      unhealthy.push(health.name);
    }
  }

  return unhealthy;
}

export function formatHealthWarnings(names: string[]): string {
  if (names.length === 0) return "";
  const lines = names.map((n) => `- ${n}`).join("\n");
  return `## ⚠️ Source Health Warnings\n\n${lines}\n`;
}
