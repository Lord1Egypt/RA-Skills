/**
 * 助推理论 (Nudge Theory) - Thaler & Sunstein, 2008
 * 选择架构与行为干预策略
 */

class NudgeTheoryEngine {
  constructor(params = {}) {
    // 默认选项设置
    this.defaultOptions = params.defaultOptions || {};
    // 选择架构参数
    this.architectureConfig = params.architectureConfig || {
      orderEffects: true,
      framing: 'neutral',
      socialProof: true,
      feedbackLoops: true
    };
    // 干预强度
    this.nudgeIntensity = params.nudgeIntensity || 0.5; // 0-1
  }

  /**
   * 选择架构设计 (Choice Architecture)
   * 通过环境设计影响决策而不限制选择
   */
  designChoiceArchitecture(options, config = {}) {
    const {
      defaultOption = null,
      orderBy = 'neutral', // 'neutral', 'popularity', 'complexity'
      frame = 'neutral',   // 'gain', 'loss', 'social', 'neutral'
      simplify = false,
      highlight = []
    } = config;

    let arrangedOptions = [...options];

    // 1. 默认选项设置
    if (defaultOption) {
      arrangedOptions = arrangedOptions.map(opt => ({
        ...opt,
        isDefault: opt.id === defaultOption,
        defaultBoost: opt.id === defaultOption ? 0.3 : 0
      }));
    }

    // 2. 排序效应
    if (orderBy === 'popularity') {
      arrangedOptions.sort((a, b) => (b.popularity || 0) - (a.popularity || 0));
    } else if (orderBy === 'complexity') {
      arrangedOptions.sort((a, b) => (a.complexity || 0.5) - (b.complexity || 0.5));
    }
    // 添加位置效应
    arrangedOptions = arrangedOptions.map((opt, idx) => ({
      ...opt,
      position: idx,
      positionEffect: this._calculatePositionEffect(idx, arrangedOptions.length)
    }));

    // 3. 框架设计
    arrangedOptions = arrangedOptions.map(opt => ({
      ...opt,
      framedDescription: this._applyFrame(opt.description, frame, opt),
      frameType: frame
    }));

    // 4. 简化选项
    if (simplify && arrangedOptions.length > 5) {
      const recommended = arrangedOptions.slice(0, 3);
      const others = { id: 'others', label: '其他选项...', options: arrangedOptions.slice(3) };
      arrangedOptions = [...recommended, others];
    }

    // 5. 高亮推荐
    if (highlight.length > 0) {
      arrangedOptions = arrangedOptions.map(opt => ({
        ...opt,
        isHighlighted: highlight.includes(opt.id),
        highlightBoost: highlight.includes(opt.id) ? 0.2 : 0
      }));
    }

    return {
      options: arrangedOptions,
      architecture: config,
      expectedChoice: this._predictChoice(arrangedOptions),
      nudgeStrength: this._calculateNudgeStrength(arrangedOptions)
    };
  }

  /**
   * 默认选项效应 (Default Effect)
   * 利用现状偏见和惰性
   */
  applyDefaultEffect(options, defaultId, optOut = false) {
    return options.map(opt => {
      const isDefault = opt.id === defaultId;
      return {
        ...opt,
        isDefault,
        // 默认选项获得显著偏好提升
        preferenceBoost: isDefault ? (optOut ? 0.2 : 0.4) : 0,
        // 主动退出增加摩擦
        friction: isDefault && optOut ? 0.3 : 0,
        description: isDefault 
          ? `${opt.description} (推荐)` 
          : opt.description
      };
    });
  }

  /**
   * 社会规范助推 (Social Norm Nudge)
   * 利用从众心理
   */
  applySocialNorm(options, participationRate = 0.7, trend = 'increasing') {
    const trendEmoji = trend === 'increasing' ? '📈' : trend === 'decreasing' ? '📉' : '➡️';
    
    return options.map(opt => {
      const socialProof = opt.popularity || 0.5;
      return {
        ...opt,
        socialNorm: {
          participationRate,
          trend,
          message: `${participationRate * 100}%的人选择了此选项 ${trendEmoji}`,
          peerComparison: socialProof > 0.6 ? 'above_average' : socialProof < 0.4 ? 'below_average' : 'average'
        },
        socialBoost: socialProof * 0.25 // 社会证明的偏好提升
      };
    });
  }

  /**
   * 框架效应应用 (Framing)
   * 增益框架 vs 损失框架
   */
  applyFraming(options, frameType = 'gain') {
    const frames = {
      gain: {
        prefix: '获得',
        suffix: '的收益',
        emphasis: '机会',
        color: 'green'
      },
      loss: {
        prefix: '避免',
        suffix: '的损失',
        emphasis: '风险',
        color: 'red'
      },
      social: {
        prefix: '加入',
        suffix: '的群体',
        emphasis: '归属',
        color: 'blue'
      },
      neutral: {
        prefix: '',
        suffix: '',
        emphasis: '',
        color: 'gray'
      }
    };

    const f = frames[frameType];
    
    return options.map(opt => ({
      ...opt,
      framedLabel: f.prefix + opt.label + f.suffix,
      framedDescription: this._reframeDescription(opt.description, frameType),
      frameType,
      frameEmphasis: f.emphasis,
      // 增益框架促进风险厌恶，损失框架促进风险寻求
      riskAttitudeShift: frameType === 'gain' ? -0.2 : frameType === 'loss' ? 0.2 : 0
    }));
  }

