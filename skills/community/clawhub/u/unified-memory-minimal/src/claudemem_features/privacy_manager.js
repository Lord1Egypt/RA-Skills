/**
 * 隐私控制系统 - Claude-Mem 风格
 * 
 * 功能：
 * 1. 隐私设置管理
 * 2. 记忆保留期限控制
 * 3. 批量删除记忆
 * 4. 记忆导出/导入
 * 5. 敏感信息过滤
 */

import { logger } from '../utils/logger.js';
import { createHash } from 'crypto';

export class PrivacyManager {
  constructor(storage, memoryEditor) {
    this.storage = storage;
    this.memoryEditor = memoryEditor;
    this.logger = logger.child({ module: 'privacy_manager' });
  }

  /**
   * 获取用户的隐私设置
   * @param {string} userId - 用户 ID
   * @returns {Promise<Object>} 隐私设置
   */
  async getPrivacySettings(userId) {
    try {
      const settings = await this.storage.findOne('privacy_settings', { userId });
      
      if (!settings) {
        // 返回默认设置
        return this.getDefaultSettings(userId);
      }
      
      return settings;
      
    } catch (error) {
      this.logger.error('Failed to get privacy settings', { error, userId });
      return this.getDefaultSettings(userId);
    }
  }

  /**
   * 获取默认隐私设置
   * @param {string} userId - 用户 ID
   * @returns {Object} 默认设置
   */
  getDefaultSettings(userId) {
    return {
      userId,
      autoSave: true,           // 自动保存记忆
      retentionDays: 90,        // 保留 90 天
      allowSensitive: false,    // 不保存敏感信息
      exportable: true,         // 允许导出
      shareable: false,         // 不允许分享
      anonymize: true,          // 匿名化处理
      
      // 敏感信息检测
      detectSensitive: true,
      sensitiveCategories: ['personal', 'financial', 'health', 'credentials'],
      
      // 自动清理
      autoCleanup: true,
      cleanupFrequency: 'weekly', // 每周清理
      cleanupThreshold: 1000,    // 超过1000条时清理
      
      // 通知设置
      notifyOnExport: true,
      notifyOnDelete: true,
      notifyOnSensitive: true,
      
      // 审计日志
      auditLogging: true,
      logRetentionDays: 180,
      
      createdAt: new Date(),
      updatedAt: new Date()
    };
  }

  /**
   * 更新隐私设置
   * @param {string} userId - 用户 ID
   * @param {Object} updates - 更新内容
   * @returns {Promise<Object>} 更新后的设置
   */
  async updateSettings(userId, updates) {
    try {
      // 验证更新字段
      const allowedFields = [
        'autoSave', 'retentionDays', 'allowSensitive', 'exportable', 'shareable', 'anonymize',
        'detectSensitive', 'sensitiveCategories', 'autoCleanup', 'cleanupFrequency', 'cleanupThreshold',
        'notifyOnExport', 'notifyOnDelete', 'notifyOnSensitive', 'auditLogging', 'logRetentionDays'
      ];
      
      const validUpdates = {};
      for (const [key, value] of Object.entries(updates)) {
        if (allowedFields.includes(key)) {
          validUpdates[key] = value;
        }
      }
      
      validUpdates.updatedAt = new Date();
      
      // 更新或创建设置
      const settings = await this.storage.findOneAndUpdate(
        'privacy_settings',
        { userId },
        { $set: validUpdates },
        { upsert: true, returnDocument: 'after' }
      );
      
      // 记录审计日志
      if (settings.auditLogging) {
        await this.logAudit(userId, 'settings_updated', {
          changes: Object.keys(updates),
          newValues: updates
        });
      }
      
      this.logger.info('Privacy settings updated', { userId, updates: Object.keys(updates) });
      
      return settings;
      
    } catch (error) {
      this.logger.error('Failed to update privacy settings', { error, userId, updates });
      throw error;
    }
  }

