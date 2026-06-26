#!/usr/bin/env node
/**
 * Usage Tracker - Token 使用追踪系统
 * 记录每个对话的输入/输出 token 消耗，累计统计，预算控制
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { pathToFileURL } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ============ 常量 ============

// Claude API 定价（$/1M tokens）
const MODEL_PRICING = {
  'claude-3-5-sonnet': { input: 3, output: 15 },
  'claude-3-opus': { input: 15, output: 75 },
  'claude-3-sonnet': { input: 3, output: 15 },
  'claude-3-haiku': { input: 0.25, output: 1.25 },
  'default': { input: 3, output: 15 }
};

// ============ Token 估算 ============

/**
 * 估算文本的 token 数
 * 中文约 1 token / 字符
 * 英文约 1 token / 4 字符
 */
export function estimateTokens(text) {
  if (!text || typeof text !== 'string') return 0;
  
  const chineseChars = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  const otherChars = text.length - chineseChars;
  
  return chineseChars + Math.ceil(otherChars / 4);
}

/**
 * 估算消息的 token 数
 */
export function estimateMessageTokens(message) {
  if (!message) return 0;
  
  let total = 0;
  
  if (typeof message === 'string') {
    total += estimateTokens(message);
  } else if (Array.isArray(message)) {
    for (const msg of message) {
      total += estimateMessageTokens(msg);
    }
  } else if (typeof message === 'object') {
    // 处理消息对象
    if (message.content) {
      total += estimateMessageTokens(message.content);
    }
    if (message.role) total += 4; // role标记
  }
  
  return total;
}

// ============ UsageBudget 类 ============

export class UsageBudget {
  constructor(config = {}) {
    this.maxInputTokens = config.maxInputTokens || Infinity;
    this.maxOutputTokens = config.maxOutputTokens || Infinity;
    this.maxTotalTokens = config.maxTotalTokens || Infinity;
    this.maxTurns = config.maxTurns || Infinity;
    this.warningThreshold = config.warningThreshold || 0.8;
    this.onWarning = config.onWarning || null;
    this.onBudgetExceeded = config.onBudgetExceeded || null;
  }

  check(inputTokens, outputTokens, turnCount) {
    const totalTokens = inputTokens + outputTokens;
    const inputPercent = inputTokens / this.maxInputTokens;
    const outputPercent = outputTokens / this.maxOutputTokens;
    const totalPercent = totalTokens / this.maxTotalTokens;
    const turnPercent = turnCount / this.maxTurns;

    const result = {
      inputPercent,
      outputPercent,
      totalPercent,
      turnPercent,
      inputTokens,
      outputTokens,
      totalTokens,
      turnCount,
      maxInputTokens: this.maxInputTokens,
      maxOutputTokens: this.maxOutputTokens,
      maxTotalTokens: this.maxTotalTokens,
      maxTurns: this.maxTurns,
      warning: false,
      exceeded: false
    };

    // 检查警告阈值
    if (inputPercent >= this.warningThreshold ||
        outputPercent >= this.warningThreshold ||
        totalPercent >= this.warningThreshold ||
        turnPercent >= this.warningThreshold) {
      result.warning = true;
      if (this.onWarning) {
        this.onWarning(result);
      }
    }

    // 检查是否超出预算
    if (inputPercent >= 1 || outputPercent >= 1 ||
        totalPercent >= 1 || turnPercent >= 1) {
      result.exceeded = true;
      if (this.onBudgetExceeded) {
        this.onBudgetExceeded(result);
      }
    }

    return result;
  }
}

// ============ UsageTracker 类 ============

export class UsageTracker {
  constructor(config = {}) {
    this.budget = new UsageBudget({
      maxInputTokens: config.maxInputTokens,
      maxOutputTokens: config.maxOutputTokens,
      maxTotalTokens: config.maxTotalTokens,
      maxTurns: config.maxTurns,
      warningThreshold: config.warningThreshold,
      onWarning: config.onWarning,
      onBudgetExceeded: config.onBudgetExceeded
    });
    
    this.model = config.model || 'claude-3-5-sonnet';
    this.currency = config.currency || 'USD';
    
    this.turns = [];
    this.totalInputTokens = 0;
    this.totalOutputTokens = 0;
    this.totalCacheCreation = 0;
    this.totalCacheRead = 0;
    this.turnCount = 0;
    
    // 尝试加载历史记录
    this.storagePath = config.storagePath || './.usage-tracker.json';
    this._load();
  }

