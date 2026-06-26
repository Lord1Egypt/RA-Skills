#!/usr/bin/env node

/**
 * Virtual Company Memory System - 记忆持久化
 * 解决子代理关闭后记忆丢失的问题
 * 
 * 核心理念：换身体不换意识
 * - 子窗口失效 → 创建新窗口 → 注入记忆 → 继续工作
 * - 每个员工有独立的记忆文件
 * - 团队有共享的项目上下文
 */

const fs = require('fs');
const path = require('path');

// 记忆根目录
const MEMORY_ROOT = path.join(process.env.HOME || process.env.USERPROFILE, '.agent-memory');

/**
 * 确保目录存在
 */
function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  return dir;
}

/**
 * 记忆管理器 - 支持虚拟公司35个员工
 */
class MemoryManager {
  constructor(teamName, officeName, sessionId) {
    this.teamName = teamName;       // 如：搞钱特战队、软件开发团队
    this.officeName = officeName;   // 如：市场猎手办公室、程序员办公室
    this.sessionId = sessionId;
    
    // 记忆目录结构
    this.officeDir = path.join(MEMORY_ROOT, 'virtual-company', teamName, officeName);
    this.teamDir = path.join(MEMORY_ROOT, 'virtual-company', teamName);
    this.companyDir = path.join(MEMORY_ROOT, 'virtual-company');
    
    this.memberFile = path.join(this.officeDir, 'member.json');
    this.sessionFile = path.join(this.officeDir, 'sessions', `${sessionId}.json`);
    this.sharedDir = path.join(this.teamDir, 'shared');
    this.companySharedDir = path.join(this.companyDir, 'shared');
    
    // 确保目录存在
    ensureDir(this.officeDir);
    ensureDir(path.dirname(this.sessionFile));
    ensureDir(this.sharedDir);
    ensureDir(this.companySharedDir);
  }

  /**
   * 初始化员工记忆
   */
  initMemberMemory(memberConfig) {
    if (!fs.existsSync(this.memberFile)) {
      const initialMemory = {
        name: memberConfig.name,           // 如：市场猎手
        role: memberConfig.role,           // 如：市场猎手
        team: memberConfig.team,           // 如：搞钱特战队
        model: memberConfig.model,         // 如：qwen3-max
        description: memberConfig.description,
        createdAt: new Date().toISOString(),
        tasks: [],
        experiences: [],
        skills: memberConfig.skills || [],
        notes: [],
        totalSessions: 0
      };
      fs.writeFileSync(this.memberFile, JSON.stringify(initialMemory, null, 2));
    }
    
    return this.loadMemberMemory();
  }

  /**
   * 加载员工记忆
   */
  loadMemberMemory() {
    if (fs.existsSync(this.memberFile)) {
      return JSON.parse(fs.readFileSync(this.memberFile, 'utf8'));
    }
    return null;
  }

  /**
   * 更新员工记忆
   */
  updateMemberMemory(updates) {
    const memory = this.loadMemberMemory() || {};
    const updated = { 
      ...memory, 
      ...updates, 
      updatedAt: new Date().toISOString(),
      totalSessions: (memory.totalSessions || 0) + 1
    };
    
    fs.writeFileSync(this.memberFile, JSON.stringify(updated, null, 2));
    return updated;
  }

  /**
   * 添加任务记录
   */
  addTask(task) {
    const memory = this.loadMemberMemory();
    if (!memory) return;
    
    memory.tasks.push({
      ...task,
      completedAt: new Date().toISOString()
    });
    
    this.updateMemberMemory(memory);
  }

  /**
   * 添加经验
   */
  addExperience(experience) {
    const memory = this.loadMemberMemory();
    if (!memory) return;
    
    memory.experiences.push({
      ...experience,
      learnedAt: new Date().toISOString()
    });
    
    this.updateMemberMemory(memory);
  }

