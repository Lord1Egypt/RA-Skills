/**
 * Agent Collaboration System v3.1 - 多Agent协作系统
 * 
 * Features:
 * - Agent registration & management
 * - Task assignment & tracking
 * - Dynamic role assignment
 * - Conflict detection & resolution
 * - Collab Bus for inter-agent communication
 * - Decision engine
 * 
 * Usage:
 *   node agent_collab_system.js register --id "agent_pm" --name "产品经理" --role "pm" --skills "需求分析,产品设计"
 *   node agent_collab_system.js list
 *   node agent_collab_system.js add-task --id "task_001" --type "development" --desc "开发用户系统"
 *   node agent_collab_system.js assign --task "task_001" --agent "agent_engineer"
 *   node agent_collab_system.js stats
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
const COLLAB_DIR = path.join(MEMORY_DIR, 'collaboration');

const AGENTS_FILE = path.join(COLLAB_DIR, 'agent_profiles.json');
const TASKS_FILE = path.join(COLLAB_DIR, 'tasks.json');
const CONFLICTS_FILE = path.join(COLLAB_DIR, 'conflicts.json');
const EVENTS_FILE = path.join(COLLAB_DIR, 'events.jsonl');

// ========== Enums ==========

const AgentStatus = {
  ONLINE: 'online',
  BUSY: 'busy',
  OFFLINE: 'offline'
};

const TaskStatus = {
  PENDING: 'pending',
  ASSIGNED: 'assigned',
  IN_PROGRESS: 'in_progress',
  COMPLETED: 'completed',
  FAILED: 'failed'
};

const ConflictType = {
  REQUIREMENT: 'requirement',
  DESIGN: 'design',
  CODE: 'code',
  RESOURCE: 'resource'
};

const ConflictSeverity = {
  LOW: 'low',
  MEDIUM: 'medium',
  HIGH: 'high',
  CRITICAL: 'critical'
};

// ========== Data Classes ==========

class Agent {
  constructor({
    agentId,
    name,
    role,
    skills = [],
    expertise = [],
    workload = 0.0,
    status = AgentStatus.ONLINE,
    registeredAt = new Date().toISOString(),
    lastActive = new Date().toISOString(),
    completedTasks = 0,
    successRate = 1.0
  }) {
    this.agentId = agentId;
    this.name = name;
    this.role = role;
    this.skills = skills;
    this.expertise = expertise;
    this.workload = workload;
    this.status = status;
    this.registeredAt = registeredAt;
    this.lastActive = lastActive;
    this.completedTasks = completedTasks;
    this.successRate = successRate;
  }
  
  toDict() {
    return {
      agentId: this.agentId,
      name: this.name,
      role: this.role,
      skills: this.skills,
      expertise: this.expertise,
      workload: this.workload,
      status: this.status,
      registeredAt: this.registeredAt,
      lastActive: this.lastActive,
      completedTasks: this.completedTasks,
      successRate: this.successRate
    };
  }
  
  static fromDict(d) {
    return new Agent(d);
  }
}

class Task {
  constructor({
    taskId,
    taskType,
    description,
    requiredSkills = [],
    priority = 'normal',
    status = TaskStatus.PENDING,
    assignedTo = null,
    createdAt = new Date().toISOString(),
    updatedAt = new Date().toISOString(),
    completedAt = null,
    result = null
  }) {
    this.taskId = taskId;
    this.taskType = taskType;
    this.description = description;
    this.requiredSkills = requiredSkills;
    this.priority = priority;
    this.status = status;
    this.assignedTo = assignedTo;
    this.createdAt = createdAt;
    this.updatedAt = updatedAt;
    this.completedAt = completedAt;
    this.result = result;
  }
  
  toDict() {
    return {
      taskId: this.taskId,
      taskType: this.taskType,
      description: this.description,
      requiredSkills: this.requiredSkills,
      priority: this.priority,
      status: this.status,
      assignedTo: this.assignedTo,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
      completedAt: this.completedAt,
      result: this.result
    };
  }
  
  static fromDict(d) {
    return new Task(d);
  }
}

class Conflict {
  constructor({
    conflictId,
    conflictType,
    severity,
    description,
    parties = [],
    detectedAt = new Date().toISOString(),
    resolved = false,
    resolution = null,
    resolvedAt = null
  }) {
    this.conflictId = conflictId;
    this.conflictType = conflictType;
    this.severity = severity;
    this.description = description;
    this.parties = parties;
    this.detectedAt = detectedAt;
    this.resolved = resolved;
    this.resolution = resolution;
    this.resolvedAt = resolvedAt;
  }
  
  toDict() {
    return {
      conflictId: this.conflictId,
      conflictType: this.conflictType,
      severity: this.severity,
      description: this.description,
      parties: this.parties,
      detectedAt: this.detectedAt,
      resolved: this.resolved,
      resolution: this.resolution,
      resolvedAt: this.resolvedAt
    };
  }
  
  static fromDict(d) {
    return new Conflict(d);
  }
}

// ========== Main System ==========

class AgentCollaborationSystem {
  constructor() {
    this._ensureDirs();
    this.agents = {};
    this.tasks = {};
    this.conflicts = [];
    this._loadAgents();
    this._loadTasks();
    this._loadConflicts();
    
    console.log(`✅ Agent 协作系统 v3.1 已初始化 (${Object.keys(this.agents).length} 个 Agent)`);
  }
  
  _ensureDirs() {
    fs.mkdir(COLLAB_DIR, { recursive: true });
  }
  
  async _loadAgents() {
    try {
      if (await fileExists(AGENTS_FILE)) {
        const data = JSON.parse(await fs.readFile(AGENTS_FILE, 'utf-8'));
        this.agents = Object.fromEntries(
          Object.entries(data).map(([k, v]) => [k, Agent.fromDict(v)])
        );
      }
    } catch (e) {
      this.agents = {};
    }
  }
  
  async _saveAgents() {
    const data = Object.fromEntries(
      Object.entries(this.agents).map(([k, v]) => [k, v.toDict()])
    );
    await fs.writeFile(AGENTS_FILE, JSON.stringify(data, null, 2), 'utf-8');
  }
  
  async _loadTasks() {
    try {
      if (await fileExists(TASKS_FILE)) {
        const data = JSON.parse(await fs.readFile(TASKS_FILE, 'utf-8'));
        this.tasks = Object.fromEntries(
          Object.entries(data).map(([k, v]) => [k, Task.fromDict(v)])
        );
      }
    } catch (e) {
      this.tasks = {};
    }
  }
  
  async _saveTasks() {
    const data = Object.fromEntries(
      Object.entries(this.tasks).map(([k, v]) => [k, v.toDict()])
    );
    await fs.writeFile(TASKS_FILE, JSON.stringify(data, null, 2), 'utf-8');
  }
  
  async _loadConflicts() {
    try {
      if (await fileExists(CONFLICTS_FILE)) {
        const data = JSON.parse(await fs.readFile(CONFLICTS_FILE, 'utf-8'));
        this.conflicts = data.map(c => Conflict.fromDict(c));
      }
    } catch (e) {
      this.conflicts = [];
    }
  }
  
  async _saveConflicts() {
    const data = this.conflicts.map(c => c.toDict());
    await fs.writeFile(CONFLICTS_FILE, JSON.stringify(data, null, 2), 'utf-8');
  }
  
  async _logEvent(eventType, data) {
    const event = {
      timestamp: new Date().toISOString(),
      event_type: eventType,
      ...data
    };
    await fs.appendFile(EVENTS_FILE, JSON.stringify(event) + '\n', 'utf-8');
  }
  
  // ===== Agent Management =====
  
  async registerAgent(agentId, name, role, skills, expertise = []) {
    const now = new Date().toISOString();
    const agent = new Agent({
      agentId,
      name,
      role,
      skills: Array.isArray(skills) ? skills : skills.split(',').map(s => s.trim()),
      expertise,
      workload: 0.0,
      status: AgentStatus.ONLINE,
      registeredAt: now,
      lastActive: now
    });
    
    this.agents[agentId] = agent;
    await this._saveAgents();
    await this._logEvent('agent_registered', { agentId, name, role });
    
    console.log(`✅ Agent 注册: ${name} (${agentId})`);
    return agent;
  }
  
  getAgent(agentId) {
    return this.agents[agentId] || null;
  }
  
  listAgents() {
    return Object.values(this.agents);
  }
  
  // ===== Task Management =====
  
  async addTask(taskId, taskType, description, requiredSkills = [], priority = 'normal') {
    const now = new Date().toISOString();
    const task = new Task({
      taskId,
      taskType,
      description,
      requiredSkills: Array.isArray(requiredSkills) ? requiredSkills : requiredSkills.split(',').map(s => s.trim()),
      priority,
      status: TaskStatus.PENDING,
      assignedTo: null,
      createdAt: now,
      updatedAt: now
    });
    
    this.tasks[taskId] = task;
    await this._saveTasks();
    await this._logEvent('task_created', { taskId, taskType });
    
    console.log(`✅ 任务创建: ${taskId} (${taskType})`);
    return task;
  }
  
  async assignTask(taskId, agentId) {
    if (!(taskId in this.tasks) || !(agentId in this.agents)) {
      return false;
    }
    
    const task = this.tasks[taskId];
    const agent = this.agents[agentId];
    
    task.assignedTo = agentId;
    task.status = TaskStatus.ASSIGNED;
    task.updatedAt = new Date().toISOString();
    
    agent.workload = Math.min(1.0, agent.workload + 0.2);
    agent.status = AgentStatus.BUSY;
    
    await this._saveTasks();
    await this._saveAgents();
    await this._logEvent('task_assigned', { taskId, agentId });
    
    console.log(`✅ 任务分配: ${taskId} → ${agent.name}`);
    return true;
  }
  
  async completeTask(taskId, result = null) {
    if (!(taskId in this.tasks)) return;
    
    const task = this.tasks[taskId];
    task.status = TaskStatus.COMPLETED;
    task.result = result;
    task.completedAt = new Date().toISOString();
    task.updatedAt = task.completedAt;
    
    if (task.assignedTo && task.assignedTo in this.agents) {
      const agent = this.agents[task.assignedTo];
      agent.workload = Math.max(0.0, agent.workload - 0.2);
      agent.completedTasks++;
      if (agent.workload < 0.3) {
        agent.status = AgentStatus.ONLINE;
      }
    }
    
    await this._saveTasks();
    await this._saveAgents();
    await this._logEvent('task_completed', { taskId });
    
    console.log(`✅ 任务完成: ${taskId}`);
  }
  
  listTasks(status = null) {
    let tasks = Object.values(this.tasks);
    if (status) {
      tasks = tasks.filter(t => t.status === status);
    }
    return tasks;
  }
  
  // ===== Dynamic Role Assignment =====
  
  recommendAgent(taskType, requiredSkills, strategy = 'skill_match') {
    const candidates = [];
    
    for (const agent of Object.values(this.agents)) {
      if (agent.status === AgentStatus.OFFLINE) continue;
      
      let score;
      if (strategy === 'skill_match') {
        score = requiredSkills.filter(s => agent.skills.includes(s)).length / Math.max(requiredSkills.length, 1);
      } else if (strategy === 'workload_balance') {
        score = 1.0 - agent.workload;
      } else {
        // hybrid
        const skillScore = requiredSkills.filter(s => agent.skills.includes(s)).length / Math.max(requiredSkills.length, 1);
        const workloadScore = 1.0 - agent.workload;
        score = skillScore * 0.7 + workloadScore * 0.3;
      }
      
      candidates.push([agent, score]);
    }
    
    candidates.sort((a, b) => b[1] - a[1]);
    return candidates;
  }
  
  // ===== Conflict Detection =====
  
  detectConflicts() {
    const newConflicts = [];
    
    // Resource conflict detection
    for (const agent of Object.values(this.agents)) {
      if (agent.workload > 0.9) {
        const conflict = new Conflict({
          conflictId: `conf_${new Date().toISOString().replace(/[-:T]/g, '').slice(0, 14)}_${agent.agentId.slice(0, 6)}`,
          conflictType: ConflictType.RESOURCE,
          severity: ConflictSeverity.HIGH,
          description: `Agent ${agent.name} 负载过高: ${(agent.workload * 100).toFixed(0)}%`,
          parties: [agent.agentId]
        });
        newConflicts.push(conflict);
      }
    }
    
    this.conflicts.push(...newConflicts);
    return this.conflicts;
  }
  
  resolveConflict(conflictId, resolution) {
    const conflict = this.conflicts.find(c => c.conflictId === conflictId);
    if (!conflict) return false;
    
    conflict.resolved = true;
    conflict.resolution = resolution;
    conflict.resolvedAt = new Date().toISOString();
    
    return true;
  }
  
  // ===== Broadcast & Events =====
  
  async broadcast(fromAgent, eventType, data = {}) {
    await this._logEvent('broadcast', { from_agent: fromAgent, event_type: eventType, data });
    console.log(`📢 广播: ${fromAgent} -> ${eventType}`);
  }
  
  async makeDecision(context, options, criteria, weights = null) {
    // Simple weighted decision
    const scores = options.map(option => {
      let score = 0;
      criteria.forEach((criterion, i) => {
        const weight = weights ? weights[criterion] || 1 : 1;
        // Simple heuristic scoring
        const optionScore = option.toLowerCase().includes(criterion.toLowerCase()) ? 1 : 0.5;
        score += optionScore * weight;
      });
      return score;
    });
    
    const winner = options[scores.indexOf(Math.max(...scores))];
    
    return {
      context,
      winner,
      scores: Object.fromEntries(options.map((o, i) => [o, scores[i]])),
      timestamp: new Date().toISOString()
    };
  }
  
  // ===== Statistics =====
  
  getStats() {
    const agentStats = Object.values(this.agents).map(a => ({
      name: a.name,
      workload: (a.workload * 100).toFixed(0) + '%',
      completed: a.completedTasks,
      successRate: (a.successRate * 100).toFixed(0) + '%'
    }));
    
    const taskStats = {
      total: Object.keys(this.tasks).length,
      pending: Object.values(this.tasks).filter(t => t.status === TaskStatus.PENDING).length,
      in_progress: Object.values(this.tasks).filter(t => t.status === TaskStatus.IN_PROGRESS).length,
      completed: Object.values(this.tasks).filter(t => t.status === TaskStatus.COMPLETED).length
    };
    
    return {
      agents: agentStats,
      tasks: taskStats,
      conflicts: {
        total: this.conflicts.length,
        unresolved: this.conflicts.filter(c => !c.resolved).length
      }
    };
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
Agent Collaboration System v3.1

Usage:
    node agent_collab_system.js register --id "agent_pm" --name "产品经理" --role "pm" --skills "需求分析,产品设计"
    node agent_collab_system.js list
    node agent_collab_system.js status --id "agent_pm"
    node agent_collab_system.js add-task --id "task_001" --type "development" --desc "开发用户系统"
    node agent_collab_system.js assign --task "task_001" --agent "agent_engineer"
    node agent_collab_system.js complete --task "task_001" --result "完成"
    node agent_collab_system.js recommend --task-type "development" --skills "Python,API"
    node agent_collab_system.js stats
`);
    process.exit(1);
  }
  
  const system = new AgentCollaborationSystem();
  
  switch (command) {
    case 'register': {
      const idIdx = args.indexOf('--id');
      const nameIdx = args.indexOf('--name');
      const roleIdx = args.indexOf('--role');
      const skillsIdx = args.indexOf('--skills');
      
      const id = idIdx !== -1 ? args[idIdx + 1] : null;
      const name = nameIdx !== -1 ? args[nameIdx + 1] : null;
      const role = roleIdx !== -1 ? args[roleIdx + 1] : null;
      const skills = skillsIdx !== -1 ? args[skillsIdx + 1] : '';
      
      if (!id || !name || !role) {
        console.log('❌ 请提供 --id, --name, --role 参数');
        process.exit(1);
      }
      
      await system.registerAgent(id, name, role, skills);
      break;
    }
    
    case 'list': {
      const agents = system.listAgents();
      console.log(`\n👥 Agent 列表 (${agents.length}):\n`);
      for (const agent of agents) {
        console.log(`  [${agent.agentId}] ${agent.name} (${agent.role})`);
        console.log(`    技能: ${agent.skills.join(', ')}`);
        console.log(`    负载: ${(agent.workload * 100).toFixed(0)}% | 状态: ${agent.status}`);
        console.log();
      }
      break;
    }
    
    case 'status': {
      const idIdx = args.indexOf('--id');
      if (idIdx === -1) {
        console.log('❌ 请提供 --id 参数');
        process.exit(1);
      }
      
      const agent = system.getAgent(args[idIdx + 1]);
      if (!agent) {
        console.log('❌ Agent 不存在');
        process.exit(1);
      }
      
      console.log(`\n👤 Agent: ${agent.name}`);
      console.log(`   ID: ${agent.agentId}`);
      console.log(`   角色: ${agent.role}`);
      console.log(`   技能: ${agent.skills.join(', ')}`);
      console.log(`   负载: ${(agent.workload * 100).toFixed(0)}%`);
      console.log(`   状态: ${agent.status}`);
      console.log(`   已完成任务: ${agent.completedTasks}`);
      console.log(`   成功率: ${(agent.successRate * 100).toFixed(0)}%`);
      break;
    }
    
    case 'add-task': {
      const idIdx = args.indexOf('--id');
      const typeIdx = args.indexOf('--type');
      const descIdx = args.indexOf('--desc');
      const skillsIdx = args.indexOf('--skills');
      
      const id = idIdx !== -1 ? args[idIdx + 1] : `task_${Date.now()}`;
      const type = typeIdx !== -1 ? args[typeIdx + 1] : 'general';
      const desc = descIdx !== -1 ? args[descIdx + 1] : '';
      const skills = skillsIdx !== -1 ? args[skillsIdx + 1] : '';
      
      await system.addTask(id, type, desc, skills);
      break;
    }
    
    case 'assign': {
      const taskIdx = args.indexOf('--task');
      const agentIdx = args.indexOf('--agent');
      
      if (taskIdx === -1 || agentIdx === -1) {
        console.log('❌ 请提供 --task 和 --agent 参数');
        process.exit(1);
      }
      
      const success = await system.assignTask(args[taskIdx + 1], args[agentIdx + 1]);
      if (!success) {
        console.log('❌ 分配失败');
      }
      break;
    }
    
    case 'complete': {
      const taskIdx = args.indexOf('--task');
      const resultIdx = args.indexOf('--result');
      
      if (taskIdx === -1) {
        console.log('❌ 请提供 --task 参数');
        process.exit(1);
      }
      
      let result = {};
      if (resultIdx !== -1) {
        try {
          result = JSON.parse(args[resultIdx + 1]);
        } catch {}
      }
      
      await system.completeTask(args[taskIdx + 1], result);
      break;
    }
    
    case 'recommend': {
      const typeIdx = args.indexOf('--task-type');
      const skillsIdx = args.indexOf('--skills');
      const strategyIdx = args.indexOf('--strategy');
      
      const taskType = typeIdx !== -1 ? args[typeIdx + 1] : 'general';
      const skills = skillsIdx !== -1 ? args[skillsIdx + 1].split(',').map(s => s.trim()) : [];
      const strategy = strategyIdx !== -1 ? args[strategyIdx + 1] : 'skill_match';
      
      const candidates = system.recommendAgent(taskType, skills, strategy);
      console.log('\n🎯 推荐 Agent:\n');
      for (const [agent, score] of candidates.slice(0, 5)) {
        console.log(`  ${agent.name}: ${(score * 100).toFixed(0)}% 匹配`);
      }
      break;
    }
    
    case 'stats':
      console.log('\n📊 统计:\n');
      console.log(JSON.stringify(system.getStats(), null, 2));
      break;
    
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
  Agent,
  Task,
  Conflict,
  AgentStatus,
  TaskStatus,
  ConflictType,
  ConflictSeverity,
  AgentCollaborationSystem
};

export default AgentCollaborationSystem;
