/**
 * 演化博弈与策略演化
 * Evolutionary Game Theory
 * 
 * 基于 Osborne 第3.4节 / Maynard Smith (1982) ESS
 * 
 * 核心概念：
 * - 种群 (Population)
 * - 策略分布 (Strategy Distribution)
 * - 适应度 (Fitness)
 * - 复制者动态 (Replicator Dynamics)
 * - 演化稳定策略 (ESS)
 */

class EvolutionaryGameDynamics {
  constructor(config) {
    this.strategies = config.strategies; // 可用策略
    this.payoffMatrix = config.payoffMatrix;
    this.mutationRate = config.mutationRate || 0.01;
    this.selectionStrength = config.selectionStrength || 1.0;
  }

  /**
   * 复制者动态 (Replicator Dynamics)
   * 
   * dx_i/dt = x_i [f_i(x) - f̄(x)]
   * 
   * 其中 f_i 是策略i的适应度，f̄ 是平均适应度
   */
  replicatorDynamics(initialPopulation, generations, dt = 0.01) {
    const trajectory = [initialPopulation];
    let currentPop = { ...initialPopulation };
    
    for (let gen = 0; gen < generations; gen++) {
      // 计算各策略的适应度
      const fitness = {};
      for (const strategy of this.strategies) {
        fitness[strategy] = this.calculateFitness(strategy, currentPop);
      }
      
      // 计算平均适应度
      const avgFitness = Object.entries(currentPop)
        .reduce((sum, [s, p]) => sum + p * fitness[s], 0);
      
      // 更新种群比例
      const newPop = {};
      for (const strategy of this.strategies) {
        const growthRate = fitness[strategy] - avgFitness;
        const newProportion = currentPop[strategy] + dt * currentPop[strategy] * growthRate;
        newPop[strategy] = Math.max(0, newProportion);
      }
      
      // 归一化
      const total = Object.values(newPop).reduce((a, b) => a + b, 0);
      for (const strategy of this.strategies) {
        newPop[strategy] /= total;
      }
      
      currentPop = newPop;
      trajectory.push(currentPop);
    }
    
    return {
      trajectory,
      finalPopulation: currentPop,
      
      // 识别稳态
      steadyState: this.identifySteadyState(trajectory),
      
      // 演化稳定策略
      ESS: this.identifyESS(trajectory)
    };
  }

  /**
   * 计算策略适应度
   * 
   * 适应度 = 与其他所有策略互动的期望收益
   */
  calculateFitness(strategy, population) {
    let fitness = 0;
    
    for (const [otherStrategy, proportion] of Object.entries(population)) {
      if (proportion === 0) continue;
      
      const payoff = this.payoffMatrix[strategy]?.[otherStrategy] || 0;
      fitness += proportion * payoff;
    }
    
    return fitness;
  }

  /**
   * 识别演化稳定策略 (ESS)
   * 
   * 定义：策略σ*是ESS，如果对于任何突变策略σ≠σ*：
   * (1) u(σ*, σ*) ≥ u(σ, σ*)  （纳什均衡条件）
   * (2) 如果等号成立，则 u(σ*, σ) > u(σ, σ)
   * 
   * 解释：ESS种群可以抵抗小规模的突变入侵
   */
  identifyESS(trajectory) {
    const finalPop = trajectory[trajectory.length - 1];
    const ESS = [];
    
    // 检查纯策略ESS
    for (const strategy of this.strategies) {
      if (finalPop[strategy] > 0.99) {
        // 几乎整个种群采用此策略
        if (this.verifyESS(strategy)) {
          ESS.push({
            type: 'pure',
            strategy,
            proportion: finalPop[strategy],
            stability: 'stable'
          });
        }
      }
    }
    
    // 检查混合策略ESS
    const mixedESS = this.findMixedESS(finalPop);
    if (mixedESS) {
      ESS.push(mixedESS);
    }
    
    return ESS;
  }

