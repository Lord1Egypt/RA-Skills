/**
 * Patterns Memory Handler - 模式型记忆处理器
 */

import { logger } from '../logger.js';

export const patterns = {
  name: 'patterns',
  description: '处理行为模式、习惯、规律',
  
  /**
   * 从文本中提取模式
   */
  async extract(text, context = {}) {
    logger.debug(`[PatternsHandler] 提取模式: ${text.substring(0, 100)}...`);
    
    // 提取频率模式
    const frequencyPatterns = this.extractFrequencyPatterns(text);
    
    // 提取时间模式
    const timePatterns = this.extractTimePatterns(text);
    
    // 提取行为模式
    const behaviorPatterns = this.extractBehaviorPatterns(text);
    
    // 提取条件模式
    const conditionPatterns = this.extractConditionPatterns(text);
    
    // 提取序列模式
    const sequencePatterns = this.extractSequencePatterns(text);
    
    // 使用LLM进行深度提取
    let llmExtracted = {};
    if (context.useLLM !== false) {
      try {
        llmExtracted = await this.extractWithLLM(text, context);
      } catch (error) {
        logger.warn(`[PatternsHandler] LLM提取失败: ${error.message}`);
      }
    }
    
    return {
      frequencyPatterns,
      timePatterns,
      behaviorPatterns,
      conditionPatterns,
      sequencePatterns,
      llmExtracted,
      confidence: this.calculateConfidence(text, frequencyPatterns, behaviorPatterns),
      metadata: {
        extractionMethod: llmExtracted ? 'hybrid' : 'rule',
        timestamp: Date.now(),
        textLength: text.length
      }
    };
  },
  
  /**
   * 提取频率模式
   */
  extractFrequencyPatterns(text) {
    const patterns = [];
    
    // 频率副词
    const frequencyWords = [
      { word: '总是', frequency: 'always', value: 1.0 },
      { word: '经常', frequency: 'often', value: 0.8 },
      { word: '通常', frequency: 'usually', value: 0.7 },
      { word: '有时', frequency: 'sometimes', value: 0.5 },
      { word: '偶尔', frequency: 'occasionally', value: 0.3 },
      { word: '很少', frequency: 'rarely', value: 0.2 },
      { word: '从不', frequency: 'never', value: 0.0 },
      { word: '每天', frequency: 'daily', value: 1.0 },
      { word: '每周', frequency: 'weekly', value: 0.14 },
      { word: '每月', frequency: 'monthly', value: 0.03 },
      { word: '每年', frequency: 'yearly', value: 0.003 }
    ];
    
    for (const freq of frequencyWords) {
      if (text.includes(freq.word)) {
        patterns.push({
          type: 'frequency',
          word: freq.word,
          frequency: freq.frequency,
          value: freq.value,
          confidence: 0.8
        });
      }
    }
    
    // 数字频率模式
    const numericPatterns = [
      { regex: /(\d+)次\/(天|周|月|年)/, type: 'numeric_frequency' },
      { regex: /每(\d+)(天|周|月|年)/, type: 'interval_frequency' },
      { regex: /(\d+)\s*%\s*的时间/, type: 'percentage_frequency' }
    ];
    
    for (const pattern of numericPatterns) {
      const matches = text.match(pattern.regex);
      if (matches) {
        patterns.push({
          type: pattern.type,
          match: matches[0],
          value: parseFloat(matches[1]),
          unit: matches[2] || 'time',
          confidence: 0.9
        });
      }
    }
    
    return patterns;
  },
  
  /**
   * 提取时间模式
   */
  extractTimePatterns(text) {
    const patterns = [];
    
    // 时间点模式
    const timePointPatterns = [
      { regex: /(早上|早晨|上午|中午|下午|晚上|深夜|凌晨)/, type: 'time_of_day' },
      { regex: /(周一|周二|周三|周四|周五|周六|周日)/, type: 'day_of_week' },
      { regex: /(月初|月中|月底)/, type: 'time_of_month' },
      { regex: /(春天|夏天|秋天|冬天)/, type: 'season' }
    ];
    
    for (const pattern of timePointPatterns) {
      const matches = text.match(pattern.regex);
      if (matches) {
        patterns.push({
          type: pattern.type,
          value: matches[1],
          confidence: 0.8
        });
      }
    }
    
    // 持续时间模式
    const durationPatterns = [
      { regex: /(\d+)(分钟|小时|天|周|月|年)/, type: 'duration' },
      { regex: /持续(\d+)(分钟|小时|天)/, type: 'continuous_duration' }
    ];
    
    for (const pattern of durationPatterns) {
      const matches = text.match(pattern.regex);
      if (matches) {
        patterns.push({
          type: pattern.type,
          value: parseFloat(matches[1]),
          unit: matches[2],
          confidence: 0.9
        });
      }
    }
    
    return patterns;
  },
  
  /**
   * 提取行为模式
   */
  extractBehaviorPatterns(text) {
    const patterns = [];
    
    // 行为动词
    const behaviorVerbs = [
      '做', '完成', '开始', '结束', '检查', '查看', '阅读', '写作',
      '学习', '工作', '休息', '运动', '吃饭', '睡觉', '开会', '讨论'
    ];
    
    // 行为模式关键词
    const behaviorKeywords = [
      '习惯', '惯例', '流程', '步骤', '方法', '方式', '做法',
      '规律', '模式', '套路', '顺序', '流程'
    ];
    
    // 检查是否包含行为描述
    for (const verb of behaviorVerbs) {
      if (text.includes(verb)) {
        // 查找相关的副词或频率词
        const context = this.extractContext(text, verb);
        patterns.push({
          type: 'behavior',
          verb: verb,
          context: context,
          confidence: 0.7
        });
      }
    }
    
    // 检查是否包含模式描述
    for (const keyword of behaviorKeywords) {
      if (text.includes(keyword)) {
        patterns.push({
          type: 'pattern_description',
          keyword: keyword,
          confidence: 0.8
        });
      }
    }
    
    return patterns;
  },
  
  /**
   * 提取条件模式
   */
  extractConditionPatterns(text) {
    const patterns = [];
    
    // 条件关键词
    const conditionKeywords = [
      { word: '如果', type: 'if' },
      { word: '当', type: 'when' },
      { word: '只要', type: 'as_long_as' },
      { word: '除非', type: 'unless' },
      { word: '假如', type: 'if' },
      { word: '假设', type: 'suppose' }
    ];
    
    // 结果关键词
    const resultKeywords = [
      { word: '那么', type: 'then' },
      { word: '就', type: 'then' },
      { word: '则', type: 'then' },
      { word: '所以', type: 'so' },
      { word: '因此', type: 'therefore' }
    ];
    
    // 查找条件-结果对
    for (const condition of conditionKeywords) {
      if (text.includes(condition.word)) {
        for (const result of resultKeywords) {
          if (text.includes(result.word)) {
            // 提取条件部分和结果部分
            const conditionIndex = text.indexOf(condition.word);
            const resultIndex = text.indexOf(result.word);
            
            if (resultIndex > conditionIndex) {
              const conditionText = text.substring(conditionIndex, resultIndex);
              const resultText = text.substring(resultIndex);
              
              patterns.push({
                type: 'condition_result',
                condition: {
                  type: condition.type,
                  word: condition.word,
                  text: conditionText
                },
                result: {
                  type: result.type,
                  word: result.word,
                  text: resultText
                },
                confidence: 0.8
              });
            }
          }
        }
      }
    }
    
    return patterns;
  },
  
  /**
   * 提取序列模式
   */
  extractSequencePatterns(text) {
    const patterns = [];
    
    // 序列关键词
    const sequenceKeywords = [
      { word: '首先', order: 1 },
      { word: '然后', order: 2 },
      { word: '接着', order: 3 },
      { word: '最后', order: 99 },
      { word: '第一步', order: 1 },
      { word: '第二步', order: 2 },
      { word: '第三步', order: 3 },
      { word: '最后一步', order: 99 }
    ];
    
    // 数字序列
    const numberSequence = text.match(/(\d+)[\.、](\s*[^，。]+)/g);
    if (numberSequence) {
      const steps = [];
      for (const match of numberSequence) {
        const stepMatch = match.match(/(\d+)[\.、]\s*(.+)/);
        if (stepMatch) {
          steps.push({
            order: parseInt(stepMatch[1]),
            text: stepMatch[2].trim()
          });
        }
      }
      
      if (steps.length > 1) {
        patterns.push({
          type: 'numbered_sequence',
          steps: steps.sort((a, b) => a.order - b.order),
          stepCount: steps.length,
          confidence: 0.9
        });
      }
    }
    
    // 关键词序列
    const foundKeywords = [];
    for (const keyword of sequenceKeywords) {
      if (text.includes(keyword.word)) {
        foundKeywords.push({
          word: keyword.word,
          order: keyword.order
        });
      }
    }
    
    if (foundKeywords.length > 1) {
      patterns.push({
        type: 'keyword_sequence',
        keywords: foundKeywords.sort((a, b) => a.order - b.order),
        confidence: 0.7
      });
    }
    
    return patterns;
  },
  
  /**
   * 提取上下文
   */
  extractContext(text, targetWord, windowSize = 20) {
    const index = text.indexOf(targetWord);
    if (index === -1) return '';
    
    const start = Math.max(0, index - windowSize);
    const end = Math.min(text.length, index + targetWord.length + windowSize);
    
    return text.substring(start, end);
  },
  
  /**
   * 使用LLM进行深度提取
   */
  async extractWithLLM(text, context) {
    // 这里可以集成实际的LLM调用
    // 暂时返回模拟数据
    return {
      patternType: this.detectPatternType(text),
      complexity: this.estimateComplexity(text),
      reliability: this.estimateReliability(text),
      applications: ['behavior_analysis', 'prediction'],
      notes: '需要更多数据验证'
    };
  },
  
  /**
   * 检测模式类型
   */
  detectPatternType(text) {
    if (text.includes('习惯') || text.includes('总是') || text.includes('经常')) {
      return 'habit';
    } else if (text.includes('流程') || text.includes('步骤') || text.includes('顺序')) {
      return 'process';
    } else if (text.includes('如果') || text.includes('当') || text.includes('条件')) {
      return 'conditional';
    } else if (text.includes('周期') || text.includes('每周') || text.includes('每月')) {
      return 'periodic';
    } else {
      return 'general';
    }
  },
  
  /**
   * 估计复杂度
   */
  estimateComplexity(text) {
    const complexityIndicators = [
      { pattern: /如果.*那么/, weight: 2 },
      { pattern: /首先.*然后.*最后/, weight: 3 },
      { pattern: /\d+个步骤/, weight: 2 },
      { pattern: /多种情况/, weight: 2 },
      { pattern: /复杂/, weight: 3 }
    ];
    
    let score = 1;
    for (const indicator of complexityIndicators) {
      if (indicator.pattern.test(text)) {
        score += indicator.weight;
      }
    }
    
    if (score >= 5) return 'high';
    if (score >= 3) return 'medium';
    return 'low';
  },
  
  /**
   * 估计可靠性
   */
  estimateReliability(text) {
    const reliabilityIndicators = [
      { pattern: /总是|从不/, weight: 0.9 },
      { pattern: /经常|通常/, weight: 0.7 },
      { pattern: /有时|偶尔/, weight: 0.5 },
      { pattern: /可能|也许/, weight: 0.3 },
      { pattern: /大概|估计/, weight: 0.2 }
    ];
    
    let maxReliability = 0.5; // 默认
    for (const indicator of reliabilityIndicators) {
      if (indicator.pattern.test(text)) {
        maxReliability = Math.max(maxReliability, indicator.weight);
      }
    }
    
    return maxReliability;
  },
  
  /**
   * 计算提取置信度
   */
  calculateConfidence(text, frequencyPatterns, behaviorPatterns) {
    let confidence = 0.4; // 基础置信度
    
    // 基于频率模式
    if (frequencyPatterns.length > 0) {
      confidence += Math.min(frequencyPatterns.length * 0.15, 0.3);
    }
    
    // 基于行为模式
    if (behaviorPatterns.length > 0) {
      confidence += Math.min(behaviorPatterns.length * 0.1, 0.2);
    }
    
    // 基于模式关键词
    const patternKeywords = /习惯|模式|规律|流程|步骤|顺序/;
    if (patternKeywords.test(text)) {
      confidence += 0.2;
    }
    
    // 基于具体性
    const specificity = /总是|经常|每天|每周|如果|那么/;
    if (specificity.test(text)) {
      confidence += 0.15;
    }
    
    return Math.min(Math.max(confidence, 0.1), 1.0);
  },
  
  /**
   * 验证模式
   */
  async validate(pattern, context = {}) {
    const validation = {
      isValid: true,
      confidence: 0.6,
      issues: [],
      suggestions: []
    };
    
    // 检查模式是否完整
    if (!pattern.text || pattern.text.length < 10) {
      validation.isValid = false;
      validation.issues.push('模式描述不完整');
      validation.confidence *= 0.6;
    }
    
    // 检查是否有频率或时间信息
    const hasFrequency = pattern.extracted?.frequencyPatterns?.length > 0;
    const hasTime = pattern.extracted?.timePatterns?.length > 0;
    
    if (!hasFrequency && !hasTime) {
      validation.issues.push('模式缺乏频率或时间信息');
      validation.confidence *= 0.8;
    }
    
    // 检查是否有行为描述
    const hasBehavior = pattern.extracted?.behaviorPatterns?.length > 0;
    if (!hasBehavior) {
      validation.suggestions.push('建议添加具体行为描述');
    }
    
    // 检查是否有观察次数
    if (!pattern.metadata?.observationCount) {
      validation.suggestions.push('建议记录观察次数');
    }
    
    return validation;
  },
  
  /**
   * 合并相似模式
   */
  async mergeSimilar(pattern1, pattern2, context = {}) {
    const merged = {
      text: `${pattern1.text}；${pattern2.text}`,
      extracted: {
        ...pattern1.extracted,
        ...pattern2.extracted,
        frequencyPatterns: [...(pattern1.extracted?.frequencyPatterns || []), ...(pattern2.extracted?.frequencyPatterns || [])],
        behaviorPatterns: [...(pattern1.extracted?.behaviorPatterns || []), ...(pattern2.extracted?.behaviorPatterns || [])]
      },
      importance: Math.max(pattern1.importance || 0.5, pattern2.importance || 0.5),
      timestamp: Math.max(pattern1.timestamp || Date.now(), pattern2.timestamp || Date.now()),
      metadata: {
        ...pattern1.metadata,
        ...pattern2.metadata,
        mergedFrom: [pattern1.id, pattern2.id],
        mergedAt: Date.now(),
        observationCount: (pattern1.metadata?.observationCount || 1) + (pattern2.metadata?.observationCount || 1)
      }
    };
    
    // 合并频率信息
    if (merged.extracted.frequencyPatterns) {
      const frequencyMap = new Map();
      for (const freq of merged.extracted.frequencyPatterns) {
        const key = freq.word || freq.type;
        if (frequencyMap.has(key)) {
          // 合并相似频率
          const existing = frequencyMap.get(key);
          existing.confidence = Math.max(existing.confidence, freq.confidence);
        } else {
          frequencyMap.set(key, { ...freq });
        }
      }
      merged.extracted.frequencyPatterns = Array.from(frequencyMap.values());
    }
    
    return merged;
  },
  
  /**
   * 预测基于模式
   */
  async predict(pattern, context = {}) {
    const predictions = [];
    
    // 基于频率模式预测
    if (pattern.extracted?.frequencyPatterns) {
      for (const freq of pattern.extracted.frequencyPatterns) {
        if (freq.type === 'frequency' && freq.value > 0.7) {
          predictions.push({
            type: 'high_frequency_event',
            description: `基于高频模式"${freq.word}"，该事件很可能再次发生`,
            confidence: freq.value * 0.8,
            timeframe: 'soon'
          });
        }
      }
    }
    
    // 基于时间模式预测
    if (pattern.extracted?.timePatterns) {
      for (const time of pattern.extracted.timePatterns) {
        if (time.type === 'time_of_day' || time.type === 'day_of_week') {
          predictions.push({
            type: 'time_based_prediction',
            description: `事件可能在${time.value}发生`,
            confidence: 0.6,
            timeframe: 'next_occurrence'
          });
        }
      }
    }
    
    return predictions;
  }
};

export default patterns;