/**
 * Memory Quality Scoring & Auto-Degradation v1.0
 * Scores memories 0-1 based on multi-factor analysis
 * Auto-degrades memories below threshold to COLD tier or archive
 * Designed to be called periodically by proactive_manager
 */

import { getAllMemories, saveMemories } from './storage.js';
import { assignTiers } from './tier.js';

// ─── Quality Scoring ─────────────────────────────────────────────────────────

/**
 * Multi-factor quality score (0-1) for a memory.
 * Higher = more valuable, should be kept in HOT/WARM.
 * Lower = candidate for COLD tier or archival.
 *
 * Factors:
 *   - importance (0-1): user-supplied importance weight
 *   - access_count: how many times accessed (recency-weighted)
 *   - recency: age in days (exponential decay, half-life 30d)
 *   - reflection_count: how many times memory was reflected/insightful
 *   - accuracy_feedback: helpful (+) vs wrong/outdated (-) signals
 *
 * @param {object} memory
 * @returns {number} score 0-1
 */
export function qualityScore(memory) {
  if (!memory) return 0;

  let score = 0.0;

  // 1. Base importance weight (user-supplied, 0-1)
  const importance = typeof memory.importance === 'number'
    ? Math.max(0, Math.min(1, memory.importance))
    : 0.5;
  score += importance * 0.35;          // up to +0.35

  // 2. Access frequency bonus (logarithmic, max +0.15 at 20+ accesses)
  const accessCount = typeof memory.access_count === 'number' ? memory.access_count : 0;
  if (accessCount > 0) {
    score += Math.min(0.15, Math.log1p(accessCount) * 0.05);
  }

  // 3. Recency bonus (exponential decay, half-life 30 days, max +0.20)
  const ageMs = Date.now() - (memory.created_at || Date.now());
  const ageDays = ageMs / (1000 * 60 * 60 * 24);
  const recencyBonus = Math.exp(-ageDays / 30) * 0.20;
  score += recencyBonus;

  // 4. Reflection / insightful flag (max +0.15 at 3+ reflections)
  const reflectionCount = typeof memory.reflection_count === 'number'
    ? memory.reflection_count
    : (memory.insightful ? 1 : 0);
  if (reflectionCount > 0) {
    score += Math.min(0.15, reflectionCount * 0.05);
  }

  // 5. Accuracy feedback signal (max +0.15 helpful, -0.20 wrong/outdated)
  const feedbackScore = getFeedbackScore(memory);
  score += feedbackScore;

  // 6. Category-specific boosts
  if (memory.category === 'preference' || memory.category === 'decision') {
    score += 0.05;  // decisions and preferences are high-value
  }

  return Math.max(0.0, Math.min(1.0, score));
}

/**
 * Extract numeric feedback signal from a memory's feedback history.
 * Memory.feedbackHistory: Array<{ outcome: 'helpful'|'irrelevant'|'wrong'|'outdated', ts: number }>
 * @param {object} memory
 * @returns {number} bonus in [-0.20, +0.15] range
 */
function getFeedbackScore(memory) {
  const history = memory.feedbackHistory || [];
  if (history.length === 0) return 0;

  let signal = 0;
  for (const fb of history) {
    if (fb.outcome === 'helpful') signal += 0.03;
    else if (fb.outcome === 'irrelevant') signal -= 0.01;
    else if (fb.outcome === 'wrong') signal -= 0.05;
    else if (fb.outcome === 'outdated') signal -= 0.04;
  }
  return Math.max(-0.20, Math.min(0.15, signal));
}

// ─── Auto-Degradation ────────────────────────────────────────────────────────

const DEGRADE_THRESHOLD = 0.15;   // below this score → COLD / archive
const DEGRADE_BATCH = 50;         // process up to this many per tick

/**
 * Auto-degrade memories below the quality threshold.
 * Moves them to the COLD tier (for archival).
 *
 * Called periodically by proactive_manager.tick().
 *
 * @param {object} [options]
 * @param {number} [options.threshold] - quality threshold (default 0.15)
 * @param {number} [options.batchSize] - max memories to process per call (default 50)
 * @param {boolean} [options.dryRun] - if true, only return what would happen (default false)
 * @returns {{ degraded: Array, archived: Array, preserved: Array, dryRun: boolean }}
 */
export function autoDegrade(options = {}) {
  const {
    threshold = DEGRADE_THRESHOLD,
    batchSize = DEGRADE_BATCH,
    dryRun = false,
  } = options;

  const memories = getAllMemories();
  const scored = memories.map(m => ({
    memory: m,
    score: qualityScore(m),
  }));

  const degraded = [];
  const preserved = [];

  for (const item of scored) {
    if (item.score < threshold) {
      degraded.push(item);
    } else {
      preserved.push(item);
    }
  }

  // Sort degraded by score ascending (worst first)
  degraded.sort((a, b) => a.score - b.score);
  const toProcess = degraded.slice(0, batchSize);

  if (dryRun || toProcess.length === 0) {
    return {
      degraded: toProcess.map(d => d.memory.id),
      archived: [],
      preserved: preserved.map(p => p.memory.id),
      dryRun,
      threshold,
      processed: toProcess.length,
      message: dryRun
        ? `Dry run: ${toProcess.length} memories would be degraded (below ${threshold})`
        : `No memories to degrade (threshold=${threshold})`,
    };
  }

  // Apply tier reassignment: degraded → COLD
  const memoriesToDegrade = toProcess.map(d => d.memory);

  // Tag degraded memories for COLD tier
  const updatedMemories = memories.map(m => {
    const degradedItem = memoriesToDegrade.find(d => d.id === m.id);
    if (degradedItem) {
      return {
        ...m,
        tier: 'COLD',
        degraded_at: Date.now(),
        degraded_score: qualityScore(degradedItem),
      };
    }
    return m;
  });

  saveMemories(updatedMemories);

  return {
    degraded: memoriesToDegrade.map(m => m.id),
    archived: [],          // archive slot for future cold-tier compression
    preserved: preserved.map(p => p.memory.id),
    dryRun: false,
    threshold,
    processed: memoriesToDegrade.length,
    message: `Degraded ${memoriesToDegrade.length} memories to COLD tier (below threshold ${threshold})`,
  };
}

/**
 * Score all memories and return them sorted by quality (worst first).
 * Useful for inspection and tuning.
 *
 * @param {number} [topK] - return topK worst memories (default all)
 * @returns {Array<{ memory: object, score: number, factors: object }>}
 */
export function scoreAllMemories(topK = null) {
  const memories = getAllMemories();
  const scored = memories.map(m => {
    const score = qualityScore(m);
    const factors = {
      importance: typeof m.importance === 'number' ? m.importance : 0.5,
      accessCount: typeof m.access_count === 'number' ? m.access_count : 0,
      ageDays: Math.round((Date.now() - (m.created_at || Date.now())) / (1000 * 60 * 60 * 24)),
      reflectionCount: typeof m.reflection_count === 'number' ? m.reflection_count : (m.insightful ? 1 : 0),
      feedbackCount: (m.feedbackHistory || []).length,
      category: m.category || 'unknown',
    };
    return { memory: m, score, factors };
  });

  scored.sort((a, b) => a.score - b.score);

  if (topK !== null) return scored.slice(0, topK);
  return scored;
}

export default { qualityScore, autoDegrade, scoreAllMemories };
