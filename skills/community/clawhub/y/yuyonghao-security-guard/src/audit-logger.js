/**
 * Security Guard - 审计日志系统
 * 完整操作记录和追踪
 */

import { EventEmitter } from 'events';
import fs from 'fs/promises';
import path from 'path';

/**
 * 审计日志器
 */
export class AuditLogger extends EventEmitter {
  constructor(config = {}) {
    super();
    this.logDir = config.logDir || './audit-logs';
    this.maxLogSize = config.maxLogSize || 10 * 1024 * 1024; // 10MB
    this.maxLogFiles = config.maxLogFiles || 10;
    this.buffer = [];
    this.bufferSize = config.bufferSize || 100;
    this.flushInterval = config.flushInterval || 5000; // 5秒
    
    // 启动定时刷新
    this.startFlushTimer();
  }

  /**
   * 记录操作
   */
  async log(operation) {
    const entry = {
      timestamp: new Date().toISOString(),
      id: `audit_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      userId: operation.userId || 'anonymous',
      action: operation.action,
      resource: operation.resource,
      status: operation.status || 'success',
      details: operation.details || {},
      ip: operation.ip || 'localhost',
      userAgent: operation.userAgent || '',
      duration: operation.duration || 0
    };

    this.buffer.push(entry);
    
    // 如果缓冲区满了，立即刷新
    if (this.buffer.length >= this.bufferSize) {
      await this.flush();
    }

    this.emit('logged', entry);
    return entry;
  }

  /**
   * 记录安全事件
   */
  async logSecurity(event) {
    return await this.log({
      action: 'security',
      resource: event.type,
      status: event.severity,
      details: {
        eventType: event.type,
        severity: event.severity,
        description: event.description,
        blocked: event.blocked || false,
        ...event.details
      }
    });
  }

  /**
   * 记录权限检查
   */
  async logPermissionCheck(userId, action, resource, allowed, details = {}) {
    return await this.log({
      userId,
      action: 'permission_check',
      resource: `${action}:${resource}`,
      status: allowed ? 'allowed' : 'denied',
      details
    });
  }

  /**
   * 记录高风险操作
   */
  async logHighRisk(operation) {
    return await this.log({
      ...operation,
      status: 'high_risk',
      details: {
        ...operation.details,
        riskLevel: 'high',
        requiresReview: true
      }
    });
  }

  /**
   * 刷新缓冲区到文件
   */
  async flush() {
    if (this.buffer.length === 0) return;

    try {
      await fs.mkdir(this.logDir, { recursive: true });
      
      const logFile = path.join(this.logDir, `audit-${new Date().toISOString().split('T')[0]}.log`);
      const entries = this.buffer.map(e => JSON.stringify(e)).join('\n') + '\n';
      
      await fs.appendFile(logFile, entries, 'utf-8');
      
      this.buffer = [];
      this.emit('flushed', { file: logFile });
      
      // 清理旧日志
      await this.cleanupOldLogs();
    } catch (error) {
      this.emit('error', { error, message: 'Failed to flush audit log' });
    }
  }

  /**
   * 启动定时刷新
   */
  startFlushTimer() {
    this.flushTimer = setInterval(() => {
      this.flush();
    }, this.flushInterval);
  }

  /**
   * 停止定时刷新
   */
  stopFlushTimer() {
    if (this.flushTimer) {
      clearInterval(this.flushTimer);
      this.flushTimer = null;
    }
  }

  /**
   * 清理旧日志
   */
  async cleanupOldLogs() {
    try {
      const files = await fs.readdir(this.logDir);
      const logFiles = files
        .filter(f => f.startsWith('audit-') && f.endsWith('.log'))
        .map(f => ({ name: f, path: path.join(this.logDir, f) }))
        .sort((a, b) => b.name.localeCompare(a.name));

      // 删除旧日志
      if (logFiles.length > this.maxLogFiles) {
        const toDelete = logFiles.slice(this.maxLogFiles);
        for (const file of toDelete) {
          await fs.unlink(file.path);
          this.emit('log-deleted', { file: file.name });
        }
      }

      // 检查单个日志大小
      for (const file of logFiles.slice(0, this.maxLogFiles)) {
        const stats = await fs.stat(file.path);
        if (stats.size > this.maxLogSize) {
          // 归档大日志
          const archiveName = file.name.replace('.log', `-${Date.now()}.archive`);
          await fs.rename(file.path, path.join(this.logDir, archiveName));
          this.emit('log-archived', { file: file.name, archive: archiveName });
        }
      }
    } catch (error) {
      // 忽略清理错误
    }
  }

  /**
   * 查询日志
   */
  async query(filters = {}) {
    const results = [];
    
    try {
      const files = await fs.readdir(this.logDir);
      const logFiles = files.filter(f => f.endsWith('.log'));

      for (const file of logFiles) {
        const content = await fs.readFile(path.join(this.logDir, file), 'utf-8');
        const entries = content.split('\n').filter(line => line.trim());
        
        for (const entry of entries) {
          try {
            const data = JSON.parse(entry);
            
            // 应用过滤器
            if (filters.userId && data.userId !== filters.userId) continue;
            if (filters.action && data.action !== filters.action) continue;
            if (filters.status && data.status !== filters.status) continue;
            if (filters.startTime && new Date(data.timestamp) < new Date(filters.startTime)) continue;
            if (filters.endTime && new Date(data.timestamp) > new Date(filters.endTime)) continue;
            
            results.push(data);
          } catch {
            // 忽略解析错误
          }
        }
      }
    } catch (error) {
      // 忽略查询错误
    }

    // 排序
    results.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp));
    
    // 限制数量
    if (filters.limit) {
      return results.slice(0, filters.limit);
    }
    
    return results;
  }

  /**
   * 生成审计报告
   */
  async generateReport(timeRange = '24h') {
    const now = new Date();
    let startTime;
    
    switch (timeRange) {
      case '1h':
        startTime = new Date(now - 60 * 60 * 1000);
        break;
      case '24h':
        startTime = new Date(now - 24 * 60 * 60 * 1000);
        break;
      case '7d':
        startTime = new Date(now - 7 * 24 * 60 * 60 * 1000);
        break;
      default:
        startTime = new Date(now - 24 * 60 * 60 * 1000);
    }

    const entries = await this.query({
      startTime: startTime.toISOString(),
      endTime: now.toISOString()
    });

    const report = {
      timeRange,
      generatedAt: now.toISOString(),
      summary: {
        totalOperations: entries.length,
        successCount: entries.filter(e => e.status === 'success').length,
        failedCount: entries.filter(e => e.status === 'failed').length,
        deniedCount: entries.filter(e => e.status === 'denied').length,
        highRiskCount: entries.filter(e => e.status === 'high_risk').length
      },
      topActions: this.getTopActions(entries),
      topUsers: this.getTopUsers(entries),
      securityEvents: entries.filter(e => e.action === 'security'),
      recentHighRisk: entries.filter(e => e.status === 'high_risk').slice(0, 10)
    };

    return report;
  }

  /**
   * 获取热门操作
   */
  getTopActions(entries) {
    const counts = {};
    for (const entry of entries) {
      counts[entry.action] = (counts[entry.action] || 0) + 1;
    }
    return Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([action, count]) => ({ action, count }));
  }

  /**
   * 获取活跃用户
   */
  getTopUsers(entries) {
    const counts = {};
    for (const entry of entries) {
      counts[entry.userId] = (counts[entry.userId] || 0) + 1;
    }
    return Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([userId, count]) => ({ userId, count }));
  }

  /**
   * 关闭日志器
   */
  async close() {
    this.stopFlushTimer();
    await this.flush();
  }
}

export default AuditLogger;
