#!/usr/bin/env node
/**
 * trigger-review.js - 触发 Sonnet 审阅
 * 
 * 用法：node trigger-review.js <task-id>
 * 
 * 这个脚本不直接审阅，而是发送消息到 Wilson 的会话，
 * 让 Wilson 用 Sonnet 模型进行审阅。
 */

const fs = require('fs');
const path = require('path');

const TASKS_DIR = path.join(__dirname, '..', 'tasks');
const LOGS_DIR = path.join(__dirname, '..', 'logs');
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

// 主程序
const taskId = process.argv[2];

if (!taskId) {
  console.log('用法：node trigger-review.js <task-id>');
  console.log('');
  console.log('示例：');
  console.log('  node trigger-review.js task-010');
  console.log('');
  console.log('这个脚本会：');
  console.log('1. 将任务状态改为 reviewing');
  console.log('2. 记录事件日志');
  console.log('3. 输出审阅 Prompt（需要人工复制到 Wilson 会话）');
  process.exit(0);
}

const task = readTask(taskId);

if (!task) {
  console.error(`❌ 任务不存在：${taskId}`);
  process.exit(1);
}

console.log(`🧠 触发 Sonnet 审阅：${taskId}`);
console.log('='.repeat(50));

// 更新任务状态
task.status = 'reviewing';
task.updated_at = new Date().toISOString();
writeTask(task);

logEvent('review_started', {
  task_id: taskId,
  model: 'aiberm/claude-sonnet-4-6',
  triggered_by: 'trigger-review.js'
});

// 生成审阅 Prompt
const prompt = `你是 Revolution 系统审阅员。请审阅以下任务的执行结果。

## 任务信息
\`\`\`json
${JSON.stringify(task, null, 2)}
\`\`\`

## 审阅要求

### 1. 读取所有 reference_files，理解上下文

### 2. 评估执行结果
- 是否达到 subtask 目标？
- 代码质量如何？
- 测试是否通过？

### 3. 判断 verdict
- **approve**: 执行成功，继续下一个 subtask
- **revise**: 需要修改，但不是致命错误
- **reject**: 执行完全错误，需要重新理解任务
- **complete**: 所有 subtasks 完成，任务可以结束

### 4. 输出格式（严格 JSON，不要 markdown 包裹）
{
  "verdict": "approve|revise|reject|complete",
  "confidence": 0.0-1.0,
  "feedback": "审阅意见",
  "next_instructions": "详细的下一步执行指令（如果 verdict=approve/revise）",
  "acceptance_criteria": ["验收标准 1", "验收标准 2"],
  "risk_flags": [],
  "technical_review": "技术选型审查说明"
}

如果 verdict 是 revise/reject，请在 feedback 中说明需要修改什么。`;

console.log('');
console.log('📋 审阅 Prompt（复制到 Wilson 会话，用 Sonnet 模型）：');
console.log('='.repeat(50));
console.log(prompt);
console.log('='.repeat(50));
console.log('');
console.log('✅ 任务状态已更新：pending → reviewing');
console.log('');
console.log('下一步（3 种方式）：');
console.log('');
console.log('方式 1：自动（推荐）- 用 sessions_spawn 调用 Sonnet，然后自动应用结果');
console.log('  在 Wilson 会话中：');
console.log('  sessions_spawn({');
console.log('    task: `<上面的 prompt>`,');
console.log('    model: "aiberm/claude-sonnet-4-6",');
console.log('    mode: "run"');
console.log('  })');
console.log('  然后用 apply-review.js 应用结果');
console.log('');
console.log('方式 2：手动 - 复制 Prompt 到 Wilson 会话，保存结果为 JSON 文件');
console.log('  1. 复制上面的 Prompt');
console.log('  2. 在 Wilson 会话中发送（确保用 aiberm/claude-sonnet-4-6 模型）');
console.log('  3. 保存 Sonnet 返回的 JSON 到 review-result.json');
console.log('  4. 运行：node scripts/apply-review.js ' + taskId + ' --file review-result.json');
console.log('');
console.log('方式 3：管道 - 从 stdin 读取 JSON');
console.log('  cat review-result.json | node scripts/apply-review.js ' + taskId + ' --stdin');
