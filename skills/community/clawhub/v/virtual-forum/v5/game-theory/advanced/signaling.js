/**
 * 信号博弈分析器
 * Signaling Game Analyzer
 * 
 * 基于 Spence (1973) 教育信号模型 / Bonanno 第15章
 * 
 * 核心概念：
 * - 发送者（知情方）vs 接收者（不知情方）
 * - 类型空间: Θ = {θ_1, θ_2, ..., θ_n}
 * - 信号空间: M = {m_1, m_2, ..., m_k}
 * - 行动空间: A = {a_1, a_2, ..., a_l}
 * 
 * 均衡类型：
 * - 分离均衡 (Separating): 不同类型发送不同信号
 * - 混同均衡 (Pooling): 所有类型发送相同信号
 * - 半分离均衡 (Semi-separating): 混合策略
 */

class SignalingGameAnalyzer {
  constructor(config) {
    this.sender = config.sender; // 信号发送者（知情）
    this.receiver = config.receiver; // 信号接收者（不知情）
    this.types = config.types; // 类型空间
    this.signals = config.signals; // 信号空间
    this.actions = config.actions; // 接收者行动空间
    this.priorBeliefs = config.priorBeliefs; // 先验信念 P(θ)
    this.signalCosts = config.signalCosts; // 信号成本 c(m, θ)
    this.payoffFunctions = config.payoffFunctions; // 收益函数
  }

  /**
   * 分析完美贝叶斯均衡 (PBE)
 * 
   * PBE = (策略组合, 信念系统) 满足：
   * 1. 序贯理性: 在每个信息集上最优
   * 2. 信念一致性: 符合贝叶斯法则（在均衡路径上）
   */
  findPerfectBayesianEquilibria() {
    const equilibria = [];
    
    // 1. 寻找分离均衡
    const separating = this.findSeparatingEquilibria();
    equilibria.push(...separating);
    
    // 2. 寻找混同均衡
    const pooling = this.findPoolingEquilibria();
    equilibria.push(...pooling);
    
    // 3. 寻找半分离均衡
    const semiSeparating = this.findSemiSeparatingEquilibria();
    equilibria.push(...semiSeparating);
    
    return {
      total: equilibria.length,
      separating: separating.length,
      pooling: pooling.length,
      semiSeparating: semiSeparating.length,
      equilibria: equilibria.map(e => this.analyzeEquilibrium(e))
    };
  }

  /**
   * 寻找分离均衡
   * 
   * 条件：不同类型选择不同信号
   * 结果：完全揭示信息
   */
  findSeparatingEquilibria() {
    const equilibria = [];
    
    // 遍历所有可能的分离策略组合
    const separatingStrategies = this.generateSeparatingStrategies();
    
    for (const strategy of separatingStrategies) {
      // 构建信念系统（完全揭示）
      const beliefs = this.buildSeparatingBeliefs(strategy);
      
      // 验证序贯理性
      if (this.checkSequentialRationality(strategy, beliefs)) {
        // 验证激励相容
        if (this.checkIncentiveCompatibility(strategy, 'separating')) {
          equilibria.push({
            type: 'separating',
            senderStrategy: strategy,
            receiverStrategy: this.deriveReceiverStrategy(beliefs),
            beliefs,
            informativeness: 1.0 // 完全信息
          });
        }
      }
    }
    
    return equilibria;
  }

  /**
   * 寻找混同均衡
   * 
   * 条件：所有类型选择相同信号
   * 结果：无信息揭示
   */
  findPoolingEquilibria() {
    const equilibria = [];
    
    // 遍历所有可能的混同信号
    for (const signal of this.signals) {
      const strategy = {};
      this.types.forEach(type => {
        strategy[type] = signal;
      });
      
      // 构建信念系统（非均衡路径上的任意信念）
      // 需要满足：对于非均衡信号，接收者的威胁足够强
      const offPathBeliefs = this.findSupportingOffPathBeliefs(strategy, signal);
      
      for (const beliefs of offPathBeliefs) {
        if (this.checkSequentialRationality(strategy, beliefs)) {
          if (this.checkIncentiveCompatibility(strategy, 'pooling', beliefs)) {
            equilibria.push({
              type: 'pooling',
              poolingSignal: signal,
              senderStrategy: strategy,
              receiverStrategy: this.deriveReceiverStrategy(beliefs),
              beliefs,
              informativeness: 0.0, // 无信息
              offPathThreats: beliefs.offPath
            });
          }
        }
      }
    }
    
    return equilibria;
  }

