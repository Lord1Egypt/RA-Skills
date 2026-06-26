/**
 * 虚拟论坛 - 核心讨论引擎
 * Virtual Forum Core Engine v3.5 (重构版)
 * 
 * 修复：
 * - [P1] 移除硬编码路径
 * - [P2] 使用 shared-config 消除重复代码
 */

const fs = require('fs');
const path = require('path');
const {
  getDefaultSkillsDir,
  DISCUSSION_MODES,
  MODERATOR_STYLES,
  VERDICT_TYPES,
  DEFAULTS,
  loadSkill,
  validateConfig
} = require('./shared-config.js');

class ForumEngine {
  constructor(skillsDir = null) {
    this.skillsDir = skillsDir || getDefaultSkillsDir();
    this.currentForum = null;
  }

  /**
   * 创建讨论
   */
  async createForum(config) {
    // 使用共享验证
    validateConfig(config);

    const {
      topic,
      mode = 'exploratory',
      rounds = DEFAULTS.rounds,
      participants = [],
      moderatorStyle = 'balanced',
      verdictType = DEFAULTS.verdictType,
      outputFormat = DEFAULTS.outputFormat
    } = config;

    this.currentForum = {
      id: Date.now(),
      topic,
      mode,
      rounds,
      participants,
      moderator: MODERATOR_STYLES[moderatorStyle] || MODERATOR_STYLES.balanced,
      verdictType,
      outputFormat,
      roundsData: [],
      arguments: {},
      scores: {},
      status: 'initialized'
    };

    // 初始化分数和论点
    for (const p of participants) {
      this.currentForum.arguments[p.name] = [];
      this.currentForum.scores[p.name] = 0;

      // 使用共享的 loadSkill 函数
      p.skillContent = loadSkill(this.skillsDir, p.skillName || p.skillPath);
    }

    this.currentForum.status = 'ready';
    return this.currentForum;
  }

  /**
   * 运行论坛（模拟模式）
   * [v3.5.2 FIX] 补全模拟模式实现
   */
  async runForum() {
    if (!this.currentForum || this.currentForum.status !== 'ready') {
      throw new Error('论坛未初始化，请先调用 createForum()');
    }

    this.currentForum.status = 'running';
    
    const { topic, mode, rounds, participants, moderator } = this.currentForum;
    const modeConfig = DISCUSSION_MODES[mode] || DISCUSSION_MODES.exploratory;
    
    console.log(`🎭 模拟论坛开始: ${topic}`);
    console.log(`  模式: ${modeConfig.name} | 轮次: ${rounds}`);
    console.log(`  参与者: ${participants.map(p => p.name).join(' vs ')}\n`);
    
    // 模拟每轮辩论
    for (let round = 1; round <= rounds; round++) {
      console.log(`--- 第 ${round}/${rounds} 轮 ---`);
      
      const roundData = {
        number: round,
        speeches: [],
        timestamp: Date.now()
      };
      
      for (const participant of participants) {
        // 生成模拟发言
        const speech = this._generateSpeech(participant, topic, mode, round);
        roundData.speeches.push(speech);
        
        // 记录论点
        this.currentForum.arguments[participant.name].push({
          text: speech.content,
          content: speech.content,
          type: 'statement',
          round: round
        });
        
        // 模拟得分
        this.currentForum.scores[participant.name] += Math.floor(Math.random() * 3) + 1;
      }
      
      this.currentForum.roundsData.push(roundData);
    }
    
    // 生成结果
    this.currentForum.result = this._generateResult();
    this.currentForum.status = 'completed';
    
    console.log(`\n✅ 模拟论坛结束`);
    return this.currentForum;
  }
  
  /**
   * 生成模拟发言
   */
  _generateSpeech(participant, topic, mode, round) {
    const templates = [
      `从${participant.name}的角度来看，${topic}这个问题需要深入分析。`,
      `${participant.name}认为，我们应该关注${topic}的长期影响。`,
      `基于${participant.name}的经验，${topic}存在以下关键点...`,
      `${participant.name}对此持保留态度，认为需要更多数据支持。`
    ];
    
    const content = templates[Math.floor(Math.random() * templates.length)] +
      ` [第${round}轮模拟发言]`;
    
    return {
      speaker: participant.name,
      content: content,
      timestamp: Date.now()
    };
  }
  
  /**
   * 生成讨论结果
   */
  _generateResult() {
    const entries = Object.entries(this.currentForum.scores);
    entries.sort((a, b) => b[1] - a[1]);
    
    return {
      winner: entries.length > 0 ? entries[0][0] : null,
      scores: this.currentForum.scores,
      summary: `模拟讨论完成，共${this.currentForum.rounds}轮，${entries.length}位参与者`,
      totalArguments: Object.values(this.currentForum.arguments).reduce((sum, args) => sum + args.length, 0)
    };
  }
}

module.exports = ForumEngine;
