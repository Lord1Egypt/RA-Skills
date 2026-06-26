/**
 * 项目评分器 - 对项目进行价值评估
 */

/**
 * 对项目列表进行评分和排序
 */
async function scoreProjects(projects) {
  const scored = projects.map(project => {
    const score = calculateScore(project);
    const confidence = calculateConfidence(project);
    
    return {
      ...project,
      score,
      confidence,
      confidenceEmoji: getConfidenceEmoji(confidence)
    };
  });
  
  // 按分数降序排序
  scored.sort((a, b) => b.score - a.score);
  
  return scored;
}

/**
 * 计算项目分数
 */
function calculateScore(project) {
  let score = 0;
  
  // 1. 创新性 (30%)
  const innovation = scoreInnovation(project);
  score += innovation * 0.3;
  
  // 2. 实用性 (30%)
  const practicality = scorePracticality(project);
  score += practicality * 0.3;
  
  // 3. 可复制性 (20%)
  const replicability = scoreReplicability(project);
  score += replicability * 0.2;
  
  // 4. 趋势性 (20%)
  const trending = scoreTrending(project);
  score += trending * 0.2;
  
  return Math.round(score);
}

/**
 * 创新性评分
 */
function scoreInnovation(project) {
  let score = 50; // 基础分
  
  // AI/自动化相关加分
  if (project.name.toLowerCase().includes('ai') || 
      project.description?.toLowerCase().includes('ai')) {
    score += 20;
  }
  
  // 新项目加分
  if (project.isNew || project.starsToday > 200) {
    score += 15;
  }
  
  // 独特功能加分
  if (project.description?.includes('first') || 
      project.description?.includes('unique')) {
    score += 15;
  }
  
  return Math.min(score, 100);
}

/**
 * 实用性评分
 */
function scorePracticality(project) {
  let score = 50;
  
  // 可部署加分
  if (project.deployable) {
    score += 20;
  }
  
  // 有文档加分
  if (project.hasReadme || project.stars > 1000) {
    score += 15;
  }
  
  // 活跃维护加分
  if (project.recentCommits > 10) {
    score += 15;
  }
  
  return Math.min(score, 100);
}

/**
 * 可复制性评分
 */
function scoreReplicability(project) {
  let score = 50;
  
  // 开源项目
  if (project.sourceType === 'github' || project.sourceType === 'tools') {
    score += 30;
  }
  
  // 技术栈简单
  if (project.language === 'JavaScript' || 
      project.language === 'Python') {
    score += 20;
  }
  
  return Math.min(score, 100);
}

/**
 * 趋势性评分
 */
function scoreTrending(project) {
  let score = 50;
  
  // Star 增长快
  if (project.starsToday > 300) {
    score += 30;
  } else if (project.starsToday > 100) {
    score += 20;
  }
  
  // 社区讨论热度
  if (project.comments > 50 || project.score > 100) {
    score += 20;
  }
  
  return Math.min(score, 100);
}

/**
 * 计算置信度
 */
function calculateConfidence(project) {
  // GitHub 官方数据最可信
  if (project.source?.includes('github')) {
    return 90;
  }
  
  // Product Hunt / HN 次之
  if (project.source === 'product-hunt' || project.source === 'hacker-news') {
    return 80;
  }
  
  // 其他来源
  return 70;
}

/**
 * 获取置信度表情
 */
function getConfidenceEmoji(confidence) {
  if (confidence >= 90) return '🟢';
  if (confidence >= 70) return '🟡';
  return '🟠';
}

/**
 * 添加趋势标记
 */
function addTrendMarker(project) {
  const growth = project.starsToday || project.stars || 0;
  
  if (growth >= 1000) {
    project.trend = '🔥';
  } else if (growth >= 300) {
    project.trend = '📈';
  } else {
    project.trend = '';
  }
  
  return project;
}

/**
 * 对项目列表进行评分和排序（增强版）
 */
async function scoreProjects(projects) {
  const scored = projects.map(project => {
    const score = calculateScore(project);
    const confidence = calculateConfidence(project);
    
    return {
      ...project,
      score,
      confidence,
      confidenceEmoji: getConfidenceEmoji(confidence)
    };
  });
  
  // 按分数降序排序
  scored.sort((a, b) => b.score - a.score);
  
  // 添加趋势标记
  scored.forEach(project => addTrendMarker(project));
  
  return scored;
}

module.exports = {
  scoreProjects,
  addTrendMarker
};
