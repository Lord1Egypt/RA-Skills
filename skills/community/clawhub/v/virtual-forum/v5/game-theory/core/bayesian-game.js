/**
 * 贝叶斯博弈 (Bayesian Game)
 * 基于 Osborne 第2章 / Bonanno 第14-16章
 * 
 * 不完全信息博弈：参与者有私有类型，通过行动传递信号
 */

class BayesianGame {
  constructor(config) {
    this.players = config.players;
    this.types = config.types; // { '巴菲特': ['强硬型', '温和型'] }
    this.priorBeliefs = config.priorBeliefs; // P(θ)
    this.strategies = config.strategies; // 类型依赖的策略
    this.payoffFunctions = config.payoffFunctions; // u_i(a, θ)
  }

  /**
   * Harsanyi转换：不完全信息 → 不完美信息
   * Osborne 第2章 / Bonanno 第16章
   * 
   * 引入"自然"作为虚拟参与者，先选择类型
   */
  harsanyiTransformation() {
    const natureMoves = this.generateNatureMoves();
    
    return {
      nature: 'Nature',
      natureStrategies: natureMoves,
      probabilities: this.priorBeliefs,
      extensiveForm: this.buildExtensiveForm()
    };
  }

  /**
   * 生成自然的所有类型组合
   */
  generateNatureMoves() {
    const typeArrays = this.players.map(p => 
      this.types[p].map(t => ({ player: p, type: t }))
    );
    
    return this.cartesianProduct(typeArrays);
  }

  /**
   * 构建扩展式博弈树
   */
  buildExtensiveForm() {
    return {
      root: {
        player: 'Nature',
        moves: this.generateNatureMoves().map(move => ({
          move,
          probability: this.calculateProbability(move),
          next: this.buildInformationSets(move)
        }))
      }
    };
  }

  /**
   * 计算类型组合的概率
   * 
   * 使用平滑处理避免0概率问题
   */
  calculateProbability(typeCombination) {
    const MIN_PROBABILITY = 0.001; // 最小概率阈值
    
    let prob = 1;
    for (const { player, type } of typeCombination) {
      const prior = this.priorBeliefs[`${player}-${type}`];
      // 如果未定义或为0，使用最小概率
      const p = (prior !== undefined && prior > 0) ? prior : MIN_PROBABILITY;
      prob *= p;
    }
    
    // 保证返回正数，避免后续除零
    return Math.max(prob, 1e-10);
  }

  /**
   * 构建信息集
   * 同一类型的参与者处于同一信息集
   */
  buildInformationSets(natureMove) {
    const informationSets = {};
    
    for (const { player, type } of natureMove) {
      informationSets[player] = {
        type,
        strategies: this.strategies[player][type],
        // 信息集：不知道其他玩家的具体类型
        information: natureMove.filter(m => m.player !== player)
      };
    }
    
    return informationSets;
  }

  /**
   * 贝叶斯更新信念
   * Bonanno 第9.3节：条件概率与贝叶斯法则
   * 
   * P(类型|行动) = P(行动|类型) * P(类型) / P(行动)
   * 
   * 添加了防止除零的保护
   */
  bayesianUpdate(observer, observedPlayer, observedAction, priorBeliefs) {
    const observedTypes = this.types[observedPlayer];
    const posteriorBeliefs = {};
    const MIN_PROBABILITY = 0.001;
    
    // 计算分母 P(行动)
    let totalProbability = 0;
    for (const type of observedTypes) {
      const likelihood = this.likelihoodOfAction(observedPlayer, type, observedAction);
      const prior = (priorBeliefs[`${observedPlayer}-${type}`] !== undefined) 
        ? priorBeliefs[`${observedPlayer}-${type}`] 
        : MIN_PROBABILITY;
      totalProbability += likelihood * prior;
    }
    
    // 防止除零
    totalProbability = Math.max(totalProbability, 1e-10);
    
    // 计算后验 P(类型|行动)
    for (const type of observedTypes) {
      const likelihood = this.likelihoodOfAction(observedPlayer, type, observedAction);
      const prior = (priorBeliefs[`${observedPlayer}-${type}`] !== undefined) 
        ? priorBeliefs[`${observedPlayer}-${type}`] 
        : MIN_PROBABILITY;
      
      posteriorBeliefs[`${observedPlayer}-${type}`] = (likelihood * prior) / totalProbability;
    }
    
    return posteriorBeliefs;
  }

