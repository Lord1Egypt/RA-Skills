/**
 * 重复博弈与声誉模型
 * Repeated Games & Reputation
 * 
 * 基于 Osborne 第8章 / Kreps-Wilson (1982) 声誉模型
 * 
 * 核心概念：
 * - 阶段博弈 G
 * - 重复次数: T (有限) 或 ∞ (无限)
 * - 折现因子: δ
 * - 历史: h^t = (a^1, a^2, ..., a^t)
 * - 策略: s_i: H^t → A_i (基于历史的映射)
 
 * 民间定理 (Folk Theorem): 
 * 当 δ → 1 时，任何可行的、个体理性的收益都可以是SPNE
 */

class RepeatedGameAnalyzer {
  constructor(config) {
    this.stageGame = config.stageGame; // 阶段博弈
    this.players = config.players;
    this.discountFactor = config.discountFactor || 0.9; // δ
    this.horizon = config.horizon || Infinity; // 重复次数
    this.reputationTypes = config.reputationTypes || {}; // 声誉类型
  }

  /**
   * 无限重复博弈分析
   * 
   * 触发策略: 
   * - 合作直到对方背叛，然后永远背叛 (冷酷触发 Grim Trigger)
   * - 合作直到对方背叛，然后惩罚 N 轮 (Tit-for-Tat 变体)
   */
  analyzeInfiniteRepeatedGame() {
    const analysis = {
      type: 'Infinite Horizon Repeated Game',
      
      // 阶段博弈均衡
      stageGameEquilibria: this.findStageGameEquilibria(),
      
      // 触发策略分析
      triggerStrategies: this.analyzeTriggerStrategies(),
      
      // 民间定理
      folkTheorem: this.verifyFolkTheorem(),
      
      // 最优策略
      optimalStrategies: this.calculateOptimalStrategies()
    };
    
    return analysis;
  }

  /**
   * 分析触发策略
   */
  analyzeTriggerStrategies() {
    const strategies = {
      grimTrigger: {
        name: 'Grim Trigger (冷酷触发)',
        description: '一旦对方背叛，永远背叛',
        phases: ['合作', '惩罚'],
        
        // 合作条件
        cooperationCondition: this.checkGrimTriggerCooperation(),
        
        // 收益计算
        payoffs: this.calculateGrimTriggerPayoffs(),
        
        // 稳健性
        robustness: '对错误敏感，一旦触发惩罚无法恢复'
      },
      
      titForTat: {
        name: 'Tit-for-Tat (以牙还牙)',
        description: '上一轮对方怎么做，这一轮就怎么做',
        phases: ['模仿上一轮'],
        
        cooperationCondition: this.checkTitForTatCooperation(),
        payoffs: this.calculateTitForTatPayoffs(),
        robustness: '对错误有一定容忍度，可以快速恢复合作'
      },
      
      limitedPunishment: {
        name: 'Limited Punishment (有限惩罚)',
        description: '背叛后惩罚N轮，然后恢复合作',
        punishmentLength: 3, // 惩罚长度
        
        cooperationCondition: this.checkLimitedPunishmentCooperation(3),
        payoffs: this.calculateLimitedPunishmentPayoffs(3),
        robustness: '平衡了惩罚力度和恢复能力'
      }
    };
    
    return strategies;
  }

  /**
   * 验证冷酷触发的合作条件
   * 
   * 正确的合作条件 (Osborne 第8章):
   * R ≥ (1-δ)*T + δ*P
   * 
   * 即: δ ≥ (T-R)/(T-P)
   * 
   * 其中:
   * R = 相互合作收益 (Reward)
   * T = 背叛诱惑 (Temptation) 
   * P = 相互背叛收益 (Punishment)
   * S = 被背叛收益 (Sucker) - 未使用但重要
   */
  checkGrimTriggerCooperation() {
    // 囚徒困境收益 (T>R>P>S)
    const R = 3;  // Reward: 相互合作
    const T = 5;  // Temptation: 背叛而对方合作
    const P = 1;  // Punishment: 相互背叛
    const S = 0;  // Sucker: 合作而对方背叛
    
    const delta = this.discountFactor;
    
    // 正确的阈值: δ ≥ (T-R)/(T-P)
    const threshold = (T - R) / (T - P);
    
    // 也可以使用更完整的公式考虑S:
    // 完整条件: R/(1-δ) ≥ T + δ*P/(1-δ)  →  δ ≥ (T-R)/(T-P)
    const condition = delta >= threshold;
    
    // 计算合作vs背叛的净现值差异
    const cooperationNPV = R / (1 - delta);
    const defectionNPV = T + delta * P / (1 - delta);
    const netBenefit = cooperationNPV - defectionNPV;
    
    return {
      condition,
      threshold: threshold.toFixed(4),
      currentDelta: delta,
      explanation: condition 
        ? `δ=${delta.toFixed(4)} ≥ ${threshold.toFixed(4)}: 冷酷触发可以维持合作。合作净收益=${netBenefit.toFixed(2)}`
        : `δ=${delta.toFixed(4)} < ${threshold.toFixed(4)}: 背叛诱惑太大，合作不可维持`,
      
      // 详细分解
      detail: {
        cooperationNPV: cooperationNPV.toFixed(2),
        defectionNPV: defectionNPV.toFixed(2),
        netBenefit: netBenefit.toFixed(2),
        requiredDelta: threshold.toFixed(4)
      }
    };
  }