  /**
   * 获取团队共享上下文
   */
  getTeamContext() {
    const contextFile = path.join(this.sharedDir, 'team-context.json');
    if (fs.existsSync(contextFile)) {
      return JSON.parse(fs.readFileSync(contextFile, 'utf8'));
    }
    return {
      team: this.teamName,
      projects: [],
      decisions: [],
      currentPhase: 'waiting'
    };
  }

  /**
   * 更新团队共享上下文
   */
  updateTeamContext(updates) {
    const context = this.getTeamContext();
    const updated = { ...context, ...updates, updatedAt: new Date().toISOString() };
    
    const contextFile = path.join(this.sharedDir, 'team-context.json');
    fs.writeFileSync(contextFile, JSON.stringify(updated, null, 2));
    return updated;
  }

  /**
   * 获取公司级共享上下文
   */
  getCompanyContext() {
    const contextFile = path.join(this.companySharedDir, 'company-context.json');
    if (fs.existsSync(contextFile)) {
      return JSON.parse(fs.readFileSync(contextFile, 'utf8'));
    }
    return {
      company: '虚拟公司',
      ceo: '马云',
      activeProjects: [],
      companyDecisions: [],
      announcements: []
    };
  }

  /**
   * 更新公司级共享上下文
   */
  updateCompanyContext(updates) {
    const context = this.getCompanyContext();
    const updated = { ...context, ...updates, updatedAt: new Date().toISOString() };
    
    const contextFile = path.join(this.companySharedDir, 'company-context.json');
    fs.writeFileSync(contextFile, JSON.stringify(updated, null, 2));
    return updated;
  }

  /**
   * 记录团队决策
   */
  recordTeamDecision(decision) {
    const decisionsFile = path.join(this.sharedDir, 'decisions.json');
    
    let decisions = [];
    if (fs.existsSync(decisionsFile)) {
      decisions = JSON.parse(fs.readFileSync(decisionsFile, 'utf8'));
    }
    
    decisions.push({
      ...decision,
      decidedAt: new Date().toISOString()
    });
    
    fs.writeFileSync(decisionsFile, JSON.stringify(decisions, null, 2));
  }

  /**
   * 记录公司决策
   */
  recordCompanyDecision(decision) {
    const decisionsFile = path.join(this.companySharedDir, 'company-decisions.json');
    
    let decisions = [];
    if (fs.existsSync(decisionsFile)) {
      decisions = JSON.parse(fs.readFileSync(decisionsFile, 'utf8'));
    }
    
    decisions.push({
      ...decision,
      decidedBy: decision.decidedBy || 'CEO',
      decidedAt: new Date().toISOString()
    });
    
    fs.writeFileSync(decisionsFile, JSON.stringify(decisions, null, 2));
  }

  /**
   * 记录经验教训
   */
  recordLesson(lesson) {
    const lessonsFile = path.join(this.sharedDir, 'lessons-learned.json');
    
    let lessons = [];
    if (fs.existsSync(lessonsFile)) {
      lessons = JSON.parse(fs.readFileSync(lessonsFile, 'utf8'));
    }
    
    lessons.push({
      ...lesson,
      learnedBy: this.officeName,
      learnedAt: new Date().toISOString()
    });
    
    fs.writeFileSync(lessonsFile, JSON.stringify(lessons, null, 2));
  }

