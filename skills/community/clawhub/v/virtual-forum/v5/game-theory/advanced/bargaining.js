/**
 * 交替出价讨价还价模型
 * Alternating Offer Bargaining
 * 
 * 基于 Osborne 第7章 / Rubinstein (1982)
 * 
 * 核心概念：
 * - 无限期界讨价还价
 * - 耐心参数 δ (折现因子)
 * - 子博弈完美均衡
 * - 唯一均衡解
 */

class AlternatingOfferBargaining {
  constructor(config = {}) {
    this.discountFactors = config.discountFactors || {}; // δ_i
    this.outsideOptions = config.outsideOptions || {}; // 外部选项
    this.totalValue = config.totalValue || 100;
    this.maxRounds = config.maxRounds || Infinity; // 无限期界或有限期界
    this.bargainingPower = config.bargainingPower || {}; // 议价能力
  }

  /**
   * Rubinstein无限期界讨价还价均衡
   * 
   * 均衡解：
   * - 提议者份额: (1 - δ_2) / (1 - δ_1 * δ_2)
   * - 回应者份额: δ_2 * (1 - δ_1) / (1 - δ_1 * δ_2)
   * 
   * 添加了外部选项约束检查 (Binmore, Rubinstein & Wolinsky 1986)
   */
  calculateRubinsteinEquilibrium(proposer, responder) {
    const delta1 = this.discountFactors[proposer] || 0.9;
    const delta2 = this.discountFactors[responder] || 0.9;
    const outside1 = this.outsideOptions[proposer] || 0;
    const outside2 = this.outsideOptions[responder] || 0;
    
    // 基础Rubinstein解
    let proposerShare = (1 - delta2) / (1 - delta1 * delta2);
    let responderShare = (delta2 * (1 - delta1)) / (1 - delta1 * delta2);
    
    // 转换为绝对值
    let proposerValue = proposerShare * this.totalValue;
    let responderValue = responderShare * this.totalValue;
    
    // 检查外部选项约束
    // 如果一方的均衡收益低于外部选项，该方会选择退出
    const constrained = [];
    
    if (proposerValue < outside1) {
      // 提议者不会接受低于外部选项的份额
      proposerValue = outside1;
      responderValue = this.totalValue - outside1;
      proposerShare = outside1 / this.totalValue;
      responderShare = responderValue / this.totalValue;
      constrained.push(proposer);
    } else if (responderValue < outside2) {
      // 回应者不会接受低于外部选项的份额
      // 注意：在Rubinstein模型中，回应者实际上在第一轮没有提议权
      // 这里简化为提议者必须提供至少outside2给回应者
      responderValue = outside2;
      proposerValue = this.totalValue - outside2;
      responderShare = outside2 / this.totalValue;
      proposerShare = proposerValue / this.totalValue;
      constrained.push(responder);
    }
    
    return {
      type: constrained.length > 0 ? 'Constrained Rubinstein Equilibrium' : 'Rubinstein Equilibrium',
      constrained: constrained.length > 0,
      constrainedBy: constrained,
      
      proposer: {
        name: proposer,
        share: proposerShare,
        value: proposerValue,
        discountFactor: delta1,
        outsideOption: outside1,
        constraintBinding: constrained.includes(proposer)
      },
      
      responder: {
        name: responder,
        share: responderShare,
        value: responderValue,
        discountFactor: delta2,
        outsideOption: outside2,
        constraintBinding: constrained.includes(responder)
      },
      
      agreementRound: constrained.length > 0 ? '受外部选项影响' : 1,
      totalValue: this.totalValue,
      
      // 比较静态分析
      comparativeStatics: {
        patienceEffect: `δ_${proposer}↑ → ${proposer}份额↑`,
        impatiencePenalty: `δ_${responder}↓ → ${responder}被迫接受更低份额`,
        outsideOptionEffect: constrained.length > 0 
          ? `外部选项约束起作用: ${constrained.join(', ')}`
          : '无外部选项约束'
      }
    };
  }

