#!/usr/bin/env node
/**
 * 任务检测 + 主动思考脚本
 * 自动扫描任务状态，识别异常，生成解决方案
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = '/Users/openclaw/.openclaw/workspace';
const MEMORY_DIR = path.join(WORKSPACE, 'memory');

/**
 * 主检测函数
 */
async function detectAndThink() {
  console.log('🔍 启动任务检测 + 主动思考...\n');
  
  const now = new Date();
  const alerts = [];
  const thinkingLogs = [];
  
  // 1. 扫描 HEARTBEAT.md
  console.log('📋 扫描 HEARTBEAT.md...');
  const heartbeatTasks = parseHeartbeatTasks();
  
  for (const task of heartbeatTasks) {
    // 检测停滞任务
    if (task.status === 'Active' && isStale(task.lastUpdate, 24)) {
      const analysis = analyzeStalledTask(task);
      alerts.push({
        type: 'stalled',
        severity: 'high',
        task,
        analysis
      });
      thinkingLogs.push(generateThinkingLog('stalled', task, analysis));
    }
    
    // 检测待确认阻塞
    if (task.status === 'Waiting' && !task.blockReason) {
      alerts.push({
        type: 'blocking_unconfirmed',
        severity: 'medium',
        task,
        analysis: { reason: '阻塞原因未填写' }
      });
    }
    
    // 检测超期任务
    if (task.status !== 'Done' && isOverdue(task.deadline)) {
      const analysis = analyzeOverdueTask(task);
      alerts.push({
        type: 'overdue',
        severity: 'high',
        task,
        analysis
      });
      thinkingLogs.push(generateThinkingLog('overdue', task, analysis));
    }
  }
  
  // 2. 扫描 WORKING.md
  console.log('📋 扫描 WORKING.md...');
  const workingTasks = parseWorkingTasks();
  
  for (const task of workingTasks) {
    // 检测依赖阻塞
    if (task.dependencies && task.status === 'Waiting') {
      const blockedBy = checkDependencyBlock(task, workingTasks);
      if (blockedBy.length > 0) {
        alerts.push({
          type: 'dependency_block',
          severity: 'medium',
          task,
          analysis: { blockedBy }
        });
      }
    }
    
    // 检测无进度任务
    if (task.status === 'Active' && task.progress === '0%' && isStale(task.lastUpdate, 48)) {
      alerts.push({
        type: 'no_progress',
        severity: 'medium',
        task,
        analysis: { reason: 'Active状态但48小时无进度' }
      });
    }
  }
  
  // 3. 尝试自动修复
  console.log('\n🔧 尝试自动修复...');
  const autoFixResults = await tryAutoFix(alerts);
  
  // 4. 写入检测结果
  console.log('\n📝 写入检测结果...');
  writeTaskAlerts(alerts, autoFixResults);
  writeThinkingLogs(thinkingLogs);
  
  // 5. 推送关键告警
  if (alerts.some(a => a.severity === 'high')) {
    console.log('\n🚨 发现关键告警，准备推送...');
    // 这里会调用 Feishu 推送
  }
  
  // 6. 输出摘要
  console.log('\n📊 检测摘要:');
  console.log(`   总任务: ${heartbeatTasks.length + workingTasks.length}`);
  console.log(`   异常任务: ${alerts.length}`);
  console.log(`   自动修复: ${autoFixResults.fixed.length}`);
  console.log(`   需人工: ${autoFixResults.manual.length}`);
  
  return { alerts, autoFixResults };
}

/**
 * 解析 HEARTBEAT.md 任务
 */
function parseHeartbeatTasks() {
  const content = fs.readFileSync(path.join(WORKSPACE, 'HEARTBEAT.md'), 'utf-8');
  const tasks = [];
  const lines = content.split('\n');
  let inTable = false;
  
  for (const line of lines) {
    if (line.includes('| 任务ID |')) {
      inTable = true;
      continue;
    }
    if (inTable && line.startsWith('|') && !line.includes('---')) {
      const cells = line.split('|').map(c => c.trim()).filter(c => c);
      if (cells.length >= 7 && cells[0] !== '任务ID') {
        tasks.push({
          id: cells[0],
          name: cells[1],
          status: cells[2],
          progress: cells[3],
          deadline: cells[4],
          lastUpdate: cells[5],
          blockReason: cells[6],
          source: 'HEARTBEAT'
        });
      }
    }
  }
  
  return tasks;
}

/**
 * 解析 WORKING.md 任务
 */
