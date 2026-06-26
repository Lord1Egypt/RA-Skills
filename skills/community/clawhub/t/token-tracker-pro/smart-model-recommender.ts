// 智能模型推荐系统

import fs from 'fs';
import path from 'path';

interface ModelStats {
  model: string;
  totalTokens: number;
  totalCost: number;  // 假设价格
  recordCount: number;
  averageTokens: number;
  averageCost: number;
  costPerToken: number;
  successRate?: number;
  avgResponseTime?: number;
}

interface TaskComplexity {
  simple: number;    // 简单任务（<100 tokens）
  medium: number;    // 中等任务（100-1000 tokens）
  complex: number;   // 复杂任务（1000-10000 tokens）
  veryComplex: number; // 非常复杂（>10000 tokens）
}

interface ModelRecommendation {
  primaryModel: string;      // 首选模型
  fallbackModel: string;     // 备选模型
  reason: string;            // 推荐理由
  expectedSavings: number;   // 预计节省（%）
  costPerTokenComparison: string;  // 价格对比
}

interface CostAnalysis {
  currentCost: number;
  optimizedCost: number;
  savings: number;
  savingsPercent: number;
  monthlySavings: number;
}

// 模型价格配置（单位：每百万 token 价格）
const MODEL_PRICES = {
  'zai/glm-4.7-flash': {
    inputPrice: 0.0001,    // $0.0001 / 1M tokens
    outputPrice: 0.0003,
    name: 'zai/glm-4.7-flash',
    tier: 'high-efficiency'
  },
  'zai/glm-4.7': {
    inputPrice: 0.0003,
    outputPrice: 0.0006,
    name: 'zai/glm-4.7',
    tier: 'standard'
  },
  'zai/glm-4.7-pro': {
    inputPrice: 0.0006,
    outputPrice: 0.0012,
    name: 'zai/glm-4.7-pro',
    tier: 'premium'
  },
  'gpt-4': {
    inputPrice: 0.03,
    outputPrice: 0.06,
    name: 'gpt-4',
    tier: 'enterprise'
  },
  'gpt-3.5-turbo': {
    inputPrice: 0.0005,
    outputPrice: 0.0015,
    name: 'gpt-3.5-turbo',
    tier: 'cost-effective'
  },
  'claude-3-opus': {
    inputPrice: 0.015,
    outputPrice: 0.075,
    name: 'claude-3-opus',
    tier: 'premium'
  },
  'claude-3-sonnet': {
    inputPrice: 0.003,
    outputPrice: 0.015,
    name: 'claude-3-sonnet',
    tier: 'balanced'
  },
  'unknown': {
    inputPrice: 0.001,
    outputPrice: 0.002,
    name: 'unknown',
    tier: 'default'
  }
};

class SmartModelRecommender {
  private dataPath: string;
  private modelStats: Map<string, ModelStats> = new Map();
  private taskComplexity: TaskComplexity;

  constructor() {
    const homeDir = process.env.OPENCLAW_HOME || process.env.HOME;
    this.dataPath = path.join(homeDir || '', '.openclaw', 'skills/token-tracker/data/token-history.json');
    this.taskComplexity = {
      simple: 0,
      medium: 0,
      complex: 0,
      veryComplex: 0
    };
    this.loadData();
  }

  // 加载数据
  private loadData(): void {
    try {
      if (fs.existsSync(this.dataPath)) {
        const content = fs.readFileSync(this.dataPath, 'utf-8');
        const data = JSON.parse(content);
        
        // 分析模型使用情况
        data.tokens.forEach(record => {
          this.recordModelUsage(record);
        });

        // 分析任务复杂度
        this.analyzeTaskComplexity();
      }
    } catch (error) {
      console.error('Failed to load model recommendation data:', error);
    }
  }

