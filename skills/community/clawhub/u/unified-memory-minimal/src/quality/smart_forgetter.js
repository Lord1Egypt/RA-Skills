/**
 * smart_forgetter.js - 智能遗忘器
 * Ported from Python smart_forgetter.py
 * 
 * 自动遗忘低价值记忆、归档旧记忆、压缩冷记忆
 */

import { existsSync, mkdirSync, readFileSync, writeFileSync, unlinkSync, readdirSync, statSync } from 'fs';
import { join } from 'path';
import { getAllMemories, saveMemories, deleteMemory } from '../storage.js';
import { log } from '../config.js';

const HOME = process.env.HOME || '/root';
const MEMORY_DIR = join(HOME, '.openclaw/workspace/memory');
const ARCHIVE_DIR = join(MEMORY_DIR, 'archive');
const STATE_FILE = join(MEMORY_DIR, 'forgetter_state.json');

// 参数配置
const FORGET_IMPORTANCE = 0.1;
const FORGET_AGE_DAYS = 90;
const FORGET_NEVER_ACCESSED_DAYS = 60;
const DUPLICATE_THRESHOLD = 0.95;
const MAX_ARCHIVE_SIZE_MB = 100;

function ensureArchiveDir() {
  if (!existsSync(ARCHIVE_DIR)) {
    mkdirSync(ARCHIVE_DIR, { recursive: true });
  }
}

function loadState() {
  try {
    if (existsSync(STATE_FILE)) {
      return JSON.parse(readFileSync(STATE_FILE, 'utf-8'));
    }
  } catch { }
  return { last_forget: null, forgotten_count: 0, archived_count: 0, compressed_count: 0 };
}

function saveState(state) {
  try {
    writeFileSync(STATE_FILE, JSON.stringify(state, null, 2), 'utf-8');
  } catch (err) {
    log('WARN', `Failed to save forgetter state: ${err.message}`);
  }
}

/**
 * 找出可遗忘的记忆
 */
export function findForgettable(memories) {
  const now = Date.now();
  const forgettable = [];
  
  for (const mem of memories) {
    const text = mem.text || '';
    const importance = mem.importance ?? 0.5;
    
    // 条件1: 重要性极低
    if (importance < FORGET_IMPORTANCE) {
      forgettable.push({
        id: mem.id,
        reason: 'low_importance',
        importance,
        text: text.slice(0, 100)
      });
      continue;
    }
    
    // 条件2: 年龄过大
    const createdAt = mem.created_at || mem.timestamp;
    if (createdAt) {
      const created = new Date(typeof createdAt === 'number' ? createdAt : createdAt).getTime();
      const ageDays = (now - created) / (1000 * 60 * 60 * 24);
      
      if (ageDays > FORGET_AGE_DAYS) {
        forgettable.push({
          id: mem.id,
          reason: 'too_old',
          age_days: Math.round(ageDays),
          text: text.slice(0, 100)
        });
      }
    }
  }
  
  return forgettable;
}

/**
 * 查找重复记忆组
 */
export function findDuplicateGroups(memories) {
  const groups = [];
  const visited = new Set();
  
  for (let i = 0; i < memories.length; i++) {
    const mem1 = memories[i];
    if (visited.has(mem1.id)) continue;
    
    const text1 = (mem1.text || '').toLowerCase();
    if (!text1) continue;
    
    const group = [mem1.id];
    
    for (let j = i + 1; j < memories.length; j++) {
      const mem2 = memories[j];
      if (visited.has(mem2.id)) continue;
      
      const text2 = (mem2.text || '').toLowerCase();
      if (!text2) continue;
      
      if (simpleSimilarity(text1, text2) >= DUPLICATE_THRESHOLD) {
        group.push(mem2.id);
        visited.add(mem2.id);
      }
    }
    
    if (group.length > 1) {
      groups.push(group);
      visited.add(mem1.id);
    }
  }
  
  return groups;
}

function simpleSimilarity(text1, text2) {
  const words1 = new Set(text1.split(/\s+/));
  const words2 = new Set(text2.split(/\s+/));
  
  if (!words1.size || !words2.size) return 0;
  
  const intersection = [...words1].filter(w => words2.has(w)).length;
  const union = new Set([...words1, ...words2]).size;
  
  return intersection / union;
}

/**
 * 执行遗忘
 */
export async function forget({ dryRun = true } = {}) {
  const memories = getAllMemories();
  const state = loadState();
  
  const forgettable = findForgettable(memories);
  
  if (dryRun) {
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          mode: 'dry_run',
          forgettable_count: forgettable.length,
          forgettable: forgettable.slice(0, 20),
          message: `将遗忘 ${forgettable.length} 条记忆（dry-run）`
        }, null, 2)
      }]
    };
  }
  
  // 执行遗忘
  const forgetIds = new Set(forgettable.map(f => f.id));
  const remaining = memories.filter(m => !forgetIds.has(m.id));
  
  saveMemories(remaining);
  
  state.forgotten_count += forgettable.length;
  state.last_forget = new Date().toISOString();
  saveState(state);
  
  return {
    content: [{
      type: 'text',
      text: JSON.stringify({
        mode: 'executed',
        forgotten_count: forgettable.length,
        remaining_count: remaining.length
      }, null, 2)
    }]
  };
}

