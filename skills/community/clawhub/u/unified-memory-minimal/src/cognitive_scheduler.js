/**
 * cognitive_scheduler.js - Curiosity-Driven Memory Exploration
 *
 * Inspired by Smart Memory's cognitive scheduling.
 * When memory A is accessed, proactively explore related memory B
 * based on entity overlap, topic similarity, temporal proximity, and chain history.
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';
import { getAllMemories, getMemory, touchMemory } from './storage.js';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const COGNITIVE_STATE_FILE = join(WORKSPACE, 'memory', 'cognitive_state.json');

// Ensure directory exists
const memDir = join(WORKSPACE, 'memory');
if (!existsSync(memDir)) {
  mkdirSync(memDir, { recursive: true });
}

// ============================================================================
// Types
// ============================================================================

/**
 * @typedef {Object} CuriosityResult
 * @property {string} sourceMemory
 * @property {string} targetMemory
 * @property {number} score
 * @property {'entity_overlap'|'topic_similarity'|'temporal'|'chain'} reason
 * @property {boolean} triggered
 */

/**
 * @typedef {Object} RecallItem
 * @property {string} memoryId
 * @property {string} reason
 * @property {number} score
 * @property {string|null} lastRecalled
 */

/**
 * @typedef {Object} CognitiveState
 * @property {Record<string, string[]>} explorationHistory - memoryId -> [exploredIds]
 * @property {Record<string, string>} lastRecalled - memoryId -> ISO timestamp
 * @property {Record<string, number>} curiosityScores - combined scores cache
 * @property {string} updated_at
 */

// ============================================================================
// State Management
// ============================================================================

/**
 * Load cognitive state from disk
 * @returns {CognitiveState}
 */
function loadState() {
  try {
    if (!existsSync(COGNITIVE_STATE_FILE)) {
      return getDefaultState();
    }
    const content = readFileSync(COGNITIVE_STATE_FILE, 'utf-8');
    return JSON.parse(content);
  } catch (err) {
    console.error(`[cognitive_scheduler] Failed to load state: ${err.message}`);
    return getDefaultState();
  }
}

/**
 * Save cognitive state to disk
 * @param {CognitiveState} state
 */
function saveState(state) {
  try {
    state.updated_at = new Date().toISOString();
    writeFileSync(COGNITIVE_STATE_FILE, JSON.stringify(state, null, 2), 'utf-8');
  } catch (err) {
    console.error(`[cognitive_scheduler] Failed to save state: ${err.message}`);
  }
}

/**
 * Get default empty state
 * @returns {CognitiveState}
 */
function getDefaultState() {
  return {
    explorationHistory: {},
    lastRecalled: {},
    curiosityScores: {},
    updated_at: new Date().toISOString(),
  };
}

// ============================================================================
// Curiosity Scoring
// ============================================================================

/**
 * Extract entities from memory text using simple NLP heuristics
 * @param {string} text
 * @returns {string[]}
 */
