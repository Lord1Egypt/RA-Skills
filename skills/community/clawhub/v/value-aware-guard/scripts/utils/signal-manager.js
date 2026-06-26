/**
 * 信号管理器 - 直接文件系统操作版本
 * 
 * 直接读写信号文件，不依赖OpenClaw CLI命令
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const WORKSPACE = process.env.HOME ? path.join(process.env.HOME, '.openclaw/workspace') : '/tmp/.openclaw/workspace';
const SOUL_DIR = path.join(WORKSPACE, '.soul');
const SIGNALS_DIR = path.join(SOUL_DIR, 'signals');
const PROCESSED_DIR = path.join(SIGNALS_DIR, 'processed');

// 确保目录存在
function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

// 生成信号ID
function generateSignalId() {
  return `sig_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
}

/**
 * 发布信号到文件系统
 * @param {string} source 信号来源
 * @param {string} type 信号类型
 * @param {object} payload 信号内容
 * @param {string} priority 优先级 (high/medium/low)
 * @returns {string} 信号ID
 */
export function publishSignal(source, type, payload, priority = 'medium') {
  ensureDir(SIGNALS_DIR);
  
  const signal = {
    id: generateSignalId(),
    source,
    type,
    payload,
    priority,
    createdAt: new Date().toISOString(),
    status: 'pending',
    processedBy: []
  };
  
  const pendingFile = path.join(SIGNALS_DIR, 'pending.jsonl');
  fs.appendFileSync(pendingFile, JSON.stringify(signal) + '\n');
  
  console.log(`[signal] 已发布: ${source} -> ${type} (${priority}) [${signal.id}]`);
  return signal.id;
}

/**
 * 读取待处理信号
 * @param {string} type 筛选信号类型
 * @param {string} source 筛选信号来源
 * @returns {Array} 信号列表
 */
export function getPendingSignals(type = null, source = null) {
  ensureDir(SIGNALS_DIR);
  
  const pendingFile = path.join(SIGNALS_DIR, 'pending.jsonl');
  if (!fs.existsSync(pendingFile)) {
    return [];
  }
  
  try {
    const content = fs.readFileSync(pendingFile, 'utf-8');
    const lines = content.split('\n').filter(line => line.trim());
    
    const signals = lines.map(line => {
      try {
        return JSON.parse(line);
      } catch {
        return null;
      }
    }).filter(signal => signal && signal.status === 'pending');
    
    // 筛选
    let filtered = signals;
    if (type) {
      filtered = filtered.filter(s => s.type === type);
    }
    if (source) {
      filtered = filtered.filter(s => s.source === source);
    }
    
    return filtered;
  } catch (error) {
    console.error('读取信号文件失败:', error.message);
    return [];
  }
}

/**
 * 处理信号（移动到已处理）
 * @param {string} signalId 信号ID
 * @param {string} status 处理状态 (done/ignored)
 * @param {string} processedBy 处理者
 * @returns {boolean} 是否成功
 */
export function resolveSignal(signalId, status = 'done', processedBy = 'proactive-trigger') {
  ensureDir(SIGNALS_DIR);
  ensureDir(PROCESSED_DIR);
  
  const pendingFile = path.join(SIGNALS_DIR, 'pending.jsonl');
  const today = new Date().toISOString().split('T')[0];
  const processedFile = path.join(PROCESSED_DIR, `${today}.jsonl`);
  
  if (!fs.existsSync(pendingFile)) {
    return false;
  }
  
  try {
    const content = fs.readFileSync(pendingFile, 'utf-8');
    const lines = content.split('\n').filter(line => line.trim());
    
    let signalFound = null;
    const remainingSignals = [];
    
    for (const line of lines) {
      try {
        const signal = JSON.parse(line);
        if (signal.id === signalId) {
          signalFound = signal;
          // 更新信号状态
          signal.status = status;
          signal.processedAt = new Date().toISOString();
          signal.processedBy = [...(signal.processedBy || []), processedBy];
          
          // 保存到已处理文件
          fs.appendFileSync(processedFile, JSON.stringify(signal) + '\n');
        } else {
          remainingSignals.push(line);
        }
      } catch {
        // 跳过无效行
      }
    }
    
    if (signalFound) {
      // 写回剩余信号
      fs.writeFileSync(pendingFile, remainingSignals.join('\n') + (remainingSignals.length > 0 ? '\n' : ''));
      console.log(`[signal] 已处理: ${signalId} -> ${status}`);
      return true;
    } else {
      console.log(`[signal] 未找到信号: ${signalId}`);
      return false;
    }
  } catch (error) {
    console.error('处理信号失败:', error.message);
    return false;
  }
}

