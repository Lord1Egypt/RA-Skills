import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const baselinePath = path.resolve(__dirname, '../data/baseline-priors.json');

let cachedBaseline = null;

function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

function loadJson(filePath, fallback) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(content);
  } catch {
    return fallback;
  }
}

export function getDefaultProfilePath() {
  return path.join(os.homedir(), '.token-cost-time', 'profile.json');
}

export function getDefaultLogPath() {
  return path.join(os.homedir(), '.token-cost-time', 'execution-log.jsonl');
}

export function resolveLogPath(profilePath = null) {
  if (!profilePath) {
    return getDefaultLogPath();
  }
  return path.join(path.dirname(profilePath), 'execution-log.jsonl');
}

export function ensureParentDir(filePath) {
  const dir = path.dirname(filePath);
  fs.mkdirSync(dir, { recursive: true });
}

export function loadBaselinePriors() {
  if (!cachedBaseline) {
    cachedBaseline = loadJson(baselinePath, { taskClasses: {}, models: {} });
  }
  return cachedBaseline;
}

export function loadProfile(profilePath = null) {
  const resolvedPath = profilePath || getDefaultProfilePath();
  const emptyProfile = {
    version: 1,
    updatedAt: null,
    modelTaskStats: {},
    modelStats: {}
  };

  return {
    path: resolvedPath,
    data: loadJson(resolvedPath, emptyProfile)
  };
}

export function saveProfile(profilePath, profileData) {
  ensureParentDir(profilePath);
  const nextProfile = {
    version: 1,
    updatedAt: new Date().toISOString(),
    modelTaskStats: profileData.modelTaskStats || {},
    modelStats: profileData.modelStats || {}
  };
  fs.writeFileSync(profilePath, `${JSON.stringify(nextProfile, null, 2)}\n`, 'utf8');
  return nextProfile;
}

export function modelTaskKey(model, taskClass) {
  return `${model}::${taskClass}`;
}

export function getModelConfig(model) {
  const baseline = loadBaselinePriors();
  return baseline.models[model] || null;
}

export function getTaskConfig(taskClass) {
  const baseline = loadBaselinePriors();
  return baseline.taskClasses[taskClass] || baseline.taskClasses.conversation || null;
}

export function calculateCostUsd(model, inputTokens, outputTokens) {
  const modelConfig = getModelConfig(model);
  if (!modelConfig) {
    throw new Error(`Unknown model: ${model}`);
  }

  const inputCost = (inputTokens / 1_000_000) * modelConfig.pricing.inputPerMTok;
  const outputCost = (outputTokens / 1_000_000) * modelConfig.pricing.outputPerMTok;
  return Number((inputCost + outputCost).toFixed(8));
}

export function confidenceFromDataPoints(dataPoints) {
  const runs = clamp(Number(dataPoints) || 0, 0, 50);
  return Number((0.2 + (runs / 50) * 0.75).toFixed(4));
}

export function qualityConfidence(qualityScore, retryRate) {
  const safeQuality = clamp(Number(qualityScore) || 0.5, 0.05, 0.99);
  const safeRetry = clamp(Number(retryRate) || 0, 0, 0.95);
  return Number(clamp(safeQuality * (1 - safeRetry), 0.05, 0.99).toFixed(4));
}

export function toPositiveInt(value, fallback = 0) {
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed < 0) {
    return fallback;
  }
  return Math.round(parsed);
}

export function toPositiveNumber(value, fallback = 0) {
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed < 0) {
    return fallback;
  }
  return parsed;
}

export function updateRunningAverage(avg, count, nextValue) {
  if (count <= 0) {
    return nextValue;
  }
  return avg + (nextValue - avg) / count;
}
