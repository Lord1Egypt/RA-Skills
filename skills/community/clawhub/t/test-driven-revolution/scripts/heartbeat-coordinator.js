#!/usr/bin/env node
/**
 * heartbeat-coordinator.js - Wilson 心跳协调器
 * 
 * 职责：
 * 1. 激活依赖完成的任务（queued → pending）
 * 2. 检测 pending 任务，进行安全扫描
 * 3. 调用 Sonnet 审阅
 * 4. 记录所有事件到 logs/events.log
 * 
 * 触发频率：每 5 分钟
 * 模型：Qwen（包月）+ Sonnet（审阅时）
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const SKILL_DIR = path.join(__dirname, '..');
const TASKS_DIR = path.join(SKILL_DIR, 'tasks');
const LOGS_DIR = path.join(SKILL_DIR, 'logs');
const SCRIPTS_DIR = path.join(SKILL_DIR, 'scripts');

// 确保日志目录存在
if (!fs.existsSync(LOGS_DIR)) {
  fs.mkdirSync(LOGS_DIR, { recursive: true });
}

const EVENTS_LOG = path.join(LOGS_DIR, 'events.log');

/**
 * 写入事件日志
 */
function logEvent(event, data = {}) {
  const entry = {
    timestamp: new Date().toISOString(),
    event,
    ...data
  };
  fs.appendFileSync(EVENTS_LOG, JSON.stringify(entry) + '\n');
  console.log(`📝 事件：${event}`, JSON.stringify(data));
  return entry;
}

/**
 * 原子锁操作
 */
function acquireLock(taskId) {
  try {
    execSync(`bash ${SCRIPTS_DIR}/atomic-lock.sh acquire ${taskId}`, { stdio: 'pipe' });
    return true;
  } catch (error) {
    return false; // 锁已存在
  }
}

function releaseLock(taskId) {
  try {
    execSync(`bash ${SCRIPTS_DIR}/atomic-lock.sh release ${taskId}`, { stdio: 'pipe' });
  } catch (error) {
    console.error(`⚠️ 释放锁失败：${taskId}`, error.message);
  }
}

/**
 * 读取任务文件
 */
function readTask(taskId) {
  const taskFile = path.join(TASKS_DIR, `${taskId}.json`);
  if (!fs.existsSync(taskFile)) {
    return null;
  }
  return JSON.parse(fs.readFileSync(taskFile, 'utf8'));
}

/**
 * 写入任务文件
 */
function writeTask(task) {
  const taskFile = path.join(TASKS_DIR, `${task.task_id}.json`);
  fs.writeFileSync(taskFile, JSON.stringify(task, null, 2));
}

/**
 * 列出所有任务
 */
function listTasks() {
  if (!fs.existsSync(TASKS_DIR)) {
    return [];
  }
  return fs.readdirSync(TASKS_DIR)
    .filter(f => f.endsWith('.json') && !f.includes('-example'))
    .map(f => f.replace('.json', ''));
}

/**
 * Step 1: 激活依赖完成的任务
 */
function activateQueuedTasks() {
  console.log('🔗 Step 1: 检查 queued 任务依赖...');
  
  try {
    const output = execSync(`node ${SCRIPTS_DIR}/activate-queued-tasks.js`, { encoding: 'utf8' });
    console.log(output);
    
    // 解析输出，找出被激活的任务
    const activatedMatch = output.match(/(\d+) 个任务已激活/);
    if (activatedMatch && parseInt(activatedMatch[1]) > 0) {
      logEvent('queued_tasks_activated', { count: parseInt(activatedMatch[1]) });
    }
  } catch (error) {
    console.error('❌ 激活任务失败:', error.message);
    logEvent('activation_failed', { error: error.message });
  }
}

/**
 * Step 2: 安全扫描
 * 注意：只在任务有 review.next_instructions 时才需要扫描
 */
