/**
 * 前景理论 (Prospect Theory) - Kahneman & Tversky, 1979
 * 用于模拟人类在风险决策中的非理性行为
 */

class ProspectTheoryEngine {
  constructor(params = {}) {
    // 价值函数参数 (基于Kahneman & Tversky 1992的估计)
    this.alpha = params.alpha || 0.88;   // 收益凹度
    this.beta = params.beta || 0.88;     // 损失凸度
    this.lambda = params.lambda || 2.25; // 损失厌恶系数
    
    // 概率加权函数参数 (Tversky & Fox, 1995)
    this.gamma = params.gamma || 0.61;   // 收益概率加权
    this.delta = params.delta || 0.69;   // 损失概率加权
    
    // 参照点
    this.referencePoint = params.referencePoint || 0;
  }

  /**
   * 价值函数 v(x)
   * 参照点依赖、损失厌恶、敏感性递减
   * v(x) = x^α if x≥0; -λ(-x)^β if x<0
   */
  valueFunction(x, referencePoint = null) {
    const rp = referencePoint !== null ? referencePoint : this.referencePoint;
    const delta = x - rp;
    
    if (delta >= 0) {
      // 收益区域: 凹函数 (风险厌恶) - 敏感性递减
      return Math.pow(delta, this.alpha);
    } else {
      // 损失区域: 凸函数且斜率更大 (风险寻求 + 损失厌恶)
      return -this.lambda * Math.pow(-delta, this.beta);
    }
  }

  /**
   * 概率加权函数 w(p) - Prelec形式
   * 高估小概率、低估中高概率
   * w(p) = exp(-(-ln(p))^γ)
   */
  probabilityWeight(p, isGain = true) {
    if (p <= 0) return 0;
    if (p >= 1) return 1;
    const param = isGain ? this.gamma : this.delta;
    return Math.exp(-Math.pow(-Math.log(p), param));
  }

  /**
   * 累积前景理论 (CPT) - 计算 prospects 的总价值
   * prospects: [{probability, outcome, referencePoint}]
   */
  calculateProspectValue(prospects) {
    // 分离收益和损失
    const gains = prospects
      .filter(p => p.outcome >= (p.referencePoint || this.referencePoint))
      .sort((a, b) => b.outcome - a.outcome); // 从高到低
    
    const losses = prospects
      .filter(p => p.outcome < (p.referencePoint || this.referencePoint))
      .sort((a, b) => a.outcome - b.outcome); // 从低到高
    
    let totalValue = 0;
    
    // 计算累积概率权重
    const decisionWeights = (sortedProspects, isGain) => {
      const weights = [];
      let cumProb = 0;
      for (let i = 0; i < sortedProspects.length; i++) {
        const newCumProb = cumProb + sortedProspects[i].probability;
        const w1 = this.probabilityWeight(newCumProb, isGain);
        const w2 = this.probabilityWeight(cumProb, isGain);
        weights.push(w1 - w2);
        cumProb = newCumProb;
      }
      return weights;
    };
    
    // 收益部分 (从高到低)
    const gainWeights = decisionWeights(gains, true);
    gains.forEach((p, i) => {
      totalValue += gainWeights[i] * this.valueFunction(p.outcome, p.referencePoint);
    });
    
    // 损失部分 (从低到高)
    const lossWeights = decisionWeights(losses, false);
    losses.forEach((p, i) => {
      totalValue += lossWeights[i] * this.valueFunction(p.outcome, p.referencePoint);
    });
    
    return totalValue;
  }

  /**
   * 四折模式 (Four-fold Pattern) - 解释彩票和保险
   * 预测人们在不同概率和收益组合下的风险态度
   */
  fourFoldPattern(probability, magnitude) {
    const isGain = magnitude > 0;
    const isSmallProb = probability < 0.3;
    
    if (isGain && isSmallProb) {
      return { 
        behavior: 'risk_seeking', 
        explanation: '彩票偏好 - 高估小概率收益，愿意冒险',
        example: '买彩票、赌小概率高回报'
      };
    } else if (isGain && !isSmallProb) {
      return { 
        behavior: 'risk_averse', 
        explanation: '确定性效应 - 偏好确定收益而非概率收益',
        example: '选择确定获得3000元而非80%概率获得4000元'
      };
    } else if (!isGain && isSmallProb) {
      return { 
        behavior: 'risk_averse', 
        explanation: '保险购买 - 高估小概率损失，愿意支付保费',
        example: '购买保险、支付溢价避免小概率大损失'
      };
    } else {
      return { 
        behavior: 'risk_seeking', 
        explanation: '拒绝确定损失 - 偏好赌一把避免损失',
        example: '确定损失3000元 vs 80%概率损失4000元，选择后者'
      };
    }
  }

