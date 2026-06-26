/**
 * 博弈论辩论引擎主入口
 * 整合战略式博弈、贝叶斯博弈、扩展式博弈
 * 
 * 虚拟论坛 v3.5 - 博弈论增强版
 */

const StrategicGame = require('./strategic-game');
const BayesianGame = require('./bayesian-game');
const GameRecognizer = require('./game-recognizer');

class GameTheoryDebateEngine {
  constructor(config = {}) {
    this.recognizer = new GameRecognizer();
    this.currentGame = null;
    this.beliefs = {}; // 信念系统
    this.history = []; // 行动历史
    this.config = {
      maxRounds: config.maxRounds || 10,
      enableBeliefUpdate: config.enableBeliefUpdate !== false,
      showEquilibriumAnalysis: config.showEquilibriumAnalysis !== false,
      ...config
    };
  }

  /**
   * 初始化辩论
   * @param {string} topic - 辩论话题
   * @param {array} participants - 参与者列表
   */
  async initializeDebate(topic, participants) {
    // 1. 识别博弈类型
    const analysis = this.recognizer.analyze(topic, participants);
    this.analysis = analysis;

    // 2. 构建博弈模型
    await this.buildGameModel(analysis, participants);

    // 3. 初始化信念系统（不完全信息博弈）
    this.initializeBeliefs(analysis, participants);

    return {
      analysis,
      gameType: analysis.recommendedGameType,
      initialBeliefs: this.beliefs
    };
  }

  /**
   * 构建博弈模型
   */
  async buildGameModel(analysis, participants) {
    const gameType = analysis.recommendedGameType;

    switch (gameType.type) {
      case 'classic':
        this.currentGame = this.buildClassicGame(gameType.subtype, participants);
        break;
      case 'bayesian':
        this.currentGame = this.buildBayesianGame(participants);
        break;
      case 'extensive':
        // TODO: 实现扩展式博弈
        this.currentGame = this.buildStrategicGame(participants);
        break;
      default:
        this.currentGame = this.buildStrategicGame(participants);
    }
  }

  /**
   * 构建经典博弈模型
   */
  buildClassicGame(subtype, participants) {
    const classicGames = {
      prisonersDilemma: {
        players: participants,
        strategies: {
          [participants[0]]: ['合作', '背叛'],
          [participants[1]]: ['合作', '背叛']
        },
        payoffMatrix: {
          '合作-合作': [3, 3],
          '合作-背叛': [0, 5],
          '背叛-合作': [5, 0],
          '背叛-背叛': [1, 1]
        }
      },

      chickenGame: {
        players: participants,
        strategies: {
          [participants[0]]: ['退让', '坚持'],
          [participants[1]]: ['退让', '坚持']
        },
        payoffMatrix: {
          '退让-退让': [3, 3],
          '退让-坚持': [2, 5],
          '坚持-退让': [5, 2],
          '坚持-坚持': [0, 0]
        }
      },

      stagHunt: {
        players: participants,
        strategies: {
          [participants[0]]: ['猎鹿', '猎兔'],
          [participants[1]]: ['猎鹿', '猎兔']
        },
        payoffMatrix: {
          '猎鹿-猎鹿': [5, 5],
          '猎鹿-猎兔': [0, 3],
          '猎兔-猎鹿': [3, 0],
          '猎兔-猎兔': [3, 3]
        }
      },

      zeroSum: {
        players: participants,
        strategies: {
          [participants[0]]: ['策略A', '策略B'],
          [participants[1]]: ['策略X', '策略Y']
        },
        payoffMatrix: {
          '策略A-策略X': [3, -3],
          '策略A-策略Y': [-1, 1],
          '策略B-策略X': [-2, 2],
          '策略B-策略Y': [1, -1]
        }
      }
    };

    const config = classicGames[subtype] || classicGames.prisonersDilemma;
    return new StrategicGame(config);
  }

  /**
   * 构建标准战略式博弈
   */
  buildStrategicGame(participants) {
    // 默认策略空间
    const strategies = {};
    participants.forEach(p => {
      strategies[p] = ['合作', '对抗', '观望'];
    });

    // 默认收益矩阵（需要根据实际情况调整）
    const payoffMatrix = this.generateDefaultPayoffMatrix(participants, strategies);

    return new StrategicGame({
      players: participants,
      strategies,
      payoffMatrix
    });
  }

