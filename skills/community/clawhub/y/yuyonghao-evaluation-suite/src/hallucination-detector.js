/**
 * Evaluation Suite - 幻觉检测器
 * 检测生成内容中的幻觉（虚构信息）
 */

import { EventEmitter } from 'events';

/**
 * 幻觉检测器
 */
export class HallucinationDetector extends EventEmitter {
  constructor(config = {}) {
    super();
    this.threshold = config.hallucinationThreshold || 0.3;
    
    // 幻觉信号词
    this.hallucinationSignals = [
      '可能', '也许', '大概', '或许',
      '我记得', '好像', '似乎',
      '根据我的知识', '据我所知',
      'maybe', 'perhaps', 'probably',
      'i think', 'i believe', 'in my opinion'
    ];
    
    // 不确定性标记
    this.uncertaintyMarkers = [
      '?', '...', '~', '左右', '上下',
      '大约', '估计', '大概'
    ];
  }

  /**
   * 检测幻觉
   * @param {Object} params
   * @param {string} params.text - 生成的文本
   * @param {Array<string>} params.sources - 源文档/上下文
   * @param {string} params.query - 原始查询
   * @returns {Promise<Object>} - 检测结果
   */
  async detect({ text, sources, query }) {
    this.emit('detection-started', { text: text.slice(0, 100) });

    const result = {
      text: text.slice(0, 500), // 截断显示
      hallucinationScore: 0,
      isHallucination: false,
      indicators: []
    };

    // 1. 源文档对比检测
    const sourceCheck = this.checkAgainstSources(text, sources);
    result.indicators.push(...sourceCheck.indicators);
    
    // 2. 信号词检测
    const signalCheck = this.checkHallucinationSignals(text);
    result.indicators.push(...signalCheck.indicators);
    
    // 3. 事实一致性检测（简化）
    const factCheck = this.checkFactConsistency(text);
    result.indicators.push(...factCheck.indicators);
    
    // 4. 数值一致性检测
    const numberCheck = this.checkNumberConsistency(text, sources);
    result.indicators.push(...numberCheck.indicators);

    // 计算总体幻觉分数
    result.hallucinationScore = this.calculateHallucinationScore(result.indicators);
    result.isHallucination = result.hallucinationScore > this.threshold;
    result.confidence = this.calculateConfidence(result.indicators);

    this.emit('detection-completed', { result });
    return result;
  }

  /**
   * 对比源文档检测
   */
  checkAgainstSources(text, sources) {
    const indicators = [];
    const sourceText = sources.join(' ').toLowerCase();
    
    // 提取文本中的关键陈述（简化：按句子分割）
    const statements = text.split(/[.!?。！？]+/).filter(s => s.trim().length > 10);
    
    let unsupportedStatements = 0;
    
    for (const statement of statements) {
      const words = statement.toLowerCase().split(/\s+/).filter(w => w.length > 3);
      const keyWords = words.slice(0, 5); // 取前5个关键词
      
      // 检查关键词是否在源文档中
      const foundInSource = keyWords.some(w => sourceText.includes(w));
      
      if (!foundInSource && keyWords.length > 0) {
        unsupportedStatements++;
        indicators.push({
          type: 'unsupported_claim',
          severity: 'medium',
          text: statement.slice(0, 50),
          description: 'Statement not found in sources'
        });
      }
    }

    const unsupportedRatio = statements.length > 0 
      ? unsupportedStatements / statements.length 
      : 0;

    if (unsupportedRatio > 0.5) {
      indicators.push({
        type: 'high_unsupported_ratio',
        severity: 'high',
        description: `${(unsupportedRatio * 100).toFixed(1)}% statements unsupported`
      });
    }

    return { indicators };
  }

