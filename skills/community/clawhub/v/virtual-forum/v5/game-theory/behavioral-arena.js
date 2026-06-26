/**
 * 行为经济学增强的子代理竞技场
 * Behavioral Economics Enhanced Subagent Arena (v3.6)
 * 
 * 在v3.5博弈论基础上集成行为经济学三大理论：
 * - 前景理论 (Prospect Theory)
 * - 有限理性 (Bounded Rationality)  
 * - 助推理论 (Nudge Theory)
 */

const GameTheorySubagentArena = require('./game-theory-arena');
const { BehavioralEconomicsArena } = require('./behavioral');

class BehavioralEconomicsSubagentArena extends GameTheorySubagentArena {
  constructor(skillsDir = null) {
    super(skillsDir);
    this.beArena = new BehavioralEconomicsArena();
    this.behavioralContext = null;
    this.roundInsights = [];
    this.strategyAdvice = {};  // [FIX] 初始化未定义的strategyAdvice
  }

  /**
   * [FIX] 基础博弈论分析 - 需要实现或由子类覆盖
   * 用于 analyzeRoundWithBehavioral() 方法
   */
  async analyzeRound(roundNumber, roundData) {
    // 基础实现：返回空分析结果
    // 子类可覆盖以提供具体的博弈论分析
    return {
      round: roundNumber,
      gameType: 'mixed_strategy',
      equilibrium: null,
      riskLevel: 0.5,
      recommendations: []
    };
  }

  /**
   * [FIX] 生成报告 - 需要实现或由子类覆盖
   * 用于 generateBehavioralReport() 方法
   */
  generateReport() {
    // 基础实现：返回当前arena的基本报告
    // 子类可覆盖以提供更详细的博弈论报告
    const debateHistory = this.arena?.debateHistory || [];
    const participantScores = this.arena?.scores || {};
    
    return {
      id: this.arena?.id || Date.now(),
      topic: this.arena?.topic || 'Unknown',
      mode: this.arena?.mode || 'adversarial',
      rounds: this.arena?.rounds || 0,
      participants: (this.arena?.participants || []).map(p => p.name),
      totalRounds: debateHistory.length,
      scores: participantScores,
      debateHistory: debateHistory.slice(-10),  // 最近10轮
      summary: this._generateBasicSummary(debateHistory),
      recommendations: []
    };
  }

  /**
   * 生成基本摘要
   */
  _generateBasicSummary(debateHistory) {
    if (!debateHistory || debateHistory.length === 0) {
      return '无讨论记录';
    }
    const speakers = [...new Set(debateHistory.map(h => h.speaker))];
    return `${speakers.length}位参与者进行了${debateHistory.length}轮讨论`;
  }

  /**
   * 初始化行为经济学增强竞技场 (v3.6)
   */
  async initArenaWithBehavioralEconomics(config) {
    // 1. 先初始化博弈论竞技场 (v3.5)
    await this.initArenaWithGameTheory(config);
    
    // 2. 运行行为经济学分析
    console.log('🧠 运行行为经济学分析...');
    
    this.behavioralContext = await this.beArena.initBehavioralDebate(
      config.topic,
      config.participants,
      {
        prospectTheory: config.prospectTheory,
        boundedRationality: config.boundedRationality,
        nudgeTheory: config.nudgeTheory
      }
    );
    
    console.log('✓ 行为经济学分析完成');
    console.log(`  检测到的行为特征: ${this.behavioralContext.topicAnalysis.features.join(', ')}`);
    
    // 3. 生成行为策略建议
    await this.generateBehavioralAdviceForAll(config.participants);
    
    return this.arena;
  }

  /**
   * 生成所有参与者的行为经济学建议
   */
  async generateBehavioralAdviceForAll(participants) {
    for (const p of participants) {
      const advice = this.beArena.generateBehavioralAdvice(p.name, {
        position: p.position,
        opponentPosition: participants.find(op => op.name !== p.name)?.position,
        topic: this.arena.topic,
        complexity: 0.6,
        timePressure: 0.4,
        audienceProfile: { riskAverse: true, socialConscious: true }
      });
      
      // [FIX] 安全地初始化strategyAdvice
      if (!this.strategyAdvice[p.name]) {
        this.strategyAdvice[p.name] = {};
      }
      this.strategyAdvice[p.name] = {
        ...this.strategyAdvice[p.name],
        behavioral: advice
      };
    }
  }

