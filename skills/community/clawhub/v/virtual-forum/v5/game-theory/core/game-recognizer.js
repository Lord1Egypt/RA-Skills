/**
 * 博弈识别器 (Game Recognizer)
 * 自动分析话题，识别适合的博弈模型
 * 
 * 基于教材中的标准博弈类型分类
 */

class GameRecognizer {
  constructor() {
    // 博弈类型定义
    this.gameTypes = {
      // 合作博弈 vs 非合作博弈
      cooperative: {
        name: '合作博弈',
        description: '可以达成有约束力的协议',
        examples: ['联盟形成', '收益分配', '集体决策'],
        solutionConcepts: ['核心', '夏普利值', '讨价还价解']
      },
      
      nonCooperative: {
        name: '非合作博弈',
        description: '个体理性决策，无法强制协议',
        examples: ['价格战', '军备竞赛', '拍卖'],
        solutionConcepts: ['纳什均衡', '子博弈完美均衡']
      },

      // 完全信息 vs 不完全信息
      completeInfo: {
        name: '完全信息博弈',
        description: '所有参与者知道所有信息',
        examples: ['象棋', '公开拍卖'],
        solutionConcepts: ['纳什均衡', '逆向归纳']
      },

      incompleteInfo: {
        name: '不完全信息博弈',
        description: '参与者有私有信息',
        examples: ['谈判', '拍卖', '信号传递'],
        solutionConcepts: ['贝叶斯纳什均衡', '完美贝叶斯均衡']
      },

      // 静态 vs 动态
      static: {
        name: '静态博弈',
        description: '同时行动或不知道对方行动',
        examples: ['囚徒困境', '石头剪刀布'],
        solutionConcepts: ['纳什均衡']
      },

      dynamic: {
        name: '动态博弈',
        description: '序贯行动，可以看到历史',
        examples: ['讨价还价', '下棋', '谈判'],
        solutionConcepts: ['子博弈完美均衡', '序贯均衡']
      }
    };

    // 经典博弈模式库
    this.classicGames = {
      prisonersDilemma: {
        name: '囚徒困境',
        pattern: /囚徒|合作.*背叛|个体.*集体|短期.*长期/i,
        payoffStructure: 'T > R > P > S',
        characteristics: ['占优策略均衡非帕累托最优', '重复博弈可促进合作'],
        examples: ['价格战', '军备竞赛', '环境保护']
      },

      chickenGame: {
        name: '懦夫博弈',
        pattern: /胆小鬼|退让|坚持.*危险|谁先眨眼/i,
        payoffStructure: '赢 > 和 > 输 > 撞',
        characteristics: ['多个均衡', '先承诺者优势'],
        examples: ['核威慑', '商业对峙', '政治僵局']
      },

      stagHunt: {
        name: '猎鹿博弈',
        pattern: /猎鹿|协调|信任|高风险高回报|安全.*冒险/i,
        payoffStructure: '合作 > 单独 > 背叛',
        characteristics: ['协调博弈', '风险占优vs收益占优'],
        examples: ['技术标准化', '联合投资', '联盟形成']
      },

      zeroSum: {
        name: '零和博弈',
        pattern: /零和|赢家.*输家|分配.*固定|竞争.*资源/i,
        payoffStructure: '总和为零',
        characteristics: ['严格竞争', ' minimax解'],
        examples: ['扑克', '选举', '市场份额争夺']
      },

      signaling: {
        name: '信号博弈',
        pattern: /信号|类型|隐藏.*信息|教育|证书|发信号/i,
        structure: '发送者-接收者-行动',
        characteristics: ['分离均衡', '混同均衡', '信息租金'],
        examples: ['教育信号', '质量认证', '谈判']
      },

      bargaining: {
        name: '讨价还价博弈',
        pattern: /谈判|讨价还价|分配|出价|还价|最后通牒/i,
        structure: '交替出价或纳什讨价还价',
        characteristics: ['耐心优势', '风险厌恶', '外部选项'],
        examples: ['工资谈判', '并购', '贸易协定']
      },

      auction: {
        name: '拍卖博弈',
        pattern: /拍卖|出价.*最高|密封.*投标|英式.*荷兰式/i,
        types: ['第一价格', '第二价格', '全支付'],
        characteristics: ['真实报价激励', '收益等价定理'],
        examples: ['艺术品拍卖', '频谱拍卖', '广告位拍卖']
      }
    };
  }

