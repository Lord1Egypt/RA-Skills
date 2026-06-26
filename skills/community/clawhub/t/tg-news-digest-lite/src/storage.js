import fs from "fs-extra";
import path from "path";

export class StateManager {
  constructor(dir = "./state") {
    this.path = path.join(dir, "seen_messages.json");
  }

  /**
   * Initialize state file (create if missing) and return parsed content
   */
  async init() {
    await fs.ensureFile(this.path);
    try {
      return await fs.readJson(this.path);
    } catch (err) {
      // Corrupted or unreadable file — start fresh
      return { channels: {}, meta: { created_at: new Date().toISOString() } };
    }
  }

  /**
   * Get set of seen message hashes for a channel
   * @param {string} channel - normalized username
   * @returns {Promise<Set<string>>}
   */
  async getSeenHashes(channel) {
    const state = await this.init();
    const hashes = state.channels?.[channel] || [];
    return new Set(hashes);
  }

  /**
   * Update seen hashes for a channel with rolling window
   * @param {string} channel - normalized username
   * @param {string[]} newHashes - hashes to add
   * @param {number} maxKeep - max hashes to retain per channel (default: 100)
   */
  async updateSeenHashes(channel, newHashes, maxKeep = 100) {
    const state = await this.init();
    if (!state.channels) state.channels = {};
    
    const existing = state.channels[channel] || [];
    // Merge + deduplicate + limit size
    const merged = [...new Set([...existing, ...newHashes])];
    if (merged.length > maxKeep) {
      merged.splice(0, merged.length - maxKeep);
    }
    
    state.channels[channel] = merged;
    state.meta = state.meta || {};
    state.meta.last_updated = new Date().toISOString();
    
    await fs.outputJson(this.path, state, { spaces: 2 });
  }

  /**
   * Clear all cached hashes for a channel (e.g., on removal)
   */
  async clearChannel(channel) {
    const state = await this.init();
    if (state.channels?.[channel]) {
      delete state.channels[channel];
      await fs.outputJson(this.path, state, { spaces: 2 });
    }
  }
}