  /**
   * 分析回合 - 增加行为经济学维度
   */
  async analyzeRoundWithBehavioral(roundNumber, roundData) {
    // 1. 基础博弈论分析
    const gtAnalysis = await this.analyzeRound(roundNumber, roundData);
    
    // 2. 行为经济学分析
    const behavioralInsights = this.beArena.analyzeRoundBehavior(roundData);
    
    // 3. 整合分析
    const integratedAnalysis = {
      round: roundNumber,
      gameTheory: gtAnalysis,
      behavioral: {
        insights: behavioralInsights,
        byAgent: this._groupByAgent(behavioralInsights),
        recommendations: this._generateBehavioralRecommendations(behavioralInsights)
      },
      combined: this._integrateGTandBE(gtAnalysis, behavioralInsights)
    };
    
    this.roundInsights.push(integratedAnalysis);
    return integratedAnalysis;
  }

  /**
   * 生成回合策略建议 - 行为经济学增强
   */
  generateRoundStrategyAdvice(agentName, roundContext) {
    // 获取博弈论建议
    const gtAdvice = this.strategyAdvice[agentName];
    
    // 获取行为经济学建议
    const beAdvice = this.beArena.generateBehavioralAdvice(agentName, {
      position: roundContext.position,
      opponentPosition: roundContext.opponentPosition,
      topic: this.arena.topic,
      complexity: roundContext.complexity,
      timePressure: roundContext.timePressure,
      audienceProfile: roundContext.audienceProfile
    });

    return {
      agent: agentName,
      round: roundContext.round,
      gameTheory: gtAdvice,
      behavioral: beAdvice,
      integrated: this._synthesizeAdvice(gtAdvice, beAdvice)
    };
  }

  /**
   * 生成最终报告 - 包含行为经济学总结
   */
  generateBehavioralReport() {
    const gtReport = this.generateReport();
    const beSummary = this.beArena.generateBehavioralSummary();
    
    return {
      ...gtReport,
      behavioralEconomics: {
        summary: beSummary,
        participantProfiles: this.behavioralContext.participantProfiles,
        keyInsights: this._extractKeyBehavioralInsights(),
        theoryApplications: {
          prospectTheory: this._summarizeProspectTheoryApps(),
          boundedRationality: this._summarizeBoundedRationalityApps(),
          nudgeTheory: this._summarizeNudgeTheoryApps()
        }
      },
      recommendations: {
        gameTheory: gtReport.recommendations,
        behavioral: this._generateBehavioralRecommendationsList()
      }
    };
  }

  // 私有辅助方法
  _groupByAgent(insights) {
    const grouped = {};
    insights.forEach(i => {
      if (!grouped[i.agent]) grouped[i.agent] = [];
      grouped[i.agent].push(i);
    });
    return grouped;
  }

  _generateBehavioralRecommendations(insights) {
    const recommendations = [];
    
    // 按理论分组建议
    const byTheory = {
      prospect_theory: insights.filter(i => i.theory === 'prospect_theory'),
      bounded_rationality: insights.filter(i => i.theory === 'bounded_rationality'),
      nudge_theory: insights.filter(i => i.theory === 'nudge_theory')
    };

    if (byTheory.prospect_theory.length > 0) {
      recommendations.push({
        category: '前景理论',
        advice: '注意参照点设置和框架效应，利用损失厌恶增强说服力'
      });
    }

    if (byTheory.bounded_rationality.length > 0) {
      recommendations.push({
        category: '有限理性',
        advice: '简化论证结构，减少认知负荷，使用启发式增强可理解性'
      });
    }

    if (byTheory.nudge_theory.length > 0) {
      recommendations.push({
        category: '助推理论',
        advice: '设计选择架构，利用默认选项和社会规范，但避免操纵性修辞'
      });
    }

    return recommendations;
  }

  _integrateGTandBE(gtAnalysis, beInsights) {
    return {
      strategicPosition: gtAnalysis.equilibrium,
      behavioralBiases: beInsights.filter(i => i.biases).length,
      recommendedApproach: this._synthesizeApproach(gtAnalysis, beInsights),
      riskAssessment: this._assessRiskWithBE(gtAnalysis, beInsights)
    };
  }

