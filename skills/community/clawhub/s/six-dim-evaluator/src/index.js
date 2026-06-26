const fs = require('fs');
const path = require('path');

/**
 * Six-Dim Evaluator - Core Engine
 * 六维评估器 - 核心引擎
 */

/**
 * Evaluate a skill across six dimensions
 * @param {string} skillPath - Path to skill directory
 * @returns {Object} Evaluation result with scores and suggestions
 */
function evaluateSkill(skillPath) {
  if (!fs.existsSync(skillPath)) {
    throw new Error(`Skill path does not exist: ${skillPath}`);
  }

  // Collect data
  const data = collectSkillData(skillPath);
  
  // Calculate dimension scores
  const scores = {
    T: calculateTDimension(data),
    C: calculateCDimension(data),
    O: calculateODimension(data),
    E: calculateEDimension(data),
    M: calculateMDimension(data),
    U: calculateUDimension(data)
  };
  
  // Calculate overall score
  const overall = calculateOverallScore(scores);
  
  // Generate suggestions
  const suggestions = generateSuggestions(scores, data);
  
  return {
    skillPath,
    scores,
    overall,
    suggestions,
    evaluatedAt: new Date().toISOString()
  };
}

/**
 * Collect skill data
 */
function collectSkillData(skillPath) {
  const data = {
    hasTests: false,
    testCoverage: 0,
    hasDocumentation: false,
    documentationScore: 0,
    hasClawHubListing: false,
    clawHubStats: null,
    codeQuality: 0,
    versionHistory: []
  };
  
  // Check for tests
  const testsPath = path.join(skillPath, 'tests');
  if (fs.existsSync(testsPath)) {
    data.hasTests = true;
    // TODO: Parse test coverage report
    data.testCoverage = 0.85; // Placeholder
  }
  
  // Check for documentation
  const readmePath = path.join(skillPath, 'README.md');
  if (fs.existsSync(readmePath)) {
    data.hasDocumentation = true;
    const readmeContent = fs.readFileSync(readmePath, 'utf8');
    data.documentationScore = calculateDocumentationScore(readmeContent);
  }
  
  // Check for SKILL.md
  const skillMdPath = path.join(skillPath, 'SKILL.md');
  if (fs.existsSync(skillMdPath)) {
    const skillMdContent = fs.readFileSync(skillMdPath, 'utf8');
    data.codeQuality = calculateCodeQualityScore(skillMdContent);
  }
  
  // Check for version history
  const versionHistoryPath = path.join(skillPath, 'CHANGELOG.md');
  if (fs.existsSync(versionHistoryPath)) {
    const changelogContent = fs.readFileSync(versionHistoryPath, 'utf8');
    data.versionHistory = parseVersionHistory(changelogContent);
  }
  
  return data;
}

/**
 * Calculate documentation score
 */
