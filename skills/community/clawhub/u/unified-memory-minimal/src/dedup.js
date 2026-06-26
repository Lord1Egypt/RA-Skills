/**
 * Deduplication + Importance Scoring
 * Jaccard similarity dedup (threshold 0.75), importance = base×access×recency×category
 */
const DEFAULT_JACCARD_THRESHOLD = 0.75;
const DEFAULT_PRUNE_THRESHOLD = 0.15;
const CATEGORY_WEIGHTS = {
  preference: 1.5, fact: 1.2, decision: 1.8, entity: 1.1, reflection: 1.3, other: 1.0,
};

/**
 * Tokenize text into word set
 */
function tokenize(text) {
  return new Set(
    String(text || '')
      .toLowerCase()
      .replace(/[^\p{L}\p{N}\s]/gu, ' ')
      .split(/\s+/)
      .filter(w => w.length > 1)
  );
}

/**
 * Jaccard similarity between two sets
 */
function jaccard(a, b) {
  if (!a.size || !b.size) return 0;
  let intersection = 0;
  for (const x of a) if (b.has(x)) intersection++;
  return intersection / (a.size + b.size - intersection);
}

/**
 * Tokenize and compute Jaccard
 */
export function similarity(a, b) {
  return jaccard(tokenize(a), tokenize(b));
}

/**
 * Remove duplicates from memory list
 * @param {Array} memories
 * @param {number} [threshold]
 * @returns {Array} deduplicated list
 */
export function deduplicate(memories, threshold = DEFAULT_JACCARD_THRESHOLD) {
  const kept = [];
  for (const m of memories) {
    // Pinned memories are always kept, never deduped
    if (m.pinned) { kept.push({ ...m }); continue; }
    let isDup = false;
    for (const existing of kept) {
      if (similarity(m.text, existing.text) >= threshold) {
        // Keep the one with higher score or newer timestamp
        if ((m.score || 0) > (existing.score || 0)) {
          Object.assign(existing, m);
        }
        isDup = true;
        break;
      }
    }
    if (!isDup) kept.push({ ...m });
  }
  return kept;
}

/**
 * Compute importance score for a memory
 * @param {object} memory
 * @param {number} [now]
 * @returns {number}
 */
export function computeImportance(memory, now = Date.now()) {
  const base = memory.importance || 0.5;
  const accessCount = memory.accessCount || 1;
  const lastAccessed = memory.lastAccessed || memory.timestamp || now;
  const ageDays = (now - lastAccessed) / 86400000;
  const recency = Math.exp(-ageDays / 30); // 0-1, decays with age
  const category = CATEGORY_WEIGHTS[memory.category] || 1.0;
  const accessBoost = Math.log1p(accessCount) / 10; // diminishing returns
  return Math.min(1, base * (1 + accessBoost) * (0.5 + 0.5 * recency) * category);
}

/**
 * Score and prune low-importance memories
 * @param {Array} memories
 * @param {number} [threshold]
 * @returns {{ kept: Array, pruned: Array }}
 */
export function scoreAndPrune(memories, threshold = DEFAULT_PRUNE_THRESHOLD) {
  const now = Date.now();
  const scored = memories.map(m => ({ ...m, importanceScore: computeImportance(m, now) }));
  // Pinned memories are always kept
  const kept = scored.filter(m => m.pinned || m.importanceScore >= threshold);
  const pruned = scored.filter(m => !m.pinned && m.importanceScore < threshold);
  return { kept, pruned, stats: { total: memories.length, kept: kept.length, pruned: pruned.length } };
}

/**
 * Full dedup + scoring pipeline
 * @param {Array} memories
 * @returns {{ memories: Array, stats: object }}
 */
export function dedupPipeline(memories) {
  const deduped = deduplicate(memories);
  const { kept, pruned, stats } = scoreAndPrune(deduped);
  return { memories: kept, pruned, stats };
}

export default { similarity, deduplicate, computeImportance, scoreAndPrune, dedupPipeline };
