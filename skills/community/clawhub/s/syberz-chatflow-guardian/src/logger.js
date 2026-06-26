/**
 * 日志模块
 * 
 * 负责：
 * 1. 记录技能运行日志
 * 2. 管理日志级别
 * 3. 日志轮转和归档
 * 4. 性能指标记录
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

class Logger {
  constructor(config) {
    this.config = config || {};
    this.levels = {
      error: 0,
      warn: 1,
      info: 2,
      debug: 3
    };
    
    this.currentLevel = this.levels[this.config.level || 'info'];
    this.logFile = null;
    this.metricsFile = null;
    
    this.setupLogFiles();
  }

  /**
   * 设置日志文件
   */
  setupLogFiles() {
    try {
      // 解析日志文件路径
      let logPath = this.config.file || '~/.openclaw/logs/dialog-manager.log';
      let metricsPath = logPath.replace('.log', '-metrics.log');
      
      // 处理 ~ 扩展
      if (logPath.startsWith('~')) {
        logPath = path.join(os.homedir(), logPath.slice(1));
      }
      if (metricsPath.startsWith('~')) {
        metricsPath = path.join(os.homedir(), metricsPath.slice(1));
      }
      
      // 创建日志目录
      const logDir = path.dirname(logPath);
      if (!fs.existsSync(logDir)) {
        fs.mkdirSync(logDir, { recursive: true });
      }
      
      this.logFile = logPath;
      this.metricsFile = metricsPath;
      
      this.info('日志系统初始化完成', {
        logFile: this.logFile,
        metricsFile: this.metricsFile,
        level: Object.keys(this.levels)[this.currentLevel]
      });
    } catch (error) {
      console.error('设置日志文件失败:', error);
      // 使用控制台日志作为后备
    }
  }

  /**
   * 记录错误日志
   * @param {string} message - 日志消息
   * @param {Object} data - 附加数据
   */
  error(message, data = {}) {
    this.log('error', message, data);
  }

  /**
   * 记录警告日志
   * @param {string} message - 日志消息
   * @param {Object} data - 附加数据
   */
  warn(message, data = {}) {
    this.log('warn', message, data);
  }

  /**
   * 记录信息日志
   * @param {string} message - 日志消息
   * @param {Object} data - 附加数据
   */
  info(message, data = {}) {
    this.log('info', message, data);
  }

  /**
   * 记录调试日志
   * @param {string} message - 日志消息
   * @param {Object} data - 附加数据
   */
  debug(message, data = {}) {
    this.log('debug', message, data);
  }

  /**
   * 记录日志
   * @param {string} level - 日志级别
   * @param {string} message - 日志消息
   * @param {Object} data - 附加数据
   */
  log(level, message, data = {}) {
    const levelNum = this.levels[level];
    if (levelNum > this.currentLevel) {
      return;
    }
    
    const timestamp = new Date().toISOString();
    const logEntry = {
      timestamp,
      level: level.toUpperCase(),
      message,
      data,
      pid: process.pid
    };
    
    // 控制台输出
    if (this.config.console !== false) {
      const consoleMessage = `[${timestamp}] ${level.toUpperCase()}: ${message}`;
      if (Object.keys(data).length > 0) {
        console.log(consoleMessage, data);
      } else {
        console.log(consoleMessage);
      }
    }
    
    // 文件输出
    if (this.logFile) {
      this.writeToFile(this.logFile, logEntry);
    }
    
    // 如果是错误，也记录到metrics
    if (level === 'error' && this.metricsFile) {
      this.recordMetric('error', { message, ...data });
    }
  }

  /**
   * 写入文件
   * @param {string} filePath - 文件路径
   * @param {Object} entry - 日志条目
   */
  writeToFile(filePath, entry) {
    try {
      const logLine = JSON.stringify(entry) + '\n';
      
      // 检查文件大小
      if (fs.existsSync(filePath)) {
        const stats = fs.statSync(filePath);
        const maxSize = this.parseSize(this.config.max_size || '10MB');
        
        if (stats.size > maxSize) {
          this.rotateLogFile(filePath);
        }
      }
      
      fs.appendFileSync(filePath, logLine, 'utf8');
    } catch (error) {
      console.error('写入日志文件失败:', error);
    }
  }

  /**
   * 解析大小字符串
   * @param {string} sizeStr - 大小字符串，如 "10MB"
   */
  parseSize(sizeStr) {
    const units = {
      B: 1,
      KB: 1024,
      MB: 1024 * 1024,
      GB: 1024 * 1024 * 1024
    };
    
    const match = sizeStr.match(/^(\d+)([BKMGT]?B)$/i);
    if (!match) {
      return 10 * 1024 * 1024; // 默认10MB
    }
    
    const size = parseInt(match[1], 10);
    const unit = match[2].toUpperCase();
    
    return size * (units[unit] || 1);
  }

  /**
   * 轮转日志文件
   * @param {string} filePath - 文件路径
   */
  rotateLogFile(filePath) {
    try {
      const dir = path.dirname(filePath);
      const ext = path.extname(filePath);
      const base = path.basename(filePath, ext);
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
      const rotatedFile = path.join(dir, `${base}-${timestamp}${ext}`);
      
      fs.renameSync(filePath, rotatedFile);
      
      this.info('日志文件已轮转', {
        original: filePath,
        rotated: rotatedFile
      });
      
      // 清理旧日志文件
      this.cleanupOldLogs(dir, base, ext);
    } catch (error) {
      console.error('轮转日志文件失败:', error);
    }
  }

  /**
   * 清理旧日志文件
   * @param {string} dir - 目录
   * @param {string} base - 基础文件名
   * @param {string} ext - 文件扩展名
   */
  cleanupOldLogs(dir, base, ext) {
    try {
      const retentionDays = this.config.retention || 7;
      const cutoffTime = Date.now() - (retentionDays * 24 * 60 * 60 * 1000);
      
      const files = fs.readdirSync(dir);
      const pattern = new RegExp(`^${base}-(.+)${ext}$`);
      
      files.forEach(file => {
        const match = file.match(pattern);
        if (match) {
          const filePath = path.join(dir, file);
          const stats = fs.statSync(filePath);
          
          if (stats.mtimeMs < cutoffTime) {
            fs.unlinkSync(filePath);
            this.debug('删除旧日志文件', { file });
          }
        }
      });
    } catch (error) {
      console.error('清理旧日志文件失败:', error);
    }
  }

  /**
   * 记录性能指标
   * @param {string} metric - 指标名称
   * @param {Object} data - 指标数据
   */
  recordMetric(metric, data = {}) {
    if (!this.metricsFile) {
      return;
    }
    
    const metricEntry = {
      timestamp: new Date().toISOString(),
      metric,
      ...data
    };
    
    try {
      const metricLine = JSON.stringify(metricEntry) + '\n';
      fs.appendFileSync(this.metricsFile, metricLine, 'utf8');
    } catch (error) {
      console.error('记录性能指标失败:', error);
    }
  }

  /**
   * 记录响应时间
   * @param {string} operation - 操作名称
   * @param {number} startTime - 开始时间
   * @param {Object} context - 上下文信息
   */
  recordResponseTime(operation, startTime, context = {}) {
    const endTime = Date.now();
    const duration = endTime - startTime;
    
    this.recordMetric('response_time', {
      operation,
      duration,
      ...context
    });
    
    if (duration > 1000) { // 超过1秒记录警告
      this.warn('操作耗时较长', {
        operation,
        duration: duration + 'ms',
        ...context
      });
    }
  }

  /**
   * 记录token使用
   * @param {number} tokens - token数量
   * @param {string} operation - 操作名称
   * @param {Object} context - 上下文信息
   */
  recordTokenUsage(tokens, operation, context = {}) {
    this.recordMetric('token_usage', {
      operation,
      tokens,
      ...context
    });
    
    if (tokens > 1000) { // 超过1000token记录警告
      this.warn('Token使用较多', {
        operation,
        tokens,
        ...context
      });
    }
  }

  /**
   * 设置日志级别
   * @param {string} level - 日志级别
   */
  setLevel(level) {
    if (this.levels[level] !== undefined) {
      this.currentLevel = this.levels[level];
      this.info('日志级别已更新', { level });
    } else {
      this.error('无效的日志级别', { level });
    }
  }

  /**
   * 获取当前日志级别
   */
  getLevel() {
    for (const [name, value] of Object.entries(this.levels)) {
      if (value === this.currentLevel) {
        return name;
      }
    }
    return 'info';
  }

  /**
   * 获取日志统计
   */
  getStats() {
    try {
      if (!this.logFile || !fs.existsSync(this.logFile)) {
        return { totalEntries: 0, fileSize: 0 };
      }
      
      const stats = fs.statSync(this.logFile);
      const content = fs.readFileSync(this.logFile, 'utf8');
      const lines = content.trim().split('\n');
      
      return {
        totalEntries: lines.length,
        fileSize: this.formatFileSize(stats.size),
        lastModified: new Date(stats.mtime).toISOString()
      };
    } catch (error) {
      return { totalEntries: 0, fileSize: '0B', error: error.message };
    }
  }

  /**
   * 格式化文件大小
   * @param {number} bytes - 字节数
   */
  formatFileSize(bytes) {
    const units = ['B', 'KB', 'MB', 'GB'];
    let size = bytes;
    let unitIndex = 0;
    
    while (size >= 1024 && unitIndex < units.length - 1) {
      size /= 1024;
      unitIndex++;
    }
    
    return `${size.toFixed(1)}${units[unitIndex]}`;
  }
}

module.exports = Logger;