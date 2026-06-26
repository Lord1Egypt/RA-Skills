/**
 * 虚拟论坛 - 共享配置
 * Shared Config for Virtual Forum v3.5
 *
 * 解决问题：
 * - [P2] forum-engine.js 和 subagent-arena.js 中大量重复的模式/风格定义
 * - [P1] 硬编码路径 /Users/caoyirong
 */

const path = require('path');
const fs = require('fs');

/**
 * 获取默认 Skills 目录（不再硬编码用户名）
 */
function getDefaultSkillsDir() {
  const home = process.env.HOME || process.env.USERPROFILE || '';
  if (!home) {
    console.warn('⚠️ 无法检测 HOME 目录，请通过构造函数显式传入 skillsDir');
  }
  return path.join(home, '.openclaw', 'skills');
}

/**
 * 讨论模式定义（唯一来源）
 */
const DISCUSSION_MODES = {
  exploratory: {
    name: '探索性讨论',
    instruction: '这是探索性讨论，请从你的视角深入分析问题，展现多角度思维。'
  },
  adversarial: {
    name: '对抗性辩论',
    instruction: '这是对抗性辩论，你必须坚定维护自己的立场，积极反驳对方观点。'
  },
  decision: {
    name: '决策型讨论',
    instruction: '这是决策型讨论，请分析各方案的利弊，给出建设性建议。'
  }
};

/**
 * 主持人风格定义（唯一来源）
 */
const MODERATOR_STYLES = {
  balanced: {
    name: '理性主持人',
    style: '客观中立，善于引导对话',
    questions: ['各位怎么看这个问题？', '有没有不同的观点？', '能否详细解释？']
  },
  provocative: {
    name: '犀利主持人',
    style: '追问到底，挑战每个观点',
    questions: ['为什么你这么认为？', '有没有相反的证据？', '你能为你的观点辩护吗？']
  },
  synthesizing: {
    name: '整合主持人',
    style: '善于归纳，推动形成共识',
    questions: ['能否总结核心观点？', '大家有没有共同点？', '能否找到折中方案？']
  }
};

/**
 * 胜负判定方式
 */
const VERDICT_TYPES = {
  points: 'points',
  vote: 'vote',
  concession: 'concession',
  consensus: 'consensus'
};

/**
 * 默认值
 */
const DEFAULTS = {
  mode: 'adversarial',
  rounds: 10,
  moderatorName: '巴菲特',
  moderatorSkill: 'warren-buffett',
  moderatorStyle: 'provocative',
  verdictType: 'points',
  outputFormat: 'dialogue',
  minResponseLength: 200,
  maxResponseLength: 400,
  contextWindowSize: 6,
  summarizeEveryNRounds: 5,
  apiRetryAttempts: 3,
  apiBaseDelay: 5000,  // [FIX] 从2000ms改为5000ms，给API更充足的响应时间
  maxRounds: 100,      // [FIX] 新增最大轮次限制，防止恶意输入
  gameTheory: {
    totalValue: 100,
    defaultDiscountFactor: 0.9,
    defaultOutsideOption: 20,
    defaultReputationType: 'balanced'
  }
};

/**
 * 加载 Skill 内容（共享函数）
 * 
 * [FIX] 防止路径遍历攻击 + 多路径搜索
 */
function loadSkill(skillsDir, skillName) {
  if (!skillName) return null;
  
  // [FIX] 防止路径遍历攻击 - 只取最后一部分
  const safeName = path.basename(skillName);
  if (safeName !== skillName || skillName.includes('..') || skillName.includes('/') || skillName.includes('\\')) {
    console.warn(`⚠️ 危险的skillName: ${skillName}，已被清理为: ${safeName}`);
  }
  
  // [FIX] 尝试多个可能的路径
  const possiblePaths = [
    path.join(skillsDir, safeName, 'SKILL.md'),
    path.join(skillsDir, `${safeName}-perspective`, 'SKILL.md'),
    path.join(skillsDir, safeName, 'skill.md'),
    path.join(skillsDir, safeName.toLowerCase(), 'SKILL.md'),
  ];
  
  for (const skillPath of possiblePaths) {
    try {
      if (fs.existsSync(skillPath)) {
        const content = fs.readFileSync(skillPath, 'utf8');
        console.log(` ✓ 加载Skill: ${safeName} (from ${path.basename(path.dirname(skillPath))})`);
        return content;
      }
    } catch (e) {
      console.warn(` ⚠️ 尝试加载 ${skillPath} 失败: ${e.message}`);
    }
  }
  
  console.warn(` ✗ Skill未找到: ${safeName}`);
  return null;
}

/**
 * 输入验证（共享函数）
 * 
 * [FIX] 增加rounds上限检查、skillName安全性验证
 */
function validateConfig(config) {
  if (!config) throw new Error('配置不能为空');
  if (!config.topic || typeof config.topic !== 'string' || config.topic.trim() === '') {
    throw new Error('话题(topic)不能为空');
  }
  if (!Array.isArray(config.participants) || config.participants.length < 2) {
    throw new Error('至少需要2位参与者(participants)');
  }
  if (config.rounds !== undefined) {
    if (!Number.isInteger(config.rounds) || config.rounds < 1) {
      throw new Error('轮次(rounds)必须是正整数');
    }
    // [FIX] 添加上限检查，防止恶意输入
    if (config.rounds > DEFAULTS.maxRounds) {
      throw new Error(`轮次(rounds)不能超过${DEFAULTS.maxRounds}，防止资源耗尽`);
    }
  }
  if (config.mode && !DISCUSSION_MODES[config.mode]) {
    throw new Error(`不支持的讨论模式: ${config.mode}，可选: ${Object.keys(DISCUSSION_MODES).join(', ')}`);
  }
  
  // [FIX] 验证参与者名称
  for (const p of config.participants) {
    if (!p.name || typeof p.name !== 'string') {
      throw new Error('每个参与者必须有name属性');
    }
    // 限制名称长度，防止过长的输入
    if (p.name.length > 50) {
      throw new Error('参与者名称不能超过50个字符');
    }
  }
}

/**
 * 指数退避延迟
 */
async function exponentialBackoff(attempt, baseDelay = DEFAULTS.apiBaseDelay) {
  const delay = baseDelay * Math.pow(2, attempt) + Math.random() * 1000;
  console.log(` ⏳ 等待 ${(delay / 1000).toFixed(1)}s 后重试...`);
  return new Promise(resolve => setTimeout(resolve, delay));
}

module.exports = {
  getDefaultSkillsDir,
  DISCUSSION_MODES,
  MODERATOR_STYLES,
  VERDICT_TYPES,
  DEFAULTS,
  loadSkill,
  validateConfig,
  exponentialBackoff
};