  /**
   * 记录一次 token 使用
   */
  record(usage) {
    this.turnCount++;
    
    const inputTokens = usage.input_tokens || 0;
    const outputTokens = usage.output_tokens || 0;
    const cacheCreation = usage.cache_creation_input_tokens || 0;
    const cacheRead = usage.cache_read_input_tokens || 0;

    this.totalInputTokens += inputTokens;
    this.totalOutputTokens += outputTokens;
    this.totalCacheCreation += cacheCreation;
    this.totalCacheRead += cacheRead;

    const turn = {
      turn: this.turnCount,
      inputTokens,
      outputTokens,
      cacheCreation,
      cacheRead,
      totalTokens: inputTokens + outputTokens,
      timestamp: new Date().toISOString()
    };

    this.turns.push(turn);
    this._save();

    // 检查预算
    return this.budget.check(
      this.totalInputTokens,
      this.totalOutputTokens,
      this.turnCount
    );
  }

  /**
   * 记录 prompt 的使用（自动估算 token）
   */
  recordPrompt(prompt, responseText = '') {
    const inputTokens = estimateTokens(prompt);
    const outputTokens = estimateTokens(responseText);
    
    return this.record({
      input_tokens: inputTokens,
      output_tokens: outputTokens
    });
  }

  /**
   * 获取统计信息
   */
  getStats() {
    const totalTokens = this.totalInputTokens + this.totalOutputTokens;
    const avgInput = this.turnCount > 0 ? Math.round(this.totalInputTokens / this.turnCount) : 0;
    const avgOutput = this.turnCount > 0 ? Math.round(this.totalOutputTokens / this.turnCount) : 0;
    const avgTotal = this.turnCount > 0 ? Math.round(totalTokens / this.turnCount) : 0;

    const pricing = MODEL_PRICING[this.model] || MODEL_PRICING['default'];
    const estimatedCost = (
      (this.totalInputTokens / 1_000_000) * pricing.input +
      (this.totalOutputTokens / 1_000_000) * pricing.output
    );

    const budgetUsedPercent = this.budget.maxTotalTokens === Infinity
      ? 0
      : (totalTokens / this.budget.maxTotalTokens) * 100;

    return {
      totalInputTokens: this.totalInputTokens,
      totalOutputTokens: this.totalOutputTokens,
      totalTokens,
      totalCacheCreation: this.totalCacheCreation,
      totalCacheRead: this.totalCacheRead,
      turnCount: this.turnCount,
      avgInputTokensPerTurn: avgInput,
      avgOutputTokensPerTurn: avgOutput,
      avgTotalTokensPerTurn: avgTotal,
      estimatedCost,
      currency: this.currency,
      model: this.model,
      budgetUsedPercent: Math.round(budgetUsedPercent * 100) / 100,
      maxTotalTokens: this.budget.maxTotalTokens,
      maxTurns: this.budget.maxTurns
    };
  }

  /**
   * 检查预算状态
   */
  checkBudget() {
    return this.budget.check(
      this.totalInputTokens,
      this.totalOutputTokens,
      this.turnCount
    );
  }

  /**
   * 获取历史记录
   */
  getHistory(limit = 10) {
    return this.turns.slice(-limit);
  }

  /**
   * 获取完整历史
   */
  getAllHistory() {
    return [...this.turns];
  }

  /**
   * 重置统计
   */
  reset() {
    this.turns = [];
    this.totalInputTokens = 0;
    this.totalOutputTokens = 0;
    this.totalCacheCreation = 0;
    this.totalCacheRead = 0;
    this.turnCount = 0;
    this._save();
  }

  /**
   * 导出数据
   */
  export() {
    return {
      stats: this.getStats(),
      budget: this.checkBudget(),
      history: this.getAllHistory(),
      exportedAt: new Date().toISOString()
    };
  }

