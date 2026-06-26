/**
 * 虚拟论坛 - 主入口 v4.0
 * Virtual Forum Main Entry
 * 
 * v4.0 架构说明：
 * - 提供配置生成供主代理使用
 * - 主代理通过 sessions_spawn 直接控制subagent
 * - 此模块不再直接运行subagent（架构限制）
 */

const ForumEngine = require('./forum-engine.js');
const ArgumentTracker = require('./argument-tracker.js');
const OutputFormatter = require('./output-formatter.js');
const SubagentArena = require('./subagent-arena.js');
const SubagentArenaV4 = require('./subagent-arena-v4.js');
const GameTheorySubagentArena = require('./v3/game-theory-arena.js');
const BehavioralEconomicsSubagentArena = require('./v3/behavioral-arena.js');
const ContextManager = require('./context-manager.js');

class VirtualForum {
  constructor(skillsDir = null) {
    this.skillsDir = skillsDir;
    this.engine = new ForumEngine(skillsDir);
    this.tracker = new ArgumentTracker();
    this.formatter = new OutputFormatter();
    this.arena = null;
    this.currentConfig = null;
  }

  /**
   * 创建并运行论坛（模拟模式）
   */
  async createDiscussion(config) {
    const forum = await this.engine.createForum(config);
    await this.engine.runForum();
    this.trackArguments(forum);
    const output = this.formatter.format(forum, config.outputFormat || 'dialogue');
    return { forum, tracker: this.tracker, output };
  }

  /**
   * 🚀 启动标准子代理辩论模式（v2.0）
   */
  async launchArena(config) {
    const {
      topic, mode = 'adversarial', rounds = 10,
      participants = [], moderatorName = '巴菲特',
      moderatorSkill = 'warren-buffett', moderatorStyle = 'provocative',
      outputFormat = 'dialogue'
    } = config;

    this.arena = new SubagentArena(this.skillsDir);
    await this.arena.initArena({ topic, mode, rounds, participants, moderatorName, moderatorSkill, moderatorStyle });
    const result = await this.arena.runDebate();
    const output = this.arena.formatOutput(outputFormat);
    return { arena: result, output };
  }

  /**
   * 🎲 启动博弈论增强的子代理辩论模式（v3.5）
   */
  async launchGameTheoryArena(config) {
    const {
      topic, mode = 'adversarial', rounds = 10,
      participants = [], moderatorName = '巴菲特',
      moderatorSkill = 'warren-buffett', moderatorStyle = 'provocative',
      outputFormat = 'dialogue',
      discountFactors, outsideOptions, totalValue = 100,
      types, priorBeliefs, reputationTypes
    } = config;

    this.arena = new GameTheorySubagentArena(this.skillsDir);
    await this.arena.initArenaWithGameTheory({
      topic, mode, rounds, participants,
      moderatorName, moderatorSkill, moderatorStyle,
      discountFactors, outsideOptions, totalValue,
      types, priorBeliefs, reputationTypes
    });

    const result = await this.arena.runDebate();
    const output = this.arena.formatOutput(outputFormat);
    const gameTheoryReport = this.arena.getGameTheoryReport();

    return { arena: result, output, gameTheoryReport };
  }

  /**
   * 🧠 启动行为经济学增强的子代理辩论模式（v3.6.1）
   */
  async launchBehavioralEconomicsArena(config) {
    const {
      topic, mode = 'adversarial', rounds = 10,
      participants = [], moderatorName = '巴菲特',
      moderatorSkill = 'warren-buffett', moderatorStyle = 'provocative',
      outputFormat = 'dialogue',
      prospectTheory = {},
      boundedRationality = {},
      nudgeTheory = {},
      discountFactors, outsideOptions, totalValue = 100,
      types, priorBeliefs, reputationTypes
    } = config;

    this.arena = new BehavioralEconomicsSubagentArena(this.skillsDir);
    await this.arena.initArenaWithBehavioralEconomics({
      topic, mode, rounds, participants,
      moderatorName, moderatorSkill, moderatorStyle,
      discountFactors, outsideOptions, totalValue,
      types, priorBeliefs, reputationTypes,
      prospectTheory, boundedRationality, nudgeTheory
    });

    const result = await this.arena.runDebate();
    const output = this.arena.formatOutput(outputFormat);
    const behavioralReport = this.arena.generateBehavioralReport();

    return { arena: result, output, behavioralReport };
  }

