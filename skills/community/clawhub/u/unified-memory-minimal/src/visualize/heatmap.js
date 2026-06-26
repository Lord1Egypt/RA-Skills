/**
 * Heatmap Generator
 */

import { readFileSync, writeSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { getAllMemories } from '../storage.js';


const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const HEATMAP_DIR = join(MEMORY_DIR, 'heatmaps');

export function calculateHeatmap() {
  const memories = getAllMemories();
  const entries = memories.map(mem => {
    const accessCount = mem.access_count || 0;
    const importance = mem.importance || 0.5;
    const heatScore = accessCount * importance;
    return { id: mem.id || 'unknown', text: (mem.text || '').substring(0, 50), category: mem.category || 'general', accessCount, importance, heatScore };
  });
  entries.sort((a, b) => b.heatScore - a.heatScore);
  return { generatedAt: new Date().toISOString(), entries, totalMemories: memories.length, hottestMemories: entries.slice(0, 10) };
}

export function generateAsciiHeatmap(heatmap) {
  const data = heatmap || calculateHeatmap();
  const lines = [];
  lines.push('🔥 Memory Access Heatmap\n');
  lines.push(`Generated: ${data.generatedAt}\n`);
  lines.push(`Total Memories: ${data.totalMemories}\n`);
  lines.push('─'.repeat(60));
  lines.push('');
  for (let i = 0; i < Math.min(data.entries.length, 20); i++) {
    const entry = data.entries[i];
    const barLen = Math.min(Math.floor(entry.heatScore * 2), 30);
    const bar = '█'.repeat(barLen) + '░'.repeat(30 - barLen);
    lines.push(`[${(i + 1).toString().padStart(2)}] ${bar} ${entry.heatScore.toFixed(1)}`);
    lines.push(`      ${entry.text}...`);
    lines.push('');
  }
  return lines.join('\n');
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args[0] === 'save') {
    mkdirSync(HEATMAP_DIR, { recursive: true });
    const heatmap = calculateHeatmap();
    const file = join(HEATMAP_DIR, `heatmap_${Date.now()}.json`);
    writeSync(file, JSON.stringify(heatmap, null, 2), 'utf-8');
    console.log(`💾 Saved: ${file}`);
  } else {
    console.log(generateAsciiHeatmap());
  }
}
