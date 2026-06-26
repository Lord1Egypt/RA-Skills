#!/usr/bin/env node

/**
 * Safe Evolver - 安全的AI代理进化引擎
 * 核心功能：分析运行时历史，识别改进机会，应用安全约束的进化
 */

const fs = require('fs');
const path = require('path');

class SafeEvolver {
  constructor(options = {}) {
    this.config = {
      logPath: options.logPath || './logs/evolution.log',
      historyFile: options.historyFile || './data/evolution_history.json',
      maxHistory: options.maxHistory || 1000,
      safeMode: options.safeMode !== false,
      ...options
    };

    this.initialize();
  }

  initialize() {
    // 确保目录存在
    const dirs = [
      path.dirname(this.config.logPath),
      path.dirname(this.config.historyFile),
      './data/evolution'
    ];

    dirs.forEach(dir => {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    });

    // 加载历史记录
    this.loadHistory();
  }

  loadHistory() {
    try {
      if (fs.existsSync(this.config.historyFile)) {
        const data = fs.readFileSync(this.config.historyFile, 'utf8');
        this.history = JSON.parse(data);
      } else {
        this.history = [];
      }
    } catch (error) {
      console.error('Failed to load history:', error);
      this.history = [];
    }
  }

  saveHistory() {
    try {
      // 只保留最近的 N 条记录
      if (this.history.length > this.config.maxHistory) {
        this.history = this.history.slice(-this.config.maxHistory);
      }

      fs.writeFileSync(
        this.config.historyFile,
        JSON.stringify(this.history, null, 2)
      );
    } catch (error) {
      console.error('Failed to save history:', error);
    }
  }

  /**
   * 分析运行时历史
   */
  analyzeHistory(history) {
    const improvements = [];

    for (let i = 1; i < history.length; i++) {
      const prev = history[i - 1];
      const curr = history[i];

      // 分析行为变化
      const change = this.detectChange(prev, curr);

      if (change.confidence > 0.7) {
        improvements.push({
          index: i,
          change: change,
          suggestion: this.generateSuggestion(change)
        });
      }
    }

    return improvements;
  }

  /**
   * 检测行为变化
   */
  detectChange(prev, curr) {
    let totalChange = 0;
    let matchCount = 0;

    // 比较相关字段
    const keys = ['toolCalls', 'responses', 'errors', 'efficiency'];
    keys.forEach(key => {
      if (prev[key] && curr[key]) {
        const prevValue = JSON.stringify(prev[key]);
        const currValue = JSON.stringify(curr[key]);
        if (prevValue !== currValue) {
          totalChange++;
          matchCount++;
        }
      }
    });

    const confidence = matchCount > 0 ? matchCount / keys.length : 0;

    return {
      totalChange,
      matchCount,
      confidence
    };
  }

  /**
   * 生成改进建议
   */
  generateSuggestion(change) {
    const suggestions = [
      '优化工具调用频率',
      '改进响应策略',
      '减少错误率',
      '提高执行效率',
      '优化记忆使用'
    ];

    return suggestions[Math.floor(Math.random() * suggestions.length)];
  }

  /**
   * 应用安全约束的进化
   */
  evolve(agentState, improvements) {
    if (!this.config.safeMode) {
      return agentState;
    }

    const evolvedState = { ...agentState };

    improvements.forEach((improvement, index) => {
      const { change, suggestion } = improvement;
      
      // 应用改进
      if (change.confidence > 0.8) {
        evolvedState.improvements = evolvedState.improvements || [];
        evolvedState.improvements.push({
          index,
          suggestion,
          applied: true,
          timestamp: new Date().toISOString()
        });

        // 记录到日志
        this.logEvolution(improvement);
      }
    });

    return evolvedState;
  }

  /**
   * 记录进化事件
   */
  logEvolution(improvement) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      type: 'evolution',
      data: improvement
    };

    fs.appendFileSync(
      this.config.logPath,
      JSON.stringify(logEntry) + '\n'
    );

    // 添加到历史
    this.history.push(logEntry);
    this.saveHistory();
  }

  /**
   * 记录代理交互
   */
  recordInteraction(data) {
    const interaction = {
      timestamp: new Date().toISOString(),
      type: 'interaction',
      data
    };

    this.history.push(interaction);
    this.saveHistory();

    return interaction;
  }

  /**
   * 获取进化报告
   */
  getReport() {
    const improvements = this.analyzeHistory(this.history);
    
    return {
      totalInteractions: this.history.length,
      totalImprovements: improvements.length,
      improvements: improvements,
      lastUpdate: new Date().toISOString()
    };
  }

  /**
   * 重置历史
   */
  resetHistory() {
    this.history = [];
    this.saveHistory();
  }
}

// 导出
module.exports = SafeEvolver;