  /**
   * Kreps-Wilson 声誉模型
   * 
   * 解决连锁店悖论：引入不完全信息
   */
  analyzeReputationModel(player, stages) {
    const analysis = {
      model: 'Kreps-Wilson Reputation',
      player,
      
      // 类型空间
      types: {
        rational: {
          prior: 1 - (this.reputationTypes[player]?.crazyProbability || 0.1),
          behavior: '最大化长期收益'
        },
        crazy: {
          prior: this.reputationTypes[player]?.crazyProbability || 0.1,
          behavior: '总是强硬/总是对抗'
        }
      },
      
      // 声誉建立
      reputationBuilding: [],
      
      // 均衡路径
      equilibriumPath: []
    };
    
    // 模拟多阶段
    let currentReputation = analysis.types.crazy.prior;
    
    for (let stage = 0; stage < stages; stage++) {
      // 理性类型模仿疯狂类型的概率
      const imitationProbability = this.calculateImitationProbability(
        stage,
        stages,
        currentReputation
      );
      
      // 观察到的行动
      const observedAction = Math.random() < imitationProbability 
        ? 'tough'  // 理性类型选择模仿
        : 'soft';  // 理性类型暴露真实偏好
      
      // 信念更新
      const updatedReputation = this.updateReputation(
        currentReputation,
        observedAction,
        imitationProbability
      );
      
      analysis.reputationBuilding.push({
        stage,
        priorReputation: currentReputation,
        imitationProbability,
        observedAction,
        posteriorReputation: updatedReputation,
        explanation: observedAction === 'tough' 
          ? '强硬行为提升了强硬声誉'
          : '软弱行为降低了强硬声誉'
      });
      
      currentReputation = updatedReputation;
    }
    
    // 总结
    analysis.finalReputation = currentReputation;
    analysis.reputationValue = this.calculateReputationValue(analysis.reputationBuilding);
    
    return analysis;
  }

  /**
   * 计算模仿概率
   * 
   * 理性类型决定是否模仿疯狂类型
   */
  calculateImitationProbability(stage, totalStages, currentReputation) {
    const remainingStages = totalStages - stage;
    
    // 早期阶段：更倾向于模仿（建立声誉）
    // 后期阶段：更倾向于暴露（收割声誉）
    
    if (remainingStages > totalStages * 0.6) {
      // 建立期：高模仿概率
      return 0.8;
    } else if (remainingStages > totalStages * 0.2) {
      // 过渡期：中等模仿概率
      return 0.5;
    } else {
      // 收割期：低模仿概率
      return 0.2;
    }
  }

  /**
   * 更新声誉（贝叶斯更新）
   */
  updateReputation(priorReputation, observedAction, imitationProb) {
    if (observedAction === 'tough') {
      // 观察到强硬行为
      // P(crazy|tough) ∝ P(tough|crazy) * P(crazy)
      const likelihoodCrazy = 1.0; // 疯狂类型总是强硬
      const likelihoodRational = imitationProb; // 理性类型以概率模仿
      
      const numerator = likelihoodCrazy * priorReputation;
      const denominator = numerator + likelihoodRational * (1 - priorReputation);
      
      return denominator > 0 ? numerator / denominator : priorReputation;
    } else {
      // 观察到软弱行为 → 一定是理性类型
      return 0;
    }
  }

  /**
   * 计算声誉价值
   */
  calculateReputationValue(reputationHistory) {
    const delta = this.discountFactor;
    let value = 0;
    
    for (let i = 0; i < reputationHistory.length; i++) {
      const stage = reputationHistory[i];
      const reputationBenefit = stage.posteriorReputation * 2; // 假设声誉带来2单位收益
      value += Math.pow(delta, i) * reputationBenefit;
    }
    
    return value;
  }