  // 记录模型使用情况
  private recordModelUsage(record: any): void {
    const model = record.model || 'unknown';
    const tokens = record.tokens || 0;
    const price = this.getModelPrice(model);

    if (!this.modelStats.has(model)) {
      this.modelStats.set(model, {
        model,
        totalTokens: 0,
        totalCost: 0,
        recordCount: 0,
        averageTokens: 0,
        averageCost: 0,
        costPerToken: 0
      });
    }

    const stats = this.modelStats.get(model)!;
    stats.totalTokens += tokens;
    stats.totalCost += this.calculateCost(tokens, price);
    stats.recordCount++;

    if (stats.recordCount > 0) {
      stats.averageTokens = stats.totalTokens / stats.recordCount;
      stats.averageCost = stats.totalCost / stats.recordCount;
      stats.costPerToken = stats.totalTokens > 0 ? stats.totalCost / stats.totalTokens : 0;
    }
  }

  // 获取模型价格
  private getModelPrice(model: string): any {
    return MODEL_PRICES[model] || MODEL_PRICES['unknown'];
  }

  // 计算成本
  private calculateCost(tokens: number, price: any): number {
    const inputCost = Math.floor(tokens / 1_000_000) * price.inputPrice;
    const outputCost = Math.floor(tokens / 1_000_000) * price.outputPrice;
    return inputCost + outputCost;
  }

  // 分析任务复杂度
  private analyzeTaskComplexity(): void {
    this.modelStats.forEach((stats, model) => {
      if (stats.averageTokens < 100) {
        this.taskComplexity.simple++;
      } else if (stats.averageTokens < 1000) {
        this.taskComplexity.medium++;
      } else if (stats.averageTokens < 10000) {
        this.taskComplexity.complex++;
      } else {
        this.taskComplexity.veryComplex++;
      }
    });
  }

  // 获取所有模型统计
  getAllModelStats(): ModelStats[] {
    return Array.from(this.modelStats.values()).sort(
      (a, b) => b.costPerToken - a.costPerToken
    );
  }

  // 获取成本最低的模型
  getMostCostEffectiveModel(): ModelStats | null {
    const allModels = this.getAllModelStats();
    if (allModels.length === 0) return null;
    return allModels.reduce((prev, current) =>
      (prev.costPerToken < current.costPerToken ? prev : current), allModels[0]
    );
  }

  // 获取性价比最高的模型
  getBestValueModel(): ModelStats | null {
    const allModels = this.getAllModelStats();
    if (allModels.length === 0) return null;
    return allModels.reduce((prev, current) =>
      (prev.costPerToken < current.costPerToken ? prev : current), allModels[0]
    );
  }

  // 根据任务复杂度推荐模型
  recommendByComplexity(taskTokens: number): ModelRecommendation {
    const complexity = this.getTaskComplexity(taskTokens);
    const allModels = this.getAllModelStats();

    // 获取成本最低的模型
    const cheapestModel = this.getMostCostEffectiveModel();
    
    // 获取性价比最高的模型
    const bestValueModel = this.getBestValueModel();

    let recommendation: ModelRecommendation;

    switch (complexity) {
      case 'simple':
        // 简单任务：使用最便宜的模型
        recommendation = {
          primaryModel: cheapestModel?.model || 'zai/glm-4.7-flash',
          fallbackModel: bestValueModel?.model || 'zai/glm-4.7',
          reason: `简单任务（${taskTokens} tokens），使用成本最低的模型可节省 ${this.calculateExpectedSavings(taskTokens, cheapestModel?.model)}%`,
          expectedSavings: this.calculateExpectedSavings(taskTokens, cheapestModel?.model) || 0,
          costPerTokenComparison: this.compareCostPerToken(cheapestModel?.model || '', bestValueModel?.model || '')
        };
        break;

      case 'medium':
        // 中等任务：使用性价比高的模型
        recommendation = {
          primaryModel: bestValueModel?.model || 'zai/glm-4.7',
          fallbackModel: cheapestModel?.model || 'zai/glm-4.7-flash',
          reason: `中等任务（${taskTokens} tokens），性价比最高的模型可平衡成本和质量`,
          expectedSavings: this.calculateExpectedSavings(taskTokens, bestValueModel?.model) || 0,
          costPerTokenComparison: this.compareCostPerToken(bestValueModel?.model || '', cheapestModel?.model || '')
        };
        break;

      case 'complex':
        // 复杂任务：使用质量较好的模型
        recommendation = {
          primaryModel: 'zai/glm-4.7-pro',
          fallbackModel: 'zai/glm-4.7',
          reason: `复杂任务（${taskTokens} tokens），建议使用更强大的模型以保证质量`,
          expectedSavings: 0,
          costPerTokenComparison: 'pro模型成本更高，但质量更好'
        };
        break;

      case 'veryComplex':
        // 非常复杂任务：使用最高质量模型
        recommendation = {
          primaryModel: 'gpt-4',
          fallbackModel: 'claude-3-opus',
          reason: `非常复杂任务（${taskTokens} tokens），建议使用顶级模型`,
          expectedSavings: 0,
          costPerTokenComparison: '顶级模型成本最高，但质量最优'
        };
        break;

      default:
        recommendation = {
          primaryModel: 'zai/glm-4.7-flash',
          fallbackModel: 'zai/glm-4.7',
          reason: '默认推荐：使用高性价比模型',
          expectedSavings: 0,
          costPerTokenComparison: 'flash: $0.0004/M, 4.7: $0.0009/M'
        };
    }

    return recommendation;
  }