  /**
   * 寻找半分离均衡
   * 
   * 条件：某些类型随机化信号选择
   */
  findSemiSeparatingEquilibria() {
    const equilibria = [];
    
    // 简化的半分离均衡：两种类型，一个随机化
    if (this.types.length === 2) {
      const [type1, type2] = this.types;
      
      // type1纯策略，type2混合策略
      for (const signal1 of this.signals) {
        for (const signal2 of this.signals) {
          if (signal1 === signal2) continue;
          
          // 尝试找到使type2无差异的混合概率
          const mixProb = this.findMixingProbability(type2, signal1, signal2);
          
          if (mixProb > 0 && mixProb < 1) {
            const strategy = {
              [type1]: signal1,
              [type2]: { [signal1]: mixProb, [signal2]: 1 - mixProb }
            };
            
            const beliefs = this.buildSemiSeparatingBeliefs(strategy);
            
            if (this.checkSequentialRationality(strategy, beliefs)) {
              equilibria.push({
                type: 'semi-separating',
                senderStrategy: strategy,
                mixingType: type2,
                mixingProbability: mixProb,
                beliefs,
                informativeness: this.calculateInformativeness(strategy)
              });
            }
          }
        }
      }
    }
    
    return equilibria;
  }

  /**
   * 分析均衡性质
   */
  analyzeEquilibrium(equilibrium) {
    const analysis = {
      type: equilibrium.type,
      
      // 信息效率
      informativeness: equilibrium.informativeness,
      
      // 福利分析
      welfare: this.calculateWelfare(equilibrium),
      
      // 效率损失
      efficiency: this.calculateEfficiency(equilibrium),
      
      // 稳定性
      stability: this.assessStability(equilibrium),
      
      // 精炼
      refinements: this.applyRefinements(equilibrium)
    };
    
    return analysis;
  }

  /**
   * 应用均衡精炼
   * 
   * Cho-Kreps 直观标准 (Intuitive Criterion)
   * 
   * 排除不合理的非均衡信念
   */
  applyRefinements(equilibrium) {
    const refinements = {
      intuitiveCriterion: null,
      divineCriterion: null,
      universalDivinity: null
    };
    
    if (equilibrium.type === 'pooling') {
      // 检验直观标准
      refinements.intuitiveCriterion = this.checkIntuitiveCriterion(equilibrium);
      
      // 直观标准：如果存在一个类型，
      // 1. 该类型可以从偏离中获益（对某些信念）
      // 2. 其他类型无法从偏离中获益（对任何信念）
      // 则偏离应该被解释为来自该类型
      
      const deviations = this.findEquilibriumDominatingDeviations(equilibrium);
      
      if (deviations.length > 0) {
        refinements.intuitiveCriterion = {
          satisfied: false,
          failingDeviations: deviations,
          explanation: '存在直观标准失败的偏离'
        };
      } else {
        refinements.intuitiveCriterion = {
          satisfied: true,
          explanation: '通过直观标准'
        };
      }
    }
    
    return refinements;
  }

  /**
   * 实时信号分析
   * 
   * 辩论中观察到信号后的实时分析
   */
  analyzeObservedSignal(observedSignal, priorBeliefs = this.priorBeliefs) {
    const analysis = {
      observedSignal,
      priorBeliefs: { ...priorBeliefs },
      
      // 均衡路径判断
      equilibriumTypes: this.identifyEquilibriumTypes(observedSignal),
      
      // 贝叶斯更新（考虑可能的均衡）
      posteriorBeliefs: {},
      
      // 信号解读
      interpretation: null,
      
      // 建议
      recommendations: []
    };
    
    // 针对每种可能的均衡类型计算后验
    for (const eqType of analysis.equilibriumTypes) {
      if (eqType === 'separating') {
        // 分离均衡：完全揭示
        const revealedType = this.inferTypeFromSeparatingSignal(observedSignal);
        analysis.posteriorBeliefs[eqType] = this.createDegenerateBelief(revealedType);
      } else if (eqType === 'pooling') {
        // 混同均衡：无信息
        analysis.posteriorBeliefs[eqType] = { ...priorBeliefs };
      } else {
        // 半分离：部分更新
        analysis.posteriorBeliefs[eqType] = this.calculateSemiSeparatingPosterior(
          observedSignal,
          priorBeliefs
        );
      }
    }
    
    // 综合解读
    analysis.interpretation = this.synthesizeInterpretation(analysis);
    
    // 生成建议
    analysis.recommendations = this.generateSignalRecommendations(analysis);
    
    return analysis;
  }