function parseWorkingTasks() {
  const content = fs.readFileSync(path.join(WORKSPACE, 'WORKING.md'), 'utf-8');
  const tasks = [];
  
  // 简单解析，匹配任务标题和属性
  const taskMatches = content.match(/### (T\d+):[\s\S]*?(?=### |$)/g) || [];
  
  taskMatches.forEach(match => {
    const id = match.match(/### (T\d+):/)?.[1];
    const status = match.match(/\*\*状态\*\*\s*\|\s*([^\n|]+)/)?.[1]?.trim();
    const progress = match.match(/\*\*进度\*\*\s*\|\s*([^\n|]+)/)?.[1]?.trim();
    const dependencies = match.match(/\*\*依赖项\*\*\s*\|\s*([^\n|]+)/)?.[1]?.trim();
    
    if (id) {
      tasks.push({
        id,
        status: status || 'Unknown',
        progress: progress || '0%',
        dependencies: dependencies ? dependencies.split(',').map(d => d.trim()) : [],
        source: 'WORKING'
      });
    }
  });
  
  return tasks;
}

/**
 * 判断是否停滞
 */
function isStale(lastUpdate, hours) {
  if (!lastUpdate) return true;
  const last = new Date(lastUpdate);
  const diff = (new Date() - last) / (1000 * 60 * 60);
  return diff > hours;
}

/**
 * 判断是否超期
 */
function isOverdue(deadline) {
  if (!deadline) return false;
  return new Date() > new Date(deadline);
}

/**
 * 分析停滞任务
 */
function analyzeStalledTask(task) {
  const reasons = [];
  const solutions = [];
  
  // 分析可能原因
  if (!task.lastUpdate) {
    reasons.push('无更新记录');
    solutions.push('检查任务是否已启动');
  }
  
  if (task.progress === '0%') {
    reasons.push('进度为0，可能未开始');
    solutions.push('确认任务优先级，是否需要分解');
  }
  
  if (task.blockReason) {
    reasons.push(`已知阻塞: ${task.blockReason}`);
    solutions.push('尝试自动解除阻塞，或升级处理');
  }
  
  // 生成3个方案
  return {
    reasons,
    solutions: [
      ...solutions,
      '更新任务状态为 Waiting（如需等待）',
      '分解任务为更小的子任务',
      '重新评估任务优先级和截止时间'
    ].slice(0, 3)
  };
}

/**
 * 分析超期任务
 */
function analyzeOverdueTask(task) {
  const progressNum = parseInt(task.progress) || 0;
  
  return {
    reasons: [
      `截止时间为 ${task.deadline}`,
      `当前进度 ${task.progress}`,
      progressNum < 50 ? '进度落后严重' : '接近完成'
    ],
    solutions: [
      progressNum > 80 ? '加急完成剩余工作' : '重新评估工作量，申请延期',
      '调整下游任务排期',
      '寻求资源支持或任务分解'
    ]
  };
}

/**
 * 检查依赖阻塞
 */
function checkDependencyBlock(task, allTasks) {
  const blockedBy = [];
  
  for (const depId of task.dependencies) {
    const depTask = allTasks.find(t => t.id === depId);
    if (depTask && depTask.status !== 'Done') {
      blockedBy.push(depId);
    }
  }
  
  return blockedBy;
}

/**
 * 生成思考日志
 */
function generateThinkingLog(type, task, analysis) {
  const timestamp = new Date().toISOString();
  
  return {
    timestamp,
    type,
    taskId: task.id,
    taskName: task.name,
    thinking: [
      `任务 ${task.id} (${task.name}) 标记为 ${type}`,
      `原因分析: ${analysis.reasons?.join(', ') || '待分析'}`,
      `解决方案:`,
      ...(analysis.solutions || []).map((s, i) => `  ${i + 1}. ${s}`)
    ].join('\n')
  };
}

/**
 * 尝试自动修复
 */
async function tryAutoFix(alerts) {
  const fixed = [];
  const manual = [];
  
  for (const alert of alerts) {
    let autoFixed = false;
    
    // 自动修复逻辑
    if (alert.type === 'dependency_block') {
      // 检查依赖是否已完成（从其他来源）
      autoFixed = false; // 需要人工确认
    }
    
    if (alert.type === 'blocking_unconfirmed') {
      // 尝试从记忆中查找阻塞原因
      autoFixed = false;
    }
    
    if (autoFixed) {
      fixed.push(alert);
    } else {
      manual.push(alert);
    }
  }
  
  return { fixed, manual };
}

/**
 * 写入任务告警
 */
function writeTaskAlerts(alerts, autoFixResults) {
  const hotDir = path.join(MEMORY_DIR, 'hot');
  if (!fs.existsSync(hotDir)) {
    fs.mkdirSync(hotDir, { recursive: true });
  }
  
  const content = [
    '# 任务告警',
    `**生成时间**: ${new Date().toISOString()}`,
    '',
    `## 异常任务 (${alerts.length})`,
    ''
  ];
  
  const grouped = {
    high: alerts.filter(a => a.severity === 'high'),
    medium: alerts.filter(a => a.severity === 'medium')
  };
  
  if (grouped.high.length > 0) {
    content.push('### 🔴 高优先级');
    grouped.high.forEach(a => {
      content.push(`- **${a.task.id}**: ${a.task.name} (${a.type})`);
      if (a.analysis?.reasons) {
        content.push(`  原因: ${a.analysis.reasons.join(', ')}`);
      }
    });
    content.push('');
  }
  
  if (grouped.medium.length > 0) {
    content.push('### 🟡 中优先级');
    grouped.medium.forEach(a => {
      content.push(`- **${a.task.id}**: ${a.task.name} (${a.type})`);
    });
    content.push('');
  }
  
  content.push(`## 自动修复结果`);
  content.push(`- 自动修复: ${autoFixResults.fixed.length}`);
  content.push(`- 需人工: ${autoFixResults.manual.length}`);
  
  fs.writeFileSync(path.join(hotDir, 'task-alert.md'), content.join('\n'));
}

/**
 * 写入思考日志
 */
function writeThinkingLogs(logs) {
  const hotDir = path.join(MEMORY_DIR, 'hot');
  if (!fs.existsSync(hotDir)) {
    fs.mkdirSync(hotDir, { recursive: true });
  }
  
  const content = [
    '# 思考日志',
    `**生成时间**: ${new Date().toISOString()}`,
    '',
    ...logs.map(log => [
      `## ${log.timestamp}`,
      log.thinking,
      ''
    ].join('\n'))
  ];
  
  fs.appendFileSync(path.join(hotDir, 'thinking-log.md'), content.join('\n') + '\n---\n');
}

// 运行
detectAndThink().catch(console.error);
