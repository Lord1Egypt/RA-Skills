/**
 * Episode Manager - High-level API for episode lifecycle management
 *
 * Orchestrates episode_store + episode_summarizer to provide
 * a complete episode lifecycle: start → add messages → complete → archive.
 *
 * Also manages auto-capture boundaries (time gap, message count).
 */

import {
  createEpisode,
  getEpisode,
  getActiveEpisode,
  addMessageToEpisode,
  updateEpisode,
  completeEpisode as storeCompleteEpisode,
  linkMemoriesToEpisode,
  archiveOldEpisodes as storeArchive,
  listEpisodes,
  getRecentEpisodes,
  getEpisodeStats as getStoreEpisodeStats,
  deleteEpisode,
  EPISODE_STATUS,
} from './episode_store.js';

import {
  summarizeEpisode,
  summarizeAndExtract,
} from './episode_summarizer.js';

import { addMemory } from './storage.js';

const DEFAULT_EPISODE_GAP_MS = 5 * 60 * 1000; // 5 minutes gap → new episode
const DEFAULT_MAX_MESSAGES = 100;             // force complete after N messages

// ─── Active Episode Tracking ───────────────────────────────────────────────────

/** @type {Map<string, {episodeId: string, lastMessageTs: number, messageCount: number}>} */
const activeTracker = new Map();

function getTrackerKey(sessionId, participant) {
  return `${sessionId}:${participant || 'default'}`;
}

// ─── Episode Lifecycle ────────────────────────────────────────────────────────

/**
 * Start a new episode for a session/participant
 * @param {string} sessionId - conversation session ID
 * @param {string[]} [participants] - participant IDs/names
 * @param {object} [metadata] - optional { title, tags }
 * @returns {object} created episode
 */
export function startEpisode(sessionId, participants = [], metadata = {}) {
  // End any existing active episode for this session
  const existing = getActiveEpisode(sessionId);
  if (existing) {
    // Auto-complete existing before starting new
    completeEpisode(existing.id).catch(err => {
      console.warn('[EpisodeManager] auto-complete failed:', err.message);
    });
  }

  const episode = createEpisode(sessionId, participants, metadata);

  // Initialize tracker
  const key = getTrackerKey(sessionId, participants[0] || 'default');
  activeTracker.set(key, {
    episodeId: episode.id,
    lastMessageTs: Date.now(),
    messageCount: 0,
  });

  return episode;
}

/**
 * Add a message to an episode, with auto-boundary detection.
 *
 * Auto-boundary rules:
 * 1. If gap between messages > episodeGapMs → start new episode
 * 2. If messageCount > maxMessages → force complete current + start new
 *
 * @param {string} sessionId
 * @param {string} role - 'user'|'assistant'|'system'
 * @param {string} content - message content
 * @param {string} [messageId]
 * @param {object} [opts]
 * @param {number} [opts.episodeGapMs=300000] - 5min gap threshold
 * @param {number} [opts.maxMessages=100]
 * @param {string} [opts.participant]
 * @returns {Promise<{added: boolean, episodeChanged: boolean, newEpisodeId: string|null}>}
 */