  // 获取任务复杂度等级
  private getTaskComplexity(tokens: number): 'simple' | 'medium' | 'complex' | 'veryComplex' {
    if (tokens < 100) return 'simple';
    if (tokens < 1000) return 'medium';
    if (tokens < 10000) return 'complex';
    return 'veryComplex';
  }

  // 计算预期节省
  private calculateExpectedSavings(tokens: number, model: string | undefined): number | null {
    if (!model) return null;
    
    const currentModelPrice = this.getModelPrice(model);
    const cheapestModelPrice = this.getModelPrice('zai/glm-4.7-flash');
    
    if (!currentModelPrice || !cheapestModelPrice) return null;
    
    const currentCost = this.calculateCost(tokens, currentModelPrice);
    const cheapestCost = this.calculateCost(tokens, cheapestModelPrice);
    
    const savings = ((currentCost - cheapestCost) / currentCost * 100);
    return savings > 0 ? Math.round(savings) : 0;
  }

  // 比较每 token 成本
  private compareCostPerToken(model1: string, model2: string): string {
    const price1 = this.getModelPrice(model1);
    const price2 = this.getModelPrice(model2);
    
    if (!price1 || !price2) return '无法比较';
    
    const cost1 = (price1.inputPrice + price1.outputPrice) / 2;
    const cost2 = (price2.inputPrice + price2.outputPrice) / 2;
    
    const ratio = (cost1 / cost2).toFixed(2);
    
    if (ratio < 1) {
      return `${model1}: $${cost1.toFixed(6)} < ${model2}: $${cost2.toFixed(6)} (便宜 ${(1 - ratio) * 100}%)`;
    } else {
      return `${model1}: $${cost1.toFixed(6)} > ${model2}: $${cost2.toFixed(6)} (贵 ${(ratio - 1) * 100}%)`;
    }
  }

  // 分析当前成本优化空间
  analyzeCostOptimization(): CostAnalysis {
    const allModels = this.getAllModelStats();
    let currentCost = 0;
    let optimizedCost = 0;
    let highestSavings = 0;

    allModels.forEach(stats => {
      // 当前成本
      currentCost += stats.totalCost;

      // 优化成本（使用最便宜的模型）
      const cheapestModel = this.getMostCostEffectiveModel();
      if (cheapestModel && cheapestModel.model !== stats.model) {
        const expectedSavings = this.calculateExpectedSavings(stats.totalTokens, cheapestModel.model);
        if (expectedSavings && expectedSavings > highestSavings) {
          highestSavings = expectedSavings;
        }
      }
    });

    // 保守估计：假设可以节省 50%
    optimizedCost = currentCost * (1 - highestSavings / 100);

    return {
      currentCost,
      optimizedCost,
      savings: currentCost - optimizedCost,
      savingsPercent: highestSavings,
      monthlySavings: (currentCost - optimizedCost) * 30 // 假设每月30天
    };
  }

