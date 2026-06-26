/**
 * Episode Auto-Capture - Automatic episode boundary detection
 *
 * Hooks into the conversation flow to automatically:
 * 1. Detect when to start a new episode (session boundary)
 * 2. Group memory_store calls within a time window into the same episode
 * 3. Create episode boundaries based on time gaps or message count
 *
 * Two modes:
 * A) Intercept memory_store calls - group stores within 5min into one episode
 * B) Hook into conversation flow - every N messages or N minutes = episode boundary
 *
 * Usage:
 *   import { EpisodeCapture } from './episode_capture.js';
 *   const capture = new EpisodeCapture({ sessionId: 'user123', autoCapture: true });
 *   capture.captureMessage('user', 'hello');
 *   capture.captureMessage('assistant', 'hi there');
 */

import { startEpisode, addMessage, completeEpisode } from './episode_manager.js';
import { EPISODE_STATUS } from './episode_store.js';

const DEFAULT_GAP_MS = 5 * 60 * 1000;      // 5 minute gap → new episode
const DEFAULT_MAX_MESSAGES = 100;           // force new episode after N messages
const DEFAULT_AUTO_COMPLETE_MS = 30 * 60 * 1000; // auto-complete after 30 min inactivity

/**
 * EpisodeCapture - auto-capture conversation messages into episodes
 */
export class EpisodeCapture {
  /**
   * @param {object} opts
   * @param {string} [opts.sessionId='default']
   * @param {string[]} [opts.participants=[]]
   * @param {number} [opts.episodeGapMs=300000] - 5min gap triggers new episode
   * @param {number} [opts.maxMessages=100]
   * @param {boolean} [opts.autoCapture=false] - if true, auto-capture all messages
   * @param {number} [opts.autoCompleteAfterMs=1800000] - auto-complete after 30min idle
   */
  constructor(opts = {}) {
    this.sessionId = opts.sessionId || 'default';
    this.participants = opts.participants || [];
    this.episodeGapMs = opts.episodeGapMs || DEFAULT_GAP_MS;
    this.maxMessages = opts.maxMessages || DEFAULT_MAX_MESSAGES;
    this.autoCompleteAfterMs = opts.autoCompleteAfterMs || DEFAULT_AUTO_COMPLETE_MS;

    this._currentEpisode = null;
    this._messageCount = 0;
    this._lastMessageTs = 0;
    this._lastActivityTs = Date.now();
    this._autoCompleteTimer = null;
    this._enabled = opts.autoCapture || false;

    // Store call interceptor: tracks recent stores for batching
    this._recentStores = [];
    this._storeCleanupTimer = null;
  }

  // ─── Message Capture ─────────────────────────────────────────────────────

  /**
   * Capture a single message in the current episode
   * @param {string} role - 'user'|'assistant'|'system'
   * @param {string} content
   * @param {string} [messageId]
   * @returns {Promise<object>|null} result or null if skipped
   */
  async captureMessage(role, content, messageId = null) {
    if (!this._enabled) return null;

    const now = Date.now();

    // Check if we need to start/complete episode
    await this._checkBoundary(now);

    // Ensure we have an active episode
    if (!this._currentEpisode) {
      this._currentEpisode = startEpisode(this.sessionId, this.participants);
    }

    // Add message
    const result = await addMessage(
      this.sessionId,
      role,
      content,
      messageId,
      {
        episodeGapMs: this.episodeGapMs,
        maxMessages: this.maxMessages,
        participant: this.participants[0] || 'default',
      }
    );

    this._messageCount++;
    this._lastMessageTs = now;
    this._lastActivityTs = now;
    this._resetAutoComplete();

    return result;
  }

  /**
   * Check if we need to start/complete based on boundaries
   * @param {number} now
   */
  async _checkBoundary(now) {
    // Gap threshold: if last message was too long ago, complete old episode
    if (this._currentEpisode && this._lastMessageTs > 0) {
      const gap = now - this._lastMessageTs;
      if (gap > this.episodeGapMs && this._messageCount > 0) {
        await this._completeCurrent();
        return;
      }
    }

    // Max messages: force complete
    if (this._currentEpisode && this._messageCount >= this.maxMessages) {
      await this._completeCurrent();
      return;
    }
  }

  /**
   * Complete the current episode
   */
  async _completeCurrent() {
    if (!this._currentEpisode) return;
    try {
      await completeEpisode(this._currentEpisode.id);
    } catch (err) {
      console.warn('[EpisodeCapture] complete failed:', err.message);
    }
    this._currentEpisode = null;
    this._messageCount = 0;
    this._clearAutoComplete();
  }

  // ─── Auto-Complete Timer ───────────────────────────────────────────────────

  _resetAutoComplete() {
    this._clearAutoComplete();
    if (this.autoCompleteAfterMs > 0) {
      this._autoCompleteTimer = setTimeout(
        () => this._onAutoComplete(),
        this.autoCompleteAfterMs
      );
    }
  }