function scanTaskSecurity(taskId, task) {
  console.log(`🛡️ Step 2: 安全扫描 ${taskId}...`);
  
  // 检查是否有 review 字段（首次执行时没有）
  if (!task.review || !task.review.next_instructions) {
    console.log(`ℹ️ ${taskId} 没有审阅指令，跳过安全扫描（需要先审阅）`);
    return { safe: true, noInstructions: true };
  }
  
  try {
    const taskFile = path.join(TASKS_DIR, `${taskId}.json`);
    const output = execSync(`node ${SCRIPTS_DIR}/security-scan.js ${taskFile}`, { 
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe']
    });
    
    const result = JSON.parse(output);
    if (result.safe) {
      console.log(`✅ ${taskId} 安全扫描通过`);
      return { safe: true };
    } else {
      console.error(`❌ ${taskId} 发现危险命令:`, result.flags);
      logEvent('security_scan_failed', {
        task_id: taskId,
        flags: result.flags.map(f => f.reason)
      });
      return { safe: false, flags: result.flags };
    }
  } catch (error) {
    // 退出码 1 表示发现危险命令
    if (error.stdout) {
      try {
        const result = JSON.parse(error.stdout);
        if (!result.safe) {
          console.error(`❌ ${taskId} 发现危险命令:`, result.flags);
          logEvent('security_scan_failed', {
            task_id: taskId,
            flags: result.flags.map(f => f.reason)
          });
          return { safe: false, flags: result.flags };
        }
      } catch {}
    }
    console.error('❌ 安全扫描异常:', error.message);
    return { safe: false, error: error.message };
  }
}

/**
 * Step 3: Sonnet 审阅
 * 必须使用 Sonnet 模型，不能用 Qwen 替代
 * 
 * 流程：
 * 1. 调用 trigger-review.js 脚本，触发审阅
 * 2. 脚本会 spawn 一个 Sonnet 子 agent 进行审阅
 * 3. 审阅结果通过 apply-review.js 应用到任务文件
 */
async function reviewTask(task) {
  console.log(`🧠 Step 3: Sonnet 审阅 ${task.task_id}...`);
  
  logEvent('review_started', {
    task_id: task.task_id,
    current_iteration: task.current_iteration,
    model: 'aiberm/claude-sonnet-4-6'
  });
  
  // 调用 trigger-review.js 脚本
  // 这个脚本会：
  // 1. 将任务状态改为 reviewing
  // 2. 生成审阅 prompt
  // 3. 通过 OpenClaw 消息系统发送到 Wilson 会话（用 Sonnet 模型）
  
  try {
    const output = execSync(
      `node ${SCRIPTS_DIR}/trigger-review.js ${task.task_id}`,
      { encoding: 'utf8' }
    );
    
    console.log(output);
    
    // trigger-review.js 会输出审阅 prompt
    // 在实际部署中，这里应该自动发送到 Wilson 的 Discord 会话
    // 让 Wilson 用 Sonnet 模型审阅
    
    // 简化版本：返回提示，让心跳暂停等待人工触发
    // 完整版本：需要集成 OpenClaw 的消息系统
    
    console.log('⚠️ 需要人工触发 Sonnet 审阅');
    console.log('运行：node scripts/trigger-review.js ' + task.task_id);
    console.log('然后复制 prompt 到 Wilson 会话（用 Sonnet 模型）');
    
    return {
      pending: true,
      message: '等待 Sonnet 审阅',
      triggerScript: `node scripts/trigger-review.js ${task.task_id}`
    };
    
  } catch (error) {
    console.error('❌ 触发审阅失败:', error.message);
    logEvent('review_trigger_failed', {
      task_id: task.task_id,
      error: error.message
    });
    
    throw error;
  }
}

/**
 * Step 4: 更新任务状态
 */
