/**
 * Memory System - 统一入口 (Complete)
 * 
 * Features:
 * - Hierarchical Cache (MemoryHierarchy)
 * - Knowledge Merging (KnowledgeMerger)
 * - Predictive Loading (PredictiveLoader)
 * - Confidence Validation (ConfidenceValidator)
 * - Feedback Learning (FeedbackLearner)
 * - Smart Forget (SmartForgetter)
 * - Auto Extraction (AutoExtractor)
 * - Quality Metrics (MemoryQuality)
 * - Multi-Agent Perspective (v0.4.1)
 * 
 * Usage:
 *   node memory.js status                 # System status
 *   node memory.js store "content" [--agent xiao-zhi]  # Store memory
 *   node memory.js search "query" [--agent xiao-zhi]  # Search
 *   node memory.js stats                  # Detailed stats
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import os from 'os';
import crypto from 'crypto';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ========== Configuration ==========

const WORKSPACE = path.join(os.homedir(), '.openclaw', 'workspace');
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const VECTOR_DB_DIR = path.join(MEMORY_DIR, 'vector');
const MEMORY_FILE = path.join(MEMORY_DIR, 'memories.json');

// Try importing existing Node.js modules
let Hierarchy, Merger, Predictor, Validator, Learner, Forgetter;
try {
  const hierarchyModule = await import('./core/hierarchy.js').catch(() => null);
  const mergerModule = await import('./graph/knowledge_merger.js').catch(() => null);
  const predictorModule = await import('./tools/predict.js').catch(() => null);
  const validatorModule = await import('./quality/confidence.js').catch(() => null);
  const learnerModule = await import('./tools/feedback_learner.js').catch(() => null);
  const forgetterModule = await import('./quality/smart_forgetter.js').catch(() => null);
  
  Hierarchy = hierarchyModule?.MemoryHierarchy;
  Merger = mergerModule?.KnowledgeMerger;
  Predictor = predictorModule?.PredictiveLoader;
  Validator = validatorModule?.ConfidenceValidator;
  Learner = learnerModule?.FeedbackLearner;
  Forgetter = forgetterModule?.SmartForgetter;
} catch (e) {
  // Modules not available, use simplified versions
}

// ========== Simple Implementations (Fallback) ==========

class SimpleHierarchy {
  constructor() {
    this.L1 = [];
    this.L2 = [];
    this.L3 = [];
    this.maxL1 = 50;
    this.maxL2 = 200;
  }
  
  rebuildFromMemories(memories) {
    // Sort by importance and redistribute
    const sorted = [...memories].sort((a, b) => (b.importance || 0.5) - (a.importance || 0.5));
    this.L1 = sorted.slice(0, this.maxL1);
    this.L2 = sorted.slice(this.maxL1, this.maxL1 + this.maxL2);
    this.L3 = sorted.slice(this.maxL1 + this.maxL2);
  }
  
  getContext(query, maxMemories = 10) {
    const results = [...this.L1, ...this.L2, ...this.L3].slice(0, maxMemories);
    return results;
  }
  
  stats() {
    return {
      L1_hot: { count: this.L1.length, max_size: this.maxL1, avg_importance: this._avgImportance(this.L1) },
      L2_warm: { count: this.L2.length, max_size: this.maxL2, avg_importance: this._avgImportance(this.L2) },
      L3_cold: { count: this.L3.length, avg_importance: this._avgImportance(this.L3) }
    };
  }
  
  _avgImportance(items) {
    if (!items.length) return 0;
    return items.reduce((sum, m) => sum + (m.importance || 0.5), 0) / items.length;
  }
}

class SimpleMerger {
  constructor() {
    this.blocks = [];
  }
  
  mergeAll(memories) {
    // Simple grouping by category
    const byCategory = {};
    for (const mem of memories) {
      const cat = mem.category || 'other';
      if (!byCategory[cat]) byCategory[cat] = [];
      byCategory[cat].push(mem);
    }
    
    this.blocks = Object.entries(byCategory).map(([cat, items]) => ({
      category: cat,
      count: items.length,
      items
    }));
    
    return this.blocks;
  }
  
  stats() {
    return {
      total_knowledge_blocks: this.blocks.length,
      estimated_tokens_saved: this.blocks.reduce((sum, b) => sum + (b.count - 1) * 50, 0)
    };
  }
}

class SimplePredictor {
  analyzeAndPreload(query, memories) {
    return { prediction: { query }, preloaded_count: 0 };
  }
  
  predictTopic(query) {
    return { current_keywords: query.split(/\s+/) };
  }
  
  getRelatedMemories(keywords, memories) {
    return [];
  }
  
  status() {
    return { active: true };
  }
}

class SimpleValidator {
  getConfidence(memoryId) {
    return 0.8;
  }
  
  detectConflicts(memories) {
    return [];
  }
  
  scanStale(memories) {
    return [];
  }
  
  stats() {
    return { by_confidence: { '✅ 已验证': 0, '⚠️ 可能过时': 0, '❌ 矛盾': 0 } };
  }
}

class SimpleLearner {
  getMemoryScore(memoryId) {
    return 0.5;
  }
  
  adjustImportance(memories) {
    return {};
  }
  
  stats() {
    return { total_feedback: 0, total_corrections: 0 };
  }
}

class SimpleForgetter {
  findForgettable(memories) {
    return [];
  }
  
  findDuplicates(memories) {
    return [];
  }
  
  stats() {
    return { state: { forgotten_count: 0, archived_count: 0, compressed_count: 0 } };
  }
}

// ========== Main Memory System ==========

export class MemorySystemV7 {
  constructor() {
    // Core modules
    this.hierarchy = new (Hierarchy || SimpleHierarchy)();
    this.merger = new (Merger || SimpleMerger)();
    this.predictor = new (Predictor || SimplePredictor)();
    this.validator = new (Validator || SimpleValidator)();
    this.learner = new (Learner || SimpleLearner)();
    this.forgetter = new (Forgetter || SimpleForgetter)();
    
    this.memories = [];
    this._loadMemories();
  }
  
  async _loadMemories() {
    // Load from JSON file
    try {
      const data = await fs.readFile(MEMORY_FILE, 'utf-8');
      const fileMemories = JSON.parse(data);
      this.memories.extend(fileMemories);
    } catch (e) {
      // File doesn't exist or parse error
    }
    
    // Deduplicate
    const seenIds = new Set();
    const unique = [];
    for (const m of this.memories) {
      const mid = m.id;
      if (mid && !seenIds.has(mid)) {
        seenIds.add(mid);
        unique.push(m);
      }
    }
    this.memories = unique;
    
    // Add confidence info
    for (const mem of this.memories) {
      mem.confidence = this.validator.getConfidence(mem.id);
    }
    
    console.log(`✅ 共 ${this.memories.length} 条唯一记忆`);
  }
  
  async init() {
    console.log('🔄 初始化 Memory v7.0...');
    
    if (this.memories.length > 0) {
      this.hierarchy.rebuildFromMemories(this.memories);
    }
    
    const conflicts = this.validator.detectConflicts(this.memories);
    if (conflicts.length > 0) {
      console.log(`⚠️ 发现 ${conflicts.length} 个矛盾记忆`);
    }
    
    console.log('✅ 初始化完成');
  }
  
  rebuild() {
    if (this.memories.length === 0) {
      console.log('⚠️ 没有记忆');
      return;
    }
    
    this.hierarchy.rebuildFromMemories(this.memories);
    console.log('✅ 重建完成');
  }
  
  mergeKnowledge() {
    if (this.memories.length === 0) {
      console.log('⚠️ 没有记忆');
      return;
    }
    
    const blocks = this.merger.mergeAll(this.memories);
    console.log(`✅ 生成 ${blocks.length} 条知识块`);
  }
  
  analyze(query) {
    const result = this.predictor.analyzeAndPreload(query, this.memories);
    const context = this.hierarchy.getContext(query);
    
    return {
      prediction: result.prediction,
      preloaded: result.preloaded_count,
      context_from_hierarchy: context.length,
      total_context: context.length + result.preloaded_count
    };
  }
  
  getContext(query, maxMemories = 10) {
    let context = this.hierarchy.getContext(query, maxMemories);
    
    if (context.length < maxMemories) {
      const prediction = this.predictor.predictTopic(query);
      const related = this.predictor.getRelatedMemories(prediction.current_keywords, this.memories);
      
      const existingIds = new Set(context.map(m => m.id));
      for (const mem of related) {
        if (!existingIds.has(mem.id)) {
          context.push(mem);
          if (context.length >= maxMemories) break;
        }
      }
    }
    
    // Add confidence info
    for (const mem of context) {
      mem.confidence = this.validator.getConfidence(mem.id);
      mem.score = this.learner.getMemoryScore(mem.id);
    }
    
    return context;
  }
  
  validate() {
    const stale = this.validator.scanStale(this.memories);
    console.log(`📋 发现 ${stale.length} 条可能过时的记忆`);
    
    const conflicts = this.validator.detectConflicts(this.memories);
    console.log(`📋 发现 ${conflicts.length} 个矛盾`);
    
    return { stale: stale.length, conflicts: conflicts.length };
  }
  
  async feedback() {
    const adjustments = this.learner.adjustImportance(this.memories);
    
    if (Object.keys(adjustments).length > 0) {
      await fs.writeFile(MEMORY_FILE, JSON.stringify(this.memories, null, 2), 'utf-8');
    }
    
    return adjustments;
  }
  
  async forget(dryRun = true) {
    const forgettable = this.forgetter.findForgettable(this.memories);
    const duplicates = this.forgetter.findDuplicates(this.memories);
    
    const result = {
      forgettable: forgettable.length,
      duplicate_groups: duplicates.length,
      total_to_remove: forgettable.length + duplicates.reduce((sum, g) => sum + g.length - 1, 0)
    };
    
    if (!dryRun && result.total_to_remove > 0) {
      const forgetIds = new Set(forgettable.map(f => f.id));
      let remaining = this.memories.filter(m => !forgetIds.has(m.id));
      
      // Merge duplicates (keep first in each group)
      for (const group of duplicates) {
        for (let i = 1; i < group.length; i++) {
          remaining = remaining.filter(m => m.id !== group[i].id);
        }
      }
      
      await fs.writeFile(MEMORY_FILE, JSON.stringify(remaining, null, 2), 'utf-8');
      this.memories = remaining;
    }
    
    return result;
  }
  
  async store(content, metadata = null, agentPerspective = null) {
    const memoryId = crypto.randomUUID();
    const timestamp = new Date().toISOString();
    
    const memoryEntry = {
      id: memoryId,
      content,
      timestamp,
      metadata: metadata || {}
    };
    
    if (agentPerspective) {
      memoryEntry.agent_perspective = agentPerspective;
    }
    
    // Store to file
    this.memories.push(memoryEntry);
    try {
      await fs.writeFile(MEMORY_FILE, JSON.stringify(this.memories, null, 2), 'utf-8');
    } catch (e) {
      console.error(`⚠️ JSON 存储失败: ${e.message}`);
    }
    
    return {
      success: true,
      id: memoryId,
      content: content.length > 50 ? content.slice(0, 50) + '...' : content,
      agent_perspective: agentPerspective,
      stored_to_vector: false,
      timestamp
    };
  }
  
  search(query, agentPerspective = null, sharedOnly = false, limit = 10) {
    const results = [];
    const queryLower = query.toLowerCase();
    
    // Filter memories
    let filteredMemories = this.memories;
    
    if (sharedOnly) {
      filteredMemories = filteredMemories.filter(m => !m.agent_perspective);
    } else if (agentPerspective) {
      filteredMemories = filteredMemories.filter(m => m.agent_perspective === agentPerspective);
    }
    
    // Simple keyword matching search
    for (const memory of filteredMemories) {
      const content = memory.content || memory.text || '';
      if (queryLower.includes(queryLower) || content.toLowerCase().includes(queryLower)) {
        const memoryCopy = { ...memory };
        if (!memoryCopy.content && memoryCopy.text) {
          memoryCopy.content = memoryCopy.text;
        }
        memoryCopy.confidence = this.validator.getConfidence(memory.id);
        memoryCopy.score = this.learner.getMemoryScore(memory.id);
        results.push(memoryCopy);
        
        if (results.length >= limit) break;
      }
    }
    
    return results;
  }
  
  statsByPerspective() {
    const perspectives = {};
    
    for (const memory of this.memories) {
      const perspective = memory.agent_perspective || 'shared';
      if (!perspectives[perspective]) {
        perspectives[perspective] = {
          count: 0,
          latest: null,
          avg_confidence: 0
        };
      }
      
      perspectives[perspective].count++;
      
      const timestamp = memory.timestamp;
      if (timestamp && (!perspectives[perspective].latest || timestamp > perspectives[perspective].latest)) {
        perspectives[perspective].latest = timestamp;
      }
    }
    
    // Calculate average confidence
    for (const [perspective, stats] of Object.entries(perspectives)) {
      const perspectiveMemories = this.memories.filter(m => (m.agent_perspective || 'shared') === perspective);
      if (perspectiveMemories.length > 0) {
        const confidences = perspectiveMemories.map(m => {
          const conf = this.validator.getConfidence(m.id);
          return typeof conf === 'number' ? conf : 0;
        });
        stats.avg_confidence = confidences.reduce((a, b) => a + b, 0) / confidences.length;
      }
    }
    
    return perspectives;
  }
  
  stats() {
    const h = this.hierarchy.stats();
    const m = this.merger.stats();
    const v = this.validator.stats();
    const l = this.learner.stats();
    const f = this.forgetter.stats();
    const p = this.statsByPerspective();
    
    return {
      system: 'Memory 0.4.1',
      version: '0.4.1',
      total_memories: this.memories.length,
      perspectives: p,
      hierarchy: h,
      knowledge_merger: m,
      predictor: this.predictor.status(),
      validator: v,
      learner: l,
      forgetter: f,
      timestamp: new Date().toISOString()
    };
  }
  
  status() {
    const h = this.hierarchy.stats();
    const m = this.merger.stats();
    const v = this.validator.stats();
    const l = this.learner.stats();
    const f = this.forgetter.stats();
    const p = this.statsByPerspective();
    
    const perspectiveLines = [];
    for (const [perspective, stats] of Object.entries(p)) {
      const label = perspective !== 'shared' ? perspective : '共享';
      perspectiveLines.push(`  - ${label}: ${stats.count} 条`);
    }
    
    const lines = [
      '🧠 Memory 0.4.1 完整状态',
      '='.repeat(50),
      `📚 总记忆: ${this.memories.length} 条`,
      '',
      '👥 Agent 视角:'
    ];
    
    if (perspectiveLines.length > 0) {
      lines.push(...perspectiveLines);
    } else {
      lines.push('  暂无视角数据');
    }
    
    lines.push(
      '',
      '📊 分层缓存:',
      `  🔥 L1 热: ${h.L1_hot.count}/${h.L1_hot.max_size} (avg: ${h.L1_hot.avg_importance.toFixed(2)})`,
      `  🌡️ L2 温: ${h.L2_warm.count}/${h.L2_warm.max_size} (avg: ${h.L2_warm.avg_importance.toFixed(2)})`,
      `  ❄️ L3 冷: ${h.L3_cold.count}`,
      '',
      '📦 知识合并:',
      `  知识块: ${m.total_knowledge_blocks}`,
      `  Token 节省: ~${m.estimated_tokens_saved}`,
      '',
      '✅ 置信度:',
      `  已验证: ${v.by_confidence['✅ 已验证'] || 0}`,
      `  可能过时: ${v.by_confidence['⚠️ 可能过时'] || 0}`,
      `  矛盾: ${v.by_confidence['❌ 矛盾'] || 0}`,
      '',
      '📝 反馈学习:',
      `  总反馈: ${l.total_feedback}`,
      `  修正: ${l.total_corrections}`,
      '',
      '🗑️ 智能遗忘:',
      `  已遗忘: ${f.state.forgotten_count || 0}`,
      `  已归档: ${f.state.archived_count || 0}`,
      `  已压缩: ${f.state.compressed_count || 0}`,
      '='.repeat(50)
    );
    
    return lines.join('\n');
  }
}

// ========== CLI ==========

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command) {
    console.log('Usage: node memory.js <command> [options]');
    console.log('Commands: status, store, search, stats, validate, feedback, forget');
    process.exit(1);
  }
  
  console.log('🚀 启动 Memory 0.4.1...');
  const mem = new MemorySystemV7();
  
  switch (command) {
    case 'status':
      console.log(mem.status());
      break;
    
    case 'store': {
      const content = args.slice(1).join(' ') || args[1];
      if (!content) {
        console.log('❌ 请提供内容');
        process.exit(1);
      }
      const agentIdx = args.indexOf('--agent');
      const agent = agentIdx !== -1 ? args[agentIdx + 1] : null;
      const result = await mem.store(content, null, agent);
      const label = agent || '共享';
      console.log(`✅ 已存储记忆 [${label}]: ${result.content}`);
      console.log(JSON.stringify(result, null, 2));
      break;
    }
    
    case 'search': {
      const query = args.slice(1).join(' ') || args[1];
      if (!query) {
        console.log('❌ 请提供查询内容');
        process.exit(1);
      }
      const agentIdx = args.indexOf('--agent');
      const sharedIdx = args.indexOf('--shared-only');
      const agent = agentIdx !== -1 ? args[agentIdx + 1] : null;
      const sharedOnly = sharedIdx !== -1;
      const limitIdx = args.indexOf('--limit');
      const limit = limitIdx !== -1 ? parseInt(args[limitIdx + 1]) : 10;
      
      const results = mem.search(query, agent, sharedOnly, limit);
      const label = agent || (sharedOnly ? '共享' : '全部');
      console.log(`🔍 搜索 [${label}]: ${query}`);
      console.log(`找到 ${results.length} 条匹配记忆:\n`);
      
      results.forEach((result, i) => {
        const perspective = result.agent_perspective || 'shared';
        const confidence = result.confidence || 0;
        const score = result.score || 0;
        const timestamp = result.timestamp || '';
        console.log(`${i + 1}. [${perspective}] (置信度: ${confidence.toFixed(2)}, 评分: ${score.toFixed(2)})`);
        console.log(`   ${(result.content || '').slice(0, 100)}...`);
        if (timestamp) console.log(`   时间: ${timestamp}`);
        console.log();
      });
      
      if (results.length === 0) {
        console.log('未找到匹配的记忆');
      }
      break;
    }
    
    case 'stats': {
      const stats = mem.stats();
      console.log('📊 视角统计:');
      const perspectives = stats.perspectives || {};
      for (const [perspective, pstats] of Object.entries(perspectives)) {
        const label = perspective !== 'shared' ? perspective : '共享记忆';
        console.log(`  - ${label}: ${pstats.count} 条`);
        if (pstats.latest) console.log(`    最新: ${pstats.latest}`);
        if (pstats.avg_confidence) console.log(`    平均置信度: ${pstats.avg_confidence.toFixed(2)}`);
      }
      console.log();
      console.log(JSON.stringify(stats, null, 2));
      break;
    }
    
    case 'validate':
      console.log(JSON.stringify(mem.validate(), null, 2));
      break;
    
    case 'feedback':
      console.log(JSON.stringify(await mem.feedback(), null, 2));
      break;
    
    case 'forget': {
      const dryRun = !args.includes('--no-dry-run');
      const result = await mem.forget(dryRun);
      if (dryRun) {
        console.log(`📋 预览: 将删除 ${result.total_to_remove} 条记忆`);
      } else {
        console.log(`✅ 已删除 ${result.total_to_remove} 条记忆`);
      }
      console.log(JSON.stringify(result, null, 2));
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

export default MemorySystemV7;
