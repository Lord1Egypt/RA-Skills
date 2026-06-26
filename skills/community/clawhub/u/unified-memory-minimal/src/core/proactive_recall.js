/**
 * Proactive Recall - Anticipate what memories to recall
 */

import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { getAllMemories } from '../storage.js';


const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');

const CONTEXT_TRIGGERS = {
  project: ['项目', '开发', '代码', 'git', 'project', 'code'],
  meeting: ['会议', '讨论', 'meeting', 'discuss'],
  decision: ['决定', '选择', 'decided', 'choice'],
};

export function predictRecall(context) {
  const memories = getAllMemories();
  const contextLower = context.toLowerCase();
  const predictions = [];
  
  for (const mem of memories) {
    let relevance = 0;
    let reason = '';
    const textLower = (mem.text || '').toLowerCase();
    
    for (const [category, keywords] of Object.entries(CONTEXT_TRIGGERS)) {
      for (const keyword of keywords) {
        if (contextLower.includes(keyword) && textLower.includes(keyword)) {
          relevance += 2;
          reason = `Context keyword "${keyword}" matched`;
        }
      }
    }
    
    relevance += (mem.importance || 0.5) * 0.5;
    relevance += Math.log1p(mem.access_count || 0) * 0.3;
    
    if (relevance > 0) predictions.push({ memory: mem, relevance, reason });
  }
  
  predictions.sort((a, b) => b.relevance - a.relevance);
  return predictions.slice(0, 10);
}

export function printRecallReport(context) {
  const predictions = context ? predictRecall(context) : predictRecall('recent');
  console.log('\n🔔 Proactive Recall Predictions\n');
  console.log(`  Context: ${context || 'time-based'}`);
  console.log(`  Predictions: ${predictions.length}\n`);
  for (const pred of predictions.slice(0, 5)) {
    console.log(`  ${pred.relevance.toFixed(2)} - ${(pred.memory.text || '').substring(0, 50)}...`);
  }
  console.log('');
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  printRecallReport(args.slice(1).join(' ') || undefined);
}
