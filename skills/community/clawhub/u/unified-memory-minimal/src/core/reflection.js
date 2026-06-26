/**
 * Memory Reflection - Periodically review and consolidate memories
 */

import { readFileSync, existsSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { getAllMemories } from '../storage.js';


const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');

export function reflect(memory) {
  const insights = [];
  const text = memory.text || '';
  if (text.includes('喜欢') || text.includes('prefer')) insights.push('Expressed preference');
  if (text.includes('决定') || text.includes('decided')) insights.push('Made a decision');
  if (text.includes('项目') || text.includes('project')) insights.push('Related to project');
  
  const reflectionCount = memory.reflection_count || 0;
  let action = 'keep';
  if (reflectionCount >= 5 && (memory.importance || 0.5) < 0.3) action = 'archive';
  
  return { memoryId: memory.id || 'unknown', insights, action };
}

export function runReflectionCycle() {
  const memories = getAllMemories();
  for (const mem of memories) {
    mem.reflection_count = (mem.reflection_count || 0) + 1;
    mem.last_reflected = new Date().toISOString();
  }
  writeFileSync(join(MEMORY_DIR, 'memories.json'), JSON.stringify(memories, null, 2), 'utf-8');
  
  const results = memories.map(reflect);
  let archived = 0;
  for (const r of results) { if (r.action === 'archive') archived++; }
  
  console.log(`🪞 Reflection complete: ${memories.length} reflected, ${archived} archived`);
  return { totalReflected: memories.length, archived };
}

export function printReflectionReport() {
  const memories = getAllMemories();
  const results = memories.slice(0, 5).map(reflect);
  console.log('\n🪞 Memory Reflection Report\n');
  console.log(`  Total Memories: ${memories.length}`);
  for (const r of results.slice(0, 3)) console.log(`    [${r.memoryId}] ${r.insights.join(', ') || 'No insights'}`);
  console.log('');
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args[0] === 'run') runReflectionCycle();
  else printReflectionReport();
}
