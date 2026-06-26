/**
 * Memory Usage Stats
 */

import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { getAllMemories } from '../storage.js';


const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');

export function generateStats() {
  const memories = getAllMemories();
  const byCategory = {}, byImportance = { high: 0, medium: 0, low: 0 };
  const tagCounts = {};
  let totalImportance = 0, totalConfidence = 0;
  
  for (const mem of memories) {
    byCategory[mem.category || 'general'] = (byCategory[mem.category || 'general'] || 0) + 1;
    const imp = mem.importance || 0.5;
    if (imp >= 0.7) byImportance.high++;
    else if (imp >= 0.4) byImportance.medium++;
    else byImportance.low++;
    totalImportance += imp;
    totalConfidence += mem.confidence || 0.8;
    if (Array.isArray(mem.tags)) {
      for (const tag of mem.tags) tagCounts[tag] = (tagCounts[tag] || 0) + 1;
    }
  }
  
  const topTags = Object.entries(tagCounts).sort((a, b) => b[1] - a[1]).slice(0, 10);
  const total = memories.length;
  
  return {
    total, byCategory, byImportance,
    avgImportance: total > 0 ? (totalImportance / total).toFixed(2) : 0,
    avgConfidence: total > 0 ? (totalConfidence / total).toFixed(2) : 0,
    topTags,
  };
}

export function printUsageStats() {
  const stats = generateStats();
  console.log('\n📊 Memory Usage Statistics\n');
  console.log(`  Total Memories: ${stats.total}`);
  console.log(`  Avg Importance: ${stats.avgImportance}`);
  console.log(`  Avg Confidence: ${stats.avgConfidence}\n`);
  console.log('  By Category:');
  for (const [cat, count] of Object.entries(stats.byCategory)) console.log(`    ${cat}: ${count}`);
  console.log('');
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args[0] === 'json') console.log(JSON.stringify(generateStats(), null, 2));
  else printUsageStats();
}
