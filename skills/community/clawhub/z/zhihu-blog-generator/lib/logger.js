/**
 * 知乎技术博客生成器 - 日志工具
 */

const fs = require('fs');
const path = require('path');
const config = require('./config');

class Logger {
  constructor(sessionId) {
    this.sessionId = sessionId;
    this.logs = [];
    this.startTime = Date.now();
  }

  /**
   * 记录日志
   */
  log(level, message, data = null) {
    const timestamp = new Date().toISOString();
    const logEntry = {
      timestamp,
      level,
      message,
      data,
      step: this.currentStep || 'unknown',
    };

    this.logs.push(logEntry);

    // 控制台输出
    const colors = {
      debug: '\x1b[36m',    // cyan
      info: '\x1b[32m',     // green
      warn: '\x1b[33m',     // yellow
      error: '\x1b[31m',    // red
      reset: '\x1b[0m',
    };

    const color = colors[level] || colors.reset;
    console.log(`${color}[${timestamp}] [${level.toUpperCase()}] ${message}${colors.reset}`);
    
    if (data && config.log.level === 'debug') {
      console.log('Data:', JSON.stringify(data, null, 2));
    }
  }

  debug(message, data) {
    if (config.log.level === 'debug') {
      this.log('debug', message, data);
    }
  }

  info(message, data) {
    this.log('info', message, data);
  }

  warn(message, data) {
    this.log('warn', message, data);
  }

  error(message, data) {
    this.log('error', message, data);
  }

  /**
   * 设置当前步骤
   */
  setStep(step) {
    this.currentStep = step;
    this.info(`========== 开始步骤: ${step} ==========`);
  }

  /**
   * 记录步骤完成
   */
  stepComplete(step, outputPath) {
    const duration = Date.now() - this.startTime;
    this.info(`========== 步骤完成: ${step} ==========`);
    this.info(`输出路径: ${outputPath}`);
    this.info(`耗时: ${(duration / 1000).toFixed(2)}s`);
  }

  /**
   * 保存日志到文件
   */
  save(sessionDir) {
    if (!config.log.saveToFile) return;

    const logPath = path.join(sessionDir, config.log.fileName);
    const logContent = this.logs.map(log => 
      `[${log.timestamp}] [${log.level.toUpperCase()}] [${log.step}] ${log.message}`
    ).join('\n');

    fs.writeFileSync(logPath, logContent, 'utf8');
    this.info(`日志已保存: ${logPath}`);
  }

  /**
   * 生成执行摘要
   */
  getSummary() {
    const duration = Date.now() - this.startTime;
    const errors = this.logs.filter(l => l.level === 'error').length;
    const warnings = this.logs.filter(l => l.level === 'warn').length;

    return {
      sessionId: this.sessionId,
      totalLogs: this.logs.length,
      errors,
      warnings,
      duration: `${(duration / 1000).toFixed(2)}s`,
      completed: errors === 0,
    };
  }
}

module.exports = Logger;
