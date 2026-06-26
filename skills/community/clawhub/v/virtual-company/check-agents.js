#!/usr/bin/env node

/**
 * Virtual Company - 自动重建检测脚本
 * 检查子代理是否失效，失效则自动重建并注入记忆
 * 
 * 用法：
 *   node check-agents.js check      # 检查所有子代理状态
 *   node check-agents.js repair     # 检查并修复失效的子代理
 *   node check-agents.js status     # 显示状态摘要
 */

const fs = require('fs');
const path = require('path');

const SKILL_DIR = __dirname;
const OFFICE_STATE_FILE = path.join(SKILL_DIR, 'office-state.json');
const MEMORY_ROOT = path.join(process.env.HOME || process.env.USERPROFILE, '.agent-memory', 'virtual-company');

/**
 * 加载办公室状态
 */
function loadOfficeState() {
  if (fs.existsSync(OFFICE_STATE_FILE)) {
    return JSON.parse(fs.readFileSync(OFFICE_STATE_FILE, 'utf8'));
  }
  return { version: '2.0.0', offices: {} };
}

/**
 * 保存办公室状态
 */
function saveOfficeState(state) {
  state.updatedAt = new Date().toISOString();
  fs.writeFileSync(OFFICE_STATE_FILE, JSON.stringify(state, null, 2));
}

/**
 * 加载成员记忆
 */
function loadMemberMemory(teamName, officeName) {
  const memoryFile = path.join(MEMORY_ROOT, teamName, officeName, 'member.json');
  if (fs.existsSync(memoryFile)) {
    return JSON.parse(fs.readFileSync(memoryFile, 'utf8'));
  }
  return null;
}

/**
 * 构建记忆上下文（用于注入）
 */
function buildMemoryContext(memory, task) {
  if (!memory) return task;
  
  let context = `## 🧠 记忆上下文\n\n`;
  
  if (memory.tasks?.length > 0) {
    context += `### 历史任务 (${memory.tasks.length}个)\n`;
    memory.tasks.slice(-5).forEach(t => {
      context += `- ${t.description || t.name} (${t.status || '完成'})\n`;
    });
    context += `\n`;
  }
  
  if (memory.experiences?.length > 0) {
    context += `### 经验积累 (${memory.experiences.length}条)\n`;
    memory.experiences.slice(-5).forEach(e => {
      context += `- ${e.insight || e.description}\n`;
    });
    context += `\n`;
  }
  
  context += `## 🎭 当前角色\n`;
  context += `你是${memory.role}，隶属于${memory.team}。\n`;
  context += `模型：${memory.model}\n\n`;
  
  context += `## 📋 当前任务\n`;
  context += `${task}\n`;
  
  return context;
}

/**
 * 检查子代理是否有效
 * 注意：这个函数需要在 OpenClaw 环境中运行才能调用 sessions_send
 * 这里只是生成检查命令
 */
function checkAgentStatus(officeName, sessionKey) {
  console.log(`\n📋 检查: ${officeName}`);
  console.log(`   SessionKey: ${sessionKey}`);
  
  // 生成检查命令
  const checkCommand = {
    tool: 'sessions_send',
    params: {
      sessionKey: sessionKey,
      message: 'PING'
    },
    timeout: 5000,
    expectSuccess: true
  };
  
  console.log(`   检查命令: sessions_send(sessionKey="${sessionKey}", message="PING")`);
  
  return checkCommand;
}

/**
 * 生成重建命令
 */
function generateRepairCommand(officeName, memory, task = '等待任务') {
  if (!memory) {
    console.log(`   ⚠️ 没有找到记忆文件，无法重建`);
    return null;
  }
  
  const context = buildMemoryContext(memory, task);
  
  const repairCommand = {
    tool: 'sessions_spawn',
    params: {
      label: `${memory.team} - ${officeName}`,
      model: memory.model,
      mode: 'session',
      thread: true,
      task: context
    }
  };
  
  console.log(`   🔄 重建命令:`);
  console.log(`      sessions_spawn(`);
  console.log(`        label: "${memory.team} - ${officeName}",`);
  console.log(`        model: "${memory.model}",`);
  console.log(`        mode: "session",`);
  console.log(`        thread: true,`);
  console.log(`        task: "<记忆上下文 + 当前任务>"`);
  console.log(`      )`);
  
  return repairCommand;
}

/**
 * 检查所有办公室状态
 */
