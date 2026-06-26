/**
 * Evaluation Suite - 推理评估
 * 评估多步骤推理和逻辑正确性
 */

import { EventEmitter } from 'events';

/**
 * 推理评估器
 */
export class ReasoningEvaluator extends EventEmitter {
  constructor(config = {}) {
    super();
    this.thresholds = {
      stepCompleteness: config.stepCompletenessThreshold || 0.7,
      logicalConsistency: config.logicalConsistencyThreshold || 0.8,
      conclusionValidity: config.conclusionValidityThreshold || 0.8
    };
  }

  /**
   * 评估推理过程
   * @param {Object} params
   * @param {string} params.question - 问题
   * @param {Array<string>} params.steps - 推理步骤
   * @param {string} params.conclusion - 结论
   * @param {string} params.expectedAnswer - 期望答案（可选）
   * @returns {Promise<Object>} - 评估结果
   */
  async evaluate({ question, steps, conclusion, expectedAnswer }) {
    this.emit('evaluation-started', { type: 'reasoning' });

    const results = {
      question,
      steps: steps.length,
      metrics: {}
    };

    // 1. 步骤完整性
    results.metrics.stepCompleteness = this.evaluateStepCompleteness(steps);

    // 2. 逻辑一致性
    results.metrics.logicalConsistency = this.evaluateLogicalConsistency(steps);

    // 3. 结论有效性
    results.metrics.conclusionValidity = this.evaluateConclusionValidity(
      steps, conclusion
    );

    // 4. 答案正确性（如果有期望答案）
    if (expectedAnswer) {
      results.metrics.answerCorrectness = this.evaluateAnswerCorrectness(
        conclusion, expectedAnswer
      );
      results.expectedAnswer = expectedAnswer;
    }

    // 计算总分
    results.overallScore = this.calculateOverallScore(results.metrics);
    results.passed = this.checkThresholds(results.metrics);

    this.emit('evaluation-completed', { type: 'reasoning', results });
    return results;
  }

  /**
   * 步骤完整性 - 推理步骤是否完整
   */
  evaluateStepCompleteness(steps) {
    // 检查步骤数量和质量
    const minSteps = 2;
    const idealSteps = 5;
    
    let score = 0;
    
    // 基础分：有步骤
    if (steps.length >= minSteps) {
      score += 0.4;
    }
    
    // 步骤数量分
    const stepScore = Math.min(steps.length / idealSteps, 1) * 0.3;
    score += stepScore;
    
    // 步骤质量分（检查是否有解释性内容）
    const qualitySteps = steps.filter(s => s.length > 20).length;
    const qualityScore = (qualitySteps / steps.length) * 0.3;
    score += qualityScore;

    return {
      score: Math.min(score, 1),
      details: `${steps.length} steps, ${qualitySteps} quality steps`
    };
  }

  /**
   * 逻辑一致性 - 步骤之间是否逻辑连贯
   */
  evaluateLogicalConsistency(steps) {
    // 简化实现：检查步骤间的过渡词
    const transitionWords = [
      '因为', '所以', '因此', '首先', '然后', '接着', '最后',
      'since', 'therefore', 'thus', 'first', 'then', 'next', 'finally',
      '如果', '那么', '假设', '结论', 'if', 'then', 'assume', 'conclusion'
    ];
    
    let transitions = 0;
    for (let i = 1; i < steps.length; i++) {
      const prevStep = steps[i - 1].toLowerCase();
      const currStep = steps[i].toLowerCase();
      
      // 检查是否有过渡词
      if (transitionWords.some(w => currStep.includes(w))) {
        transitions++;
      }
      
      // 检查是否有内容重叠（连贯性）
      const prevWords = new Set(prevStep.split(/\s+/));
      const currWords = currStep.split(/\s+/);
      const overlap = currWords.filter(w => prevWords.has(w)).length;
      if (overlap > 0) transitions += 0.5;
    }

    const score = steps.length > 1 ? transitions / (steps.length - 1) : 0;

    return {
      score: Math.min(score, 1),
      details: `${Math.floor(transitions)} logical transitions found`
    };
  }

  /**
   * 结论有效性 - 结论是否由步骤合理推出
   */
  evaluateConclusionValidity(steps, conclusion) {
    if (!conclusion || steps.length === 0) {
      return { score: 0, details: 'No conclusion or steps' };
    }

    // 检查结论是否与步骤相关
    const allStepsText = steps.join(' ').toLowerCase();
    const conclusionWords = conclusion.toLowerCase().split(/\s+/).filter(w => w.length > 3);
    
    let relevantWords = 0;
    for (const word of conclusionWords) {
      if (allStepsText.includes(word)) {
        relevantWords++;
      }
    }

    const relevanceScore = conclusionWords.length > 0 
      ? relevantWords / conclusionWords.length 
      : 0;

    // 检查结论长度（过短可能不合理）
    const lengthScore = conclusion.length > 10 ? 0.3 : 0;

    return {
      score: Math.min(relevanceScore * 0.7 + lengthScore, 1),
      details: `${relevantWords}/${conclusionWords.length} words from steps`
    };
  }

  /**
   * 答案正确性 - 与期望答案对比
   */
  evaluateAnswerCorrectness(conclusion, expectedAnswer) {
    const conclusionNorm = conclusion.toLowerCase().trim();
    const expectedNorm = expectedAnswer.toLowerCase().trim();
    
    // 完全匹配
    if (conclusionNorm === expectedNorm) {
      return { score: 1, details: 'Exact match' };
    }
    
    // 关键词匹配
    const conclusionWords = new Set(conclusionNorm.split(/\s+/).filter(w => w.length > 3));
    const expectedWords = expectedNorm.split(/\s+/).filter(w => w.length > 3);
    
    const matches = expectedWords.filter(w => conclusionWords.has(w)).length;
    const score = expectedWords.length > 0 ? matches / expectedWords.length : 0;

    return {
      score,
      details: `${matches}/${expectedWords.length} key words matched`
    };
  }

  /**
   * 计算总分
   */
  calculateOverallScore(metrics) {
    const scores = [
      metrics.stepCompleteness?.score || 0,
      metrics.logicalConsistency?.score || 0,
      metrics.conclusionValidity?.score || 0,
      metrics.answerCorrectness?.score || 0
    ].filter(s => s > 0);

    return scores.reduce((a, b) => a + b, 0) / scores.length;
  }

  /**
   * 检查阈值
   */
  checkThresholds(metrics) {
    return (
      (metrics.stepCompleteness?.score || 1) >= this.thresholds.stepCompleteness &&
      (metrics.logicalConsistency?.score || 1) >= this.thresholds.logicalConsistency &&
      (metrics.conclusionValidity?.score || 1) >= this.thresholds.conclusionValidity
    );
  }

  /**
   * 批量评估
   */
  async batchEvaluate(testCases) {
    const results = [];
    
    for (const testCase of testCases) {
      try {
        const result = await this.evaluate(testCase);
        results.push({ ...result, success: true });
      } catch (error) {
        results.push({ ...testCase, success: false, error: error.message });
      }
    }

    const successful = results.filter(r => r.success);
    const passed = results.filter(r => r.passed);
    
    return {
      total: results.length,
      successful: successful.length,
      passed: passed.length,
      passRate: results.length > 0 ? passed.length / results.length : 0,
      avgScore: successful.length > 0 
        ? successful.reduce((a, r) => a + r.overallScore, 0) / successful.length 
        : 0,
      results
    };
  }
}

export default ReasoningEvaluator;
