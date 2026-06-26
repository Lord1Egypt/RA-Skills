/**
 * Session 管理器 - Session Manager
 * 借鉴 OpenViking 的 Session 管理机制
 */

import { logger } from '../utils/logger.js';
import { VikingURI, URI_TEMPLATES } from '../core/viking_uri.js';

/**
 * Message Part 类型
 */
export class TextPart {
  constructor(text) {
    this.type = 'text';
    this.text = text;
  }
  
  toJSON() {
    return { type: 'text', text: this.text };
  }
}

export class ContextPart {
  constructor(uri, abstract = '') {
    this.type = 'context';
    this.uri = uri;
    this.abstract = abstract;
  }
  
  toJSON() {
    return { type: 'context', uri: this.uri, abstract: this.abstract };
  }
}

export class ToolPart {
  constructor(toolId, input, output, success = true) {
    this.type = 'tool';
    this.toolId = toolId;
    this.input = input;
    this.output = output;
    this.success = success;
  }
  
  toJSON() {
    return {
      type: 'tool',
      toolId: this.toolId,
      input: this.input,
      output: this.output,
      success: this.success
    };
  }
}

/**
 * Message
 */
export class Message {
  constructor(options) {
    this.id = options.id || `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    this.role = options.role;  // 'user' | 'assistant'
    this.parts = options.parts || [];
    this.createdAt = options.createdAt || Date.now();
    this.metadata = options.metadata || {};
  }
  
  addPart(part) {
    this.parts.push(part);
  }
  
  toJSON() {
    return {
      id: this.id,
      role: this.role,
      parts: this.parts.map(p => p.toJSON()),
      createdAt: this.createdAt,
      metadata: this.metadata
    };
  }
}

/**
 * Session
 */
export class Session {
  constructor(options) {
    this.id = options.id;
    this.userId = options.userId;
    this.agentId = options.agentId;
    this.messages = [];
    this.usedContexts = [];
    this.usedSkills = [];
    this.createdAt = Date.now();
    this.updatedAt = Date.now();
    this.compressionIndex = 0;
    this.metadata = options.metadata || {};
    
    // 归档历史
    this.history = [];
  }
  
  /**
   * 添加消息
   */
  addMessage(role, parts) {
    const message = new Message({
      role: role,
      parts: Array.isArray(parts) ? parts : [new TextPart(parts)]
    });
    
    this.messages.push(message);
    this.updatedAt = Date.now();
    
    logger.debug(`[Session] 添加消息: ${role}, ${message.id}`);
    
    return message;
  }
  
  /**
   * 记录使用的上下文
   */
  recordContextUsage(contexts) {
    for (const context of contexts) {
      this.usedContexts.push({
        uri: typeof context === 'string' ? context : context.uri,
        timestamp: Date.now()
      });
    }
    
    this.updatedAt = Date.now();
  }
  
  /**
   * 记录使用的技能
   */
  recordSkillUsage(skill) {
    this.usedSkills.push({
      uri: skill.uri,
      input: skill.input,
      output: skill.output,
      success: skill.success,
      timestamp: Date.now()
    });
    
    this.updatedAt = Date.now();
  }
  
  /**
   * 获取最近 N 条消息
   */
  getRecentMessages(n = 5) {
    return this.messages.slice(-n);
  }
  
  /**
   * 获取会话摘要
   */
  getSummary() {
    const userMessages = this.messages.filter(m => m.role === 'user').length;
    const assistantMessages = this.messages.filter(m => m.role === 'assistant').length;
    
    return {
      id: this.id,
      messageCount: this.messages.length,
      userMessages: userMessages,
      assistantMessages: assistantMessages,
      usedContexts: this.usedContexts.length,
      usedSkills: this.usedSkills.length,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
      compressionIndex: this.compressionIndex
    };
  }
  
  toJSON() {
    return {
      id: this.id,
      userId: this.userId,
      agentId: this.agentId,
      messages: this.messages.map(m => m.toJSON()),
      usedContexts: this.usedContexts,
      usedSkills: this.usedSkills,
      createdAt: this.createdAt,
      updatedAt: this.updatedAt,
      compressionIndex: this.compressionIndex,
      metadata: this.metadata
    };
  }
}

/**
 * Session 管理器
 */
export class SessionManager {
  constructor(options = {}) {
    this.storage = options.storage;
    this.memoryExtractor = options.memoryExtractor;
    this.compressor = options.compressor;
    
    // 配置
    this.maxMessagesBeforeArchive = options.maxMessagesBeforeArchive || 20;
    this.enableAutoArchive = options.enableAutoArchive !== false;
    this.enableMemoryExtraction = options.enableMemoryExtraction !== false;
    
    // Session 缓存
    this.sessions = new Map();
    this.maxCacheSize = options.maxCacheSize || 100;
    
    // 统计
    this.stats = {
      totalSessions: 0,
      totalMessages: 0,
      totalArchives: 0,
      totalMemoryExtractions: 0,
      avgMessagesPerSession: 0
    };
  }
  
  /**
   * 获取或创建 Session
   */
  async getSession(sessionId, options = {}) {
    // 检查缓存
    if (this.sessions.has(sessionId)) {
      return this.sessions.get(sessionId);
    }
    
    // 从存储加载
    let session = null;
    
    if (this.storage) {
      try {
        const data = await this.storage.read(
          URI_TEMPLATES.SESSION_ROOT(sessionId) + 'session.json'
        );
        
        if (data) {
          session = this.deserializeSession(data);
        }
      } catch (error) {
        logger.debug(`[SessionManager] Session 不存在: ${sessionId}`);
      }
    }
    
    // 创建新 Session
    if (!session && options.autoCreate) {
      session = new Session({
        id: sessionId,
        userId: options.userId,
        agentId: options.agentId,
        metadata: options.metadata
      });
      
      this.stats.totalSessions++;
      
      logger.info(`[SessionManager] 创建新 Session: ${sessionId}`);
    }
    
    // 缓存
    if (session) {
      this.sessions.set(sessionId, session);
      
      // 限制缓存大小
      if (this.sessions.size > this.maxCacheSize) {
        const firstKey = this.sessions.keys().next().value;
        this.sessions.delete(firstKey);
      }
    }
    
    return session;
  }
  
  /**
   * 添加消息
   */
  async addMessage(sessionId, role, parts) {
    const session = await this.getSession(sessionId, { autoCreate: true });
    
    if (!session) {
      throw new Error(`Session not found: ${sessionId}`);
    }
    
    const message = session.addMessage(role, parts);
    this.stats.totalMessages++;
    
    // 检查是否需要归档
    if (this.enableAutoArchive && session.messages.length >= this.maxMessagesBeforeArchive) {
      await this.archiveMessages(session);
    }
    
    // 保存
    await this.saveSession(session);
    
    return message;
  }
  
  /**
   * 记录上下文使用
   */
  async recordContextUsage(sessionId, contexts) {
    const session = await this.getSession(sessionId);
    
    if (!session) {
      logger.warn(`[SessionManager] Session 不存在: ${sessionId}`);
      return;
    }
    
    session.recordContextUsage(contexts);
    await this.saveSession(session);
  }
  
  /**
   * 记录技能使用
   */
  async recordSkillUsage(sessionId, skill) {
    const session = await this.getSession(sessionId);
    
    if (!session) {
      logger.warn(`[SessionManager] Session 不存在: ${sessionId}`);
      return;
    }
    
    session.recordSkillUsage(skill);
    await this.saveSession(session);
  }
  
  /**
   * 提交 Session（归档 + 记忆提取）
   */
  async commit(sessionId) {
    const session = await this.getSession(sessionId);
    
    if (!session) {
      throw new Error(`Session not found: ${sessionId}`);
    }
    
    logger.info(`[SessionManager] 提交 Session: ${sessionId}`);
    
    // 1. 归档消息
    const archiveUri = await this.archiveMessages(session);
    
    // 2. 异步提取记忆
    let taskId = null;
    
    if (this.enableMemoryExtraction && this.memoryExtractor) {
      taskId = await this.extractMemories(session);
    }
    
    return {
      status: 'accepted',
      taskId: taskId,
      archiveUri: archiveUri,
      archived: archiveUri !== null
    };
  }
  
  /**
   * 归档消息
   */
  async archiveMessages(session) {
    if (!this.storage || session.messages.length === 0) {
      return null;
    }
    
    const archiveNum = session.compressionIndex + 1;
    const archiveUri = URI_TEMPLATES.SESSION_ARCHIVE(session.id, archiveNum);
    
    logger.info(`[SessionManager] 归档消息到: ${archiveUri}`);
    
    try {
      // 写入消息
      await this.storage.write(
        archiveUri + 'messages.jsonl',
        session.messages.map(m => JSON.stringify(m.toJSON())).join('\n')
      );
      
      // 生成摘要（如果有压缩器）
      if (this.compressor) {
        const summary = await this.generateSessionSummary(session);
        
        await this.storage.write(archiveUri + '.abstract.md', summary.abstract);
        await this.storage.write(archiveUri + '.overview.md', summary.overview);
      }
      
      // 写入完成标记
      await this.storage.write(archiveUri + '.done', JSON.stringify({
        archivedAt: Date.now(),
        messageCount: session.messages.length
      }));
      
      // 更新 Session
      session.history.push({
        archiveNum: archiveNum,
        uri: archiveUri,
        messageCount: session.messages.length,
        archivedAt: Date.now()
      });
      
      session.messages = [];
      session.compressionIndex = archiveNum;
      
      this.stats.totalArchives++;
      
      await this.saveSession(session);
      
      return archiveUri;
      
    } catch (error) {
      logger.error('[SessionManager] 归档失败:', error);
      return null;
    }
  }
  
  /**
   * 生成 Session 摘要
   */
  async generateSessionSummary(session) {
    const messages = session.messages.map(m => {
      const text = m.parts
        .filter(p => p.type === 'text')
        .map(p => p.text)
        .join(' ');
      
      return `${m.role}: ${text}`;
    }).join('\n');
    
    // 简单摘要（实际应该用 LLM）
    const abstract = `Session ${session.id}: ${session.messages.length} messages, ${session.usedContexts.length} contexts used`;
    const overview = `# Session ${session.id}\n\n## Messages\n\n${messages.substring(0, 2000)}...`;
    
    return { abstract, overview };
  }
  
