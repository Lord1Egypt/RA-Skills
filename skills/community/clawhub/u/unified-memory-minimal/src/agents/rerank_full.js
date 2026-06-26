/**
 * Rerank Full - Complete reranking implementation
 * Integrates with search to rerank results
 */

import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { getAllMemories } from '../storage.js';


const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');

/**
 * Default rerank config
 */
const DEFAULT_CONFIG = {
  useModel: false,
  modelWeights: { original: 0.3, cross: 0.7 },
  topK: 10,
};

/**
 * Load memories
 */

/**
 * Simple text scoring for reranking
 */
function textScore(query, text) {
  const queryWords = new Set(query.toLowerCase().split(/\W+/).filter(w => w.length > 2));
  const textWords = new Set(text.toLowerCase().split(/\W+/));
  
  if (queryWords.size === 0) return 0;
  
  // Jaccard similarity
  let intersection = 0;
  for (const word of queryWords) {
    if (textWords.has(word)) intersection++;
  }
  const union = queryWords.size + textWords.size - intersection;
  const jaccard = union > 0 ? intersection / union : 0;
  
  // Position score (earlier is better)
  const textLower = text.toLowerCase();
  const queryLower = query.toLowerCase();
  let positionScore = 0;
  
  const firstMatch = textLower.indexOf(queryLower);
  if (firstMatch === 0) positionScore = 1;
  else if (firstMatch > 0) positionScore = 1 / (firstMatch + 1);
  
  // Length penalty (prefer medium length)
  const textLen = text.length;
  let lengthScore = 1;
  if (textLen < 20) lengthScore = 0.5;
  else if (textLen > 500) lengthScore = 0.8;
  
  return (jaccard * 0.5 + positionScore * 0.3 + lengthScore * 0.2);
}

/**
 * Rerank results using the configured method
 */
export function rerank(query, results, config) {
  const cfg = { ...DEFAULT_CONFIG, ...config };
  
  if (results.length === 0) return [];
  
  // Score each result
  const scored = results.map(result => {
    // Original score
    const originalScore = result.score || result.hybrid_score || 0.5;
    
    // Text matching score
    const crossScore = textScore(query, result.text || '');
    
    // Combine scores based on config
    let finalScore;
    
    if (cfg.useModel) {
      // Would use real model here
      finalScore = originalScore * cfg.modelWeights.original + 
                   crossScore * cfg.modelWeights.cross;
    } else {
      // Fallback scoring
      finalScore = originalScore * 0.4 + crossScore * 0.6;
    }
    
    return {
      ...result,
      original_score: originalScore,
      cross_score: crossScore,
      final_score: finalScore,
    };
  });
  
  // Sort by final score
  scored.sort((a, b) => (b.final_score || 0) - (a.final_score || 0));
  
  // Return top K
  return scored.slice(0, cfg.topK);
}

/**
 * Search and rerank
 */
export function searchAndRerank(query, options = {}) {
  const memories = getAllMemories();
  const q = query.toLowerCase();
  
  // Initial search
  let results = memories.filter(m =>
    (m.text && m.text.toLowerCase().includes(q)) ||
    (m.category && m.category.toLowerCase().includes(q)) ||
    (m.tags && m.tags.some(t => t.toLowerCase().includes(q)))
  );
  
  // Score by importance and add to results
  results = results.map(r => ({
    ...r,
    score: (r.importance || 0.5) * 0.5,
  }));
  
  // Rerank if requested
  if (options.rerank !== false) {
    results = rerank(query, results, { topK: options.limit || 10 });
  }
  
  return results.slice(0, options.limit || 10);
}

/**
 * Print rerank analysis
 */
export function printRerankAnalysis(query) {
  const results = searchAndRerank(query, { limit: 10, rerank: true });
  
  console.log('\n🔄 Rerank Analysis\n');
  console.log(`  Query: "${query}"`);
  console.log(`  Results: ${results.length}\n`);
  
  console.log('  Results (original -> final):');
  for (const r of results.slice(0, 5)) {
    const orig = ((r.original_score || 0)).toFixed(3);
    const cross = ((r.cross_score || 0)).toFixed(3);
    const final = ((r.final_score || 0)).toFixed(3);
    console.log(`    ${(r.text || '').substring(0, 40)}...`);
    console.log(`      Original: ${orig} | Cross: ${cross} | Final: ${final}`);
  }
  
  console.log('');
}

// CLI
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args[0] === 'search' && args[1]) {
    printRerankAnalysis(args.slice(1).join(' '));
  } else {
    printRerankAnalysis('example query');
  }
}
