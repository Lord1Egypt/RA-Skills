/**
 * ReAct Orchestrator - 双系统 AI 代理协调器
 * 
 * 基于 ReAct (Reason+Act) 框架，实现：
 * - System 1: 快速直觉执行 (~3-5s)
 * - System 2: 深度反思推理 (~10-15s，带 Reflexion)
 * 
 * @author 余永浩
 * @version 0.1.0
 */

const { System1Engine } = require('./system1');
const { System2Engine } = require('./system2');
const { ToolRegistry } = require('./tool-registry');

class ReActOrchestrator {
  constructor(options = {}) {
    this.system1 = new System1Engine(options);
    this.system2 = new System2Engine(options);
    this.toolRegistry = new ToolRegistry();
    
    // 配置
    this.config = {
      // 任务复杂度阈值（0-1，> 阈值用 System 2）
      complexityThreshold: options.complexityThreshold ?? 0.5,
      // System 1 超时 (秒)
      system1Timeout: options.system1Timeout ?? 30,
      // System 2 超时 (秒)
      system2Timeout: options.system2Timeout ?? 120,
      // 最大迭代次数
      maxIterationsSystem1: options.maxIterationsSystem1 ?? 5,
      maxIterationsSystem2: options.maxIterationsSystem2 ?? 15,
      // 是否启用日志
      verbose: options.verbose ?? false,
    };

    this.log('🦞 ReAct Orchestrator 初始化完成');
  }

  log(...args) {
    if (this.config.verbose) {
      console.log('[ReAct]', ...args);
    }
  }

  /**
   * 注册工具到工具层
   * @param {string} name - 工具名称
   * @param {Function} fn - 工具函数
   * @param {Object} metadata - 工具元数据（描述、参数 schema 等）
   */
  registerTool(name, fn, metadata = {}) {
    this.toolRegistry.register(name, fn, metadata);
    this.log(`✅ 注册工具：${name}`);
  }

  /**
   * 批量注册工具
   * @param {Array} tools - [{name, fn, metadata}]
   */
  registerTools(tools) {
    tools.forEach(({ name, fn, metadata }) => {
      this.registerTool(name, fn, metadata);
    });
  }

  /**
   * 评估任务复杂度（0-1）
   * 决定使用 System 1 还是 System 2
   * 
   * @param {string} query - 用户查询
   * @returns {Promise<{mode: 'system1'|'system2', score: number, reasons: string[]}>}
   */
  async evaluateComplexity(query) {
    const q = query.toLowerCase();
    const indicators = {
      // 多步推理信号
      multiStep: q.includes('然后') || q.includes('接着') || q.includes('之后') || q.includes('分步骤') || q.includes('第一步') || q.includes('第二步') || q.includes('并'),
      // 条件/分支信号
      conditional: q.includes('如果') || q.includes('否则') || q.includes('假设'),
      // 创造性/开放性
      openEnded: q.includes('分析') || q.includes('评估') || q.includes('比较') || q.includes('设计') || q.includes('规划') || q.includes('策略') || q.includes('建议'),
      // 需要外部知识
      knowledgeIntensive: q.includes('最新') || q.includes('202') || q.includes('趋势') || q.includes('研究') || q.includes('调查') || q.includes('调研'),
      // 需要代码/技术操作
      technical: q.includes('代码') || q.includes('编程') || q.includes('脚本') || q.includes('调试') || q.includes('优化'),
      // 长度信号（长查询通常更复杂）
      longQuery: query.length > 50,
    };

    const score = Object.values(indicators).filter(Boolean).length / Object.keys(indicators).length;
    const reasons = Object.entries(indicators)
      .filter(([_, v]) => v)
      .map(([k]) => k);

    const mode = score >= this.config.complexityThreshold ? 'system2' : 'system1';

    this.log(`📊 复杂度评估：${score.toFixed(2)} → ${mode.toUpperCase()} (${reasons.join(', ') || '简单任务'})`);

    return { mode, score, reasons };
  }

  /**
   * 执行 ReAct 推理循环
   * 
   * @param {string} query - 用户查询
   * @param {Object} options - 执行选项
   * @param {'auto'|'system1'|'system2'} options.mode - 执行模式（auto=自动选择）
   * @param {number} options.timeout - 超时秒数（覆盖默认）
   * @returns {Promise<{answer: string, history: Array, mode: string, iterations: number, duration: number}>}
   */
  async execute(query, options = {}) {
    const startTime = Date.now();
    const mode = options.mode === 'auto' || !options.mode 
      ? (await this.evaluateComplexity(query)).mode 
      : options.mode;

    this.log(`🚀 开始执行 [${mode.toUpperCase()}]: ${query.substring(0, 50)}...`);

    let result;
    try {
      if (mode === 'system1') {
        result = await this.executeSystem1(query, options);
      } else {
        result = await this.executeSystem2(query, options);
      }

      const duration = ((Date.now() - startTime) / 1000).toFixed(2);
      this.log(`✅ 完成 [${mode}] 耗时：${duration}s, 迭代：${result.iterations}`);

      return {
        ...result,
        mode,
        duration: parseFloat(duration),
      };
    } catch (error) {
      this.log(`❌ 执行失败：${error.message}`);
      throw error;
    }
  }

  /**
   * System 1 快速执行路径
   */
  async executeSystem1(query, options = {}) {
    return await this.system1.run(query, {
      toolRegistry: this.toolRegistry,
      timeout: options.timeout ?? this.config.system1Timeout,
      maxIterations: options.maxIterations ?? this.config.maxIterationsSystem1,
      verbose: this.config.verbose,
    });
  }

  /**
   * System 2 深度推理路径（带 Reflexion）
   */
  async executeSystem2(query, options = {}) {
    return await this.system2.run(query, {
      toolRegistry: this.toolRegistry,
      timeout: options.timeout ?? this.config.system2Timeout,
      maxIterations: options.maxIterations ?? this.config.maxIterationsSystem2,
      verbose: this.config.verbose,
    });
  }

  /**
   * 获取工具列表
   */
  getAvailableTools() {
    return this.toolRegistry.list();
  }

  /**
   * 导出执行历史用于调试/审计
   */
  exportHistory(history) {
    return JSON.stringify(history, null, 2);
  }
}

// 导出
module.exports = { ReActOrchestrator };