  _synthesizeApproach(gt, be) {
    // 综合博弈论和行为经济学的建议
    const hasLossAversion = be.some(i => 
      i.features?.includes('loss_aversion')
    );
    
    const isZeroSum = gt.gameType === 'zero_sum';
    
    if (hasLossAversion && isZeroSum) {
      return '利用对方的损失厌恶，将博弈框架为损失避免情境';
    } else if (hasLossAversion) {
      return '强调合作失败的机会成本';
    } else {
      return '基于博弈论均衡选择最优策略';
    }
  }

  _assessRiskWithBE(gt, be) {
    const baseRisk = gt.riskLevel || 0.5;
    
    // 考虑行为偏差对风险判断的影响
    const overconfidence = be.some(i => 
      i.biases?.some(b => b.type === 'confirmation_bias')
    );
    
    const availabilityBias = be.some(i =>
      i.biases?.some(b => b.type === 'availability_bias')
    );

    return {
      baseRisk,
      adjustedRisk: baseRisk * (overconfidence ? 1.2 : 1) * (availabilityBias ? 0.9 : 1),
      factors: {
        overconfidence,
        availabilityBias
      }
    };
  }

  _synthesizeAdvice(gt, be) {
    return {
      primaryStrategy: this._determinePrimaryStrategy(gt, be),
      framing: this._determineFraming(gt, be),
      tactics: this._combineTactics(gt, be)
    };
  }

  _determinePrimaryStrategy(gt, be) {
    // 根据博弈类型和行为特征确定主要策略
    if (be?.behavioral?.recommendations?.[0]?.strategies?.length > 0) {
      return be.behavioral.recommendations[0].strategies[0].tactic;
    }
    return gt?.primaryStrategy || '均衡策略';
  }

  _determineFraming(gt, be) {
    // 确定最优框架
    const hasLossAversion = be?.behavioral?.recommendations?.some(
      r => r.strategies?.some(s => s.tactic === 'loss_frame')
    );
    return hasLossAversion ? '损失框架' : '收益框架';
  }

  _combineTactics(gt, be) {
    const tactics = [];
    
    // 博弈论战术
    if (gt?.tactics) tactics.push(...gt.tactics);
    
    // 行为经济学战术
    be?.behavioral?.recommendations?.forEach(r => {
      if (r.strategies) {
        tactics.push(...r.strategies.map(s => ({
          source: 'behavioral',
          tactic: s.tactic,
          description: s.description
        })));
      }
    });
    
    return tactics;
  }

  _extractKeyBehavioralInsights() {
    const allInsights = this.roundInsights.flatMap(r => r.behavioral.insights);
    
    // 统计最常见的洞察
    const insightTypes = {};
    allInsights.forEach(i => {
      const key = `${i.theory}_${i.features?.[0] || i.biases?.[0]?.type || 'general'}`;
      insightTypes[key] = (insightTypes[key] || 0) + 1;
    });
    
    return Object.entries(insightTypes)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([type, count]) => ({ type, count }));
  }

  _summarizeProspectTheoryApps() {
    return this.roundInsights.flatMap(r => 
      r.behavioral.insights
        .filter(i => i.theory === 'prospect_theory')
        .map(i => ({
          agent: i.agent,
          features: i.features,
          recommendation: i.recommendation
        }))
    );
  }

  _summarizeBoundedRationalityApps() {
    return this.roundInsights.flatMap(r => 
      r.behavioral.insights
        .filter(i => i.theory === 'bounded_rationality')
        .map(i => ({
          agent: i.agent,
          biases: i.biases,
          recommendation: i.recommendation
        }))
    );
  }

  _summarizeNudgeTheoryApps() {
    return this.roundInsights.flatMap(r => 
      r.behavioral.insights
        .filter(i => i.theory === 'nudge_theory')
        .map(i => ({
          agent: i.agent,
          darkPatterns: i.darkPatterns,
          recommendation: i.recommendation
        }))
    );
  }

  _generateBehavioralRecommendationsList() {
    const summary = this.beArena.generateBehavioralSummary();
    
    return [
      {
        category: '偏差纠正',
        items: summary.keyRecommendations.map(r => ({
          bias: r.bias,
          mitigation: r.mitigation
        }))
      },
      {
        category: '策略优化',
        items: [
          '利用前景理论的损失框架增强说服力',
          '考虑有限理性，简化复杂论证',
          '设计选择架构引导有利决策',
          '警惕并对抗操纵性助推'
        ]
      }
    ];
  }
}

module.exports = { BehavioralEconomicsSubagentArena };
