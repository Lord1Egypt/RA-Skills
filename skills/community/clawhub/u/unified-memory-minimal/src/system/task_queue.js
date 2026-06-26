/**
 * Task Queue - 智能任务分配系统 v1.0
 * 
 * Features:
 * - Smart task assignment (skill matching, load balancing, round-robin, volunteer, expert-first)
 * - Task status tracking & handoff
 * - Agent Profile integration
 * - Collab Bus integration
 * - Priority-based DAG scheduling
 * 
 * Usage:
 *   node task_queue.js add "title" --desc "description" --skills "python,coding" --priority 7
 *   node task_queue.js assign <id> --strategy skill_match
 *   node task_queue.js start <id> --agent xiao-zhi
 *   node task_queue.js complete <id> --result '{"status":"success"}'
 *   node task_queue.js handoff <id> --from xiao-zhi --to xiao-liu --reason "需要飞书操作"
 *   node task_queue.js list --agent xiao-zhi
 *   node task_queue.js stats
 */

import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import os from 'os';
import crypto from 'crypto';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// ========== Configuration ==========

const WORKSPACE = path.join(os.homedir(), '.openclaw', 'workspace');
const MEMORY_DIR = path.join(WORKSPACE, 'memory');
const TASK_DIR = path.join(MEMORY_DIR, 'tasks');
const STORAGE_FILE = path.join(TASK_DIR, 'tasks.json');
const HISTORY_FILE = path.join(TASK_DIR, 'history.jsonl');
const PROFILES_FILE = path.join(TASK_DIR, 'profiles.json');
const EVENTS_FILE = path.join(TASK_DIR, 'events.jsonl');

// Ensure directories
await fs.mkdir(TASK_DIR, { recursive: true });

// ========== Enums ==========

const TaskStatus = {
  PENDING: 'pending',
  ASSIGNED: 'assigned',
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed',
  FAILED: 'failed',
  CANCELLED: 'cancelled'
};

const AssignmentStrategy = {
  SKILL_MATCH: 'skill_match',
  LOAD_BALANCE: 'load_balance',
  ROUND_ROBIN: 'round_robin',
  VOLUNTEER: 'volunteer',
  EXPERT_FIRST: 'expert_first'
};

// ========== Data Classes ==========

class Task {
  constructor({
    taskId = null,
    title,
    description = '',
    requiredSkills = [],
    priority = 5,
    status = TaskStatus.PENDING,
    assignedTo = null,
    createdBy = null,
    createdAt = new Date(),
    startedAt = null,
    completedAt = null,
    result = null,
    handoffHistory = []
  }) {
    this.taskId = taskId || crypto.randomUUID().slice(0, 12);
    this.title = title;
    this.description = description;
    this.requiredSkills = requiredSkills;
    this.priority = Math.min(10, Math.max(1, priority));
    this.status = status;
    this.assignedTo = assignedTo;
    this.createdBy = createdBy;
    this.createdAt = createdAt instanceof Date ? createdAt.toISOString() : createdAt;
    this.startedAt = startedAt;
    this.completedAt = completedAt;
    this.result = result;
    this.handoffHistory = handoffHistory;
  }
  
  toDict() {
    return {
      taskId: this.taskId,
      title: this.title,
      description: this.description,
      requiredSkills: this.requiredSkills,
      priority: this.priority,
      status: this.status,
      assignedTo: this.assignedTo,
      createdBy: this.createdBy,
      createdAt: this.createdAt,
      startedAt: this.startedAt,
      completedAt: this.completedAt,
      result: this.result,
      handoffHistory: this.handoffHistory
    };
  }
  
  static fromDict(d) {
    return new Task({
      taskId: d.taskId,
      title: d.title,
      description: d.description,
      requiredSkills: d.requiredSkills || [],
      priority: d.priority || 5,
      status: d.status || TaskStatus.PENDING,
      assignedTo: d.assignedTo,
      createdBy: d.createdBy,
      createdAt: d.createdAt,
      startedAt: d.startedAt,
      completedAt: d.completedAt,
      result: d.result,
      handoffHistory: d.handoffHistory || []
    });
  }
}

class AgentProfile {
  constructor(agentId, name = null) {
    this.agentId = agentId;
    this.name = name || agentId;
    this.skills = {}; // skill -> score (0-1)
    this.workload = 0.0;
    this.expertise = [];
    this.preferences = {};
    this.trustScores = {};
    this.taskHistory = [];
    this.successRate = 1.0;
  }
  
