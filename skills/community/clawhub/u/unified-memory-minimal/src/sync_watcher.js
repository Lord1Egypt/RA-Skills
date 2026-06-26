/**
 * sync_watcher.js - File System Watcher for Memory Sync
 * 
 * Watches ~/.openclaw/workspace/memory/memories.json for changes
 * and triggers sync events with debouncing.
 * 
 * Events emitted:
 *   - sync:triggered  { type: 'add'|'change'|'unlink', timestamp, stats }
 *   - sync:conflict   { conflicts, timestamp }
 *   - sync:completed  { synced_peers, timestamp, duration_ms }
 *   - watcher:error   { error }
 */

import { watch } from 'fs';
import { existsSync, readFileSync, statSync } from 'fs';
import { join } from 'path';
import EventEmitter from 'events';
import { getAllMemories } from './storage.js';

const HOME = process.env.HOME || '/root';
const MEMORY_DIR = join(HOME, '.openclaw/workspace/memory');
const MEMORIES_FILE = join(MEMORY_DIR, 'memories.json');

const DEBOUNCE_MS = 2000;
const HEALTH_CHECK_INTERVAL_MS = 30000;

class SyncWatcher extends EventEmitter {
  constructor() {
    super();
    this.watcher = null;
    this.debounceTimer = null;
    this.isRunning = false;
    this.lastStats = null;
    this.healthInterval = null;
    this._computeInitialStats();
  }

  _computeInitialStats() {
    try {
      if (existsSync(MEMORIES_FILE)) {
        const stat = statSync(MEMORIES_FILE);
        const content = readFileSync(MEMORIES_FILE, 'utf-8');
        const mems = JSON.parse(content);
        const arr = Array.isArray(mems) ? mems : (mems.memories || []);
        this.lastStats = {
          mtime: stat.mtimeMs,
          size: stat.size,
          memoryCount: arr.length,
          checksum: simpleChecksum(content)
        };
      }
    } catch { this.lastStats = null; }
  }

  _currentStats() {
    try {
      if (!existsSync(MEMORIES_FILE)) return null;
      const stat = statSync(MEMORIES_FILE);
      const content = readFileSync(MEMORIES_FILE, 'utf-8');
      const mems = JSON.parse(content);
      const arr = Array.isArray(mems) ? mems : (mems.memories || []);
      return {
        mtime: stat.mtimeMs,
        size: stat.size,
        memoryCount: arr.length,
        checksum: simpleChecksum(content)
      };
    } catch { return null; }
  }

  _changed() {
    const curr = this._currentStats();
    if (!curr || !this.lastStats) return { changed: true, type: 'init' };
    if (curr.checksum !== this.lastStats.checksum) {
      if (!this.lastStats) return { changed: true, type: 'init' };
      if (curr.memoryCount > this.lastStats.memoryCount) return { changed: true, type: 'add' };
      if (curr.memoryCount < this.lastStats.memoryCount) return { changed: true, type: 'unlink' };
      return { changed: true, type: 'change' };
    }
    return { changed: false };
  }

  _debouncedTrigger(eventType) {
    if (this.debounceTimer) {
      clearTimeout(this.debounceTimer);
    }
    this.debounceTimer = setTimeout(() => {
      this.debounceTimer = null;
      this._doTrigger(eventType);
    }, DEBOUNCE_MS);
  }

  _doTrigger(eventType) {
    const stats = this._currentStats();
    const change = this._changed();
    this.lastStats = stats;
    this.emit('sync:triggered', {
      type: change.type || eventType,
      timestamp: new Date().toISOString(),
      stats: {
        memoryCount: stats?.memoryCount || 0,
        size: stats?.size || 0
      }
    });
  }

  start() {
    if (this.isRunning) return;
    if (!existsSync(MEMORIES_FILE)) {
      this.emit('watcher:error', { error: `Memory file not found: ${MEMORIES_FILE}` });
      return;
    }

    this.isRunning = true;
    this._computeInitialStats();

    try {
      this.watcher = watch(MEMORIES_FILE, (eventType) => {
        if (eventType === 'change' || eventType === 'rename') {
          this._debouncedTrigger(eventType);
        }
      });
    } catch (err) {
      this.emit('watcher:error', { error: err.message });
      return;
    }

    this.healthInterval = setInterval(() => {
      if (!existsSync(MEMORIES_FILE) && this.isRunning) {
        this.emit('watcher:error', { error: 'Memory file deleted or moved' });
        this.stop();
      }
    }, HEALTH_CHECK_INTERVAL_MS);
  }

  stop() {
    if (this.debounceTimer) {
      clearTimeout(this.debounceTimer);
      this.debounceTimer = null;
    }
    if (this.healthInterval) {
      clearInterval(this.healthInterval);
      this.healthInterval = null;
    }
    if (this.watcher) {
      try { this.watcher.close(); } catch { /* ignore */ }
      this.watcher = null;
    }
    this.isRunning = false;
  }

  forceSync() {
    this._computeInitialStats();
    this._doTrigger('force');
  }

  getStatus() {
    return {
      running: this.isRunning,
      watching: MEMORIES_FILE,
      debounce_ms: DEBOUNCE_MS,
      last_stats: this.lastStats
    };
  }
}

function simpleChecksum(content) {
  let hash = 0;
  for (let i = 0; i < Math.min(content.length, 4096); i++) {
    hash = ((hash << 5) - hash + content.charCodeAt(i)) | 0;
  }
  return hash.toString(16);
}

// Singleton instance
let _watcherInstance = null;

export function getSyncWatcher() {
  if (!_watcherInstance) {
    _watcherInstance = new SyncWatcher();
  }
  return _watcherInstance;
}

export function startSyncWatcher() {
  const watcher = getSyncWatcher();
  watcher.start();
  return watcher;
}

export function stopSyncWatcher() {
  if (_watcherInstance) {
    _watcherInstance.stop();
  }
}

export { SyncWatcher };
export default { getSyncWatcher, startSyncWatcher, stopSyncWatcher, SyncWatcher };
