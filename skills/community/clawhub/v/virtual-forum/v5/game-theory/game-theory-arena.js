/**
 * 虚拟论坛 - 博弈论增强子代理竞技场
 * Game Theory Enhanced Subagent Arena v3.5
 * 
 * [P0 FIX] 补全 index.js 中引用但缺失的文件
 * 
 * 博弈论在辩论中的作用：
 * - discountFactor: 影响参与者的耐心程度（越低越急于达成共识）
 * - outsideOption: 参与者的 BATNA（最佳替代方案），影响让步意愿
 * - reputationType: 影响其他参与者对其策略的预判
 * - priorBeliefs: 贝叶斯更新，根据对方行为更新对其类型的判断
 */

const SubagentArena = require('../subagent-arena.js');
const { DEFAULTS } = require('../shared-config.js');

class GameTheorySubagentArena extends SubagentArena {
  constructor(skillsDir = null) {
    super(skillsDir);
    this.gameState = null;
  }

  /**
   * 初始化博弈论增强的竞技场
   */
  async initArenaWithGameTheory(config) {
    // 先执行基础初始化
    await this.initArena(config);

    const gtDefaults = DEFAULTS.gameTheory;
    const {
      discountFactors = {},
      outsideOptions = {},
      totalValue = gtDefaults.totalValue,
      types = {},
      priorBeliefs = {},
      reputationTypes = {}
    } = config;

    // 初始化博弈论状态
    this.gameState = {
      totalValue,
      round: 0,
      participants: {}
    };

    for (const p of this.arena.participants) {
      this.gameState.participants[p.name] = {
        discountFactor: discountFactors[p.name] || gtDefaults.defaultDiscountFactor,
        outsideOption: outsideOptions[p.name] || gtDefaults.defaultOutsideOption,
        type: types[p.name] || 'unknown',
        reputationType: reputationTypes[p.name] || gtDefaults.defaultReputationType,
        beliefs: priorBeliefs[p.name] || {},
        concessions: [],
        currentOffer: null,
        utility: 0
      };
    }

    console.log('🎲 博弈论参数已初始化:');
    for (const [name, state] of Object.entries(this.gameState.participants)) {
      console.log(` ${name}: δ=${state.discountFactor}, BATNA=${state.outsideOption}, 声誉=${state.reputationType}`);
    }

    return this.arena;
  }

  /**
   * 计算参与者在当前轮次的折扣效用
   * U_i(t) = δ^t * value - outsideOption
   */
  calculateDiscountedUtility(participantName, value) {
    const state = this.gameState.participants[participantName];
    if (!state) return 0;

    const discounted = Math.pow(state.discountFactor, this.gameState.round) * value;
    return Math.max(discounted, state.outsideOption);
  }

  /**
   * 判断参与者是否应该让步
   * 当折扣效用接近外部选项时，倾向让步
   */
  shouldConcede(participantName) {
    const state = this.gameState.participants[participantName];
    if (!state) return false;

    const currentUtility = this.calculateDiscountedUtility(
      participantName,
      this.gameState.totalValue / Object.keys(this.gameState.participants).length
    );

    // 当效用低于外部选项的 1.2 倍时，倾向让步
    return currentUtility < state.outsideOption * 1.2;
  }

  /**
   * 贝叶斯更新：根据对方行为更新信念
   */
  updateBeliefs(observerName, targetName, observedAction) {
    const observer = this.gameState.participants[observerName];
    if (!observer || !observer.beliefs[targetName]) return;

    const beliefs = observer.beliefs[targetName];

    // 简化的贝叶斯更新
    if (observedAction === 'aggressive') {
      beliefs.hardliner = Math.min(0.95, (beliefs.hardliner || 0.5) * 1.3);
      beliefs.cooperative = Math.max(0.05, (beliefs.cooperative || 0.5) * 0.7);
    } else if (observedAction === 'concede') {
      beliefs.hardliner = Math.max(0.05, (beliefs.hardliner || 0.5) * 0.7);
      beliefs.cooperative = Math.min(0.95, (beliefs.cooperative || 0.5) * 1.3);
    }

    // 归一化
    const total = Object.values(beliefs).reduce((s, v) => s + v, 0);
    if (total > 0) {
      for (const key of Object.keys(beliefs)) {
        beliefs[key] /= total;
      }
    }
  }

