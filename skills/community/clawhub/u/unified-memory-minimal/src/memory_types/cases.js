/**
 * Cases Memory Handler - 案例型记忆处理器
 */

import { logger } from '../logger.js';

export const cases = {
  name: 'cases',
  description: '处理案例、经验、教训',
  
  /**
   * 从文本中提取案例
   */
  async extract(text, context = {}) {
    logger.debug(`[CasesHandler] 提取案例: ${text.substring(0, 100)}...`);
    
    // 提取案例结构
    const caseStructure = this.extractCaseStructure(text);
    
    // 提取关键事件
    const keyEvents = this.extractKeyEvents(text);
    
    // 提取经验教训
    const lessonsLearned = this.extractLessonsLearned(text);
    
    // 提取成功因素
    const successFactors = this.extractSuccessFactors(text);
    
    // 提取失败原因
    const failureReasons = this.extractFailureReasons(text);
    
    // 提取可复用点
    const reusablePoints = this.extractReusablePoints(text);
    
    return {
      caseStructure,
      keyEvents,
      lessonsLearned,
      successFactors,
      failureReasons,
      reusablePoints,
      confidence: this.calculateConfidence(text, caseStructure, lessonsLearned),
      metadata: {
        extractionMethod: 'hybrid',
        timestamp: Date.now(),
        textLength: text.length
      }
    };
  },
  
  /**
   * 提取案例结构
   */
  extractCaseStructure(text) {
    const structure = {
      hasBackground: false,
      hasProblem: false,
      hasSolution: false,
      hasResult: false,
      sections: []
    };
    
    // 检查案例结构关键词
    const structureKeywords = {
      background: ['背景', '情况', '环境', '起初', '原来', 'background'],
      problem: ['问题', '挑战', '困难', '遇到', '面临', 'problem', 'challenge'],
      solution: ['解决', '方案', '方法', '措施', '做法', 'solution', 'approach'],
      result: ['结果', '效果', '成果', '成效', 'outcome', 'result']
    };
    
    for (const [section, keywords] of Object.entries(structureKeywords)) {
      for (const keyword of keywords) {
        if (text.includes(keyword)) {
          structure[`has${section.charAt(0).toUpperCase() + section.slice(1)}`] = true;
          structure.sections.push({
            type: section,
            keyword: keyword,
            confidence: 0.7
          });
          break;
        }
      }
    }
    
    // 计算结构完整性
    const completeness = Object.values(structure).filter(v => v === true).length / 4;
    structure.completeness = completeness;
    
    return structure;
  },
  
  /**
   * 提取关键事件
   */
  extractKeyEvents(text) {
    const events = [];
    
    // 事件关键词
    const eventKeywords = [
      '发生', '出现', '遇到', '发现', '意识到', '决定',
      'occurred', 'happened', 'encountered', 'discovered', 'decided'
    ];
    
    // 时间标记
    const timeMarkers = [
      '首先', '然后', '接着', '之后', '最后', '最终',
      'first', 'then', 'next', 'after', 'finally'
    ];
    
    // 分句
    const sentences = text.split(/[。！？；\.\?!;]/).filter(s => s.trim());
    
    for (const sentence of sentences) {
      // 检查事件关键词
      for (const keyword of eventKeywords) {
        if (sentence.includes(keyword)) {
          events.push({
            text: sentence.trim(),
            keyword: keyword,
            type: 'event',
            confidence: 0.7
          });
          break;
        }
      }
      
      // 检查时间标记
      for (const marker of timeMarkers) {
        if (sentence.includes(marker)) {
          events.push({
            text: sentence.trim(),
            marker: marker,
            type: 'sequence',
            confidence: 0.6
          });
          break;
        }
      }
    }
    
    return events;
  },
  
  /**
   * 提取经验教训
   */
  extractLessonsLearned(text) {
    const lessons = [];
    
    // 教训关键词
    const lessonKeywords = [
      '教训', '经验', '学到', '明白', '认识到', '意识到',
      'lesson', 'experience', 'learned', 'realized', 'understood'
    ];
    
    // 教训模式
    const lessonPatterns = [
      /(.+)教训[是为：:]\s*(.+)/,
      /从(.+)中学到[了的是]\s*(.+)/,
      /(.+)让[我我们]明白[了的是]\s*(.+)/,
      /经验[是为：:]\s*(.+)/
    ];
    
    // 检查关键词
    for (const keyword of lessonKeywords) {
      if (text.includes(keyword)) {
        const context = this.extractContext(text, keyword, 30);
        lessons.push({
          keyword: keyword,
          context: context,
          type: 'lesson',
          confidence: 0.8
        });
      }
    }
    
    // 检查模式
    for (const pattern of lessonPatterns) {
      const match = text.match(pattern);
      if (match) {
        lessons.push({
          pattern: pattern.source,
          fullMatch: match[0],
          content: match[2] || match[1],
          type: 'structured_lesson',
          confidence: 0.9
        });
      }
    }
    
    return lessons;
  },
  
  /**
   * 提取成功因素
   */
  extractSuccessFactors(text) {
    const factors = [];
    
    // 成功关键词
    const successKeywords = [
      '成功', '有效', '关键', '重要', '得益于', '归功于',
      'success', 'effective', 'key', 'important', 'thanks to'
    ];
    
    for (const keyword of successKeywords) {
      if (text.includes(keyword)) {
        const context = this.extractContext(text, keyword, 25);
        factors.push({
          keyword: keyword,
          context: context,
          type: 'success_factor',
          confidence: 0.7
        });
      }
    }
    
    return factors;
  },
  
  /**
   * 提取失败原因
   */
  extractFailureReasons(text) {
    const reasons = [];
    
    // 失败关键词
    const failureKeywords = [
      '失败', '错误', '问题', '缺陷', '不足', '原因',
      'failed', 'error', 'mistake', 'problem', 'issue', 'reason'
    ];
    
    for (const keyword of failureKeywords) {
      if (text.includes(keyword)) {
        const context = this.extractContext(text, keyword, 25);
        reasons.push({
          keyword: keyword,
          context: context,
          type: 'failure_reason',
          confidence: 0.7
        });
      }
    }
    
    return reasons;
  },
  
  /**
   * 提取可复用点
   */
  extractReusablePoints(text) {
    const points = [];
    
    // 可复用关键词
    const reusableKeywords = [
      '可以', '建议', '推荐', '值得', '参考', '借鉴',
      'can', 'suggest', 'recommend', 'worth', 'reference'
    ];
    
    for (const keyword of reusableKeywords) {
      if (text.includes(keyword)) {
        const context = this.extractContext(text, keyword, 25);
        points.push({
          keyword: keyword,
          context: context,
          type: 'reusable',
          confidence: 0.6
        });
      }
    }
    
    return points;
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
   * 计算置信度
   */
  calculateConfidence(text, caseStructure, lessonsLearned) {
    let confidence = 0.3;
    
    // 基于结构完整性
    confidence += caseStructure.completeness * 0.3;
    
    // 基于经验教训
    if (lessonsLearned.length > 0) {
      confidence += Math.min(lessonsLearned.length * 0.15, 0.3);
    }
    
    // 基于案例关键词
    const casePattern = /案例|经验|教训|故事|经历/;
    if (casePattern.test(text)) {
      confidence += 0.2;
    }
    
    return Math.min(Math.max(confidence, 0.1), 1.0);
  },
  
  /**
   * 验证案例
   */
  async validate(caseMemory, context = {}) {
    const validation = {
      isValid: true,
      confidence: 0.5,
      issues: [],
      suggestions: []
    };
    
    if (!caseMemory.text || caseMemory.text.length < 50) {
      validation.isValid = false;
      validation.issues.push('案例描述太短');
      validation.confidence *= 0.5;
    }
    
    const structure = caseMemory.extracted?.caseStructure;
    if (structure && structure.completeness < 0.5) {
      validation.issues.push('案例结构不完整');
      validation.suggestions.push('建议包含背景、问题、解决方案和结果');
      validation.confidence *= 0.8;
    }
    
    const hasLessons = caseMemory.extracted?.lessonsLearned?.length > 0;
    if (!hasLessons) {
      validation.suggestions.push('建议添加经验教训总结');
    }
    
    return validation;
  },
  
  /**
   * 合并相似案例
   */
  async mergeSimilar(case1, case2, context = {}) {
    const merged = {
      text: `${case1.text}\n\n---\n\n${case2.text}`,
      extracted: {
        ...case1.extracted,
        ...case2.extracted,
        keyEvents: [...(case1.extracted?.keyEvents || []), ...(case2.extracted?.keyEvents || [])],
        lessonsLearned: [...(case1.extracted?.lessonsLearned || []), ...(case2.extracted?.lessonsLearned || [])]
      },
      importance: Math.max(case1.importance || 0.5, case2.importance || 0.5),
      timestamp: Math.max(case1.timestamp || Date.now(), case2.timestamp || Date.now()),
      metadata: {
        ...case1.metadata,
        ...case2.metadata,
        mergedFrom: [case1.id, case2.id],
        mergedAt: Date.now()
      }
    };
    
    return merged;
  }
};

export default cases;