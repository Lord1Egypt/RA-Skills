/**
 * 虚拟论坛 v4.0 - 配置驱动架构
 * 
 * 【重要架构说明】
 * 此模块不直接运行subagent，而是生成配置供主代理使用。
 * 实际subagent orchestration由主代理通过sessions_spawn完成。
 * 
 * 使用方式：
 * 1. 主代理调用 generateDebateConfig() 获取辩论配置
 * 2. 主代理使用 sessions_spawn 启动subagents
 * 3. 主代理使用 sessions_send 进行协调
 */

const path = require('path');
const fs = require('fs');
const {
  getDefaultSkillsDir,
  DISCUSSION_MODES,
  DEFAULTS,
  loadSkill
} = require('./shared-config.js');

/**
 * 生成辩论配置
 * 主代理调用此函数获取完整的辩论参数
 */
async function generateDebateConfig(config) {
  const {
    topic,
    mode = 'adversarial',
    rounds = 10,
    participants = [],
    moderatorName = '主持人',
    moderatorSkill = null,
    contextWindowSize = 16000
  } = config;

  // 加载所有skill内容
  const participantsWithSkills = [];
  for (const p of participants) {
    const skillContent = await loadSkill(getDefaultSkillsDir(), p.skillName);
    participantsWithSkills.push({
      name: p.name,
      skillName: p.skillName,
      skillContent: skillContent || ''
    });
  }

  // 加载主持人的skill
  let moderatorSkillContent = '';
  if (moderatorSkill) {
    moderatorSkillContent = await loadSkill(getDefaultSkillsDir(), moderatorSkill);
  }

  const debateConfig = {
    id: `debate-${Date.now()}`,
    topic,
    mode,
    rounds,
    participants: participantsWithSkills,
    moderator: {
      name: moderatorName,
      skillName: moderatorSkill,
      skillContent: moderatorSkillContent
    },
    contextWindowSize,
    settings: {
      minResponseLength: DEFAULTS.minResponseLength,
      maxResponseLength: DEFAULTS.maxResponseLength
    }
  };

  return debateConfig;
}

/**
 * 为指定参与者构建系统提示
 */
function buildSystemPrompt(participant, config) {
  const modeConfig = DISCUSSION_MODES[config.mode] || DISCUSSION_MODES.adversarial;

  return `你是${participant.name}。

背景资料：
${participant.skillContent || '（无可用背景）'}

讨论话题：${config.topic}

讨论模式：${modeConfig.name}
${modeConfig.instruction}

你的任务：
1. 用第一人称表达你的观点
2. 体现你的性格、思维方式和表达风格
3. 可以向对方提问或质疑
4. 必要时引用具体数据或案例
5. 每次发言控制在 ${config.settings.minResponseLength}-${config.settings.maxResponseLength} 字

重要规则：
- 保持角色一致性
- 不要重复已经说过的观点
- 针对对方最新发言做出回应
- 等待主持人协调后发言`;
}

/**
 * 为主持人构建系统提示
 */
function buildModeratorPrompt(moderator, config) {
  const modeConfig = DISCUSSION_MODES[config.mode] || DISCUSSION_MODES.adversarial;

  return `你是${moderator.name}，虚拟论坛的主持人。

背景资料：
${moderator.skillContent || ''}

讨论话题：${config.topic}

你的职责：
1. 协调辩论秩序，确保每位参与者都有发言机会
2. 推动讨论深入，提出尖锐问题
3. 每轮结束后进行简要总结
4. 必要时点名提问或要求某位参与者回应

讨论模式：${modeConfig.name}
${modeConfig.instruction}

请以客观、公正但有洞察力的方式主持讨论。`;
}

/**
 * 构建发言请求消息
 */
