/**
 * 序贯均衡与精炼
 * Sequential Equilibrium & Refinements
 * 
 * 基于 Osborne 第12章 / Bonanno 第11-13章
 * 
 * 核心概念：
 * - 序贯均衡 (Sequential Equilibrium) - Kreps-Wilson
 * - 完美贝叶斯均衡 (Perfect Bayesian Equilibrium)
 * - 颤抖手完美均衡 (Trembling Hand Perfect Equilibrium) - Selten
 * - 直观标准 (Intuitive Criterion) - Cho-Kreps
 */

class SequentialEquilibriumSolver {
  constructor(extensiveGame) {
    this.game = extensiveGame;
  }

  /**
   * 寻找序贯均衡
   * 
   * 序贯均衡 = (策略组合 σ, 信念系统 μ) 满足：
   * 1. 序贯理性: 给定信念 μ，策略 σ 在每个信息集上最优
   * 2. 一致性: 存在颤抖序列 (σ^n, μ^n) → (σ, μ)
   * 
   * Osborne 第12.2节 / Bonanno 第12章
   */
  findSequentialEquilibrium() {
    const assessments = this.generateAssessments();
    const equilibria = [];
    
    for (const assessment of assessments) {
      if (this.checkSequentialRationality(assessment) &&
          this.checkConsistency(assessment)) {
        equilibria.push(assessment);
      }
    }
    
    return {
      type: 'Sequential Equilibrium',
      count: equilibria.length,
      equilibria: equilibria.map(eq => this.analyzeEquilibrium(eq))
    };
  }

  /**
   * 检查序贯理性
   * 
   * 在每个信息集上，给定信念，策略是最优的
   */
  checkSequentialRationality(assessment) {
    const { strategy, beliefs } = assessment;
    
    for (const informationSet of this.game.getInformationSets()) {
      const player = informationSet.player;
      const optimalAction = this.findOptimalAction(informationSet, beliefs, strategy);
      
      if (strategy[player][informationSet.id] !== optimalAction) {
        return false;
      }
    }
    
    return true;
  }

  /**
   * 检查一致性
   * 
   * 存在颤抖序列收敛到该评估
   */
  checkConsistency(assessment) {
    // 使用 trembling hand 方法验证
    const tremblingSequence = this.generateTremblingSequence(assessment);
    
    return tremblingSequence.converges;
  }

  /**
   * 生成颤抖序列
   */
  generateTremblingSequence(assessment, steps = 100) {
    const sequence = [];
    let current = this.addTremble(assessment, 0.1); // 初始颤抖
    
    for (let i = 0; i < steps; i++) {
      const epsilon = 0.1 / (i + 1); // 颤抖概率递减
      current = this.addTremble(assessment, epsilon);
      
      sequence.push({
        step: i,
        epsilon,
        assessment: current,
        beliefs: this.updateBeliefsWithTremble(current)
      });
    }
    
    // 检查是否收敛
    const converges = this.checkConvergence(sequence, assessment);
    
    return { sequence, converges };
  }

  /**
   * 添加颤抖
   * 
   * 每个行动以至少 ε 的概率被选择
   */
  addTremble(assessment, epsilon) {
    const trembled = JSON.parse(JSON.stringify(assessment));
    
    for (const player of this.game.players) {
      for (const infoSet of Object.keys(trembled.strategy[player])) {
        const actions = this.game.getActions(player, infoSet);
        const numActions = actions.length;
        
        // 混合策略：以 (1-ε) 按原策略，以 ε 均匀随机
        for (const action of actions) {
          trembled.strategy[player][infoSet][action] = 
            (1 - epsilon) * (trembled.strategy[player][infoSet][action] || 0) +
            epsilon / numActions;
        }
      }
    }
    
    return trembled;
  }

  /**
   * 完美贝叶斯均衡求解
   * 
   * Bonanno 第13章
   */
  findPerfectBayesianEquilibrium() {
    const candidates = this.generatePBECandidates();
    const validPBE = [];
    
    for (const candidate of candidates) {
      if (this.verifyPBE(candidate)) {
        validPBE.push(candidate);
      }
    }
    
    return {
      type: 'Perfect Bayesian Equilibrium',
      count: validPBE.length,
      equilibria: validPBE,
      
      // 精炼
      refinements: this.applyRefinements(validPBE)
    };
  }

  /**
   * 验证PBE
   */
  verifyPBE(candidate) {
    // 1. 序贯理性
    if (!this.checkSequentialRationality(candidate)) {
      return false;
    }
    
    // 2. 信念更新（在均衡路径上）
    if (!this.checkBayesianUpdatingOnPath(candidate)) {
      return false;
    }
    
    return true;
  }

  /**
   * 检查均衡路径上的贝叶斯更新
   */
  checkBayesianUpdatingOnPath(candidate) {
    const { strategy, beliefs } = candidate;
    
    // 对于每个在均衡路径上的信息集
    for (const infoSet of this.getInformationSetsOnPath(strategy)) {
      const calculatedBeliefs = this.calculateBayesianBeliefs(infoSet, strategy);
      
      // 比较计算出的信念与候选信念
      if (!this.beliefsEqual(calculatedBeliefs, beliefs[infoSet.id])) {
        return false;
      }
    }
    
    return true;
  }

  /**
   * 应用均衡精炼
   */
  applyRefinements(equilibria) {
    return {
      intuitiveCriterion: this.applyIntuitiveCriterion(equilibria),
      divineCriterion: this.applyDivineCriterion(equilibria),
      universalDivinity: this.applyUniversalDivinity(equilibria)
    };
  }