function checkAllOffices() {
  console.log('\n🔍 检查所有办公室状态...\n');
  console.log('━'.repeat(60));
  
  const state = loadOfficeState();
  const offices = state.offices || {};
  
  if (Object.keys(offices).length === 0) {
    console.log('⚠️ 没有找到任何办公室记录');
    console.log('💡 运行 "node spawn.js init-all" 初始化');
    return;
  }
  
  let validCount = 0;
  let invalidCount = 0;
  
  for (const [officeName, sessionKey] of Object.entries(offices)) {
    const checkCmd = checkAgentStatus(officeName, sessionKey);
    
    // 模拟检查结果（实际需要 OpenClaw 环境）
    // 这里我们假设需要用户手动确认
    console.log(`   状态: ⏳ 待确认（需要 OpenClaw 环境）`);
    
    // 尝试加载记忆
    const parts = officeName.split(' - ');
    if (parts.length >= 2) {
      const teamName = parts[0];
      const memberOffice = parts[1];
      const memory = loadMemberMemory(teamName, memberOffice);
      
      if (memory) {
        console.log(`   📚 记忆: ${memory.tasks?.length || 0}个任务, ${memory.experiences?.length || 0}条经验`);
      } else {
        console.log(`   📚 记忆: 无`);
      }
    }
    
    console.log('');
  }
  
  console.log('━'.repeat(60));
  console.log(`\n💡 提示：实际检查需要在 OpenClaw 环境中进行`);
  console.log(`   如果子代理失效，会自动调用 generateRepairCommand 重建`);
}

/**
 * 显示状态摘要
 */
function showStatus() {
  console.log('\n📊 虚拟公司状态摘要\n');
  console.log('━'.repeat(60));
  
  // 检查记忆目录
  if (fs.existsSync(MEMORY_ROOT)) {
    const teams = fs.readdirSync(MEMORY_ROOT);
    let totalOffices = 0;
    let totalTasks = 0;
    let totalExperiences = 0;
    
    teams.forEach(team => {
      const teamPath = path.join(MEMORY_ROOT, team);
      if (fs.statSync(teamPath).isDirectory() && team !== 'shared') {
        const offices = fs.readdirSync(teamPath);
        offices.forEach(office => {
          const officePath = path.join(teamPath, office);
          if (fs.statSync(officePath).isDirectory() && office !== 'shared') {
            const memberFile = path.join(officePath, 'member.json');
            if (fs.existsSync(memberFile)) {
              const memory = JSON.parse(fs.readFileSync(memberFile, 'utf8'));
              totalOffices++;
              totalTasks += memory.tasks?.length || 0;
              totalExperiences += memory.experiences?.length || 0;
            }
          }
        });
      }
    });
    
    console.log(`🧠 记忆系统:`);
    console.log(`   办公室数量: ${totalOffices}`);
    console.log(`   总任务记录: ${totalTasks}`);
    console.log(`   总经验积累: ${totalExperiences}`);
  } else {
    console.log(`🧠 记忆系统: 未初始化`);
    console.log(`   💡 运行 "node spawn.js init-all" 初始化`);
  }
  
  // 检查 office-state.json
  if (fs.existsSync(OFFICE_STATE_FILE)) {
    const state = loadOfficeState();
    const officeCount = Object.keys(state.offices || {}).length;
    console.log(`\n📋 子代理状态:`);
    console.log(`   已记录子代理: ${officeCount}`);
    console.log(`   最后更新: ${state.updatedAt || '未知'}`);
  } else {
    console.log(`\n📋 子代理状态: 未创建`);
  }
  
  console.log('\n' + '━'.repeat(60));
}

/**
 * 生成修复脚本
 */
function generateRepairScript() {
  console.log('\n🔧 生成修复脚本...\n');
  
  const state = loadOfficeState();
  const offices = state.offices || {};
  const repairs = [];
  
  for (const [officeName, sessionKey] of Object.entries(offices)) {
    const parts = officeName.split(' - ');
    if (parts.length >= 2) {
      const teamName = parts[0];
      const memberOffice = parts[1];
      const memory = loadMemberMemory(teamName, memberOffice);
      
      if (memory) {
        repairs.push({
          officeName,
          teamName,
          memberOffice,
          memory,
          oldSessionKey: sessionKey
        });
      }
    }
  }
  
  console.log(`发现 ${repairs.length} 个办公室需要检查/修复\n`);
  
  // 生成修复命令列表
  console.log('修复命令列表（复制到 OpenClaw 环境执行）:\n');
  console.log('```javascript');
  repairs.forEach(r => {
    console.log(`// ${r.officeName}`);
    console.log(`// 如果 sessions_send("${r.oldSessionKey}", "PING") 失败，则执行：`);
    console.log(`sessions_spawn({`);
    console.log(`  label: "${r.teamName} - ${r.memberOffice}",`);
    console.log(`  model: "${r.memory.model}",`);
    console.log(`  mode: "session",`);
    console.log(`  thread: true,`);
    console.log(`  task: "<注入记忆>"`);
    console.log(`});`);
    console.log('');
  });
  console.log('```');
}

// 主函数
function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'status';
  
  switch (command) {
    case 'check':
      checkAllOffices();
      break;
      
    case 'repair':
      generateRepairScript();
      break;
      
    case 'status':
      showStatus();
      break;
      
    default:
      console.log('用法:');
      console.log('  node check-agents.js check    # 检查所有子代理状态');
      console.log('  node check-agents.js repair   # 生成修复脚本');
      console.log('  node check-agents.js status   # 显示状态摘要');
  }
}

main();