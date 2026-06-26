/**
 * 博弈论虚拟论坛 - 高级模块集成
 * Game Theory Virtual Forum - Advanced Modules Integration
 * 
 * 整合5个深化方向：
 * 1. 讨价还价 (Bargaining)
 * 2. 信号博弈 (Signaling)
 * 3. 重复博弈/声誉 (Repeated Games)
 * 4. 机制设计 (Mechanism Design)
 * 5. 演化博弈 (Evolutionary)
 */

const AlternatingOfferBargaining = require('./bargaining');
const SignalingGameAnalyzer = require('./signaling');
const RepeatedGameAnalyzer = require('./repeated-games');
const MechanismDesign = require('./mechanism-design');
const EvolutionaryGameDynamics = require('./evolutionary');

class AdvancedGameTheoryEngine {
  constructor(config = {}) {
    this.config = config;
    this.modules = {
      bargaining: null,
      signaling: null,
      repeated: null,
      mechanism: null,
      evolutionary: null
    };
  }

  /**
   * 根据话题自动选择最合适的博弈论工具
   */
  selectTool(topic, context) {
    const toolSelection = {
      bargaining: /谈判|讨价还价|出价|还价|价格|收购|工资/i.test(topic),
      signaling: /信号|类型|隐藏|质量|教育|证书|证明/i.test(topic),
      repeated: /长期|重复|声誉|关系|历史|信任/i.test(topic),
      mechanism: /拍卖|投票|机制|规则|设计|激励/i.test(topic),
      evolutionary: /演化|学习|适应|长期趋势|策略分布/i.test(topic)
    };

    const selectedTools = Object.entries(toolSelection)
      .filter(([tool, match]) => match)
      .map(([tool]) => tool);

    return {
      primaryTool: selectedTools[0] || 'bargaining',
      secondaryTools: selectedTools.slice(1),
      allTools: selectedTools
    };
  }

  /**
   * 综合博弈论分析
   * 应用多个工具进行全方位分析
   */
  async comprehensiveAnalysis(topic, participants, context) {
    const tools = this.selectTool(topic, context);
    const analysis = {
      topic,
      participants,
      toolsUsed: tools.allTools,
      
      // 各模块分析结果
      results: {},
      
      // 综合洞察
      synthesis: null,
      
      // 策略建议
      recommendations: []
    };

    // 1. 讨价还价分析
    if (tools.allTools.includes('bargaining')) {
      this.modules.bargaining = new AlternatingOfferBargaining({
        discountFactors: context.discountFactors,
        outsideOptions: context.outsideOptions,
        totalValue: context.totalValue || 100
      });

      analysis.results.bargaining = {
        rubinstein: this.modules.bargaining.calculateRubinsteinEquilibrium(
          participants[0], participants[1]
        ),
        nash: this.modules.bargaining.calculateNashBargainingSolution(
          participants[0], participants[1]
        ),
        simulation: this.modules.bargaining.simulateBargainingProcess(
          participants[0], participants[1], context.rounds || 5
        )
      };
    }

    // 2. 信号博弈分析
    if (tools.allTools.includes('signaling')) {
      this.modules.signaling = new SignalingGameAnalyzer({
        sender: participants[0],
        receiver: participants[1],
        types: context.types || ['高类型', '低类型'],
        signals: context.signals || ['强信号', '弱信号'],
        actions: context.actions || ['接受', '拒绝'],
        priorBeliefs: context.priorBeliefs,
        signalCosts: context.signalCosts,
        payoffFunctions: context.payoffFunctions
      });

      analysis.results.signaling = {
        equilibria: this.modules.signaling.findPerfectBayesianEquilibria(),
        singleCrossing: this.modules.signaling.verifySingleCrossingProperty()
      };
    }

    // 3. 重复博弈分析
    if (tools.allTools.includes('repeated')) {
      this.modules.repeated = new RepeatedGameAnalyzer({
        players: participants,
        discountFactor: context.discountFactor || 0.9,
        horizon: context.horizon || Infinity,
        reputationTypes: context.reputationTypes
      });

      analysis.results.repeated = {
        triggerStrategies: this.modules.repeated.analyzeTriggerStrategies(),
        folkTheorem: this.modules.repeated.verifyFolkTheorem(),
        reputation: context.reputationAnalysis ? 
          this.modules.repeated.analyzeReputationModel(
            context.reputationPlayer,
            context.stages || 10
          ) : null
      };
    }

    // 4. 机制设计分析
    if (tools.allTools.includes('mechanism')) {
      this.modules.mechanism = new MechanismDesign({
        players: participants,
        typeSpace: context.typeSpace,
        outcomeSpace: context.outcomeSpace
      });

      analysis.results.mechanism = {
        auction: context.auction ?
          this.modules.mechanism.designAuction(
            context.auctionItem,
            context.bidders
          ) : null,
        voting: context.voting ?
          this.modules.mechanism.designVotingMechanism(
            context.alternatives,
            context.voters
          ) : null,
        vcg: context.vcg ?
          this.modules.mechanism.designVCGMechanism(
            context.allocations,
            context.valuations
          ) : null
      };
    }

    // 5. 演化博弈分析
    if (tools.allTools.includes('evolutionary')) {
      this.modules.evolutionary = new EvolutionaryGameDynamics({
        strategies: context.strategies || ['合作', '背叛'],
        payoffMatrix: context.payoffMatrix,
        mutationRate: context.mutationRate || 0.01
      });

      analysis.results.evolutionary = {
        dynamics: this.modules.evolutionary.replicatorDynamics(
          context.initialPopulation || { '合作': 0.5, '背叛': 0.5 },
          context.generations || 1000
        ),
        invasionTests: context.invasionTests ?
          context.invasionTests.map(test =>
            this.modules.evolutionary.simulateInvasion(
              test.incumbent,
              test.mutant,
              test.size
            )
          ) : []
      };
    }

    // 综合洞察
    analysis.synthesis = this.synthesizeInsights(analysis.results);
    
    // 策略建议
    analysis.recommendations = this.generateRecommendations(analysis);

    return analysis;
  }

