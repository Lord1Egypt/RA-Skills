/**
 * Noise Filter - Filter out low-value noise from stored memories
 * shouldStore() determines if a memory should be stored
 * qualityScore() scores existing memories for potential cleanup
 * learnNoisePattern() auto-learns noise patterns from deletions
 */
const NOISE_PATTERNS = [
  /^(ok|okay|ok✅|好|好的|收到|👍|✅|收到收到)$/i,
  /^[\p{Emoji_Presentation}\p{Extended_Pictographic}]{1,3}$/u,
  /^(hi|hey|hello|hiya|yo|sup|what('s| is) up)$/i,
  /\b(thanks?|thank\s+you|thx|ty|tq)\b/i,
  /\b(bye|goodbye|see\s+ya|ttyl|talk\s+later)\b/i,
  /^!.*!/,  // single word exclamation
  /^(ha+|lol|lmao|rotfl|kek)$/i,
];
const LOW_QUALITY_PATTERNS = [
  /^(nothing|na|no\s*idea|idk|i\s*don'?t\s*know|nope)$/i,
  /^(?:check\s+the\s+log|see\s+above|as\s+mentioned\s+earlier)/i,
];
const STORED_NOISE = new Set();
const MIN_TEXT_LENGTH = 3;

/**
 * Determine if a text should be stored as memory
 * @param {string} text
 * @param {object} [opts]
 * @returns {{ store: boolean, reason?: string }}
 */
export function shouldStore(text, opts = {}) {
  const { minLength = MIN_TEXT_LENGTH } = opts;
  const t = String(text || '').trim();
  if (t.length < minLength) return { store: false, reason: 'too_short' };
  for (const p of NOISE_PATTERNS) {
    if (p.test(t)) return { store: false, reason: 'noise_pattern' };
  }
  if (t.split(/\s+/).length > 2) {
    for (const p of LOW_QUALITY_PATTERNS) {
      if (p.test(t)) return { store: false, reason: 'low_quality_pattern' };
    }
  }
  if (STORED_NOISE.has(t.toLowerCase())) return { store: false, reason: 'learned_noise' };
  return { store: true };
}

/**
 * Score memory quality (0-1, higher = more valuable)
 * @param {object} memory
 * @returns {number}
 */
export function qualityScore(memory) {
  const t = String(memory.text || '').trim();
  let score = 0.5;
  // Length bonus
  const words = t.split(/\s+/).length;
  if (words >= 5) score += 0.1;
  if (words >= 15) score += 0.15;
  // Has category
  if (memory.category && memory.category !== 'other') score += 0.1;
  // Has importance field
  if (typeof memory.importance === 'number') score += memory.importance * 0.15;
  // Access count bonus
  if (memory.accessCount && memory.accessCount > 3) score += 0.1;
  // Negative: known noise
  if (STORED_NOISE.has(t.toLowerCase())) score -= 0.5;
  // Negative: low info patterns
  for (const p of LOW_QUALITY_PATTERNS) {
    if (p.test(t)) { score -= 0.3; break; }
  }
  return Math.max(0, Math.min(1, score));
}

/**
 * Learn that this text is noise (from user deletion or auto-detection)
 * @param {string} text
 */
export function learnNoisePattern(text) {
  STORED_NOISE.add(String(text || '').trim().toLowerCase());
}

export function clearLearnedNoise() { STORED_NOISE.clear(); }
export function getNoiseCount() { return STORED_NOISE.size; }

/**
 * Filter memories by quality threshold
 * @param {Array} memories
 * @param {number} [threshold=0.3]
 * @returns {{ kept: Array, removed: Array }}
 */
export function filterByQuality(memories, threshold = 0.3) {
  const scored = memories.map(m => ({ ...m, qualityScore: qualityScore(m) }));
  const kept = scored.filter(m => m.qualityScore >= threshold);
  const removed = scored.filter(m => m.qualityScore < threshold);
  return { kept, removed };
}

export default { shouldStore, qualityScore, learnNoisePattern, clearLearnedNoise, filterByQuality };