  /**
   * 获取完整记忆摘要（用于子代理启动时注入）
   * 核心功能：换身体不换意识
   */
  getMemoryContext() {
    const memberMemory = this.loadMemberMemory();
    const teamContext = this.getTeamContext();
    const companyContext = this.getCompanyContext();
    
    let context = `## 🧠 记忆上下文（换身体不换意识）\n\n`;
    
    // 公司级上下文
    context += `### 🏢 公司信息\n`;
    context += `- CEO: ${companyContext.ceo || '马云'}\n`;
    if (companyContext.activeProjects?.length > 0) {
      context += `- 活跃项目: ${companyContext.activeProjects.join(', ')}\n`;
    }
    if (companyContext.announcements?.length > 0) {
      const recentAnnouncements = companyContext.announcements.slice(-3);
      context += `- 最新公告:\n`;
      recentAnnouncements.forEach(a => {
        context += `  - ${a.content}\n`;
      });
    }
    context += `\n`;
    
    // 团队级上下文
    context += `### 👥 团队信息\n`;
    context += `- 团队: ${this.teamName}\n`;
    context += `- 阶段: ${teamContext.currentPhase || 'waiting'}\n`;
    if (teamContext.projects?.length > 0) {
      context += `- 项目: ${teamContext.projects.join(', ')}\n`;
    }
    if (teamContext.decisions?.length > 0) {
      const recentDecisions = teamContext.decisions.slice(-3);
      context += `- 近期决策:\n`;
      recentDecisions.forEach(d => {
        context += `  - ${d.decision}\n`;
      });
    }
    context += `\n`;
    
    // 个人记忆
    if (memberMemory) {
      context += `### 👤 个人记忆 (${memberMemory.totalSessions || 0}次会话)\n`;
      
      if (memberMemory.tasks?.length > 0) {
        context += `#### 历史任务 (${memberMemory.tasks.length}个)\n`;
        const recentTasks = memberMemory.tasks.slice(-5);
        recentTasks.forEach(t => {
          context += `- ${t.description || t.name} (${t.status || '完成'})\n`;
        });
        context += `\n`;
      }
      
      if (memberMemory.experiences?.length > 0) {
        context += `#### 经验积累 (${memberMemory.experiences.length}条)\n`;
        const recentExp = memberMemory.experiences.slice(-5);
        recentExp.forEach(e => {
          context += `- ${e.insight || e.description}\n`;
        });
        context += `\n`;
      }
      
      if (memberMemory.skills?.length > 0) {
        context += `#### 专业技能\n`;
        context += `- ${memberMemory.skills.join(', ')}\n`;
        context += `\n`;
      }
    }
    
    return context;
  }

  /**
   * 保存会话记录
   */
  saveSession(sessionData) {
    const session = {
      ...sessionData,
      office: this.officeName,
      team: this.teamName,
      endedAt: new Date().toISOString()
    };
    
    fs.writeFileSync(this.sessionFile, JSON.stringify(session, null, 2));
    
    // 更新会话计数
    this.updateMemberMemory({ lastSession: session });
  }

  /**
   * 列出所有办公室的记忆状态
   */
  static listAllOffices() {
    const companyDir = path.join(MEMORY_ROOT, 'virtual-company');
    if (!fs.existsSync(companyDir)) {
      return [];
    }
    
    const offices = [];
    const teams = fs.readdirSync(companyDir);
    
    teams.forEach(team => {
      const teamPath = path.join(companyDir, team);
      if (fs.statSync(teamPath).isDirectory() && team !== 'shared') {
        const officesInTeam = fs.readdirSync(teamPath);
        officesInTeam.forEach(office => {
          const officePath = path.join(teamPath, office);
          if (fs.statSync(officePath).isDirectory() && office !== 'shared') {
            const memberFile = path.join(officePath, 'member.json');
            if (fs.existsSync(memberFile)) {
              const memory = JSON.parse(fs.readFileSync(memberFile, 'utf8'));
              offices.push({
                team,
                office,
                name: memory.name,
                totalSessions: memory.totalSessions || 0,
                tasks: memory.tasks?.length || 0,
                experiences: memory.experiences?.length || 0,
                lastUpdated: memory.updatedAt || memory.createdAt
              });
            }
          }
        });
      }
    });
    
    return offices;
  }
}

