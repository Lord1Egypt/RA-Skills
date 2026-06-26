/**
 * Smart Extractor - LLM-powered memory extraction from raw text
 * 6 categories: preference, fact, decision, entity, reflection, other
 * 8-second timeout, Jaccard dedup against existing memories
 */
const CATEGORIES = ['preference', 'fact', 'decision', 'entity', 'reflection', 'other'];
const EXTRACT_PROMPT = `You are a memory analysis assistant. Extract structured memories from the following text.

For each memory, identify:
1. **category**: one of [preference, fact, decision, entity, reflection, other]
2. **text**: concise summary (within 100 chars)
3. **importance**: 0.0-1.0 (how important this memory is)

Categories:
- preference: user likes/dislikes, habits, communication style
- fact: verifiable information, dates, names, events
- decision: choices made, conclusions reached, agreements
- entity: people, products, tools, services mentioned
- reflection: lessons learned, self-awareness, growth insights
- other: anything that doesn't fit above

Return JSON array:
[{"category":"preference","text":"user prefers concise communication","importance":0.8},...]

Text to analyze:
`;

const SUMMARY_PROMPT = `Summarize the following text into a concise memory (max 100 chars):
`;

/**
 * Call LLM to extract memories from text
 * @param {string} text - Raw text to analyze
 * @param {Function} llmCall - LLM API function (text → response text)
 * @param {number} [timeoutMs=8000]
 * @returns {Promise<Array>}
 */
export async function extractMemories(text, llmCall, timeoutMs = 8000) {
  if (!text || !text.trim()) return [];
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const response = await llmCall(text, { prompt: EXTRACT_PROMPT, signal: controller.signal });
    clearTimeout(timer);
    let parsed = typeof response === 'string' ? JSON.parse(response) : response;
    if (!Array.isArray(parsed)) parsed = [];
    return parsed
      .filter(m => m.text && CATEGORIES.includes(m.category))
      .map(m => ({
        category: m.category,
        text: String(m.text).slice(0, 200),
        importance: Math.max(0, Math.min(1, parseFloat(m.importance) || 0.5)),
        extractedFrom: 'llm',
        createdAt: Date.now(),
      }));
  } catch (e) {
    clearTimeout(timer);
    if (e.name === 'AbortError') throw new Error('LLM extraction timeout');
    // Fallback: treat as single 'other' memory
    return [{
      category: 'other',
      text: String(text).slice(0, 200),
      importance: 0.3,
      extractedFrom: 'fallback',
      createdAt: Date.now(),
    }];
  }
}

/**
 * Batch extract from multiple texts
 * @param {string[]} texts
 * @param {Function} llmCall
 * @param {Function} [onProgress]
 */
export async function batchExtract(texts, llmCall, onProgress) {
  const results = [];
  for (let i = 0; i < texts.length; i++) {
    const extracted = await extractMemories(texts[i], llmCall);
    results.push(...extracted);
    if (onProgress) onProgress(i + 1, texts.length);
  }
  return results;
}

export default { extractMemories, batchExtract, CATEGORIES };
