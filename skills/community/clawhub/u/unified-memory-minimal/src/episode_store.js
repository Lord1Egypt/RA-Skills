/**
 * Episode Store - Persistent storage for conversation episodes
 *
 * An "episode" = a complete conversation session (multiple messages exchanged).
 * Stored separately from individual memories in ~/.openclaw/workspace/memory/episodes.json
 *
 * Episode states: ACTIVE (in-progress), COMPLETED (finished + summarized), ARCHIVED (cold storage)
 *
 * Structure:
 * {
 *   episodes: Episode[],
 *   archive: Episode[],  // cold storage for old episodes
 *   metadata: { version, lastUpdated, episodeCount }
 * }
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';
import { config } from './config.js';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const EPISODE_STATUS = {
  ACTIVE: 'active',
  COMPLETED: 'completed',
  ARCHIVED: 'archived',
};

const EPISODE_FILE = join(config.memoryDir, 'episodes.json');

/** @type {Map<string, any>} */
const episodeCache = new Map();
let cacheDirty = false;

// ─── File I/O ────────────────────────────────────────────────────────────────

function ensureDir() {
  const dir = config.memoryDir;
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
}

function loadEpisodeStore() {
  ensureDir();
  if (!existsSync(EPISODE_FILE)) {
    return createEmptyStore();
  }
  try {
    const raw = JSON.parse(readFileSync(EPISODE_FILE, 'utf-8'));
    return {
      episodes: Array.isArray(raw.episodes) ? raw.episodes : [],
      archive: Array.isArray(raw.archive) ? raw.archive : [],
      metadata: raw.metadata || { version: '1.0', lastUpdated: Date.now(), episodeCount: 0 },
    };
  } catch {
    return createEmptyStore();
  }
}

function createEmptyStore() {
  return {
    episodes: [],
    archive: [],
    metadata: {
      version: '1.0',
      lastUpdated: Date.now(),
      episodeCount: 0,
    },
  };
}

function saveEpisodeStore(store) {
  ensureDir();
  store.metadata.lastUpdated = Date.now();
  store.metadata.episodeCount = store.episodes.length + store.archive.length;
  writeFileSync(EPISODE_FILE, JSON.stringify(store, null, 2), 'utf-8');
  episodeCache.set('store', store);
  cacheDirty = false;
}

function getStore() {
  if (!episodeCache.has('store')) {
    episodeCache.set('store', loadEpisodeStore());
  }
  return episodeCache.get('store');
}

// ─── Episode CRUD ─────────────────────────────────────────────────────────────

/**
 * Create a new episode
 * @param {string} sessionId - unique session identifier
 * @param {string[]} participants - list of participant identifiers
 * @param {object} [metadata] - optional extra metadata
 * @returns {object} created episode
 */
export function createEpisode(sessionId, participants = [], metadata = {}) {
  const store = getStore();

  // Check for existing active episode with same sessionId
  const existing = store.episodes.find(
    e => e.sessionId === sessionId && e.state === EPISODE_STATUS.ACTIVE
  );
  if (existing) {
    return existing;
  }

  const now = Date.now();
  /** @type {object} */
  const episode = {
    id: `ep_${now}_${Math.random().toString(36).slice(2, 8)}`,
    sessionId,
    participants: [...participants],
    state: EPISODE_STATUS.ACTIVE,
    startTime: now,
    endTime: null,
    lastActivity: now,
    messageCount: 0,
    messages: [],
    summary: null,
    title: metadata.title || null,
    keyTopics: [],
    decisions: [],
    nextSteps: [],
    tags: metadata.tags || [],
    memoryIds: [], // references to memories created during this episode
    createdAt: now,
  };

  store.episodes.push(episode);
  cacheDirty = true;
  saveEpisodeStore(store);
  return episode;
}

/**
 * Get episode by ID or sessionId
 * @param {string} id - episode id or sessionId
 * @param {boolean} [includeArchived=false] - also search archive
 * @returns {object|null}
 */
export function getEpisode(id, includeArchived = false) {
  const store = getStore();
  let found = store.episodes.find(e => e.id === id || e.sessionId === id);
  if (!found && includeArchived) {
    found = store.archive.find(e => e.id === id || e.sessionId === id);
  }
  return found || null;
}

/**
 * Get the current active episode for a session (if any)
 * @param {string} sessionId
 * @returns {object|null}
 */
export function getActiveEpisode(sessionId) {
  const store = getStore();
  return store.episodes.find(
    e => e.sessionId === sessionId && e.state === EPISODE_STATUS.ACTIVE
  ) || null;
}

/**
 * Add a message to an episode
 * @param {string} episodeId
 * @param {string} role - 'user'|'assistant'|'system'
 * @param {string} content - message text
 * @param {string} [messageId] - optional external message ID
 * @returns {boolean}
 */
export function addMessageToEpisode(episodeId, role, content, messageId = null) {
  const store = getStore();
  const episode = store.episodes.find(e => e.id === episodeId);
  if (!episode || episode.state !== EPISODE_STATUS.ACTIVE) {
    return false;
  }

  const now = Date.now();
  const message = {
    id: `msg_${now}_${Math.random().toString(36).slice(2, 6)}`,
    messageId: messageId || null,
    role,
    content,
    timestamp: now,
  };

  episode.messages.push(message);
  episode.messageCount = episode.messages.length;
  episode.lastActivity = now;
  cacheDirty = true;
  saveEpisodeStore(store);
  return true;
}

/**
 * Update episode metadata
 * @param {string} episodeId
 * @param {object} updates
 * @returns {boolean}
 */