  /**
   * 构建贝叶斯博弈
   */
  buildBayesianGame(participants) {
    // 默认类型空间
    const types = {};
    participants.forEach(p => {
      types[p] = ['强硬型', '温和型'];
    });

    // 默认先验信念
    const priorBeliefs = {};
    participants.forEach(p => {
      types[p].forEach(t => {
        priorBeliefs[`${p}-${t}`] = 0.5;
      });
    });

    // 默认策略（类型依赖）
    const strategies = {};
    participants.forEach(p => {
      strategies[p] = {
        '强硬型': ['强硬', '妥协'],
        '温和型': ['妥协', '退让']
      };
    });

    // 收益函数（简化版）
    const payoffFunctions = {};
    participants.forEach(p => {
      payoffFunctions[p] = (strategyProfile, typeProfile) => {
        // 简化的收益计算
        const myType = typeProfile[p];
        const myStrategy = strategyProfile[p];
        
        if (myType === '强硬型' && myStrategy === '强硬') return 5;
        if (myType === '强硬型' && myStrategy === '妥协') return 3;
        if (myType === '温和型' && myStrategy === '妥协') return 4;
        if (myType === '温和型' && myStrategy === '退让') return 2;
        
        return 0;
      };
    });

    return new BayesianGame({
      players: participants,
      types,
      priorBeliefs,
      strategies,
      payoffFunctions
    });
  }

  /**
   * 初始化信念系统
   */
  initializeBeliefs(analysis, participants) {
    if (analysis.gameDimensions.information < 0.5) {
      // 不完全信息：使用先验信念
      participants.forEach(p => {
        this.beliefs[p] = { ...analysis.priorBeliefs };
      });
    } else {
      // 完全信息：确定性的
      participants.forEach(p => {
        this.beliefs[p] = { known: true };
      });
    }
  }

  /**
   * 执行一轮辩论
   * @param {number} round - 轮次
   * @param {object} actions - 各参与者的行动
   */
  async executeRound(round, actions) {
    // 1. 记录行动
    this.history.push({ round, actions });

    // 2. 贝叶斯信念更新（不完全信息博弈）
    if (this.config.enableBeliefUpdate && this.currentGame instanceof BayesianGame) {
      this.updateBeliefs(actions);
    }

    // 3. 分析策略选择
    const strategyAnalysis = this.analyzeStrategies(actions);

    // 4. 检查均衡
    const equilibriumInfo = this.checkEquilibrium();

    return {
      round,
      actions,
      beliefUpdate: this.config.enableBeliefUpdate ? this.beliefs : null,
      strategyAnalysis,
      equilibriumInfo,
      recommendations: this.generateRoundRecommendations(actions)
    };
  }

  /**
   * 更新信念
   */
  updateBeliefs(actions) {
    if (!(this.currentGame instanceof BayesianGame)) return;

    const participants = Object.keys(actions);
    
    for (const observer of participants) {
      for (const observed of participants) {
        if (observer === observed) continue;
        
        const observedAction = actions[observed];
        const priorBeliefs = this.beliefs[observer] || {};
        
        const posterior = this.currentGame.bayesianUpdate(
          observer,
          observed,
          observedAction,
          priorBeliefs
        );
        
        // 更新信念
        this.beliefs[observer] = { ...this.beliefs[observer], ...posterior };
      }
    }
  }

  /**
   * 分析策略选择
   */
  analyzeStrategies(actions) {
    const analysis = {};
    
    for (const [player, action] of Object.entries(actions)) {
      // 检查是否为最佳反应
      const isBestResponse = this.checkBestResponse(player, action);
      
      // 检查是否为均衡策略
      const isEquilibriumStrategy = this.checkEquilibriumStrategy(player, action);
      
      analysis[player] = {
        action,
        isBestResponse,
        isEquilibriumStrategy,
        payoff: this.estimatePayoff(player, action)
      };
    }
    
    return analysis;
  }

  /**
   * 检查最佳反应
   */
  checkBestResponse(player, action) {
    // 简化的检查：对比历史收益
    const playerHistory = this.history.filter(h => h.actions[player] === action);
    const otherHistory = this.history.filter(h => h.actions[player] !== action);
    
    if (playerHistory.length === 0 || otherHistory.length === 0) return null;
    
    const avgPayoffCurrent = playerHistory.reduce((sum, h) => 
      sum + this.estimatePayoff(player, h.actions[player]), 0) / playerHistory.length;
    
    const avgPayoffOther = otherHistory.reduce((sum, h) => 
      sum + this.estimatePayoff(player, h.actions[player]), 0) / otherHistory.length;
    
    return avgPayoffCurrent >= avgPayoffOther;
  }

  /**
   * 检查均衡策略
   */
  checkEquilibriumStrategy(player, action) {
    // 需要求解均衡后对比
    // 简化版：假设当前策略组合是均衡
    return null;
  }

  /**
   * 估计收益
   */
  estimatePayoff(player, action) {
    // 基于当前博弈模型估计收益
    if (this.currentGame instanceof StrategicGame) {
      // 查找历史中的类似情况
      const similar = this.history.filter(h => h.actions[player] === action);
      if (similar.length > 0) {
        // 简化：返回平均收益
        return 3; // 默认中等收益
      }
    }
    return 0;
  }