  /**
   * 框架效应分析 - 同一问题的不同表述如何影响决策
   */
  analyzeFramingEffect(options, frame = 'neutral') {
    const frames = {
      gain: { multiplier: 1, refShift: 0, description: '正向框架 - 强调收益' },
      loss: { multiplier: 1, refShift: -400, description: '负向框架 - 强调损失' },
      neutral: { multiplier: 1, refShift: 0, description: '中性框架' },
      survival: { multiplier: 1.1, refShift: 100, description: '生存框架 - 强调存活' },
      mortality: { multiplier: 0.9, refShift: -100, description: '死亡框架 - 强调死亡' }
    };
    
    const f = frames[frame] || frames.neutral;
    
    return options.map(opt => {
      const adjustedProspects = opt.prospects.map(p => ({
        ...p,
        outcome: p.outcome * f.multiplier,
        referencePoint: (p.referencePoint || this.referencePoint) + f.refShift
      }));
      
      const prospectValue = this.calculateProspectValue(adjustedProspects);
      const expectedValue = opt.prospects.reduce((sum, p) => sum + p.probability * p.outcome, 0);
      
      return {
        option: opt.name,
        frame: frame,
        frameDescription: f.description,
        prospectValue: prospectValue,
        expectedValue: expectedValue,
        ratio: prospectValue / (expectedValue || 1),
        preference: null // 将在比较后设置
      };
    }).sort((a, b) => b.prospectValue - a.prospectValue);
  }

  /**
   * 禀赋效应 - 人们高估自己拥有的东西
   * 基于损失厌恶：放弃拥有的东西被视为损失
   */
  endowmentEffect(itemValue, ownershipDuration = 0, emotionalAttachment = 0.5) {
    // 拥有时间增加情感依恋
    const timeFactor = 1 + Math.log(1 + ownershipDuration / 365) * 0.1;
    // 情感依恋强化禀赋效应
    const attachmentFactor = 1 + emotionalAttachment * (this.lambda - 1);
    return itemValue * timeFactor * attachmentFactor;
  }

  /**
   * 现状偏见 - 维持现状的额外效用
   */
  statusQuoBias(alternatives, statusQuoIndex = 0, biasStrength = 0.3) {
    const maxValue = Math.max(...alternatives.map(a => a.value));
    return alternatives.map((alt, idx) => ({
      ...alt,
      adjustedValue: alt.value + (idx === statusQuoIndex ? biasStrength * maxValue : 0),
      isStatusQuo: idx === statusQuoIndex
    }));
  }

  /**
   * 生成辩论中的行为偏差检测与建议
   */
  generateDebiasingAdvice(agentContext) {
    const biases = [];
    const { recentDecisions, argumentHistory, emotionalState } = agentContext;
    
    // 检测损失厌恶升级
    const recentLosses = recentDecisions?.filter(d => d.outcome < 0).length || 0;
    if (recentLosses > 2) {
      biases.push({
        type: 'loss_aversion_escalation',
        warning: '连续损失后可能过度冒险以挽回损失',
        advice: '暂停，重新评估参照点，避免追损行为。记住：过去的损失是沉没成本',
        severity: 'high'
      });
    }
    
    // 检测确定性效应
    const certaintyPhrases = ['确定', '肯定', '必然', '绝对', '毫无疑问'];
    const certaintyCount = argumentHistory?.filter(arg => 
      certaintyPhrases.some(p => arg.includes(p))
    ).length || 0;
    if (certaintyCount > 0) {
      biases.push({
        type: 'certainty_effect',
        warning: '过度重视确定性表述，可能低估概率性结果',
        advice: '计算期望值而非依赖确定性。考虑所有可能结果的加权平均',
        severity: 'medium'
      });
    }
    
    // 检测小概率高估
    const smallProbMentions = argumentHistory?.filter(arg => 
      /1%|5%|10%|小概率|万一|可能|或许/.test(arg)
    ).length || 0;
    if (smallProbMentions > 3) {
      biases.push({
        type: 'overweighting_small_probs',
        warning: '可能高估小概率事件的影响',
        advice: '使用实际概率加权而非直觉。小概率事件的实际权重应更低',
        severity: 'medium'
      });
    }
    
    // 检测参照点依赖
    if (emotionalState?.referencePointShift) {
      biases.push({
        type: 'reference_point_dependence',
        warning: '参照点偏移可能导致非理性评估',
        advice: '尝试从不同参照点评估同一问题，检查一致性',
        severity: 'low'
      });
    }
    
    return biases;
  }

  /**
   * 辩论策略建议 - 基于前景理论
   */
  generateDebateStrategy(agentPosition, opponentPosition, topic) {
    const strategies = [];
    
    // 利用损失厌恶
    if (opponentPosition.hasGains) {
      strategies.push({
        tactic: 'loss_frame',
        description: '将对方的收益框架转为损失框架',
        example: '不说"你会获得X"，而说"不采纳将失去X"',
        effectiveness: 'high'
      });
    }
    
    // 利用确定性效应
    if (opponentPosition.uncertainty > 0.3) {
      strategies.push({
        tactic: 'certainty_appeal',
        description: '强调自己方案的确定性',
        example: '提供确定的替代方案，对比对方的不确定方案',
        effectiveness: 'high'
      });
    }
    
    // 利用现状偏见
    strategies.push({
      tactic: 'status_quo_anchor',
      description: '将自己方案设为默认/现状',
      example: '"正如我们一直以来做的..." 或 "行业标准是..."',
      effectiveness: 'medium'
    });
    
    // 针对小概率事件
    if (topic.includes('风险') || topic.includes('安全')) {
      strategies.push({
        tactic: 'small_prob_salience',
        description: '突出小概率但高影响的事件',
        example: '即使概率低，一旦发生后果严重',
        effectiveness: 'medium'
      });
    }
    
    return strategies;
  }
}

module.exports = { ProspectTheoryEngine };
