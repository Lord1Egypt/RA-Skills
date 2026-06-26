/**
 * 行为经济学集成模块 (Behavioral Economics Integration)
 * 整合前景理论、有限理性、助推理论到虚拟论坛
 * v3.6 - Behavioral Economics Enhanced
 */

const { ProspectTheoryEngine } = require('./prospect-theory');
const { BoundedRationalityEngine } = require('./bounded-rationality');
const { NudgeTheoryEngine } = require('./nudge-theory');

class BehavioralEconomicsArena {
  constructor(config = {}) {
    this.prospectTheory = new ProspectTheoryEngine(config.prospectTheory);
    this.boundedRationality = new BoundedRationalityEngine(config.boundedRationality);
    this.nudgeTheory = new NudgeTheoryEngine(config.nudgeTheory);
    
    this.debateHistory = [];
    this.agentProfiles = new Map();
    this.behavioralInsights = [];
  }

  /**
   * 初始化行为经济学增强的辩论
   */
  async initBehavioralDebate(topic, participants, config = {}) {
    console.log('🧠 初始化行为经济学分析...');
    
    // 为每个参与者创建行为档案
    for (const participant of participants) {
      this.agentProfiles.set(participant.name, {
        ...participant,
        riskProfile: this._inferRiskProfile(participant),
        cognitiveStyle: this._inferCognitiveStyle(participant),
        biases: [],
        nudgesApplied: [],
        prospectValue: 0
      });
    }

    // 分析议题的行为经济学特征
    const topicAnalysis = this._analyzeTopicBehavioralFeatures(topic);
    
    // 生成行为策略建议
    const behavioralStrategies = this._generateBehavioralStrategies(topic, participants);

    console.log('✓ 行为经济学分析完成');
    console.log(`  检测到的行为特征: ${topicAnalysis.features.join(', ')}`);
    
    return {
      topic,
      topicAnalysis,
      participantProfiles: Array.from(this.agentProfiles.values()),
      behavioralStrategies,
      tools: ['prospect_theory', 'bounded_rationality', 'nudge_theory']
    };
  }

  /**
   * 分析回合中的行为偏差
   */
  analyzeRoundBehavior(roundData) {
    const insights = [];
    
    for (const argument of roundData.arguments) {
      const agent = this.agentProfiles.get(argument.agent);
      if (!agent) continue;

      // 1. 前景理论分析
      const prospectAnalysis = this._analyzeProspectFeatures(argument);
      if (prospectAnalysis.hasFeatures) {
        insights.push({
          agent: argument.agent,
          theory: 'prospect_theory',
          features: prospectAnalysis.features,
          recommendation: prospectAnalysis.recommendation
        });
      }

      // 2. 有限理性分析
      const boundedAnalysis = this.boundedRationality.detectCognitiveBiases(argument.content);
      if (boundedAnalysis.length > 0) {
        insights.push({
          agent: argument.agent,
          theory: 'bounded_rationality',
          biases: boundedAnalysis,
          recommendation: '考虑认知限制，简化论证结构'
        });
      }

      // 3. 助推检测
      const nudgeAnalysis = this.nudgeTheory.detectDarkNudges(argument.content);
      if (nudgeAnalysis.length > 0) {
        insights.push({
          agent: argument.agent,
          theory: 'nudge_theory',
          darkPatterns: nudgeAnalysis,
          recommendation: '警惕操纵性修辞，要求透明论证'
        });
      }

      // 更新代理档案
      agent.biases.push(...boundedAnalysis.map(b => b.type));
    }

    this.behavioralInsights.push(...insights);
    return insights;
  }

