/**
 * Proactive Memory Manager v1.0
 * Unified management of proactive recall and proactive care
 * Periodic checks, active injection
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { getAllMemories } from './storage.js';
import { predictRecall } from './core/proactive_recall.js';
import { runCheck as runProactiveCare } from './core/proactive_care.js';
import { autoDegrade } from './quality.js';
import { runLifecycle, autoMigrateTiers } from './tier.js';
import { saveMemories } from './storage.js';

const LIFECYCLE_STATE_FILE = join(process.env.HOME || '/root', '.unified-memory', 'lifecycle_state.json');
const DAILY_MIGRATION_INTERVAL_MS = 24 * 60 * 60 * 1000; // 24 hours

function loadOperationCount() {
  try {
    if (existsSync(LIFECYCLE_STATE_FILE)) {
      const data = JSON.parse(readFileSync(LIFECYCLE_STATE_FILE, 'utf8'));
      return {
        count: typeof data.operationCount === 'number' ? data.operationCount : 0,
        lastDailyMigration: data.lastDailyMigration || 0,
      };
    }
  } catch { /* ignore */ }
  return { count: 0, lastDailyMigration: 0 };
}

function saveOperationCount(count, lastDailyMigration) {
  try {
    const dir = join(process.env.HOME || '/root', '.unified-memory');
    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
    }
    writeFileSync(LIFECYCLE_STATE_FILE, JSON.stringify({ operationCount: count, lastDailyMigration }, null, 2), 'utf8');
  } catch (e) {
    console.error('[ProactiveManager] failed to persist state:', e.message);
  }
}

export class ProactiveManager {
  constructor(intervalMs = 300000) { // Default 5 minutes
    this.intervalMs = intervalMs;
    this.timer = null;
    this.lastRecallResults = [];
    this.lastCareResults = null;
    const state = loadOperationCount();
    this.operationCount = state.count;
    this.lastDailyMigration = state.lastDailyMigration;
  }

  start() {
    if (this.timer) return;
    this.timer = setInterval(() => this.tick(), this.intervalMs);
    console.log(`[ProactiveManager] started, interval=${this.intervalMs}ms`);
  }

  stop() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }

  async tick() {
    try {
      // 1. Run proactive care (status detection)
      this.lastCareResults = await runProactiveCare();

      // 2. Predict memories that need recall
      const recent = this._getRecentContext();
      this.lastRecallResults = predictRecall(recent);

      // 3. Auto-degrade low-quality memories to COLD tier
      this.lastDegradeResult = autoDegrade({ threshold: 0.15, batchSize: 50 });

      // 4. Lifecycle: every 100 operations, run lifecycle management
      this.operationCount++;
      if (this.operationCount % 100 === 0) {
        console.log(`[ProactiveManager] operationCount=${this.operationCount}, triggering lifecycle...`);
        this.lastLifecycleResult = runLifecycle();
        saveOperationCount(this.operationCount, this.lastDailyMigration);
      }

      // 5. Daily tier migration: check every tick if 24h has passed
      const now = Date.now();
      if (now - this.lastDailyMigration >= DAILY_MIGRATION_INTERVAL_MS) {
        console.log('[ProactiveManager] Running daily tier migration...');
        try {
          const memories = getAllMemories();
          const result = autoMigrateTiers(memories, { dryRun: false });
          if (result.changes.length > 0) {
            saveMemories(result.memories);
            console.log(`[ProactiveManager] Tier migration: ${result.changes.length} memories moved`);
          }
          this.lastDailyMigration = now;
          this.lastMigrationResult = result;
          saveOperationCount(this.operationCount, this.lastDailyMigration);
        } catch (e) {
          console.error('[ProactiveManager] Daily migration error:', e.message);
        }
      }

      return {
        care: this.lastCareResults,
        recall: this.lastRecallResults.slice(0, 5),
        degrade: this.lastDegradeResult,
        lifecycle: this.lastLifecycleResult || null,
        migration: this.lastMigrationResult || null,
        ts: Date.now(),
      };
    } catch (e) {
      console.error('[ProactiveManager] tick error:', e.message);
    }
  }

  _getRecentContext() {
    // Extract context from recent memories
    const memories = getAllMemories();
    const recent = memories
      .sort((a, b) => (b.updated_at || 0) - (a.updated_at || 0))
      .slice(0, 10)
      .map(m => m.text)
      .join(' ');
    return recent;
  }

  getStatus() {
    return {
      running: !!this.timer,
      intervalMs: this.intervalMs,
      lastCare: this.lastCareResults,
      lastRecallCount: this.lastRecallResults.length,
      recallPredictions: this.lastRecallResults.slice(0, 3),
      lastDegrade: this.lastDegradeResult || null,
      lastMigrationCount: this.lastMigrationResult?.changes?.length || 0,
      lastMigrationTs: this.lastMigrationResult ? Date.now() : null,
    };
  }

  // Manual trigger once
  async trigger() {
    return this.tick();
  }
}

// Global instance
let globalManager = null;

export function getProactiveManager() {
  if (!globalManager) {
    globalManager = new ProactiveManager();
  }
  return globalManager;
}