export async function addMessage(sessionId, role, content, messageId = null, opts = {}) {
  const {
    episodeGapMs = DEFAULT_EPISODE_GAP_MS,
    maxMessages = DEFAULT_MAX_MESSAGES,
    participant = 'default',
  } = opts;

  const trackerKey = getTrackerKey(sessionId, participant);
  let tracker = activeTracker.get(trackerKey);
  const now = Date.now();

  // Check if we need to start a new episode due to time gap
  if (tracker) {
    const gap = now - tracker.lastMessageTs;
    if (gap > episodeGapMs) {
      // Time gap exceeded → complete old, start new
      const oldEpisode = getEpisode(tracker.episodeId);
      if (oldEpisode && oldEpisode.state === EPISODE_STATUS.ACTIVE) {
        await completeEpisode(tracker.episodeId).catch(() => {});
      }
      tracker = null;
    }
  }

  // Get or create episode
  let episode;
  if (tracker) {
    episode = getEpisode(tracker.episodeId);
  }

  if (!episode || episode.state !== EPISODE_STATUS.ACTIVE) {
    // Start new episode
    episode = startEpisode(sessionId, [participant]);
    tracker = activeTracker.get(trackerKey) || {
      episodeId: episode.id,
      lastMessageTs: now,
      messageCount: 0,
    };
  }

  // Check message count limit
  const messageCount = (episode.messageCount || 0) + 1;
  if (messageCount > maxMessages) {
    // Complete current and start fresh
    await completeEpisode(episode.id).catch(() => {});
    episode = startEpisode(sessionId, [participant]);
    tracker = {
      episodeId: episode.id,
      lastMessageTs: now,
      messageCount: 0,
    };
  }

  // Add the message
  const added = addMessageToEpisode(episode.id, role, content, messageId);

  // Update tracker
  tracker.lastMessageTs = now;
  tracker.messageCount = (tracker.messageCount || 0) + 1;
  activeTracker.set(trackerKey, tracker);

  return {
    added,
    episodeId: episode.id,
    messageCount: tracker.messageCount,
  };
}

/**
 * Complete an episode: generate summary + extract decision memories
 * @param {string} episodeId
 * @param {object} [overrideSummary] - optionally provide summary directly
 * @returns {Promise<{episode: object, summary: object, decisionMemories: Array}>}
 */
export async function completeEpisode(episodeId, overrideSummary = null) {
  const episode = getEpisode(episodeId);
  if (!episode) {
    throw new Error(`Episode not found: ${episodeId}`);
  }

  if (episode.state !== EPISODE_STATUS.ACTIVE) {
    throw new Error(`Episode already ${episode.state}: ${episodeId}`);
  }

  // Generate summary
  const summaryData = overrideSummary || await summarizeEpisode(episode);

  // Store decision memories
  const decisionMemories = [];
  if (summaryData.decisions?.length || episode.decisions?.length) {
    const decisions = summaryData.decisions || episode.decisions || [];
    for (const d of decisions) {
      try {
        const mem = addMemory({
          text: d,
          category: 'decision',
          importance: 0.8,
          tags: ['episode-decision', `ep:${episodeId}`],
        });
        decisionMemories.push(mem);

        // Link memory to episode
        linkMemoriesToEpisode(episodeId, [mem.id]);
      } catch (err) {
        console.warn('[EpisodeManager] failed to store decision memory:', err.message);
      }
    }
  }

  // Complete in store
  storeCompleteEpisode(episodeId, summaryData);

  // Clean up tracker
  for (const [key, tracker] of activeTracker.entries()) {
    if (tracker.episodeId === episodeId) {
      activeTracker.delete(key);
      break;
    }
  }

  return {
    episode: getEpisode(episodeId),
    summary: summaryData,
    decisionMemories,
  };
}

/**
 * Archive old completed episodes
 * @param {number} [daysOld=30]
 * @returns {number} count archived
 */
export function archiveOldEpisodes(daysOld = 30) {
  return storeArchive(daysOld);
}

/**
 * Search within episodes using full-text search on message content
 * @param {string} query
 * @param {object} [opts]
 * @param {number} [opts.limit=10]
 * @param {string} [opts.state] - ACTIVE|COMPLETED|ARCHIVED
 * @param {boolean} [opts.includeArchived=false]
 * @returns {Array<{episode: object, matchedMessages: Array, relevance: number}>}
 */
