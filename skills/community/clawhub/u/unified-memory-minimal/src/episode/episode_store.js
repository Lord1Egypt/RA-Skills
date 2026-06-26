/**
 * Episode Store v2 - Persistent storage for conversation episodes (v2 schema)
 *
 * Episode = a self-contained conversation unit around a single topic.
 * Default 8 turns, auto-splits when exceeded.
 *
 * Storage: memory/episodes.json
 * Schema:
 * {
 *   episodes: Episode[],
 *   metadata: { version, lastUpdated }
 * }
 *
 * Episode {
 *   id: "ep_<hash>",
 *   topic: "刘总问unified-memory功能",
 *   started_at: "2026-03-28T10:00:00+08:00",
 *   ended_at: "2026-03-28T10:30:00+08:00",
 *   turns: 12,           // conversation rounds (user+assistant)
 *   message_count: 24,  // raw message count
 *   memory_ids: [],     // associated memory IDs
 *   entities: [],       // extracted entities
 *   last_refresh: "...",
 *   status: "active" | "completed"
 * }
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { config } from '../config.js';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const EPISODE_FILE = path.join(config.memoryDir, 'episodes.json');

const EPISODE_STATUS = {
  ACTIVE: 'active',
  COMPLETED: 'completed',
};

const DEFAULT_MAX_TURNS = 8;

// ─── File I/O ────────────────────────────────────────────────────────────────

function ensureDir() {
  if (!existsSync(config.memoryDir)) {
    mkdirSync(config.memoryDir, { recursive: true });
  }
}

function loadEpisodes() {
  ensureDir();
  if (!existsSync(EPISODE_FILE)) {
    return createEmptyStore();
  }
  try {
    const raw = JSON.parse(readFileSync(EPISODE_FILE, 'utf-8'));
    return {
      episodes: Array.isArray(raw.episodes) ? raw.episodes : [],
      metadata: raw.metadata || { version: '2.0', lastUpdated: Date.now() },
    };
  } catch {
    return createEmptyStore();
  }
}

function createEmptyStore() {
  return {
    episodes: [],
    metadata: { version: '2.0', lastUpdated: Date.now() },
  };
}

function saveEpisodes(store) {
  ensureDir();
  store.metadata.lastUpdated = Date.now();
  writeFileSync(EPISODE_FILE, JSON.stringify(store, null, 2), 'utf-8');
}

function getStore() {
  return loadEpisodes();
}

// ─── ID Generation ───────────────────────────────────────────────────────────

function generateId(topic) {
  const seed = `${topic || 'untitled'}_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
  const hash = seed.split('').reduce((acc, c) => ((acc << 5) - acc + c.charCodeAt(0)) | 0, 0);
  return `ep_${Math.abs(hash).toString(36).slice(0, 12)}`;
}

// ─── Episode CRUD ───────────────────────────────────────────────────────────

/**
 * Create a new episode
 * @param {string} topic - Episode topic/title
 * @param {object} [opts]
 * @param {string[]} [opts.entities] - Pre-extracted entities
 * @returns {object} New episode
 */
export function createEpisode(topic, opts = {}) {
  const store = getStore();
  const now = new Date().toISOString();

  // End any existing active episode first
  const active = store.episodes.find(e => e.status === EPISODE_STATUS.ACTIVE);
  if (active) {
    endEpisodeInternal(store, active.id);
  }

  /** @type {object} */
  const episode = {
    id: generateId(topic),
    topic: topic || 'Untitled Episode',
    started_at: now,
    ended_at: null,
    turns: 0,
    message_count: 0,
    memory_ids: [],
    entities: opts.entities || [],
    last_refresh: now,
    status: EPISODE_STATUS.ACTIVE,
  };

  store.episodes.push(episode);
  saveEpisodes(store);
  return episode;
}

/**
 * End an episode — marks completed and generates a summary
 * @param {string} id - Episode ID
 * @returns {object|null} Updated episode or null if not found
 */
export function endEpisode(id) {
  const store = getStore();
  const updated = endEpisodeInternal(store, id);
  if (updated) saveEpisodes(store);
  return updated;
}

function endEpisodeInternal(store, id) {
  const episode = store.episodes.find(e => e.id === id);
  if (!episode || episode.status !== EPISODE_STATUS.ACTIVE) return null;

  const now = new Date().toISOString();
  episode.ended_at = now;
  episode.status = EPISODE_STATUS.COMPLETED;
  episode.last_refresh = now;
  return episode;
}

/**
 * Update episode fields
 * @param {string} id
 * @param {object} updates - Allowed: topic, entities, memory_ids, last_refresh
 * @returns {boolean}
 */
export function updateEpisode(id, updates) {
  const store = getStore();
  const episode = store.episodes.find(e => e.id === id);
  if (!episode) return false;

  const allowed = ['topic', 'entities', 'memory_ids', 'last_refresh', 'turns', 'message_count'];
  for (const key of allowed) {
    if (key in updates) episode[key] = updates[key];
  }
  episode.last_refresh = new Date().toISOString();
  saveEpisodes(store);
  return true;
}

