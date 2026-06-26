/**
 * memory.js 鈥?瀹欎竴鏈湴璁板繂寮曟搸
 *
 * 鍙栬嚜鎸佺画璁板繂鏈嶅姟灏佽鎶€鑳界殑鏍稿績寮曟搸銆? * 淇濈暀浜嗗叏閮ㄨ兘鍔涳細璇箟妫€绱€侀噸瑕佹€у姞鏉冦€佹椂闂磋“鍑忋€佸帇缂┿€佽嚜鍔ㄦ窐姹般€? *
 * 涓庡皝瑁呯増鐨勬牳蹇冨尯鍒細
 *   - 娌℃湁浜嗙綉缁?鏀粯/澶氱鎴? *   - 瀛樺偍鍒版湰鍦?JSON 鏂囦欢
 *   - 涓撲负瀹欎竴宸ヤ綔鍖鸿璁? */

import { randomUUID } from 'node:crypto';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DEFAULT_STORE_PATH = join(__dirname, 'MEMORY_STORE.json');

export class MemorySystem {
  #memories = [];
  #config;
  #dirty = false;
  #storePath;

  constructor(config = {}) {
    this.#storePath = config.storePath || DEFAULT_STORE_PATH;
    this.#config = {
      decayRate: 7200,
      simWeight: 0.6,
      recencyWeight: 0.4,
      maxMemories: 1000,
      defaultImportance: 1.0,
      ...config,
    };
    this.#load();
  }

  // ---- 鍐?----

  add(content, importance, metadata = {}) {
    if (!content || typeof content !== 'string') throw new Error('Content must be non-empty string');
    const trimmed = content.trim();
    if (trimmed.length < 1 || trimmed.length > 5000) throw new Error('Content must be between 1 and 5000 characters');

    const item = {
      id: randomUUID(),
      content: trimmed,
      timestamp: Date.now(),
      importance: importance ?? this.#config.defaultImportance,
      metadata,
    };
    this.#memories.push(item);
    this.#dirty = true;
    this.#autoCleanup();
    this.#save();
    return item;
  }

  // ---- 鎵归噺鍐欏叆 ----
  addBatch(items) {
    const results = [];
    for (const { content, importance, metadata } of items) {
      results.push(this.add(content, importance, metadata));
    }
    return results;
  }

  // ---- 妫€绱?----

  retrieve(query, k = 5, minImportance = 0, maxAgeSeconds) {
    if (!query || typeof query !== 'string') return [];
    const now = Date.now();
    const scored = [];

    for (const mem of this.#memories) {
      if (mem.importance < minImportance) continue;
      if (maxAgeSeconds && (now - mem.timestamp) / 1000 > maxAgeSeconds) continue;

      const sim = contentSimilarity(query, mem.content);
      const rec = recencyScore(mem.timestamp, now, this.#config.decayRate);
      const score = this.#config.simWeight * sim + this.#config.recencyWeight * rec;
      scored.push({ score, item: { ...mem } }); // shallow copy to avoid mutation
    }

    scored.sort((a, b) => b.score - a.score);
    return scored.slice(0, k).map(s => ({
      ...s.item,
      _score: Math.round(s.score * 10000) / 10000,
    }));
  }

  // ---- 鏈€杩戣蹇?----

  getRecent(n = 10, minImportance = 0) {
    const filtered = this.#memories.filter(m => m.importance >= minImportance);
    filtered.sort((a, b) => b.timestamp - a.timestamp);
    return filtered.slice(0, n).map(m => ({ ...m }));
  }

  // ---- 鍒犻櫎 ----

  remove(predicate) {
    const before = this.#memories.length;
    this.#memories = this.#memories.filter(m => !predicate(m));
    if (this.#memories.length !== before) {
      this.#dirty = true;
      this.#save();
    }
    return before - this.#memories.length;
  }

  clear() {
    this.#memories = [];
    this.#dirty = true;
    this.#save();
  }

  // ---- 缁熻 ----

  get count() { return this.#memories.length; }

  get config() { return { ...this.#config }; }

  // ---- 娓呯悊 ----

  cleanup(maxAgeSeconds, minImportance = 0, maxItems) {
    const before = this.#memories.length;
    const now = Date.now();

    this.#memories = this.#memories.filter(m => {
      if (maxAgeSeconds && (now - m.timestamp) / 1000 > maxAgeSeconds) return false;
      if (m.importance < minImportance) return false;
      return true;
    });

    if (maxItems && this.#memories.length > maxItems) {
      this.#cleanupKeepBest(maxItems);
    }

    if (this.#memories.length !== before) {
      this.#dirty = true;
      this.#save();
    }
    return before - this.#memories.length;
  }

  // ---- 鍘嬬缉 ----

  compact(groupSize = 5, minImportance = 0.5) {
    if (groupSize <= 1) return 0;
    const originalCount = this.#memories.length;

    const sorted = [...this.#memories].sort((a, b) => a.timestamp - b.timestamp);
    const newMems = [];

    for (let i = 0; i < sorted.length; ) {
      const group = [];
      let j = i;
      while (j < sorted.length && (j - i) < groupSize) {
        if (sorted[j].importance >= minImportance) {
          group.push(sorted[j]);
        }
        j++;
      }

      if (group.length >= 2) {
        const contents = group.map(m => m.content);
        const summaryText = `[Summary of ${group.length} items: ${contents.map(t => t.length > 60 ? t.slice(0, 57) + '...' : t).join('; ')}]`;
        const avgImp = group.reduce((s, m) => s + m.importance, 0) / group.length;
        const newestTs = Math.max(...group.map(m => m.timestamp));

        newMems.push({
          id: randomUUID(),
          content: summaryText,
          timestamp: newestTs,
          importance: avgImp,
          metadata: { compacted: true, originalCount: group.length },
        });
      } else {
        newMems.push(...group);
      }
      i = j;
    }

    this.#memories = newMems;
    this.#autoCleanup();
    this.#dirty = true;
    this.#save();
    return originalCount - this.#memories.length;
  }

  // ---- 搴忓垪鍖?----

  toJSON() {
    return {
      version: 3,
      updatedAt: Date.now(),
      config: { ...this.#config },
      memories: this.#memories.map(m => ({ ...m })),
    };
  }

  fromJSON(data) {
    if (data.config) this.#config = { ...this.#config, ...data.config };
    if (data.memories) this.#memories = data.memories.map(m => ({ ...m }));
  }

  // ---- 绉佹湁 ----

  #load() {
    try {
      if (existsSync(this.#storePath)) {
        const raw = readFileSync(this.#storePath, 'utf-8');
        const data = JSON.parse(raw);
        this.fromJSON(data);
        console.error(`[memory] Loaded ${this.#memories.length} memories from ${this.#storePath}`);
      } else {
        console.error(`[memory] No store file found, starting fresh`);
      }
    } catch (err) {
      console.error(`[memory] Error loading store: ${err.message}`);
    }
  }

  #save() {
    if (!this.#dirty) return;
    try {
      writeFileSync(this.#storePath, JSON.stringify(this.toJSON(), null, 2), 'utf-8');
      this.#dirty = false;
    } catch (err) {
      console.error(`[memory] Error saving store: ${err.message}`);
    }
  }

  #autoCleanup() {
    if (this.#config.maxMemories && this.#memories.length > this.#config.maxMemories) {
      this.#cleanupKeepBest(this.#config.maxMemories);
    }
  }

  #cleanupKeepBest(maxItems) {
    if (maxItems <= 0) { this.#memories = []; return; }
    const now = Date.now();
    const scored = this.#memories.map(m => ({
      score: recencyScore(m.timestamp, now, this.#config.decayRate) * m.importance,
      item: m,
    }));
    scored.sort((a, b) => b.score - a.score);
    this.#memories = scored.slice(0, maxItems).map(s => s.item);
  }
}

// ---- 鐙珛宸ュ叿鍑芥暟 ----

export function contentSimilarity(text1, text2) {
  if (!text1 || !text2) return 0;
  const a = text1.toLowerCase();
  const b = text2.toLowerCase();

  const setA = new Set(a);
  const setB = new Set(b);
  const intersection = new Set([...setA].filter(c => setB.has(c)));
  const union = new Set([...setA, ...setB]);

  const bigramsA = getBigrams(a);
  const bigramsB = getBigrams(b);
  const biIntersection = bigramsA.filter(bg => bigramsB.includes(bg)).length;
  const biUnion = new Set([...bigramsA, ...bigramsB]).size;

  const charSim = union.size > 0 ? intersection.size / union.size : 0;
  const biSim = biUnion > 0 ? biIntersection / biUnion : 0;

  return 0.4 * charSim + 0.6 * biSim;
}

function getBigrams(s) {
  const result = [];
  for (let i = 0; i < s.length - 1; i++) result.push(s.slice(i, i + 2));
  return result;
}

export function recencyScore(timestamp, now, decayRate) {
  const delta = (now - timestamp) / 1000;
  if (delta <= 0) return 1;
  return Math.exp(-delta / decayRate);
}