  /**
   * 检测幻觉信号词
   */
  checkHallucinationSignals(text) {
    const indicators = [];
    const textLower = text.toLowerCase();
    
    for (const signal of this.hallucinationSignals) {
      if (textLower.includes(signal.toLowerCase())) {
        indicators.push({
          type: 'uncertainty_signal',
          severity: 'low',
          signal: signal,
          description: `Uncertainty phrase detected: "${signal}"`
        });
      }
    }

    return { indicators };
  }

  /**
   * 检查事实一致性
   */
  checkFactConsistency(text) {
    const indicators = [];
    
    // 检测矛盾的时间表述
    const timePatterns = [
      /(\d{4})年.*(\d{4})年/,  // 两个年份
      /(昨天|今天|明天).*(昨天|今天|明天)/  // 矛盾的时间词
    ];
    
    for (const pattern of timePatterns) {
      if (pattern.test(text)) {
        indicators.push({
          type: 'temporal_inconsistency',
          severity: 'medium',
          description: 'Potential temporal contradiction detected'
        });
      }
    }

    // 检测过度具体的数字（可能是编造的）
    const specificNumbers = text.match(/\b\d{5,}\b/g);
    if (specificNumbers && specificNumbers.length > 2) {
      indicators.push({
        type: 'overly_specific_numbers',
        severity: 'low',
        description: `Many specific numbers: ${specificNumbers.length} found`
      });
    }

    return { indicators };
  }

  /**
   * 检查数值一致性
   */
  checkNumberConsistency(text, sources) {
    const indicators = [];
    
    // 提取文本中的数字
    const textNumbers = text.match(/\b\d+(?:\.\d+)?\b/g) || [];
    const sourceNumbers = sources.join(' ').match(/\b\d+(?:\.\d+)?\b/g) || [];
    
    const sourceNumberSet = new Set(sourceNumbers);
    
    let inconsistentNumbers = 0;
    for (const num of textNumbers) {
      if (!sourceNumberSet.has(num)) {
        inconsistentNumbers++;
      }
    }

    const inconsistencyRatio = textNumbers.length > 0 
      ? inconsistentNumbers / textNumbers.length 
      : 0;

    if (inconsistencyRatio > 0.7 && textNumbers.length > 3) {
      indicators.push({
        type: 'number_inconsistency',
        severity: 'high',
        description: `${(inconsistencyRatio * 100).toFixed(1)}% numbers not in sources`
      });
    }

    return { indicators };
  }

  /**
   * 计算幻觉分数
   */
  calculateHallucinationScore(indicators) {
    if (indicators.length === 0) return 0;
    
    const severityWeights = {
      low: 0.1,
      medium: 0.3,
      high: 0.6
    };
    
    let totalWeight = 0;
    for (const indicator of indicators) {
      totalWeight += severityWeights[indicator.severity] || 0.1;
    }
    
    // 归一化到 0-1
    return Math.min(totalWeight, 1);
  }

  /**
   * 计算置信度
   */
  calculateConfidence(indicators) {
    const highSeverityCount = indicators.filter(i => i.severity === 'high').length;
    const mediumSeverityCount = indicators.filter(i => i.severity === 'medium').length;
    
    if (highSeverityCount > 0) return 'low';
    if (mediumSeverityCount > 1) return 'medium';
    return 'high';
  }

  /**
   * 批量检测
   */
  async batchDetect(testCases) {
    const results = [];
    let hallucinationCount = 0;
    
    for (const testCase of testCases) {
      try {
        const result = await this.detect(testCase);
        results.push(result);
        if (result.isHallucination) hallucinationCount++;
      } catch (error) {
        results.push({ error: error.message });
      }
    }

    return {
      total: results.length,
      hallucinations: hallucinationCount,
      hallucinationRate: results.length > 0 ? hallucinationCount / results.length : 0,
      avgScore: results.length > 0 
        ? results.reduce((a, r) => a + (r.hallucinationScore || 0), 0) / results.length 
        : 0,
      results
    };
  }
}

export default HallucinationDetector;