  /**
   * 构建博弈论增强的系统提示
   * 在基础提示上附加博弈论策略指导
   */
  buildDebaterSystemPrompt(participant) {
    const basePrompt = super.buildDebaterSystemPrompt(participant);
    const state = this.gameState?.participants[participant.name];

    if (!state) return basePrompt;

    const shouldConcede = this.shouldConcede(participant.name);
    const utility = this.calculateDiscountedUtility(
      participant.name,
      this.gameState.totalValue / Object.keys(this.gameState.participants).length
    );

    let strategyHint = '';
    if (shouldConcede) {
      strategyHint = `
【策略提示】当前局势对你不利（效用=${utility.toFixed(1)}，接近你的底线=${state.outsideOption}）。
你可以考虑：
- 做出有条件的让步
- 提出折中方案
- 强调共同利益`;
    } else {
      strategyHint = `
【策略提示】当前局势对你有利（效用=${utility.toFixed(1)}，远高于底线=${state.outsideOption}）。
你可以考虑：
- 坚持核心立场
- 提出更高要求
- 用数据和案例强化论点`;
    }

    return basePrompt + '\n' + strategyHint;
  }

  /**
   * 重写 runDebate，在每轮后更新博弈状态
   */
  async runDebate() {
    if (!this.gameState) {
      throw new Error('博弈论状态未初始化，请先调用 initArenaWithGameTheory()');
    }

    // 保存原始的 onRoundComplete
    const originalCallback = this.onRoundComplete;

    this.onRoundComplete = (round, speeches) => {
      // 更新博弈轮次
      this.gameState.round = round;

      // 分析发言行为并更新信念
      for (const speech of speeches) {
        const action = this.classifyAction(speech.content);
        for (const otherName of Object.keys(this.gameState.participants)) {
          if (otherName !== speech.speaker) {
            this.updateBeliefs(otherName, speech.speaker, action);
          }
        }
      }

      // 调用原始回调
      if (typeof originalCallback === 'function') {
        originalCallback(round, speeches);
      }
    };

    return await super.runDebate();
  }

  /**
   * 简单分类发言行为
   * @param {string} content - 发言内容
   * @returns {string} 'aggressive' | 'concede' | 'neutral'
   */
  classifyAction(content) {
    if (!content) return 'neutral';

    const aggressiveKeywords = ['反对', '错误', '不可能', '荒谬', '完全不同意', '必须', '绝对'];
    const concedeKeywords = ['同意', '有道理', '让步', '折中', '妥协', '可以接受', '共同点'];

    const aggressiveCount = aggressiveKeywords.filter(k => content.includes(k)).length;
    const concedeCount = concedeKeywords.filter(k => content.includes(k)).length;

    if (aggressiveCount > concedeCount) return 'aggressive';
    if (concedeCount > aggressiveCount) return 'concede';
    return 'neutral';
  }

  /**
   * 获取博弈论状态报告
   */
  getGameTheoryReport() {
    if (!this.gameState) return '博弈论状态未初始化';

    let report = '🎲 博弈论状态报告\n';
    report += `═══════════════════════\n`;
    report += `总价值池: ${this.gameState.totalValue}\n`;
    report += `当前轮次: ${this.gameState.round}\n\n`;

    for (const [name, state] of Object.entries(this.gameState.participants)) {
      const utility = this.calculateDiscountedUtility(
        name, this.gameState.totalValue / Object.keys(this.gameState.participants).length
      );
      report += `【${name}】\n`;
      report += ` 折扣因子: ${state.discountFactor}\n`;
      report += ` 外部选项(BATNA): ${state.outsideOption}\n`;
      report += ` 当前效用: ${utility.toFixed(1)}\n`;
      report += ` 声誉类型: ${state.reputationType}\n`;
      report += ` 应该让步: ${this.shouldConcede(name) ? '是 ⚠️' : '否'}\n`;
      if (Object.keys(state.beliefs).length > 0) {
        report += ` 信念: ${JSON.stringify(state.beliefs)}\n`;
      }
      report += `\n`;
    }

    return report;
  }
}

module.exports = GameTheorySubagentArena;
