/**
 * Evaluation Suite - 统一评估入口
 */

import RAGEvaluator from './rag-eval.js';
import ReasoningEvaluator from './reasoning-eval.js';
import HallucinationDetector from './hallucination-detector.js';
import { EventEmitter } from 'events';

/**
 * 统一评估器
 */
export class Evaluator extends EventEmitter {
  constructor(config = {}) {
    super();
    this.ragEvaluator = new RAGEvaluator(config.rag);
    this.reasoningEvaluator = new ReasoningEvaluator(config.reasoning);
    this.hallucinationDetector = new HallucinationDetector(config.hallucination);
  }

  /**
   * 运行完整评估
   */
  async evaluate(type, params) {
    switch (type) {
      case 'rag':
        return await this.ragEvaluator.evaluate(params);
      case 'reasoning':
        return await this.reasoningEvaluator.evaluate(params);
      case 'hallucination':
        return await this.hallucinationDetector.detect(params);
      default:
        throw new Error(`Unknown evaluation type: ${type}`);
    }
  }

  /**
   * 批量评估
   */
  async batchEvaluate(type, testCases) {
    switch (type) {
      case 'rag':
        return await this.ragEvaluator.batchEvaluate(testCases);
      case 'reasoning':
        return await this.reasoningEvaluator.batchEvaluate(testCases);
      case 'hallucination':
        return await this.hallucinationDetector.batchDetect(testCases);
      default:
        throw new Error(`Unknown evaluation type: ${type}`);
    }
  }

  /**
   * 生成评估报告
   */
  generateReport(results) {
    return {
      timestamp: new Date().toISOString(),
      summary: {
        totalTests: results.total,
        passed: results.passed,
        failed: results.total - results.passed,
        passRate: results.passRate,
        avgScore: results.avgScore
      },
      details: results.results
    };
  }
}

export { RAGEvaluator, ReasoningEvaluator, HallucinationDetector };
export default Evaluator;
