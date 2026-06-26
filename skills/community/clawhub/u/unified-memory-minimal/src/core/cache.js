/**
 * cache.js - 多级缓存系统
 * Ported from Python memory_cache.py
 * 
 * LRU 内存缓存 + 可选的 SQLite 持久缓存
 */

import { createHash } from 'crypto';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const CACHE_DIR = join(HOME, '.openclaw/workspace/memory/cache');

function ensureCacheDir() {
  if (!existsSync(CACHE_DIR)) {
    mkdirSync(CACHE_DIR, { recursive: true });
  }
}

function makeKey(query, topK = 10) {
  const raw = `${query}:${topK}`;
  return createHash('md5').update(raw).digest('hex');
}

/**
 * LRU 内存缓存
 */
export class LRUCache {
  constructor(maxSize = 1000, ttlSeconds = 3600) {
    this.maxSize = maxSize;
    this.ttl = ttlSeconds * 1000; // ms
    this.cache = new Map(); // key -> { value, timestamp }
  }

  _isExpired(entry) {
    return Date.now() - entry.timestamp > this.ttl;
  }

  get(query, topK = 10) {
    const key = makeKey(query, topK);
    const entry = this.cache.get(key);
    
    if (!entry) return null;
    
    if (this._isExpired(entry)) {
      this.cache.delete(key);
      return null;
    }
    
    // Move to end (most recently used)
    this.cache.delete(key);
    this.cache.set(key, entry);
    
    return entry.value;
  }

  set(query, results, topK = 10) {
    const key = makeKey(query, topK);
    
    // Remove if exists
    if (this.cache.has(key)) {
      this.cache.delete(key);
    }
    
    // Add to end
    this.cache.set(key, { value: results, timestamp: Date.now() });
    
    // Evict oldest if over max size
    if (this.cache.size > this.maxSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
  }

  clear() {
    this.cache.clear();
  }

  stats() {
    const now = Date.now();
    let expired = 0;
    let valid = 0;
    
    for (const entry of this.cache.values()) {
      if (this._isExpired(entry)) expired++;
      else valid++;
    }
    
    return {
      size: this.cache.size,
      maxSize: this.maxSize,
      valid,
      expired,
      ttlSeconds: this.ttl / 1000
    };
  }
}

/**
 * 文件缓存（持久化）
 */
export class FileCache {
  constructor(cacheDir = CACHE_DIR) {
    this.cacheDir = cacheDir;
    ensureCacheDir();
  }

  _filePath(key) {
    return join(this.cacheDir, `${key}.json`);
  }

  get(query, topK = 10, maxAgeMs = 3600000) {
    const key = makeKey(query, topK);
    const file = this._filePath(key);
    
    if (!existsSync(file)) return null;
    
    try {
      const stat = { mtimeMs: 0 };
      // Check age
      const content = readFileSync(file, 'utf-8');
      const entry = JSON.parse(content);
      
      if (Date.now() - entry.timestamp > maxAgeMs) {
        return null;
      }
      
      return entry.value;
    } catch {
      return null;
    }
  }

  set(query, results, topK = 10) {
    const key = makeKey(query, topK);
    const file = this._filePath(key);
    
    try {
      writeFileSync(file, JSON.stringify({
        value: results,
        timestamp: Date.now()
      }), 'utf-8');
    } catch (err) {
      // Silently fail - cache write errors shouldn't break things
    }
  }

  clear() {
    const { readdirSync, unlinkSync } = require('fs');
    try {
      const files = readdirSync(this.cacheDir);
      for (const file of files) {
        if (file.endsWith('.json')) {
          unlinkSync(join(this.cacheDir, file));
        }
      }
    } catch { }
  }
}

/**
 * 混合缓存（LRU + File）
 */
export class HybridCache {
  constructor(lruTTL = 300, fileTTL = 3600) {
    this.lru = new LRUCache(500, lruTTL);
    this.file = new FileCache();
    this.fileTTL = fileTTL * 1000;
  }

  get(query, topK = 10) {
    // Try LRU first
    const lruResult = this.lru.get(query, topK);
    if (lruResult) return lruResult;
    
    // Try file cache
    const fileResult = this.file.get(query, topK, this.fileTTL);
    if (fileResult) {
      // Promote to LRU
      this.lru.set(query, fileResult, topK);
      return fileResult;
    }
    
    return null;
  }

  set(query, results, topK = 10) {
    this.lru.set(query, results, topK);
    this.file.set(query, results, topK);
  }

  clear() {
    this.lru.clear();
    this.file.clear();
  }

  stats() {
    return {
      lru: this.lru.stats(),
      file: { cacheDir: this.cacheDir }
    };
  }
}

// Default global cache instance
export const globalCache = new HybridCache();