  /**
   * 检查当前是否处于均衡状态
   */
  checkEquilibrium() {
    if (!this.currentGame) return null;

    if (this.currentGame instanceof StrategicGame) {
      const equilibria = this.currentGame.findPureStrategyNashEquilibrium();
      return {
        type: 'Nash',
        found: equilibria.length > 0,
        count: equilibria.length,
        equilibria: equilibria.slice(0, 3) // 最多显示3个
      };
    }

    if (this.currentGame instanceof BayesianGame) {
      const equilibria = this.currentGame.findBayesianNashEquilibrium();
      return {
        type: 'Bayesian Nash',
        found: equilibria.length > 0,
        count: equilibria.length
      };
    }

    return null;
  }

  /**
   * 生成每轮建议
   */
  generateRoundRecommendations(actions) {
    const recommendations = [];
    
    // 基于信念的建议
    if (this.config.enableBeliefUpdate) {
      for (const [player, beliefs] of Object.entries(this.beliefs)) {
        if (beliefs.known) continue;
        
        const mostLikelyType = Object.entries(beliefs)
          .filter(([k, v]) => k.includes('-'))
          .sort((a, b) => b[1] - a[1])[0];
        
        if (mostLikelyType) {
          recommendations.push({
            target: player,
            type: 'belief',
            content: `基于观察，${player}有${(mostLikelyType[1] * 100).toFixed(1)}%的概率是${mostLikelyType[0].split('-')[1]}`
          });
        }
      }
    }
    
    // 基于均衡的建议
    if (this.config.showEquilibriumAnalysis) {
      const equilibrium = this.checkEquilibrium();
      if (equilibrium && equilibrium.found) {
        recommendations.push({
          type: 'equilibrium',
          content: `当前博弈存在${equilibrium.count}个纳什均衡`
        });
      }
    }
    
    return recommendations;
  }

  /**
   * 生成最终报告
   */
  generateFinalReport() {
    const report = {
      topic: this.analysis.topic,
      participants: this.analysis.participants,
      totalRounds: this.history.length,
      gameType: this.analysis.recommendedGameType,
      finalBeliefs: this.beliefs,
      equilibriumAnalysis: this.performEquilibriumAnalysis(),
      strategicInsights: this.generateStrategicInsights(),
      debateHistory: this.history
    };

    return report;
  }

  /**
   * 执行均衡分析
   */
  performEquilibriumAnalysis() {
    if (!this.currentGame) return null;

    const analysis = {
      type: 'Equilibrium Analysis',
      timestamp: Date.now()
    };

    if (this.currentGame instanceof StrategicGame) {
      // 纯策略均衡
      analysis.pureStrategyEquilibria = this.currentGame.findPureStrategyNashEquilibrium();
      
      // 尝试寻找混合策略均衡
      try {
        analysis.mixedStrategyEquilibria = this.currentGame.findMixedStrategyNashEquilibrium();
      } catch (e) {
        analysis.mixedStrategyError = e.message;
      }
      
      // IEDS分析
      analysis.iesds = this.currentGame.iteratedEliminationOfStrictlyDominatedStrategies();
    }

    if (this.currentGame instanceof BayesianGame) {
      analysis.bayesianEquilibria = this.currentGame.findBayesianNashEquilibrium();
    }

    return analysis;
  }

  /**
   * 生成战略洞察
   */
  generateStrategicInsights() {
    const insights = [];
    
    // 基于历史生成洞察
    const cooperationRate = this.history.filter(h => 
      Object.values(h.actions).includes('合作')
    ).length / this.history.length;
    
    insights.push({
      type: 'behavioral',
      content: `整体合作率: ${(cooperationRate * 100).toFixed(1)}%`
    });

    // 基于均衡生成洞察
    const equilibrium = this.checkEquilibrium();
    if (equilibrium && equilibrium.found) {
      insights.push({
        type: 'equilibrium',
        content: `辩论收敛到${equilibrium.type}均衡`
      });
    }

    return insights;
  }

  /**
   * 生成默认收益矩阵
   */
  generateDefaultPayoffMatrix(participants, strategies) {
    // 简化的2人博弈收益矩阵
    if (participants.length === 2) {
      return {
        '合作-合作': [3, 3],
        '合作-对抗': [0, 5],
        '合作-观望': [1, 2],
        '对抗-合作': [5, 0],
        '对抗-对抗': [1, 1],
        '对抗-观望': [2, 1],
        '观望-合作': [2, 1],
        '观望-对抗': [1, 2],
        '观望-观望': [2, 2]
      };
    }
    
    // 多人博弈：简化处理
    return {};
  }
}

module.exports = GameTheoryDebateEngine;
