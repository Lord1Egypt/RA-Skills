/**
 * Incremental Learning - Continuously update embeddings
 */

import { readFileSync, existsSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');

export function generateEmbedding(text, dim = 384) {
  const vector = new Array(dim).fill(0);
  const textLower = text.toLowerCase();
  for (let i = 0; i < textLower.length; i++) {
    const charCode = textLower.charCodeAt(i);
    const idx = (charCode * (i + 1)) % dim;
    vector[idx] += charCode / 255;
  }
  const magnitude = Math.sqrt(vector.reduce((sum, v) => sum + v * v, 0));
  if (magnitude > 0) { for (let i = 0; i < dim; i++) vector[i] /= magnitude; }
  return vector;
}

export function cosineSimilarity(a, b) {
  if (a.length !== b.length) return 0;
  let dotProduct = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) { dotProduct += a[i] * b[i]; normA += a[i] * a[i]; normB += b[i] * b[i]; }
  const denominator = Math.sqrt(normA) * Math.sqrt(normB);
  return denominator > 0 ? dotProduct / denominator : 0;
}

export function incrementalUpdate(options = {}) {
  const file = join(MEMORY_DIR, 'memories.json');
  if (!existsSync(file)) return { processed: 0, updated: 0 };
  let memories;
  try { memories = JSON.parse(readFileSync(file, 'utf-8')); }
  catch { return { processed: 0, updated: 0 }; }
  
  const batchSize = options.batchSize || 10;
  let processed = 0, updated = 0;
  
  for (const mem of memories) {
    if (processed >= batchSize) break;
    if (!mem.embedding || options.forceUpdate) {
      mem.embedding = generateEmbedding(mem.text || '');
      mem.last_updated = new Date().toISOString();
      updated++;
    }
    processed++;
  }
  
  if (updated > 0) { mkdirSync(MEMORY_DIR, { recursive: true }); writeFileSync(file, JSON.stringify(memories, null, 2), 'utf-8'); }
  return { processed, updated };
}

export function updateAllEmbeddings() {
  const file = join(MEMORY_DIR, 'memories.json');
  if (!existsSync(file)) return { totalMemories: 0, embeddingsUpdated: 0, lastUpdate: new Date().toISOString() };
  let memories;
  try { memories = JSON.parse(readFileSync(file, 'utf-8')); }
  catch { return { totalMemories: 0, embeddingsUpdated: 0, lastUpdate: new Date().toISOString() }; }
  
  let updated = 0;
  for (const mem of memories) {
    if (!mem.embedding) { mem.embedding = generateEmbedding(mem.text || ''); mem.last_updated = new Date().toISOString(); updated++; }
  }
  writeFileSync(file, JSON.stringify(memories, null, 2), 'utf-8');
  return { totalMemories: memories.length, embeddingsUpdated: updated, lastUpdate: new Date().toISOString() };
}

export function printLearningStats() {
  const file = join(MEMORY_DIR, 'memories.json');
  let memories = [];
  if (existsSync(file)) { try { memories = JSON.parse(readFileSync(file, 'utf-8')); } catch {} }
  const withEmbeddings = memories.filter(m => m.embedding).length;
  console.log('\n📈 Incremental Learning Stats\n');
  console.log(`  Total Memories: ${memories.length}`);
  console.log(`  With Embeddings: ${withEmbeddings}`);
  console.log(`  Without Embeddings: ${memories.length - withEmbeddings}`);
  console.log('');
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args[0] === 'update') { const result = incrementalUpdate({ batchSize: parseInt(args[1] || '10', 10) }); console.log(`📊 Processed ${result.processed}, Updated ${result.updated}`); }
  else if (args[0] === 'update-all') { const stats = updateAllEmbeddings(); console.log(`📊 Total: ${stats.totalMemories}, Updated: ${stats.embeddingsUpdated}`); }
  else printLearningStats();
}