  addSkill(skill, score) {
    this.skills[skill.toLowerCase()] = Math.min(1.0, Math.max(0.0, score));
  }
  
  hasSkill(skill) {
    return skill.toLowerCase() in this.skills;
  }
  
  getSkillScore(skill) {
    return this.skills[skill.toLowerCase()] || 0.0;
  }
  
  toDict() {
    return {
      agentId: this.agentId,
      name: this.name,
      skills: this.skills,
      workload: this.workload,
      expertise: this.expertise,
      preferences: this.preferences,
      trustScores: this.trustScores,
      taskHistory: this.taskHistory.slice(-20),
      successRate: this.successRate
    };
  }
  
  static fromDict(d) {
    const profile = new AgentProfile(d.agentId, d.name);
    profile.skills = d.skills || {};
    profile.workload = d.workload || 0.0;
    profile.expertise = d.expertise || [];
    profile.preferences = d.preferences || {};
    profile.trustScores = d.trustScores || {};
    profile.taskHistory = d.taskHistory || [];
    profile.successRate = d.successRate || 1.0;
    return profile;
  }
}

class AgentProfileManager {
  constructor(storagePath) {
    this.storagePath = storagePath;
    this.profiles = {};
    this._load();
  }
  
  async _load() {
    try {
      if (await fileExists(this.storagePath)) {
        const data = JSON.parse(await fs.readFile(this.storagePath, 'utf-8'));
        for (const [agentId, profileData] of Object.entries(data.profiles || {})) {
          this.profiles[agentId] = AgentProfile.fromDict(profileData);
        }
      }
    } catch (e) {
      // File doesn't exist or parse error
    }
    
    // Default agents
    if (!this.profiles['xiao-zhi']) {
      this.profiles['xiao-zhi'] = new AgentProfile('xiao-zhi', '小智');
      this.profiles['xiao-zhi'].addSkill('coding', 0.9);
      this.profiles['xiao-zhi'].addSkill('python', 0.9);
      this.profiles['xiao-zhi'].addSkill('planning', 0.85);
      this.profiles['xiao-zhi'].addSkill('documentation', 0.8);
    }
    
    if (!this.profiles['xiao-liu']) {
      this.profiles['xiao-liu'] = new AgentProfile('xiao-liu', '小六');
      this.profiles['xiao-liu'].addSkill('feishu', 0.95);
      this.profiles['xiao-liu'].addSkill('communication', 0.9);
      this.profiles['xiao-liu'].addSkill('coordination', 0.85);
    }
  }
  
  async _save() {
    const data = {
      profiles: Object.fromEntries(
        Object.entries(this.profiles).map(([k, v]) => [k, v.toDict()])
      )
    };
    await fs.writeFile(this.storagePath, JSON.stringify(data, null, 2), 'utf-8');
  }
  
  getProfile(agentId) {
    return this.profiles[agentId] || null;
  }
  
  getAllAgents() {
    return Object.values(this.profiles);
  }
  
  async updateWorkload(agentId, delta) {
    if (agentId in this.profiles) {
      this.profiles[agentId].workload = Math.max(0, this.profiles[agentId].workload + delta);
      await this._save();
    }
  }
  
  async recordTaskCompletion(agentId, taskId, success) {
    if (agentId in this.profiles) {
      const profile = this.profiles[agentId];
      profile.taskHistory.push(success ? `${taskId}_success` : `${taskId}_failed`);
      // Update success rate
      const total = profile.taskHistory.length;
      const successful = profile.taskHistory.filter(t => t.endsWith('_success')).length;
      profile.successRate = successful / total || 1.0;
      await this._save();
    }
  }
}

class CollabBus {
  constructor(logPath) {
    this.logPath = logPath;
    this.subscribers = {}; // topic -> agent_ids
  }
  
  async _ensureLog() {
    await fs.mkdir(path.dirname(this.logPath), { recursive: true });
    try {
      await fs.access(this.logPath);
    } catch {
      await fs.writeFile(this.logPath, '', 'utf-8');
    }
  }
  
