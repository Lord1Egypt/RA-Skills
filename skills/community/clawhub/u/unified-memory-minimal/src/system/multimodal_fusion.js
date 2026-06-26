/**
 * Multimodal Fusion - Combine multiple memory sources
 */

import { readFileSync, existsSync } from 'fs';
import { join } from 'path';

const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');

function loadUnifiedMemories() {
  const file = join(MEMORY_DIR, 'memories.json');
  if (!existsSync(file)) return [];
  try { return JSON.parse(readFileSync(file, 'utf-8')); }
  catch { return []; }
}

export function fuseMemories(config = {}) {
  const memories = loadUnifiedMemories();
  const seen = new Set();
  const result = [];
  
  for (const mem of memories) {
    if (!seen.has(mem.id)) {
      seen.add(mem.id);
      result.push(mem);
    }
  }
  return result;
}

export function getFusionStats() {
  const memories = loadUnifiedMemories();
  const idSet = new Set();
  let duplicates = 0;
  
  for (const mem of memories) {
    if (idSet.has(mem.id)) duplicates++;
    else idSet.add(mem.id);
  }
  
  return { totalMemories: memories.length, duplicates };
}

export function printFusionReport() {
  const stats = getFusionStats();
  console.log('\n🔗 Multimodal Fusion Report\n');
  console.log(`  Total Memories: ${stats.totalMemories}`);
  console.log(`  Duplicates: ${stats.duplicates}`);
  console.log('');
}

if (require.main === module) { printFusionReport(); }