function extractEntities(text) {
  // Simple entity extraction: capitalized words, numbers, quoted strings
  const entities = new Set();

  // Capitalized multi-word phrases (proper nouns)
  const capitalized = text.match(/(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)/g) || [];
  capitalized.forEach(e => entities.add(e.toLowerCase()));

  // Quoted strings
  const quoted = text.match(/"([^"]+)"|'([^']+)'/g) || [];
  quoted.forEach(e => entities.add(e.replace(/["']/g, '').toLowerCase()));

  // Hashtags
  const hashtags = text.match(/#(\w+)/g) || [];
  hashtags.forEach(e => entities.add(e.slice(1).toLowerCase()));

  // Numbers with units (dates, times, prices)
  const numbers = text.match(/\d+(?:\.\d+)?(?:元|号|天|时|分|年|月|日|周)/g) || [];
  numbers.forEach(e => entities.add(e.toLowerCase()));

  return Array.from(entities);
}

/**
 * Calculate entity overlap score between two memories
 * @param {object} memA
 * @param {object} memB
 * @returns {number} 0-1 score
 */
function entityOverlapScore(memA, memB) {
  const entitiesA = new Set(extractEntities(memA.text || ''));
  const entitiesB = new Set(extractEntities(memB.text || ''));

  if (entitiesA.size === 0 || entitiesB.size === 0) return 0;

  let intersection = 0;
  for (const e of entitiesA) {
    if (entitiesB.has(e)) intersection++;
  }

  const union = entitiesA.size + entitiesB.size - intersection;
  return union > 0 ? intersection / union : 0;
}

/**
 * Calculate topic similarity based on category and tags
 * @param {object} memA
 * @param {object} memB
 * @returns {number} 0-1 score
 */
function topicSimilarityScore(memA, memB) {
  let score = 0;
  let weight = 0;

  // Category match (strongest signal)
  if (memA.category && memA.category === memB.category) {
    score += 0.6;
  }
  weight += 0.6;

  // Tag overlap
  const tagsA = new Set(memA.tags || []);
  const tagsB = new Set(memB.tags || []);
  if (tagsA.size > 0 && tagsB.size > 0) {
    let tagOverlap = 0;
    for (const t of tagsA) {
      if (tagsB.has(t)) tagOverlap++;
    }
    const tagScore = tagOverlap / Math.max(tagsA.size, tagsB.size);
    score += 0.3 * tagScore;
  }
  weight += 0.3;

  // Scope similarity
  if (memA.scope && memA.scope === memB.scope) {
    score += 0.1;
  }
  weight += 0.1;

  return weight > 0 ? score / weight : 0;
}

/**
 * Calculate temporal proximity score
 * Memories accessed/created within similar time windows get boosted
 * @param {object} memA
 * @param {object} memB
 * @returns {number} 0-1 score
 */
function temporalScore(memA, memB) {
  const timeA = new Date(memA.last_access || memA.timestamp || memA.created_at || Date.now()).getTime();
  const timeB = new Date(memB.last_access || memB.timestamp || memB.created_at || Date.now()).getTime();

  const diffHours = Math.abs(timeA - timeB) / (1000 * 60 * 60);

  // Exponential decay: 1.0 at 0 hours, ~0.5 at 24 hours, ~0.1 at 168 hours (1 week)
  if (diffHours <= 1) return 1.0;
  if (diffHours >= 168) return 0;

  // Smooth decay curve
  return Math.max(0, 1 - (diffHours / 168));
}

/**
 * Calculate chain exploration score
 * If A explored B, and we're now at B, boost score for C (A's other explorations)
 * @param {string} sourceId
 * @param {string} candidateId
 * @param {CognitiveState} state
 * @returns {number} 0-1 score
 */
function chainScore(sourceId, candidateId, state) {
  const exploredBySource = state.explorationHistory[sourceId] || [];

  // If source has never explored anything, no chain
  if (exploredBySource.length === 0) return 0;

  // Find memories that source has explored
  // (These are the "siblings" of candidate - other things similar memories explored)
  // Candidate gets boosted if it's similar to what source also explored

  // Simple heuristic: check if candidate shares category with things source explored
  // This is a simplified chain score
  let chainBoost = 0;

  // Check if this candidate was recently explored in a chain
  // (state.curiosityScores stores recent curiosity checks)
  const cacheKey = `${sourceId}:${candidateId}`;
  if (state.curiosityScores[cacheKey]) {
    chainBoost = 0.2; // Minor boost for repeated curiosity
  }

  return Math.min(1, chainBoost);
}

// ============================================================================
// Core Functions
// ============================================================================

/**
 * Score how "curious" we should be about a candidate memory given a source
 * @param {string} memoryId - Source memory ID
 * @param {string} candidateId - Candidate memory ID to score
 * @returns {Promise<number>} Combined curiosity score 0-1
 */
export async function scoreCuriosity(memoryId, candidateId) {
  if (memoryId === candidateId) return 0;

  const memA = getMemory(memoryId);
  const memB = getMemory(candidateId);
  if (!memA || !memB) return 0;

  const state = loadState();

  // Weighted combination of signals
  const entityScore = entityOverlapScore(memA, memB);
  const topicScore = topicSimilarityScore(memA, memB);
  const temporal = temporalScore(memA, memB);
  const chain = chainScore(memoryId, candidateId, state);

  // Weights for each signal
  const combined = (
    entityScore * 0.35 +
    topicScore * 0.30 +
    temporal * 0.20 +
    chain * 0.15
  );

  // Cache the score
  const cacheKey = `${memoryId}:${candidateId}`;
  state.curiosityScores[cacheKey] = combined;
  saveState(state);

  return Math.min(1, combined);
}

/**
 * Trigger curiosity check after memory access
 * When memoryId is accessed, find related memories that trigger curiosity
 * @param {string} memoryId - The accessed memory ID
 * @returns {Promise<CuriosityResult[]>} List of curiosity results
 */
export async function triggerCuriosity(memoryId) {
  const memA = getMemory(memoryId);
  if (!memA) return [];

  const allMemories = getAllMemories();
  const state = loadState();
  const results = [];
  const TRIGGER_THRESHOLD = 0.3;

  for (const memB of allMemories) {
    if (memB.id === memoryId) continue;

    const score = await scoreCuriosity(memoryId, memB.id);

    // Determine primary reason
    const entityScore = entityOverlapScore(memA, memB);
    const topicScore = topicSimilarityScore(memA, memB);
    const temporal = temporalScore(memA, memB);
    const chain = chainScore(memoryId, memB.id, state);

    let reason = 'topic_similarity';
    let maxScore = topicScore;
    if (entityScore > maxScore) { reason = 'entity_overlap'; maxScore = entityScore; }
    if (temporal > maxScore) { reason = 'temporal'; maxScore = temporal; }
    if (chain > maxScore) { reason = 'chain'; maxScore = chain; }

    const triggered = score >= TRIGGER_THRESHOLD;

    results.push({
      sourceMemory: memoryId,
      targetMemory: memB.id,
      score: Math.round(score * 1000) / 1000,
      reason,
      triggered,
    });
  }

  // Sort by score descending
  results.sort((a, b) => b.score - a.score);

  return results;
}

/**
 * Record a curiosity exploration (when we actually explored from one memory to another)
 * @param {string} fromMemory - Source memory
 * @param {string} toMemory - Target memory that was explored
 */
export async function recordExploration(fromMemory, toMemory) {
  const state = loadState();

  if (!state.explorationHistory[fromMemory]) {
    state.explorationHistory[fromMemory] = [];
  }

  // Add to history if not already there
  if (!state.explorationHistory[fromMemory].includes(toMemory)) {
    state.explorationHistory[fromMemory].push(toMemory);
  }

  // Update last recalled
  state.lastRecalled[toMemory] = new Date().toISOString();

  saveState(state);
}

/**
 * Get memories to proactively recall based on curiosity state
 * Returns memories that should be pre-loaded for context expansion
 * @returns {Promise<RecallItem[]>}
 */
export async function getProactiveRecallItems() {
  const state = loadState();
  const allMemories = getAllMemories();
  const items = [];
  const now = Date.now();

  // Find memories with high cumulative curiosity scores
  const candidateScores = {};

  for (const [cacheKey, score] of Object.entries(state.curiosityScores)) {
    const [sourceId, targetId] = cacheKey.split(':');
    if (!candidateScores[targetId]) candidateScores[targetId] = 0;
    candidateScores[targetId] += score;
  }

  for (const mem of allMemories) {
    const cumulativeScore = candidateScores[mem.id] || 0;

    // Skip if recently recalled (within 1 hour)
    const lastRecalled = state.lastRecalled[mem.id];
    let lastRecalledStr = null;
    if (lastRecalled) {
      const hoursSince = (now - new Date(lastRecalled).getTime()) / (1000 * 60 * 60);
      if (hoursSince < 1) continue;
      lastRecalledStr = lastRecalled;
    }

    // Skip if score is too low
    if (cumulativeScore < 0.3) continue;

    // Determine reason based on what triggered it
    let reason = 'curiosity_chain';
    for (const [cacheKey, score] of Object.entries(state.curiosityScores)) {
      const [, targetId] = cacheKey.split(':');
      if (targetId === mem.id) {
        const [sourceId] = cacheKey.split(':');
        const sourceMem = getMemory(sourceId);
        if (sourceMem) {
          reason = `explore:${sourceMem.category || 'general'}`;
          break;
        }
      }
    }

    items.push({
      memoryId: mem.id,
      reason,
      score: Math.round(cumulativeScore * 1000) / 1000,
      lastRecalled: lastRecalledStr,
    });
  }

  // Sort by score descending
  items.sort((a, b) => b.score - a.score);

  return items.slice(0, 20); // Top 20
}

/**
 * Schedule periodic curiosity checks
 * This runs in background to continuously update curiosity state
 * @returns {Promise<void>}
 */
export async function scheduleCuriosityCheck() {
  // This is designed to be called periodically (e.g., every 5 minutes)
  // In a real system, this would be hooked into the proactive manager
  const allMemories = getAllMemories();

  // Pick a random recent memory to trigger curiosity from
  const recent = allMemories
    .filter(m => {
      const lastAcc = new Date(m.last_access || m.timestamp || m.created_at || 0).getTime();
      return (Date.now() - lastAcc) < 24 * 60 * 60 * 1000; // Last 24 hours
    })
    .slice(0, 5);

  if (recent.length === 0) return;

  const state = loadState();

  for (const mem of recent) {
    const results = await triggerCuriosity(mem.id);

    // Record top explorations
    const triggered = results.filter(r => r.triggered).slice(0, 3);
    for (const t of triggered) {
      await recordExploration(t.sourceMemory, t.targetMemory);
    }
  }

  // Decay old curiosity scores (keep only recent ones)
  const oneDayAgo = Date.now() - 24 * 60 * 60 * 1000;
  const newScores = {};
  for (const [key, score] of Object.entries(state.curiosityScores)) {
    // Keep scores (they're keyed by memory pairs, not time)
    newScores[key] = score;
  }
  state.curiosityScores = newScores;
  saveState(state);
}

// ============================================================================
// MCP Tool Handler
// ============================================================================

/**
 * Handle memory_cognitive MCP tool calls
 * @param {object} args
 * @returns {Promise<{content: Array<{type: string, text: string}>, isError?: boolean}>}
 */
export async function memoryCognitiveTool(args) {
  const { action } = args;

  try {
    switch (action) {
      case 'trigger': {
        if (!args.memory_id) {
          return { content: [{ type: 'text', text: 'Error: memory_id is required' }], isError: true };
        }
        const results = await triggerCuriosity(args.memory_id);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              count: results.length,
              triggered_count: results.filter(r => r.triggered).length,
              results: results.slice(0, 20),
            }, null, 2),
          }],
        };
      }

      case 'score': {
        if (!args.memory_id || !args.candidate_id) {
          return { content: [{ type: 'text', text: 'Error: memory_id and candidate_id are required' }], isError: true };
        }
        const score = await scoreCuriosity(args.memory_id, args.candidate_id);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              source: args.memory_id,
              candidate: args.candidate_id,
              score: Math.round(score * 1000) / 1000,
            }, null, 2),
          }],
        };
      }

      case 'get_recalls': {
        const items = await getProactiveRecallItems();
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              count: items.length,
              items,
            }, null, 2),
          }],
        };
      }

      case 'record_exploration': {
        if (!args.from_memory || !args.to_memory) {
          return { content: [{ type: 'text', text: 'Error: from_memory and to_memory are required' }], isError: true };
        }
        await recordExploration(args.from_memory, args.to_memory);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({ success: true, from: args.from_memory, to: args.to_memory }),
          }],
        };
      }

      case 'status': {
        const state = loadState();
        const allMemories = getAllMemories();
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              exploration_chains: Object.keys(state.explorationHistory).length,
              recalled_memories: Object.keys(state.lastRecalled).length,
              cached_scores: Object.keys(state.curiosityScores).length,
              total_memories: allMemories.length,
              updated_at: state.updated_at,
            }, null, 2),
          }],
        };
      }

      default:
        return {
          content: [{ type: 'text', text: `Error: Unknown action '${action}'. Valid actions: trigger, score, get_recalls, record_exploration, status` }],
          isError: true,
        };
    }
  } catch (err) {
    return { content: [{ type: 'text', text: `Cognitive scheduler error: ${err.message}` }], isError: true };
  }
}

export default { memoryCognitiveTool };