function updateTaskAfterReview(task, review) {
  console.log(`📝 Step 4: 更新任务 ${task.task_id}...`);
  
  const oldStatus = task.status;
  task.review = review;
  task.updated_at = new Date().toISOString();
  
  // 根据 verdict 更新状态
  if (review.verdict === 'complete') {
    task.status = 'completed';
    task.completed_at = task.updated_at;
  } else if (review.verdict === 'reject') {
    task.current_iteration = (task.current_iteration || 0) + 1;
    if (task.current_iteration >= task.max_iterations) {
      task.status = 'failed';
    } else {
      task.status = 'pending'; // 重新执行
    }
  } else {
    // approve 或 revise
    task.status = 'reviewed';
  }
  
  // 记录到 history
  task.history = task.history || [];
  task.history.push({
    timestamp: task.updated_at,
    action: 'review_completed',
    verdict: review.verdict,
    confidence: review.confidence,
    feedback: review.feedback
  });
  
  writeTask(task);
  
  logEvent('review_completed', {
    task_id: task.task_id,
    from: oldStatus,
    to: task.status,
    verdict: review.verdict
  });
  
  console.log(`✅ ${task.task_id} 状态更新：${oldStatus} → ${task.status}`);
}

/**
 * 主流程
 */
async function heartbeat() {
  console.log('🫀 Wilson 心跳开始...');
  console.log('='.repeat(50));
  
  logEvent('heartbeat_started', { agent: 'wilson' });
  
  try {
    // Step 1: 激活依赖完成的任务
    activateQueuedTasks();
    
    // Step 2 & 3 & 4: 处理 pending 任务
    const taskIds = listTasks();
    let processedCount = 0;
    
    for (const taskId of taskIds) {
      const task = readTask(taskId);
      if (!task) continue;
      
      // 只处理 pending 状态
      if (task.status !== 'pending') {
        continue;
      }
      
      // 尝试获取锁
      if (!acquireLock(taskId)) {
        console.log(`⏳ ${taskId} 已锁定，跳过`);
        continue;
      }
      
      try {
        // Step 2: 安全扫描（只在有 review.next_instructions 时扫描）
        const security = scanTaskSecurity(taskId, task);
        
        // 如果没有指令（首次执行），跳过安全扫描直接审阅
        if (!security.noInstructions && !security.safe) {
          // 发现危险命令，标记为 blocked
          task.status = 'blocked';
          task.blocked_at = new Date().toISOString();
          task.blocked_reason = '安全扫描失败';
          task.blocked_flags = security.flags;
          writeTask(task);
          
          logEvent('task_blocked', {
            task_id: taskId,
            reason: 'security_scan_failed',
            flags: security.flags
          });
          
          console.log(`❌ ${taskId} 因安全问题被 blocked`);
          continue;
        }
        
        // Step 3: Sonnet 审阅
        const review = await reviewTask(task);
        
        // 如果审阅是异步的（pending），不更新状态，等待 apply-review.js
        if (review.pending) {
          console.log(`⏳ ${taskId} 等待 Sonnet 审阅结果`);
          console.log(`   运行：${review.triggerScript}`);
          // 不增加 processedCount，因为还没完成
        } else {
          // Step 4: 更新任务状态
          updateTaskAfterReview(task, review);
          processedCount++;
        }
        
      } finally {
        // 释放锁
        releaseLock(taskId);
      }
    }
    
    console.log('='.repeat(50));
    console.log(`🫀 Wilson 心跳完成，处理 ${processedCount} 个任务`);
    
    logEvent('heartbeat_completed', {
      processed: processedCount,
      agent: 'wilson'
    });
    
    if (processedCount === 0) {
      console.log('✅ 没有需要处理的任务');
      return 'HEARTBEAT_OK';
    } else {
      return `✅ 处理 ${processedCount} 个任务`;
    }
    
  } catch (error) {
    console.error('❌ 心跳异常:', error);
    logEvent('heartbeat_failed', { error: error.message });
    return `❌ 心跳失败：${error.message}`;
  }
}

// 命令行执行
if (require.main === module) {
  heartbeat().then(result => {
    console.log(result);
    process.exit(0);
  }).catch(error => {
    console.error(error);
    process.exit(1);
  });
}

module.exports = { heartbeat, activateQueuedTasks, scanTaskSecurity, reviewTask };
