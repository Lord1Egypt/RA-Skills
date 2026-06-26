const fs = require('fs');
const path = require('path');

/**
 * Skill Discoverer - Core Engine
 * 技能发现器 - 核心引擎
 */

/**
 * Search skills by keyword or semantic query
 * @param {string} query - Search query
 * @param {Array} skills - Skill list
 * @returns {Array} Matching skills with similarity scores
 */
function searchSkills(query, skills) {
  if (!query || typeof query !== 'string') {
    throw new Error('Query must be a non-empty string');
  }

  // Simple keyword matching (v0.1.0)
  // TODO: Implement vector similarity search in v0.2.0
  const queryKeywords = query.toLowerCase().split(' ');
  
  const results = skills.map(skill => {
    const skillText = `${skill.name} ${skill.description} ${skill.tags.join(' ')}`.toLowerCase();
    const matchCount = queryKeywords.filter(kw => skillText.includes(kw)).length;
    const similarity = matchCount / queryKeywords.length;
    
    return {
      ...skill,
      similarity,
      matchedKeywords: queryKeywords.filter(kw => skillText.includes(kw))
    };
  })
  .filter(result => result.similarity > 0.3)
  .sort((a, b) => b.similarity - a.similarity);
  
  return results;
}

/**
 * Recommend skills based on task type
 * @param {string} taskType - Task type (technical/business/creative/learning)
 * @param {Array} skills - Skill list
 * @returns {Array} Recommended skills
 */
function recommendSkills(taskType, skills) {
  const taskSkillMap = {
    technical: ['first-principle-analyzer', 'systematic-debugging', 'skill-evolver'],
    business: ['business-model-assistant', 'ecological-niche-assistant'],
    creative: ['copywriting', 'pptx', 'docx'],
    learning: ['skill-creator', 'skill-discoverer', 'meta-cognition-assistant']
  };
  
  const targetSkills = taskSkillMap[taskType] || [];
  
  return skills
    .filter(skill => targetSkills.includes(skill.id))
    .map(skill => ({
      ...skill,
      recommendationReason: `适合${taskType}任务`
    }));
}

/**
 * Recommend skill combinations for complex tasks
 * @param {string} taskDescription - Complex task description
 * @param {Array} skills - Skill list
 * @returns {Object} Recommended skill combination
 */
function recommendCombination(taskDescription, skills) {
  // Simple rule-based combination (v0.1.0)
  // TODO: Implement ML-based optimization in v0.3.0
  
  const workflow = analyzeWorkflow(taskDescription);
  
  const combination = workflow.map(step => {
    return recommendSkills(step.type, skills)[0];
  }).filter(Boolean);
  
  const synergyEffect = calculateSynergy(combination);
  
  return {
    skills: combination,
    workflow,
    synergyEffect,
    estimatedEfficiency: 1 + (synergyEffect * 0.5)
  };
}

/**
 * Analyze task workflow
 */
function analyzeWorkflow(taskDescription) {
  const workflows = {
    '分析': { type: 'technical', phase: 'analysis' },
    '报告': { type: 'creative', phase: 'output' },
    '优化': { type: 'technical', phase: 'optimization' },
    '学习': { type: 'learning', phase: 'learning' }
  };
  
  const result = [];
  for (const [keyword, workflow] of Object.entries(workflows)) {
    if (taskDescription.includes(keyword)) {
      result.push(workflow);
    }
  }
  
  return result.length > 0 ? result : [{ type: 'technical', phase: 'general' }];
}

/**
 * Calculate synergy effect
 */
function calculateSynergy(combination) {
  // Simple synergy calculation (v0.1.0)
  // Based on skill category diversity
  const categories = new Set(combination.map(s => s.category));
  return categories.size / combination.length;
}

/**
 * Generate usage guide for a skill
 * @param {Object} skill - Skill object
 * @returns {Object} Usage guide
 */
function generateGuide(skill) {
  return {
    introduction: {
      title: '技能介绍',
      duration: '30 秒',
      content: [
        `技能定位：${skill.description}`,
        `核心价值：${skill.valueProposition || '提升效率'}`,
        `适用场景：${skill.scenarios?.join('、') || '通用场景'}`
      ]
    },
    quickStart: {
      title: '快速开始',
      duration: '2 分钟',
      content: [
        '基本用法示例',
        '第一个示例任务'
      ]
    },
    advanced: {
      title: '进阶使用',
      duration: '5 分钟',
      content: [
        '高级功能介绍',
        '最佳实践建议'
      ]
    },
    practice: {
      title: '实战练习',
      duration: '10 分钟',
      content: [
        '实际任务演练',
        '即时反馈指导'
      ]
    }
  };
}

module.exports = {
  searchSkills,
  recommendSkills,
  recommendCombination,
  analyzeWorkflow,
  calculateSynergy,
  generateGuide
};