  /**
   * 综合各模块的洞察
   */
  synthesizeInsights(results) {
    const insights = {
      // 均衡分析
      equilibriumAnalysis: {
        static: results.bargaining?.rubinstein || results.signaling?.equilibria,
        dynamic: results.repeated?.triggerStrategies,
        evolutionary: results.evolutionary?.dynamics?.ESS
      },

      // 效率分析
      efficiency: {
        staticEfficiency: this.assessStaticEfficiency(results),
        dynamicEfficiency: this.assessDynamicEfficiency(results),
        longRunEfficiency: results.evolutionary?.dynamics?.finalPopulation
      },

      // 信息分析
      information: {
        revelation: results.signaling?.equilibria?.separating > 0,
        learning: results.evolutionary?.dynamics?.trajectory,
        commitment: results.bargaining?.commitmentValue
      },

      // 合作可能性
      cooperation: {
        oneShot: results.bargaining?.nash?.efficiency === '帕累托最优',
        repeated: results.repeated?.folkTheorem?.cooperationPossibility,
        evolutionary: results.evolutionary?.dynamics?.ESS?.some(e => 
          e.strategy === '合作' || e.strategy === 'cooperate'
        )
      }
    };

    // 综合结论
    insights.conclusion = this.generateConclusion(insights);

    return insights;
  }

  /**
   * 评估静态效率
   */
  assessStaticEfficiency(results) {
    if (results.mechanism?.vcg) {
      return results.mechanism.vcg.properties.efficient ? 
        'efficient' : 'inefficient';
    }
    
    if (results.bargaining?.nash) {
      return results.bargaining.nash.efficiency;
    }
    
    return 'unknown';
  }

  /**
   * 评估动态效率
   */
  assessDynamicEfficiency(results) {
    if (results.repeated?.folkTheorem) {
      return results.repeated.folkTheorem.cooperationPossibility ?
        'cooperation sustainable' : 'defection dominant';
    }
    
    return 'unknown';
  }

