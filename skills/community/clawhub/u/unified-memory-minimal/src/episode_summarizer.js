/**
 * Episode Summarizer - Generate structured summaries for completed episodes
 *
 * When an episode completes, generates a summary with:
 * - title: short session title
 * - keyTopics: main topics discussed
 * - decisions: key decisions made during session
 * - nextSteps: action items / follow-ups
 *
 * Also extracts DECISION category memories from the episode.
 */

import { config } from './config.js';

const OLLAMA_HOST = process.env.OLLAMA_HOST || process.env.OLLAMA_BASE_URL || 'http://localhost:11434';
const OLLAMA_LLM_MODEL = process.env.OLLAMA_LLM_MODEL || 'deepseek-v3:cloud';

const SUMMARY_SYSTEM_PROMPT = `You are a conversation analyst. Your task is to analyze a conversation transcript and produce a structured summary.

Respond ONLY with valid JSON in this exact format:
{
  "title": "Short session title (max 60 chars)",
  "keyTopics": ["topic1", "topic2", "topic3"],
  "decisions": ["decision1", "decision2"],
  "nextSteps": ["next step 1", "next step 2"]
}

Guidelines:
- title: capture the main purpose/theme of the conversation in a few words
- keyTopics: 3-5 main topics or themes discussed (be specific, not generic)
- decisions: any conclusions reached, choices made, or agreements reached during the session
- nextSteps: any follow-up actions, pending items, or things to do next
- If no decisions were made, use an empty array []
- If no next steps, use an empty array []
- Output ONLY the JSON, no additional text or markdown fences
`;

const DECISION_EXTRACT_PROMPT = `You are a decision extractor. Given a conversation transcript, extract all key decisions made.

Respond ONLY with valid JSON array:
["decision 1", "decision 2", ...]

Rules:
- A "decision" is a clear choice, conclusion, or agreement reached
- Include only decisions explicitly mentioned in the conversation
- If no decisions found, return []
- Output ONLY the JSON array, no markdown or text
`;

// ─── LLM Calls ────────────────────────────────────────────────────────────────

/**
 * Call Ollama LLM with a prompt
 * @param {string} prompt
 * @param {string} [systemPrompt]
 * @param {number} [timeoutMs=30000]
 * @returns {Promise<string>}
 */
async function callOllama(prompt, systemPrompt = null, timeoutMs = 30000) {
  const messages = [];
  if (systemPrompt) {
    messages.push({ role: 'system', content: systemPrompt });
  }
  messages.push({ role: 'user', content: prompt });

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(`${OLLAMA_HOST}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: OLLAMA_LLM_MODEL,
        messages,
        stream: false,
        options: { temperature: 0.3 },
      }),
      signal: controller.signal,
    });

    clearTimeout(timer);
    if (!response.ok) {
      throw new Error(`Ollama error: ${response.status}`);
    }
    const data = await response.json();
    return (data.message?.content || '').trim();
  } catch (err) {
    clearTimeout(timer);
    throw err;
  }
}

/**
 * Parse JSON from LLM response, stripping markdown fences if present
 * @param {string} raw
 * @returns {object|null}
 */
function parseJsonResponse(raw) {
  let text = raw.trim();
  // Strip markdown code fences
  if (text.startsWith('```')) {
    text = text.replace(/^```[a-z]*\n?/i, '').replace(/\n?```$/, '');
  }
  try {
    return JSON.parse(text.trim());
  } catch {
    return null;
  }
}

// ─── Core Summarizer ──────────────────────────────────────────────────────────

/**
 * Build conversation text from episode messages
 * @param {object[]} messages
 * @returns {string}
 */
function buildTranscript(messages) {
  return messages
    .map(m => `[${m.role}] ${m.content}`)
    .join('\n');
}

/**
 * Generate structured summary for an episode
 * @param {object} episode - full episode object
 * @param {number} [timeoutMs=30000]
 * @returns {Promise<{title: string|null, keyTopics: string[], decisions: string[], nextSteps: string[], summary: string|null}>}
 */
export async function summarizeEpisode(episode, timeoutMs = 30000) {
  const messages = episode.messages || [];

  if (messages.length === 0) {
    return {
      title: episode.title || 'Empty session',
      keyTopics: [],
      decisions: [],
      nextSteps: [],
      summary: null,
    };
  }

  const transcript = buildTranscript(messages);
  // Truncate transcript if too long (Ollama context limits)
  const truncated = transcript.length > 4000 ? transcript.slice(0, 4000) + '\n[...truncated...]' : transcript;

  try {
    const raw = await callOllama(
      `Analyze this conversation transcript and produce a structured summary:\n\n${truncated}`,
      SUMMARY_SYSTEM_PROMPT,
      timeoutMs
    );

    const parsed = parseJsonResponse(raw);

    if (parsed && typeof parsed === 'object') {
      return {
        title: String(parsed.title || '').slice(0, 60) || null,
        keyTopics: Array.isArray(parsed.keyTopics) ? parsed.keyTopics.slice(0, 10) : [],
        decisions: Array.isArray(parsed.decisions) ? parsed.decisions.slice(0, 10) : [],
        nextSteps: Array.isArray(parsed.nextSteps) ? parsed.nextSteps.slice(0, 10) : [],
        summary: buildSummaryText(parsed),
      };
    }
  } catch (err) {
    console.warn('[EpisodeSummarizer] LLM call failed, using fallback:', err.message);
  }

  // Fallback: rule-based summary
  return fallbackSummary(episode);
}