  _clearAutoComplete() {
    if (this._autoCompleteTimer) {
      clearTimeout(this._autoCompleteTimer);
      this._autoCompleteTimer = null;
    }
  }

  async _onAutoComplete() {
    if (this._currentEpisode && this._messageCount > 0) {
      console.log(`[EpisodeCapture] Auto-completing episode ${this._currentEpisode.id} after ${this.autoCompleteAfterMs}ms inactivity`);
      await this._completeCurrent();
    }
  }

  // ─── Memory Store Interceptor ─────────────────────────────────────────────

  /**
   * Intercept a memory_store call to group related stores into an episode.
   * If multiple stores happen within episodeGapMs from same user, group them.
   *
   * Call this BEFORE each memory_store operation:
   *   await capture.interceptStore({ userId: 'u1', text: 'memory content' });
   *
   * @param {object} storeData - { userId, text, category, ... }
   * @returns {Promise<object>} - { grouped: boolean, episodeId: string|null }
   */
  async interceptStore(storeData) {
    const now = Date.now();
    const userId = storeData.userId || 'default';
    const key = `store:${this.sessionId}:${userId}`;

    // Clean up old store records (> gap threshold)
    this._recentStores = this._recentStores.filter(s => now - s.ts < this.episodeGapMs);

    // Check if this store is part of a burst
    const recentForUser = this._recentStores.filter(s => s.userId === userId);

    let grouped = false;
    let episodeId = this._currentEpisode?.id || null;

    if (recentForUser.length > 0) {
      // Part of a burst - will be linked to same episode
      grouped = true;
    } else {
      // First store in potential new burst
      grouped = false;
    }

    // Record this store
    this._recentStores.push({
      userId,
      text: storeData.text?.slice(0, 50) || '',
      ts: now,
      data: storeData,
    });

    // Ensure we have an episode for this session
    if (!this._currentEpisode) {
      this._currentEpisode = startEpisode(this.sessionId, [userId]);
      episodeId = this._currentEpisode.id;
    }

    // Update tracker
    this._lastActivityTs = now;
    this._resetAutoComplete();

    return { grouped, episodeId, burstSize: recentForUser.length + 1 };
  }

  /**
   * After storing a memory, call this to link it to the current episode
   * @param {string} memoryId
   */
  linkMemory(memoryId) {
    if (this._currentEpisode && memoryId) {
      const { linkMemoriesToEpisode } = require('./episode_store.js');
      try {
        linkMemoriesToEpisode(this._currentEpisode.id, [memoryId]);
      } catch (err) {
        console.warn('[EpisodeCapture] linkMemory failed:', err.message);
      }
    }
  }

  // ─── Session Control ───────────────────────────────────────────────────────

  /**
   * Manually start an episode (overrides auto-start)
   * @param {string} [sessionId]
   * @param {string[]} [participants]
   */
  start(sessionId, participants = []) {
    this.sessionId = sessionId || this.sessionId;
    this.participants = participants;
    this._currentEpisode = startEpisode(this.sessionId, this.participants);
    this._messageCount = 0;
    this._lastMessageTs = Date.now();
    this._lastActivityTs = Date.now();
    this._resetAutoComplete();
    return this._currentEpisode;
  }

  /**
   * Manually complete the current episode
   * @returns {Promise<object|null>}
   */
  async complete() {
    await this._completeCurrent();
    return null;
  }

  /**
   * Get current episode info
   * @returns {object|null}
   */
  getCurrentEpisode() {
    return this._currentEpisode;
  }

  /**
   * Enable/disable auto-capture
   * @param {boolean} enabled
   */
  setEnabled(enabled) {
    this._enabled = enabled;
    if (!enabled) {
      this._clearAutoComplete();
    }
  }

  /**
   * Cleanup resources
   */
  destroy() {
    this._clearAutoComplete();
    this._currentEpisode = null;
    this._recentStores = [];
  }
}

// ─── Global capture registry ───────────────────────────────────────────────────

/** @type {Map<string, EpisodeCapture>} */
const captures = new Map();

/**
 * Get or create a capture instance for a session
 * @param {string} sessionId
 * @param {object} [opts]
 * @returns {EpisodeCapture}
 */
export function getCapture(sessionId, opts = {}) {
  if (!captures.has(sessionId)) {
    captures.set(sessionId, new EpisodeCapture({ sessionId, ...opts }));
  }
  return captures.get(sessionId);
}

/**
 * Remove a capture instance
 * @param {string} sessionId
 */
export function removeCapture(sessionId) {
  const cap = captures.get(sessionId);
  if (cap) {
    cap.destroy();
    captures.delete(sessionId);
  }
}

export default { EpisodeCapture, getCapture, removeCapture };