export function updateEpisode(episodeId, updates) {
  const store = getStore();
  const episode = store.episodes.find(e => e.id === episodeId);
  if (!episode) return false;

  // Only allow updating certain fields
  const allowed = ['title', 'keyTopics', 'decisions', 'nextSteps', 'tags', 'participants'];
  for (const key of allowed) {
    if (key in updates) {
      episode[key] = updates[key];
    }
  }
  cacheDirty = true;
  saveEpisodeStore(store);
  return true;
}

/**
 * Complete an episode - transitions from ACTIVE to COMPLETED
 * @param {string} episodeId
 * @param {object} summaryData - { title, keyTopics, decisions, nextSteps, summary }
 * @returns {boolean}
 */
export function completeEpisode(episodeId, summaryData = {}) {
  const store = getStore();
  const episode = store.episodes.find(e => e.id === episodeId);
  if (!episode || episode.state !== EPISODE_STATUS.ACTIVE) {
    return false;
  }

  episode.state = EPISODE_STATUS.COMPLETED;
  episode.endTime = Date.now();
  episode.summary = summaryData.summary || null;
  episode.title = summaryData.title || episode.title || null;
  episode.keyTopics = summaryData.keyTopics || episode.keyTopics || [];
  episode.decisions = summaryData.decisions || episode.decisions || [];
  episode.nextSteps = summaryData.nextSteps || episode.nextSteps || [];
  cacheDirty = true;
  saveEpisodeStore(store);
  return true;
}

/**
 * Add memory ID references to an episode
 * @param {string} episodeId
 * @param {string[]} memoryIds
 * @returns {boolean}
 */
export function linkMemoriesToEpisode(episodeId, memoryIds) {
  const store = getStore();
  const episode = store.episodes.find(e => e.id === episodeId);
  if (!episode) return false;

  for (const mid of memoryIds) {
    if (!episode.memoryIds.includes(mid)) {
      episode.memoryIds.push(mid);
    }
  }
  cacheDirty = true;
  saveEpisodeStore(store);
  return true;
}

/**
 * Archive old episodes (move from episodes[] to archive[])
 * @param {number} [daysOld=30] - archive episodes older than this many days
 * @returns {number} number of episodes archived
 */
export function archiveOldEpisodes(daysOld = 30) {
  const store = getStore();
  const cutoff = Date.now() - daysOld * 24 * 60 * 60 * 1000;

  const toArchive = store.episodes.filter(
    e => e.state === EPISODE_STATUS.COMPLETED && e.endTime && e.endTime < cutoff
  );

  if (toArchive.length === 0) return 0;

  // Move to archive
  for (const ep of toArchive) {
    ep.state = EPISODE_STATUS.ARCHIVED;
    store.archive.push(ep);
  }

  // Remove from active list
  store.episodes = store.episodes.filter(
    e => !toArchive.some(a => a.id === e.id)
  );

  cacheDirty = true;
  saveEpisodeStore(store);
  return toArchive.length;
}

/**
 * Get all episodes (optionally filtered by state)
 * @param {string} [state] - ACTIVE|COMPLETED|ARCHIVED
 * @param {object} [opts]
 * @param {number} [opts.limit=50]
 * @param {number} [opts.offset=0]
 * @param {boolean} [opts.includeArchived=false]
 * @returns {object[]}
 */
export function listEpisodes(state = null, opts = {}) {
  const { limit = 50, offset = 0, includeArchived = false } = opts;
  const store = getStore();

  let episodes = includeArchived
    ? [...store.episodes, ...store.archive]
    : store.episodes;

  if (state) {
    episodes = episodes.filter(e => e.state === state);
  }

  // Sort by lastActivity descending (most recent first)
  episodes.sort((a, b) => (b.lastActivity || 0) - (a.lastActivity || 0));

  return episodes.slice(offset, offset + limit);
}

/**
 * Delete an episode permanently
 * @param {string} episodeId
 * @returns {boolean}
 */
export function deleteEpisode(episodeId) {
  const store = getStore();
  const idx = store.episodes.findIndex(e => e.id === episodeId);
  if (idx !== -1) {
    store.episodes.splice(idx, 1);
    cacheDirty = true;
    saveEpisodeStore(store);
    return true;
  }
  const arcIdx = store.archive.findIndex(e => e.id === episodeId);
  if (arcIdx !== -1) {
    store.archive.splice(arcIdx, 1);
    cacheDirty = true;
    saveEpisodeStore(store);
    return true;
  }
  return false;
}

/**
 * Get episode count stats
 * @returns {object}
 */
export function getEpisodeStats() {
  const store = getStore();
  return {
    active: store.episodes.filter(e => e.state === EPISODE_STATUS.ACTIVE).length,
    completed: store.episodes.filter(e => e.state === EPISODE_STATUS.COMPLETED).length,
    archived: store.archive.length,
    total: store.metadata.episodeCount,
    lastUpdated: store.metadata.lastUpdated,
  };
}

/**
 * Get recent episodes (last N by endTime or lastActivity)
 * @param {number} [n=10]
 * @param {boolean} [includeArchived=false]
 * @returns {object[]}
 */
export function getRecentEpisodes(n = 10, includeArchived = false) {
  const store = getStore();
  let episodes = includeArchived
    ? [...store.episodes, ...store.archive]
    : store.episodes;

  episodes.sort((a, b) => (b.lastActivity || 0) - (a.lastActivity || 0));
  return episodes.slice(0, n);
}

export { EPISODE_STATUS };
export default {
  createEpisode,
  getEpisode,
  getActiveEpisode,
  addMessageToEpisode,
  updateEpisode,
  completeEpisode,
  linkMemoriesToEpisode,
  archiveOldEpisodes,
  listEpisodes,
  deleteEpisode,
  getEpisodeStats,
  getRecentEpisodes,
  EPISODE_STATUS,
};