function buildRoundMessage(round, context, config) {
  const modeConfig = DISCUSSION_MODES[config.mode] || DISCUSSION_MODES.adversarial;

  let intro = `【第${round}轮发言请求】\n\n`;
  
  if (context && context.length > 0) {
    intro += `【之前的讨论】\n`;
    // 显示最近2轮的内容摘要
    const recentRounds = context.slice(-2);
    for (const r of recentRounds) {
      intro += `\n--- 第${r.round}轮 ---\n`;
      for (const e of r.entries) {
        intro += `【${e.speaker}】：${e.content.substring(0, 150)}...\n`;
      }
    }
  } else {
    intro += `这是第一轮讨论。请介绍你的基本立场和对"${config.topic}"的初步看法。`;
  }

  intro += `\n\n请针对以上讨论，以${config.participants[0]?.name || '参与者'}的身份发表本轮正式发言。`;
  intro += `\n\n发言格式：\n【你的名字】(第${round}轮)\n[你的发言内容]`;

  return intro;
}

/**
 * 构建主持人总结请求
 */
function buildModeratorSummaryRequest(round, responses, config) {
  const responsesText = responses
    .map(r => `【${r.speaker}】：${r.content.substring(0, 200)}...`)
    .join('\n');

  return `【第${round}轮总结请求】

请主持人基于以下发言进行总结：

${responsesText}

总结要点：
1. 本轮核心观点有哪些？
2. 主要分歧是什么？
3. 下轮讨论应该聚焦哪些问题？`;
}

/**
 * 格式化辩论历史为可读输出
 */
function formatDebateOutput(debateHistory, config) {
  const lines = [];
  
  lines.push(`# 🎭 虚拟论坛：${config.topic}\n`);
  lines.push(`> **模式**：${config.mode} | **轮次**：${config.rounds}`);
  lines.push(`> **参与者**：${config.participants.map(p => p.name).join('、')}`);
  lines.push(`> **主持人**：${config.moderator?.name || '无'}\n`);
  lines.push('---\n');

  // 按轮次组织
  const rounds = {};
  for (const entry of debateHistory) {
    if (!rounds[entry.round]) {
      rounds[entry.round] = [];
    }
    rounds[entry.round].push(entry);
  }

  for (const [roundNum, entries] of Object.entries(rounds)) {
    lines.push(`\n## 第${roundNum}轮\n`);
    
    for (const entry of entries) {
      if (entry.speaker === config.moderator?.name) {
        lines.push(`### 🎙️ ${entry.speaker} 总结\n${entry.content}\n`);
      } else {
        lines.push(`### ${entry.speaker}\n${entry.content}\n`);
      }
    }
  }

  return lines.join('\n');
}

/**
 * 生成主代理协调脚本
 * 这是一个可以被主代理执行的协调任务列表
 */
function generateCoordinationTask(config, debateHistory = []) {
  const task = {
    description: `协调${config.topic}辩论（${config.rounds}轮）`,
    participants: config.participants.map(p => ({
      name: p.name,
      skillName: p.skillName,
      systemPrompt: buildSystemPrompt(p, config)
    })),
    moderator: config.moderator ? {
      name: config.moderator.name,
      skillName: config.moderator.skillName,
      systemPrompt: buildModeratorPrompt(config.moderator, config)
    } : null,
    currentRound: Math.floor(debateHistory.length / config.participants.length) + 1,
    totalRounds: config.rounds,
    nextSteps: []
  };

  // 计算下一步
  const currentRound = task.currentRound;
  
  if (currentRound <= config.rounds) {
    // 需要进行下一轮
    for (const p of config.participants) {
      task.nextSteps.push({
        type: 'spawn_and_collect',
        participant: p.name,
        round: currentRound,
        message: buildRoundMessage(currentRound, debateHistory, config)
      });
    }
    
    if (config.moderator) {
      task.nextSteps.push({
        type: 'collect_moderator_summary',
        round: currentRound,
        afterParticipants: config.participants.map(p => p.name)
      });
    }
  } else {
    task.nextSteps.push({
      type: 'end_debate',
      formatOutput: true
    });
  }

  return task;
}

// 导出所有函数
module.exports = {
  generateDebateConfig,
  buildSystemPrompt,
  buildModeratorPrompt,
  buildRoundMessage,
  buildModeratorSummaryRequest,
  formatDebateOutput,
  generateCoordinationTask
};