  /**
   * 分析话题，识别博弈类型
   * @param {string} topic - 讨论话题
   * @param {array} participants - 参与者列表
   */
  analyze(topic, participants) {
    const analysis = {
      topic,
      participants,
      detectedPatterns: [],
      recommendedGameType: null,
      classicGameMatch: null,
      complexity: 'medium',
      recommendations: []
    };

    // 1. 检测经典博弈模式
    for (const [key, game] of Object.entries(this.classicGames)) {
      if (game.pattern.test(topic)) {
        analysis.detectedPatterns.push({
          type: key,
          name: game.name,
          confidence: this.calculateConfidence(topic, game.pattern)
        });
      }
    }

    // 2. 排序并选择最可能的模式
    if (analysis.detectedPatterns.length > 0) {
      analysis.detectedPatterns.sort((a, b) => b.confidence - a.confidence);
      analysis.classicGameMatch = analysis.detectedPatterns[0];
    }

    // 3. 分析博弈维度
    analysis.gameDimensions = this.analyzeDimensions(topic, participants);

    // 4. 推荐博弈模型
    analysis.recommendedGameType = this.recommendGameType(analysis);

    // 5. 生成建议
    analysis.recommendations = this.generateRecommendations(analysis);

    return analysis;
  }

  /**
   * 计算模式匹配置信度
   */
  calculateConfidence(topic, pattern) {
    const matches = topic.match(pattern);
    if (!matches) return 0;
    
    // 基于匹配数量和位置计算置信度
    let confidence = Math.min(matches.length * 0.3, 0.9);
    
    // 如果在话题开头匹配，增加置信度
    if (topic.search(pattern) < topic.length * 0.3) {
      confidence += 0.1;
    }
    
    return Math.min(confidence, 1.0);
  }

  /**
   * 分析博弈维度
   */
  analyzeDimensions(topic, participants) {
    const dimensions = {
      // 合作性维度
      cooperation: this.scoreCooperation(topic),
      
      // 信息维度
      information: this.scoreInformationCompleteness(topic),
      
      // 时间维度
      timing: this.scoreTiming(topic),
      
      // 对称性维度
      symmetry: this.scoreSymmetry(participants),
      
      // 重复性维度
      repetition: this.scoreRepetition(topic)
    };

    return dimensions;
  }

  /**
   * 评分：合作性
   */
  scoreCooperation(topic) {
    const cooperationIndicators = ['合作', '联盟', '共同', '双赢', '协调', '协议'];
    const competitionIndicators = ['竞争', '对抗', '击败', '战胜', '零和', '独赢'];
    
    let cooperationScore = 0;
    let competitionScore = 0;
    
    for (const indicator of cooperationIndicators) {
      if (topic.includes(indicator)) cooperationScore++;
    }
    
    for (const indicator of competitionIndicators) {
      if (topic.includes(indicator)) competitionScore++;
    }
    
    const total = cooperationScore + competitionScore;
    if (total === 0) return 0.5; // 中性
    
    return cooperationScore / total;
  }

  /**
   * 评分：信息完全性
   */
  scoreInformationCompleteness(topic) {
    const incompleteIndicators = ['不知道', '隐藏', '秘密', '私有', '类型', '信号'];
    const completeIndicators = ['公开', '透明', '完全信息', '共同知识'];
    
    let incompleteScore = 0;
    let completeScore = 0;
    
    for (const indicator of incompleteIndicators) {
      if (topic.includes(indicator)) incompleteScore++;
    }
    
    for (const indicator of completeIndicators) {
      if (topic.includes(indicator)) completeScore++;
    }
    
    if (incompleteScore > 0) return 0.3; // 不完全信息
    if (completeScore > 0) return 0.9; // 完全信息
    return 0.7; // 默认接近完全信息
  }

  /**
   * 评分：时间结构
   */
  scoreTiming(topic) {
    const dynamicIndicators = ['先', '后', '轮流', '阶段', '步骤', '动态', '序列'];
    const staticIndicators = ['同时', '一次性', '静态'];
    
    for (const indicator of dynamicIndicators) {
      if (topic.includes(indicator)) return 0.8; // 动态
    }
    
    for (const indicator of staticIndicators) {
      if (topic.includes(indicator)) return 0.2; // 静态
    }
    
    return 0.5; // 不确定
  }