  /**
   * 生成行为经济学增强的策略建议
   */
  generateBehavioralAdvice(agentName, context) {
    const agent = this.agentProfiles.get(agentName);
    if (!agent) return null;

    const advice = {
      agent: agentName,
      recommendations: []
    };

    // 基于前景理论的建议
    const prospectAdvice = this.prospectTheory.generateDebateStrategy(
      agent.position,
      context.opponentPosition,
      context.topic
    );
    advice.recommendations.push({
      theory: 'prospect_theory',
      strategies: prospectAdvice
    });

    // 基于有限理性的建议
    const boundedAdvice = this.boundedRationality.dualSystemDecision(
      { complexity: context.complexity, familiarity: agent.expertise },
      { timePressure: context.timePressure, cognitiveLoad: agent.cognitiveLoad }
    );
    advice.recommendations.push({
      theory: 'bounded_rationality',
      system: boundedAdvice.system,
      mechanism: boundedAdvice.mechanism,
      suggestion: boundedAdvice.system === 1 
        ? '使用直觉和模式识别快速回应'
        : '启动深度分析，系统性地拆解对方论点'
    });

    // 基于助推理论的建议
    const nudgeAdvice = this.nudgeTheory.generateDebateNudges(
      agent.position,
      context.audienceProfile
    );
    advice.recommendations.push({
      theory: 'nudge_theory',
      nudges: nudgeAdvice
    });

    return advice;
  }

  /**
   * 评估决策的行为经济学合理性
   */
  evaluateDecisionBehavioral(decision, context) {
    const evaluation = {
      decision,
      behavioralAssessment: {}
    };

    // 前景理论评估
    const prospects = context.options.map(opt => ({
      probability: opt.probability || 0.5,
      outcome: opt.value,
      referencePoint: context.referencePoint || 0
    }));
    const prospectValue = this.prospectTheory.calculateProspectValue(prospects);
    evaluation.behavioralAssessment.prospectValue = prospectValue;

    // 检查四折模式
    const selectedOption = context.options.find(o => o.id === decision);
    if (selectedOption) {
      const pattern = this.prospectTheory.fourFoldPattern(
        selectedOption.probability || 0.5,
        selectedOption.value
      );
      evaluation.behavioralAssessment.fourFoldPattern = pattern;
    }

    // 有限理性评估
    const cognitiveCost = this.boundedRationality.attentionAllocation(
      context.options.map(o => o.id),
      context.salienceMap || {}
    );
    evaluation.behavioralAssessment.cognitiveCost = cognitiveCost;

    return evaluation;
  }

  /**
   * 生成辩论总结 - 行为经济学视角
   */
  generateBehavioralSummary() {
    const summary = {
      totalInsights: this.behavioralInsights.length,
      byTheory: {
        prospect_theory: this.behavioralInsights.filter(i => i.theory === 'prospect_theory').length,
        bounded_rationality: this.behavioralInsights.filter(i => i.theory === 'bounded_rationality').length,
        nudge_theory: this.behavioralInsights.filter(i => i.theory === 'nudge_theory').length
      },
      commonBiases: this._countCommonBiases(),
      keyRecommendations: this._generateKeyRecommendations()
    };

    return summary;
  }

  // 私有辅助方法
  _inferRiskProfile(participant) {
    const name = participant.name.toLowerCase();
    if (name.includes('巴菲特') || name.includes('graham')) return 'risk_averse';
    if (name.includes('马斯克') || name.includes('wood')) return 'risk_seeking';
    if (name.includes('索罗斯') || name.includes('德鲁克')) return 'opportunistic';
    return 'moderate';
  }

  _inferCognitiveStyle(participant) {
    const name = participant.name.toLowerCase();
    if (name.includes('芒格') || name.includes('munger')) return 'multidisciplinary';
    if (name.includes('西蒙') || name.includes('simon')) return 'bounded_rational';
    if (name.includes('卡尼曼') || name.includes('kahneman')) return 'behavioral';
    return 'analytical';
  }

  _analyzeTopicBehavioralFeatures(topic) {
    const features = [];
    
    if (/风险|损失|收益|投资|赌博/.test(topic)) {
      features.push('risk_decision');
    }
    if (/选择|决策|选项|偏好/.test(topic)) {
      features.push('choice_architecture');
    }
    if (/认知|理性|偏见|偏差/.test(topic)) {
      features.push('cognitive_bias');
    }
    if (/社会|群体|规范|从众/.test(topic)) {
      features.push('social_influence');
    }
    
    return { features, complexity: features.length };
  }