  async publish(eventType, data, fromAgent = 'system') {
    await this._ensureLog();
    
    const event = {
      id: crypto.createHash('md5').update(`${Date.now()}${eventType}`).digest('hex').slice(0, 12),
      timestamp: new Date().toISOString(),
      type: eventType,
      from: fromAgent,
      data
    };
    
    await fs.appendFile(this.logPath, JSON.stringify(event) + '\n', 'utf-8');
    return event.id;
  }
  
  async notifyTaskAssigned(taskId, agentId, assignedBy = 'system') {
    return this.publish('task_assigned', {
      taskId,
      agentId,
      assignedBy
    }, assignedBy);
  }
  
  async notifyTaskHandoff(taskId, fromAgent, toAgent, reason) {
    return this.publish('task_handoff', {
      taskId,
      fromAgent,
      toAgent,
      reason
    }, fromAgent);
  }
  
  async notifyTaskCompleted(taskId, agentId, result) {
    return this.publish('task_completed', {
      taskId,
      agentId,
      result
    }, agentId);
  }
  
  async getRecentEvents(limit = 20) {
    try {
      const content = await fs.readFile(this.logPath, 'utf-8');
      const lines = content.split('\n').filter(l => l.trim());
      return lines.slice(-limit).map(l => JSON.parse(l));
    } catch {
      return [];
    }
  }
}

class AssignmentEngine {
  constructor(agentProfiles) {
    this.agentProfiles = agentProfiles;
    this.roundRobinIndex = 0;
  }
  
  findBestAgent(task, strategy) {
    const agents = this.agentProfiles.getAllAgents();
    if (!agents.length) return null;
    
    switch (strategy) {
      case AssignmentStrategy.SKILL_MATCH:
        return this._skillMatch(task, agents);
      case AssignmentStrategy.LOAD_BALANCE:
        return this._loadBalance(task, agents);
      case AssignmentStrategy.ROUND_ROBIN:
        return this._roundRobin(task, agents);
      case AssignmentStrategy.EXPERT_FIRST:
        return this._expertFirst(task, agents);
      default:
        return agents[0].agentId;
    }
  }
  
  _skillMatch(task, agents) {
    let bestAgent = null;
    let bestScore = -1;
    
    for (const agent of agents) {
      let score = this.calculateSkillMatchScore(task, agent.agentId);
      score -= agent.workload * 0.1;
      if (score > bestScore) {
        bestScore = score;
        bestAgent = agent.agentId;
      }
    }
    
    return bestAgent;
  }
  
  _loadBalance(task, agents) {
    let bestAgent = null;
    let minWorkload = Infinity;
    
    for (const agent of agents) {
      if (task.requiredSkills.length > 0) {
        const skillScore = this.calculateSkillMatchScore(task, agent.agentId);
        if (skillScore < 0.3) continue;
      }
      
      const score = this.getLoadBalanceScore(agent.agentId);
      if (score < minWorkload) {
        minWorkload = score;
        bestAgent = agent.agentId;
      }
    }
    
    return bestAgent;
  }
  
  _roundRobin(task, agents) {
    if (!agents.length) return null;
    
    let attempts = 0;
    while (attempts < agents.length) {
      const agent = agents[this.roundRobinIndex % agents.length];
      this.roundRobinIndex++;
      
      if (task.requiredSkills.length > 0) {
        const skillScore = this.calculateSkillMatchScore(task, agent.agentId);
        if (skillScore >= 0.3) return agent.agentId;
      } else {
        return agent.agentId;
      }
      
      attempts++;
    }
    
    return agents[0].agentId;
  }
  
  _expertFirst(task, agents) {
    let bestAgent = null;
    let bestScore = -1;
    
    for (const agent of agents) {
      // Check expertise match
      const expertiseMatch = task.requiredSkills.some(skill =>
        agent.expertise.some(e => e.toLowerCase().includes(skill.toLowerCase()))
      );
      
      const skillScore = this.calculateSkillMatchScore(task, agent.agentId);
      const successScore = agent.successRate;
      
      // Expertise bonus
      if (expertiseMatch) score *= 1.5;
      
      const score = skillScore * 0.6 + successScore * 0.4 - agent.workload * 0.1;
      
      if (score > bestScore) {
        bestScore = score;
        bestAgent = agent.agentId;
      }
    }
    
    return bestAgent;
  }
  
  calculateSkillMatchScore(task, agentId) {
    const profile = this.agentProfiles.getProfile(agentId);
    if (!profile) return 0.0;
    
    if (!task.requiredSkills.length) return 1.0;
    
    const scores = task.requiredSkills.map(skill => profile.getSkillScore(skill));
    return scores.reduce((a, b) => a + b, 0) / scores.length;
  }
  