  /**
   * 评分：对称性
   */
  scoreSymmetry(participants) {
    // 基于参与者数量和特征判断对称性
    if (participants.length === 2) {
      return 0.7; // 2人博弈通常较对称
    }
    return 0.4; // 多人博弈往往不对称
  }

  /**
   * 评分：重复性
   */
  scoreRepetition(topic) {
    const repeatedIndicators = ['长期', '重复', '多次', '关系', '声誉', '未来'];
    const oneShotIndicators = ['一次', '单次', '短期', '一次性'];
    
    for (const indicator of repeatedIndicators) {
      if (topic.includes(indicator)) return 0.8;
    }
    
    for (const indicator of oneShotIndicators) {
      if (topic.includes(indicator)) return 0.2;
    }
    
    return 0.5;
  }

  /**
   * 推荐博弈类型
   */
  recommendGameType(analysis) {
    const dims = analysis.gameDimensions;
    
    // 基于检测到的经典模式
    if (analysis.classicGameMatch && analysis.classicGameMatch.confidence > 0.6) {
      return {
        type: 'classic',
        subtype: analysis.classicGameMatch.type,
        name: analysis.classicGameMatch.name,
        confidence: analysis.classicGameMatch.confidence
      };
    }
    
    // 基于维度分析
    if (dims.information < 0.5) {
      return {
        type: 'bayesian',
        description: '不完全信息博弈',
        solutionConcept: '贝叶斯纳什均衡'
      };
    }
    
    if (dims.timing > 0.6) {
      return {
        type: 'extensive',
        description: '动态博弈',
        solutionConcept: '子博弈完美均衡'
      };
    }
    
    if (dims.cooperation > 0.7) {
      return {
        type: 'cooperative',
        description: '合作博弈',
        solutionConcept: '核心或夏普利值'
      };
    }
    
    // 默认：标准战略式博弈
    return {
      type: 'strategic',
      description: '标准战略式博弈',
      solutionConcept: '纳什均衡'
    };
  }

  /**
   * 生成实施建议
   */
  generateRecommendations(analysis) {
    const recommendations = [];
    const dims = analysis.gameDimensions;

    // 结构建议
    if (dims.information < 0.5) {
      recommendations.push({
        type: 'structure',
        priority: 'high',
        content: '设置类型空间和先验信念，使用Harsanyi转换'
      });
    }

    if (dims.timing > 0.6) {
      recommendations.push({
        type: 'structure',
        priority: 'high',
        content: '使用扩展式博弈表示，考虑逆向归纳求解'
      });
    }

    // 分析建议
    if (analysis.classicGameMatch) {
      const game = this.classicGames[analysis.classicGameMatch.type];
      recommendations.push({
        type: 'analysis',
        priority: 'medium',
        content: `这是典型的${game.name}，收益结构：${game.payoffStructure}`
      });
    }

    // 均衡建议
    if (dims.repetition > 0.6) {
      recommendations.push({
        type: 'equilibrium',
        priority: 'medium',
        content: '考虑民间定理，可能存在多个均衡，关注声誉机制'
      });
    }

    return recommendations;
  }

  /**
   * 生成博弈描述
   */
  generateGameDescription(analysis) {
    const lines = [];
    
    lines.push(`# 博弈分析`);
    lines.push(`## 话题: ${analysis.topic}`);
    lines.push(`## 识别结果`);
    
    if (analysis.classicGameMatch) {
      const game = this.classicGames[analysis.classicGameMatch.type];
      lines.push(`- 经典博弈: ${game.name} (置信度: ${(analysis.classicGameMatch.confidence * 100).toFixed(1)}%)`);
      lines.push(`- 典型例子: ${game.examples.join(', ')}`);
    }
    
    lines.push(`## 博弈特征`);
    const dims = analysis.gameDimensions;
    lines.push(`- 合作性: ${(dims.cooperation * 100).toFixed(0)}%`);
    lines.push(`- 信息完全性: ${(dims.information * 100).toFixed(0)}%`);
    lines.push(`- 动态性: ${(dims.timing * 100).toFixed(0)}%`);
    lines.push(`- 重复性: ${(dims.repetition * 100).toFixed(0)}%`);
    
    lines.push(`## 建议`);
    for (const rec of analysis.recommendations) {
      lines.push(`- [${rec.priority.toUpperCase()}] ${rec.content}`);
    }
    
    return lines.join('\n');
  }
}

module.exports = GameRecognizer;
