/**
 * Model Router - 动态模型路由
 * 根据任务复杂度自动选择最合适的模型
 */
const { promisify } = require('util');
const { exec } = require('child_process');
const execAsync = promisify(exec);

// 动态定价配置
const MODEL_PRICING = {
  'gpt-4o': { input: 0.005, output: 0.015 },
  'gpt-4o-mini': { input: 0.00015, output: 0.0006 },
  'claude-3.5-sonnet': { input: 0.003, output: 0.015 },
  'claude-3-haiku': { input: 0.00025, output: 0.00125 },
  'glm-4-flash': { input: 0.0001, output: 0.0001 },
};

// 模型能力评分
const MODEL_CAPABILITIES = {
  'gpt-4o': { reasoning: 95, creativity: 90, speed: 70 },
  'gpt-4o-mini': { reasoning: 80, creativity: 75, speed: 95 },
  'claude-3.5-sonnet': { reasoning: 95, creativity: 85, speed: 75 },
  'claude-3-haiku': { reasoning: 70, creativity: 65, speed: 95 },
  'glm-4-flash': { reasoning: 65, creativity: 60, speed: 90 },
};

class ModelRouter {
  constructor(config = {}) {
    this.config = config;
    this.localModels = config.localModels || [];
  }

  /**
   * 评估任务复杂度 (0-100)
   */
  calculateComplexity(task) {
    let score = 30; // 基础分

    // 上下文长度
    const contextLength = task.contextLength || 0;
    if (contextLength > 100000) score += 30;
    else if (contextLength > 50000) score += 20;
    else if (contextLength > 10000) score += 10;

    // 任务类型
    const taskType = task.type || 'general';
    const complexTasks = ['reasoning', 'analysis', 'coding', 'math'];
    if (complexTasks.includes(taskType)) score += 25;

    // 质量要求
    if (task.quality === 'high') score += 15;
    else if (task.quality === 'medium') score += 8;

    return Math.min(100, score);
  }

  /**
   * 估算任务成本
   */
  estimateCost(model, inputTokens, outputTokens) {
    const pricing = MODEL_PRICING[model] || { input: 0.001, output: 0.002 };
    return (inputTokens * pricing.input + outputTokens * pricing.output) / 1000;
  }

  /**
   * 选择最优模型
   */
  async selectModel(task) {
    const complexity = this.calculateComplexity(task);

    // 简单任务优先考虑成本
    if (complexity < 40) {
      // 检查本地模型
      if (this.localModels.length > 0) {
        return { model: this.localModels[0], cost: 0, reason: '使用本地零成本模型' };
      }

      // 选择最便宜的云端模型
      const candidates = ['gpt-4o-mini', 'glm-4-flash', 'claude-3-haiku'];
      const selected = candidates[0];
      return {
        model: selected,
        cost: this.estimateCost(selected, task.inputTokens || 1000, task.outputTokens || 500),
        reason: `简单任务(${complexity}分)，选择经济模型`
      };
    }

    // 中等复杂度
    if (complexity < 70) {
      const selected = 'gpt-4o-mini';
      return {
        model: selected,
        cost: this.estimateCost(selected, task.inputTokens || 2000, task.outputTokens || 1000),
        reason: `中等任务(${complexity}分)，平衡成本与质量`
      };
    }

    // 高复杂度
    return {
      model: 'claude-3.5-sonnet',
      cost: this.estimateCost('claude-3.5-sonnet', task.inputTokens || 5000, task.outputTokens || 2000),
      reason: `复杂任务(${complexity}分)，选择高性能模型`
    };
  }

  /**
   * 检查本地模型可用性
   */
  async checkLocalModels() {
    try {
      const { stdout } = await execAsync('ollama list 2>/dev/null || echo "not found"', { timeout: 5000 });
      if (stdout.includes('NAME')) {
        const models = stdout.split('\n')
          .slice(1)
          .filter(line => line.trim())
          .map(line => 'ollama/' + line.split(' ')[0]);
        return models;
      }
    } catch (e) {
      // 本地模型不可用
    }
    return [];
  }
}

module.exports = ModelRouter;