  /**
   * 有限期界讨价还价（逆向归纳）
   * 
   * 最后阶段：提议者拿走全部（没有未来）
   * 倒数第二阶段：回应者接受任何正收益
   * ...
   */
  calculateFiniteHorizonEquilibrium(proposer, responder, rounds) {
    const delta1 = this.discountFactors[proposer] || 0.9;
    const delta2 = this.discountFactors[responder] || 0.9;
    
    // 逆向归纳求解
    let proposerShare, responderShare;
    
    if (rounds === 1) {
      // 最后阶段：提议者优势
      proposerShare = 1;
      responderShare = 0;
    } else if (rounds === 2) {
      // 倒数第二阶段
      proposerShare = 1 - delta2 * 0; // 提议者知道最后阶段回应者得0
      responderShare = 0;
    } else {
      // 多轮递归求解
      const nextRound = this.calculateFiniteHorizonEquilibrium(
        responder, proposer, rounds - 1
      );
      
      // 当前提议者提供的份额使回应者在接受和拒绝之间无差异
      const continuationValue = delta2 * nextRound.proposer.share;
      proposerShare = 1 - continuationValue;
      responderShare = continuationValue;
    }
    
    return {
      type: 'Finite Horizon Equilibrium',
      rounds,
      proposer: {
        name: proposer,
        share: proposerShare,
        value: proposerShare * this.totalValue
      },
      responder: {
        name: responder,
        share: responderShare,
        value: responderShare * this.totalValue
      },
      
      // 收敛到Rubinstein均衡
      convergence: rounds >= 10 ? '接近无限期界均衡' : '偏离无限期界均衡'
    };
  }

  /**
   * 纳什讨价还价解 (Nash Bargaining Solution)
   * 
   * 最大化: (u_1 - d_1)^α * (u_2 - d_2)^(1-α)
 * 
   * 其中 d 是威胁点（外部选项）
   * α 是议价能力
   */
  calculateNashBargainingSolution(player1, player2) {
    const d1 = this.outsideOptions[player1] || 0; // 威胁点
    const d2 = this.outsideOptions[player2] || 0;
    const alpha = this.bargainingPower[player1] || 0.5;
    
    // 纳什解
    const u1 = d1 + alpha * (this.totalValue - d1 - d2);
    const u2 = d2 + (1 - alpha) * (this.totalValue - d1 - d2);
    
    return {
      type: 'Nash Bargaining Solution',
      threatPoint: [d1, d2],
      bargainingPower: { [player1]: alpha, [player2]: 1 - alpha },
      
      [player1]: {
        payoff: u1,
        surplus: u1 - d1, // 合作剩余
        share: u1 / this.totalValue
      },
      
      [player2]: {
        payoff: u2,
        surplus: u2 - d2,
        share: u2 / this.totalValue
      },
      
      // 效率性质
      efficiency: '帕累托最优',
      individualRationality: u1 >= d1 && u2 >= d2 ? '满足' : '不满足',
      symmetry: alpha === 0.5 ? '对称' : '非对称'
    };
  }

  /**
   * Kalai-Smorodinsky讨价还价解
   * 
   * 特点：考虑理想点（乌托邦点）
   */
  calculateKalaiSmorodinskySolution(player1, player2) {
    const d1 = this.outsideOptions[player1] || 0;
    const d2 = this.outsideOptions[player2] || 0;
    
    // 理想点（如果一方获得全部，另一方至少获得威胁点）
    const idealPoint = [this.totalValue - d2, this.totalValue - d1];
    
    // KS解：按比例分配从威胁点到理想点的增益
    const ratio1 = (idealPoint[0] - d1) / idealPoint[0];
    const ratio2 = (idealPoint[1] - d2) / idealPoint[1];
    
    // 找到使两个参与者增益比例相等的分配
    const lambda = Math.min(
      (this.totalValue - d1 - d2) / (idealPoint[0] - d1 + idealPoint[1] - d2),
      1
    );
    
    const u1 = d1 + lambda * (idealPoint[0] - d1);
    const u2 = d2 + lambda * (idealPoint[1] - d2);
    
    return {
      type: 'Kalai-Smorodinsky Solution',
      idealPoint,
      threatPoint: [d1, d2],
      
      [player1]: { payoff: u1, share: u1 / this.totalValue },
      [player2]: { payoff: u2, share: u2 / this.totalValue },
      
      // 单调性性质
      monotonicity: '满足', // KS解的主要优势
      efficiency: '帕累托最优'
    };
  }

