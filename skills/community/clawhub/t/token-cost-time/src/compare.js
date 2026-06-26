import { calibrate } from './calibrate.js';

const VALID_SORTS = new Set(['cost', 'quality', 'balanced']);

function balancedScore(result) {
  return result.estimate.costUsd / Math.max(result.qualityConfidence, 0.0001);
}

export function compare(objective, models, profilePath = null, sortBy = 'cost') {
  if (!Array.isArray(models) || models.length === 0) {
    throw new Error('compare requires a non-empty models array');
  }

  const normalizedSortBy = String(sortBy || 'cost').trim().toLowerCase();
  if (!VALID_SORTS.has(normalizedSortBy)) {
    throw new Error("sortBy must be one of: 'cost' | 'quality' | 'balanced'");
  }

  const results = models.map((model) => calibrate(objective, model, profilePath));
  const recommendationResult = results
    .slice()
    .sort((a, b) => balancedScore(a) - balancedScore(b))[0] || null;

  const ranked = results.sort((a, b) => {
    if (normalizedSortBy === 'quality') {
      return b.qualityConfidence - a.qualityConfidence;
    }
    if (normalizedSortBy === 'balanced') {
      return balancedScore(a) - balancedScore(b);
    }
    return a.estimate.costUsd - b.estimate.costUsd;
  });

  const recommendation = recommendationResult
    ? {
        model: recommendationResult.model,
        reason: 'Best cost-to-quality ratio (costUsd / qualityConfidence).'
      }
    : null;

  return {
    objective,
    sortBy: normalizedSortBy,
    ranked,
    recommendation
  };
}