/**
 * Get the currently active episode (if any)
 * @returns {object|null}
 */
export function getActiveEpisode() {
  const store = getStore();
  return store.episodes.find(e => e.status === EPISODE_STATUS.ACTIVE) || null;
}

/**
 * Get episode by ID
 * @param {string} id
 * @returns {object|null}
 */
export function getEpisode(id) {
  const store = getStore();
  return store.episodes.find(e => e.id === id) || null;
}

/**
 * Auto-split an episode if turns exceed maxTurns.
 * Creates a new episode continuing the same topic.
 * Returns { original, newEpisode }
 * @param {string} id - Episode ID to check
 * @param {number} [maxTurns] - Threshold for split (default 8)
 * @returns {object|null} null if no split needed, or { original, newEpisode }
 */
export function autoSplitEpisode(id, maxTurns = DEFAULT_MAX_TURNS) {
  const store = getStore();
  const episode = store.episodes.find(e => e.id === id);
  if (!episode) return null;

  if (episode.turns <= maxTurns) return null;

  // Create continuation episode with same topic
  const now = new Date().toISOString();
  const newEpisode = {
    id: generateId(episode.topic),
    topic: episode.topic,
    started_at: now,
    ended_at: null,
    turns: 0,
    message_count: 0,
    memory_ids: [],
    entities: [...episode.entities],
    last_refresh: now,
    status: EPISODE_STATUS.ACTIVE,
  };

  // End the original
  episode.ended_at = now;
  episode.status = EPISODE_STATUS.COMPLETED;

  store.episodes.push(newEpisode);
  saveEpisodes(store);

  return { original: episode, newEpisode };
}

/**
 * List episodes with optional pagination and status filter
 * @param {object} [opts]
 * @param {string} [opts.status] - 'active' | 'completed'
 * @param {number} [opts.limit] - Default 20
 * @param {number} [opts.offset] - Default 0
 * @returns {{ episodes: object[], total: number }}
 */
export function listEpisodes(opts = {}) {
  const { status, limit = 20, offset = 0 } = opts;
  const store = getStore();

  let episodes = store.episodes;
  if (status) {
    episodes = episodes.filter(e => e.status === status);
  }

  // Sort by started_at desc (most recent first)
  episodes.sort((a, b) => new Date(b.started_at) - new Date(a.started_at));

  return {
    episodes: episodes.slice(offset, offset + limit),
    total: episodes.length,
  };
}

/**
 * Delete an episode by ID
 * @param {string} id
 * @returns {boolean}
 */
export function deleteEpisode(id) {
  const store = getStore();
  const idx = store.episodes.findIndex(e => e.id === id);
  if (idx === -1) return false;
  store.episodes.splice(idx, 1);
  saveEpisodes(store);
  return true;
}

/**
 * Merge two episodes into one
 * @param {string} id1
 * @param {string} id2
 * @returns {object|null} Merged episode or null on failure
 */
export function mergeEpisodes(id1, id2) {
  const store = getStore();
  const ep1 = store.episodes.find(e => e.id === id1);
  const ep2 = store.episodes.find(e => e.id === id2);
  if (!ep1 || !ep2) return null;

  // Merge: ep1 survives, ep2's memory_ids and entities merged in
  const mergedMemoryIds = [...new Set([...ep1.memory_ids, ...ep2.memory_ids])];
  const mergedEntities = [...new Set([...ep1.entities, ...ep2.entities])];
  const now = new Date().toISOString();

  ep1.ended_at = now;
  ep1.status = EPISODE_STATUS.COMPLETED;
  ep1.memory_ids = mergedMemoryIds;
  ep1.entities = mergedEntities;
  ep1.last_refresh = now;

  // Remove ep2
  store.episodes = store.episodes.filter(e => e.id !== id2);
  saveEpisodes(store);
  return ep1;
}

// recallEpisodeAsync: full context including associated memories
export async function recallEpisodeAsync(id) {
  const episode = getEpisode(id);
  if (!episode) return null;

  let memories = [];
  try {
    const { getAllMemories: getM } = await import('../storage.js');
    const all = getM();
    memories = all.filter(m => episode.memory_ids.includes(m.id));
  } catch {
    memories = [];
  }

  return { episode, memories };
}

// recallEpisode: sync version (no memory lookup)
export function recallEpisode(id) {
  return getEpisode(id);
}

export { EPISODE_STATUS, DEFAULT_MAX_TURNS };
export default {
  createEpisode,
  endEpisode,
  updateEpisode,
  getActiveEpisode,
  getEpisode,
  autoSplitEpisode,
  listEpisodes,
  deleteEpisode,
  mergeEpisodes,
  recallEpisode,
  recallEpisodeAsync,
  EPISODE_STATUS,
  DEFAULT_MAX_TURNS,
};
