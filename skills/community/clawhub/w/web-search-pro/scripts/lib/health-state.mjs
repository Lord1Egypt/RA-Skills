import fs from "node:fs/promises";
import path from "node:path";

import { resolveCacheDir } from "./config.mjs";
import { listProviders } from "./providers.mjs";

const NETWORK_ERROR_PATTERN =
  /(?:ECONNRESET|ENOTFOUND|ETIMEDOUT|EAI_AGAIN|network|socket|certificate|tls|fetch failed|unable to verify|timeout)/i;
const CHALLENGE_ERROR_PATTERN = /(?:challenge|captcha|bot check|automated requests|rate limit page)/i;

function getNow(options = {}) {
  return typeof options.now === "number" ? options.now : Date.now();
}

function getStatePath(options = {}) {
  const cwd = options.cwd ?? process.cwd();
  return path.join(resolveCacheDir(options.config, cwd), "health-state.json");
}

async function ensureStateDir(options = {}) {
  await fs.mkdir(path.dirname(getStatePath(options)), { recursive: true });
}

function createEmptyState() {
  return { providers: {} };
}

function normalizeProviderState(state) {
  return {
    consecutiveFailures: state?.consecutiveFailures ?? 0,
    cooldownUntil: state?.cooldownUntil ?? null,
    lastFailureAt: state?.lastFailureAt ?? null,
    lastSuccessAt: state?.lastSuccessAt ?? null,
    lastError: state?.lastError ?? null,
    lastCategory: state?.lastCategory ?? null,
  };
}

function extractHttpStatus(error) {
  const message = error?.message ?? String(error ?? "");
  const match = message.match(/\((\d{3})\)/);
  if (!match) {
    return null;
  }
  return Number.parseInt(match[1], 10);
}

export function classifyProviderError(error) {
  const message = error?.message ?? String(error ?? "");
  const status = extractHttpStatus(error);

  if (status === 202 || CHALLENGE_ERROR_PATTERN.test(message)) {
    return {
      recordFailure: true,
      countsTowardCooldown: true,
      category: "challenge",
    };
  }
  if (status === 429) {
    return { recordFailure: true, countsTowardCooldown: true, category: "rate-limit" };
  }
  if (status !== null && status >= 500) {
    return { recordFailure: true, countsTowardCooldown: true, category: "server" };
  }
  if (status !== null && status >= 400 && status < 500) {
    return { recordFailure: true, countsTowardCooldown: false, category: "client" };
  }
  if (NETWORK_ERROR_PATTERN.test(message)) {
    return { recordFailure: true, countsTowardCooldown: true, category: "network" };
  }
  return { recordFailure: true, countsTowardCooldown: false, category: "unknown" };
}

export async function loadHealthState(options = {}) {
  if (!options.config.health.enabled) {
    return createEmptyState();
  }

  const statePath = getStatePath(options);

  try {
    const raw = await fs.readFile(statePath, "utf8");
    const parsed = JSON.parse(raw);
    return {
      providers: Object.fromEntries(
        Object.entries(parsed.providers ?? {}).map(([providerId, state]) => [
          providerId,
          normalizeProviderState(state),
        ]),
      ),
    };
  } catch (error) {
    if (error.code === "ENOENT") {
      return createEmptyState();
    }
    throw error;
  }
}

async function saveHealthState(state, options = {}) {
  if (!options.config.health.enabled) {
    return;
  }

  await ensureStateDir(options);
  await fs.writeFile(getStatePath(options), JSON.stringify(state, null, 2));
}

export function getProviderHealthEntry(healthState, providerId, now = Date.now()) {
  const entry = normalizeProviderState(healthState?.providers?.[providerId]);
  const coolingDown = entry.cooldownUntil !== null && entry.cooldownUntil > now;
  const degraded =
    !coolingDown &&
    entry.lastFailureAt !== null &&
    (entry.lastSuccessAt === null || entry.lastFailureAt > entry.lastSuccessAt);
  return {
    ...entry,
    status: coolingDown ? "cooldown" : degraded ? "degraded" : "healthy",
  };
}

export async function recordProviderFailure(providerId, error, options = {}) {
  if (!options.config.health.enabled) {
    return createEmptyState();
  }

  const now = getNow(options);
  const classification = classifyProviderError(error);
  const state = await loadHealthState(options);
  const current = normalizeProviderState(state.providers[providerId]);
  const activeCooldownUntil =
    current.cooldownUntil !== null && current.cooldownUntil > now ? current.cooldownUntil : null;

  if (!classification.recordFailure) {
    await saveHealthState(state, options);
    return state;
  }

  const consecutiveFailures = classification.countsTowardCooldown
    ? current.consecutiveFailures + 1
    : current.consecutiveFailures;
  const cooldownUntil =
    classification.countsTowardCooldown && consecutiveFailures >= options.config.health.failureThreshold
      ? now + options.config.health.cooldownSeconds * 1000
      : activeCooldownUntil;

  state.providers[providerId] = {
    consecutiveFailures,
    cooldownUntil,
    lastFailureAt: now,
    lastSuccessAt: current.lastSuccessAt,
    lastError: error?.message ?? String(error),
    lastCategory: classification.category,
  };

  await saveHealthState(state, options);
  return state;
}

export async function recordProviderSuccess(providerId, options = {}) {
  if (!options.config.health.enabled) {
    return createEmptyState();
  }

  const now = getNow(options);
  const state = await loadHealthState(options);
  state.providers[providerId] = {
    consecutiveFailures: 0,
    cooldownUntil: null,
    lastFailureAt: state.providers[providerId]?.lastFailureAt ?? null,
    lastSuccessAt: now,
    lastError: null,
    lastCategory: null,
  };
  await saveHealthState(state, options);
  return state;
}

export async function recordProviderOutcomes(providerOutcomes = [], options = {}) {
  let state = null;

  for (const outcome of providerOutcomes) {
    if (outcome.status === "success") {
      state = await recordProviderSuccess(outcome.providerId, options);
      continue;
    }
    if (outcome.status === "failure") {
      const error =
        outcome.error instanceof Error ? outcome.error : new Error(String(outcome.error ?? "Unknown failure"));
      state = await recordProviderFailure(outcome.providerId, error, options);
    }
  }

  return state ?? createEmptyState();
}

export async function buildHealthSnapshot(options = {}) {
  const now = getNow(options);
  const state = await loadHealthState(options);

  return {
    command: "health",
    providers: Object.fromEntries(
      listProviders().map((provider) => [
        provider.id,
        getProviderHealthEntry(state, provider.id, now),
      ]),
    ),
  };
}
