/**
 * memory_dedup - 记忆去重检测
 * 检测相似记忆并可选合并
 */

import { getAllMemories, saveMemories } from '../storage.js';
import { simpleHash, levenshteinDistance } from '../utils/text.js';

export async function dedupMemories({ threshold = 0.85, dryRun = true }) {
  const memories = await getAllMemories();
  
  if (memories.length < 2) {
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({ message: '记忆少于2条，无需去重', count: memories.length }, null, 2)
      }]
    };
  }
  
  // Build hash index for quick candidate lookup
  const hashIndex = new Map();
  const duplicates = [];
  
  for (const mem of memories) {
    const hash = simpleHash(mem.text);
    if (!hashIndex.has(hash)) {
      hashIndex.set(hash, []);
    }
    hashIndex.get(hash).push(mem);
  }
  
  // Find duplicates via hash + Levenshtein
  const checked = new Set();
  
  for (const [hash, candidates] of hashIndex) {
    if (candidates.length > 1) {
      // Exact duplicates
      for (let i = 1; i < candidates.length; i++) {
        duplicates.push({
          type: 'exact',
          original: candidates[0],
          duplicate: candidates[i],
          similarity: 1.0
        });
        checked.add(candidates[i].id);
      }
    }
  }
  
  // Fuzzy matches (only if few exact dupes)
  if (duplicates.length < 3) {
    for (let i = 0; i < memories.length; i++) {
      for (let j = i + 1; j < memories.length; j++) {
        if (checked.has(memories[i].id) && checked.has(memories[j].id)) continue;
        
        const dist = levenshteinDistance(memories[i].text, memories[j].text);
        const maxLen = Math.max(memories[i].text.length, memories[j].text.length);
        const similarity = maxLen === 0 ? 0 : 1 - dist / maxLen;
        
        if (similarity >= threshold) {
          duplicates.push({
            type: 'fuzzy',
            original: memories[i],
            duplicate: memories[j],
            similarity: Math.round(similarity * 1000) / 1000
          });
          checked.add(memories[j].id);
        }
      }
    }
  }
  
  // Apply if not dry run
  if (!dryRun && duplicates.length > 0) {
    const idsToRemove = new Set(duplicates.map(d => d.duplicate.id));
    const kept = memories.filter(m => !idsToRemove.has(m.id));
    saveMemories(kept);
  }
  
  return {
    content: [{
      type: 'text',
      text: JSON.stringify({
        total_memories: memories.length,
        duplicates_found: duplicates.length,
        duplicates,
        action: dryRun ? 'dry_run' : 'applied'
      }, null, 2)
    }]
  };
}