  /**
   * 反馈机制 (Feedback Mechanisms)
   * 提供行为反馈以促进改变
   */
  designFeedback(currentBehavior, targetBehavior, config = {}) {
    const {
      frequency = 'immediate', // 'immediate', 'daily', 'weekly'
      comparison = 'self',     // 'self', 'social', 'target'
      visualization = 'simple' // 'simple', 'detailed', 'gamified'
    } = config;

    const gap = targetBehavior - currentBehavior;
    const progress = currentBehavior / targetBehavior;

    const feedbackTypes = [];

    // 即时反馈
    if (frequency === 'immediate') {
      feedbackTypes.push({
        type: 'immediate',
        trigger: 'action',
        message: gap > 0 
          ? `距离目标还差 ${(gap * 100).toFixed(1)}%` 
          : `已达成目标！🎉`
      });
    }

    // 社会比较
    if (comparison === 'social') {
      feedbackTypes.push({
        type: 'social_comparison',
        message: `您超过了 ${(progress * 100).toFixed(0)}% 的用户`,
        percentile: progress * 100
      });
    }

    // 自我比较
    if (comparison === 'self') {
      feedbackTypes.push({
        type: 'self_comparison',
        trend: progress > 0.5 ? 'improving' : 'needs_work',
        message: progress > 0.5 ? '比上周进步！' : '需要更多努力'
      });
    }

    // 游戏化
    if (visualization === 'gamified') {
      feedbackTypes.push({
        type: 'gamification',
        points: Math.floor(currentBehavior * 100),
        level: Math.floor(progress * 5) + 1,
        badges: progress > 0.8 ? ['high_achiever'] : progress > 0.5 ? ['on_track'] : []
      });
    }

    return {
      currentBehavior,
      targetBehavior,
      gap,
      progress,
      feedback: feedbackTypes,
      recommendation: this._generateRecommendation(gap, progress)
    };
  }

  /**
   * 承诺机制 (Commitment Devices)
   * 利用承诺一致性原理
   */
  designCommitmentDevice(behavior, commitmentLevel = 'soft') {
    const devices = {
      soft: {
        type: 'public_commitment',
        mechanism: '公开承诺，利用社会压力',
        cost: 0,
        effectiveness: 0.3,
        example: '在社交媒体上宣布目标'
      },
      medium: {
        type: 'accountability_partner',
        mechanism: '问责伙伴，定期检查',
        cost: 0.1,
        effectiveness: 0.5,
        example: '找朋友监督进度'
      },
      hard: {
        type: 'financial_stake',
        mechanism: '金钱承诺，失败有代价',
        cost: 0.3,
        effectiveness: 0.7,
        example: '设定失败罚金或押金'
      },
      extreme: {
        type: 'binding_commitment',
        mechanism: '绑定承诺，不可逆',
        cost: 0.5,
        effectiveness: 0.85,
        example: '自动扣款、锁定账户'
      }
    };

    return devices[commitmentLevel] || devices.soft;
  }

  /**
   * 简化复杂选择 (Simplification)
   * 减少认知负荷
   */
  simplifyChoice(complexOptions, strategy = 'categorization') {
    if (strategy === 'categorization') {
      // 按类别分组
      const categories = {};
      complexOptions.forEach(opt => {
        const cat = opt.category || '其他';
        if (!categories[cat]) categories[cat] = [];
        categories[cat].push(opt);
      });
      
      return Object.entries(categories).map(([cat, opts]) => ({
        category: cat,
        options: opts,
        recommended: opts.find(o => o.recommended) || opts[0],
        count: opts.length
      }));
    }

    if (strategy === 'tiered') {
      // 分层展示：推荐 -> 其他
      const recommended = complexOptions.filter(o => o.recommended || o.popular);
      const others = complexOptions.filter(o => !o.recommended && !o.popular);
      
      return [
        { tier: '推荐', options: recommended },
        { tier: '其他选择', options: others.slice(0, 3), more: others.length > 3 }
      ];
    }

    if (strategy === 'wizard') {
      // 向导式：分步决策
      return {
        type: 'wizard',
        steps: [
          { question: '您的主要目标是什么？', options: this._extractDimensions(complexOptions, 'goal') },
          { question: '您的预算是？', options: this._extractDimensions(complexOptions, 'budget') },
          { question: '您的时间安排？', options: this._extractDimensions(complexOptions, 'time') }
        ],
        finalRecommendation: null // 根据选择动态生成
      };
    }

    return complexOptions;
  }

