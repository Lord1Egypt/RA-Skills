/**
 * Skills Memory Handler - 技能型记忆处理器
 */

import { logger } from '../logger.js';

export const skills = {
  name: 'skills',
  description: '处理技能、能力、专长',
  
  /**
   * 从文本中提取技能
   */
  async extract(text, context = {}) {
    logger.debug(`[SkillsHandler] 提取技能: ${text.substring(0, 100)}...`);
    
    // 提取技能关键词
    const skillKeywords = this.extractSkillKeywords(text);
    
    // 提取能力等级
    const proficiencyLevels = this.extractProficiencyLevels(text);
    
    // 提取学习路径
    const learningPaths = this.extractLearningPaths(text);
    
    // 提取应用场景
    const applicationScenarios = this.extractApplicationScenarios(text);
    
    // 提取相关工具
    const relatedTools = this.extractRelatedTools(text);
    
    return {
      skillKeywords,
      proficiencyLevels,
      learningPaths,
      applicationScenarios,
      relatedTools,
      confidence: this.calculateConfidence(text, skillKeywords, proficiencyLevels),
      metadata: {
        extractionMethod: 'hybrid',
        timestamp: Date.now(),
        textLength: text.length
      }
    };
  },
  
  /**
   * 提取技能关键词
   */
  extractSkillKeywords(text) {
    const keywords = [];
    
    // 技能动词
    const skillVerbs = [
      '会', '能', '擅长', '精通', '熟练', '掌握', '了解', '熟悉',
      'can', 'able to', 'good at', 'expert in', 'skilled in'
    ];
    
    // 技能名词
    const skillNouns = [
      '编程', '设计', '写作', '分析', '管理', '沟通', '协调',
      'programming', 'design', 'writing', 'analysis', 'management'
    ];
    
    // 技术栈
    const techStacks = [
      'JavaScript', 'Python', 'Java', 'Go', 'Rust', 'TypeScript',
      'React', 'Vue', 'Angular', 'Node.js', 'Django', 'Spring',
      'Docker', 'Kubernetes', 'AWS', 'GCP', 'Azure',
      'MySQL', 'PostgreSQL', 'MongoDB', 'Redis'
    ];
    
    // 检查技能动词
    for (const verb of skillVerbs) {
      if (text.includes(verb)) {
        const context = this.extractContext(text, verb, 15);
        keywords.push({
          type: 'skill_verb',
          value: verb,
          context: context,
          confidence: 0.7
        });
      }
    }
    
    // 检查技能名词
    for (const noun of skillNouns) {
      if (text.includes(noun)) {
        keywords.push({
          type: 'skill_noun',
          value: noun,
          confidence: 0.8
        });
      }
    }
    
    // 检查技术栈
    for (const tech of techStacks) {
      if (text.toLowerCase().includes(tech.toLowerCase())) {
        keywords.push({
          type: 'tech_stack',
          value: tech,
          confidence: 0.9
        });
      }
    }
    
    return keywords;
  },
  
  /**
   * 提取能力等级
   */
  extractProficiencyLevels(text) {
    const levels = [];
    
    // 等级关键词
    const levelKeywords = [
      { words: ['精通', '专家', '大师', 'expert', 'master'], level: 'expert', value: 5 },
      { words: ['熟练', '高级', 'advanced', 'senior'], level: 'advanced', value: 4 },
      { words: ['熟悉', '中级', 'intermediate', 'mid'], level: 'intermediate', value: 3 },
      { words: ['了解', '初级', 'beginner', 'junior'], level: 'beginner', value: 2 },
      { words: ['听说过', '知道', 'heard of', 'aware'], level: 'aware', value: 1 }
    ];
    
    for (const levelDef of levelKeywords) {
      for (const word of levelDef.words) {
        if (text.includes(word)) {
          levels.push({
            word: word,
            level: levelDef.level,
            value: levelDef.value,
            confidence: 0.8
          });
        }
      }
    }
    
    // 数字等级
    const numberLevelMatch = text.match(/(\d+)[级星]/);
    if (numberLevelMatch) {
      const numValue = parseInt(numberLevelMatch[1]);
      if (numValue >= 1 && numValue <= 5) {
        levels.push({
          type: 'numeric_level',
          value: numValue,
          confidence: 0.9
        });
      }
    }
    
    return levels;
  },
  
  /**
   * 提取学习路径
   */
  extractLearningPaths(text) {
    const paths = [];
    
    // 学习关键词
    const learningKeywords = [
      '学习', '学会', '掌握', '入门', '进阶', '精通',
      'learn', 'study', 'master', 'beginner', 'advanced'
    ];
    
    // 资源关键词
    const resourceKeywords = [
      '课程', '教程', '文档', '书籍', '视频',
      'course', 'tutorial', 'documentation', 'book', 'video'
    ];
    
    // 检查学习描述
    for (const keyword of learningKeywords) {
      if (text.includes(keyword)) {
        const context = this.extractContext(text, keyword, 20);
        paths.push({
          type: 'learning_action',
          keyword: keyword,
          context: context,
          confidence: 0.7
        });
      }
    }
    
    // 检查资源提及
    for (const resource of resourceKeywords) {
      if (text.includes(resource)) {
        paths.push({
          type: 'learning_resource',
          resource: resource,
          confidence: 0.6
        });
      }
    }
    
    return paths;
  },
  
  /**
   * 提取应用场景
   */
  extractApplicationScenarios(text) {
    const scenarios = [];
    
    // 场景关键词
    const scenarioKeywords = [
      '用于', '应用', '场景', '项目', '案例',
      'used for', 'applied in', 'scenario', 'project', 'case'
    ];
    
    for (const keyword of scenarioKeywords) {
      if (text.includes(keyword)) {
        const context = this.extractContext(text, keyword, 20);
        scenarios.push({
          keyword: keyword,
          context: context,
          confidence: 0.7
        });
      }
    }
    
    return scenarios;
  },
  
  /**
   * 提取相关工具
   */
  extractRelatedTools(text) {
    const tools = [];
    
    // 常见工具列表
    const commonTools = [
      // 开发工具
      'VS Code', 'IntelliJ', 'Vim', 'Emacs', 'Sublime',
      // 版本控制
      'Git', 'GitHub', 'GitLab', 'Bitbucket',
      // 项目管理
      'Jira', 'Trello', 'Asana', 'Notion',
      // 设计工具
      'Figma', 'Sketch', 'Adobe XD', 'Photoshop',
      // 数据库工具
      'DBeaver', 'Navicat', 'pgAdmin',
      // 云服务
      'AWS', 'GCP', 'Azure', 'Vercel', 'Netlify'
    ];
    
    for (const tool of commonTools) {
      if (text.toLowerCase().includes(tool.toLowerCase())) {
        tools.push({
          name: tool,
          confidence: 0.8
        });
      }
    }
    
    return tools;
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
  calculateConfidence(text, skillKeywords, proficiencyLevels) {
    let confidence = 0.4;
    
    if (skillKeywords.length > 0) {
      confidence += Math.min(skillKeywords.length * 0.15, 0.3);
    }
    
    if (proficiencyLevels.length > 0) {
      confidence += Math.min(proficiencyLevels.length * 0.1, 0.2);
    }
    
    const skillPattern = /会|能|擅长|精通|熟练/;
    if (skillPattern.test(text)) {
      confidence += 0.2;
    }
    
    return Math.min(Math.max(confidence, 0.1), 1.0);
  },
  
  /**
   * 验证技能
   */
  async validate(skill, context = {}) {
    const validation = {
      isValid: true,
      confidence: 0.6,
      issues: [],
      suggestions: []
    };
    
    if (!skill.text || skill.text.length < 5) {
      validation.isValid = false;
      validation.issues.push('技能描述不完整');
      validation.confidence *= 0.6;
    }
    
    const hasKeywords = skill.extracted?.skillKeywords?.length > 0;
    const hasLevel = skill.extracted?.proficiencyLevels?.length > 0;
    
    if (!hasKeywords) {
      validation.issues.push('未识别到具体技能');
      validation.confidence *= 0.7;
    }
    
    if (!hasLevel) {
      validation.suggestions.push('建议添加技能熟练度等级');
    }
    
    return validation;
  },
  
  /**
   * 合并相似技能
   */
  async mergeSimilar(skill1, skill2, context = {}) {
    const merged = {
      text: `${skill1.text}；${skill2.text}`,
      extracted: {
        ...skill1.extracted,
        ...skill2.extracted,
        skillKeywords: [...(skill1.extracted?.skillKeywords || []), ...(skill2.extracted?.skillKeywords || [])],
        proficiencyLevels: [...(skill1.extracted?.proficiencyLevels || []), ...(skill2.extracted?.proficiencyLevels || [])]
      },
      importance: Math.max(skill1.importance || 0.5, skill2.importance || 0.5),
      timestamp: Math.max(skill1.timestamp || Date.now(), skill2.timestamp || Date.now()),
      metadata: {
        ...skill1.metadata,
        ...skill2.metadata,
        mergedFrom: [skill1.id, skill2.id],
        mergedAt: Date.now()
      }
    };
    
    // 去重技能关键词
    if (merged.extracted.skillKeywords) {
      const seen = new Set();
      merged.extracted.skillKeywords = merged.extracted.skillKeywords.filter(keyword => {
        const key = `${keyword.type}:${keyword.value}`;
        if (seen.has(key)) return false;
        seen.add(key);
        return true;
      });
    }
    
    // 取最高熟练度
    if (merged.extracted.proficiencyLevels && merged.extracted.proficiencyLevels.length > 0) {
      const maxLevel = merged.extracted.proficiencyLevels.reduce((max, level) => {
        return (level.value || 0) > (max.value || 0) ? level : max;
      }, merged.extracted.proficiencyLevels[0]);
      
      merged.extracted.proficiencyLevels = [maxLevel];
    }
    
    return merged;
  }
};

export default skills;