/**
 * Build a natural-language summary from structured data
 * @param {object} parsed
 * @returns {string}
 */
function buildSummaryText(parsed) {
  const parts = [];
  if (parsed.title) parts.push(`Session: ${parsed.title}`);
  if (parsed.keyTopics?.length) parts.push(`Topics: ${parsed.keyTopics.join(', ')}`);
  if (parsed.decisions?.length) parts.push(`Decisions: ${parsed.decisions.join('; ')}`);
  if (parsed.nextSteps?.length) parts.push(`Next steps: ${parsed.nextSteps.join('; ')}`);
  return parts.join('\n');
}

/**
 * Rule-based fallback when LLM is unavailable
 * @param {object} episode
 * @returns {object}
 */
function fallbackSummary(episode) {
  const messages = episode.messages || [];
  const text = messages.map(m => m.content).join(' ');

  // Extract key sentences using simple heuristics
  const decisionKeywords = ['决定', '选择', '确认', 'agreed', 'decided', 'concluded', 'will', '应该', '要'];
  const nextKeywords = ['下一步', '接下来', '待办', 'follow', 'next', 'later', '需要', '应该'];

  const sentences = text.replace(/[.!?。]/g, '\n').split('\n').filter(s => s.trim().length > 5);

  const decisions = sentences.filter(s => decisionKeywords.some(k => s.includes(k))).slice(0, 5);
  const nextSteps = sentences.filter(s => nextKeywords.some(k => s.includes(k))).slice(0, 5);

  // Extract topics: most frequent noun phrases (simple approach: 3-10 char segments)
  const words = text.match(/[\w\u4e00-\u9fff]{2,15}/g) || [];
  const freq = {};
  for (const w of words) {
    freq[w] = (freq[w] || 0) + 1;
  }
  const topics = Object.entries(freq)
    .sort((a, b) => b[1] - a[1])
    .filter(([, count]) => count >= 2 && count < words.length * 0.3)
    .slice(0, 5)
    .map(([word]) => word);

  return {
    title: topics[0] ? `Session about: ${topics[0]}` : 'Session summary',
    keyTopics: topics,
    decisions: decisions.map(s => s.trim().slice(0, 100)),
    nextSteps: nextSteps.map(s => s.trim().slice(0, 100)),
    summary: `Fallback summary: discussed ${topics.length} topics, made ${decisions.length} decisions`,
  };
}

/**
 * Extract decision memories from episode
 * Returns memory-ready objects for DECISION category
 * @param {object} episode
 * @returns {Promise<Array<{text: string, category: string, importance: number}>>}
 */
export async function extractDecisionMemories(episode) {
  const messages = episode.messages || [];
  if (messages.length === 0) return [];

  const transcript = buildTranscript(messages);
  const truncated = transcript.length > 4000 ? transcript.slice(0, 4000) : transcript;

  try {
    const raw = await callOllama(
      `Extract all key decisions from this conversation:\n\n${truncated}`,
      DECISION_EXTRACT_PROMPT,
      20000
    );

    let parsed = null;
    try {
      parsed = JSON.parse(raw.trim());
    } catch {
      // Try stripping markdown
      const cleaned = raw.replace(/```json\n?|```/g, '').trim();
      try {
        parsed = JSON.parse(cleaned);
      } catch { /* ignore */ }
    }

    if (Array.isArray(parsed)) {
      return parsed
        .filter(d => d && typeof d === 'string' && d.trim().length > 0)
        .slice(0, 10)
        .map(d => ({
          text: d.trim().slice(0, 200),
          category: 'decision',
          importance: 0.8,
          extractedFrom: `episode:${episode.id}`,
          episodeId: episode.id,
          createdAt: Date.now(),
        }));
    }
  } catch (err) {
    console.warn('[EpisodeSummarizer] Decision extraction failed:', err.message);
  }

  // Fallback: use decisions from summary
  if (episode.decisions?.length) {
    return episode.decisions.slice(0, 5).map(d => ({
      text: d.slice(0, 200),
      category: 'decision',
      importance: 0.8,
      extractedFrom: `episode:${episode.id}`,
      episodeId: episode.id,
      createdAt: Date.now(),
    }));
  }

  return [];
}

/**
 * Summarize and store - full pipeline:
 * 1. Generate structured summary via LLM
 * 2. Extract decision memories
 * 3. Return summary + decision memories
 *
 * @param {object} episode
 * @returns {Promise<{summary: object, decisionMemories: Array}>}
 */
export async function summarizeAndExtract(episode) {
  const [summary, decisionMemories] = await Promise.all([
    summarizeEpisode(episode),
    extractDecisionMemories(episode),
  ]);

  return { summary, decisionMemories };
}

export default { summarizeEpisode, extractDecisionMemories, summarizeAndExtract };
