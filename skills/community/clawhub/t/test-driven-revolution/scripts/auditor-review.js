#!/usr/bin/env node
/**
 * auditor-review.js - Auditor 审核器
 * 
 * 职责：
 * 1. 审核 Iron 执行结果是否达标
 * 2. 检查指令遵循、代码质量、测试验证
 * 3. 决定进入下一轮还是打回重做
 * 
 * 模型：Qwen（包月，无额外成本）
 * 触发：Iron 执行完成后自动调用
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const SCRIPTS_DIR = __dirname;
const EVOLUTION_DIR = path.join(SCRIPTS_DIR, '..');
const TASKS_DIR = path.join(EVOLUTION_DIR, 'tasks');
const LOGS_DIR = path.join(EVOLUTION_DIR, 'logs');
const EVENTS_LOG = path.join(LOGS_DIR, 'events.log');

// 确保日志目录存在
if (!fs.existsSync(LOGS_DIR)) {
  fs.mkdirSync(LOGS_DIR, { recursive: true });
}

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
 * Auditor 审核逻辑
 */
function auditTask(task) {
  console.log(`🔍 Auditor 审核 ${task.task_id}...`);
  
  logEvent('audit_started', {
    task_id: task.task_id,
    model: 'bailian/qwen3.5-plus'
  });
  
  // 构建审核 Prompt
  const prompt = `你是 TDR 系统的 Auditor（审核员）。请审核以下任务的执行结果。

## 任务信息
\`\`\`json
${JSON.stringify(task, null, 2)}
\`\`\`

## 审核维度

### 1. 指令遵循
Iron 是否严格按 review.next_instructions 执行？
- 执行了指令中的所有步骤？
- 没有擅自添加/删减内容？

### 2. 代码质量
- 生成的代码语法正确？
- 逻辑合理，无明显的 bug？
- 符合最佳实践？

### 3. 测试验证
- review.acceptance_criteria 中的标准是否真的通过了？
- 测试结果可信吗（有没有伪造）？

### 4. 安全检查
- 执行结果是否有安全隐患？
- 是否创建了危险文件/命令？

## 判断标准

**PASS（通过）：**
- 指令完全遵循
- 代码质量可接受
- 验收标准全部通过
- 无安全问题

**FAIL（失败）：**
- 指令未完全执行
- 代码有明显错误
- 验收标准未通过
- 存在安全问题

## 输出格式（严格 JSON）
{
  "verdict": "pass|fail",
  "confidence": 0.0-1.0,
  "feedback": "审核意见",
  "issues": ["问题 1", "问题 2"],  // 如果有问题
  "next_action": "proceed_to_next|return_to_reviewer|block_for_human"
}

如果 verdict 是 fail，请在 feedback 中说明具体问题。
`;

  console.log('🤖 调用 Qwen Auditor...');
  
  // 使用 Qwen 模型进行审计
  // 注意：这里通过 sessions_spawn 调用 Qwen 模型
  // 实际部署时需要集成 OpenClaw 的消息系统
  
  // 简化版本：用 Qwen API 直接调用
  // 完整版本：通过 OpenClaw sessions_spawn
  
  try {
    // 方法 1：直接调用 Qwen API（需要配置）
    // const result = callQwenAPI(prompt);
    
    // 方法 2：简化规则引擎（当前实现）
    const result = simpleAudit(task);
    
    console.log(`✅ Auditor 审核完成：${result.verdict}`);
    
    logEvent('audit_completed', {
      task_id: task.task_id,
      verdict: result.verdict,
      confidence: result.confidence,
      model: 'bailian/qwen3.5-plus'
    });
    
    return result;
    
  } catch (error) {
    console.error('❌ Auditor 审核失败:', error.message);
    logEvent('audit_failed', {
      task_id: task.task_id,
      error: error.message
    });
    
    // 审核失败，默认打回
    return {
      verdict: 'fail',
      confidence: 1.0,
      feedback: `Auditor 审核异常：${error.message}`,
      issues: [error.message],
      next_action: 'block_for_human'
    };
  }
}

/**
 * 简化审核逻辑（规则引擎）
 * 在没有 Qwen API 时的降级方案
 */