/**
 * 批量处理信号
 * @param {Array} signalIds 信号ID数组
 * @param {string} status 处理状态
 * @param {string} processedBy 处理者
 * @returns {number} 成功处理的数量
 */
export function resolveSignals(signalIds, status = 'done', processedBy = 'proactive-trigger') {
  let successCount = 0;
  
  for (const signalId of signalIds) {
    if (resolveSignal(signalId, status, processedBy)) {
      successCount++;
    }
  }
  
  console.log(`[signal] 批量处理完成: ${successCount}/${signalIds.length}个信号`);
  return successCount;
}

/**
 * 获取信号统计
 * @returns {object} 统计信息
 */
export function getSignalStats() {
  ensureDir(SIGNALS_DIR);
  
  const pendingFile = path.join(SIGNALS_DIR, 'pending.jsonl');
  const today = new Date().toISOString().split('T')[0];
  const processedFile = path.join(PROCESSED_DIR, `${today}.jsonl`);
  
  let pendingSignals = [];
  let processedToday = [];
  
  if (fs.existsSync(pendingFile)) {
    try {
      const content = fs.readFileSync(pendingFile, 'utf-8');
      pendingSignals = content.split('\n').filter(line => line.trim()).map(line => {
        try { return JSON.parse(line); } catch { return null; }
      }).filter(Boolean);
    } catch {}
  }
  
  if (fs.existsSync(processedFile)) {
    try {
      const content = fs.readFileSync(processedFile, 'utf-8');
      processedToday = content.split('\n').filter(line => line.trim()).map(line => {
        try { return JSON.parse(line); } catch { return null; }
      }).filter(Boolean);
    } catch {}
  }
  
  const allSignals = [...pendingSignals, ...processedToday];
  const stats = {};
  
  for (const signal of allSignals) {
    stats[signal.type] = (stats[signal.type] || 0) + 1;
  }
  
  return {
    pending: pendingSignals.length,
    processedToday: processedToday.length,
    stats: Object.entries(stats).map(([type, count]) => ({ type, count }))
  };
}

/**
 * 清理旧信号文件（保留最近7天）
 */
export function cleanupOldSignals(daysToKeep = 7) {
  ensureDir(PROCESSED_DIR);
  
  try {
    const files = fs.readdirSync(PROCESSED_DIR);
    const now = Date.now();
    const cutoff = daysToKeep * 24 * 60 * 60 * 1000;
    
    let deletedCount = 0;
    
    for (const file of files) {
      if (file.endsWith('.jsonl')) {
        const filePath = path.join(PROCESSED_DIR, file);
        const stat = fs.statSync(filePath);
        const age = now - stat.mtimeMs;
        
        if (age > cutoff) {
          fs.unlinkSync(filePath);
          deletedCount++;
          console.log(`[signal] 清理旧文件: ${file}`);
        }
      }
    }
    
    if (deletedCount > 0) {
      console.log(`[signal] 清理完成: 删除${deletedCount}个旧文件`);
    }
    
    return deletedCount;
  } catch (error) {
    console.error('清理信号文件失败:', error.message);
    return 0;
  }
}

/**
 * 测试信号系统
 */
export function testSignalSystem() {
  console.log('=== 信号系统测试 ===');
  
  // 发布测试信号
  const testId = publishSignal('test', 'test_signal', { message: '测试信号' }, 'low');
  console.log(`1. 发布测试信号: ${testId}`);
  
  // 读取信号
  const signals = getPendingSignals();
  console.log(`2. 读取待处理信号: ${signals.length}个`);
  
  // 处理信号
  const resolved = resolveSignal(testId, 'done', 'test');
  console.log(`3. 处理信号: ${resolved ? '成功' : '失败'}`);
  
  // 获取统计
  const stats = getSignalStats();
  console.log('4. 信号统计:');
  console.log(`   待处理: ${stats.pending}`);
  console.log(`   今日已处理: ${stats.processedToday}`);
  
  console.log('=== 测试完成 ===');
  return { testId, resolved, stats };
}

export default {
  publishSignal,
  getPendingSignals,
  resolveSignal,
  resolveSignals,
  getSignalStats,
  cleanupOldSignals,
  testSignalSystem
};