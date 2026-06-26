/**
 * Preheat System - Preload hot memories for fast retrieval
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { getAllMemories } from '../storage.js';


const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const PREHEAT_DIR = join(MEMORY_DIR, 'preheat');

export function classifyMemories(config = {}) {
  const hotThreshold = config.hotThreshold ?? 10;
  const warmThreshold = config.warmThreshold ?? 3;
  const memories = getAllMemories();
  
  const hot = [], warm = [], cold = [];
  
  for (const mem of memories) {
    const accessCount = mem.access_count || 0;
    if (accessCount >= hotThreshold) hot.push(mem);
    else if (accessCount >= warmThreshold) warm.push(mem);
    else cold.push(mem);
  }
  
  return { hot: hot.slice(0, 100), warm: warm.slice(0, 200), cold };
}

export function preheat() {
  const { hot, warm } = classifyMemories();
  const cache = { generatedAt: new Date().toISOString(), hot, warm, hotIds: hot.map(m => m.id), warmIds: warm.map(m => m.id) };
  mkdirSync(PREHEAT_DIR, { recursive: true });
  writeFileSync(join(PREHEAT_DIR, 'preheat_cache.json'), JSON.stringify(cache, null, 2), 'utf-8');
  return { hot: hot.length, warm: warm.length, total: hot.length + warm.length };
}

export function getPreheatStatus() {
  const file = join(PREHEAT_DIR, 'preheat_cache.json');
  if (!existsSync(file)) return { hotCount: 0, warmCount: 0, totalCount: 0, isStale: true };
  try {
    const cache = JSON.parse(readFileSync(file, 'utf-8'));
    return { hotCount: cache.hot.length, warmCount: cache.warm.length, totalCount: cache.hot.length + cache.warm.length, cacheAge: cache.generatedAt, isStale: false };
  } catch { return { hotCount: 0, warmCount: 0, totalCount: 0, isStale: true }; }
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args[0] === 'run') { const result = preheat(); console.log(`🔥 Preheat: ${result.hot} hot + ${result.warm} warm = ${result.total} total`); }
  else { const status = getPreheatStatus(); console.log(`🔥 Preheat: ${status.hotCount} hot, ${status.warmCount} warm`); }
}
