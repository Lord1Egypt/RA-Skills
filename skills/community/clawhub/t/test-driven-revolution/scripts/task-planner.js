#!/usr/bin/env node
/**
 * task-planner.js - 任务规划器（Sonnet 版）
 * 
 * 用法：
 *   node scripts/task-planner.js "需求描述"
 *   node scripts/task-planner.js --create plan-result.json
 * 
 * 固定使用 Sonnet 进行任务拆解
 */

const fs = require('fs');
const path = require('path');

const SCRIPTS_DIR = __dirname;
const EVOLUTION_DIR = path.join(SCRIPTS_DIR, '..');
const TASKS_DIR = path.join(EVOLUTION_DIR, 'tasks');
const LOGS_DIR = path.join(EVOLUTION_DIR, 'logs');
const EVENTS_LOG = path.join(LOGS_DIR, 'events.log');

// 确保目录存在
[TASKS_DIR, LOGS_DIR].forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
});

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
 * 生成任务 ID
 */
function generateTaskId() {
  const existing = fs.readdirSync(TASKS_DIR)
    .filter(f => f.startsWith('task-') && f.endsWith('.json'))
    .map(f => parseInt(f.replace('task-', '').replace('.json', '')))
    .filter(n => !isNaN(n));
  
  const nextId = existing.length > 0 ? Math.max(...existing) + 1 : 1;
  return `task-${String(nextId).padStart(3, '0')}`;
}

const args = process.argv.slice(2);

// --create 模式：从 JSON 文件创建任务
if (args.includes('--create')) {
  const fileIndex = args.indexOf('--create');
  const planFile = args[fileIndex + 1];
  
  if (!planFile) {
    console.error('❌ 缺少文件名');
    process.exit(1);
  }
  
  try {
    const plan = JSON.parse(fs.readFileSync(planFile, 'utf8'));
    const taskId = generateTaskId();
    
    const task = {
      task_id: taskId,
      title: plan.title,
      description: plan.description,
      status: 'pending',
      depends_on: [],
      current_subtask: 0,
      current_iteration: 0,
      max_iterations: (plan.estimated_iterations || 3) + 2,
      subtasks: plan.subtasks,
      reference_files: plan.reference_files || [],
      complexity_score: plan.complexity_score || 5,
      requires_audit: plan.requires_audit !== false,
      review_tier: plan.review_tier || 'sonnet',
      risk_assessment: plan.risk_assessment,
      acceptance_criteria: plan.acceptance_criteria || [],
      history: [],
      created_at: new Date().toISOString(),
      planner: {
        model: 'aiberm/claude-sonnet-4-6',
        planned_at: new Date().toISOString()
      }
    };
    
    const taskFile = path.join(TASKS_DIR, `${taskId}.json`);
    fs.writeFileSync(taskFile, JSON.stringify(task, null, 2));
    
    logEvent('task_planned', {
      task_id: taskId,
      complexity: plan.complexity_score,
      subtasks_count: plan.subtasks.length,
      model: 'aiberm/claude-sonnet-4-6'
    });
    
    console.log(`✅ 任务已创建：${taskId}`);
    console.log(`   标题：${plan.title}`);
    console.log(`   子任务：${plan.subtasks.length} 个`);
    console.log(`   复杂度：${plan.complexity_score}/10`);
    console.log('');
    console.log('下一步：运行 Wilson 心跳开始执行');
    console.log('  node scripts/heartbeat-coordinator.js');
    
    process.exit(0);
    
  } catch (error) {
    console.error('❌ 创建失败:', error.message);
    process.exit(1);
  }
}

// 规划模式
const requirement = args.join(' ');

if (!requirement) {
  console.log('用法：');
  console.log('  node scripts/task-planner.js "需求描述"');
  console.log('  node scripts/task-planner.js --create plan-result.json');
  console.log('');
  console.log('流程：');
  console.log('1. 运行：node scripts/task-planner.js "需求"');
  console.log('2. 复制 Prompt 到 Sonnet 会话（aiberm/claude-sonnet-4-6）');
  console.log('3. 保存 Sonnet 返回的 JSON');
  console.log('4. 运行：node scripts/task-planner.js --create result.json');
  process.exit(0);
}

console.log('🎯 任务规划器（Sonnet 版）');
console.log('='.repeat(50));
console.log(`需求：${requirement}`);
console.log('='.repeat(50));
console.log('');

// 生成规划 Prompt
const prompt = `你是 TDR 系统的任务规划师。请将以下需求拆解成可执行的 subtasks。

## 用户需求
${requirement}

## 规划要求

### 1. 分析需求
- 核心目标是什么？
- 需要哪些技术栈？
- 有什么潜在风险？

### 2. 拆解 subtasks
- 每个 subtask 应该是独立的、可测试的
- 按依赖顺序排列
- 每个 subtask 完成时间不超过 5 分钟
- 使用中文描述

### 3. 评估复杂度
- 1-10 分（1=简单配置，10=复杂系统）
- 预计迭代轮次

### 4. 输出格式（严格 JSON，不要 markdown 包裹）
{
  "title": "任务标题",
  "description": "详细描述",
  "subtasks": [
    "Subtask 1: 具体、可执行的动作",
    "Subtask 2: ...",
    "Subtask 3: ..."
  ],
  "reference_files": [],
  "complexity_score": 5,
  "estimated_iterations": 3,
  "requires_audit": true,
  "review_tier": "sonnet",
  "risk_assessment": {
    "level": "low|medium|high",
    "notes": "风险评估说明"
  },
  "acceptance_criteria": [
    "验收标准 1",
    "验收标准 2"
  ]
}
`;

logEvent('planning_started', {
  requirement,
  model: 'aiberm/claude-sonnet-4-6'
});

console.log('📋 规划 Prompt（复制到 Sonnet 会话）：');
console.log('-'.repeat(50));
console.log(prompt);
console.log('-'.repeat(50));
console.log('');
console.log('下一步：');
console.log('1. 复制上面的 Prompt');
console.log('2. 在 Wilson 会话中发送，使用 aiberm/claude-sonnet-4-6 模型');
console.log('3. 保存 Sonnet 返回的 JSON 到文件（如 plan-result.json）');
console.log('4. 运行：node scripts/task-planner.js --create plan-result.json');
console.log('');

// 保存 Prompt 到临时文件
const tempFile = path.join(EVOLUTION_DIR, 'temp-plan-prompt.txt');
fs.writeFileSync(tempFile, prompt);
console.log(`📝 Prompt 已保存到：${tempFile}`);
