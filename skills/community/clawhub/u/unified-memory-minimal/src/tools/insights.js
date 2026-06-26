/**
 * memory_insights - 用户记忆洞察分析
 * 分析用户偏好、记忆热点、行为趋势
 */

import { getAllMemories } from '../storage.js';
import { Counter } from '../utils/counter.js';

const TOOLS = ['飞书', '微信', 'QQ', '钉钉', 'Slack', 'Notion', 'Obsidian', 'GitHub', 'OpenClaw'];
const PROJECT_PATTERNS = ['项目', '龙宫', '官网', '重构', '电商', 'MetaGPT', 'OpenClaw'];
const CATEGORY_KEYWORDS = {
  'preference': ['喜欢', '偏好', '决定', '选择', '使用'],
  'fact': ['事实', '知道', '了解', '认识'],
  'decision': ['决定', '决策', '选择', '方案'],
  'learning': ['学习', '学到了', '掌握了', '了解']
};

export async function analyzeInsights() {
  const memories = getAllMemories();
  
  if (memories.length === 0) {
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({ summary: '暂无记忆数据', count: 0 }, null, 2)
      }]
    };
  }
  
  // Category distribution
  const categoryStats = new Counter();
  const toolUsage = new Counter();
  const projectUsage = new Counter();
  const importanceScores = [];
  
  for (const mem of memories) {
    categoryStats.increment(mem.category || 'other');
    importanceScores.push(mem.importance || 0.5);
    
    const text = mem.text || '';
    for (const tool of TOOLS) {
      if (text.includes(tool)) toolUsage.increment(tool);
    }
    for (const proj of PROJECT_PATTERNS) {
      if (text.includes(proj)) projectUsage.increment(proj);
    }
  }
  
  // Calculate average importance
  const avgImportance = importanceScores.reduce((a, b) => a + b, 0) / importanceScores.length;
  
  // Memory growth over time (by month)
  const monthlyCount = new Counter();
  for (const mem of memories) {
    const ts = mem.created_at || mem.timestamp;
    if (ts) {
      const date = new Date(typeof ts === 'number' ? ts : ts);
      const month = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
      monthlyCount.increment(month);
    }
  }
  
  const result = {
    summary: {
      total_memories: memories.length,
      avg_importance: Math.round(avgImportance * 100) / 100,
      category_count: Object.keys(categoryStats.counts).length
    },
    category_distribution: categoryStats.top(5),
    top_tools: toolUsage.top(5),
    top_projects: projectUsage.top(5),
    monthly_growth: Object.entries(monthlyCount.counts)
      .sort(([a], [b]) => b.localeCompare(a))
      .slice(0, 6)
      .reduce((acc, [month, count]) => ({ ...acc, [month]: count }), {}),
    suggestions: generateSuggestions(categoryStats, toolUsage, avgImportance)
  };
  
  return {
    content: [{
      type: 'text',
      text: JSON.stringify(result, null, 2)
    }]
  };
}

function generateSuggestions(categoryStats, toolUsage, avgImportance) {
  const suggestions = [];
  
  if (avgImportance < 0.5) {
    suggestions.push('平均重要性偏低，建议关注更高价值的记忆');
  }
  
  if (categoryStats.counts['other'] > 5) {
    suggestions.push('有较多未分类记忆，建议使用 category 参数进行分类');
  }
  
  const topTool = toolUsage.top(1)[0];
  if (topTool) {
    suggestions.push(`你最常用 ${topTool[0]}，相关记忆最多`);
  }
  
  return suggestions;
}

// CLI entry
export async function cmdInsightsCLI(args) {
  const result = await analyzeInsights();
  console.log(result.content[0].text);
}
