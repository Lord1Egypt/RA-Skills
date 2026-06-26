/**
 * Adaptive Skip - Skip non-retrieval queries
 * Determines whether to skip vector search based on query patterns
 */
const SKIP_PATTERNS = [
  { pattern: /^(\*ping\*|\/ping|ping\s*\?|is\s+anyone\s+there)/i, label: 'ping' },
  { pattern: /^(ok|okay|thanks?|thank\s+you|👍|✅|好|好的|收到)/i, label: 'ack' },
  { pattern: /^(bye|goodbye|exit|quit|结束|再见)/i, label: 'bye' },
  { pattern: /^(help|command|命令|指令)/i, label: 'help' },
  { pattern: /^HEARTBEAT/i, label: 'heartbeat' },
  { pattern: /^(who\s+are\s+you|what\s+are\s+you|你是谁|自我介绍)/i, label: 'identity' },
  { pattern: /^(how\s+are\s+you|how('s| is)\s+(it|things|everything))/i, label: 'greeting_casual' },
];
const FORCE_PATTERNS = [
  { pattern: /(记得|之前|以前|曾经| recall|remember|earlier|past)/i, label: 'force_recall' },
];
/** @type {Set<string>} */
const skipCache = new Set();

/**
 * Check if query should skip retrieval
 * @param {string} query
 * @returns {{ skip: boolean, reason?: string, force?: boolean }}
 */
export function shouldSkipRetrieval(query) {
  const q = query.trim();
  if (!q) return { skip: true, reason: 'empty' };
  if (skipCache.has(q)) return { skip: true, reason: 'cached' };
  for (const { pattern, label } of FORCE_PATTERNS) {
    if (pattern.test(q)) return { skip: false, force: true, reason: `force:${label}` };
  }
  for (const { pattern, label } of SKIP_PATTERNS) {
    if (pattern.test(q)) {
      skipCache.add(q);
      return { skip: true, reason: `match:${label}` };
    }
  }
  // Skip single emoji
  if (/^[\p{Emoji_Presentation}\p{Extended_Pictographic}]$/u.test(q)) {
    skipCache.add(q);
    return { skip: true, reason: 'emoji' };
  }
  return { skip: false, reason: 'retrieval_needed' };
}

export function clearAdaptiveCache() { skipCache.clear(); }
export default { shouldSkipRetrieval, clearAdaptiveCache };
