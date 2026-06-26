/**
 * memory_search - BM25 + Vector hybrid search CLI
 * CLI wrapper around the core search functionality
 */

import { hybridSearch } from '../fusion.js';
import { getAllMemories, touchMemory } from '../storage.js';
import { parseArgs } from 'util';

export async function cmdSearch(args) {
  const query = args.query || args._[0] || '';
  const topK = args.topK || args.k || 5;
  const mode = args.mode || 'hybrid';
  
  if (!query) {
    console.log('Usage: memory search <query> [--mode hybrid|bm25|vector] [--top-k 5]');
    return;
  }
  
  try {
    const results = await hybridSearch(query, topK, mode);
    
    // Update access stats
    for (const r of results) {
      touchMemory(r.memory.id);
    }
    
    if (results.length === 0) {
      console.log('🔍 未找到相关记忆');
      return;
    }
    
    console.log(`📊 找到 ${results.length} 条相关记忆:\n`);
    
    for (let i = 0; i < results.length; i++) {
      const r = results[i];
      const score = Math.round(r.fusionScore * 1000) / 1000;
      console.log(`[${i + 1}] ${r.memory.text.slice(0, 80)}...`);
      console.log(`    分类: ${r.memory.category} | 重要性: ${r.memory.importance} | 匹配度: ${score}`);
      if (r.highlight) {
        console.log(`    高亮: ${r.highlight.slice(0, 60)}...`);
      }
      console.log();
    }
  } catch (err) {
    console.error(`❌ 搜索失败: ${err.message}`);
  }
}
