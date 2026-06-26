/**
 * Compression Evaluation - Evaluate memory compression effectiveness
 */

import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { getAllMemories } from '../storage.js';


const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');

function compressText(text) {
  return text.replace(/\s+/g, ' ').replace(/，/g, ',').replace(/。/g, '.').trim();
}

export function evaluateCompression(memory) {
  const original = memory.text || '';
  const originalSize = Buffer.byteLength(original, 'utf-8');
  const compressed = compressText(original);
  const compressedSize = Buffer.byteLength(compressed, 'utf-8');
  return { originalSize, compressedSize, ratio: originalSize > 0 ? compressedSize / originalSize : 1 };
}

export function evaluateAllMemories() {
  const memories = getAllMemories();
  let totalOriginal = 0, totalCompressed = 0;
  const recommendations = [];
  
  for (const mem of memories) {
    const result = evaluateCompression(mem);
    totalOriginal += result.originalSize;
    totalCompressed += result.compressedSize;
  }
  
  const avgRatio = totalOriginal > 0 ? totalCompressed / totalOriginal : 1;
  if (avgRatio > 0.95) recommendations.push('Memory text is already compact');
  else recommendations.push('Compression provides modest benefit');
  
  return { totalMemories: memories.length, avgOriginalSize: totalOriginal / memories.length, avgCompressedSize: totalCompressed / memories.length, avgRatio, recommendations };
}

if (require.main === module) {
  const report = evaluateAllMemories();
  console.log('\n📦 Compression Evaluation Report\n');
  console.log(`  Total Memories: ${report.totalMemories}`);
  console.log(`  Avg Original: ${report.avgOriginalSize.toFixed(0)} bytes`);
  console.log(`  Avg Compressed: ${report.avgCompressedSize.toFixed(0)} bytes`);
  console.log(`  Ratio: ${(report.avgRatio * 100).toFixed(1)}%`);
  console.log('');
}