  /**
   * 批量删除记忆
   * @param {string} userId - 用户 ID
   * @param {Object} options - 选项
   * @param {string} options.category - 按分类删除
   * @param {Date} options.beforeDate - 删除此日期之前的记忆
   * @param {number} options.minQuality - 删除质量分数低于此值的记忆
   * @param {boolean} options.onlyUnused - 仅删除未使用的记忆
   * @param {Array<string>} options.memoryIds - 直接指定记忆 ID
   * @returns {Promise<Object>} 删除结果
   */
  async bulkDelete(userId, options = {}) {
    try {
      const settings = await this.getPrivacySettings(userId);
      
      // 构建查询条件
      const conditions = { userId };
      
      if (options.category) {
        conditions.category = options.category;
      }
      
      if (options.beforeDate) {
        conditions.createdAt = { $lt: options.beforeDate };
      }
      
      if (options.minQuality !== undefined) {
        // 需要先获取记忆的质量分数
        const memories = await this.storage.find('memories', { userId });
        const lowQualityIds = [];
        
        for (const memory of memories) {
          const qualityScore = await this.memoryEditor.calculateQualityScore(memory);
          if (qualityScore < options.minQuality) {
            lowQualityIds.push(memory._id);
          }
        }
        
        if (lowQualityIds.length > 0) {
          conditions._id = { $in: lowQualityIds };
        } else {
          return { deleted: 0, skipped: 0, reason: 'No low quality memories found' };
        }
      }
      
      if (options.onlyUnused) {
        const memories = await this.storage.find('memories', { userId });
        const unusedIds = [];
        
        for (const memory of memories) {
          const usage = await this.memoryEditor.getMemoryUsage(memory._id);
          if (usage.totalUses === 0) {
            unusedIds.push(memory._id);
          }
        }
        
        if (unusedIds.length > 0) {
          conditions._id = { $in: unusedIds };
        } else {
          return { deleted: 0, skipped: 0, reason: 'No unused memories found' };
        }
      }
      
      if (options.memoryIds && options.memoryIds.length > 0) {
        conditions._id = { $in: options.memoryIds };
      }
      
      // 获取要删除的记忆
      const memoriesToDelete = await this.storage.find('memories', conditions);
      
      if (memoriesToDelete.length === 0) {
        return { deleted: 0, skipped: 0, reason: 'No memories match criteria' };
      }
      
      // 执行删除
      let deleted = 0;
      let skipped = 0;
      const deletedIds = [];
      
      for (const memory of memoriesToDelete) {
        try {
          // 检查是否为重要记忆
          if (memory.important && !options.forceDeleteImportant) {
            this.logger.warn('Skipping important memory', { memoryId: memory._id });
            skipped++;
            continue;
          }
          
          await this.memoryEditor.deleteMemory(memory._id);
          deleted++;
          deletedIds.push(memory._id);
          
        } catch (error) {
          this.logger.error('Failed to delete memory in bulk', { error, memoryId: memory._id });
          skipped++;
        }
      }
      
      // 记录审计日志
      if (settings.auditLogging) {
        await this.logAudit(userId, 'bulk_delete', {
          deletedCount: deleted,
          skippedCount: skipped,
          criteria: options,
          deletedMemoryIds: deletedIds.slice(0, 10) // 只记录前10个
        });
      }
      
      // 发送通知
      if (settings.notifyOnDelete && deleted > 0) {
        await this.sendNotification(userId, 'bulk_delete_completed', {
          deletedCount: deleted,
          skippedCount: skipped
        });
      }
      
      this.logger.info('Bulk delete completed', { 
        userId, 
        deleted, 
        skipped,
        criteria: options 
      });
      
      return {
        deleted,
        skipped,
        deletedIds,
        total: memoriesToDelete.length
      };
      
    } catch (error) {
      this.logger.error('Bulk delete failed', { error, userId, options });
      throw error;
    }
  }