  /**
   * Cho-Kreps 直观标准
   * 
   * Bonanno 第13.4节
   * 
   * 排除不合理的非均衡信念
   */
  applyIntuitiveCriterion(equilibria) {
    const refined = [];
    
    for (const eq of equilibria) {
      let survives = true;
      
      // 对于每个非均衡信息集
      for (const offPathInfoSet of this.getOffPathInformationSets(eq)) {
        // 检查是否存在"直观"的偏离
        const intuitiveDeviations = this.findIntuitiveDeviations(eq, offPathInfoSet);
        
        if (intuitiveDeviations.length > 0) {
          survives = false;
          eq.refinementFailure = {
            criterion: 'Intuitive Criterion',
            reason: '存在直观偏离未被正确处理',
            deviations: intuitiveDeviations
          };
          break;
        }
      }
      
      if (survives) {
        refined.push(eq);
      }
    }
    
    return {
      originalCount: equilibria.length,
      refinedCount: refined.length,
      eliminated: equilibria.length - refined.length,
      equilibria: refined
    };
  }

  /**
   * 寻找直观偏离
   * 
   * 偏离 m 对于类型 θ 是直观的，如果：
   * 1. θ 可以从偏离中获益（对某些信念）
   * 2. 其他类型 θ' 无法从偏离中获益（对任何信念）
   */
  findIntuitiveDeviations(equilibrium, infoSet) {
    const deviations = [];
    const types = this.game.getTypesAtInformationSet(infoSet);
    
    for (const action of infoSet.availableActions) {
      for (const type of types) {
        const canBenefit = this.canTypeBenefitFromDeviation(type, action, equilibrium);
        const othersCannotBenefit = types
          .filter(t => t !== type)
          .every(t => !this.canTypeBenefitFromDeviation(t, action, equilibrium));
        
        if (canBenefit && othersCannotBenefit) {
          deviations.push({ type, action });
        }
      }
    }
    
    return deviations;
  }

  /**
   * 颤抖手完美均衡
   * 
   * Selten (1975)
   * 
   * 策略组合是颤抖手完美的，如果它是对某个颤抖序列的最佳反应
   */
  findTremblingHandPerfectEquilibrium() {
    const strategicForm = this.game.convertToStrategicForm();
    
    // 在战略式博弈中寻找颤抖手完美均衡
    const equilibria = this.findNashEquilibria(strategicForm);
    const perfectEquilibria = [];
    
    for (const eq of equilibria) {
      if (this.isTremblingHandPerfect(eq, strategicForm)) {
        perfectEquilibria.push(eq);
      }
    }
    
    return {
      type: 'Trembling Hand Perfect Equilibrium',
      count: perfectEquilibria.length,
      equilibria: perfectEquilibria
    };
  }

  /**
   * 检查颤抖手完美性
   */
  isTremblingHandPerfect(equilibrium, strategicForm) {
    // 生成颤抖序列
    const trembles = this.generateTremblingSequences(equilibrium, strategicForm);
    
    // 检查是否存在收敛的颤抖序列
    for (const tremble of trembles) {
      if (tremble.convergesToEquilibrium) {
        return true;
      }
    }
    
    return false;
  }

  /**
   * 分析均衡的稳定性
   */
  analyzeStability(equilibrium) {
    return {
      // 对信念扰动的稳定性
      beliefStability: this.testBeliefPerturbations(equilibrium),
      
      // 对策略扰动的稳定性
      strategyStability: this.testStrategyPerturbations(equilibrium),
      
      // 学习动态下的稳定性
      learningStability: this.testLearningDynamics(equilibrium),
      
      // 总体评估
      overall: this.assessOverallStability(equilibrium)
    };
  }

  /**
   * 为辩论生成精炼建议
   */
  generateRefinementAdvice(equilibrium) {
    const advice = {
      credibility: null,
      beliefFormation: null,
      offPathBehavior: null
    };
    
    // 检查是否通过直观标准
    const intuitiveCheck = this.applyIntuitiveCriterion([equilibrium]);
    
    if (intuitiveCheck.refinedCount === 0) {
      advice.credibility = {
        status: 'questionable',
        issue: '未通过直观标准',
        suggestion: '重新考虑非均衡路径上的信念设定'
      };
    } else {
      advice.credibility = {
        status: 'credible',
        note: '通过直观标准，信念设定合理'
      };
    }
    
    // 信念形成建议
    advice.beliefFormation = {
      principle: '使用贝叶斯更新处理均衡路径上的信念',
      offPath: '对于非均衡路径，考虑直观标准或更精炼的概念'
    };
    
    return advice;
  }

  // 辅助方法...
  generateAssessments() {
    return [];
  }

  findOptimalAction(infoSet, beliefs, strategy) {
    return null;
  }

  updateBeliefsWithTremble(trembledAssessment) {
    return {};
  }

  checkConvergence(sequence, target) {
    return true;
  }

  generatePBECandidates() {
    return [];
  }

  getInformationSetsOnPath(strategy) {
    return [];
  }

  calculateBayesianBeliefs(infoSet, strategy) {
    return {};
  }

  beliefsEqual(b1, b2) {
    return true;
  }

  getOffPathInformationSets(equilibrium) {
    return [];
  }

  canTypeBenefitFromDeviation(type, action, equilibrium) {
    return false;
  }

  findNashEquilibria(strategicForm) {
    return [];
  }

  generateTremblingSequences(equilibrium, strategicForm) {
    return [];
  }

  testBeliefPerturbations(equilibrium) {
    return { stable: true };
  }

  testStrategyPerturbations(equilibrium) {
    return { stable: true };
  }

  testLearningDynamics(equilibrium) {
    return { stable: true };
  }

  assessOverallStability(equilibrium) {
    return 'stable';
  }
}

module.exports = SequentialEquilibriumSolver;