  /**
   * 计算信号成本
   * 
   * Spence 模型核心：不同类型有不同信号成本
   */
  calculateSignalingCosts(signal, type) {
    const baseCost = this.signalCosts[signal]?.[type] || 0;
    
    // 单交叉性质 (Single Crossing)
    // 高类型信号成本相对较低（或相对收益更高）
    const typeIndex = this.types.indexOf(type);
    const costAdjustment = typeIndex * 0.1; // 高类型成本更低
    
    return Math.max(0, baseCost - costAdjustment);
  }

  /**
   * 验证单交叉性质
   * 
   * 高类型从信号中获得更多净收益
   */
  verifySingleCrossingProperty() {
    const results = [];
    
    for (let i = 0; i < this.types.length - 1; i++) {
      for (let j = i + 1; j < this.types.length; j++) {
        const lowType = this.types[i];
        const highType = this.types[j];
        
        for (const signal of this.signals) {
          const netBenefitLow = this.calculateNetBenefit(lowType, signal);
          const netBenefitHigh = this.calculateNetBenefit(highType, signal);
          
          results.push({
            lowType,
            highType,
            signal,
            singleCrossing: netBenefitHigh > netBenefitLow,
            difference: netBenefitHigh - netBenefitLow
          });
        }
      }
    }
    
    return {
      satisfied: results.every(r => r.singleCrossing),
      violations: results.filter(r => !r.singleCrossing),
      details: results
    };
  }

  /**
   * 计算净收益（信号收益 - 信号成本）
   */
  calculateNetBenefit(type, signal) {
    const benefit = this.payoffFunctions.sender(type, signal, 'optimal_response');
    const cost = this.calculateSignalingCosts(signal, type);
    return benefit - cost;
  }

  /**
   * 生成辩论中的信号策略建议
   */
  generateSignalingStrategyAdvice(senderType) {
    const advice = {
      type: senderType,
      
      // 最优信号选择
      optimalSignal: null,
      
      // 每种均衡下的策略
      equilibriumStrategies: {},
      
      // 偏离分析
      deviationAnalysis: {}
    };
    
    // 分析每种均衡下的最优策略
    const pbeAnalysis = this.findPerfectBayesianEquilibria();
    
    for (const eq of pbeAnalysis.equilibria) {
      if (eq.type === 'separating') {
        // 分离均衡：必须选择能标识类型的信号
        advice.equilibriumStrategies.separating = {
          recommendedSignal: eq.senderStrategy[senderType],
          explanation: '选择独特的信号以证明你的类型',
          risk: '信号成本可能很高'
        };
      } else if (eq.type === 'pooling') {
        // 混同均衡：与其他类型发送相同信号
        advice.equilibriumStrategies.pooling = {
          recommendedSignal: eq.poolingSignal,
          explanation: '隐藏在群体中，不暴露真实类型',
          benefit: '节省信号成本'
        };
      }
    }
    
    // 分析有利偏离
    advice.deviationAnalysis = this.analyzeProfitableDeviations(senderType);
    
    return advice;
  }

  // 辅助方法（简化实现）...
  generateSeparatingStrategies() {
    // 生成所有可能的分离策略
    // 每种类型选择不同信号
    return []; // 简化
  }

  buildSeparatingBeliefs(strategy) {
    // 分离均衡下的信念：完全揭示
    const beliefs = {};
    for (const [type, signal] of Object.entries(strategy)) {
      beliefs[signal] = {};
      this.types.forEach(t => {
        beliefs[signal][t] = (t === type) ? 1.0 : 0.0;
      });
    }
    return beliefs;
  }

  checkSequentialRationality(strategy, beliefs) {
    // 验证序贯理性
    return true; // 简化
  }

  checkIncentiveCompatibility(strategy, type, beliefs = null) {
    // 验证激励相容
    return true; // 简化
  }
}

module.exports = SignalingGameAnalyzer;