  /**
   * 导出记忆
   * @param {string} userId - 用户 ID
   * @param {Object} options - 选项
   * @param {string} options.format - 导出格式: 'json', 'csv', 'markdown'
   * @param {boolean} options.includeMetadata - 是否包含元数据
   * @param {boolean} options.includeUsage - 是否包含使用统计
   * @param {boolean} options.anonymize - 是否匿名化
   * @returns {Promise<Object>} 导出结果
   */
  async exportMemories(userId, options = {}) {
    const {
      format = 'json',
      includeMetadata = true,
      includeUsage = false,
      anonymize = true
    } = options;
    
    try {
      const settings = await this.getPrivacySettings(userId);
      
      if (!settings.exportable) {
        throw new Error('Export is not allowed for this user');
      }
      
      // 获取所有记忆
      const memories = await this.memoryEditor.listMemories(userId, { limit: 1000 });
      
      if (memories.length === 0) {
        return { success: true, count: 0, data: null, message: 'No memories to export' };
      }
      
      // 处理记忆数据
      const processedMemories = await Promise.all(
        memories.map(async (memory) => {
          const exportData = {
            id: memory._id,
            content: memory.content,
            summary: memory.summary,
            category: memory.category,
            tags: memory.tags,
            important: memory.important,
            createdAt: memory.createdAt,
            updatedAt: memory.updatedAt
          };
          
          if (includeMetadata && memory.metadata) {
            exportData.metadata = memory.metadata;
          }
          
          if (includeUsage) {
            exportData.usage = await this.memoryEditor.getMemoryUsage(memory._id);
          }
          
          // 匿名化处理
          if (anonymize) {
            exportData.content = this.anonymizeText(exportData.content);
            if (exportData.summary) {
              exportData.summary = this.anonymizeText(exportData.summary);
            }
          }
          
          return exportData;
        })
      );
      
      // 格式化数据
      let exportData;
      switch (format) {
        case 'json':
          exportData = JSON.stringify(processedMemories, null, 2);
          break;
          
        case 'csv':
          exportData = this.convertToCSV(processedMemories);
          break;
          
        case 'markdown':
          exportData = this.convertToMarkdown(processedMemories);
          break;
          
        default:
          throw new Error(`Unsupported format: ${format}`);
      }
      
      // 生成导出ID
      const exportId = createHash('sha256')
        .update(userId + Date.now().toString())
        .digest('hex')
        .substring(0, 16);
      
      // 保存导出记录
      const exportRecord = {
        exportId,
        userId,
        format,
        memoryCount: memories.length,
        includeMetadata,
        includeUsage,
        anonymize,
        exportedAt: new Date(),
        checksum: createHash('sha256').update(exportData).digest('hex')
      };
      
      await this.storage.insertOne('export_records', exportRecord);
      
      // 记录审计日志
      if (settings.auditLogging) {
        await this.logAudit(userId, 'export_completed', {
          exportId,
          memoryCount: memories.length,
          format,
          anonymize
        });
      }
      
      // 发送通知
      if (settings.notifyOnExport) {
        await this.sendNotification(userId, 'export_completed', {
          exportId,
          memoryCount: memories.length,
          format
        });
      }
      
      this.logger.info('Memories exported', { 
        userId, 
        exportId,
        count: memories.length,
        format 
      });
      
      return {
        success: true,
        exportId,
        count: memories.length,
        format,
        data: exportData,
        record: exportRecord
      };
      
    } catch (error) {
      this.logger.error('Export failed', { error, userId, options });
      throw error;
    }
  }

  /**
   * 导入记忆
   * @param {string} userId - 用户 ID
   * @param {string} data - 导入数据
   * @param {Object} options - 选项
   * @param {string} options.format - 数据格式
   * @param {boolean} options.overwrite - 是否覆盖现有记忆
   * @returns {Promise<Object>} 导入结果
   */
  async importMemories(userId, data, options = {}) {
    const { format = 'json', overwrite = false } = options;
    
    try {
      const settings = await this.getPrivacySettings(userId);
      
      // 解析数据
      let memories;
      switch (format) {
        case 'json':
          memories = JSON.parse(data);
          break;
          
        case 'csv':
          memories = this.parseCSV(data);
          break;
          
        default:
          throw new Error(`Unsupported import format: ${format}`);
      }
      
      if (!Array.isArray(memories)) {
        throw new Error('Import data must be an array of memories');
      }
      
      // 导入记忆
      let imported = 0;
      let skipped = 0;
      let failed = 0;
      const importedIds = [];
      
      for (const memoryData of memories) {
        try {
          // 检查是否已存在（基于内容哈希）
          const contentHash = createHash('sha256')
            .update(memoryData.content || '')
            .digest('hex');
          
          const existing = await this.storage.findOne('memories', {
            userId,
            'metadata.contentHash': contentHash
          });
          
          if (existing && !overwrite) {
            this.logger.debug('Memory already exists, skipping', { memoryId: existing._id });
            skipped++;
            continue;
          }
          
          // 创建新记忆
          const memory = {
            userId,
            content: memoryData.content,
            summary: memoryData.summary || '',
            category: memoryData.category || 'imported',
            tags: memoryData.tags || [],
            important: memoryData.important || false,
            metadata: {
              ...memoryData.metadata,
              contentHash,
              importedAt: new Date(),
              importSource: 'user_import'
            },
            createdAt: memoryData.createdAt || new Date(),
            updatedAt: new Date()
          };
          
          // 保存记忆
          const result = await this.storage.insertOne('memories', memory);
          
          // 添加到向量存储
          await this.memoryEditor.vectorStore?.insert?.({
            id: result.insertedId,
            text: memory.content,
            metadata: {
              ...memory.metadata,
              userId
            }
          });
          
          imported++;
          importedIds.push(result.insertedId);
          
        } catch (error) {
          this.logger.error('Failed to import memory', { error, memoryData });
          failed++;
        }
      }
      
      // 保存导入记录
      const importRecord = {
        userId,
        format,
        total: memories.length,
        imported,
        skipped,
        failed,
        importedIds: importedIds.slice(0, 10),
        importedAt: new Date()
      };
      
      await this.storage.insertOne('import_records', importRecord);
      
      // 记录审计日志
      if (settings.auditLogging) {
        await this.logAudit(userId, 'import_completed', {
          total: memories.length,
          imported,
          skipped,
          failed,
          format
        });
      }
      
      this.logger.info('Memories imported', { 
        userId, 
        total: memories.length,
        imported,
        skipped,
        failed
      });
      
      return {
        success: true,
        total: memories.length,
        imported,
        skipped,
        failed,
        importRecord
      };
      
    } catch (error) {
      this.logger.error('Import failed', { error, userId, options });
      throw error;
    }
  }

