import { classifyObjective } from './classify.js';
import {
  calculateCostUsd,
  confidenceFromDataPoints,
  getModelConfig,
  getTaskConfig,
  loadProfile,
  modelTaskKey,
  qualityConfidence,
  toPositiveInt
} from './models.js';

function estimateFromBaseline(taskConfig, modelConfig) {
  const inputTokens = toPositiveInt(taskConfig.baseInputTokens, 0);
  const outputTokens = toPositiveInt(
    taskConfig.baseOutputTokens * (modelConfig.outputFactor || 1),
    0
  );
  const durationMs = toPositiveInt(
    taskConfig.baseDurationMs * (modelConfig.durationFactor || 1),
    0
  );

  return {
    inputTokens,
    outputTokens,
    durationMs
  };
}

export function calibrate(objective, model, profilePath = null) {
  const taskClass = classifyObjective(objective);
  const modelConfig = getModelConfig(model);

  if (!modelConfig) {
    throw new Error(`Unknown model: ${model}`);
  }

  const taskConfig = getTaskConfig(taskClass);
  if (!taskConfig) {
    throw new Error(`Unknown task class: ${taskClass}`);
  }

  const { data: profile } = loadProfile(profilePath);
  const key = modelTaskKey(model, taskClass);

  const taskStats = profile.modelTaskStats[key] || null;
  const modelStats = profile.modelStats[model] || null;

  const baselineEstimate = estimateFromBaseline(taskConfig, modelConfig);
  const inputTokens = toPositiveInt(taskStats?.inputAvg, baselineEstimate.inputTokens);
  const outputTokens = toPositiveInt(taskStats?.outputAvg, baselineEstimate.outputTokens);
  const durationMs = toPositiveInt(taskStats?.durationAvg, baselineEstimate.durationMs);

  const dataPoints = toPositiveInt(taskStats?.runs, 0);
  const confidence = confidenceFromDataPoints(dataPoints);

  const retryRate = taskStats?.retryRate ?? modelStats?.retryRate ?? modelConfig.retryRate ?? 0;
  const quality = qualityConfidence(modelConfig.qualityScore, retryRate);

  const costUsd = calculateCostUsd(model, inputTokens, outputTokens);

  return {
    taskClass,
    model,
    estimate: {
      tokens: {
        input: inputTokens,
        output: outputTokens,
        total: inputTokens + outputTokens
      },
      costUsd,
      durationMs
    },
    confidence,
    qualityConfidence: quality,
    dataPoints
  };
}