  /**
   * 模拟长期关系
   * 
   * 追踪声誉、合作/背叛历史
   */
  simulateLongTermRelationship(stages, strategies) {
    const simulation = {
      stages: [],
      cooperationRate: 0,
      betrayalEvents: [],
      trustEvolution: []
    };
    
    let trustLevel = 0.5; // 初始信任水平
    
    for (let stage = 0; stage < stages; stage++) {
      // 根据信任水平选择行动
      const player1Action = this.chooseAction(strategies.player1, trustLevel);
      const player2Action = this.chooseAction(strategies.player2, trustLevel);
      
      // 更新信任
      if (player1Action === 'cooperate' && player2Action === 'cooperate') {
        trustLevel = Math.min(1, trustLevel + 0.1);
      } else if (player1Action === 'defect' || player2Action === 'defect') {
        trustLevel = Math.max(0, trustLevel - 0.3);
        simulation.betrayalEvents.push({ stage, betrayer: player1Action === 'defect' ? 'player1' : 'player2' });
      }
      
      simulation.stages.push({
        stage,
        actions: { player1: player1Action, player2: player2Action },
        trustLevel,
        outcome: this.calculateStageOutcome(player1Action, player2Action)
      });
      
      simulation.trustEvolution.push(trustLevel);
    }
    
    // 统计
    const cooperations = simulation.stages.filter(s => 
      s.actions.player1 === 'cooperate' && s.actions.player2 === 'cooperate'
    ).length;
    simulation.cooperationRate = cooperations / stages;
    
    return simulation;
  }

  /**
   * 民间定理验证
   * 
   * 识别可行的、个体理性的收益集合
   */
  verifyFolkTheorem() {
    // 可行性：凸包
    const feasibleSet = this.calculateFeasibleSet();
    
    // 个体理性：不低于最小最大收益
    const individualRationality = this.calculateMinmaxPayoffs();
    
    // 民间定理区域
    const folkTheoremRegion = feasibleSet.filter(payoff => 
      this.players.every(p => payoff[p] >= individualRationality[p])
    );
    
    return {
      feasibleSet,
      individualRationality,
      folkTheoremRegion,
      
      explanation: `当折现因子δ→1时，民间定理区域内的任何收益组合都可以通过某个SPNE实现`,
      
      cooperationPossibility: folkTheoremRegion.some(p => 
        p[this.players[0]] > individualRationality[this.players[0]] &&
        p[this.players[1]] > individualRationality[this.players[1]]
      )
    };
  }

  /**
   * 为辩论生成声誉策略建议
   */
  generateReputationStrategyAdvice(player, currentStage, totalStages, currentReputation) {
    const remainingStages = totalStages - currentStage;
    const advice = {
      player,
      currentStage,
      currentReputation,
      
      phase: this.identifyReputationPhase(currentStage, totalStages),
      
      recommendedAction: null,
      
      reasoning: null,
      
      futureValue: null
    };
    
    if (remainingStages > totalStages * 0.6) {
      // 声誉建立期
      advice.phase = '声誉建立期';
      advice.recommendedAction = 'tough';
      advice.reasoning = '早期投资声誉，让对手相信你是强硬类型';
      advice.futureValue = '后期可以利用声誉获得更好交易条件';
    } else if (remainingStages > totalStages * 0.2) {
      // 声誉维持期
      advice.phase = '声誉维持期';
      advice.recommendedAction = currentReputation > 0.3 ? 'tough' : 'soft';
      advice.reasoning = currentReputation > 0.3 
        ? '维持已建立的强硬声誉'
        : '声誉已不足，考虑暴露真实类型';
    } else {
      // 声誉收割期
      advice.phase = '声誉收割期';
      advice.recommendedAction = 'soft';
      advice.reasoning = '关系即将结束，收割声誉带来的收益';
    }
    
    return advice;
  }

  identifyReputationPhase(stage, total) {
    if (stage < total * 0.4) return 'building';
    if (stage < total * 0.8) return 'maintaining';
    return 'harvesting';
  }

  // 辅助方法...
  findStageGameEquilibria() {
    return []; // 简化
  }

  calculateFeasibleSet() {
    return []; // 简化
  }

  calculateMinmaxPayoffs() {
    return {}; // 简化
  }

  chooseAction(strategy, trustLevel) {
    return trustLevel > 0.5 ? 'cooperate' : 'defect';
  }

  calculateStageOutcome(a1, a2) {
    if (a1 === 'cooperate' && a2 === 'cooperate') return [3, 3];
    if (a1 === 'cooperate' && a2 === 'defect') return [0, 5];
    if (a1 === 'defect' && a2 === 'cooperate') return [5, 0];
    return [1, 1];
  }
}

module.exports = RepeatedGameAnalyzer;
