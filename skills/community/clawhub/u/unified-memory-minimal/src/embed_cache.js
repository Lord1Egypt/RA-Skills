/**
 * Embedding Cache - LRU cache with TTL
 * SHA-256 hash key, 256 entries, 30min TTL
 */
import crypto from 'crypto';

const DEFAULT_MAX_SIZE = 256;
const DEFAULT_TTL_MS = 30 * 60 * 1000; // 30 minutes

class EmbedCache {
  constructor(maxSize = DEFAULT_MAX_SIZE, ttlMs = DEFAULT_TTL_MS) {
    this.maxSize = maxSize;
    this.ttlMs = ttlMs;
    /** @type {Map<string, {embedding: number[], timestamp: number, text: string}>} */
    this.cache = new Map();
  }

  _hash(text) {
    return crypto.createHash('sha256').update(text).digest('base64');
  }

  _isExpired(entry) {
    return Date.now() - entry.timestamp > this.ttlMs;
  }

  get(text) {
    const key = this._hash(text);
    const entry = this.cache.get(key);
    if (!entry) return null;
    if (this._isExpired(entry)) {
      this.cache.delete(key);
      return null;
    }
    // Move to end (most recently used)
    this.cache.delete(key);
    this.cache.set(key, entry);
    return entry.embedding;
  }

  set(text, embedding) {
    const key = this._hash(text);
    if (this.cache.has(key)) this.cache.delete(key);
    if (this.cache.size >= this.maxSize) {
      // Delete oldest (first) entry
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(key, { embedding, timestamp: Date.now(), text });
  }

  has(text) {
    return this.get(text) !== null;
  }

  clear() { this.cache.clear(); }

  get stats() {
    const now = Date.now();
    let expired = 0;
    for (const e of this.cache.values()) {
      if (now - e.timestamp > this.ttlMs) expired++;
    }
    return { size: this.cache.size, maxSize: this.maxSize, expired };
  }
}

// Singleton
export const embedCache = new EmbedCache();
export { EmbedCache };
export default embedCache;