function calculateDocumentationScore(content) {
  let score = 0;
  
  // Check for key sections
  const sections = [
    '使用场景', '使用方法', '核心功能',
    '六维评估', 'FAQ', '快速开始'
  ];
  
  sections.forEach(section => {
    if (content.includes(section)) {
      score += 0.15;
    }
  });
  
  // Check for code examples
  const codeExamples = (content.match(/```/g) || []).length;
  if (codeExamples >= 5) {
    score += 0.1;
  }
  
  return Math.min(1.0, score);
}

/**
 * Calculate code quality score
 */
function calculateCodeQualityScore(content) {
  // Simple heuristic based on SKILL.md completeness
  let score = 0.5; // Base score
  
  if (content.includes('版本')) score += 0.1;
  if (content.includes('定位')) score += 0.1;
  if (content.includes('使用场景')) score += 0.1;
  if (content.includes('核心功能')) score += 0.1;
  if (content.includes('六维评估')) score += 0.1;
  
  return Math.min(1.0, score);
}

/**
 * Parse version history
 */
function parseVersionHistory(content) {
  const versions = [];
  const versionRegex = /##?\s*v?(\d+\.\d+\.\d+)/g;
  let match;
  
  while ((match = versionRegex.exec(content)) !== null) {
    versions.push(match[1]);
  }
  
  return versions;
}

/**
 * Calculate T dimension score
 */
function calculateTDimension(data) {
  // T = (T₁×1.5 + T₂×1.2 + T₃×1.0 + T₄×1.5) / 5.2
  const T1 = 0.75; // Architecture (placeholder)
  const T2 = data.codeQuality;
  const T3 = 0.70; // Performance (placeholder)
  const T4 = data.testCoverage;
  
  return (T1 * 1.5 + T2 * 1.2 + T3 * 1.0 + T4 * 1.5) / 5.2;
}

/**
 * Calculate C dimension score
 */
function calculateCDimension(data) {
  // C = (C₁×1.5 + C₂×1.2 + C₃×1.0 + C₄×1.0) / 4.7
  const C1 = 0.70; // Framework (placeholder)
  const C2 = 0.70; // Insight (placeholder)
  const C3 = 0.70; // Decision support (placeholder)
  const C4 = data.documentationScore > 0.7 ? 0.75 : 0.65;
  
  return (C1 * 1.5 + C2 * 1.2 + C3 * 1.0 + C4 * 1.0) / 4.7;
}

/**
 * Calculate O dimension score
 */
function calculateODimension(data) {
  // O = (O₁×1.5 + O₂×1.2 + O₃×1.0 + O₄×1.5) / 5.2
  const O1 = 0.75; // API design (placeholder)
  const O2 = 0.70; // Event-driven (placeholder)
  const O3 = 0.70; // Data transfer (placeholder)
  const O4 = 0.75; // Task decomposition (placeholder)
  
  return (O1 * 1.5 + O2 * 1.2 + O3 * 1.0 + O4 * 1.5) / 5.2;
}

/**
 * Calculate E dimension score
 */
function calculateEDimension(data) {
  // E = (E₁×1.5 + E₂×1.5 + E₃×1.0 + E₄×1.2) / 5.2
  const E1 = 0.70; // Self-monitoring (placeholder)
  const E2 = 0.70; // Self-optimization (placeholder)
  const E3 = data.versionHistory.length > 3 ? 0.75 : 0.65;
  const E4 = 0.70; // Feedback collection (placeholder)
  
  return (E1 * 1.5 + E2 * 1.5 + E3 * 1.0 + E4 * 1.2) / 5.2;
}

/**
 * Calculate M dimension score
 */
function calculateMDimension(data) {
  // M = (M₁×1.5 + M₂×1.2 + M₃×1.5 + M₄×1.0) / 5.2
  const M1 = data.hasClawHubListing ? 1.0 : 0.4;
  const M2 = 0.50; // Adoption (placeholder)
  const M3 = 0.50; // Conversion (placeholder)
  const M4 = 0.50; // Revenue (placeholder)
  
  return (M1 * 1.5 + M2 * 1.2 + M3 * 1.5 + M4 * 1.0) / 5.2;
}

/**
 * Calculate U dimension score
 */
function calculateUDimension(data) {
  // U = (U₁×1.2 + U₂×1.5 + U₃×1.0 + U₄×1.0) / 4.7
  const U1 = 0.70; // Learning cost (placeholder)
  const U2 = data.documentationScore;
  const U3 = 0.70; // Error handling (placeholder)
  const U4 = 0.70; // Interaction (placeholder)
  
  return (U1 * 1.2 + U2 * 1.5 + U3 * 1.0 + U4 * 1.0) / 4.7;
}

/**
 * Calculate overall score
 */
function calculateOverallScore(scores) {
  // Weighted average
  const weights = {
    T: 1.0,
    C: 1.0,
    O: 1.5,
    E: 1.5,
    M: 1.2,
    U: 1.0
  };
  
  const totalWeight = Object.values(weights).reduce((a, b) => a + b, 0);
  const weightedSum = Object.entries(scores).reduce((sum, [dim, score]) => {
    return sum + score * weights[dim];
  }, 0);
  
  return weightedSum / totalWeight;
}

/**
 * Generate improvement suggestions
 */
function generateSuggestions(scores, data) {
  const suggestions = [];
  
  // Check each dimension
  Object.entries(scores).forEach(([dim, score]) => {
    if (score < 0.80) {
      suggestions.push({
        dimension: dim,
        currentScore: score,
        targetScore: 0.80,
        gap: 0.80 - score,
        actions: getDimensionActions(dim, score, data)
      });
    }
  });
  
  return suggestions;
}

/**
 * Get improvement actions for a dimension
 */
function getDimensionActions(dim, score, data) {
  const actions = {
    T: [
      '提升测试覆盖率至 85%+',
      '优化代码质量（ESLint 得分 95%+）',
      '添加性能基准测试'
    ],
    C: [
      '添加 5 个实战案例',
      '完善思维框架文档',
      '提供决策支持工具'
    ],
    O: [
      '完善 API 文档',
      '添加技能协作示例',
      '实现事件驱动架构'
    ],
    E: [
      '建立反馈收集机制',
      '完善版本历史',
      '实现自动优化触发'
    ],
    M: [
      'ClawHub 上架',
      '收集用户反馈',
      '制定定价策略'
    ],
    U: [
      '完善 FAQ（10+ 问题）',
      '添加快速开始指南',
      '优化错误提示'
    ]
  };
  
  return actions[dim] || [];
}

/**
 * Compare two versions of a skill
 */
function compareVersions(oldResult, newResult) {
  const comparison = {
    oldVersion: oldResult,
    newVersion: newResult,
    changes: {}
  };
  
  Object.keys(oldResult.scores).forEach(dim => {
    const oldScore = oldResult.scores[dim];
    const newScore = newResult.scores[dim];
    const change = newScore - oldScore;
    
    comparison.changes[dim] = {
      old: oldScore,
      new: newScore,
      change: change,
      trend: change > 0 ? 'improved' : change < 0 ? 'degraded' : 'stable'
    };
  });
  
  comparison.changes.overall = {
    old: oldResult.overall,
    new: newResult.overall,
    change: newResult.overall - oldResult.overall,
    trend: newResult.overall > oldResult.overall ? 'improved' : 'degraded'
  };
  
  return comparison;
}

module.exports = {
  evaluateSkill,
  compareVersions,
  collectSkillData,
  calculateTDimension,
  calculateCDimension,
  calculateODimension,
  calculateEDimension,
  calculateMDimension,
  calculateUDimension,
  calculateOverallScore,
  generateSuggestions
};