  getLoadBalanceScore(agentId) {
    const profile = this.agentProfiles.getProfile(agentId);
    if (!profile) return Infinity;
    return profile.workload;
  }
}

class TaskQueue {
  constructor(storagePath, agentProfiles, collabBus) {
    this.storagePath = storagePath;
    this.historyPath = path.join(path.dirname(storagePath), 'history.jsonl');
    this.agentProfiles = agentProfiles;
    this.collabBus = collabBus;
    this.assignmentEngine = new AssignmentEngine(agentProfiles);
    this.tasks = {};
    this._load();
  }
  
  async _load() {
    try {
      if (await fileExists(this.storagePath)) {
        const data = JSON.parse(await fs.readFile(this.storagePath, 'utf-8'));
        for (const [taskId, taskData] of Object.entries(data.tasks || {})) {
          this.tasks[taskId] = Task.fromDict(taskData);
        }
      }
    } catch (e) {
      // File doesn't exist or parse error
    }
  }
  
  async _save() {
    const data = {
      tasks: Object.fromEntries(
        Object.entries(this.tasks).map(([k, v]) => [k, v.toDict()])
      )
    };
    await fs.writeFile(this.storagePath, JSON.stringify(data, null, 2), 'utf-8');
  }
  
  async _appendHistory(task) {
    await fs.mkdir(path.dirname(this.historyPath), { recursive: true });
    await fs.appendFile(this.historyPath, JSON.stringify(task.toDict()) + '\n', 'utf-8');
  }
  
  async addTask(task) {
    if (!task.taskId) {
      task.taskId = crypto.createHash('md5')
        .update(`${new Date().toISOString()}${task.title}`)
        .digest('hex').slice(0, 12);
    }
    
    this.tasks[task.taskId] = task;
    await this._save();
    
    console.log(`✅ 创建任务: [${task.taskId}] ${task.title}`);
    console.log(`   技能要求: ${task.requiredSkills.join(', ') || '无'}`);
    console.log(`   优先级: ${task.priority}/10`);
    
    return task.taskId;
  }
  
  async assign(taskId, strategy = AssignmentStrategy.SKILL_MATCH) {
    const task = this.tasks[taskId];
    if (!task) {
      console.log(`❌ 任务不存在: ${taskId}`);
      return null;
    }
    
    if (task.status !== TaskStatus.PENDING) {
      console.log(`❌ 任务状态不允许分配: ${task.status}`);
      return null;
    }
    
    const agentId = this.assignmentEngine.findBestAgent(task, strategy);
    if (!agentId) {
      console.log(`❌ 没有可用的 Agent`);
      return null;
    }
    
    task.assignedTo = agentId;
    task.status = TaskStatus.ASSIGNED;
    
    await this.agentProfiles.updateWorkload(agentId, 1);
    await this._save();
    await this.collabBus.notifyTaskAssigned(taskId, agentId);
    
    console.log(`✅ 任务已分配: [${taskId}] → ${agentId}`);
    console.log(`   分配策略: ${strategy}`);
    
    return agentId;
  }
  
  getAgentTasks(agentId, status = null) {
    const result = [];
    for (const task of Object.values(this.tasks)) {
      if (task.assignedTo === agentId) {
        if (status === null || task.status === status) {
          result.push(task);
        }
      }
    }
    // Sort by priority
    result.sort((a, b) => b.priority - a.priority);
    return result;
  }
  
  async startTask(taskId, agentId) {
    const task = this.tasks[taskId];
    if (!task) {
      console.log(`❌ 任务不存在: ${taskId}`);
      return false;
    }
    
    if (task.assignedTo !== agentId) {
      console.log(`❌ 任务未分配给 ${agentId}`);
      return false;
    }
    
    if (task.status !== TaskStatus.ASSIGNED) {
      console.log(`❌ 任务状态不允许开始: ${task.status}`);
      return false;
    }
    
    task.status = TaskStatus.IN_PROGRESS;
    task.startedAt = new Date().toISOString();
    
    await this._save();
    console.log(`🚀 任务开始: [${taskId}] by ${agentId}`);
    return true;
  }
  