export function searchEpisodes(query, opts = {}) {
  const { limit = 10, state = null, includeArchived = false } = opts;

  const episodes = listEpisodes(state, { limit: 100, includeArchived });
  const queryLower = query.toLowerCase();
  const results = [];

  for (const episode of episodes) {
    const messages = episode.messages || [];
    const matchedMessages = [];

    for (const msg of messages) {
      const content = msg.content || '';
      if (content.toLowerCase().includes(queryLower)) {
        // Score based on position (earlier = slightly higher weight)
        const posScore = 1 - (messages.indexOf(msg) / Math.max(messages.length, 1)) * 0.3;
        const lenNorm = 1 / Math.log2(Math.max(content.length, 2));
        matchedMessages.push({
          ...msg,
          relevance: Math.round(posScore * 100) / 100,
        });
      }
    }

    if (matchedMessages.length > 0) {
      // Overall episode relevance = avg of matched message relevance
      const avgRelevance = matchedMessages.reduce((s, m) => s + m.relevance, 0) / matchedMessages.length;

      // Also check summary/title/topics
      let titleBoost = 0;
      if (episode.title && episode.title.toLowerCase().includes(queryLower)) titleBoost = 0.2;
      if (episode.keyTopics?.some(t => t.toLowerCase().includes(queryLower))) titleBoost = Math.max(titleBoost, 0.15);

      results.push({
        episode,
        matchedMessages: matchedMessages.sort((a, b) => b.relevance - a.relevance),
        relevance: Math.min(avgRelevance + titleBoost, 1.0),
        matchCount: matchedMessages.length,
      });
    }
  }

  // Sort by relevance desc, then match count desc
  results.sort((a, b) => {
    if (b.relevance !== a.relevance) return b.relevance - a.relevance;
    return b.matchCount - a.matchCount;
  });

  return results.slice(0, limit);
}

/**
 * Get episode context for a query - retrieve episode messages as context
 * Used by search.js to supplement search results with episode context
 * @param {string} query
 * @param {number} [maxMessages=10]
 * @returns {Promise<Array<{episodeId: string, sessionId: string, title: string, messages: Array, relevance: number}>>}
 */
export async function getEpisodeContext(query, maxMessages = 10) {
  const results = searchEpisodes(query, { limit: 5, includeArchived: false });

  return results.map(r => ({
    episodeId: r.episode.id,
    sessionId: r.episode.sessionId,
    title: r.episode.title || r.episode.summary || `Session ${r.episode.id.slice(0, 8)}`,
    messages: r.matchedMessages.slice(0, maxMessages).map(m => ({
      role: m.role,
      content: m.content,
      timestamp: m.timestamp,
      relevance: m.relevance,
    })),
    relevance: r.relevance,
    keyTopics: r.episode.keyTopics || [],
    decisions: r.episode.decisions || [],
  }));
}

/**
 * List episodes with pagination
 * @param {object} [opts]
 * @param {string} [opts.state]
 * @param {number} [opts.limit=20]
 * @param {number} [opts.offset=0]
 * @param {boolean} [opts.includeArchived=false]
 * @returns {object}
 */
export function episodeList(opts = {}) {
  const episodes = listEpisodes(opts.state, opts);
  return {
    episodes: episodes.map(e => ({
      id: e.id,
      sessionId: e.sessionId,
      state: e.state,
      startTime: e.startTime ? new Date(e.startTime).toISOString() : null,
      endTime: e.endTime ? new Date(e.endTime).toISOString() : null,
      lastActivity: e.lastActivity ? new Date(e.lastActivity).toISOString() : null,
      messageCount: e.messageCount,
      title: e.title || e.summary || null,
      keyTopics: e.keyTopics || [],
      participants: e.participants || [],
      summary: e.summary || null,
    })),
    stats: getEpisodeStats(),
  };
}

/**
 * Get a single episode with full messages
 * @param {string} episodeId
 * @returns {object|null}
 */
export function getEpisodeWithMessages(episodeId) {
  const episode = getEpisode(episodeId, true);
  if (!episode) return null;
  return episode;
}

export function getEpisodeStats() {
  return getStoreEpisodeStats();
}
