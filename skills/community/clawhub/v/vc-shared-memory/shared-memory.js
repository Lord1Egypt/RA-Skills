#!/usr/bin/env node

/**
 * Shared Memory System - 跨团队、跨窗口、跨会话的统一记忆系统
 * 
 * 核心功能：
 * - 公司公告板：重大决策、战略方向、全员通知
 * - 项目协作空间：跨团队项目进展、任务分配
 * - 知识库：经验教训、最佳实践、技术文档
 * - 员工状态：当前任务、可用状态、协作请求
 * - 跨团队链接：团队间信息共享、协作记录
 * 
 * 设计理念：
 * - 全面架构：从一开始就考虑全面
 * - 细节完善：确保每个功能都有完整实现
 * - 安全可靠：访问控制、审计记录、数据备份
 * - 易于集成：简单的 API，方便与其他系统集成
 */

const fs = require('fs');
const path = require('path');

// ============================================================================
// 基础配置
// ============================================================================

const MEMORY_ROOT = path.join(
  process.env.HOME || process.env.USERPROFILE, 
  '.shared-memory'
);

const CONFIG_FILE = path.join(MEMORY_ROOT, 'config.json');

// 默认配置
const DEFAULT_CONFIG = {
  version: '1.0.0',
  createdAt: new Date().toISOString(),
  maxItemsPerFile: 1000,        // 单文件最大记录数
  autoBackup: true,             // 自动备份
  backupInterval: 100,          // 每写入100次备份一次
  auditEnabled: true,           // 启用审计
  notifyEnabled: true,          // 启用通知（未来扩展）
  retentionDays: 365,           // 数据保留天数
  company: '虚拟公司',
  ceo: '马云'
};

// 数据类型定义
const DATA_TYPES = {
  announcement: {
    file: 'company-board/announcements.json',
    subtypes: ['decision', 'strategy', 'alert', 'notice'],
    fields: ['id', 'type', 'title', 'content', 'author', 'createdAt', 'priority', 'visibleTo', 'readBy', 'tags']
  },
  decision: {
    file: 'company-board/decisions.json',
    fields: ['id', 'title', 'content', 'decidedBy', 'decidedAt', 'impact', 'teams', 'status']
  },
  project: {
    file: 'projects/active',
    fields: ['id', 'name', 'status', 'createdBy', 'createdAt', 'teams', 'members', 'timeline', 'updates', 'tasks', 'decisions', 'artifacts']
  },
  lesson: {
    file: 'knowledge-base/lessons-learned.json',
    fields: ['id', 'category', 'title', 'content', 'learnedBy', 'team', 'learnedAt', 'appliedTo', 'tags', 'importance']
  },
  bestPractice: {
    file: 'knowledge-base/best-practices.json',
    fields: ['id', 'category', 'title', 'content', 'createdBy', 'createdAt', 'appliedCount', 'tags']
  },
  employeeStatus: {
    file: 'employee-status/current-tasks.json',
    fields: ['name', 'team', 'currentTask', 'availability', 'workload', 'lastUpdate']
  },
  collaboration: {
    file: 'cross-team-links/team-sync.json',
    fields: ['id', 'fromTeam', 'toTeam', 'type', 'content', 'createdAt', 'participants']
  },
  meetingNote: {
    file: 'cross-team-links/meeting-notes.json',
    fields: ['id', 'title', 'participants', 'date', 'summary', 'decisions', 'actionItems']
  }
};

// ============================================================================
// 工具函数
// ============================================================================

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
 * 生成唯一 ID
 */
function generateId(type) {
  const timestamp = Date.now();
  const random = Math.floor(Math.random() * 1000).toString().padStart(3, '0');
  const prefix = {
    announcement: 'ann',
    decision: 'dec',
    project: 'proj',
    lesson: 'lesson',
    bestPractice: 'bp',
    collaboration: 'collab',
    meetingNote: 'meet'
  };
  return `${prefix[type] || 'item'}-${timestamp}-${random}`;
}

/**
 * 获取当前时间戳
 */
function getTimestamp() {
  return new Date().toISOString();
}

/**
 * 深拷贝对象
 */
function deepClone(obj) {
  return JSON.parse(JSON.stringify(obj));
}

/**
 * 合并对象（保留原有字段）
 */
function mergeWithDefaults(obj, defaults) {
  return { ...defaults, ...obj };
}

/**
 * 加载 JSON 文件
 */
function loadJsonFile(filePath) {
  if (!fs.existsSync(filePath)) {
    return null;
  }
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    return JSON.parse(content);
  } catch (error) {
    console.error(`Error loading ${filePath}:`, error.message);
    return null;
  }
}

/**
 * 保存 JSON 文件
 */