  async completeTask(taskId, agentId, result = {}) {
    const task = this.tasks[taskId];
    if (!task) {
      console.log(`❌ 任务不存在: ${taskId}`);
      return false;
    }
    
    if (task.assignedTo !== agentId) {
      console.log(`❌ 任务未分配给 ${agentId}`);
      return false;
    }
    
    task.status = TaskStatus.COMPLETED;
    task.completedAt = new Date().toISOString();
    task.result = result;
    
    await this.agentProfiles.updateWorkload(agentId, -1);
    await this.agentProfiles.recordTaskCompletion(agentId, taskId, true);
    await this._appendHistory(task);
    delete this.tasks[taskId];
    
    await this._save();
    await this.collabBus.notifyTaskCompleted(taskId, agentId, result);
    
    console.log(`✅ 任务完成: [${taskId}] by ${agentId}`);
    return true;
  }
  
  async failTask(taskId, agentId, error) {
    const task = this.tasks[taskId];
    if (!task) {
      console.log(`❌ 任务不存在: ${taskId}`);
      return false;
    }
    
    if (task.assignedTo !== agentId) {
      console.log(`❌ 任务未分配给 ${agentId}`);
      return false;
    }
    
    task.status = TaskStatus.FAILED;
    task.completedAt = new Date().toISOString();
    task.result = { error };
    
    await this.agentProfiles.updateWorkload(agentId, -1);
    await this.agentProfiles.recordTaskCompletion(agentId, taskId, false);
    await this._appendHistory(task);
    delete this.tasks[taskId];
    
    await this._save();
    console.log(`❌ 任务失败: [${taskId}] by ${agentId}`);
    console.log(`   错误: ${error}`);
    return true;
  }
  
  async handoff(taskId, fromAgent, toAgent, reason) {
    const task = this.tasks[taskId];
    if (!task) {
      console.log(`❌ 任务不存在: ${taskId}`);
      return false;
    }
    
    if (task.assignedTo !== fromAgent) {
      console.log(`❌ 任务未分配给 ${fromAgent}`);
      return false;
    }
    
    task.handoffHistory.push({
      from: fromAgent,
      to: toAgent,
      reason,
      timestamp: new Date().toISOString()
    });
    
    task.assignedTo = toAgent;
    
    await this.agentProfiles.updateWorkload(fromAgent, -1);
    await this.agentProfiles.updateWorkload(toAgent, 1);
    
    await this._save();
    await this.collabBus.notifyTaskHandoff(taskId, fromAgent, toAgent, reason);
    
    console.log(`🔄 任务移交: [${taskId}] ${fromAgent} → ${toAgent}`);
    console.log(`   原因: ${reason}`);
    return true;
  }
  
  getPendingTasks() {
    const result = Object.values(this.tasks).filter(t => t.status === TaskStatus.PENDING);
    result.sort((a, b) => b.priority - a.priority);
    return result;
  }
  
  getTaskStats() {
    const stats = {};
    for (const task of Object.values(this.tasks)) {
      const status = task.status;
      if (!stats[status]) stats[status] = 0;
      stats[status]++;
    }
    return stats;
  }
  
  listTasks(status = null) {
    let tasks = Object.values(this.tasks);
    if (status) {
      tasks = tasks.filter(t => t.status === status);
    }
    tasks.sort((a, b) => b.priority - a.priority);
    return tasks;
  }
}

// ========== Utilities ==========

async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