  // 获取使用场景推荐
  getScenarioRecommendation(scenario: string): ModelRecommendation {
    const scenarioRecommendations: Record<string, ModelRecommendation> = {
      '简单查询': {
        primaryModel: 'zai/glm-4.7-flash',
        fallbackModel: 'zai/glm-4.7',
        reason: '简单查询任务，使用最快最便宜的模型',
        expectedSavings: 55,
        costPerTokenComparison: 'flash: $0.0004/M, 4.7: $0.0009/M'
      },
      '代码生成': {
        primaryModel: 'zai/glm-4.7',
        fallbackModel: 'zai/glm-4.7-pro',
        reason: '代码生成需要质量，使用中等模型',
        expectedSavings: 30,
        costPerTokenComparison: '4.7: $0.0009/M, pro: $0.0018/M'
      },
      '数据分析': {
        primaryModel: 'zai/glm-4.7-pro',
        fallbackModel: 'zai/glm-4.7',
        reason: '数据分析需要准确性和深度',
        expectedSavings: 15,
        costPerTokenComparison: 'pro: $0.0018/M, 4.7: $0.0009/M'
      },
      '文本创作': {
        primaryModel: 'zai/glm-4.7',
        fallbackModel: 'zai/glm-4.7-pro',
        reason: '文本创作需要创造力，使用中等模型',
        expectedSavings: 30,
        costPerTokenComparison: '4.7: $0.0009/M, pro: $0.0018/M'
      },
      '翻译': {
        primaryModel: 'zai/glm-4.7-flash',
        fallbackModel: 'zai/glm-4.7',
        reason: '翻译任务，使用快速模型即可',
        expectedSavings: 55,
        costPerTokenComparison: 'flash: $0.0004/M, 4.7: $0.0009/M'
      },
      '总结': {
        primaryModel: 'zai/glm-4.7-flash',
        fallbackModel: 'zai/glm-4.7',
        reason: '总结任务，使用快速模型',
        expectedSavings: 55,
        costPerTokenComparison: 'flash: $0.0004/M, 4.7: $0.0009/M'
      },
      '问答': {
        primaryModel: 'zai/glm-4.7',
        fallbackModel: 'zai/glm-4.7-flash',
        reason: '问答任务，使用中等模型',
        expectedSavings: 30,
        costPerTokenComparison: '4.7: $0.0009/M, flash: $0.0004/M'
      },
      '复杂推理': {
        primaryModel: 'gpt-4',
        fallbackModel: 'claude-3-opus',
        reason: '复杂推理需要最强模型',
        expectedSavings: 0,
        costPerTokenComparison: 'gpt-4: $0.045/M, opus: $0.090/M'
      }
    };

    return scenarioRecommendations[scenario] || scenarioRecommendations['简单查询'];
  }