  /**
   * 模拟讨价还价过程
   * 追踪每轮出价和信念更新
   */
  simulateBargainingProcess(proposer, responder, actualRounds) {
    const history = [];
    let currentProposer = proposer;
    let currentResponder = responder;
    
    for (let round = 1; round <= actualRounds; round++) {
      // 计算本轮最优出价
      const equilibrium = this.calculateFiniteHorizonEquilibrium(
        currentProposer,
        currentResponder,
        actualRounds - round + 1
      );
      
      const offer = {
        round,
        proposer: currentProposer,
        offerToResponder: equilibrium.responder.value,
        proposerKeeps: equilibrium.proposer.value,
        responderAccepts: true, // 均衡路径上接受
        
        // 偏离分析
        ifReject: {
          responderContinues: this.calculateFiniteHorizonEquilibrium(
            currentResponder,
            currentProposer,
            actualRounds - round
          ),
          explanation: `${currentResponder}拒绝后将在下一轮成为提议者，但需承担折现损失`
        }
      };
      
      history.push(offer);
      
      // 角色交换
      [currentProposer, currentResponder] = [currentResponder, currentProposer];
      
      // 如果达成协议，提前结束
      if (offer.responderAccepts) {
        break;
      }
    }
    
    return {
      history,
      finalAgreement: history[history.length - 1],
      totalRounds: history.length,
      efficiency: history.length === 1 ? '即时协议' : '延迟协议'
    };
  }

  /**
   * 分析承诺策略
   * 如：最后通牒、不可接受选项
   */
  analyzeCommitmentStrategies(player, commitmentType) {
    switch (commitmentType) {
      case 'take-it-or-leave-it':
        // 最后通牒
        return {
          type: 'Ultimatum Game',
          power: '承诺者获得先动优势',
          risk: '如果要求过高，对方选择外部选项',
          optimalDemand: this.outsideOptions[player] + 
            (this.totalValue - this.outsideOptions[player]) * 0.9
        };
        
      case 'walk-away':
        // 可退出威胁
        return {
          type: 'Threat of Walking Away',
          credibility: '取决于外部选项质量',
          effectiveness: this.outsideOptions[player] > 0.3 * this.totalValue 
            ? '高' : '低'
        };
        
      case 'delay':
        // 拖延策略
        return {
          type: 'Strategic Delay',
          condition: '适用于更有耐心的一方',
          effect: `每延迟一轮，${player}的折现损失较小，可以迫使对方让步`
        };
    }
  }

  /**
   * 比较不同讨价还价解
   */
  compareSolutions(player1, player2) {
    const rubinstein = this.calculateRubinsteinEquilibrium(player1, player2);
    const nash = this.calculateNashBargainingSolution(player1, player2);
    const ks = this.calculateKalaiSmorodinskySolution(player1, player2);
    
    return {
      comparison: {
        rubinstein: {
          [player1]: rubinstein.proposer.share,
          [player2]: rubinstein.responder.share,
          feature: '基于耐心和交替出价'
        },
        nash: {
          [player1]: nash[player1].share,
          [player2]: nash[player2].share,
          feature: '最大化纳什积'
        },
        kalaiSmorodinsky: {
          [player1]: ks[player1].share,
          [player2]: ks[player2].share,
          feature: '满足单调性'
        }
      },
      
      recommendations: {
        ifImpatient: '选择Nash解可能更有利',
        ifPatient: 'Rubinstein均衡更有利',
        ifFairnessMatters: 'Kalai-Smorodinsky解更合适'
      }
    };
  }
}

module.exports = AlternatingOfferBargaining;
