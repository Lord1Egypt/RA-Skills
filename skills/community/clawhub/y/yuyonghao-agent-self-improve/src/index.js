/**
 * Agent Self-Improve - Main Entry Point
 * Agent 自我改进系统
 */

import PerformanceAnalyzer from './performance-analyzer.js';
import StrategyOptimizer from './strategy-optimizer.js';

class SelfImprovementSystem {
  constructor(options = {}) {
    this.options = options;
    this.analyzer = new PerformanceAnalyzer(options.analyzer);
    this.optimizer = new StrategyOptimizer(options.optimizer);
    this.history = [];
  }

  async analyze(target) {
    return await this.analyzer.profile(target);
  }

  async improve(options = {}) {
    const strategy = options.strategy || 'default';
    return await this.optimizer.optimize({ strategy, ...options });
  }

  getImprovementHistory() {
    return this.history;
  }
}

export {
  SelfImprovementSystem,
  PerformanceAnalyzer,
  StrategyOptimizer
};

export default SelfImprovementSystem;