/**
 * 归档旧记忆
 */
export async function archive({ days = 90, dryRun = true } = {}) {
  ensureArchiveDir();
  const memories = getAllMemories();
  const now = Date.now();
  const archivedIds = [];
  
  for (const mem of memories) {
    const createdAt = mem.created_at || mem.timestamp;
    if (!createdAt) continue;
    
    const created = new Date(typeof createdAt === 'number' ? createdAt : createdAt).getTime();
    const ageDays = (now - created) / (1000 * 60 * 60 * 24);
    
    if (ageDays > days) {
      archivedIds.push(mem.id);
      
      if (!dryRun) {
        const archiveFile = join(ARCHIVE_DIR, `mem_${mem.id}_${Date.now()}.json`);
        try {
          writeFileSync(archiveFile, JSON.stringify(mem, null, 2), 'utf-8');
        } catch { }
      }
    }
  }
  
  if (!dryRun && archivedIds.length > 0) {
    const remaining = memories.filter(m => !archivedIds.includes(m.id));
    saveMemories(remaining);
    
    const state = loadState();
    state.archived_count += archivedIds.length;
    state.last_forget = new Date().toISOString();
    saveState(state);
  }
  
  return {
    content: [{
      type: 'text',
      text: JSON.stringify({
        mode: dryRun ? 'dry_run' : 'executed',
        archived_count: archivedIds.length,
        days
      }, null, 2)
    }]
  };
}

/**
 * 压缩冷记忆
 */
export async function compressCold() {
  const memories = getAllMemories();
  let compressed = 0;
  let beforeTotal = 0;
  let afterTotal = 0;
  
  for (const mem of memories) {
    const importance = mem.importance ?? 0.5;
    
    if (importance < 0.3) {
      const text = mem.text || '';
      if (text.length > 200) {
        const originalLen = text.length;
        mem.text = compressText(text);
        mem.compressed = true;
        mem.original_length = originalLen;
        compressed++;
        beforeTotal += originalLen;
        afterTotal += mem.text.length;
      }
    }
  }
  
  if (compressed > 0) {
    saveMemories(memories);
    const state = loadState();
    state.compressed_count += compressed;
    saveState(state);
  }
  
  return {
    content: [{
      type: 'text',
      text: JSON.stringify({
        compressed_count: compressed,
        compression_ratio: beforeTotal > 0 ? afterTotal / beforeTotal : 1,
        before_chars: beforeTotal,
        after_chars: afterTotal
      }, null, 2)
    }]
  };
}

function compressText(text) {
  const lines = text.split('\n');
  if (lines.length > 5) {
    return [...lines.slice(0, 3), `... (${lines.length - 4} lines omitted) ...`, lines[lines.length - 1]].join('\n');
  } else if (text.length > 200) {
    return text.slice(0, 150) + '... [truncated]';
  }
  return text;
}

/**
 * 清理归档目录
 */
export async function cleanArchive() {
  ensureArchiveDir();
  
  try {
    const files = readdirSync(ARCHIVE_DIR)
      .filter(f => f.endsWith('.json'))
      .map(f => ({
        name: f,
        path: join(ARCHIVE_DIR, f),
        mtime: statSync(join(ARCHIVE_DIR, f)).mtimeMs
      }))
      .sort((a, b) => a.mtime - b.mtime); // oldest first
    
    let totalSize = files.reduce((sum, f) => sum + statSync(f.path).size, 0);
    const maxBytes = MAX_ARCHIVE_SIZE_MB * 1024 * 1024;
    
    let removed = 0;
    while (totalSize > maxBytes * 0.8 && files.length > 0) {
      const oldest = files.shift();
      const size = statSync(oldest.path).size;
      unlinkSync(oldest.path);
      totalSize -= size;
      removed++;
    }
    
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({ removed_files: removed, remaining_files: files.length }, null, 2)
      }]
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `Clean failed: ${err.message}` }], isError: true };
  }
}

/**
 * 统计
 */
export async function forgetterStats() {
  const state = loadState();
  let archiveSize = 0;
  let archiveFiles = 0;
  
  try {
    if (existsSync(ARCHIVE_DIR)) {
      const files = readdirSync(ARCHIVE_DIR).filter(f => f.endsWith('.json'));
      archiveFiles = files.length;
      for (const f of files) {
        archiveSize += statSync(join(ARCHIVE_DIR, f)).size;
      }
    }
  } catch { }
  
  return {
    content: [{
      type: 'text',
      text: JSON.stringify({
        state,
        archive_size_mb: Math.round(archiveSize / (1024 * 1024) * 100) / 100,
        archive_files: archiveFiles,
        parameters: {
          forget_importance: FORGET_IMPORTANCE,
          forget_age_days: FORGET_AGE_DAYS,
          duplicate_threshold: DUPLICATE_THRESHOLD,
          max_archive_size_mb: MAX_ARCHIVE_SIZE_MB
        }
      }, null, 2)
    }]
  };
}
