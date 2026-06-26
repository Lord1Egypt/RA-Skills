/**
 * Memory Predict - 记忆预测模块
 * 
 * 功能:
 * - 基于时间模式预测需求
 * - 基于行为模式预测需求
 * - 主动推送预测结果
 * 
 * Ported from memory_predict.py
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { getAllMemories } from '../storage.js';


const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const MEMORIES_FILE = join(MEMORY_DIR, 'memories.json');
const ACCESS_FILE = join(MEMORY_DIR, 'access_history.json');
const PATTERN_FILE = join(MEMORY_DIR, 'patterns.json');
const PREDICTION_FILE = join(MEMORY_DIR, 'predictions.json');
const PREDICTION_CONFIG_FILE = join(MEMORY_DIR, 'prediction_config.json');

// Default config
const DEFAULT_CONFIG = {
  enabled: true,
  min_confidence: 0.7,
  max_predictions: 5,
  push_enabled: true,
  patterns: {
    time_based: true,
    behavior_based: true,
    project_based: true
  },
  quiet_hours: { start: 23, end: 8 }
};

// Time patterns
const TIME_PATTERNS = [
  {
    name: 'weekday_morning',
    condition: (dt) => dt.day < 5 && dt.hour >= 8 && dt.hour < 12,
    predictions: ['查看日程', '查看任务', '今日重点'],
    confidence: 0.8
  },
  {
    name: 'weekday_afternoon',
    condition: (dt) => dt.day < 5 && dt.hour >= 14 && dt.hour < 18,
    predictions: ['项目进度', '待办事项', '会议安排'],
    confidence: 0.75
  },
  {
    name: 'weekday_evening',
    condition: (dt) => dt.day < 5 && dt.hour >= 18 && dt.hour < 22,
    predictions: ['明日计划', '今日总结', '邮件处理'],
    confidence: 0.7
  },
  {
    name: 'friday_afternoon',
    condition: (dt) => dt.day === 4 && dt.hour >= 14 && dt.hour < 18,
    predictions: ['周末安排', '下周计划', '项目进度'],
    confidence: 0.85
  },
  {
    name: 'weekend',
    condition: (dt) => dt.day >= 5,
    predictions: ['减少打扰', '轻松话题'],
    confidence: 0.6
  }
];

// ============================================================
// Config
// ============================================================

function loadConfig() {
  if (existsSync(PREDICTION_CONFIG_FILE)) {
    try {
      return JSON.parse(readFileSync(PREDICTION_CONFIG_FILE, 'utf-8'));
    } catch { /* ignore */ }
  }
  return { ...DEFAULT_CONFIG };
}

function saveConfig(config) {
  mkdirSync(MEMORY_DIR, { recursive: true });
  writeFileSync(PREDICTION_CONFIG_FILE, JSON.stringify(config, null, 2), 'utf-8');
}

// ============================================================
// Data Loading
// ============================================================

function loadAccessHistory() {
  if (existsSync(ACCESS_FILE)) {
    try {
      return JSON.parse(readFileSync(ACCESS_FILE, 'utf-8'));
    } catch { /* ignore */ }
  }
  return [];
}

// ============================================================
// Pattern Analysis
// ============================================================

function analyzeTimePatterns() {
  const accessHistory = loadAccessHistory();
  const patterns = { hourly: {}, daily: {}, weekly: {}, monthly: {} };

  for (const entry of (accessHistory.accesses || [])) {
    const timestamp = entry.timestamp || entry.create_time;
    if (!timestamp) continue;
    try {
      const dt = new Date(timestamp);
      const hour = dt.getHours();
      const day = dt.getDay();
      patterns.hourly[hour] = (patterns.hourly[hour] || 0) + 1;
      patterns.daily[day] = (patterns.daily[day] || 0) + 1;
    } catch { /* skip */ }
  }

  return patterns;
}

function analyzeBehaviorPatterns() {
  const accessHistory = loadAccessHistory();
  const patterns = { search_keywords: {}, categories: {} };

  for (const entry of (accessHistory.accesses || [])) {
    const query = entry.query || entry.keyword;
    if (query) patterns.search_keywords[query] = (patterns.search_keywords[query] || 0) + 1;
    const category = entry.category;
    if (category) patterns.categories[category] = (patterns.categories[category] || 0) + 1;
  }

  return patterns;
}

