/**
 * Facts Memory Handler - 事实型记忆处理器
 */

import { logger } from '../logger.js';

export const facts = {
  name: 'facts',
  description: '处理客观事实、数据、信息',
  
  /**
   * 从文本中提取事实
   */
  async extract(text, context = {}) {
    logger.debug(`[FactsHandler] 提取事实: ${text.substring(0, 100)}...`);
    
    // 提取实体
    const entities = this.extractEntities(text);
    
    // 提取关系
    const relations = this.extractRelations(text, entities);
    
    // 提取数值数据
    const numericData = this.extractNumericData(text);
    
    // 提取时间信息
    const timeInfo = this.extractTimeInfo(text);
    
    // 提取地点信息
    const locationInfo = this.extractLocationInfo(text);
    
    // 使用LLM进行深度提取（如果可用）
    let llmExtracted = {};
    if (context.useLLM !== false) {
      try {
        llmExtracted = await this.extractWithLLM(text, context);
      } catch (error) {
        logger.warn(`[FactsHandler] LLM提取失败: ${error.message}`);
      }
    }
    
    return {
      entities,
      relations,
      numericData,
      timeInfo,
      locationInfo,
      llmExtracted,
      confidence: this.calculateConfidence(text, entities, numericData),
      metadata: {
        extractionMethod: llmExtracted ? 'hybrid' : 'rule',
        timestamp: Date.now(),
        textLength: text.length
      }
    };
  },
  
  /**
   * 提取实体
   */
  extractEntities(text) {
    const entities = [];
    
    // 人名模式
    const namePatterns = [
      /([\u4e00-\u9fa5]{2,4})先生|女士|老师|教授|博士/g,
      /([A-Z][a-z]+ [A-Z][a-z]+)/g // 英文全名
    ];
    
    // 组织名模式
    const orgPatterns = [
      /([\u4e00-\u9fa5]{2,10})(公司|集团|企业|组织|机构|部门)/g,
      /([A-Z][a-z]+ (Inc|Ltd|Corp|LLC))/g
    ];
    
    // 产品名模式
    const productPatterns = [
      /([\u4e00-\u9fa5]{2,10})(软件|系统|平台|应用|工具)/g,
      /([A-Z][a-z]+ (Pro|Plus|Max|Lite))/g
    ];
    
    // 检查所有模式
    const patterns = [
      { type: 'person', regex: namePatterns },
      { type: 'organization', regex: orgPatterns },
      { type: 'product', regex: productPatterns }
    ];
    
    for (const pattern of patterns) {
      for (const regex of pattern.regex) {
        const matches = text.match(regex) || [];
        for (const match of matches) {
          // 清理匹配结果
          const cleaned = match.replace(/(先生|女士|老师|教授|博士|公司|集团|企业|组织|机构|部门|软件|系统|平台|应用|工具| Inc| Ltd| Corp| LLC| Pro| Plus| Max| Lite)/g, '').trim();
          if (cleaned) {
            entities.push({
              type: pattern.type,
              value: cleaned,
              original: match,
              position: text.indexOf(match)
            });
          }
        }
      }
    }
    
    // 去重
    const uniqueEntities = [];
    const seen = new Set();
    
    for (const entity of entities) {
      const key = `${entity.type}:${entity.value}`;
      if (!seen.has(key)) {
        seen.add(key);
        uniqueEntities.push(entity);
      }
    }
    
    return uniqueEntities;
  },
  
  /**
   * 提取关系
   */
  extractRelations(text, entities) {
    const relations = [];
    
    if (entities.length < 2) {
      return relations;
    }
    
    // 关系模式
    const relationPatterns = [
      { pattern: /是|为|属于|隶属于/, type: 'is_a' },
      { pattern: /有|包含|包括/, type: 'has' },
      { pattern: /在|位于/, type: 'located_at' },
      { pattern: /与|和|跟/, type: 'and' },
      { pattern: /或|或者/, type: 'or' },
      { pattern: /因为|由于/, type: 'because' },
      { pattern: /所以|因此/, type: 'so' }
    ];
    
    // 简单的句子分割
    const sentences = text.split(/[。！？；\.\?!;]/).filter(s => s.trim());
    
    for (const sentence of sentences) {
      for (const entity1 of entities) {
        for (const entity2 of entities) {
          if (entity1.value === entity2.value) continue;
          
          // 检查两个实体是否出现在同一个句子中
          if (sentence.includes(entity1.value) && sentence.includes(entity2.value)) {
            // 查找关系词
            for (const relPattern of relationPatterns) {
              if (relPattern.pattern.test(sentence)) {
                relations.push({
                  source: entity1.value,
                  target: entity2.value,
                  type: relPattern.type,
                  sentence: sentence.trim(),
                  confidence: 0.7
                });
                break;
              }
            }
          }
        }
      }
    }
    
    return relations;
  },
  
  /**
   * 提取数值数据
   */
  extractNumericData(text) {
    const numericData = [];
    
    // 百分比
    const percentMatches = text.match(/\d+(\.\d+)?%/g) || [];
    for (const match of percentMatches) {
      numericData.push({
        type: 'percentage',
        value: parseFloat(match),
        unit: '%',
        original: match
      });
    }
    
    // 货币
    const currencyMatches = text.match(/(¥|￥|＄|\$|€|£)\s*\d+(\.\d+)?/g) || [];
    for (const match of currencyMatches) {
      const value = match.replace(/[¥￥＄\$€£\s]/g, '');
      const unit = match.match(/[¥￥＄\$€£]/)?.[0] || '¥';
      numericData.push({
        type: 'currency',
        value: parseFloat(value),
        unit: unit,
        original: match
      });
    }
    
    // 数字
    const numberMatches = text.match(/\d+(\.\d+)?/g) || [];
    for (const match of numberMatches) {
      // 跳过已经是百分比或货币的数字
      if (match.includes('%') || /[¥￥＄\$€£]/.test(text.substring(text.indexOf(match) - 1, text.indexOf(match) + 1))) {
        continue;
      }
      
      numericData.push({
        type: 'number',
        value: parseFloat(match),
        unit: '',
        original: match
      });
    }
    
    // 范围
    const rangeMatches = text.match(/\d+(\.\d+)?\s*[-~至]\s*\d+(\.\d+)?/g) || [];
    for (const match of rangeMatches) {
      const [start, end] = match.split(/[-~至]/).map(s => parseFloat(s.trim()));
      numericData.push({
        type: 'range',
        value: { start, end },
        unit: '',
        original: match
      });
    }
    
    return numericData;
  },
  
  /**
   * 提取时间信息
   */
  extractTimeInfo(text) {
    const timeInfo = [];
    
    // 日期模式
    const datePatterns = [
      /\d{4}年\d{1,2}月\d{1,2}日/g,
      /\d{4}-\d{1,2}-\d{1,2}/g,
      /\d{4}\/\d{1,2}\/\d{1,2}/g,
      /(今天|明天|昨天|后天|前天)/g,
      /(周一|周二|周三|周四|周五|周六|周日)/g,
      /(星期一|星期二|星期三|星期四|星期五|星期六|星期日)/g
    ];
    
    for (const pattern of datePatterns) {
      const matches = text.match(pattern) || [];
      for (const match of matches) {
        timeInfo.push({
          type: 'date',
          value: match,
          normalized: this.normalizeDate(match)
        });
      }
    }
    
    // 时间模式
    const timePatterns = [
      /\d{1,2}[:：]\d{1,2}/g,
      /\d{1,2}[:：]\d{1,2}[:：]\d{1,2}/g,
      /(上午|下午|晚上|凌晨|早晨|中午)\s*\d{1,2}点/g
    ];
    
    for (const pattern of timePatterns) {
      const matches = text.match(pattern) || [];
      for (const match of matches) {
        timeInfo.push({
          type: 'time',
          value: match,
          normalized: this.normalizeTime(match)
        });
      }
    }
    
    return timeInfo;
  },
  
  /**
   * 提取地点信息
   */
  extractLocationInfo(text) {
    const locationInfo = [];
    
    // 地点后缀
    const locationSuffixes = ['市', '省', '区', '县', '镇', '村', '街道', '路', '巷', '号'];
    
    for (const suffix of locationSuffixes) {
      const pattern = new RegExp(`[\\u4e00-\\u9fa5]{1,10}${suffix}`, 'g');
      const matches = text.match(pattern) || [];
      for (const match of matches) {
        locationInfo.push({
          type: 'location',
          value: match,
          suffix: suffix
        });
      }
    }
    
    // 国家/城市名
    const knownLocations = ['北京', '上海', '广州', '深圳', '杭州', '成都', '重庆', '武汉', '南京', '西安'];
    for (const location of knownLocations) {
      if (text.includes(location)) {
        locationInfo.push({
          type: 'city',
          value: location,
          isKnown: true
        });
      }
    }
    
    return locationInfo;
  },
  
  /**
   * 使用LLM进行深度提取
   */
  async extractWithLLM(text, context) {
    // 这里可以集成实际的LLM调用
    // 暂时返回模拟数据
    return {
      summary: text.substring(0, 100) + '...',
      keyPoints: [
        '这是一个事实陈述',
        '包含具体信息'
      ],
      categories: ['information', 'data'],
      sentiment: 'neutral',
      complexity: 'medium'
    };
  },
  
  /**
   * 计算提取置信度
   */
  calculateConfidence(text, entities, numericData) {
    let confidence = 0.5; // 基础置信度
    
    // 基于实体数量
    if (entities.length > 0) {
      confidence += Math.min(entities.length * 0.1, 0.3);
    }
    
    // 基于数值数据
    if (numericData.length > 0) {
      confidence += Math.min(numericData.length * 0.05, 0.2);
    }
    
    // 基于文本长度
    if (text.length > 50) {
      confidence += 0.1;
    }
    
    // 基于具体性（包含数字、日期等）
    const specificityIndicators = /\d+|日期|时间|地点|金额|百分比/;
    if (specificityIndicators.test(text)) {
      confidence += 0.15;
    }
    
    return Math.min(Math.max(confidence, 0.1), 1.0);
  },
  
  /**
   * 标准化日期
   */
  normalizeDate(dateStr) {
    // 简单的日期标准化
    const dateMap = {
      '今天': new Date().toISOString().split('T')[0],
      '明天': new Date(Date.now() + 86400000).toISOString().split('T')[0],
      '昨天': new Date(Date.now() - 86400000).toISOString().split('T')[0],
      '后天': new Date(Date.now() + 172800000).toISOString().split('T')[0],
      '前天': new Date(Date.now() - 172800000).toISOString().split('T')[0]
    };
    
    if (dateMap[dateStr]) {
      return dateMap[dateStr];
    }
    
    // 尝试解析其他格式
    try {
      const date = new Date(dateStr);
      if (!isNaN(date.getTime())) {
        return date.toISOString().split('T')[0];
      }
    } catch (e) {
      // 解析失败，返回原字符串
    }
    
    return dateStr;
  },
  
  /**
   * 标准化时间
   */
  normalizeTime(timeStr) {
    // 简单的时间标准化
    const timeMap = {
      '上午': 'AM',
      '下午': 'PM',
      '晚上': 'PM',
      '凌晨': 'AM',
      '早晨': 'AM',
      '中午': '12:00'
    };
    
    let normalized = timeStr;
    
    // 替换中文时间描述
    for (const [chinese, english] of Object.entries(timeMap)) {
      normalized = normalized.replace(chinese, english);
    }
    
    // 替换中文标点
    normalized = normalized.replace(/：/g, ':');
    normalized = normalized.replace(/点/g, ':00');
    
    return normalized;
  },
  
  /**
   * 验证事实
   */
  async validate(fact, context = {}) {
    const validation = {
      isValid: true,
      confidence: 0.7,
      issues: [],
      suggestions: []
    };
    
    // 检查事实是否完整
    if (!fact.text || fact.text.length < 5) {
      validation.isValid = false;
      validation.issues.push('事实文本太短或不完整');
      validation.confidence *= 0.5;
    }
    
    // 检查是否有具体信息
    const hasSpecificInfo = /\d+|具体|明确|详细/.test(fact.text);
    if (!hasSpecificInfo) {
      validation.issues.push('事实缺乏具体信息');
      validation.confidence *= 0.8;
    }
    
    // 检查是否有来源信息
    if (!fact.metadata?.source) {
      validation.suggestions.push('建议添加事实来源');
    }
    
    // 检查时间信息
    if (!fact.extracted?.timeInfo || fact.extracted.timeInfo.length === 0) {
      validation.suggestions.push('建议添加时间信息');
    }
    
    return validation;
  },
  
  /**
   * 合并相似事实
   */
  async mergeSimilar(fact1, fact2, context = {}) {
    const merged = {
      text: `${fact1.text} ${fact2.text}`,
      extracted: {
        ...fact1.extracted,
        ...fact2.extracted,
        entities: [...(fact1.extracted?.entities || []), ...(fact2.extracted?.entities || [])],
        numericData: [...(fact1.extracted?.numericData || []), ...(fact2.extracted?.numericData || [])]
      },
      importance: Math.max(fact1.importance || 0.5, fact2.importance || 0.5),
      timestamp: Math.max(fact1.timestamp || Date.now(), fact2.timestamp || Date.now()),
      metadata: {
        ...fact1.metadata,
        ...fact2.metadata,
        mergedFrom: [fact1.id, fact2.id],
        mergedAt: Date.now()
      }
    };
    
    // 去重实体
    if (merged.extracted.entities) {
      const seen = new Set();
      merged.extracted.entities = merged.extracted.entities.filter(entity => {
        const key = `${entity.type}:${entity.value}`;
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      });
    }
    
    return merged;
  }
};

export default facts;