  /**
   * 辩论中的助推策略
   * 用于虚拟论坛的说服技巧
   */
  generateDebateNudges(agentPosition, audienceProfile = {}) {
    const nudges = [];
    const { riskAverse, socialConscious, timePressed } = audienceProfile;

    // 针对风险厌恶者
    if (riskAverse) {
      nudges.push({
        tactic: 'default_anchor',
        description: '将自己的立场设为"标准做法"或"默认选择"',
        example: '"正如行业惯例..." 或 "大多数专家都同意..."',
        target: 'risk_averse'
      });
    }

    // 针对社会意识
    if (socialConscious) {
      nudges.push({
        tactic: 'social_proof',
        description: '引用社会规范和同行行为',
        example: '"90%的同行都支持这一观点" 或 "领先机构都采用..."',
        target: 'social_conscious'
      });
    }

    // 针对时间压力
    if (timePressed) {
      nudges.push({
        tactic: 'simplified_frame',
        description: '提供简化框架，减少认知负荷',
        example: '"关键只有三点：A、B、C" 或 "简而言之..."',
        target: 'time_pressed'
      });
    }

    // 通用助推
    nudges.push({
      tactic: 'loss_frame',
      description: '将不采纳自己观点框架为损失',
      example: '"如果不这样做，我们将失去..." 而非 "这样做能获得..."',
      target: 'universal'
    });

    nudges.push({
      tactic: 'immediate_feedback',
      description: '提供即时、具体的反馈',
      example: '"这个观点已经被数据证实" 并立即展示证据',
      target: 'universal'
    });

    return nudges;
  }

  /**
   * 检测和对抗不良助推
   */
  detectDarkNudges(argument) {
    const darkPatterns = [];

    // 隐藏选项
    if (/显然|毫无疑问|只能|必须/.test(argument)) {
      darkPatterns.push({
        type: 'hidden_options',
        description: '隐藏或淡化其他选择',
        counter: '明确列出所有可行选项，包括被忽略的'
      });
    }

    // 误导性框架
    if (/大家都|所有人|从来没有人/.test(argument)) {
      darkPatterns.push({
        type: 'false_social_proof',
        description: '虚假的社会证明',
        counter: '要求具体数据来源，质疑统计有效性'
      });
    }

    // 紧急压力
    if (/马上|立即|最后机会|错过/.test(argument)) {
      darkPatterns.push({
        type: 'artificial_scarcity',
        description: '人为制造的紧迫感',
        counter: '质疑时间限制的合理性，要求延期决策'
      });
    }

    return darkPatterns;
  }

  // 辅助方法
  _calculatePositionEffect(position, total) {
    // 首因效应和近因效应
    if (position === 0) return 0.15; // 首位
    if (position === total - 1) return 0.1; // 末位
    return 0;
  }

  _applyFrame(description, frame, option) {
    if (frame === 'gain') {
      return `通过选择${option.label}，您将获得${description}`;
    } else if (frame === 'loss') {
      return `如果不选择${option.label}，您将错失${description}`;
    }
    return description;
  }

  _reframeDescription(desc, frameType) {
    if (frameType === 'gain' && desc.includes('避免')) {
      return desc.replace('避免', '获得');
    } else if (frameType === 'loss' && desc.includes('获得')) {
      return desc.replace('获得', '避免失去');
    }
    return desc;
  }

  _predictChoice(arrangedOptions) {
    // 基于架构预测最可能被选择的选项
    const scored = arrangedOptions.map(opt => ({
      ...opt,
      choiceScore: (opt.isDefault ? 0.4 : 0) +
                   (opt.positionEffect || 0) +
                   (opt.highlightBoost || 0) +
                   (opt.socialBoost || 0) +
                   (opt.popularity || 0) * 0.2
    }));
    return scored.reduce((max, curr) => curr.choiceScore > max.choiceScore ? curr : max);
  }

  _calculateNudgeStrength(arrangedOptions) {
    const totalBoost = arrangedOptions.reduce((sum, opt) => 
      sum + (opt.defaultBoost || 0) + (opt.highlightBoost || 0) + (opt.socialBoost || 0),
    0);
    return Math.min(totalBoost / arrangedOptions.length, 1);
  }

  _generateRecommendation(gap, progress) {
    if (gap <= 0) return '已达成目标，保持当前行为';
    if (progress < 0.3) return '需要显著改变，考虑使用承诺机制';
    if (progress < 0.7) return '进展良好，增加反馈频率以维持动力';
    return '接近目标，利用社会比较强化行为';
  }

  _extractDimensions(options, dimension) {
    const values = [...new Set(options.map(o => o[dimension]).filter(Boolean))];
    return values.map(v => ({ value: v, count: options.filter(o => o[dimension] === v).length }));
  }
}

module.exports = { NudgeTheoryEngine };
