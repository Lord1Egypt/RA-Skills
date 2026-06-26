/**
 * 有限理性模型 (Bounded Rationality) - Herbert Simon & Bryan Jones
 * 模拟人类认知限制下的决策行为
 */

class BoundedRationalityEngine {
  constructor(params = {}) {
    // 认知资源参数
    this.attentionCapacity = params.attentionCapacity || 7; // 工作记忆容量(Miller, 1956)
    this.processingSpeed = params.processingSpeed || 1.0; // 信息处理速度
    this.cognitiveLoad = params.cognitiveLoad || 0; // 当前认知负荷
    
    // 满意化阈值
    this.aspirationLevel = params.aspirationLevel || 0.7; // 满意化阈值
    this.searchDepth = params.searchDepth || 5; // 搜索深度限制
    
    // 启发式偏好
    this.heuristicBias = params.heuristicBias || {
      availability: 0.3,    // 可得性启发
      representativeness: 0.3, // 代表性启发
      anchoring: 0.4      // 锚定启发
    };
  }

  /**
   * 满意化决策 (Satisficing)
   * Simon 1955: 寻找第一个满足阈值的选项，而非最优
   */
  satisficingDecision(alternatives, evaluateFn, threshold = null) {
    const asp = threshold !== null ? threshold : this.aspirationLevel;
    const maxSearch = Math.min(this.searchDepth, alternatives.length);
    
    let searchOrder = this.cognitiveLoad > 0.7 
      ? this._biasedSearchOrder(alternatives) // 高负荷时使用启发式排序
      : [...alternatives.keys()].sort(() => Math.random() - 0.5);
    
    for (let i = 0; i < maxSearch; i++) {
      const idx = searchOrder[i];
      const value = evaluateFn(alternatives[idx]);
      
      if (value >= asp) {
        return {
          choice: alternatives[idx],
          value: value,
          searchSteps: i + 1,
          isOptimal: false, // 满意化不保证最优
          mechanism: 'satisficing'
        };
      }
    }
    
    // 如果都没满足阈值，选择已搜索中最好的
    const searched = searchOrder.slice(0, maxSearch).map(i => ({
      alt: alternatives[i],
      value: evaluateFn(alternatives[i])
    }));
    const best = searched.reduce((max, curr) => curr.value > max.value ? curr : max);
    
    return {
      choice: best.alt,
      value: best.value,
      searchSteps: maxSearch,
      isOptimal: false,
      mechanism: 'satisficing_fallback'
    };
  }

  /**
   * 可得性启发 (Availability Heuristic)
   * 基于记忆可提取性判断概率
   */
  availabilityJudgment(eventType, recentExamples = [], vividness = 0.5) {
    // 最近例子数量影响可得性
    const recencyBoost = Math.min(recentExamples.length / 3, 1) * 0.4;
    // 生动性影响可得性
    const vividnessBoost = vividness * 0.3;
    // 基础可得性
    const baseAvailability = 0.3;
    
    const judgedProbability = Math.min(
      baseAvailability + recencyBoost + vividnessBoost,
      1.0
    );
    
    return {
      eventType,
      judgedProbability,
      actualProbability: null, // 需要外部数据
      bias: 'overestimation_if_vivid',
      factors: {
        recentExamples: recentExamples.length,
        vividness,
        recencyBoost,
        vividnessBoost
      }
    };
  }

  /**
   * 代表性启发 (Representativeness Heuristic)
   * 基于相似性判断概率，忽视基础概率
   */
  representativenessJudgment(target, categoryPrototype, baseRate = 0.1) {
    // 计算与典型特征的相似度
    const similarity = this._calculateSimilarity(target, categoryPrototype);
    
    // 代表性判断 = 相似度 (忽视基础概率)
    const judgedProbability = similarity;
    
    // 基础概率忽视程度
    const baseRateNeglect = Math.abs(similarity - baseRate) > 0.2;
    
    // 合取谬误风险
    const conjunctionFallacyRisk = target.features?.length > categoryPrototype.features?.length;
    
    return {
      target,
      judgedProbability,
      actualProbability: baseRate * similarity, // 贝叶斯正确值
      similarity,
      baseRate,
      baseRateNeglect,
      conjunctionFallacyRisk,
      bias: baseRateNeglect ? 'base_rate_neglect' : null
    };
  }

  /**
   * 锚定与调整 (Anchoring and Adjustment)
   * 从初始值出发，调整不足
   */
  anchoringAdjustment(anchor, targetValue, adjustmentRange = 0.5) {
    // 实际需要的调整
    const neededAdjustment = targetValue - anchor;
    // 实际调整 (不足)
    const actualAdjustment = neededAdjustment * adjustmentRange;
    // 最终估计
    const estimate = anchor + actualAdjustment;
    
    return {
      anchor,
      targetValue,
      estimate,
      neededAdjustment,
      actualAdjustment,
      adjustmentInsufficiency: neededAdjustment - actualAdjustment,
      bias: 'insufficient_adjustment'
    };
  }

  /**
   * 双系统理论 (System 1 vs System 2)
   * Kahneman: 快速直觉 vs 慢速理性
   */
  dualSystemDecision(problem, context = {}) {
    const { timePressure, cognitiveLoad, emotionalArousal } = context;
    
    // 系统1触发条件
    const system1Triggers = {
      timePressure: timePressure > 0.7,
      highCognitiveLoad: cognitiveLoad > 0.6,
      emotionalArousal: emotionalArousal > 0.5,
      patternMatch: this._isPatternMatch(problem),
      expertise: this._hasExpertiseHeuristic(problem)
    };
    
    const useSystem1 = Object.values(system1Triggers).some(t => t);
    
    if (useSystem1) {
      return {
        system: 1,
        mechanism: 'heuristic',
        speed: 'fast',
        accuracy: 'moderate',
        triggers: system1Triggers,
        output: this._system1Response(problem)
      };
    } else {
      return {
        system: 2,
        mechanism: 'analytical',
        speed: 'slow',
        accuracy: 'high',
        effort: 'high',
        output: this._system2Response(problem)
      };
    }
  }

