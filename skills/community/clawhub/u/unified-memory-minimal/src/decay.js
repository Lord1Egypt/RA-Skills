/**
 * Weibull Time Decay - Time-based importance decay
 * Memories decay over time using Weibull distribution
 * halfLife: days until importance drops to ~37% (1/e)
 */
const WEIBULL_SCALE = 30; // scale parameter (days)
const WEIBULL_SHAPE = 1.5; // shape parameter (>1 = faster early decay)

/**
 * Calculate decay multiplier for a memory's age
 * @param {number} ageMs - Age in milliseconds
 * @param {number} scale - Scale parameter in days
 * @param {number} shape - Shape parameter
 * @returns {number} multiplier 0-1
 */
export function weibullDecay(ageMs, scale = WEIBULL_SCALE, shape = WEIBULL_SHAPE) {
  const ageDays = ageMs / (1000 * 60 * 60 * 24);
  const t = ageDays / scale;
  return Math.exp(-Math.pow(t, shape));
}

/**
 * Apply decay boost to search results
 * @param {Array} results - Search results with timestamp field
 * @param {string} [timestampField='createdAt']
 * @param {object} config
 * @returns {Array} results with decayBoost added
 */
export function applyDecayBoost(results, timestampField = 'createdAt', config = {}) {
  const { scale = WEIBULL_SCALE, shape = WEIBULL_SHAPE, boostFactor = 0.3 } = config;
  const now = Date.now();
  return results.map(r => {
    const ageMs = now - (r[timestampField] || r.createdAt || now);
    const decay = weibullDecay(ageMs, scale, shape);
    const decayBoost = decay * boostFactor;
    const { [timestampField]: _t, createdAt: _c, ...rest } = r;
    return {
      ...rest,
      timestamp: r[timestampField] || r.createdAt,
      decay,
      decayBoost,
      finalScore: (r.score || r.finalScore || 0) + decayBoost
    };
  });
}

export default { weibullDecay, applyDecayBoost };
