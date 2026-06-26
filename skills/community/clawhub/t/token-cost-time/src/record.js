import fs from 'node:fs';

import {
  calculateCostUsd,
  ensureParentDir,
  loadProfile,
  modelTaskKey,
  resolveLogPath,
  saveProfile,
  toPositiveInt,
  toPositiveNumber,
  updateRunningAverage
} from './models.js';

function asIsoNow() {
  return new Date().toISOString();
}

function normalizeRetryCount(executionData) {
  if (executionData.retries !== undefined) {
    return toPositiveInt(executionData.retries, 0);
  }
  if (executionData.retry === true) {
    return 1;
  }
  return 0;
}

function updateModelTaskStats(existing = {}, executionData) {
  const runs = toPositiveInt(existing.runs, 0) + 1;
  const retryCount = toPositiveInt(existing.retryCount, 0) + normalizeRetryCount(executionData);

  return {
    runs,
    inputAvg: updateRunningAverage(
      toPositiveNumber(existing.inputAvg, 0),
      runs,
      toPositiveInt(executionData.inputTokens, 0)
    ),
    outputAvg: updateRunningAverage(
      toPositiveNumber(existing.outputAvg, 0),
      runs,
      toPositiveInt(executionData.outputTokens, 0)
    ),
    durationAvg: updateRunningAverage(
      toPositiveNumber(existing.durationAvg, 0),
      runs,
      toPositiveInt(executionData.durationMs, 0)
    ),
    costAvg: updateRunningAverage(
      toPositiveNumber(existing.costAvg, 0),
      runs,
      toPositiveNumber(executionData.costUsd, 0)
    ),
    retryCount,
    retryRate: Number((retryCount / runs).toFixed(4))
  };
}

function updateModelStats(existing = {}, executionData) {
  const runs = toPositiveInt(existing.runs, 0) + 1;
  const retryCount = toPositiveInt(existing.retryCount, 0) + normalizeRetryCount(executionData);

  return {
    runs,
    retryCount,
    retryRate: Number((retryCount / runs).toFixed(4))
  };
}

function normalizeExecutionData(executionData) {
  const model = String(executionData.model || '').trim();
  const taskClass = String(executionData.taskClass || '').trim();

  if (!model) {
    throw new Error('record requires executionData.model');
  }
  if (!taskClass) {
    throw new Error('record requires executionData.taskClass');
  }

  const inputTokens = toPositiveInt(executionData.inputTokens, 0);
  const outputTokens = toPositiveInt(executionData.outputTokens, 0);
  const durationMs = toPositiveInt(executionData.durationMs, 0);

  const costFromInput = toPositiveNumber(executionData.costUsd, Number.NaN);
  const costFromAlias = toPositiveNumber(executionData.cost, Number.NaN);
  const resolvedCost = Number.isFinite(costFromInput)
    ? costFromInput
    : Number.isFinite(costFromAlias)
      ? costFromAlias
      : calculateCostUsd(model, inputTokens, outputTokens);

  return {
    model,
    taskClass,
    inputTokens,
    outputTokens,
    durationMs,
    costUsd: Number(resolvedCost.toFixed(8)),
    retries: normalizeRetryCount(executionData),
    timestamp: executionData.timestamp || asIsoNow()
  };
}

export function record(executionData, profilePath = null) {
  const normalized = normalizeExecutionData(executionData);
  const { path: resolvedProfilePath, data: profile } = loadProfile(profilePath);

  const key = modelTaskKey(normalized.model, normalized.taskClass);
  const nextTaskStats = updateModelTaskStats(profile.modelTaskStats[key], normalized);
  const nextModelStats = updateModelStats(profile.modelStats[normalized.model], normalized);

  const nextProfile = {
    ...profile,
    modelTaskStats: {
      ...profile.modelTaskStats,
      [key]: nextTaskStats
    },
    modelStats: {
      ...profile.modelStats,
      [normalized.model]: nextModelStats
    }
  };

  const savedProfile = saveProfile(resolvedProfilePath, nextProfile);

  const executionLogPath = resolveLogPath(resolvedProfilePath);
  ensureParentDir(executionLogPath);
  fs.appendFileSync(executionLogPath, `${JSON.stringify(normalized)}\n`, 'utf8');

  return {
    profilePath: resolvedProfilePath,
    logPath: executionLogPath,
    entry: normalized,
    profile: savedProfile
  };
}