  /**
   * 验证纯策略ESS
   */
  verifyESS(strategy) {
    const payoffSS = this.payoffMatrix[strategy][strategy];
    
    for (const otherStrategy of this.strategies) {
      if (otherStrategy === strategy) continue;
      
      const payoffOS = this.payoffMatrix[otherStrategy][strategy];
      
      // 条件1: u(s, s) ≥ u(o, s)
      if (payoffSS < payoffOS) {
        return false;
      }
      
      // 条件2: 如果等号，则 u(s, o) > u(o, o)
      if (payoffSS === payoffOS) {
        const payoffSO = this.payoffMatrix[strategy][otherStrategy];
        const payoffOO = this.payoffMatrix[otherStrategy][otherStrategy];
        
        if (payoffSO <= payoffOO) {
          return false;
        }
      }
    }
    
    return true;
  }

  /**
   * 寻找混合策略ESS
   */
  findMixedESS(population) {
    // 简化的混合策略ESS检测
    const significantStrategies = Object.entries(population)
      .filter(([s, p]) => p > 0.05)
      .map(([s, p]) => s);
    
    if (significantStrategies.length >= 2) {
      // 可能是混合策略均衡
      return {
        type: 'mixed',
        strategies: significantStrategies.map(s => ({
          strategy: s,
          proportion: population[s]
        })),
        stability: this.assessMixedStability(population)
      };
    }
    
    return null;
  }

  /**
   * 模拟突变入侵
   * 
   * 检验ESS的稳健性
   */
  simulateInvasion(incumbentStrategy, mutantStrategy, invasionSize = 0.01) {
    const initialPop = {};
    
    for (const s of this.strategies) {
      if (s === incumbentStrategy) {
        initialPop[s] = 1 - invasionSize;
      } else if (s === mutantStrategy) {
        initialPop[s] = invasionSize;
      } else {
        initialPop[s] = 0;
      }
    }
    
    // 运行动态
    const result = this.replicatorDynamics(initialPop, 1000);
    
    // 分析结果
    const finalIncumbent = result.finalPopulation[incumbentStrategy];
    const finalMutant = result.finalPopulation[mutantStrategy];
    
    return {
      incumbentStrategy,
      mutantStrategy,
      invasionSize,
      
      outcome: finalIncumbent > finalMutant ? 'repelled' : 'successful',
      
      finalProportions: {
        incumbent: finalIncumbent,
        mutant: finalMutant
      },
      
      // ESS验证
      isESS: finalIncumbent > 0.95
    };
  }

  /**
   * 分析长期演化趋势
   */
  analyzeLongTermEvolution(initialConditions, horizon = 10000) {
    const results = initialConditions.map(init => 
      this.replicatorDynamics(init, horizon)
    );
    
    // 识别吸引域 (Basin of Attraction)
    const attractors = this.identifyAttractors(results);
    
    return {
      attractors,
      
      // 收敛性分析
      convergence: results.map(r => ({
        initialCondition: r.trajectory[0],
        finalState: r.finalPopulation,
        convergenceTime: this.estimateConvergenceTime(r.trajectory),
        attractor: this.identifyAttractor(r.finalPopulation, attractors)
      })),
      
      // 路径依赖
      pathDependence: this.assessPathDependence(results)
    };
  }

  /**
   * 模拟辩论中的策略演化
   * 
   * 观察多轮辩论中策略的分布变化
   */
  simulateDebateEvolution(debaters, rounds, initialStrategies) {
    const evolution = {
      rounds: [],
      strategyDistribution: [],
      dominanceShifts: [],
      
      // 演化指标
      metrics: {
        diversity: [], // 策略多样性
        entropy: [],   // 香农熵
        dominance: []  // 主导策略比例
      }
    };
    
    let currentDistribution = { ...initialStrategies };
    
    for (let round = 0; round < rounds; round++) {
      // 计算本轮各策略的表现
      const performance = {};
      for (const [strategy, proportion] of Object.entries(currentDistribution)) {
        performance[strategy] = this.calculateDebatePerformance(
          strategy,
          currentDistribution,
          debaters
        );
      }
      
      // 更新策略分布（表现好的策略被更多采用）
      const newDistribution = this.updateStrategyDistribution(
        currentDistribution,
        performance
      );
      
      // 记录指标
      evolution.rounds.push(round);
      evolution.strategyDistribution.push(newDistribution);
      evolution.metrics.diversity.push(this.calculateDiversity(newDistribution));
      evolution.metrics.entropy.push(this.calculateEntropy(newDistribution));
      evolution.metrics.dominance.push(Math.max(...Object.values(newDistribution)));
      
      // 检测主导权转移
      if (round > 0) {
        const prevDominant = this.findDominantStrategy(evolution.strategyDistribution[round - 1]);
        const currDominant = this.findDominantStrategy(newDistribution);
        
        if (prevDominant !== currDominant) {
          evolution.dominanceShifts.push({
            round,
            from: prevDominant,
            to: currDominant,
            reason: this.analyzeShiftReason(prevDominant, currDominant, performance)
          });
        }
      }
      
      currentDistribution = newDistribution;
    }
    
    return evolution;
  }