  /**
   * 检测敏感信息
   * @param {string} text - 文本内容
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 检测结果
   */
  async detectSensitiveInfo(text, options = {}) {
    try {
      const sensitivePatterns = {
        // 个人身份信息
        email: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g,
        phone: /\b\d{3}[-.]?\d{3}[-.]?\d{4}\b|\b\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b/g,
        ssn: /\b\d{3}-\d{2}-\d{4}\b/g,
        
        // 金融信息
        creditCard: /\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b/g,
        bankAccount: /\b\d{8,20}\b/g,
        
        // 地址
        address: /\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr)\b/gi,
        
        // 健康信息
        medicalId: /\b[A-Z]{2}\d{6}\b/g
      };
      
      const detected = {};
      let hasSensitive = false;
      
      for (const [category, pattern] of Object.entries(sensitivePatterns)) {
        const matches = text.match(pattern);
        if (matches && matches.length > 0) {
          detected[category] = {
            count: matches.length,
            examples: matches.slice(0, 3)
          };
          hasSensitive = true;
        }
      }
      
      // 关键词检测
      const sensitiveKeywords = {
        personal: ['密码', '口令', '密钥', 'token', 'secret', 'private key'],
        financial: ['银行卡', '信用卡', '账户', '余额', '转账', '支付'],
        health: ['病历', '诊断', '处方', '症状', '病史']
      };
      
      for (const [category, keywords] of Object.entries(sensitiveKeywords)) {
        const foundKeywords = keywords.filter(keyword => 
          text.toLowerCase().includes(keyword.toLowerCase())
        );
        
        if (foundKeywords.length > 0) {
          detected[category] = detected[category] || { count: 0, examples: [] };
          detected[category].keywords = foundKeywords;
          detected[category].count += foundKeywords.length;
          hasSensitive = true;
        }
      }
      
      return {
        hasSensitive,
        detected,
        riskLevel: this.calculateRiskLevel(detected),
        recommendation: this.getRecommendation(detected)
      };
      
    } catch (error) {
      this.logger.error('Sensitive info detection failed', { error });
      return {
        hasSensitive: false,
        detected: {},
        riskLevel: 'low',
        recommendation: 'No issues detected'
      };
    }
  }

  /**
   * 匿名化文本
   * @param {string} text - 原始文本
   * @returns {string} 匿名化后的文本
   */
  anonymizeText(text) {
    if (!text) return text;
    
    // 替换邮箱
    text = text.replace(/\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b/g, '[EMAIL_REDACTED]');
    
    // 替换手机号
    text = text.replace(/\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g, '[PHONE_REDACTED]');
    
    // 替换身份证/SSN
    text = text.replace(/\b\d{3}-\d{2}-\d{4}\b/g, '[ID_REDACTED]');
    
    // 替换信用卡号
    text = text.replace(/\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b/g, '[CARD_REDACTED]');
    
    return text;
  }

  /**
   * 计算风险等级
   * @param {Object} detected - 检测到的敏感信息
   * @returns {string} 风险等级
   */
  calculateRiskLevel(detected) {
    let score = 0;
    
    for (const [category, info] of Object.entries(detected)) {
      switch (category) {
        case 'ssn':
        case 'creditCard':
          score += info.count * 10;
          break;
        case 'email':
        case 'phone':
          score += info.count * 5;
          break;
        default:
          score += info.count * 3;
      }
    }
    
    if (score >= 20) return 'critical';
    if (score >= 10) return 'high';
    if (score >= 5) return 'medium';
    return 'low';
  }

  /**
   * 获取处理建议
   * @param {Object} detected - 检测到的敏感信息
   * @returns {string} 建议
   */
  getRecommendation(detected) {
    const riskLevel = this.calculateRiskLevel(detected);
    
    switch (riskLevel) {
      case 'critical':
        return '立即删除或匿名化处理';
      case 'high':
        return '建议匿名化处理';
      case 'medium':
        return '可以考虑匿名化';
      default:
        return '风险较低，可以保留';
    }
  }

  /**
   * 记录审计日志
   * @param {string} userId - 用户 ID
   * @param {string} action - 操作类型
   * @param {Object} details - 详细信息
   */
  async logAudit(userId, action, details = {}) {
    try {
      const auditLog = {
        userId,
        action,
        details,
        timestamp: new Date(),
        ip: details.ip || 'unknown',
        userAgent: details.userAgent || 'unknown'
      };
      
      await this.storage.insertOne('audit_logs', auditLog);
      
    } catch (error) {
      this.logger.error('Failed to log audit', { error, userId, action });
    }
  }

  /**
   * 发送通知
   * @param {string} userId - 用户 ID
   * @param {string} type - 通知类型
   * @param {Object} data - 通知数据
   */
  async sendNotification(userId, type, data = {}) {
    try {
      const notification = {
        userId,
        type,
        data,
        sentAt: new Date(),
        read: false
      };
      
      await this.storage.insertOne('notifications', notification);
      
      this.logger.debug('Notification sent', { userId, type });
      
    } catch (error) {
      this.logger.error('Failed to send notification', { error, userId, type });
    }
  }

  /**
   * 转换为 CSV
   * @param {Array} data - 数据数组
   * @returns {string} CSV 字符串
   */
  convertToCSV(data) {
    if (data.length === 0) return '';
    
    const headers = Object.keys(data[0]);
    const rows = data.map(item => 
      headers.map(header => {
        const value = item[header];
        if (typeof value === 'object') {
          return JSON.stringify(value);
        }
        return `"${String(value).replace(/"/g, '""')}"`;
      }).join(',')
    );
    
    return [headers.join(','), ...rows].join('\n');
  }

  /**
   * 转换为 Markdown
   * @param {Array} data - 数据数组
   * @returns {string} Markdown 字符串
   */
  convertToMarkdown(data) {
    let markdown = `# 记忆导出\n\n`;
    markdown += `导出时间: ${new Date().toISOString()}\n`;
    markdown += `记忆数量: ${data.length}\n\n`;
    
    data.forEach((item, index) => {
      markdown += `## 记忆 ${index + 1}\n\n`;
      markdown += `**内容**: ${item.content}\n\n`;
      
      if (item.summary) {
        markdown += `**摘要**: ${item.summary}\n\n`;
      }
      
      markdown += `**分类**: ${item.category || '未分类'}\n`;
      markdown += `**标签**: ${item.tags?.join(', ') || '无'}\n`;
      markdown += `**创建时间**: ${item.createdAt}\n\n`;
      
      markdown += `---\n\n`;
    });
    
    return markdown;
  }

  /**
   * 解析 CSV
   * @param {string} csv - CSV 字符串
   * @returns {Array} 解析后的数据
   */
  parseCSV(csv) {
    const lines = csv.split('\n');
    if (lines.length < 2) return [];
    
    const headers = lines[0].split(',').map(h => h.trim().replace(/"/g, ''));
    const result = [];
    
    for (let i = 1; i < lines.length; i++) {
      const line = lines[i].trim();
      if (!line) continue;
      
      const values = line.split(',').map(v => v.trim().replace(/^"|"$/g, ''));
      const item = {};
      
      headers.forEach((header, index) => {
        if (values[index]) {
          try {
            item[header] = JSON.parse(values[index]);
          } catch {
            item[header] = values[index];
          }
        }
      });
      
      result.push(item);
    }
    
    return result;
  }
}

export default PrivacyManager;