  /**
   * 提取记忆
   */
  async extractMemories(session) {
    if (!this.memoryExtractor) {
      return null;
    }
    
    const taskId = `task_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    logger.info(`[SessionManager] 开始提取记忆，任务 ID: ${taskId}`);
    
    // 异步执行
    setImmediate(async () => {
      try {
        const memories = await this.memoryExtractor.extract(session);
        
        this.stats.totalMemoryExtractions++;
        
        logger.info(`[SessionManager] 记忆提取完成，提取 ${memories.length} 条记忆`);
        
      } catch (error) {
        logger.error('[SessionManager] 记忆提取失败:', error);
      }
    });
    
    return taskId;
  }
  
  /**
   * 保存 Session
   */
  async saveSession(session) {
    if (!this.storage) {
      return;
    }
    
    try {
      await this.storage.write(
        URI_TEMPLATES.SESSION_ROOT(session.id) + 'session.json',
        JSON.stringify(session.toJSON(), null, 2)
      );
      
      // 更新统计
      this.stats.avgMessagesPerSession = 
        (this.stats.avgMessagesPerSession * (this.stats.totalSessions - 1) + session.messages.length) / 
        this.stats.totalSessions;
      
    } catch (error) {
      logger.error('[SessionManager] 保存 Session 失败:', error);
    }
  }
  
  /**
   * 删除 Session
   */
  async deleteSession(sessionId) {
    // 从缓存删除
    this.sessions.delete(sessionId);
    
    // 从存储删除
    if (this.storage) {
      try {
        await this.storage.rm(URI_TEMPLATES.SESSION_ROOT(sessionId));
      } catch (error) {
        logger.error('[SessionManager] 删除 Session 失败:', error);
      }
    }
    
    logger.info(`[SessionManager] 删除 Session: ${sessionId}`);
  }
  
  /**
   * 列出所有 Session
   */
  async listSessions(options = {}) {
    if (!this.storage) {
      return Array.from(this.sessions.values()).map(s => s.getSummary());
    }
    
    try {
      const sessions = await this.storage.ls('viking://session/');
      
      return sessions.map(s => ({
        id: s.name,
        uri: s.uri
      }));
      
    } catch (error) {
      logger.error('[SessionManager] 列出 Session 失败:', error);
      return [];
    }
  }
  
  /**
   * 反序列化 Session
   */
  deserializeSession(data) {
    const parsed = typeof data === 'string' ? JSON.parse(data) : data;
    
    const session = new Session({
      id: parsed.id,
      userId: parsed.userId,
      agentId: parsed.agentId,
      metadata: parsed.metadata
    });
    
    session.createdAt = parsed.createdAt;
    session.updatedAt = parsed.updatedAt;
    session.compressionIndex = parsed.compressionIndex;
    session.usedContexts = parsed.usedContexts || [];
    session.usedSkills = parsed.usedSkills || [];
    session.history = parsed.history || [];
    
    // 反序列化消息
    for (const msg of parsed.messages || []) {
      const message = new Message({
        id: msg.id,
        role: msg.role,
        createdAt: msg.createdAt,
        metadata: msg.metadata
      });
      
      // 反序列化 parts
      for (const part of msg.parts || []) {
        if (part.type === 'text') {
          message.addPart(new TextPart(part.text));
        } else if (part.type === 'context') {
          message.addPart(new ContextPart(part.uri, part.abstract));
        } else if (part.type === 'tool') {
          message.addPart(new ToolPart(part.toolId, part.input, part.output, part.success));
        }
      }
      
      session.messages.push(message);
    }
    
    return session;
  }
  
  /**
   * 获取统计信息
   */
  getStats() {
    return {
      ...this.stats,
      cachedSessions: this.sessions.size
    };
  }
}

/**
 * 获取 Session 管理器实例
 */
let defaultManager = null;

export function getSessionManager(options = {}) {
  if (!defaultManager) {
    defaultManager = new SessionManager(options);
  }
  return defaultManager;
}

export default SessionManager;