  /**
   * 格式化输出
   */
  format() {
    const stats = this.getStats();
    const budget = this.checkBudget();
    
    const lines = [
      '📊 Token 使用统计',
      '═'.repeat(40),
      `模型: ${stats.model}`,
      `对话轮次: ${stats.turnCount}`,
      '',
      'Token 消耗:',
      `  输入: ${stats.totalInputTokens.toLocaleString()}`,
      `  输出: ${stats.totalOutputTokens.toLocaleString()}`,
      `  总计: ${stats.totalTokens.toLocaleString()}`,
      '',
      '缓存:',
      `  创建: ${stats.totalCacheCreation.toLocaleString()}`,
      `  读取: ${stats.totalCacheRead.toLocaleString()}`,
      '',
      '平均每轮:',
      `  输入: ${stats.avgInputTokensPerTurn}`,
      `  输出: ${stats.avgOutputTokensPerTurn}`,
      '',
      `预算使用: ${stats.budgetUsedPercent}%`,
      '',
      `💰 估算费用: $${stats.estimatedCost.toFixed(4)}`
    ];

    if (budget.warning) {
      lines.push('');
      lines.push('⚠️ 接近预算上限！');
    }

    if (budget.exceeded) {
      lines.push('');
      lines.push('❌ 已超出预算！');
    }

    return lines.join('\n');
  }

  // ============ 私有方法 ============

  _load() {
    try {
      if (fs.existsSync(this.storagePath)) {
        const data = JSON.parse(fs.readFileSync(this.storagePath, 'utf-8'));
        this.turns = data.turns || [];
        this.totalInputTokens = data.totalInputTokens || 0;
        this.totalOutputTokens = data.totalOutputTokens || 0;
        this.totalCacheCreation = data.totalCacheCreation || 0;
        this.totalCacheRead = data.totalCacheRead || 0;
        this.turnCount = data.turnCount || 0;
      }
    } catch (e) {
      // 忽略加载错误
    }
  }

  _save() {
    try {
      const data = {
        turns: this.turns,
        totalInputTokens: this.totalInputTokens,
        totalOutputTokens: this.totalOutputTokens,
        totalCacheCreation: this.totalCacheCreation,
        totalCacheRead: this.totalCacheRead,
        turnCount: this.turnCount,
        savedAt: new Date().toISOString()
      };
      fs.writeFileSync(this.storagePath, JSON.stringify(data, null, 2), 'utf-8');
    } catch (e) {
      console.error('保存使用统计失败:', e.message);
    }
  }
}

// ============ CLI ============

function printHelp() {
  console.log(`
Usage Tracker - Token 使用追踪系统
====================================

用法:
  node usage-tracker.mjs <command> [options]

命令:
  stats              显示当前统计
  record <in> <out>  记录一次使用
  reset              重置统计
  export             导出数据
  history            显示历史

选项:
  --model <name>     设置模型 (claude-3-5-sonnet, claude-3-opus, etc.)
  --budget <n>       设置预算上限 (token数)

示例:
  node usage-tracker.mjs stats
  node usage-tracker.mjs record 500 200
  node usage-tracker.mjs record --model claude-3-opus --budget 100000
`);
}

async function main(args) {
  const tracker = new UsageTracker();

  const cmd = args[0];

  if (cmd === 'stats') {
    console.log(tracker.format());
    return 0;
  }

  if (cmd === 'record') {
    const inputTokens = parseInt(args[1]) || 0;
    const outputTokens = parseInt(args[2]) || 0;
    
    const budget = tracker.record({
      input_tokens: inputTokens,
      output_tokens: outputTokens
    });
    
    console.log(`\n✅ 已记录`);
    console.log(`   输入: ${inputTokens} tokens`);
    console.log(`   输出: ${outputTokens} tokens`);
    
    if (budget.warning) {
      console.log(`\n⚠️ 警告: 接近预算上限 (${(budget.totalPercent * 100).toFixed(1)}%)`);
    }
    
    if (budget.exceeded) {
      console.log(`\n❌ 超出预算!`);
    }
    
    return 0;
  }

  if (cmd === 'reset') {
    tracker.reset();
    console.log('✅ 统计已重置');
    return 0;
  }

  if (cmd === 'export') {
    console.log(JSON.stringify(tracker.export(), null, 2));
    return 0;
  }

  if (cmd === 'history') {
    const history = tracker.getHistory(20);
    console.log('\n📜 最近使用记录:\n');
    for (const turn of history) {
      console.log(`  轮次 ${turn.turn}: in=${turn.inputTokens}, out=${turn.outputTokens}, total=${turn.totalTokens}`);
    }
    return 0;
  }

  printHelp();
  return 0;
}

// ============ 导出 ============

export { MODEL_PRICING };

// ============ CLI 入口 ============

const isMain = import.meta.url === pathToFileURL(process.argv[1]).href;
if (isMain) {
  const cliArgs = process.argv.slice(2);
  if (cliArgs[0] === '--help' || cliArgs[0] === '-h') {
    printHelp();
  } else {
    main(cliArgs).then(code => process.exit(code));
  }
}
