/**
 * Evaluation Suite - RAG 评估
 * 基于 RAGAS 指标的检索增强生成评估
 */

import { EventEmitter } from 'events';

/**
 * RAG 评估器
 */
export class RAGEvaluator extends EventEmitter {
  constructor(config = {}) {
    super();
    this.thresholds = {
      contextRelevance: config.contextRelevanceThreshold || 0.7,
      faithfulness: config.faithfulnessThreshold || 0.8,
      answerRelevance: config.answerRelevanceThreshold || 0.7,
      contextRecall: config.contextRecallThreshold || 0.7
    };
  }

  /**
   * 评估 RAG 结果
   * @param {Object} params
   * @param {string} params.query - 查询
   * @param {string} params.answer - 生成的答案
   * @param {Array<string>} params.contexts - 检索的上下文
   * @param {string} params.groundTruth - 标准答案（可选）
   * @returns {Promise<Object>} - 评估结果
   */
  async evaluate({ query, answer, contexts, groundTruth }) {
    this.emit('evaluation-started', { type: 'rag' });

    const results = {
      query,
      metrics: {}
    };

    // 1. 上下文相关性 (Context Relevance)
    results.metrics.contextRelevance = await this.evaluateContextRelevance(
      query, contexts
    );

    // 2. 忠实度 (Faithfulness)
    results.metrics.faithfulness = await this.evaluateFaithfulness(
      answer, contexts
    );

    // 3. 答案相关性 (Answer Relevance)
    results.metrics.answerRelevance = await this.evaluateAnswerRelevance(
      query, answer
    );

    // 4. 上下文召回率 (Context Recall) - 需要标准答案
    if (groundTruth) {
      results.metrics.contextRecall = await this.evaluateContextRecall(
        groundTruth, contexts
      );
      results.groundTruth = groundTruth;
    }

    // 计算总分
    results.overallScore = this.calculateOverallScore(results.metrics);
    results.passed = this.checkThresholds(results.metrics);

    this.emit('evaluation-completed', { type: 'rag', results });
    return results;
  }

  /**
   * 上下文相关性 - 检索的上下文与查询的相关程度
   */
  async evaluateContextRelevance(query, contexts) {
    // 简化实现：基于关键词匹配
    const queryWords = new Set(query.toLowerCase().split(/\s+/));
    let totalScore = 0;

    for (const context of contexts) {
      const contextWords = new Set(context.toLowerCase().split(/\s+/));
      const intersection = [...queryWords].filter(w => contextWords.has(w));
      const score = intersection.length / queryWords.size;
      totalScore += score;
    }

    return {
      score: contexts.length > 0 ? totalScore / contexts.length : 0,
      details: `${contexts.length} contexts evaluated`
    };
  }

  /**
   * 忠实度 - 答案是否基于上下文（无幻觉）
   */
  async evaluateFaithfulness(answer, contexts) {
    // 简化实现：检查答案中的信息是否在上下文中
    const contextText = contexts.join(' ').toLowerCase();
    const answerSentences = answer.split(/[.!?]+/).filter(s => s.trim());
    
    let faithfulSentences = 0;
    for (const sentence of answerSentences) {
      const words = sentence.toLowerCase().split(/\s+/).filter(w => w.length > 3);
      const foundInContext = words.some(w => contextText.includes(w));
      if (foundInContext) faithfulSentences++;
    }

    const score = answerSentences.length > 0 
      ? faithfulSentences / answerSentences.length 
      : 0;

    return {
      score,
      details: `${faithfulSentences}/${answerSentences.length} sentences faithful`
    };
  }

  /**
   * 答案相关性 - 答案是否直接回答问题
   */
  async evaluateAnswerRelevance(query, answer) {
    // 简化实现：基于关键词重叠
    const queryWords = new Set(query.toLowerCase().split(/\s+/));
    const answerWords = answer.toLowerCase().split(/\s+/);
    
    let relevantWords = 0;
    for (const word of answerWords) {
      if (queryWords.has(word) || word.length > 4) {
        relevantWords++;
      }
    }

    const score = answerWords.length > 0 ? relevantWords / answerWords.length : 0;

    return {
      score: Math.min(score * 1.5, 1.0), // 调整分数
      details: `Answer length: ${answerWords.length} words`
    };
  }

  /**
   * 上下文召回率 - 上下文是否包含标准答案的信息
   */
  async evaluateContextRecall(groundTruth, contexts) {
    const contextText = contexts.join(' ').toLowerCase();
    const truthWords = groundTruth.toLowerCase().split(/\s+/).filter(w => w.length > 3);
    
    let recalledWords = 0;
    for (const word of truthWords) {
      if (contextText.includes(word)) recalledWords++;
    }

    const score = truthWords.length > 0 ? recalledWords / truthWords.length : 0;

    return {
      score,
      details: `${recalledWords}/${truthWords.length} key words recalled`
    };
  }

  /**
   * 计算总分
   */
  calculateOverallScore(metrics) {
    const scores = [
      metrics.contextRelevance?.score || 0,
      metrics.faithfulness?.score || 0,
      metrics.answerRelevance?.score || 0,
      metrics.contextRecall?.score || 0
    ].filter(s => s > 0);

    return scores.reduce((a, b) => a + b, 0) / scores.length;
  }

  /**
   * 检查阈值
   */
  checkThresholds(metrics) {
    return (
      (metrics.contextRelevance?.score || 1) >= this.thresholds.contextRelevance &&
      (metrics.faithfulness?.score || 1) >= this.thresholds.faithfulness &&
      (metrics.answerRelevance?.score || 1) >= this.thresholds.answerRelevance &&
      (metrics.contextRecall?.score || 1) >= this.thresholds.contextRecall
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

    // 计算统计
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

export default RAGEvaluator;