function analyzeProjectPatterns(memories) {
  const projects = {};
  const projectRegex = /项目[：:]\s*([^\s，。]+)|project[：:]\s*([^\s，。]+)/i;
  const deadlineRegex = /截止[日期]*[：:]\s*(\d{4}-\d{2}-\d{2})/;

  for (const mem of memories) {
    const text = mem.text || '';
    const match = text.match(projectRegex);
    if (match) {
      const projectName = match[1] || match[2];
      if (!projects[projectName]) projects[projectName] = { memories: [], deadline: null };
      projects[projectName].memories.push(mem.id);
      const deadlineMatch = text.match(deadlineRegex);
      if (deadlineMatch) projects[projectName].deadline = deadlineMatch[1];
    }
  }

  return projects;
}

// ============================================================
// Predictions
// ============================================================

function getTimeBasedPredictions(now) {
  const predictions = [];
  const dt = {
    hour: now.getHours(),
    day: now.getDay(),
    weekday: now.getDay()
  };

  for (const pattern of TIME_PATTERNS) {
    if (pattern.condition(dt)) {
      for (const pred of pattern.predictions) {
        predictions.push({
          type: 'time_based',
          pattern: pattern.name,
          prediction: pred,
          confidence: pattern.confidence,
          reason: `当前时间匹配模式: ${pattern.name}`
        });
      }
    }
  }

  return predictions;
}

function getBehaviorBasedPredictions(accessHistory) {
  const predictions = [];
  const recent = [];
  const now = Date.now();

  for (const entry of (accessHistory.accesses || [])) {
    const timestamp = entry.timestamp || entry.create_time;
    if (!timestamp) continue;
    try {
      const dt = new Date(timestamp);
      if (now - dt.getTime() < 3600000) recent.push(entry);
    } catch { /* skip */ }
  }

  /** @type {Map<string, number>} */
  const topics = new Map();
  for (const entry of recent) {
    const cat = entry.category;
    if (cat) topics.set(cat, (topics.get(cat) || 0) + 1);
  }

  for (const [topic, count] of topics) {
    if (count >= 2) {
      predictions.push({
        type: 'behavior_based',
        prediction: `深入了解${topic}相关信息`,
        confidence: Math.min(0.9, 0.7 + count * 0.05),
        reason: `最近${count}次访问${topic}相关记忆`
      });
    }
  }

  return predictions;
}

function getProjectBasedPredictions(projects) {
  const predictions = [];
  const now = new Date();

  for (const [projectName, projectData] of Object.entries(projects)) {
    const deadline = projectData.deadline;
    if (!deadline) continue;
    try {
      const deadlineDt = new Date(deadline);
      const daysLeft = Math.floor((deadlineDt - now) / (24 * 60 * 60 * 1000));
      if (daysLeft > 0 && daysLeft <= 3) {
        predictions.push({
          type: 'project_based',
          prediction: `项目「${projectName}」即将截止（${daysLeft}天后）`,
          confidence: 0.9,
          reason: '项目截止时间临近'
        });
      } else if (daysLeft <= 0) {
        predictions.push({
          type: 'project_based',
          prediction: `项目「${projectName}」已过期，需要更新`,
          confidence: 0.95,
          reason: '项目已过截止日期'
        });
      }
    } catch { /* skip */ }
  }

  return predictions;
}

function predictToday() {
  const config = loadConfig();
  const memories = getAllMemories();
  const accessHistory = loadAccessHistory();
  const now = new Date();

  // Quiet hours check
  const hour = now.getHours();
  if (config.quiet_hours.start <= hour || hour < config.quiet_hours.end) {
    return {
      predictions: [{
        type: 'quiet_hours',
        prediction: '静默时段，减少推送',
        confidence: 1.0,
        reason: `当前时间 ${hour}:00 在静默时段 (${config.quiet_hours.start}:00-${config.quiet_hours.end}:00)`
      }],
      push: false
    };
  }

  /** @type {Array} */
  const allPredictions = [];

  if (config.patterns.time_based) {
    allPredictions.push(...getTimeBasedPredictions(now));
  }
  if (config.patterns.behavior_based) {
    allPredictions.push(...getBehaviorBasedPredictions(accessHistory));
  }
  if (config.patterns.project_based) {
    const projects = analyzeProjectPatterns(memories);
    allPredictions.push(...getProjectBasedPredictions(projects));
  }

  // Filter by confidence
  const filtered = allPredictions.filter(p => p.confidence >= config.min_confidence);
  filtered.sort((a, b) => b.confidence - a.confidence);

  return {
    predictions: filtered.slice(0, config.max_predictions),
    push: config.push_enabled && filtered.length > 0,
    generated_at: now.toISOString()
  };
}

