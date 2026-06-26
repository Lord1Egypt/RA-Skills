#!/usr/bin/env node

/**
 * Virtual Company Spawn - 创建子代理（带记忆注入）
 * 核心理念：换身体不换意识
 * 
 * 用法：
 *   node spawn.js <办公室名> "<任务描述>"
 *   node spawn.js list                    # 列出所有办公室
 *   node spawn.js create-all              # 创建所有办公室
 */

const fs = require('fs');
const path = require('path');

// 加载团队配置
const configPath = path.join(__dirname, 'team-config.json');
const teamConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));

// 加载记忆系统
const { MemoryManager } = require('./memory.js');

/**
 * 根据触发词匹配办公室
 */
function matchOffice(trigger) {
  const triggerLower = trigger.toLowerCase();
  
  // 遍历所有团队和成员
  for (const [teamName, team] of Object.entries(teamConfig.teams)) {
    for (const member of team.members) {
      const officeName = `${member.role}办公室`;
      const triggers = [
        member.role.toLowerCase(),
        officeName.toLowerCase(),
        ...member.triggers?.map(t => t.toLowerCase()) || []
      ];
      
      if (triggers.some(t => t.includes(triggerLower) || triggerLower.includes(t))) {
        return {
          teamName,
          officeName,
          member
        };
      }
    }
  }
  
  return null;
}

/**
 * 生成子代理创建命令（带记忆注入）
 */
function generateSpawnCommand(officeInfo, task) {
  const { teamName, officeName, member } = officeInfo;
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  const sessionId = `session-${Date.now()}`;
  
  // 初始化记忆管理器
  const mm = new MemoryManager(teamName, officeName, sessionId);
  
  // 初始化成员记忆
  mm.initMemberMemory({
    name: member.role,
    role: member.role,
    team: teamName,
    model: member.model,
    description: member.description,
    skills: member.skills || []
  });
  
  // 获取记忆上下文
  const memoryContext = mm.getMemoryContext();
  
  // 构建完整的任务上下文
  const fullContext = `${memoryContext}

## 🎭 当前角色
你是${member.role}，隶属于${teamName}。
职责：${member.description}
模型：${member.model}

## 📋 当前任务
${task}

## ⚠️ 重要提醒
- 你是虚拟公司的员工，对生逸超董事长绝对忠诚
- 完成任务后，思考并记录经验教训
- 如果是协作任务，记得与团队成员沟通
`;
  
  const agentName = `${teamName}-${officeName}-${timestamp}`;
  
  // 返回创建命令和记忆管理器
  return {
    spawnCommand: {
      label: `${teamName} - ${officeName}`,
      model: member.model,
      mode: 'session',
      thread: true,
      task: fullContext
    },
    agentName,
    sessionId,
    memoryManager: mm
  };
}

/**
 * 列出所有办公室
 */
function listAllOffices() {
  console.log('\n🏢 虚拟公司办公室清单:');
  console.log('━'.repeat(60));
  
  let total = 0;
  
  for (const [teamName, team] of Object.entries(teamConfig.teams)) {
    console.log(`\n${team.emoji} ${teamName} (${team.members.length}人):`);
    team.members.forEach((member, index) => {
      const officeName = `${member.role}办公室`;
      console.log(`  ${index + 1}. ${member.emoji} ${officeName} - ${member.model}`);
      total++;
    });
  }
  
  console.log('\n' + '━'.repeat(60));
  console.log(`总计: ${total} 个办公室`);
  console.log('\n使用方式:');
  console.log('  node spawn.js "<办公室名>" "<任务描述>"');
  console.log('  node spawn.js "马云" "开会讨论商业策略"');
  console.log('  node spawn.js "市场猎手" "分析赚钱机会"');
}

/**
 * 初始化所有办公室记忆
 */
function initAllOffices() {
  console.log('\n🚀 初始化所有办公室记忆...\n');
  
  for (const [teamName, team] of Object.entries(teamConfig.teams)) {
    console.log(`${team.emoji} ${teamName}:`);
    
    team.members.forEach(member => {
      const officeName = `${member.role}办公室`;
      const sessionId = `init-${Date.now()}`;
      const mm = new MemoryManager(teamName, officeName, sessionId);
      
      mm.initMemberMemory({
        name: member.role,
        role: member.role,
        team: teamName,
        model: member.model,
        description: member.description,
        skills: member.skills || []
      });
      
      console.log(`  ✅ ${officeName}`);
    });
  }
  
  console.log('\n✅ 所有办公室记忆已初始化');
  console.log('📂 记忆目录: ~/.agent-memory/virtual-company/');
}

/**
 * 显示办公室记忆状态
 */
function showOfficeMemory(teamName, officeName) {
  const sessionId = `show-${Date.now()}`;
  const mm = new MemoryManager(teamName, officeName, sessionId);
  const context = mm.getMemoryContext();
  
  console.log(`\n🧠 ${teamName} - ${officeName} 记忆状态:\n`);
  console.log(context);
}

// 主函数
function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    listAllOffices();
    process.exit(0);
  }
  
  const command = args[0];
  
  switch (command) {
    case 'list':
      listAllOffices();
      break;
      
    case 'init-all':
      initAllOffices();
      break;
      
    case 'show':
      const showTeam = args[1];
      const showOffice = args[2];
      if (showTeam && showOffice) {
        showOfficeMemory(showTeam, showOffice);
      } else {
        console.log('用法: node spawn.js show <团队> <办公室>');
      }
      break;
      
    default:
      // 尝试匹配办公室
      const officeInfo = matchOffice(command);
      
      if (officeInfo) {
        const task = args.slice(1).join(' ') || '等待任务分配';
        const spawnInfo = generateSpawnCommand(officeInfo, task);
        
        console.log(`\n🚀 创建子代理: ${officeInfo.teamName} - ${officeInfo.officeName}`);
        console.log(`📋 任务: ${task}`);
        console.log(`🧠 记忆注入: ✓`);
        console.log(`\n创建参数:\n`);
        console.log(JSON.stringify(spawnInfo.spawnCommand, null, 2));
        console.log(`\n💡 提示: 使用 sessions_spawn 工具创建子代理`);
      } else {
        console.log(`❌ 未找到办公室: ${command}`);
        console.log(`运行 "node spawn.js list" 查看所有办公室`);
      }
  }
}

main();