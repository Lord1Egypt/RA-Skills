/**
 * Knowledge Merger - 知识合并器 v7.0
 * 
 * Features:
 * - Detect similar/duplicate memories
 * - Merge into Knowledge Blocks
 * - Reduce memory redundancy
 * - Improve retrieval efficiency
 * 
 * Usage:
 *   node knowledge_merger.js scan                    # 扫描相似记忆
 *   node knowledge_merger.js merge --threshold 0.9   # 合并高相似记忆
 *   node knowledge_merger.js stats                   # 统计合并效果
 *   node knowledge_merger.js preview <group-id>     # 预览合并结果
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import os from 'os';
import http from 'http';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ========== Configuration ==========

const WORKSPACE = path.join(os.homedir(), '.openclaw', 'workspace');
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const VECTOR_DB_DIR = path.join(WORKSPACE, 'memory', 'vector');
const MERGED_DIR = path.join(MEMORY_DIR, 'knowledge_blocks');

const OLLAMA_URL = process.env.OLLAMA_HOST || 'http://localhost:11434';
const OLLAMA_EMBED_MODEL = process.env.OLLAMA_EMBED_MODEL || 'nomic-embed-text:latest';
const OLLAMA_LLM_MODEL = process.env.OLLAMA_LLM_MODEL || 'deepseek-v3.2:cloud';

const SIMILARITY_THRESHOLD = 0.85;
const MIN_GROUP_SIZE = 2;
const MAX_GROUP_SIZE = 10;

const SIMILARITY_CACHE_FILE = path.join(MERGED_DIR, 'similarity_cache.json');
const MERGE_HISTORY_FILE = path.join(MERGED_DIR, 'merge_history.json');
const KNOWLEDGE_BLOCKS_FILE = path.join(MERGED_DIR, 'knowledge_blocks.json');

// Ensure directories exist
await fs.mkdir(MERGED_DIR, { recursive: true });

// ========== Ollama Integration ==========

async function getEmbedding(text) {
  try {
    const result = await new Promise((resolve, reject) => {
      const req = http.request(
        `${OLLAMA_URL}/api/embeddings`,
        { method: 'POST', timeout: 30000 },
        (res) => {
          let data = '';
          res.on('data', chunk => data += chunk);
          res.on('end', () => {
            try { resolve(JSON.parse(data)); }
            catch { reject(new Error('Invalid JSON')); }
          });
        }
      );
      req.on('error', reject);
      req.write(JSON.stringify({ model: OLLAMA_EMBED_MODEL, prompt: text }));
      req.end();
    });
    return result.embedding || null;
  } catch (e) {
    console.warn(`⚠️ Embedding 失败: ${e.message}`);
    return null;
  }
}

async function callLLM(prompt, temperature = 0.3) {
  try {
    const result = await new Promise((resolve, reject) => {
      const req = http.request(
        `${OLLAMA_URL}/api/generate`,
        { method: 'POST', timeout: 60000 },
        (res) => {
          let data = '';
          res.on('data', chunk => data += chunk);
          res.on('end', () => {
            try { resolve(JSON.parse(data)); }
            catch { reject(new Error('Invalid JSON')); }
          });
        }
      );
      req.on('error', reject);
      req.write(JSON.stringify({
        model: OLLAMA_LLM_MODEL,
        prompt,
        stream: false,
        options: { temperature }
      }));
      req.end();
    });
    return result.response || null;
  } catch (e) {
    console.warn(`⚠️ LLM 失败: ${e.message}`);
    return null;
  }
}

function cosineSimilarity(vec1, vec2) {
  if (!vec1 || !vec2 || vec1.length !== vec2.length) return 0.0;
  
  let dotProduct = 0;
  let norm1 = 0;
  let norm2 = 0;
  
  for (let i = 0; i < vec1.length; i++) {
    dotProduct += vec1[i] * vec2[i];
    norm1 += vec1[i] * vec1[i];
    norm2 += vec2[i] * vec2[i];
  }
  
  const d1 = Math.sqrt(norm1);
  const d2 = Math.sqrt(norm2);
  
  if (d1 === 0 || d2 === 0) return 0.0;
  return dotProduct / (d1 * d2);
}

// ========== Knowledge Merger ==========

class KnowledgeMerger {
  constructor() {
    this.similarityCache = {};
    this.mergeHistory = [];
    this.knowledgeBlocks = {};
    this._load();
  }
  
  async _load() {
    try {
      if (await fileExists(SIMILARITY_CACHE_FILE)) {
        this.similarityCache = JSON.parse(await fs.readFile(SIMILARITY_CACHE_FILE, 'utf-8'));
      }
      if (await fileExists(MERGE_HISTORY_FILE)) {
        this.mergeHistory = JSON.parse(await fs.readFile(MERGE_HISTORY_FILE, 'utf-8'));
      }
      if (await fileExists(KNOWLEDGE_BLOCKS_FILE)) {
        this.knowledgeBlocks = JSON.parse(await fs.readFile(KNOWLEDGE_BLOCKS_FILE, 'utf-8'));
      }
    } catch (e) {
      console.warn(`⚠️ 加载缓存失败: ${e.message}`);
    }
  }
  
  async _save() {
    try {
      await fs.writeFile(SIMILARITY_CACHE_FILE, JSON.stringify(this.similarityCache), 'utf-8');
      await fs.writeFile(MERGE_HISTORY_FILE, JSON.stringify(this.mergeHistory), 'utf-8');
      await fs.writeFile(KNOWLEDGE_BLOCKS_FILE, JSON.stringify(this.knowledgeBlocks), 'utf-8');
    } catch (e) {
      console.warn(`⚠️ 保存缓存失败: ${e.message}`);
    }
  }
  
  async loadMemories() {
    const memories = [];
    const files = (await fs.readdir(MEMORY_DIR)).filter(f => f.endsWith('.md'));
    
    for (const file of files) {
      const content = await fs.readFile(path.join(MEMORY_DIR, file), 'utf-8');
      const lines = content.split('\n');
      
      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || !trimmed.startsWith('-')) continue;
        
        const match = trimmed.match(/^- \[([^\]]+)\] \[([^\]]+)\] \[([^\]]+)\](?: \[I=([^\]]+)\])? (.+)$/);
        if (match) {
          const [, timestamp, category, scope, impStr, text] = match;
          memories.push({
            id: `${file}_${timestamp}_${memories.length}`,
            text,
            timestamp,
            category,
            scope,
            importance: impStr ? parseFloat(impStr) : 0.5
          });
        }
      }
    }
    
    return memories;
  }
  
  async computeSimilarity(mem1, mem2) {
    const key = `${mem1.id}::${mem2.id}`;
    
    if (key in this.similarityCache) {
      return this.similarityCache[key];
    }
    
    // Try to get embeddings
    const emb1 = await getEmbedding(mem1.text);
    const emb2 = await getEmbedding(mem2.text);
    
    let similarity = 0.0;
    
    if (emb1 && emb2) {
      similarity = cosineSimilarity(emb1, emb2);
    } else {
      // Fallback to text similarity
      similarity = this._textSimilarity(mem1.text, mem2.text);
    }
    
    this.similarityCache[key] = similarity;
    return similarity;
  }
  
  _textSimilarity(text1, text2) {
    // Simple Jaccard similarity
    const words1 = new Set(text1.toLowerCase().split(/\s+/));
    const words2 = new Set(text2.toLowerCase().split(/\s+/));
    
    const intersection = new Set([...words1].filter(x => words2.has(x)));
    const union = new Set([...words1, ...words2]);
    
    return intersection.size / union.size;
  }
  
  async findSimilarGroups(memories, threshold = SIMILARITY_THRESHOLD) {
    const groups = [];
    const used = new Set();
    
    for (let i = 0; i < memories.length; i++) {
      if (used.has(memories[i].id)) continue;
      
      const group = [memories[i]];
      used.add(memories[i].id);
      
      for (let j = i + 1; j < memories.length && group.length < MAX_GROUP_SIZE; j++) {
        if (used.has(memories[j].id)) continue;
        
        const similarity = await this.computeSimilarity(memories[i], memories[j]);
        if (similarity >= threshold) {
          group.push(memories[j]);
          used.add(memories[j].id);
        }
      }
      
      if (group.length >= MIN_GROUP_SIZE) {
        groups.push({
          id: `group_${groups.length}`,
          members: group,
          avg_similarity: await this._calcGroupSimilarity(group),
          representative: group[0]
        });
      }
    }
    
    return groups;
  }
  
  async _calcGroupSimilarity(group) {
    if (group.length < 2) return 1.0;
    
    let total = 0;
    let count = 0;
    
    for (let i = 0; i < group.length; i++) {
      for (let j = i + 1; j < group.length; j++) {
        const sim = await this.computeSimilarity(group[i], group[j]);
        total += sim;
        count++;
      }
    }
    
    return count > 0 ? total / count : 0;
  }
  
  async mergeGroup(group) {
    if (!group || group.members.length < 2) return null;
    
    // Use LLM to generate merged content
    const texts = group.members.map(m => `- ${m.text}`).join('\n');
    const prompt = `以下是对同一主题的多条记忆，请合并为一条简洁的摘要：

${texts}

请生成合并后的摘要，保持核心信息，去除重复。回复格式：
{
  "summary": "合并后的摘要",
  "key_points": ["要点1", "要点2"],
  "category": "最合适的分类"
}`;
    
    let summary = texts; // Default fallback
    let keyPoints = [];
    let category = 'merged';
    
    const response = await callLLM(prompt, 0.3);
    if (response) {
      try {
        const parsed = JSON.parse(response);
        summary = parsed.summary || summary;
        keyPoints = parsed.key_points || [];
        category = parsed.category || category;
      } catch {
        // Use first 100 chars as summary
        summary = summary.slice(0, 100);
      }
    }
    
    const block = {
      id: `kb_${Date.now()}`,
      summary,
      key_points: keyPoints,
      category,
      source_memories: group.members.map(m => m.id),
      merged_at: new Date().toISOString(),
      importance: Math.max(...group.members.map(m => m.importance))
    };
    
    this.knowledgeBlocks[block.id] = block;
    this.mergeHistory.push({
      block_id: block.id,
      merged_at: block.merged_at,
      member_count: group.members.length
    });
    
    await this._save();
    return block;
  }
  
  async mergeAll(memories, threshold = SIMILARITY_THRESHOLD) {
    console.log('🔍 扫描相似记忆...');
    const groups = await this.findSimilarGroups(memories, threshold);
    console.log(`📦 发现 ${groups.length} 个相似组`);
    
    const blocks = [];
    for (const group of groups) {
      const block = await this.mergeGroup(group);
      if (block) blocks.push(block);
      console.log(`✅ 合并组 ${group.id}: ${block?.summary?.slice(0, 50)}...`);
    }
    
    return blocks;
  }
  
  getStats() {
    return {
      total_blocks: Object.keys(this.knowledgeBlocks).length,
      merge_history_count: this.mergeHistory.length,
      similarity_cache_entries: Object.keys(this.similarityCache).length,
      last_merge: this.mergeHistory[this.mergeHistory.length - 1]?.merged_at || null
    };
  }
  
  getBlocks() {
    return Object.values(this.knowledgeBlocks);
  }
  
  async previewBlock(blockId) {
    const block = this.knowledgeBlocks[blockId];
    if (!block) return null;
    
    return {
      id: block.id,
      summary: block.summary,
      key_points: block.key_points,
      category: block.category,
      source_memories: block.source_memories,
      merged_at: block.merged_at,
      importance: block.importance
    };
  }
}

// ========== Utilities ==========

async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

// ========== CLI ==========

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command) {
    console.log(`
Knowledge Merger - 知识合并器 v7.0

Usage:
    node knowledge_merger.js scan                    # 扫描相似记忆
    node knowledge_merger.js merge --threshold 0.9   # 合并高相似记忆
    node knowledge_merger.js stats                   # 统计合并效果
    node knowledge_merger.js preview <block-id>    # 预览合并结果
`);
    process.exit(1);
  }
  
  console.log('🚀 Knowledge Merger v7.0...\n');
  
  const merger = new KnowledgeMerger();
  
  switch (command) {
    case 'scan': {
      const thresholdIdx = args.indexOf('--threshold');
      const threshold = thresholdIdx !== -1 ? parseFloat(args[thresholdIdx + 1]) : SIMILARITY_THRESHOLD;
      
      const memories = await merger.loadMemories();
      console.log(`📚 加载 ${memories.length} 条记忆\n`);
      
      const groups = await merger.findSimilarGroups(memories, threshold);
      console.log(`📦 发现 ${groups.length} 个相似组:\n`);
      
      for (const group of groups) {
        console.log(`组 ${group.id}: ${group.members.length} 条记忆`);
        console.log(`  代表: ${group.representative.text.slice(0, 60)}...`);
        console.log(`  平均相似度: ${(group.avg_similarity * 100).toFixed(1)}%`);
        console.log();
      }
      break;
    }
    
    case 'merge': {
      const thresholdIdx = args.indexOf('--threshold');
      const threshold = thresholdIdx !== -1 ? parseFloat(args[thresholdIdx + 1]) : SIMILARITY_THRESHOLD;
      
      const memories = await merger.loadMemories();
      console.log(`📚 加载 ${memories.length} 条记忆\n`);
      
      const blocks = await merger.mergeAll(memories, threshold);
      console.log(`\n✅ 合并完成，生成 ${blocks.length} 个知识块`);
      break;
    }
    
    case 'stats': {
      const stats = merger.getStats();
      console.log('📊 统计:\n');
      console.log(`  知识块总数: ${stats.total_blocks}`);
      console.log(`  合并历史: ${stats.merge_history_count}`);
      console.log(`  相似度缓存: ${stats.similarity_cache_entries} 条`);
      console.log(`  最后合并: ${stats.last_merge || '无'}`);
      
      console.log('\n📦 知识块:\n');
      const blocks = merger.getBlocks();
      for (const block of blocks.slice(0, 10)) {
        console.log(`  [${block.id}] ${block.summary.slice(0, 50)}...`);
      }
      break;
    }
    
    case 'preview': {
      const blockId = args[1];
      if (!blockId) {
        console.log('❌ 请提供 block-id');
        process.exit(1);
      }
      
      const preview = await merger.previewBlock(blockId);
      if (!preview) {
        console.log(`❌ 知识块不存在: ${blockId}`);
        process.exit(1);
      }
      
      console.log(`📋 知识块: ${preview.id}\n`);
      console.log(`摘要: ${preview.summary}`);
      console.log(`分类: ${preview.category}`);
      console.log(`重要性: ${preview.importance.toFixed(2)}`);
      console.log(`来源: ${preview.source_memories.length} 条记忆`);
      console.log(`合并时间: ${preview.merged_at}`);
      if (preview.key_points.length > 0) {
        console.log('\n要点:');
        for (const point of preview.key_points) {
          console.log(`  - ${point}`);
        }
      }
      break;
    }
    
    default:
      console.log(`❌ 未知命令: ${command}`);
      process.exit(1);
  }
}

// Run if executed directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch(console.error);
}

export { KnowledgeMerger };

export default KnowledgeMerger;