  _analyzeProspectFeatures(argument) {
    const features = [];
    const content = argument.content;

    // 检测损失厌恶
    if (/损失|失去|错过|放弃/.test(content)) {
      features.push('loss_aversion');
    }

    // 检测确定性效应
    if (/确定|肯定|必然|绝对/.test(content)) {
      features.push('certainty_effect');
    }

    // 检测框架效应
    if (/获得|收益|赢得/.test(content) && /失去|损失|错过/.test(content)) {
      features.push('framing_effect');
    }

    return {
      hasFeatures: features.length > 0,
      features,
      recommendation: features.includes('loss_aversion')
        ? '利用损失框架增强说服力'
        : '注意参照点设置'
    };
  }

  _generateBehavioralStrategies(topic, participants) {
    const strategies = [];

    // 为每个参与者生成策略
    participants.forEach(p => {
      const profile = this.agentProfiles.get(p.name);
      
      strategies.push({
        agent: p.name,
        riskBased: this._generateRiskBasedStrategy(profile.riskProfile),
        cognitiveBased: this._generateCognitiveStrategy(profile.cognitiveStyle),
        nudgeBased: this.nudgeTheory.generateDebateNudges(p.position, {})
      });
    });

    return strategies;
  }

  _generateRiskBasedStrategy(riskProfile) {
    const strategies = {
      risk_averse: {
        emphasis: '确定性和安全边际',
        framing: '避免损失',
        appeal: '长期稳定'
      },
      risk_seeking: {
        emphasis: '机会和增长潜力',
        framing: '获得收益',
        appeal: '创新和突破'
      },
      opportunistic: {
        emphasis: '风险收益比',
        framing: '不对称机会',
        appeal: '有限下行无限上行'
      },
      moderate: {
        emphasis: '平衡和多样化',
        framing: '相对优势',
        appeal: '稳健增长'
      }
    };
    return strategies[riskProfile] || strategies.moderate;
  }

  _generateCognitiveStrategy(cognitiveStyle) {
    const strategies = {
      multidisciplinary: '使用多学科心智模型',
      bounded_rational: '承认认知限制，使用满意化策略',
      behavioral: '利用认知偏差，设计选择架构',
      analytical: '系统分析，逐步拆解'
    };
    return strategies[cognitiveStyle] || strategies.analytical;
  }

  _countCommonBiases() {
    const biasCount = {};
    this.behavioralInsights
      .filter(i => i.biases)
      .forEach(i => {
        i.biases.forEach(b => {
          biasCount[b.type] = (biasCount[b.type] || 0) + 1;
        });
      });
    return biasCount;
  }

  _generateKeyRecommendations() {
    const recommendations = [];
    
    // 基于检测到的偏差生成建议
    const biasCount = this._countCommonBiases();
    const topBiases = Object.entries(biasCount)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3);
    
    topBiases.forEach(([bias, count]) => {
      recommendations.push({
        bias,
        frequency: count,
        mitigation: this._getMitigationStrategy(bias)
      });
    });

    return recommendations;
  }

  _getMitigationStrategy(bias) {
    const strategies = {
      availability_bias: '要求提供全面的统计数据，而非易得例子',
      representativeness_bias: '考虑基础概率，避免合取谬误',
      anchoring_bias: '尝试从不同起点重新评估',
      confirmation_bias: '主动寻找反面证据进行检验',
      loss_aversion_escalation: '暂停，重新评估参照点，避免追损',
      certainty_effect: '计算期望值而非依赖确定性'
    };
    return strategies[bias] || '保持警觉，多角度验证';
  }
}

module.exports = { 
  BehavioralEconomicsArena,
  ProspectTheoryEngine,
  BoundedRationalityEngine,
  NudgeTheoryEngine
};