function saveJsonFile(filePath, data) {
  ensureDir(path.dirname(filePath));
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

/**
 * 按条件过滤数组
 */
function filterItems(items, filter) {
  if (!items || !filter) return items;
  
  return items.filter(item => {
    for (const [key, value] of Object.entries(filter)) {
      // 支持数组匹配（如 tags）
      if (Array.isArray(item[key])) {
        if (!item[key].includes(value)) return false;
      }
      // 支持范围匹配（如 workload）
      else if (typeof value === 'string' && value.startsWith('<')) {
        if (item[key] >= parseFloat(value.slice(1))) return false;
      }
      else if (typeof value === 'string' && value.startsWith('>')) {
        if (item[key] <= parseFloat(value.slice(1))) return false;
      }
      // 普通匹配
      else if (item[key] !== value) return false;
    }
    return true;
  });
}

/**
 * 按字段排序数组
 */
function sortItems(items, field = 'createdAt', order = 'desc') {
  if (!items) return items;
  
  const sorted = [...items].sort((a, b) => {
    const aVal = a[field];
    const bVal = b[field];
    
    if (aVal === undefined) return order === 'desc' ? 1 : -1;
    if (bVal === undefined) return order === 'desc' ? -1 : 1;
    
    // 时间排序
    if (typeof aVal === 'string' && aVal.includes('T')) {
      const aTime = new Date(aVal).getTime();
      const bTime = new Date(bVal).getTime();
      return order === 'desc' ? bTime - aTime : aTime - bTime;
    }
    
    // 数字排序
    if (typeof aVal === 'number') {
      return order === 'desc' ? bVal - aVal : aVal - bVal;
    }
    
    // 字符串排序
    return order === 'desc' 
      ? String(bVal).localeCompare(String(aVal))
      : String(aVal).localeCompare(String(bVal));
  });
  
  return sorted;
}

/**
 * 搜索文本内容
 */
function searchItems(items, query, fields = ['title', 'content', 'tags']) {
  if (!items || !query) return items;
  
  const queryLower = query.toLowerCase();
  
  return items.filter(item => {
    for (const field of fields) {
      const value = item[field];
      if (typeof value === 'string' && value.toLowerCase().includes(queryLower)) {
        return true;
      }
      if (Array.isArray(value)) {
        for (const v of value) {
          if (String(v).toLowerCase().includes(queryLower)) {
            return true;
          }
        }
      }
    }
    return false;
  });
}

// ============================================================================
// 核心类：SharedMemory
// ============================================================================

class SharedMemory {
  constructor() {
    this.config = null;
    this.auditLog = [];
    this.writeCount = 0;
    this._initialize();
  }

  /**
   * 初始化系统
   */
  _initialize() {
    // 确保根目录存在
    ensureDir(MEMORY_ROOT);
    
    // 加载或创建配置
    if (fs.existsSync(CONFIG_FILE)) {
      this.config = loadJsonFile(CONFIG_FILE);
    } else {
      this.config = DEFAULT_CONFIG;
      saveJsonFile(CONFIG_FILE, this.config);
    }
    
    // 确保所有必要目录存在
    this._ensureDirectories();
    
    // 初始化审计日志
    if (this.config.auditEnabled) {
      const auditFile = path.join(MEMORY_ROOT, 'audit-log.json');
      this.auditLog = loadJsonFile(auditFile) || [];
    }
  }

  /**
   * 确保所有必要目录存在
   */
  _ensureDirectories() {
    const dirs = [
      'company-board',
      'projects/active',
      'projects/archived',
      'projects/templates',
      'knowledge-base',
      'employee-status',
      'cross-team-links',
      'backups'
    ];
    
    dirs.forEach(dir => ensureDir(path.join(MEMORY_ROOT, dir)));
    
    // 确保基础文件存在
    this._initBaseFiles();
  }

  /**
   * 初始化基础文件
   */
  _initBaseFiles() {
    const baseFiles = {
      'company-board/announcements.json': { items: [] },
      'company-board/decisions.json': { items: [] },
      'company-board/alerts.json': { items: [] },
      'knowledge-base/lessons-learned.json': { items: [] },
      'knowledge-base/best-practices.json': { items: [] },
      'knowledge-base/technical-docs.json': { items: [] },
      'knowledge-base/market-insights.json': { items: [] },
      'employee-status/current-tasks.json': { employees: [] },
      'employee-status/availability.json': { employees: [] },
      'employee-status/collaboration-requests.json': { requests: [] },
      'cross-team-links/team-sync.json': { syncs: [] },
      'cross-team-links/meeting-notes.json': { notes: [] }
    };
    
    for (const [file, defaultData] of Object.entries(baseFiles)) {
      const fullPath = path.join(MEMORY_ROOT, file);
      if (!fs.existsSync(fullPath)) {
        saveJsonFile(fullPath, defaultData);
      }
    }
  }

  // ========================================================================
  // 核心操作：Write / Read / Update / Delete / Search
  // ========================================================================

  /**
   * 写入数据（核心方法）
   */
  write(options) {
    const { type, data, notify = false } = options;
    
    // 验证类型
    if (!DATA_TYPES[type]) {
      throw new Error(`Unknown type: ${type}`);
    }
    
    // 生成完整记录
    const record = {
      id: generateId(type),
      createdAt: getTimestamp(),
      updatedAt: getTimestamp(),
      ...data
    };
    
    // 获取文件路径
    const typeConfig = DATA_TYPES[type];
    const filePath = path.join(MEMORY_ROOT, typeConfig.file);
    
    // 添加记录（根据类型处理）
    if (type === 'project') {
      // 项目单独保存为文件
      ensureDir(filePath);
      const projectFile = path.join(filePath, `${record.id}.json`);
      saveJsonFile(projectFile, record);
    } else if (type === 'employeeStatus') {
      // 员工状态按名字索引
      let fileData = loadJsonFile(filePath) || { employees: [] };
      const existing = fileData.employees.find(e => e.name === data.name);
      if (existing) {
        Object.assign(existing, record);
      } else {
        fileData.employees.push(record);
      }
      saveJsonFile(filePath, fileData);
    } else if (type === 'collaboration') {
      // 跨团队同步
      let fileData = loadJsonFile(filePath) || { syncs: [] };
      fileData.syncs.push(record);
      saveJsonFile(filePath, fileData);
    } else if (type === 'meetingNote') {
      // 会议纪要
      const meetingFile = path.join(MEMORY_ROOT, 'cross-team-links/meeting-notes.json');
      let fileData = loadJsonFile(meetingFile) || { notes: [] };
      fileData.notes.push(record);
      saveJsonFile(meetingFile, fileData);
    } else {
      // 其他类型追加到 items 数组
      let fileData = loadJsonFile(filePath) || { items: [] };
      fileData.items.push(record);
      
      // 检查是否需要归档（超过最大记录数）
      if (fileData.items.length > this.config.maxItemsPerFile) {
        this._archiveOldItems(type, fileData);
      }
      
      saveJsonFile(filePath, fileData);
    }
    
    // 记录审计
    this._recordAudit('write', type, record.id, data.author || 'unknown');
    
    // 自动备份
    this.writeCount++;
    if (this.config.autoBackup && this.writeCount % this.config.backupInterval === 0) {
      this.backup();
    }
    
    // 触发通知（未来扩展）
    if (notify && this.config.notifyEnabled) {
      this._triggerNotify(type, record);
    }
    
    return record;
  }

  /**
   * 读取数据（核心方法）
   */
  read(options) {
    const { type, filter, limit, sort, sortOrder = 'desc', unreadOnly = false, reader = null } = options;
    
    // 验证类型
    if (!DATA_TYPES[type]) {
      throw new Error(`Unknown type: ${type}`);
    }
    
    // 获取文件路径
    const typeConfig = DATA_TYPES[type];
    const filePath = path.join(MEMORY_ROOT, typeConfig.file);
    
    // 特殊处理：项目类型读取目录下的所有文件
    if (type === 'project') {
      const projectDir = filePath;
      ensureDir(projectDir);
      
      const files = fs.readdirSync(projectDir).filter(f => f.endsWith('.json'));
      
      let projects = files.map(f => loadJsonFile(path.join(projectDir, f)));
      
      // 应用过滤
      if (filter) {
        projects = filterItems(projects, filter);
      }
      
      // 排序
      if (sort) {
        projects = sortItems(projects, sort, sortOrder);
      }
      
      // 限制数量
      if (limit) {
        projects = projects.slice(0, limit);
      }
      
      return projects;
    }
    
    // 加载数据
    let fileData = loadJsonFile(filePath);
    
    // 根据类型获取正确的数据数组
    let items;
    if (type === 'employeeStatus') {
      fileData = fileData || { employees: [] };
      items = fileData.employees;
    } else if (type === 'collaboration') {
      fileData = fileData || { syncs: [] };
      items = fileData.syncs;
    } else if (type === 'meetingNote') {
      fileData = fileData || { notes: [] };
      items = fileData.notes;
    } else {
      fileData = fileData || { items: [] };
      items = fileData.items;
    }
    
    // 应用过滤
    if (filter) {
      items = filterItems(items, filter);
    }
    
    // 只读未读
    if (unreadOnly && reader) {
      items = items.filter(item => {
        const readBy = item.readBy || [];
        return !readBy.includes(reader);
      });
    }
    
    // 排序
    if (sort) {
      items = sortItems(items, sort, sortOrder);
    }
    
    // 限制数量
    if (limit) {
      items = items.slice(0, limit);
    }
    
    // 标记已读（可选）
    if (reader && options.markRead) {
      items.forEach(item => {
        if (!item.readBy) item.readBy = [];
        if (!item.readBy.includes(reader)) {
          item.readBy.push(reader);
        }
      });
      saveJsonFile(filePath, fileData);
    }
    
    return items;
  }

  /**
   * 更新数据（核心方法）
   */
  update(options) {
    const { type, id, updates, by } = options;
    
    // 验证类型
    if (!DATA_TYPES[type]) {
      throw new Error(`Unknown type: ${type}`);
    }
    
    // 获取文件路径
    const typeConfig = DATA_TYPES[type];
    const filePath = path.join(MEMORY_ROOT, typeConfig.file);
    
    // 特殊处理：项目类型
    if (type === 'project') {
      const projectFile = path.join(filePath, `${id}.json`);
      const project = loadJsonFile(projectFile);
      
      if (!project) {
        throw new Error(`Project not found: ${id}`);
      }
      
      // 记录更新历史
      if (!project.updateHistory) {
        project.updateHistory = [];
      }
      
      project.updateHistory.push({
        at: getTimestamp(),
        by: by || 'unknown',
        updates: deepClone(updates)
      });
      
      // 应用更新
      Object.assign(project, updates, { updatedAt: getTimestamp() });
      
      saveJsonFile(projectFile, project);
      
      this._recordAudit('update', type, id, by || 'unknown');
      
      return project;
    }
    
    // 加载数据
    const fileData = loadJsonFile(filePath);
    if (!fileData) {
      throw new Error(`File not found for type: ${type}`);
    }
    
    // 查找记录
    const items = type === 'employeeStatus' ? fileData.employees : fileData.items;
    const index = type === 'employeeStatus' 
      ? items.findIndex(i => i.name === id)
      : items.findIndex(i => i.id === id);
    
    if (index === -1) {
      throw new Error(`Record not found: ${id}`);
    }
    
    // 应用更新
    const original = deepClone(items[index]);
    items[index] = mergeWithDefaults(updates, items[index]);
    items[index].updatedAt = getTimestamp();
    items[index].updatedBy = by || 'unknown';
    
    // 保存文件
    saveJsonFile(filePath, fileData);
    
    // 记录审计
    this._recordAudit('update', type, id, by || 'unknown');
    
    return items[index];
  }

  /**
   * 删除数据（核心方法）
   */
  delete(options) {
    const { type, id, by, archive = true } = options;
    
    // 验证类型
    if (!DATA_TYPES[type]) {
      throw new Error(`Unknown type: ${type}`);
    }
    
    // 获取文件路径
    const typeConfig = DATA_TYPES[type];
    const filePath = path.join(MEMORY_ROOT, typeConfig.file);
    
    // 特殊处理：项目类型
    if (type === 'project') {
      const projectFile = path.join(filePath, `${id}.json`);
      const project = loadJsonFile(projectFile);
      
      if (!project) {
        throw new Error(`Project not found: ${id}`);
      }
      
      // 归档而不是删除
      if (archive) {
        const archiveFile = path.join(MEMORY_ROOT, 'projects/archived', `${id}.json`);
        project.status = 'archived';
        project.archivedAt = getTimestamp();
        project.archivedBy = by || 'unknown';
        saveJsonFile(archiveFile, project);
      }
      
      // 删除原文件
      fs.unlinkSync(projectFile);
      
      this._recordAudit('delete', type, id, by || 'unknown');
      
      return { success: true, archived: archive };
    }
    
    // 加载数据
    const fileData = loadJsonFile(filePath);
    if (!fileData) {
      throw new Error(`File not found for type: ${type}`);
    }
    
    // 查找记录
    const items = type === 'employeeStatus' ? fileData.employees : fileData.items;
    const index = type === 'employeeStatus' 
      ? items.findIndex(i => i.name === id)
      : items.findIndex(i => i.id === id);
    
    if (index === -1) {
      throw new Error(`Record not found: ${id}`);
    }
    
    // 保存删除的记录用于返回
    const deleted = deepClone(items[index]);
    
    // 归档
    if (archive && type !== 'employeeStatus') {
      const archiveDir = path.join(MEMORY_ROOT, 'archives', typeConfig.file.replace('/', '-'));
      ensureDir(archiveDir);
      const archiveFile = path.join(archiveDir, `${id}.json`);
      deleted.archivedAt = getTimestamp();
      deleted.archivedBy = by || 'unknown';
      saveJsonFile(archiveFile, deleted);
    }
    
    // 删除记录
    items.splice(index, 1);
    
    // 保存文件
    saveJsonFile(filePath, fileData);
    
    // 记录审计
    this._recordAudit('delete', type, id, by || 'unknown');
    
    return { success: true, archived: archive, record: deleted };
  }

  /**
   * 搜索数据（核心方法）
   */
  search(options) {
    const { query, types, filter, limit = 10, fields } = options;
    
    const results = [];
    
    // 如果没有指定类型，搜索所有类型
    const searchTypes = types || Object.keys(DATA_TYPES);
    
    for (const type of searchTypes) {
      if (!DATA_TYPES[type]) continue;
      
      try {
        const items = this.read({ type, filter });
        const matched = searchItems(items, query, fields);
        
        matched.forEach(item => {
          results.push({ ...item, _type: type, _matched: true });
        });
      } catch (error) {
        // 忽略错误，继续搜索其他类型
      }
    }
    
    // 排序结果（按相关度，这里简单按时间排序）
    const sorted = sortItems(results, 'createdAt', 'desc');
    
    // 限制数量
    return sorted.slice(0, limit);
  }

  // ========================================================================
  // 专用 API：公告板
  // ========================================================================

  /**
   * 发布公告
   */
  announce(options) {
    const { title, content, type = 'notice', priority = 'medium', visibleTo = ['all'], author } = options;
    
    return this.write({
      type: 'announcement',
      data: {
        type,
        title,
        content,
        author,
        priority,
        visibleTo,
        readBy: [],
        tags: []
      },
      notify: priority === 'critical' || priority === 'high'
    });
  }

  /**
   * 获取公告
   */
  getAnnouncements(options = {}) {
    const { unreadOnly = false, reader, limit = 10, priority } = options;
    
    return this.read({
      type: 'announcement',
      filter: priority ? { priority } : undefined,
      unreadOnly,
      reader,
      limit,
      sort: 'createdAt'
    });
  }

  /**
   * 标记公告已读
   */
  markRead(announcementId, reader) {
    return this.update({
      type: 'announcement',
      id: announcementId,
      updates: {
        readBy: (this.read({ type: 'announcement', filter: { id: announcementId } })[0]?.readBy || []).concat(reader)
      },
      by: reader
    });
  }

  // ========================================================================
  // 专用 API：项目协作
  // ========================================================================

  /**
   * 创建项目
   */
  createProject(options) {
    const { name, teams, members, timeline, createdBy } = options;
    
    return this.write({
      type: 'project',
      data: {
        name,
        status: 'active',
        createdBy,
        teams: teams || [],
        members: members || [],
        timeline: timeline || { startDate: getTimestamp() },
        updates: [],
        tasks: [],
        decisions: [],
        artifacts: [],
        milestones: []
      }
    });
  }

  /**
   * 更新项目进展
   */
  updateProject(projectId, options) {
    const { content, type = 'progress', by, notify = [] } = options;
    
    const project = this.read({ type: 'project', filter: { id: projectId } })[0];
    
    if (!project) {
      throw new Error(`Project not found: ${projectId}`);
    }
    
    const updateRecord = {
      id: generateId('update'),
      by,
      at: getTimestamp(),
      content,
      type,
      notify
    };
    
    project.updates.push(updateRecord);
    
    return this.update({
      type: 'project',
      id: projectId,
      updates: { updates: project.updates },
      by
    });
  }

  /**
   * 分配任务
   */
  assignTask(projectId, options) {
    const { to, task, by } = options;
    
    const project = this.read({ type: 'project', filter: { id: projectId } })[0];
    
    if (!project) {
      throw new Error(`Project not found: ${projectId}`);
    }
    
    const taskRecord = {
      id: generateId('task'),
      assignedTo: to,
      assignedBy: by,
      assignedAt: getTimestamp(),
      ...task,
      status: 'assigned'
    };
    
    project.tasks.push(taskRecord);
    
    return this.update({
      type: 'project',
      id: projectId,
      updates: { tasks: project.tasks },
      by
    });
  }

  /**
   * 获取项目列表
   */
  getProjects(options = {}) {
    const { status, limit = 10 } = options;
    
    return this.read({
      type: 'project',
      filter: status ? { status } : undefined,
      limit,
      sort: 'createdAt'
    });
  }

  /**
   * 归档项目
   */
  archiveProject(projectId, by) {
    return this.update({
      type: 'project',
      id: projectId,
      updates: { status: 'archived' },
      by
    });
  }

  // ========================================================================
  // 专用 API：知识库
  // ========================================================================

  /**
   * 记录经验教训
   */
  recordLesson(options) {
    const { category, title, content, learnedBy, team, appliedTo, tags, importance = 'medium' } = options;
    
    return this.write({
      type: 'lesson',
      data: {
        category,
        title,
        content,
        learnedBy,
        team,
        appliedTo: appliedTo || [],
        tags: tags || [],
        importance
      }
    });
  }

  /**
   * 添加最佳实践
   */
  addBestPractice(options) {
    const { category, title, content, createdBy, tags } = options;
    
    return this.write({
      type: 'bestPractice',
      data: {
        category,
        title,
        content,
        createdBy,
        appliedCount: 0,
        tags: tags || []
      }
    });
  }

  /**
   * 搜索知识库
   */
  searchKnowledge(options) {
    const { query, category, limit = 10 } = options;
    
    // 搜索经验教训和最佳实践
    const lessons = this.search({
      query,
      types: ['lesson', 'bestPractice'],
      filter: category ? { category } : undefined,
      limit
    });
    
    return lessons;
  }

  /**
   * 获取最佳实践
   */
  getBestPractices(options = {}) {
    const { category, limit = 10 } = options;
    
    return this.read({
      type: 'bestPractice',
      filter: category ? { category } : undefined,
      limit,
      sort: 'appliedCount',
      sortOrder: 'desc'
    });
  }

  // ========================================================================
  // 专用 API：员工状态
  // ========================================================================

  /**
   * 更新员工状态
   */
  updateEmployeeStatus(options) {
    const { name, team, task, availability = 'available', workload = 0 } = options;
    
    return this.write({
      type: 'employeeStatus',
      data: {
        name,
        team,
        currentTask: task ? {
          id: generateId('task'),
          description: task.description || task,
          project: task.project,
          startedAt: getTimestamp(),
          status: 'in-progress'
        } : null,
        availability,
        workload,
        lastUpdate: getTimestamp()
      }
    });
  }

  /**
   * 查询可用员工
   */
  findAvailableEmployees(options = {}) {
    const { team, workload = '<0.5' } = options;
    
    return this.read({
      type: 'employeeStatus',
      filter: { 
        ...(team ? { team } : {}),
        availability: 'available',
        workload
      },
      sort: 'workload',
      sortOrder: 'asc'
    });
  }

  /**
   * 发送协作请求
   */
  requestCollaboration(options) {
    const { from, to, project, reason } = options;
    
    const filePath = path.join(MEMORY_ROOT, 'employee-status/collaboration-requests.json');
    const data = loadJsonFile(filePath) || { requests: [] };
    
    const request = {
      id: generateId('collab-request'),
      from,
      to,
      project,
      reason,
      status: 'pending',
      createdAt: getTimestamp()
    };
    
    data.requests.push(request);
    saveJsonFile(filePath, data);
    
    return request;
  }

  /**
   * 获取员工状态列表
   */
  getEmployeeStatuses(options = {}) {
    const { team, availability, limit = 35 } = options;
    
    return this.read({
      type: 'employeeStatus',
      filter: {
        ...(team ? { team } : {}),
        ...(availability ? { availability } : {})
      },
      limit,
      sort: 'lastUpdate'
    });
  }

  // ========================================================================
  // 专用 API：跨团队链接
  // ========================================================================

  /**
   * 记录跨团队同步
   */
  recordTeamSync(options) {
    const { fromTeam, toTeam, type, content, participants } = options;
    
    return this.write({
      type: 'collaboration',
      data: {
        fromTeam,
        toTeam,
        type,
        content,
        participants: participants || []
      }
    });
  }

  /**
   * 记录会议纪要
   */
  recordMeeting(options) {
    const { title, participants, date, summary, decisions, actionItems } = options;
    
    return this.write({
      type: 'meetingNote',
      data: {
        title,
        participants: participants || [],
        date: date || getTimestamp(),
        summary,
        decisions: decisions || [],
        actionItems: actionItems || []
      }
    });
  }

  /**
   * 获取跨团队链接
   */
  getCrossTeamLinks(options = {}) {
    const { fromTeam, toTeam, limit = 10 } = options;
    
    const syncs = this.read({
      type: 'collaboration',
      filter: fromTeam ? { fromTeam } : undefined,
      limit
    });
    
    const notes = this.read({
      type: 'meetingNote',
      limit
    });
    
    return { syncs, notes };
  }

  // ========================================================================
  // 辅助功能：为员工构建上下文
  // ========================================================================

  /**
   * 为员工构建记忆上下文（核心功能）
   * 用于 virtual-company 集成
   */
  getContextFor(employeeName, options = {}) {
    const { team, includeProjects = true, includeLessons = true, includeAnnouncements = true } = options;
    
    let context = `## 🧠 共享记忆上下文\n\n`;
    
    // 1. 公司公告（高优先级）
    if (includeAnnouncements) {
      const announcements = this.getAnnouncements({ limit: 5 });
      if (announcements.length > 0) {
        context += `### 📢 公司公告 (${announcements.length}条)\n`;
        announcements.forEach(a => {
          context += `- **${a.title}** (${a.priority}) - ${a.author}\n`;
          if (a.content) {
            context += `  > ${a.content.slice(0, 100)}${a.content.length > 100 ? '...' : ''}\n`;
          }
        });
        context += `\n`;
      }
    }
    
    // 2. 相关项目
    if (includeProjects) {
      const projects = this.getProjects({ status: 'active', limit: 5 });
      const relevantProjects = projects.filter(p => {
        // 检查是否是项目成员
        return p.members?.some(m => m.name === employeeName) ||
               p.teams?.includes(team);
      });
      
      if (relevantProjects.length > 0) {
        context += `### 📋 相关项目 (${relevantProjects.length}个)\n`;
        relevantProjects.forEach(p => {
          context += `- **${p.name}** (${p.status})\n`;
          // 最近进展
          if (p.updates?.length > 0) {
            const recentUpdates = p.updates.slice(-3);
            context += `  > 最近进展:\n`;
            recentUpdates.forEach(u => {
              context += `    - ${u.by}: ${u.content.slice(0, 50)}...\n`;
            });
          }
        });
        context += `\n`;
      }
    }
    
    // 3. 相关经验教训
    if (includeLessons) {
      const lessons = this.searchKnowledge({
        query: employeeName,
        limit: 3
      });
      
      if (lessons.length > 0) {
        context += `### 💡 相关经验 (${lessons.length}条)\n`;
        lessons.forEach(l => {
          context += `- **${l.title}** (${l.importance || 'medium'})\n`;
          if (l.content) {
            context += `  > ${l.content.slice(0, 80)}...\n`;
          }
        });
        context += `\n`;
      }
    }
    
    // 4. 员工自身状态
    const status = this.read({
      type: 'employeeStatus',
      filter: { name: employeeName }
    })[0];
    
    if (status) {
      context += `### 👤 当前状态\n`;
      context += `- 团队: ${status.team}\n`;
      context += `- 可用性: ${status.availability}\n`;
      context += `- 工作负载: ${(status.workload * 100).toFixed(0)}%\n`;
      if (status.currentTask) {
        context += `- 当前任务: ${status.currentTask.description}\n`;
      }
      context += `\n`;
    }
    
    return context;
  }

  // ========================================================================
  // 辅助功能：备份、恢复、审计
  // ========================================================================

  /**
   * 备份数据
   */
  backup() {
    const timestamp = getTimestamp().replace(/[:.]/g, '-').slice(0, 19);
    const backupDir = path.join(MEMORY_ROOT, 'backups', timestamp);
    
    ensureDir(backupDir);
    
    // 复制所有文件到备份目录
    const dirsToBackup = [
      'company-board',
      'knowledge-base',
      'employee-status',
      'cross-team-links'
    ];
    
    dirsToBackup.forEach(dir => {
      const sourceDir = path.join(MEMORY_ROOT, dir);
      const targetDir = path.join(backupDir, dir);
      
      if (fs.existsSync(sourceDir)) {
        ensureDir(targetDir);
        
        const files = fs.readdirSync(sourceDir);
        files.forEach(file => {
          const sourceFile = path.join(sourceDir, file);
          const targetFile = path.join(targetDir, file);
          
          if (fs.statSync(sourceFile).isFile()) {
            fs.copyFileSync(sourceFile, targetFile);
          }
        });
      }
    });
    
    // 备份项目文件
    const projectDir = path.join(MEMORY_ROOT, 'projects/active');
    if (fs.existsSync(projectDir)) {
      const targetProjectDir = path.join(backupDir, 'projects/active');
      ensureDir(targetProjectDir);
      
      const projectFiles = fs.readdirSync(projectDir).filter(f => f.endsWith('.json'));
      projectFiles.forEach(file => {
        fs.copyFileSync(
          path.join(projectDir, file),
          path.join(targetProjectDir, file)
        );
      });
    }
    
    // 记录备份信息
    const backupInfo = {
      timestamp,
      createdAt: getTimestamp(),
      filesCount: this._countBackupFiles(backupDir),
      trigger: 'auto'
    };
    
    saveJsonFile(path.join(backupDir, 'backup-info.json'), backupInfo);
    
    this._recordAudit('backup', 'system', timestamp, 'system');
    
    return backupInfo;
  }

  /**
   * 恢复数据
   */
  restore(backupTimestamp) {
    const backupDir = path.join(MEMORY_ROOT, 'backups', backupTimestamp);
    
    if (!fs.existsSync(backupDir)) {
      throw new Error(`Backup not found: ${backupTimestamp}`);
    }
    
    // 清空现有数据（保留配置）
    const dirsToClear = [
      'company-board',
      'knowledge-base',
      'employee-status',
      'cross-team-links'
    ];
    
    dirsToClear.forEach(dir => {
      const targetDir = path.join(MEMORY_ROOT, dir);
      if (fs.existsSync(targetDir)) {
        const files = fs.readdirSync(targetDir);
        files.forEach(file => {
          fs.unlinkSync(path.join(targetDir, file));
        });
      }
    });
    
    // 从备份恢复
    const dirsToRestore = [
      'company-board',
      'knowledge-base',
      'employee-status',
      'cross-team-links',
      'projects'
    ];
    
    dirsToRestore.forEach(dir => {
      const sourceDir = path.join(backupDir, dir);
      if (fs.existsSync(sourceDir)) {
        const targetDir = path.join(MEMORY_ROOT, dir);
        ensureDir(targetDir);
        
        const files = fs.readdirSync(sourceDir);
        files.forEach(file => {
          const sourceFile = path.join(sourceDir, file);
          const targetFile = path.join(targetDir, file);
          
          if (fs.statSync(sourceFile).isFile()) {
            fs.copyFileSync(sourceFile, targetFile);
          }
        });
      }
    });
    
    this._recordAudit('restore', 'system', backupTimestamp, 'system');
    
    return { success: true, restoredFrom: backupTimestamp };
  }

  /**
   * 获取备份列表
   */
  listBackups() {
    const backupRoot = path.join(MEMORY_ROOT, 'backups');
    
    if (!fs.existsSync(backupRoot)) {
      return [];
    }
    
    const backups = fs.readdirSync(backupRoot)
      .filter(dir => fs.statSync(path.join(backupRoot, dir)).isDirectory())
      .map(dir => {
        const infoFile = path.join(backupRoot, dir, 'backup-info.json');
        const info = loadJsonFile(infoFile);
        return {
          timestamp: dir,
          ...info,
          exists: fs.existsSync(infoFile)
        };
      });
    
    return sortItems(backups, 'createdAt', 'desc');
  }

  /**
   * 获取统计数据
   */
  getStats() {
    const stats = {
      announcements: this.read({ type: 'announcement' }).length,
      projects: {
        active: this.read({ type: 'project', filter: { status: 'active' } }).length,
        archived: this.read({ type: 'project', filter: { status: 'archived' } }).length
      },
      lessons: this.read({ type: 'lesson' }).length,
      bestPractices: this.read({ type: 'bestPractice' }).length,
      employees: {
        total: this.read({ type: 'employeeStatus' }).length,
        available: this.read({ type: 'employeeStatus', filter: { availability: 'available' } }).length,
        busy: this.read({ type: 'employeeStatus', filter: { availability: 'busy' } }).length
      },
      collaborations: this.read({ type: 'collaboration' }).length,
      meetingNotes: this.read({ type: 'meetingNote' }).length,
      auditLog: this.auditLog.length,
      writeCount: this.writeCount,
      backups: this.listBackups().length
    };
    
    return stats;
  }

  // ========================================================================
  // 内部方法
  // ========================================================================

  /**
   * 记录审计日志
   */
  _recordAudit(action, type, id, by) {
    if (!this.config.auditEnabled) return;
    
    const entry = {
      action,
      type,
      id,
      by,
      at: getTimestamp()
    };
    
    this.auditLog.push(entry);
    
    // 保存审计日志
    const auditFile = path.join(MEMORY_ROOT, 'audit-log.json');
    saveJsonFile(auditFile, this.auditLog);
  }

  /**
   * 归档旧记录
   */
  _archiveOldItems(type, fileData) {
    const archiveCount = Math.floor(this.config.maxItemsPerFile * 0.2);
    const itemsToArchive = fileData.items.slice(0, archiveCount);
    
    const archiveDir = path.join(MEMORY_ROOT, 'archives', type);
    ensureDir(archiveDir);
    
    const archiveFile = path.join(archiveDir, `archive-${getTimestamp().slice(0, 10)}.json`);
    
    // 加载已有归档
    let archiveData = loadJsonFile(archiveFile) || { items: [] };
    archiveData.items.push(...itemsToArchive);
    
    saveJsonFile(archiveFile, archiveData);
    
    // 从主文件移除
    fileData.items = fileData.items.slice(archiveCount);
  }

  /**
   * 触发通知（未来扩展）
   */
  _triggerNotify(type, record) {
    // TODO: 飞书机器人通知
    // TODO: 子代理 sessions_send
    console.log(`[Notify] ${type}: ${record.title || record.id}`);
  }

  /**
   * 计算备份文件数
   */
  _countBackupFiles(dir) {
    let count = 0;
    
    const items = fs.readdirSync(dir);
    items.forEach(item => {
      const fullPath = path.join(dir, item);
      if (fs.statSync(fullPath).isFile() && item.endsWith('.json')) {
        count++;
      } else if (fs.statSync(fullPath).isDirectory()) {
        count += this._countBackupFiles(fullPath);
      }
    });
    
    return count;
  }
}

// ============================================================================
// CLI 工具
// ============================================================================

function printStats(sm) {
  const stats = sm.getStats();
  
  console.log('\n┌─────────────────────────────────────┐');
  console.log('│ 🧠 Shared Memory Statistics         │');
  console.log('├─────────────────────────────────────┤');
  console.log(`│ 📢 公告板: ${stats.announcements} 条                      │`);
  console.log(`│ 📋 项目: ${stats.projects.active} 个活跃, ${stats.projects.archived} 个归档          │`);
  console.log(`│ 💡 知识库: ${stats.lessons} 条经验, ${stats.bestPractices} 条最佳实践   │`);
  console.log(`│ 👥 员工: ${stats.employees.total} 人, ${stats.employees.busy} 人忙碌, ${stats.employees.available} 人空闲 │`);
  console.log(`│ 🔗 跨团队链接: ${stats.collaborations} 条                  │`);
  console.log(`│ 📝 总写入: ${stats.writeCount} 次                     │`);
  console.log(`│ 💾 备份: ${stats.backups} 个                        │`);
  console.log('└─────────────────────────────────────┘');
}

function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  const sm = new SharedMemory();
  
  if (!command) {
    console.log('Shared Memory System v1.0.0');
    console.log('');
    console.log('用法:');
    console.log('  node shared-memory.js stats              # 查看统计');
    console.log('  node shared-memory.js backup             # 创建备份');
    console.log('  node shared-memory.js list-backups       # 查看备份列表');
    console.log('  node shared-memory.js restore <timestamp> # 恢复备份');
    console.log('  node shared-memory.js search <query>     # 搜索');
    console.log('  node shared-memory.js context <员工名>   # 获取员工上下文');
    console.log('');
    console.log('公告板:');
    console.log('  node shared-memory.js announce list');
    console.log('  node shared-memory.js announce add "标题" "内容" --priority high');
    console.log('');
    console.log('项目:');
    console.log('  node shared-memory.js project list');
    console.log('  node shared-memory.js project create "名称" --teams "A,B"');
    console.log('');
    console.log('知识库:');
    console.log('  node shared-memory.js knowledge list');
    console.log('  node shared-memory.js knowledge add lesson "标题" "内容"');
    console.log('');
    console.log('员工:');
    console.log('  node shared-memory.js status list');
    console.log('  node shared-memory.js status update "员工名" --task "任务"');
    printStats(sm);
    process.exit(0);
  }
  
  switch (command) {
    case 'stats':
      printStats(sm);
      break;
      
    case 'backup':
      const backupInfo = sm.backup();
      console.log(`✅ 备份已创建: ${backupInfo.timestamp}`);
      console.log(`   文件数: ${backupInfo.filesCount}`);
      break;
      
    case 'list-backups':
      const backups = sm.listBackups();
      console.log('\n💾 备份列表:');
      backups.forEach(b => {
        console.log(`  - ${b.timestamp} (${b.filesCount} 文件)`);
      });
      break;
      
    case 'restore':
      const restoreTs = args[1];
      if (!restoreTs) {
        console.log('用法: node shared-memory.js restore <timestamp>');
        process.exit(1);
      }
      const restoreResult = sm.restore(restoreTs);
      console.log(`✅ 已从 ${restoreTs} 恢复`);
      break;
      
    case 'search':
      const query = args[1];
      if (!query) {
        console.log('用法: node shared-memory.js search <query>');
        process.exit(1);
      }
      const searchResults = sm.search({ query, limit: 10 });
      console.log(`\n🔍 搜索结果 (${searchResults.length}条):`);
      searchResults.forEach(r => {
        console.log(`  - [${r._type}] ${r.title}`);
      });
      break;
      
    case 'context':
      const employee = args[1];
      if (!employee) {
        console.log('用法: node shared-memory.js context <员工名>');
        process.exit(1);
      }
      const context = sm.getContextFor(employee);
      console.log(context);
      break;
      
    case 'announce':
      if (args[1] === 'list') {
        const announcements = sm.getAnnouncements({ limit: 10 });
        console.log('\n📢 公告列表:');
        announcements.forEach(a => {
          console.log(`  - ${a.title} (${a.priority}) - ${a.author}`);
        });
      } else if (args[1] === 'add') {
        const title = args[2];
        const content = args[3];
        const priority = args.includes('--priority') ? args[args.indexOf('--priority') + 1] : 'medium';
        sm.announce({ title, content, priority, author: 'CLI' });
        console.log(`✅ 公告已添加: ${title}`);
      }
      break;
      
    case 'project':
      if (args[1] === 'list') {
        const projects = sm.getProjects({ limit: 10 });
        console.log('\n📋 项目列表:');
        projects.forEach(p => {
          console.log(`  - ${p.name} (${p.status})`);
        });
      } else if (args[1] === 'create') {
        const name = args[2];
        const teams = args.includes('--teams') ? args[args.indexOf('--teams') + 1].split(',') : [];
        sm.createProject({ name, teams, createdBy: 'CLI' });
        console.log(`✅ 项目已创建: ${name}`);
      }
      break;
      
    case 'knowledge':
      if (args[1] === 'list') {
        const lessons = sm.read({ type: 'lesson', limit: 10 });
        console.log('\n💡 经验教训:');
        lessons.forEach(l => {
          console.log(`  - ${l.title} (${l.importance})`);
        });
      } else if (args[1] === 'add' && args[2] === 'lesson') {
        const title = args[3];
        const content = args[4];
        const category = args.includes('--category') ? args[args.indexOf('--category') + 1] : '其他';
        sm.recordLesson({ title, content, category, learnedBy: 'CLI' });
        console.log(`✅ 经验已记录: ${title}`);
      }
      break;
      
    case 'status':
      if (args[1] === 'list') {
        const employees = sm.getEmployeeStatuses({ limit: 35 });
        console.log('\n👥 员工状态:');
        employees.forEach(e => {
          console.log(`  - ${e.name} (${e.team}) - ${e.availability} (${(e.workload * 100).toFixed(0)}%)`);
        });
      } else if (args[1] === 'update') {
        const name = args[2];
        const task = args.includes('--task') ? args[args.indexOf('--task') + 1] : null;
        const availability = args.includes('--busy') ? 'busy' : args.includes('--available') ? 'available' : 'available';
        sm.updateEmployeeStatus({ name, task, availability });
        console.log(`✅ 状态已更新: ${name}`);
      }
      break;
      
    default:
      console.log('未知命令:', command);
      printStats(sm);
  }
}

// 只在直接运行时执行 CLI
if (require.main === module) {
  main();
}

module.exports = { SharedMemory };