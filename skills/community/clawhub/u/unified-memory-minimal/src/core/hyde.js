/**
 * HyDE (Hypothetical Document Embeddings)
 */

import { readFileSync, existsSync } from 'fs';
import { join } from 'path';

const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');

export function generateHypotheticalAnswer(query, config) {
  const cfg = { maxHypotheticalLength: 200, ...config };
  const words = query.split(/\s+/).filter(w => w.length > 2);
  let hypothetical = `Based on "${query}", relevant information includes: `;
  if (words.length > 0) hypothetical += words.slice(0, 3).map(w => `concept of ${w}`).join(', ') + '. ';
  hypothetical += 'Key points include specific details and actionable insights.';
  if (hypothetical.length > cfg.maxHypotheticalLength) hypothetical = hypothetical.substring(0, cfg.maxHypotheticalLength) + '...';
  return hypothetical;
}

export function extractTopics(hypothetical) {
  const stopWords = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are'];
  const words = hypothetical.toLowerCase().split(/\W+/).filter(w => w.length > 3 && !stopWords.includes(w));
  const counts = {};
  for (const word of words) counts[word] = (counts[word] || 0) + 1;
  return Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([word]) => word);
}

export function hydeSearch(query, memories, topK = 5) {
  const hypothetical = generateHypotheticalAnswer(query);
  const topics = extractTopics(hypothetical);
  
  const scored = memories.map(mem => {
    let score = 0;
    const text = (mem.text || '').toLowerCase();
    for (const topic of topics) { if (text.includes(topic)) score += 1; }
    if (text.includes(query.toLowerCase())) score += 2;
    score += (mem.importance || 0.5) * 0.5;
    return { memory: mem, score };
  });
  
  return scored.filter(s => s.score > 0).sort((a, b) => b.score - a.score).slice(0, topK).map(s => s.memory);
}

export function printHyDEAnalysis(query) {
  const file = join(MEMORY_DIR, 'memories.json');
  let memories = [];
  if (existsSync(file)) { try { memories = JSON.parse(readFileSync(file, 'utf-8')); } catch {} }
  
  const hypothetical = generateHypotheticalAnswer(query);
  const topics = extractTopics(hypothetical);
  const results = hydeSearch(query, memories, 5);
  
  console.log('\n🔍 HyDE Analysis\n');
  console.log(`  Query: "${query}"\n`);
  console.log(`  Hypothetical Answer:\n  ${hypothetical.substring(0, 100)}...\n`);
  console.log(`  Extracted Topics: ${topics.join(', ')}`);
  console.log(`  Matching Memories: ${results.length}`);
  console.log('');
}

if (require.main === module) {
  const args = process.argv.slice(2);
  printHyDEAnalysis(args.slice(1).join(' ') || 'example query');
}