  /**
   * 计算辩论表现
   */
  calculateDebatePerformance(strategy, distribution, debaters) {
    // 简化的表现计算
    const basePayoff = this.calculateFitness(strategy, distribution);
    
    // 考虑对手适应
    const adaptationPenalty = Object.entries(distribution)
      .filter(([s, p]) => s !== strategy && p > 0.1)
      .reduce((penalty, [s, p]) => {
        // 如果策略s对strategy有优势，则产生适应惩罚
        if (this.payoffMatrix[s][strategy] > this.payoffMatrix[strategy][s]) {
          return penalty + p * 0.1;
        }
        return penalty;
      }, 0);
    
    return basePayoff - adaptationPenalty;
  }

  /**
   * 为辩论生成策略演化建议
   */
  generateEvolutionaryAdvice(currentDistribution, trend) {
    const advice = {
      currentState: currentDistribution,
      
      // 演化趋势
      trend,
      
      // 预测
      prediction: this.predictEvolution(currentDistribution, 10),
      
      // 策略建议
      recommendations: []
    };
    
    const dominantStrategy = this.findDominantStrategy(currentDistribution);
    const diversity = this.calculateDiversity(currentDistribution);
    
    if (diversity < 0.3) {
      // 低多样性：尝试突变策略
      advice.recommendations.push({
        type: 'innovation',
        content: `当前${dominantStrategy}主导，考虑采用反制策略`,
        risk: '可能失败，但有机会改变均衡'
      });
    } else {
      // 高多样性：强化当前优势策略
      advice.recommendations.push({
        type: 'exploitation',
        content: `多样化环境中，坚持${dominantStrategy}并优化执行`,
        benefit: '利用当前优势巩固地位'
      });
    }
    
    // ESS分析
    if (this.verifyESS(dominantStrategy)) {
      advice.recommendations.push({
        type: 'stability',
        content: `${dominantStrategy}是演化稳定策略，难以被入侵`,
        implication: '需要重大扰动才能改变格局'
      });
    }
    
    return advice;
  }

  // 辅助方法...
  identifySteadyState(trajectory) {
    // 识别轨迹是否收敛
    return trajectory[trajectory.length - 1];
  }

  assessMixedStability(population) {
    return 'unknown'; // 简化
  }

  identifyAttractors(results) {
    return []; // 简化
  }

  identifyAttractor(finalState, attractors) {
    return null; // 简化
  }

  assessPathDependence(results) {
    return { degree: 'medium' }; // 简化
  }

  estimateConvergenceTime(trajectory) {
    return trajectory.length; // 简化
  }

  updateStrategyDistribution(current, performance) {
    // 简化的更新规则
    const newDist = {};
    const totalPerformance = Object.values(performance).reduce((a, b) => a + b, 0);
    
    for (const strategy of this.strategies) {
      newDist[strategy] = performance[strategy] / totalPerformance;
    }
    
    return newDist;
  }

  calculateDiversity(distribution) {
    // 香农多样性指数
    let entropy = 0;
    for (const p of Object.values(distribution)) {
      if (p > 0) {
        entropy -= p * Math.log(p);
      }
    }
    return entropy;
  }

  calculateEntropy(distribution) {
    return this.calculateDiversity(distribution);
  }

  findDominantStrategy(distribution) {
    return Object.entries(distribution)
      .reduce((max, [s, p]) => p > max.proportion ? {strategy: s, proportion: p} : max, 
        {strategy: null, proportion: 0}
      ).strategy;
  }

  analyzeShiftReason(from, to, performance) {
    return `${to}的表现(${performance[to].toFixed(2)})超过了${from}(${performance[from].toFixed(2)})`;
  }

  predictEvolution(current, steps) {
    const result = this.replicatorDynamics(current, steps);
    return result.finalPopulation;
  }
}

module.exports = EvolutionaryGameDynamics;