  /**
   * ⚡ 快速启动子代理辩论（便捷方法）
   */
  async quickArena(topic, participantNames, options = {}) {
    const {
      mode = 'adversarial',
      rounds = 10,
      moderatorStyle = 'provocative',
      moderatorName = '巴菲特',
      moderatorSkill = 'warren-buffett',
      outputFormat = 'dialogue',
      useBehavioralEconomics = false
    } = options;

    const participants = participantNames.map(name => ({ name }));

    if (useBehavioralEconomics) {
      return this.launchBehavioralEconomicsArena({
        topic, mode, rounds, participants,
        moderatorName, moderatorSkill, moderatorStyle, outputFormat
      });
    }

    return this.launchArena({
      topic, mode, rounds, participants,
      moderatorName, moderatorSkill, moderatorStyle, outputFormat
    });
  }

  /**
   * 追踪论点
   */
  trackArguments(forum) {
    if (!forum || !forum.arguments) return;
    for (const [name, args] of Object.entries(forum.arguments)) {
      for (const arg of args) {
        this.tracker.addArgument(name, arg.text || arg.content || '', arg.type || 'statement', arg.round || 0);
      }
    }
  }

  /**
   * 🚀 启动v4.0辩论模式（配置驱动）
   * 
   * 【重要】此方法生成配置，主代理使用 sessions_spawn 执行
   * 
   * @param {Object} config - 辩论配置
   * @param {string} config.topic - 辩论话题
   * @param {number} config.rounds - 辩论轮次
   * @param {Array} config.participants - 参与者列表 [{name, skillName}]
   * @param {string} config.moderatorName - 主持人名称
   * @param {string} config.moderatorSkill - 主持人skill名
   * @param {string} config.mode - 辩论模式
   * 
   * @returns {Object} 辩论配置对象，包含协调任务
   * 
   * @example
   * // 在主代理中调用
   * const forum = new VirtualForum();
   * const config = await forum.prepareV4Debate({
   *   topic: '2026年美以伊战争',
   *   rounds: 10,
   *   participants: [
   *     {name: '特朗普', skillName: 'donald-trump-perspective'},
   *     {name: '内塔尼亚胡', skillName: 'benjamin-netanyahu-perspective'},
   *     // ...
   *   ],
   *   moderatorName: '斯塔默',
   *   moderatorSkill: 'keir-starmer-perspective'
   * });
   * // config 包含所有subagent的系统提示和协调任务
   */
  async prepareV4Debate(config) {
    this.currentConfig = await SubagentArenaV4.generateDebateConfig(config);
    
    return {
      config: this.currentConfig,
      // 生成第一轮的协调任务
      coordinationTask: SubagentArenaV4.generateCoordinationTask(this.currentConfig),
      // 格式化工具
      formatOutput: (history) => SubagentArenaV4.formatDebateOutput(history, this.currentConfig),
      // 消息构建工具
      messageBuilder: {
        buildRoundMessage: (round, history) => 
          SubagentArenaV4.buildRoundMessage(round, history, this.currentConfig),
        buildModeratorSummary: (round, responses) => 
          SubagentArenaV4.buildModeratorSummaryRequest(round, responses, this.currentConfig)
      },
      // 更新协调任务（用于下一轮）
      getNextCoordinationTask: (debateHistory) => 
        SubagentArenaV4.generateCoordinationTask(this.currentConfig, debateHistory)
    };
  }

  /**
   * launchArenaV4 - 保留向后兼容
   * 注意：由于架构限制，此方法现在返回配置而非直接运行
   */
  async launchArenaV4(config) {
    console.warn('⚠️ launchArenaV4 已改为 prepareV4Debate - 请使用新方法');
    return this.prepareV4Debate(config);
  }
}

module.exports = VirtualForum;