// ========== CLI ==========

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command) {
    console.log(`
Task Queue - 智能任务分配系统 v1.0

Usage:
    node task_queue.js add "title" --desc "描述" --skills "python,coding" --priority 7
    node task_queue.js assign <id> --strategy skill_match
    node task_queue.js start <id> --agent xiao-zhi
    node task_queue.js complete <id> --result '{"status":"success"}'
    node task_queue.js handoff <id> --from xiao-zhi --to xiao-liu --reason "需要飞书操作"
    node task_queue.js list --agent xiao-zhi
    node task_queue.js stats
`);
    process.exit(1);
  }
  
  const agentProfiles = new AgentProfileManager(PROFILES_FILE);
  const collabBus = new CollabBus(EVENTS_FILE);
  const taskQueue = new TaskQueue(STORAGE_FILE, agentProfiles, collabBus);
  
  switch (command) {
    case 'add': {
      const title = args.slice(1).join(' ') || args[1];
      const descIdx = args.indexOf('--desc');
      const skillsIdx = args.indexOf('--skills');
      const priorityIdx = args.indexOf('--priority');
      const byIdx = args.indexOf('--by');
      
      const task = new Task({
        title,
        description: descIdx !== -1 ? args[descIdx + 1] : '',
        requiredSkills: skillsIdx !== -1 ? args[skillsIdx + 1].split(',').map(s => s.trim()) : [],
        priority: priorityIdx !== -1 ? parseInt(args[priorityIdx + 1]) : 5,
        createdBy: byIdx !== -1 ? args[byIdx + 1] : null
      });
      
      await taskQueue.addTask(task);
      break;
    }
    
    case 'assign': {
      const taskId = args[1];
      const strategyIdx = args.indexOf('--strategy');
      const strategy = strategyIdx !== -1 ? args[strategyIdx + 1] : 'skill_match';
      
      if (!taskId) {
        console.log('❌ 请提供任务 ID');
        process.exit(1);
      }
      
      await taskQueue.assign(taskId, strategy);
      break;
    }
    
    case 'start': {
      const taskId = args[1];
      const agentIdx = args.indexOf('--agent');
      const agentId = agentIdx !== -1 ? args[agentIdx + 1] : 'xiao-zhi';
      
      if (!taskId) {
        console.log('❌ 请提供任务 ID');
        process.exit(1);
      }
      
      await taskQueue.startTask(taskId, agentId);
      break;
    }
    
    case 'complete': {
      const taskId = args[1];
      const resultIdx = args.indexOf('--result');
      const agentIdx = args.indexOf('--agent');
      const agentId = agentIdx !== -1 ? args[agentIdx + 1] : 'xiao-zhi';
      let result = {};
      
      if (resultIdx !== -1) {
        try {
          result = JSON.parse(args[resultIdx + 1]);
        } catch (e) {
          console.log('❌ 结果格式错误，请提供 JSON');
          process.exit(1);
        }
      }
      
      if (!taskId) {
        console.log('❌ 请提供任务 ID');
        process.exit(1);
      }
      
      await taskQueue.completeTask(taskId, agentId, result);
      break;
    }
    
    case 'handoff': {
      const taskId = args[1];
      const fromIdx = args.indexOf('--from');
      const toIdx = args.indexOf('--to');
      const reasonIdx = args.indexOf('--reason');
      
      if (!taskId || fromIdx === -1 || toIdx === -1) {
        console.log('❌ 请提供任务 ID, --from 和 --to');
        process.exit(1);
      }
      
      await taskQueue.handoff(
        taskId,
        args[fromIdx + 1],
        args[toIdx + 1],
        reasonIdx !== -1 ? args[reasonIdx + 1] : '未指定原因'
      );
      break;
    }
    
    case 'list': {
      const agentIdx = args.indexOf('--agent');
      const statusIdx = args.indexOf('--status');
      
      let tasks;
      if (agentIdx !== -1) {
        const status = statusIdx !== -1 ? args[statusIdx + 1] : null;
        tasks = taskQueue.getAgentTasks(args[agentIdx + 1], status);
      } else {
        const status = statusIdx !== -1 ? args[statusIdx + 1] : null;
        tasks = taskQueue.listTasks(status);
      }
      
      if (tasks.length === 0) {
        console.log('没有任务');
      } else {
        console.log(`📋 任务列表 (${tasks.length}):\n`);
        for (const task of tasks) {
          console.log(`  [${task.taskId}] ${task.title}`);
          console.log(`    状态: ${task.status} | 优先级: ${task.priority} | 分配给: ${task.assignedTo || '无'}`);
          console.log();
        }
      }
      break;
    }
    
    case 'stats': {
      const stats = taskQueue.getTaskStats();
      console.log('📊 任务统计:\n');
      for (const [status, count] of Object.entries(stats)) {
        console.log(`  ${status}: ${count}`);
      }
      console.log(`\n  总计: ${Object.values(stats).reduce((a, b) => a + b, 0)}`);
      
      console.log('\n👥 Agent 负载:\n');
      for (const agent of agentProfiles.getAllAgents()) {
        console.log(`  ${agent.name} (${agent.agentId}): ${(agent.workload * 100).toFixed(0)}%`);
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

export {
  Task,
  TaskStatus,
  AgentProfile,
  AgentProfileManager,
  CollabBus,
  AssignmentEngine,
  AssignmentStrategy,
  TaskQueue
};

export default TaskQueue;