function trainPatterns() {
  const memories = getAllMemories();
  const accessHistory = loadAccessHistory();

  const timePatterns = analyzeTimePatterns();
  const behaviorPatterns = analyzeBehaviorPatterns();
  const projectPatterns = analyzeProjectPatterns(memories);

  const result = {
    time: timePatterns,
    behavior: behaviorPatterns,
    projects: projectPatterns,
    trained_at: new Date().toISOString()
  };

  mkdirSync(MEMORY_DIR, { recursive: true });
  writeFileSync(PATTERN_FILE, JSON.stringify(result, null, 2), 'utf-8');

  return result;
}

// ============================================================
// CLI Handler
// ============================================================

/**
 * @param {string} command
 * @param {object} args
 * @returns {object}
 */
export function cmdPredict(command, args) {
  switch (command) {
    case 'config': {
      const config = loadConfig();
      if (args.json) return { type: 'json', data: config };
      const lines = ['🔮 预测配置', ''];
      for (const [k, v] of Object.entries(config)) {
        lines.push(`   ${k}: ${JSON.stringify(v)}`);
      }
      return { type: 'text', text: lines.join('\n') };
    }

    case 'enable-push': {
      const config = loadConfig();
      config.push_enabled = true;
      saveConfig(config);
      return { type: 'text', text: '✅ 已启用预测推送' };
    }

    case 'disable-push': {
      const config = loadConfig();
      config.push_enabled = false;
      saveConfig(config);
      return { type: 'text', text: '✅ 已禁用预测推送' };
    }

    case 'train':
    case 'analyze': {
      const result = trainPatterns();
      if (args.json) return { type: 'json', data: result };
      const lines = [
        '🧠 训练预测模型...',
        '',
        '✅ 时间模式分析完成',
        `   小时分布: ${JSON.stringify(result.time.hourly)}`,
        `   星期分布: ${JSON.stringify(result.time.daily)}`,
        '',
        '✅ 行为模式分析完成',
        '',
        '✅ 项目模式分析完成',
        `   项目数量: ${Object.keys(result.projects).length}`,
        '',
        `💾 模式已保存到 ${PATTERN_FILE}`
      ];
      return { type: 'text', text: lines.join('\n') };
    }

    case 'today': {
      const result = predictToday();
      const predictions = result.predictions || [];
      const lines = ['🔮 今日需求预测', '', '='.repeat(50)];
      if (predictions.length === 0) {
        lines.push('暂无预测');
      } else {
        predictions.forEach((p, i) => {
          const confBar = '█'.repeat(Math.round(p.confidence * 10)) + '░'.repeat(10 - Math.round(p.confidence * 10));
          lines.push(`\n[${i + 1}] ${p.prediction}`);
          lines.push(`    置信度: |${confBar}| ${Math.round(p.confidence * 100)}%`);
          lines.push(`    类型: ${p.type}`);
          lines.push(`    原因: ${p.reason}`);
        });
      }
      lines.push(`\n📱 推送状态: ${result.push ? '启用' : '禁用'}`);

      // Save prediction
      mkdirSync(MEMORY_DIR, { recursive: true });
      writeFileSync(PREDICTION_FILE, JSON.stringify(result, null, 2), 'utf-8');

      return { type: 'text', text: lines.join('\n') };
    }

    case 'week': {
      return { type: 'text', text: '🔮 本周需求预测\n\n   功能开发中...\n   建议: 先使用 `mem predict train` 训练模型' };
    }

    default:
      return { error: `未知命令: ${command}` };
  }
}

// ============================================================
// Enhanced Predict Recall (v1.2 extension)
// ============================================================

/**
 * Enhanced prediction with time-awareness, TTL warnings, and importance scoring
 * @param {string} context - Context string for prediction
 * @param {object} options - Options object
 * @param {number} options.topK - Number of predictions to return (default 5)
 * @param {boolean} options.includeTTL - Include TTL-based predictions (default true)
 */