  /**
   * 注意力分配模型
   * Jones: 注意力是稀缺资源
   */
  attentionAllocation(topics, salienceMap = {}) {
    const totalAttention = this.attentionCapacity;
    const n = topics.length;
    
    // 默认均匀分配
    let allocations = topics.map(t => ({
      topic: t,
      baseAllocation: totalAttention / n,
      salience: salienceMap[t] || 0.5,
      finalAllocation: 0
    }));
    
    // 显著性调整
    const totalSalience = allocations.reduce((sum, a) => sum + a.salience, 0);
    allocations = allocations.map(a => ({
      ...a,
      finalAllocation: (a.salience / totalSalience) * totalAttention
    }));
    
    // 检查超载
    const overloaded = allocations.some(a => a.finalAllocation < 1);
    
    return {
      allocations,
      totalCapacity: totalAttention,
      utilized: Math.min(allocations.reduce((sum, a) => sum + a.finalAllocation, 0), totalAttention),
      overloaded,
      neglectedTopics: allocations.filter(a => a.finalAllocation < 1).map(a => a.topic)
    };
  }

  /**
   * 情感对决策的影响
   * Jones: 情感是程序性限制
   */
  emotionalInfluence(decision, emotionalState = {}) {
    const { fear, anger, joy, sadness } = emotionalState;
    const influences = [];
    
    if (fear && fear > 0.5) {
      influences.push({
        emotion: 'fear',
        effect: 'risk_aversion',
        magnitude: fear,
        description: '恐惧增加风险厌恶，偏好确定性'
      });
    }
    
    if (anger && anger > 0.5) {
      influences.push({
        emotion: 'anger',
        effect: 'risk_seeking',
        magnitude: anger,
        description: '愤怒导致风险寻求，可能过度乐观'
      });
    }
    
    if (joy && joy > 0.7) {
      influences.push({
        emotion: 'joy',
        effect: 'optimism_bias',
        magnitude: joy,
        description: '过度乐观，低估风险'
      });
    }
    
    return {
      originalDecision: decision,
      emotionalAdjustments: influences,
      adjustedDecision: this._applyEmotionalAdjustments(decision, influences)
    };
  }

  /**
   * 生成辩论中的认知偏差检测
   */
  detectCognitiveBiases(argument, context = {}) {
    const biases = [];
    
    // 可得性检测
    if (/最近|常常|总是|听说|记得/.test(argument)) {
      biases.push({
        type: 'availability_bias',
        description: '使用易得例子判断概率',
        suggestion: '检查是否有更全面的统计数据'
      });
    }
    
    // 代表性检测
    if (/典型的|就像|类似于|一看就是/.test(argument)) {
      biases.push({
        type: 'representativeness_bias',
        description: '基于相似性判断，可能忽视基础概率',
        suggestion: '考虑基础概率，避免合取谬误'
      });
    }
    
    // 锚定检测
    if (/最初|首先|一开始|参考/.test(argument)) {
      biases.push({
        type: 'anchoring_bias',
        description: '可能过度依赖初始信息',
        suggestion: '尝试从不同起点重新评估'
      });
    }
    
    // 确认偏误
    if (/显然|明显|毫无疑问|肯定/.test(argument)) {
      biases.push({
        type: 'confirmation_bias',
        description: '过度自信，可能忽视反面证据',
        suggestion: '主动寻找反面证据进行检验'
      });
    }
    
    return biases;
  }

  // 辅助方法
  _biasedSearchOrder(alternatives) {
    // 高认知负荷时：优先选择显著的选项
    return alternatives.map((alt, i) => ({
      index: i,
      salience: alt.salience || Math.random()
    })).sort((a, b) => b.salience - a.salience).map(x => x.index);
  }

  _calculateSimilarity(target, prototype) {
    if (!target.features || !prototype.features) return 0.5;
    const common = target.features.filter(f => prototype.features.includes(f));
    return common.length / Math.max(target.features.length, prototype.features.length);
  }

  _isPatternMatch(problem) {
    // 检查是否匹配已知模式
    return problem.familiarity > 0.6 || problem.complexity < 0.4;
  }

  _hasExpertiseHeuristic(problem) {
    return problem.domainExpertise > 0.7;
  }

  _system1Response(problem) {
    return {
      confidence: 0.8,
      processingTime: 'fast',
      basis: 'pattern_recognition'
    };
  }

  _system2Response(problem) {
    return {
      confidence: 0.9,
      processingTime: 'slow',
      basis: 'analytical_reasoning'
    };
  }

  _applyEmotionalAdjustments(decision, influences) {
    let adjusted = { ...decision };
    influences.forEach(inf => {
      if (inf.effect === 'risk_aversion') {
        adjusted.riskTolerance = (adjusted.riskTolerance || 0.5) * (1 - inf.magnitude * 0.3);
      } else if (inf.effect === 'risk_seeking') {
        adjusted.riskTolerance = (adjusted.riskTolerance || 0.5) * (1 + inf.magnitude * 0.3);
      }
    });
    return adjusted;
  }
}

module.exports = { BoundedRationalityEngine };