  /**
   * 计算给定类型下观察到某行动的可能性
   * 基于策略和收益计算
   */
  likelihoodOfAction(player, type, action) {
    const strategies = this.strategies[player][type];
    
    // 如果是最佳反应策略，赋予高概率
    if (this.isBestResponse(player, type, action)) {
      return 0.8;
    }
    
    // 如果是可行策略但非最优，赋予中等概率
    if (strategies.includes(action)) {
      return 0.2 / (strategies.length - 1);
    }
    
    // 否则赋予极低概率（错误/噪音）
    return 0.01;
  }

  /**
   * 检查行动是否为最佳反应
   */
  isBestResponse(player, type, action) {
    // 简化的最佳反应计算
    // 实际应根据期望收益计算
    const strategies = this.strategies[player][type];
    return strategies[0] === action; // 假设第一个策略是最佳反应
  }

  /**
   * 寻找贝叶斯纳什均衡
   * Bonanno 第14章 / Osborne 第2章
   * 
   * 策略组合 σ 是BNE当且仅当：
   * 对每个参与者i，每个类型θ_i，σ_i(θ_i) 是对 σ_{-i} 的最佳反应
   */
  findBayesianNashEquilibrium() {
    const equilibria = [];
    
    // 生成所有可能的策略组合
    const strategyProfiles = this.generateStrategyProfiles();
    
    for (const profile of strategyProfiles) {
      if (this.isBayesianNashEquilibrium(profile)) {
        equilibria.push({
          profile,
          expectedPayoffs: this.calculateExpectedPayoffs(profile)
        });
      }
    }
    
    return equilibria;
  }

  /**
   * 检查是否为贝叶斯纳什均衡
   */
  isBayesianNashEquilibrium(profile) {
    for (const player of this.players) {
      for (const type of this.types[player]) {
        const currentStrategy = profile[player][type];
        const currentExpectedPayoff = this.expectedPayoffForType(
          player, type, currentStrategy, profile
        );
        
        // 检查所有其他策略
        for (const alternativeStrategy of this.strategies[player][type]) {
          if (alternativeStrategy === currentStrategy) continue;
          
          const alternativeExpectedPayoff = this.expectedPayoffForType(
            player, type, alternativeStrategy, profile
          );
          
          if (alternativeExpectedPayoff > currentExpectedPayoff + 1e-9) {
            return false;
          }
        }
      }
    }
    return true;
  }

  /**
   * 计算某类型采用某策略的期望收益
   */
  expectedPayoffForType(player, type, strategy, profile) {
    let expectedPayoff = 0;
    
    // 对所有其他参与者的类型组合求期望
    const otherPlayers = this.players.filter(p => p !== player);
    const typeCombinations = this.generateTypeCombinations(otherPlayers);
    
    for (const typeCombo of typeCombinations) {
      const probability = this.calculateTypeComboProbability(typeCombo);
      const payoff = this.calculatePayoff(player, type, strategy, typeCombo, profile);
      expectedPayoff += probability * payoff;
    }
    
    return expectedPayoff;
  }

  /**
   * 生成类型组合
   */
  generateTypeCombinations(players) {
    if (players.length === 0) return [[]];
    
    const [first, ...rest] = players;
    const restCombinations = this.generateTypeCombinations(rest);
    const combinations = [];
    
    for (const type of this.types[first]) {
      for (const combo of restCombinations) {
        combinations.push([{ player: first, type }, ...combo]);
      }
    }
    
    return combinations;
  }

  /**
   * 计算类型组合的概率
   */
  calculateTypeComboProbability(typeCombo) {
    let prob = 1;
    for (const { player, type } of typeCombo) {
      prob *= this.priorBeliefs[`${player}-${type}`] || 0.5;
    }
    return prob;
  }