export async function enhancedPredictRecall(context, options = {}) {
  const { topK = 5, includeTTL = true } = options;

  const memories = getAllMemories();
  const now = Date.now();
  const DAY_MS = 24 * 3600 * 1000;

  // 1. Base predictions from context triggers
  const predictions = [];
  const contextLower = (context || '').toLowerCase();

  const ENHANCED_TRIGGERS = {
    project: ['项目', '开发', '代码', 'git', 'project', 'code', 'bug', 'feature'],
    meeting: ['会议', '讨论', 'meeting', 'discuss', '评审', 'review'],
    decision: ['决定', '选择', 'decided', 'choice', '方案'],
    personal: ['生活', '健康', '家庭', 'personal', 'health', 'family'],
    learning: ['学习', '阅读', '课程', 'learning', 'study', 'book'],
  };

  for (const mem of memories) {
    const textLower = (mem.text || '').toLowerCase();
    let relevance = 0;
    const reasons = [];

    // Context keyword matching
    for (const [category, keywords] of Object.entries(ENHANCED_TRIGGERS)) {
      for (const keyword of keywords) {
        if (contextLower.includes(keyword) && textLower.includes(keyword)) {
          relevance += 2;
          reasons.push(`context:${keyword}`);
        }
      }
    }

    // Importance score contribution
    relevance += (mem.importance || 0.5) * 0.5;

    // Access frequency contribution
    relevance += Math.log1p(mem.access_count || 0) * 0.3;

    // NEW: Time-aware predictions (TTL warning - 7 days before expiry)
    if (includeTTL && mem.expires_at) {
      const expiresAt = new Date(mem.expires_at).getTime();
      const daysUntilExpiry = (expiresAt - now) / DAY_MS;
      if (daysUntilExpiry > 0 && daysUntilExpiry <= 7) {
        relevance += (7 - daysUntilExpiry) * 0.5; // Higher boost as expiry approaches
        reasons.push(`ttl_warning:${Math.ceil(daysUntilExpiry)}d`);
      }
    }

    // NEW: Anniversary predictions (memories created around same date in past)
    if (includeTTL && mem.created_at) {
      const created = new Date(mem.created_at);
      const nowDate = new Date(now);
      if (
        created.getMonth() === nowDate.getMonth() &&
        Math.abs(created.getDate() - nowDate.getDate()) <= 3
      ) {
        relevance += 1.5;
        reasons.push('anniversary');
      }
    }

    if (relevance > 0) {
      predictions.push({
        memory: mem,
        relevance,
        reasons,
        type: 'enhanced',
      });
    }
  }

  predictions.sort((a, b) => b.relevance - a.relevance);
  return predictions.slice(0, topK);
}

/**
 * Predict related memories when a specific memory is accessed
 * @param {string} memoryId - The memory ID that was just accessed
 * @param {number} topK - Number of related memories to predict
 */
export function predictRelatedOnAccess(memoryId, topK = 3) {
  const memories = getAllMemories();
  const target = memories.find(m => m.id === memoryId);
  if (!target) return [];

  const targetLower = (target.text || '').toLowerCase();
  const targetTags = new Set(target.tags || []);
  const targetCategory = target.category || '';

  const predictions = [];

  for (const mem of memories) {
    if (mem.id === memoryId) continue;

    let relevance = 0;
    const reasons = [];

    // Tag overlap
    const memTags = new Set(mem.tags || []);
    const overlap = [...targetTags].filter(t => memTags.has(t)).length;
    if (overlap > 0) {
      relevance += overlap * 1.5;
      reasons.push(`tag_match:${overlap}`);
    }

    // Category match
    if (mem.category === targetCategory) {
      relevance += 1.0;
      reasons.push('category_match');
    }

    // Keyword overlap
    const memLower = (mem.text || '').toLowerCase();
    const words = targetLower.split(/\s+/).filter(w => w.length > 2);
    for (const word of words) {
      if (memLower.includes(word)) {
        relevance += 0.3;
      }
    }

    // Importance bonus
    relevance += (mem.importance || 0.5) * 0.3;

    if (relevance > 0) {
      predictions.push({
        memory: mem,
        relevance,
        reasons,
        type: 'related',
      });
    }
  }

  predictions.sort((a, b) => b.relevance - a.relevance);
  return predictions.slice(0, topK);
}

/**
 * High-value memory prediction based on historical access patterns
 * @param {number} topK - Number of high-value memories to return
 */
export function predictHighValueMemories(topK = 5) {
  const memories = getAllMemories();
  const now = Date.now();
  const DAY_MS = 24 * 3600 * 1000;

  const scored = memories.map(mem => {
    let score = 0;
    const reasons = [];

    // Importance contribution
    score += (mem.importance || 0.5) * 3;
    if (mem.importance >= 0.8) reasons.push('high_importance');

    // Recent access bonus (accessed in last 7 days)
    const lastAccessed = mem.last_accessed_at || mem.updated_at || mem.created_at;
    if (lastAccessed) {
      const daysSince = (now - new Date(lastAccessed).getTime()) / DAY_MS;
      if (daysSince <= 7) {
        score += 2 * (1 - daysSince / 7);
        reasons.push('recently_accessed');
      }
    }

    // Frequent access bonus
    score += Math.log1p(mem.access_count || 0) * 0.5;
    if ((mem.access_count || 0) >= 5) reasons.push('frequently_accessed');

    // Has tags (structured) bonus
    if ((mem.tags || []).length > 0) {
      score += 0.5;
      reasons.push('has_tags');
    }

    return { memory: mem, score, reasons, type: 'high_value' };
  });

  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, topK);
}

export default { cmdPredict };