// CLI 工具
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command) {
    console.log('Virtual Company Memory System');
    console.log('');
    console.log('用法:');
    console.log('  node memory.js init <团队> <办公室> <配置JSON>');
    console.log('  node memory.js context <团队> <办公室>');
    console.log('  node memory.js update <团队> <办公室> <更新JSON>');
    console.log('  node memory.js add-task <团队> <办公室> <任务描述>');
    console.log('  node memory.js add-exp <团队> <办公室> <经验描述>');
    console.log('  node memory.js record-decision <团队> <决策>');
    console.log('  node memory.js record-lesson <团队> <教训>');
    console.log('  node memory.js list              # 列出所有办公室状态');
    console.log('');
    console.log('团队名：搞钱特战队、软件开发团队、小说+漫剧团队、技术中台团队、CEO+CEO秘书');
    console.log('办公室名：市场猎手办公室、程序员办公室、马云办公室 等');
    process.exit(0);
  }
  
  switch (command) {
    case 'init':
      const team1 = args[1];
      const office1 = args[2];
      const config1 = JSON.parse(args[3]);
      const sessionId1 = `session-${Date.now()}`;
      const mm1 = new MemoryManager(team1, office1, sessionId1);
      const memory1 = mm1.initMemberMemory(config1);
      console.log(`✅ 已初始化 ${team1} - ${office1}`);
      console.log(JSON.stringify(memory1, null, 2));
      break;
      
    case 'context':
      const team2 = args[1];
      const office2 = args[2];
      const sessionId2 = `session-${Date.now()}`;
      const mm2 = new MemoryManager(team2, office2, sessionId2);
      const context2 = mm2.getMemoryContext();
      console.log(context2);
      break;
      
    case 'update':
      const team3 = args[1];
      const office3 = args[2];
      const updates3 = JSON.parse(args[3]);
      const sessionId3 = `session-${Date.now()}`;
      const mm3 = new MemoryManager(team3, office3, sessionId3);
      const updated3 = mm3.updateMemberMemory(updates3);
      console.log(`✅ 已更新 ${team3} - ${office3}`);
      console.log(JSON.stringify(updated3, null, 2));
      break;
      
    case 'add-task':
      const team4 = args[1];
      const office4 = args[2];
      const task4 = args[3];
      const sessionId4 = `session-${Date.now()}`;
      const mm4 = new MemoryManager(team4, office4, sessionId4);
      mm4.addTask({ description: task4, status: '完成' });
      console.log(`✅ 已添加任务到 ${team4} - ${office4}`);
      break;
      
    case 'add-exp':
      const team5 = args[1];
      const office5 = args[2];
      const exp5 = args[3];
      const sessionId5 = `session-${Date.now()}`;
      const mm5 = new MemoryManager(team5, office5, sessionId5);
      mm5.addExperience({ insight: exp5 });
      console.log(`✅ 已添加经验到 ${team5} - ${office5}`);
      break;
      
    case 'record-decision':
      const team6 = args[1];
      const decision6 = args[2];
      const sessionId6 = `session-${Date.now()}`;
      const mm6 = new MemoryManager(team6, 'shared', sessionId6);
      mm6.recordTeamDecision({ decision: decision6 });
      console.log(`✅ 已记录 ${team6} 的决策`);
      break;
      
    case 'record-lesson':
      const team7 = args[1];
      const lesson7 = args[2];
      const sessionId7 = `session-${Date.now()}`;
      const mm7 = new MemoryManager(team7, 'shared', sessionId7);
      mm7.recordLesson({ lesson: lesson7 });
      console.log(`✅ 已记录 ${team7} 的教训`);
      break;
      
    case 'list':
      const offices = MemoryManager.listAllOffices();
      console.log('\n🏢 虚拟公司记忆状态:');
      console.log('━'.repeat(60));
      offices.forEach(o => {
        console.log(`${o.team} - ${o.office}`);
        console.log(`  会话: ${o.totalSessions} | 任务: ${o.tasks} | 经验: ${o.experiences}`);
        console.log(`  最后更新: ${o.lastUpdated}`);
      });
      console.log('━'.repeat(60));
      console.log(`总计: ${offices.length} 个办公室`);
      break;
      
    default:
      console.log('未知命令:', command);
  }
}

// 只在直接运行时执行 CLI
if (require.main === module) {
  main();
}

module.exports = { MemoryManager };