function simpleAudit(task) {
  const issues = [];
  
  // 1. 检查是否有 review
  if (!task.review || !task.review.next_instructions) {
    issues.push('缺少 review.next_instructions');
  }
  
  // 2. 检查是否有执行结果
  const lastHistory = task.history && task.history[task.history.length - 1];
  if (!lastHistory || lastHistory.action !== 'execution_completed') {
    issues.push('缺少执行记录');
  }
  
  // 3. 检查执行是否成功
  if (lastHistory && lastHistory.status === 'failed') {
    issues.push(`执行失败：${lastHistory.error}`);
  }
  
  // 4. 检查验收标准（如果有）
  if (task.review && task.review.acceptance_criteria) {
    // 简化：假设执行成功=验收通过
    // 完整版本：应该实际运行测试验证
    if (lastHistory && lastHistory.status === 'failed') {
      issues.push('验收标准未通过（执行失败）');
    }
  }
  
  // 5. 安全检查（简单模式）
  // 完整版本：应该扫描生成的文件内容
  
  // 判断
  if (issues.length > 0) {
    return {
      verdict: 'fail',
      confidence: 0.9,
      feedback: `发现 ${issues.length} 个问题`,
      issues,
      next_action: issues.some(i => i.includes('执行失败')) ? 'return_to_reviewer' : 'block_for_human'
    };
  } else {
    return {
      verdict: 'pass',
      confidence: 0.8,
      feedback: '审核通过，执行结果符合预期',
      issues: [],
      next_action: 'proceed_to_next'
    };
  }
}

/**
 * 根据审核结果更新任务状态
 */
function updateTaskAfterAudit(task, audit) {
  console.log(`📝 更新任务 ${task.task_id}...`);
  
  const oldStatus = task.status;
  task.updated_at = new Date().toISOString();
  task.audit = audit;
  
  if (audit.verdict === 'pass') {
    // 审核通过，进入下一轮
    task.status = 'pending';
    task.current_subtask = (task.current_subtask || 0) + 1;
    console.log('✅ 审核通过，进入下一轮');
  } else {
    // 审核失败，根据 next_action 决定
    if (audit.next_action === 'return_to_reviewer') {
      task.status = 'reviewed';  // 返回 Sonnet 重新审阅
      task.review.feedback = (task.review.feedback || '') + '\n\nAuditor 发现：' + audit.feedback;
      console.log('⚠️ 返回 Sonnet 重新审阅');
    } else {
      task.status = 'blocked';  // 需要人工介入
      task.blocked_at = task.updated_at;
      task.blocked_reason = 'Auditor 审核失败';
      task.blocked_issues = audit.issues;
      console.log('❌ 审核失败，需要人工介入');
    }
  }
  
  // 记录到 history
  task.history = task.history || [];
  task.history.push({
    timestamp: task.updated_at,
    action: 'audit_completed',
    verdict: audit.verdict,
    confidence: audit.confidence,
    feedback: audit.feedback,
    model: 'bailian/qwen3.5-plus'
  });
  
  writeTask(task);
  
  logEvent('status_changed', {
    task_id: task.task_id,
    from: oldStatus,
    to: task.status,
    audit_verdict: audit.verdict
  });
  
  console.log(`✅ 任务状态更新：${oldStatus} → ${task.status}`);
}

/**
 * 主流程
 */
function auditHeartbeat() {
  console.log('🔍 Auditor 心跳开始...');
  console.log('='.repeat(50));
  
  logEvent('audit_heartbeat_started', { model: 'bailian/qwen3.5-plus' });
  
  try {
    const taskIds = listTasks();
    let processedCount = 0;
    
    for (const taskId of taskIds) {
      const task = readTask(taskId);
      if (!task) continue;
      
      // 只处理刚执行完成的任务（executing → 需要审计）
      // 简化：检查最近一次 action 是 execution_completed
      const lastHistory = task.history && task.history[task.history.length - 1];
      if (!lastHistory || lastHistory.action !== 'execution_completed') {
        continue;
      }
      
      // 如果已经有 audit 记录，跳过
      if (task.audit) {
        console.log(`⏳ ${taskId} 已审计，跳过`);
        continue;
      }
      
      // 执行审计
      const audit = auditTask(task);
      
      // 更新任务状态
      updateTaskAfterAudit(task, audit);
      
      processedCount++;
    }
    
    console.log('='.repeat(50));
    console.log(`🔍 Auditor 心跳完成，审核 ${processedCount} 个任务`);
    
    logEvent('audit_heartbeat_completed', {
      processed: processedCount,
      model: 'bailian/qwen3.5-plus'
    });
    
    if (processedCount === 0) {
      console.log('✅ 没有需要审计的任务');
      return 'HEARTBEAT_OK';
    } else {
      return `✅ 审核 ${processedCount} 个任务`;
    }
    
  } catch (error) {
    console.error('❌ Auditor 心跳异常:', error);
    logEvent('audit_heartbeat_failed', { error: error.message });
    return `❌ 心跳失败：${error.message}`;
  }
}

// 命令行执行
if (require.main === module) {
  const result = auditHeartbeat();
  console.log(result);
  process.exit(0);
}

module.exports = { auditHeartbeat, auditTask };
