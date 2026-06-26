/**
 * Collaboration Analytics - 协作效率分析系统 v1.0
 * 
 * Features:
 * - Statistics on collaboration efficiency
 * - Task completion rate analysis
 * - Identify collaboration bottlenecks
 * - Generate optimization suggestions
 * 
 * Usage:
 *   node analytics.js report      # 生成报告
 *   node analytics.js metrics     # 查看指标
 *   node analytics.js bottlenecks  # 分析瓶颈
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
const TASKS_DIR = path.join(MEMORY_DIR, 'tasks');
const TASKS_FILE = path.join(TASKS_DIR, 'tasks.jsonl');
const COLLAB_DIR = path.join(MEMORY_DIR, 'collaboration');
const COLLAB_LOG = path.join(COLLAB_DIR, 'collab_log.jsonl');
const SYNC_DIR = path.join(MEMORY_DIR, 'shared');
const SYNC_QUEUE = path.join(SYNC_DIR, 'sync_queue.jsonl');
const ANALYTICS_DIR = path.join(MEMORY_DIR, 'analytics');
const REPORTS_FILE = path.join(ANALYTICS_DIR, 'reports.jsonl');

// Ensure directories exist
await fs.mkdir(ANALYTICS_DIR, { recursive: true });

// ========== Data Loading ==========

async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function loadTasks() {
  if (!await fileExists(TASKS_FILE)) return [];
  
  try {
    const content = await fs.readFile(TASKS_FILE, 'utf-8');
    const lines = content.split('\n').filter(l => l.trim());
    return lines.map(l => {
      try { return JSON.parse(l); }
      catch { return null; }
    }).filter(Boolean);
  } catch {
    return [];
  }
}

async function loadCollabLogs() {
  if (!await fileExists(COLLAB_LOG)) return [];
  
  try {
    const content = await fs.readFile(COLLAB_LOG, 'utf-8');
    const lines = content.split('\n').filter(l => l.trim());
    return lines.map(l => {
      try { return JSON.parse(l); }
      catch { return null; }
    }).filter(Boolean);
  } catch {
    return [];
  }
}

async function loadSyncQueue() {
  if (!await fileExists(SYNC_QUEUE)) return [];
  
  try {
    const content = await fs.readFile(SYNC_QUEUE, 'utf-8');
    const lines = content.split('\n').filter(l => l.trim());
    return lines.map(l => {
      try { return JSON.parse(l); }
      catch { return null; }
    }).filter(Boolean);
  } catch {
    return [];
  }
}

// ========== Metrics Calculation ==========

function calculateMetrics() {
  return {
    tasks: { total: 0, completed: 0, pending: 0, in_progress: 0 },
    collab: { total: 0, by_action: {}, by_agent: {} },
    sync: { total: 0, synced: 0, pending: 0, rate: 0 },
    performance: { avg_task_duration: 0, completion_rate: 0 }
  };
}

async function getMetrics() {
  const tasks = await loadTasks();
  const logs = await loadCollabLogs();
  const syncItems = await loadSyncQueue();
  
  // Task metrics
  const totalTasks = tasks.length;
  const completedTasks = tasks.filter(t => t.status === 'completed').length;
  const pendingTasks = tasks.filter(t => t.status === 'pending').length;
  const inProgressTasks = tasks.filter(t => t.status === 'in_progress').length;
  
  // Task completion rate
  const completionRate = totalTasks > 0 ? (completedTasks / totalTasks * 100) : 0;
  
  // Average task duration
  let totalDuration = 0;
  let durationCount = 0;
  for (const task of tasks) {
    if (task.status === 'completed' && task.history) {
      let created = null;
      let completed = null;
      for (const h of task.history) {
        if (h.action === 'created') created = new Date(h.timestamp);
        if (h.action === 'status_change' && h.to === 'completed') completed = new Date(h.timestamp);
      }
      if (created && completed) {
        totalDuration += (completed - created) / 1000; // seconds
        durationCount++;
      }
    }
  }
  const avgTaskDuration = durationCount > 0 ? totalDuration / durationCount : 0;
  
  // Collaboration metrics
  const totalCollabs = logs.length;
  const byAction = {};
  const byAgent = {};
  
  for (const log of logs) {
    const action = log.action || 'unknown';
    byAction[action] = (byAction[action] || 0) + 1;
    
    const fromAgent = log.from_agent || 'unknown';
    const toAgent = log.to_agent || 'unknown';
    byAgent[fromAgent] = (byAgent[fromAgent] || 0) + 1;
    byAgent[toAgent] = (byAgent[toAgent] || 0) + 1;
  }
  
  // Sync metrics
  const totalSyncs = syncItems.length;
  const syncedItems = syncItems.filter(s => (s.synced_to?.length || 0) >= 2).length;
  const pendingSyncs = totalSyncs - syncedItems;
  const syncRate = totalSyncs > 0 ? (syncedItems / totalSyncs * 100) : 0;
  
  return {
    tasks: {
      total: totalTasks,
      completed: completedTasks,
      pending: pendingTasks,
      in_progress: inProgressTasks,
      completion_rate: completionRate.toFixed(1)
    },
    collab: {
      total: totalCollabs,
      by_action: byAction,
      by_agent: byAgent
    },
    sync: {
      total: totalSyncs,
      synced: syncedItems,
      pending: pendingSyncs,
      rate: syncRate.toFixed(1)
    },
    performance: {
      avg_task_duration: avgTaskDuration.toFixed(0),
      avg_task_duration_formatted: formatDuration(avgTaskDuration)
    }
  };
}

function formatDuration(seconds) {
  if (seconds < 60) return `${seconds.toFixed(0)}秒`;
  if (seconds < 3600) return `${(seconds / 60).toFixed(0)}分钟`;
  if (seconds < 86400) return `${(seconds / 3600).toFixed(1)}小时`;
  return `${(seconds / 86400).toFixed(1)}天`;
}

// ========== Bottleneck Analysis ==========

async function analyzeBottlenecks() {
  const metrics = await getMetrics();
  const bottlenecks = [];
  
  // Task completion rate bottleneck
  if (parseFloat(metrics.tasks.completion_rate) < 50) {
    bottlenecks.push({
      type: 'low_completion_rate',
      severity: 'high',
      description: `任务完成率过低: ${metrics.tasks.completion_rate}%`,
      suggestion: '检查任务分配是否合理，是否存在阻塞任务'
    });
  }
  
  // Pending tasks bottleneck
  if (metrics.tasks.pending > 10) {
    bottlenecks.push({
      type: 'high_pending',
      severity: 'medium',
      description: `待处理任务过多: ${metrics.tasks.pending}个`,
      suggestion: '考虑增加资源或分解任务'
    });
  }
  
  // Sync bottleneck
  if (parseFloat(metrics.sync.rate) < 80) {
    bottlenecks.push({
      type: 'low_sync_rate',
      severity: 'medium',
      description: `同步率较低: ${metrics.sync.rate}%`,
      suggestion: '检查同步队列和协作总线状态'
    });
  }
  
  // Long task duration
  if (parseFloat(metrics.performance.avg_task_duration) > 86400) { // > 1 day
    bottlenecks.push({
      type: 'long_task_duration',
      severity: 'low',
      description: `平均任务时长过长: ${metrics.performance.avg_task_duration_formatted}`,
      suggestion: '考虑分解大任务或增加并行'
    });
  }
  
  return bottlenecks;
}

// ========== Report Generation ==========

async function generateReport() {
  const metrics = await getMetrics();
  const bottlenecks = await analyzeBottlenecks();
  
  const report = {
    id: `report_${Date.now()}`,
    timestamp: new Date().toISOString(),
    metrics,
    bottlenecks,
    summary: generateSummary(metrics, bottlenecks)
  };
  
  // Save report
  await fs.appendFile(REPORTS_FILE, JSON.stringify(report) + '\n', 'utf-8');
  
  return report;
}

function generateSummary(metrics, bottlenecks) {
  const lines = [];
  
  lines.push('📊 协作效率概览');
  lines.push('='.repeat(40));
  lines.push('');
  lines.push('任务统计:');
  lines.push(`  总任务: ${metrics.tasks.total}`);
  lines.push(`  已完成: ${metrics.tasks.completed} (${metrics.tasks.completion_rate}%)`);
  lines.push(`  进行中: ${metrics.tasks.in_progress}`);
  lines.push(`  待处理: ${metrics.tasks.pending}`);
  lines.push('');
  lines.push('协作统计:');
  lines.push(`  总协作事件: ${metrics.collab.total}`);
  const topActions = Object.entries(metrics.collab.by_action)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3)
    .map(([k, v]) => `${k}: ${v}`);
  lines.push(`  主要活动: ${topActions.join(', ')}`);
  lines.push('');
  lines.push('同步状态:');
  lines.push(`  同步率: ${metrics.sync.rate}%`);
  lines.push(`  同步队列: ${metrics.sync.pending} 待处理`);
  
  if (bottlenecks.length > 0) {
    lines.push('');
    lines.push('⚠️ 瓶颈分析:');
    for (const bn of bottlenecks) {
      lines.push(`  [${bn.severity}] ${bn.description}`);
    }
  }
  
  return lines.join('\n');
}

// ========== CLI ==========

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command) {
    console.log(`
Collaboration Analytics - 协作效率分析系统 v1.0

Usage:
    node analytics.js report      # 生成报告
    node analytics.js metrics     # 查看指标
    node analytics.js bottlenecks  # 分析瓶颈
`);
    process.exit(1);
  }
  
  console.log('🚀 Collaboration Analytics v1.0...\n');
  
  switch (command) {
    case 'report': {
      const report = await generateReport();
      console.log(report.summary);
      break;
    }
    
    case 'metrics': {
      const metrics = await getMetrics();
      console.log('📊 指标详情:\n');
      console.log(JSON.stringify(metrics, null, 2));
      break;
    }
    
    case 'bottlenecks': {
      const bottlenecks = await analyzeBottlenecks();
      console.log('🔍 瓶颈分析:\n');
      
      if (bottlenecks.length === 0) {
        console.log('✅ 未发现明显瓶颈');
      } else {
        for (const bn of bottlenecks) {
          console.log(`[${bn.severity.toUpperCase()}] ${bn.description}`);
          console.log(`   建议: ${bn.suggestion}`);
          console.log();
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

export { getMetrics, analyzeBottlenecks, generateReport };

export default { getMetrics, analyzeBottlenecks, generateReport };