  /**
   * 计算收益
   */
  calculatePayoff(player, playerType, playerStrategy, othersTypeCombo, profile) {
    // 构建完整的类型组合
    const typeProfile = { [player]: playerType };
    othersTypeCombo.forEach(({ player: p, type }) => {
      typeProfile[p] = type;
    });
    
    // 构建策略组合
    const strategyProfile = { [player]: playerStrategy };
    othersTypeCombo.forEach(({ player: p, type }) => {
      strategyProfile[p] = profile[p][type];
    });
    
    // 计算收益
    return this.payoffFunctions[player](strategyProfile, typeProfile);
  }

  /**
   * 生成所有策略组合
   */
  generateStrategyProfiles() {
    const playerStrategies = {};
    
    for (const player of this.players) {
      playerStrategies[player] = this.generatePlayerStrategies(player);
    }
    
    return this.combinePlayerStrategies(playerStrategies);
  }

  /**
   * 生成某参与者的所有类型依赖策略
   */
  generatePlayerStrategies(player) {
    const typeStrategies = this.types[player].map(type => 
      this.strategies[player][type]
    );
    
    const combinations = this.cartesianProduct(typeStrategies);
    
    return combinations.map(combo => {
      const strategy = {};
      this.types[player].forEach((type, i) => {
        strategy[type] = combo[i];
      });
      return strategy;
    });
  }

  /**
   * 组合所有参与者的策略
   */
  combinePlayerStrategies(playerStrategies) {
    const players = Object.keys(playerStrategies);
    const arrays = players.map(p => playerStrategies[p]);
    const combinations = this.cartesianProduct(arrays);
    
    return combinations.map(combo => {
      const profile = {};
      players.forEach((p, i) => {
        profile[p] = combo[i];
      });
      return profile;
    });
  }

  /**
   * 计算均衡的期望收益
   */
  calculateExpectedPayoffs(profile) {
    const expectedPayoffs = {};
    
    for (const player of this.players) {
      let totalPayoff = 0;
      
      for (const type of this.types[player]) {
        const typeProbability = this.priorBeliefs[`${player}-${type}`] || 0.5;
        const typeExpectedPayoff = this.expectedPayoffForType(
          player, type, profile[player][type], profile
        );
        totalPayoff += typeProbability * typeExpectedPayoff;
      }
      
      expectedPayoffs[player] = totalPayoff;
    }
    
    return expectedPayoffs;
  }

  /**
   * 信号传递分析
   * 用于分析分离均衡 vs 混同均衡
   */
  analyzeSignaling(player, action, priorBeliefs) {
    const types = this.types[player];
    const analysis = {};
    
    for (const type of types) {
      const likelihood = this.likelihoodOfAction(player, type, action);
      const prior = priorBeliefs[`${player}-${type}`] || 0.5;
      
      analysis[type] = {
        likelihood,
        prior,
        isEquilibriumStrategy: this.isBestResponse(player, type, action)
      };
    }
    
    // 判断是分离均衡还是混同均衡
    const equilibriumTypes = types.filter(t => analysis[t].isEquilibriumStrategy);
    
    if (equilibriumTypes.length === 1) {
      analysis.equilibriumType = 'separating'; // 分离均衡
    } else if (equilibriumTypes.length === types.length) {
      analysis.equilibriumType = 'pooling'; // 混同均衡
    } else {
      analysis.equilibriumType = 'semi-separating'; // 半分离均衡
    }
    
    return analysis;
  }

  // 辅助方法
  cartesianProduct(arrays) {
    if (arrays.length === 0) return [[]];
    if (arrays.length === 1) return arrays[0].map(a => [a]);
    
    const result = [];
    const [first, ...rest] = arrays;
    const restProduct = this.cartesianProduct(rest);
    
    for (const item of first) {
      for (const combo of restProduct) {
        result.push([item, ...combo]);
      }
    }
    return result;
  }
}

module.exports = BayesianGame;