  // 生成详细报告
  generateDetailedReport(): string {
    const allModels = this.getAllModelStats();
    const costAnalysis = this.analyzeCostOptimization();
    const scenarioRecommendations = this.getScenarioRecommendation('简单查询');

    let report = '\n' + '='.repeat(70);
    report += '\n  🧠 智能模型推荐系统报告';
    report += '\n' + '='.repeat(70);
    report += '\n';

    // 模型使用统计
    report += '📊 模型使用统计\n';
    report += '─'.repeat(70);
    report += '\n';
    
    allModels.forEach((stats, index) => {
      const price = this.getModelPrice(stats.model);
      report += `\n${index + 1}. ${stats.model.padEnd(20)} `;
      report += `[${price.tier.padEnd(12)}] `;
      report += `💰 $${stats.totalCost.toFixed(4)} `;
      report += `(Token: ${stats.totalTokens.toLocaleString()}, `;
      report += `Cost/Token: $${stats.costPerToken.toFixed(6)})`;
      report += '\n';
    });

    // 任务复杂度分析
    report += '\n📈 任务复杂度分析\n';
    report += '─'.repeat(70);
    report += '\n';
    report += `简单任务: ${this.taskComplexity.simple} 次 (${this.getComplexityPercent('simple')}%)\n`;
    report += `中等任务: ${this.taskComplexity.medium} 次 (${this.getComplexityPercent('medium')}%)\n`;
    report += `复杂任务: ${this.taskComplexity.complex} 次 (${this.getComplexityPercent('complex')}%)\n`;
    report += `非常复杂: ${this.taskComplexity.veryComplex} 次 (${this.getComplexityPercent('veryComplex')}%)\n`;

    // 成本优化分析
    report += '\n💰 成本优化分析\n';
    report += '─'.repeat(70);
    report += '\n';
    report += `当前总成本: $${costAnalysis.currentCost.toFixed(4)}\n`;
    report += `优化后成本: $${costAnalysis.optimizedCost.toFixed(4)}\n`;
    report += `预计节省: $${costAnalysis.savings.toFixed(4)} (${costAnalysis.savingsPercent}%)\n`;
    report += `每月节省: $${costAnalysis.monthlySavings.toFixed(4)}\n`;

    // 场景推荐
    report += '\n🎯 使用场景推荐\n';
    report += '─'.repeat(70);
    report += '\n';
    report += `${scenarioRecommendations.primaryModel.padEnd(20)} ← 首选\n`;
    report += `${scenarioRecommendations.fallbackModel.padEnd(20)} ← 备选\n`;
    report += `理由: ${scenarioRecommendations.reason}\n`;
    report += `预期节省: ${scenarioRecommendations.expectedSavings}%\n`;
    report += `价格对比: ${scenarioRecommendations.costPerTokenComparison}\n`;

    // 模型推荐建议
    report += '\n💡 模型使用建议\n';
    report += '─'.repeat(70);
    report += '\n';
    
    if (costAnalysis.savingsPercent > 0) {
      report += `1. 优先使用 ${this.getMostCostEffectiveModel()?.model || 'zai/glm-4.7-flash'}\n`;
      report += `   预计可节省 ${costAnalysis.savingsPercent}%\n`;
    }

    report += '\n2. 根据任务复杂度选择：\n';
    report += '   - 简单任务（<100 tokens）→ 使用最便宜模型\n';
    report += '   - 中等任务（100-1000 tokens）→ 使用性价比模型\n';
    report += '   - 复杂任务（1000-10000 tokens）→ 使用中等模型\n';
    report += '   - 非常复杂（>10000 tokens）→ 使用顶级模型\n';

    report += '\n3. 根据使用场景选择：\n';
    const scenarios = Object.keys(this.getScenarioRecommendation(''));
    scenarios.slice(0, 4).forEach(scenario => {
      const rec = this.getScenarioRecommendation(scenario);
      report += `   - ${scenario} → ${rec.primaryModel}\n`;
    });

    report += '\n4. 模型性价比排序：\n';
    const sortedModels = [...allModels].sort((a, b) => a.costPerToken - b.costPerToken);
    sortedModels.forEach((stats, index) => {
      report += `   ${index + 1}. ${stats.model.padEnd(20)} $${stats.costPerToken.toFixed(6)}\n`;
    });

    report += '\n' + '='.repeat(70);
    report += '\n';

    return report;
  }

  // 获取复杂度百分比
  private getComplexityPercent(type: string): number {
    const total = this.taskComplexity.simple + this.taskComplexity.medium + 
                  this.taskComplexity.complex + this.taskComplexity.veryComplex;
    if (total === 0) return 0;
    return Math.round((this.taskComplexity[type as keyof TaskComplexity] / total) * 100);
  }

  // 保存报告
  saveReport(outputPath?: string): void {
    const report = this.generateDetailedReport();
    const path = outputPath || path.join(
      process.env.OPENCLAW_HOME || process.env.HOME || '',
      '.openclaw',
      'skills/token-tracker/data/model-recommendation-report.txt'
    );
    
    fs.writeFileSync(path, report, 'utf-8');
    console.log(`\n✅ 报告已保存到: ${path}\n`);
  }
}

// 导出单例
export const smartModelRecommender = new SmartModelRecommender();

export { SmartModelRecommender, ModelStats, TaskComplexity, ModelRecommendation, CostAnalysis };
