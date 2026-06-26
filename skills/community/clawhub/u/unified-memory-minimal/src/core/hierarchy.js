/**
 * Memory Hierarchy - L1/L2/L3 memory tiering
 */

import { readFileSync, existsSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { getAllMemories, saveMemories } from '../storage.js';


const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');

const TIERS = { L1_hot: { minAccess: 10, minImportance: 0.7 }, L2_warm: { minAccess: 3, minImportance: 0.4 }, L3_cold: { default: true } };

export function getTier(memory) {
  const accessCount = memory.access_count ?? 0;
  const importance = memory.importance ?? 0.5;
  if (accessCount >= TIERS.L1_hot.minAccess || (importance >= TIERS.L1_hot.minImportance && accessCount >= 5)) return 'L1_hot';
  if (accessCount >= TIERS.L2_warm.minAccess || importance >= TIERS.L2_warm.minImportance) return 'L2_warm';
  return 'L3_cold';
}

export function getTierStats() {
  const memories = getAllMemories();
  const stats = { L1_hot: { count: 0, totalImportance: 0, totalAccess: 0 }, L2_warm: { count: 0, totalImportance: 0, totalAccess: 0 }, L3_cold: { count: 0, totalImportance: 0, totalAccess: 0 } };
  
  for (const mem of memories) {
    const tier = getTier(mem);
    stats[tier].count++;
    stats[tier].totalImportance += mem.importance ?? 0.5;
    stats[tier].totalAccess += mem.access_count ?? 0;
  }
  
  const result = {};
  for (const tier of Object.keys(stats)) {
    const s = stats[tier];
    result[tier] = { count: s.count, avgImportance: s.count > 0 ? Math.round(s.totalImportance / s.count * 100) / 100 : 0, avgAccess: s.count > 0 ? Math.round(s.totalAccess / s.count * 10) / 10 : 0 };
  }
  return result;
}

export function printHierarchyReport() {
  const stats = getTierStats();
  const memories = getAllMemories();
  
  console.log('\n🗂️  Memory Hierarchy Report\n');
  console.log(`  Total Memories: ${memories.length}\n`);
  console.log('  🔥 L1 Hot:');
  console.log(`     Count: ${stats.L1_hot.count} | Avg Importance: ${stats.L1_hot.avgImportance}`);
  console.log('  🌡️  L2 Warm:');
  console.log(`     Count: ${stats.L2_warm.count} | Avg Importance: ${stats.L2_warm.avgImportance}`);
  console.log('  ❄️  L3 Cold:');
  console.log(`     Count: ${stats.L3_cold.count} | Avg Importance: ${stats.L3_cold.avgImportance}`);
  console.log('');
}

if (require.main === module) {
  printHierarchyReport();
}