  /**
   * 生成综合结论
   */
  generateConclusion(insights) {
    const conclusions = [];

    // 均衡方面
    if (insights.equilibriumAnalysis.evolutionary) {
      conclusions.push('演化稳定策略存在，长期行为可预测');
    }

    // 效率方面
    if (insights.efficiency.staticEfficiency === '帕累托最优') {
      conclusions.push('静态配置效率达到最优');
    }

    // 合作方面
    if (insights.cooperation.repeated) {
      conclusions.push('重复互动可以促进合作');
    }

    return conclusions;
  }

  /**
   * 生成综合策略建议
   */
  generateRecommendations(analysis) {
    const recommendations = [];

    // 基于讨价还价
    if (analysis.results.bargaining) {
      const rubinstein = analysis.results.bargaining.rubinstein;
      recommendations.push({
        source: 'bargaining',
        priority: 'high',
        content: `根据Rubinstein模型，${rubinstein.proposer.name}应提出${(rubinstein.proposer.share * 100).toFixed(1)}%的份额要求`,
        reasoning: '基于耐心参数的均衡分析'
      });
    }

    // 基于信号博弈
    if (analysis.results.signaling?.singleCrossing?.satisfied) {
      recommendations.push({
        source: 'signaling',
        priority: 'high',
        content: '单交叉性质满足，分离均衡可行',
        reasoning: '高类型参与者可以通过选择高成本信号来可信地传递信息'
      });
    }

    // 基于重复博弈
    if (analysis.results.repeated?.triggerStrategies?.grimTrigger?.cooperationCondition?.condition) {
      recommendations.push({
        source: 'repeated',
        priority: 'high',
        content: '采用冷酷触发策略可以维持合作',
        reasoning: `折现因子满足合作条件: δ ≥ ${analysis.results.repeated.triggerStrategies.grimTrigger.cooperationCondition.threshold}`
      });
    }

    // 基于机制设计
    if (analysis.results.mechanism?.auction) {
      recommendations.push({
        source: 'mechanism',
        priority: 'medium',
        content: `推荐使用${analysis.results.mechanism.auction.recommendation}`,
        reasoning: '真实报价激励相容'
      });
    }

    // 基于演化博弈
    if (analysis.results.evolutionary?.dynamics?.ESS?.length > 0) {
      const ess = analysis.results.evolutionary.dynamics.ESS[0];
      recommendations.push({
        source: 'evolutionary',
        priority: 'medium',
        content: `长期演化趋向于${ess.strategy}策略`,
        reasoning: `${ess.strategy}是演化稳定策略，可以抵抗突变入侵`
      });
    }

    return recommendations;
  }

  /**
   * 生成辩论报告
   */
  generateDebateReport(analysis) {
    const report = {
      title: `博弈论分析报告：${analysis.topic}`,
      
      summary: {
        toolsUsed: analysis.toolsUsed,
        keyFindings: analysis.synthesis.conclusion,
        topRecommendations: analysis.recommendations
          .filter(r => r.priority === 'high')
          .map(r => r.content)
      },

      detailedAnalysis: analysis.results,

      synthesis: analysis.synthesis,

      strategicGuidance: {
        shortTerm: analysis.recommendations
          .filter(r => r.source === 'bargaining' || r.source === 'signaling')
          .map(r => ({ content: r.content, reasoning: r.reasoning })),
        
        mediumTerm: analysis.recommendations
          .filter(r => r.source === 'repeated' || r.source === 'mechanism')
          .map(r => ({ content: r.content, reasoning: r.reasoning })),
        
        longTerm: analysis.recommendations
          .filter(r => r.source === 'evolutionary')
          .map(r => ({ content: r.content, reasoning: r.reasoning }))
      },

      theoreticalFoundation: {
        bargaining: 'Osborne 第7章 / Rubinstein (1982)',
        signaling: 'Spence (1973) / Bonanno 第15章',
        repeated: 'Osborne 第8章 / Kreps-Wilson (1982)',
        mechanism: 'Myerson (1981) / VCG',
        evolutionary: 'Maynard Smith (1982) / Osborne 第3.4节'
      }
    };

    return report;
  }
}

module.exports = {
  AdvancedGameTheoryEngine,
  AlternatingOfferBargaining,
  SignalingGameAnalyzer,
  RepeatedGameAnalyzer,
  MechanismDesign,
  EvolutionaryGameDynamics
};
