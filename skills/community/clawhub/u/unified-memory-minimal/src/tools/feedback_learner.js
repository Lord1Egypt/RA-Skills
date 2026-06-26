/**
 * Feedback Learner - 反馈学习闭环 v7.0
 * 
 * Features:
 * - Track memory usage effectiveness
 * - Adjust importance based on feedback
 * - Record correction history
 * - Support active learning
 * 
 * Usage:
 *   node feedback_learner.js track <memory_id> <outcome>
 *   node feedback_learner.js adjust
 *   node feedback_learner.js corrections
 *   node feedback_learner.js learn <correction>
 *   node feedback_learner.js stats
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import os from 'os';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ========== Configuration ==========

const WORKSPACE = path.join(os.homedir(), '.openclaw', 'workspace');
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const FEEDBACK_DIR = path.join(MEMORY_DIR, 'feedback');

const IMPORTANCE_BOOST = 0.1;
const IMPORTANCE_DECAY = 0.1;
const MIN_IMPORTANCE = 0.1;
const MAX_IMPORTANCE = 1.0;

const FEEDBACK_LOG_FILE = path.join(FEEDBACK_DIR, 'feedback_log.jsonl');
const CORRECTIONS_FILE = path.join(FEEDBACK_DIR, 'corrections.json');
const IMPORTANCE_ADJUSTMENTS_FILE = path.join(FEEDBACK_DIR, 'importance_adjustments.json');

// Ensure directories exist
await fs.mkdir(FEEDBACK_DIR, { recursive: true });

// ========== Outcome Types ==========

const OUTCOME_HELPFUL = 'helpful';
const OUTCOME_IRRELEVANT = 'irrelevant';
const OUTCOME_WRONG = 'wrong';
const OUTCOME_OUTDATED = 'outdated';

// ========== Feedback Learner ==========

class FeedbackLearner {
  constructor() {
    this.feedbackLog = [];
    this.corrections = [];
    this.adjustments = {}; // memory_id -> adjustments
    this._load();
  }
  
  async _load() {
    try {
      if (await fileExists(FEEDBACK_LOG_FILE)) {
        const content = await fs.readFile(FEEDBACK_LOG_FILE, 'utf-8');
        const lines = content.split('\n').filter(l => l.trim());
        this.feedbackLog = lines.map(l => {
          try { return JSON.parse(l); }
          catch { return null; }
        }).filter(Boolean);
      }
      
      if (await fileExists(CORRECTIONS_FILE)) {
        this.corrections = JSON.parse(await fs.readFile(CORRECTIONS_FILE, 'utf-8'));
      }
      
      if (await fileExists(IMPORTANCE_ADJUSTMENTS_FILE)) {
        this.adjustments = JSON.parse(await fs.readFile(IMPORTANCE_ADJUSTMENTS_FILE, 'utf-8'));
      }
    } catch (e) {
      console.warn(`⚠️ 加载反馈数据失败: ${e.message}`);
    }
  }
  
  async _save() {
    try {
      const feedbackContent = this.feedbackLog.map(f => JSON.stringify(f)).join('\n');
      await fs.writeFile(FEEDBACK_LOG_FILE, feedbackContent, 'utf-8');
      await fs.writeFile(CORRECTIONS_FILE, JSON.stringify(this.corrections, null, 2), 'utf-8');
      await fs.writeFile(IMPORTANCE_ADJUSTMENTS_FILE, JSON.stringify(this.adjustments, null, 2), 'utf-8');
    } catch (e) {
      console.warn(`⚠️ 保存反馈数据失败: ${e.message}`);
    }
  }
  
  track(memoryId, outcome, context = null) {
    const feedback = {
      memory_id: memoryId,
      outcome,
      context: context ? context.slice(0, 200) : null,
      timestamp: new Date().toISOString()
    };
    
    this.feedbackLog.push(feedback);
    
    if (!(memoryId in this.adjustments)) {
      this.adjustments[memoryId] = [];
    }
    
    this.adjustments[memoryId].push({
      outcome,
      timestamp: feedback.timestamp
    });
    
    this._save();
    console.log(`📝 记录反馈: ${memoryId} -> ${outcome}`);
    
    return feedback;
  }
  
  adjustImportance(memories) {
    const adjustments = {};
    
    for (const mem of memories) {
      const memId = mem.id;
      if (!memId) continue;
      
      let currentImportance = parseFloat(mem.importance) || 0.5;
      const memAdjustments = this.adjustments[memId] || [];
      
      if (!memAdjustments.length) continue;
      
      // Get recent adjustments
      const recent = memAdjustments.filter(a => this._isRecent(a.timestamp));
      if (!recent.length) continue;
      
      // Count outcomes
      const outcomeCounts = {};
      for (const a of recent) {
        outcomeCounts[a.outcome] = (outcomeCounts[a.outcome] || 0) + 1;
      }
      
      // Adjust importance
      let newImportance = currentImportance;
      
      if (outcomeCounts[OUTCOME_HELPFUL] > 0) {
        newImportance = Math.min(MAX_IMPORTANCE, currentImportance + IMPORTANCE_BOOST * outcomeCounts[OUTCOME_HELPFUL]);
      }
      if (outcomeCounts[OUTCOME_IRRELEVANT] > 0) {
        newImportance = Math.max(MIN_IMPORTANCE, currentImportance - IMPORTANCE_DECAY * outcomeCounts[OUTCOME_IRRELEVANT]);
      }
      if (outcomeCounts[OUTCOME_WRONG] > 0 || outcomeCounts[OUTCOME_OUTDATED] > 0) {
        newImportance = Math.max(MIN_IMPORTANCE, currentImportance - IMPORTANCE_DECAY * 2);
      }
      
      if (newImportance !== currentImportance) {
        adjustments[memId] = {
          old: currentImportance,
          new: newImportance,
          delta: newImportance - currentImportance
        };
        mem.importance = newImportance;
      }
    }
    
    return adjustments;
  }
  
  _isRecent(timestamp) {
    if (!timestamp) return false;
    const ts = new Date(timestamp);
    const daysDiff = (Date.now() - ts.getTime()) / (1000 * 60 * 60 * 24);
    return daysDiff <= 7; // Within 7 days
  }
  
  learn(correction) {
    const entry = {
      id: `correction_${Date.now()}`,
      content: correction,
      learned_at: new Date().toISOString()
    };
    
    this.corrections.push(entry);
    this._save();
    console.log(`📚 学习修正: ${correction.slice(0, 50)}...`);
    
    return entry;
  }
  
  getCorrectionHistory(limit = 10) {
    return this.corrections.slice(-limit).reverse();
  }
  
  getFeedbackStats() {
    const stats = {
      total_feedback: this.feedbackLog.length,
      by_outcome: {},
      total_corrections: this.corrections.length,
      memories_with_feedback: Object.keys(this.adjustments).length
    };
    
    for (const feedback of this.feedbackLog) {
      const outcome = feedback.outcome;
      stats.by_outcome[outcome] = (stats.by_outcome[outcome] || 0) + 1;
    }
    
    return stats;
  }
  
  suggestForgetting(memories, threshold = 0.2) {
    const forgettable = [];
    
    for (const mem of memories) {
      const memId = mem.id;
      if (!memId) continue;
      
      const memAdjustments = this.adjustments[memId] || [];
      const recent = memAdjustments.filter(a => this._isRecent(a.timestamp));
      
      if (recent.length === 0) continue;
      
      // Check for repeated negative feedback
      const negativeCount = recent.filter(a => 
        a.outcome === OUTCOME_IRRELEVANT || 
        a.outcome === OUTCOME_WRONG || 
        a.outcome === OUTCOME_OUTDATED
      ).length;
      
      if (negativeCount >= 3) {
        forgettable.push({
          memory: mem,
          reason: 'repeated_negative_feedback',
          negative_count: negativeCount
        });
      }
    }
    
    return forgettable;
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
            id: `mem_${memories.length}`,
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
  
  async saveMemories(memories) {
    // Group by date
    const byDate = {};
    
    for (const mem of memories) {
      const date = mem.timestamp?.slice(0, 10) || new Date().toISOString().slice(0, 10);
      if (!byDate[date]) byDate[date] = [];
      byDate[date].push(mem);
    }
    
    // Write each date file
    for (const [date, mems] of Object.entries(byDate)) {
      const file = path.join(MEMORY_DIR, `${date}.md`);
      const lines = mems.map(m => 
        `- [${m.timestamp}] [${m.category}] [${m.scope}] [I=${m.importance.toFixed(2)}] ${m.text}`
      ).join('\n') + '\n';
      
      try {
        const existing = await fileExists(file) ? await fs.readFile(file, 'utf-8') : '';
        // This is simplified - in production would preserve existing content
        await fs.writeFile(file, existing + lines, 'utf-8');
      } catch (e) {
        console.warn(`保存失败: ${file}: ${e.message}`);
      }
    }
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
Feedback Learner - 反馈学习闭环 v7.0

Usage:
    node feedback_learner.js track <memory_id> <outcome>   # 记录使用效果
    node feedback_learner.js adjust                        # 调整重要性
    node feedback_learner.js corrections                    # 查看修正历史
    node feedback_learner.js learn <correction>            # 从修正中学习
    node feedback_learner.js stats                         # 统计
    node feedback_learner.js suggest                       # 建议遗忘
`);
    process.exit(1);
  }
  
  console.log('🚀 Feedback Learner v7.0...\n');
  
  const learner = new FeedbackLearner();
  
  switch (command) {
    case 'track': {
      const memoryId = args[1];
      const outcome = args[2];
      
      if (!memoryId || !outcome) {
        console.log('❌ 请提供 memory_id 和 outcome');
        console.log('   outcome 可选: helpful, irrelevant, wrong, outdated');
        process.exit(1);
      }
      
      learner.track(memoryId, outcome);
      break;
    }
    
    case 'adjust': {
      const memories = await learner.loadMemories();
      console.log(`📚 加载 ${memories.length} 条记忆`);
      
      const adjustments = learner.adjustImportance(memories);
      console.log(`\n📊 调整了 ${Object.keys(adjustments).length} 条记忆:`);
      
      for (const [id, adj] of Object.entries(adjustments)) {
        console.log(`  ${id}: ${adj.old.toFixed(2)} -> ${adj.new.toFixed(2)} (${adj.delta >= 0 ? '+' : ''}${adj.delta.toFixed(2)})`);
      }
      
      if (Object.keys(adjustments).length > 0) {
        await learner.saveMemories(memories);
        console.log('\n✅ 已保存调整后的记忆');
      }
      break;
    }
    
    case 'corrections': {
      const history = learner.getCorrectionHistory();
      console.log(`📜 修正历史 (${history.length}):\n`);
      
      for (const entry of history) {
        console.log(`[${entry.learned_at}] ${entry.content}`);
        console.log();
      }
      break;
    }
    
    case 'learn': {
      const correction = args.slice(1).join(' ');
      if (!correction) {
        console.log('❌ 请提供 correction 内容');
        process.exit(1);
      }
      
      learner.learn(correction);
      break;
    }
    
    case 'stats': {
      const stats = learner.getFeedbackStats();
      console.log('📊 统计:\n');
      console.log(`  总反馈: ${stats.total_feedback}`);
      console.log(`  修正数: ${stats.total_corrections}`);
      console.log(`  有反馈的记忆: ${stats.memories_with_feedback}`);
      console.log('\n  按结果类型:');
      for (const [outcome, count] of Object.entries(stats.by_outcome)) {
        console.log(`    ${outcome}: ${count}`);
      }
      break;
    }
    
    case 'suggest': {
      const memories = await learner.loadMemories();
      console.log(`📚 加载 ${memories.length} 条记忆`);
      
      const forgettable = learner.suggestForgetting(memories);
      console.log(`\n🗑️ 建议遗忘 (${forgettable.length}):\n`);
      
      for (const { memory, reason, negative_count } of forgettable) {
        console.log(`  - ${memory.text.slice(0, 50)}...`);
        console.log(`    原因: ${reason} (${negative_count}次负面反馈)`);
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

export { FeedbackLearner, OUTCOME_HELPFUL, OUTCOME_IRRELEVANT, OUTCOME_WRONG, OUTCOME_OUTDATED };

export default FeedbackLearner;
