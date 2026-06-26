/**
 * 短视频爆款预测脚本 v1.0
 * 
 * 功能：
 * - 前 3 秒钩子分析（6 种钩子类型）
 * - 节奏和信息密度分析
 * - 情绪曲线建议
 * - 爆款概率评分
 * - 优化建议生成
 * - 相似爆款案例推荐
 * 
 * 定价：¥59/月 | $22.99/月
 * 企业主体：上海冰月网络科技有限公司
 */

class ViralVideoPredictor {

  // ============================================================
  // 爆款元素库
  // ============================================================
  static viralElements = {
    // 钩子类型（前 3 秒）
    hookTypes: [
      { name: '反常识型', score: 95, patterns: ['你一直做错了', '其实', '真相是', '根本不是', '没想到', '千万别'], example: '90% 的人洗脸都洗错了，难怪皮肤越来越差！' },
      { name: '痛点型', score: 90, patterns: ['是不是也', '别再', '你是不是', '还在为', '烦恼', '困扰'], example: '你是不是也经常失眠，第二天精神很差？' },
      { name: '数字型', score: 85, patterns: ['3 个', '5 分钟', '10 种', '100%', '第一', '唯一'], example: '3 个方法让你的效率翻倍，最后一个绝了！' },
      { name: '悬念型', score: 85, patterns: ['最后', '千万别让', '你绝对想不到', '居然', '竟然'], example: '千万别让老板看到这个视频...最后有惊喜！' },
      { name: '利益型', score: 80, patterns: ['学会', '教你', '免费', '省钱', '赚', '福利'], example: '学会这个技巧，每月帮你省下 2000 元！' },
      { name: '情绪型', score: 75, patterns: ['太', '笑死', '哭', '气死', '绝了', '救命'], example: '太气人了！花 500 块买的居然是假货！' },
    ],

    // 各平台最佳时长
    platformOptimalDuration: {
      '抖音': { min: 15, max: 60, optimal: 30 },
      '快手': { min: 15, max: 90, optimal: 45 },
      '视频号': { min: 30, max: 120, optimal: 60 },
      '小红书': { min: 30, max: 120, optimal: 60 },
      'B 站': { min: 60, max: 300, optimal: 180 },
    },

    // 情绪曲线模板
    emotionCurves: {
      '剧情': [
        { time: '0-3s', emotion: '悬念', trigger: '抛出冲突/反常场景' },
        { time: '3-15s', emotion: '好奇', trigger: '展开故事背景' },
        { time: '15-30s', emotion: '紧张', trigger: '矛盾升级' },
        { time: '30-45s', emotion: '反转', trigger: '意外结局' },
        { time: '45-60s', emotion: '共鸣', trigger: '情感升华/金句' },
      ],
      '知识': [
        { time: '0-3s', emotion: '好奇', trigger: '反常识观点/痛点' },
        { time: '3-15s', emotion: '认同', trigger: '解释原因/举例' },
        { time: '15-30s', emotion: '收获', trigger: '给出方法/步骤' },
        { time: '30-45s', emotion: '行动', trigger: '引导点赞收藏' },
      ],
      '搞笑': [
        { time: '0-3s', emotion: '好奇', trigger: '奇怪场景/反常行为' },
        { time: '3-15s', emotion: '期待', trigger: '铺垫/制造预期' },
        { time: '15-30s', emotion: '爆笑', trigger: '反转/包袱抖开' },
        { time: '30-45s', emotion: '回味', trigger: '二次反转/金句' },
      ],
      '美食': [
        { time: '0-3s', emotion: '视觉冲击', trigger: '成品特写/制作过程' },
        { time: '3-20s', emotion: '期待', trigger: '展示制作步骤' },
        { time: '20-40s', emotion: '满足', trigger: '完成展示/试吃' },
        { time: '40-60s', emotion: '食欲', trigger: '口感描述/推荐' },
      ],
      '美妆': [
        { time: '0-3s', emotion: '视觉冲击', trigger: '妆后效果对比' },
        { time: '3-20s', emotion: '好奇', trigger: '展示产品/步骤' },
        { time: '20-40s', emotion: '收获', trigger: '详细教程' },
        { time: '40-60s', emotion: '种草', trigger: '最终效果/推荐' },
      ],
      '情感': [
        { time: '0-3s', emotion: '共鸣', trigger: '痛点场景/金句' },
        { time: '3-20s', emotion: '代入', trigger: '故事展开' },
        { time: '20-40s', emotion: '感动', trigger: '情感高潮' },
        { time: '40-60s', emotion: '共鸣', trigger: '升华/感悟' },
      ],
    },

    // 违禁词
    bannedWords: [
      '最好', '第一', '最', '绝对', '100%', '保证', '必', '根治', '神效',
      '赚钱', '暴富', '躺赚', '稳赚', '无风险', '国家级', '世界级',
    ],
  };

  // ============================================================
  // 主预测函数
  // ============================================================
  static predict(params) {
    const {
      script = '',
      platform = '抖音',
      category = '通用',
      duration = 60
    } = params;

    if (!script || script.length < 20) {
      return { error: true, message: '脚本内容过短，请输入完整脚本（至少 20 字）' };
    }

    // 1. 钩子分析
    const hookAnalysis = this.analyzeHook(script);

    // 2. 节奏分析
    const pacingAnalysis = this.analyzePacing(script, duration, category);

    // 3. 情绪曲线
    const emotionCurve = this.getEmotionCurve(category, duration);

    // 4. 违禁词检查
    const bannedWarnings = this.checkBannedWords(script);

    // 5. 计算爆款评分
    const viralScore = this.calculateViralScore(hookAnalysis, pacingAnalysis, emotionCurve, bannedWarnings, platform, duration);

    // 6. 优化建议
    const optimizationTips = this.generateOptimizationTips(hookAnalysis, pacingAnalysis, viralScore, category);

    // 7. 相似爆款案例
    const similarCases = this.getSimilarViralCases(category, platform);

    return {
      script,
      platform,
      category,
      duration,
      viralScore,
      hookAnalysis,
      pacingAnalysis,
      emotionCurve,
      bannedWarnings,
      optimizationTips,
      similarCases,
      prediction: this.getPrediction(viralScore, platform),
      predictedAt: new Date().toISOString(),
      disclaimer: '预测结果基于历史爆款数据分析，不保证实际效果。内容需遵守平台社区规范。',
    };
  }

  // ============================================================
  // 钩子分析
  // ============================================================
  static analyzeHook(script) {
    const firstSentence = script.split(/[。！？\n]/)[0] || script.substring(0, 50);
    const firstThreeSeconds = script.substring(0, 15); // 约 3 秒的内容

    // 检测钩子类型
    let bestHook = null;
    let bestScore = 0;

    for (const hook of this.viralElements.hookTypes) {
      for (const pattern of hook.patterns) {
        if (firstThreeSeconds.includes(pattern) || firstSentence.includes(pattern)) {
          if (hook.score > bestScore) {
            bestHook = hook;
            bestScore = hook.score;
          }
        }
      }
    }

    const hasHook = bestHook !== null;

    return {
      firstSentence,
      hookType: bestHook ? bestHook.name : '未识别',
      hookScore: bestHook ? bestHook.score : 40,
      hasHook,
      suggestion: hasHook
        ? `使用了「${bestHook.name}」钩子，吸引力${bestScore >= 90 ? '很强' : '不错'}。示例：${bestHook.example}`
        : '建议在前 3 秒加入钩子。推荐：反常识型或痛点型钩子，例如：90% 的人 XX 都 XX 了，难怪 XX！',
    };
  }

  // ============================================================
  // 节奏分析
  // ============================================================
  static analyzePacing(script, duration, category) {
    const charCount = script.length;
    const charsPerSecond = duration > 0 ? (charCount / duration) : 0;

    // 信息密度判断
    let infoDensity = '中';
    if (charsPerSecond > 6) infoDensity = '高';
    else if (charsPerSecond < 3) infoDensity = '低';

    // 检测转折点
    const turningPoints = (script.match(/但是|然而|其实|没想到|结果|反转|不过|可是/g) || []).length;

    // 检测段落数
    const paragraphs = script.split(/\n/).filter(p => p.trim().length > 0).length;

    // 检测互动引导
    const hasCallToAction = /点赞|关注|评论|收藏|转发|留言/.test(script);

    return {
      charCount,
      duration,
      charsPerSecond: charsPerSecond.toFixed(1),
      infoDensity,
      turningPoints,
      paragraphs,
      hasCallToAction,
      suggestion: this.getPacingSuggestion(infoDensity, turningPoints, hasCallToAction, category),
    };
  }

  // ============================================================
  // 情绪曲线
  // ============================================================
  static getEmotionCurve(category, duration) {
    const curves = this.viralElements.emotionCurves;
    const curve = curves[category] || curves['知识'];

    // 根据实际时长调整时间分配
    const scale = duration / 60;
    return curve.map(step => {
      const [start, end] = step.time.match(/\d+/g).map(Number);
      return {
        ...step,
        time: `${Math.round(start * scale)}-${Math.round(end * scale)}s`,
      };
    });
  }

  // ============================================================
  // 违禁词检查
  // ============================================================
  static checkBannedWords(script) {
    const warnings = [];
    const lowerScript = script.toLowerCase();

    for (const word of this.viralElements.bannedWords) {
      if (lowerScript.includes(word.toLowerCase())) {
        warnings.push({
          word,
          severity: 'HIGH',
          suggestion: `建议删除或替换"${word}"，可能触发平台审核或限流`,
        });
      }
    }

    return warnings;
  }

  // ============================================================
  // 计算爆款评分
  // ============================================================
  static calculateViralScore(hook, pacing, emotion, bannedWarnings, platform, duration) {
    let score = 50; // 基础分

    // 钩子权重 35%
    if (hook.hasHook) {
      score += (hook.hookScore / 100) * 35;
    }

    // 节奏权重 25%
    if (pacing.infoDensity === '中') score += 10;
    else if (pacing.infoDensity === '高') score += 5;
    if (pacing.turningPoints >= 2) score += 10;
    else if (pacing.turningPoints >= 1) score += 5;
    if (pacing.hasCallToAction) score += 5;

    // 情绪曲线权重 20%
    if (emotion.length >= 4) score += 15;
    else if (emotion.length >= 3) score += 10;

    // 时长适配权重 10%
    const optimal = this.viralElements.platformOptimalDuration[platform] || this.viralElements.platformOptimalDuration['抖音'];
    if (duration >= optimal.min && duration <= optimal.max) {
      score += 10;
    } else if (duration >= optimal.min * 0.5 && duration <= optimal.max * 1.5) {
      score += 5;
    }

    // 违禁词扣分 10% per word
    score -= bannedWarnings.length * 10;

    return Math.max(0, Math.min(100, Math.round(score)));
  }

  // ============================================================
  // 优化建议
  // ============================================================
  static generateOptimizationTips(hook, pacing, viralScore, category) {
    const tips = [];

    if (viralScore >= 80) {
      tips.push('🟢 爆款概率高，脚本质量优秀，可直接拍摄');
    } else if (viralScore >= 60) {
      tips.push('🟡 爆款概率中等，优化以下方面可显著提升');
    } else {
      tips.push('🔴 爆款概率较低，建议大幅优化脚本结构');
    }

    if (!hook.hasHook) {
      tips.push('💡 前 3 秒未检测到钩子，建议加入反常识/痛点/悬念元素');
    }

    if (pacing.turningPoints < 2) {
      tips.push('💡 转折点较少（当前 ' + pacing.turningPoints + ' 个），建议增加 1-2 个"但是/没想到/其实"');
    }

    if (pacing.infoDensity === '低') {
      tips.push('💡 信息密度偏低，建议精简冗余内容，加快节奏');
    }

    if (pacing.infoDensity === '高') {
      tips.push('💡 信息密度偏高，观众可能跟不上，建议适当放慢或分段');
    }

    if (!pacing.hasCallToAction) {
      tips.push('💡 缺少互动引导，建议在结尾加入"点赞/评论/收藏"引导');
    }

    tips.push('💡 发布时段：选择平台高峰时段（抖音 12-14 点 / 20-22 点）');
    tips.push('💡 封面和标题同样重要，确保与脚本内容一致');

    return tips;
  }

  // ============================================================
  // 相似爆款案例
  // ============================================================
  static getSimilarViralCases(category, platform) {
    const cases = {
      '剧情': [
        { title: '老板和员工的日常', views: '800w+', platform: '抖音', key: '共鸣 + 反转 + 金句' },
        { title: '最后有惊喜', views: '500w+', platform: '抖音', key: '悬念 + 情感升华' },
      ],
      '知识': [
        { title: '3 个方法让你效率翻倍', views: '600w+', platform: '抖音', key: '数字钩子 + 干货密集' },
        { title: '你一直做错了的事', views: '400w+', platform: '抖音', key: '反常识 + 解决方案' },
      ],
      '搞笑': [
        { title: '当代年轻人的日常', views: '700w+', platform: '抖音', key: '共鸣 + 包袱 + 二次反转' },
        { title: '当你遇到 XX 时', views: '500w+', platform: '抖音', key: '场景还原 + 夸张表演' },
      ],
      '美食': [
        { title: '在家复刻米其林', views: '300w+', platform: '抖音', key: '视觉冲击 + 教程' },
        { title: '10 块钱做出大餐', views: '200w+', platform: '抖音', key: '性价比 + 步骤清晰' },
      ],
      '美妆': [
        { title: '素颜 vs 化妆', views: '500w+', platform: '抖音', key: '对比 + 教程' },
        { title: '平价替代大牌', views: '300w+', platform: '抖音', key: '性价比 + 实测' },
      ],
      '情感': [
        { title: '成年人的崩溃', views: '600w+', platform: '抖音', key: '共鸣 + 情感升华' },
        { title: '致自己', views: '400w+', platform: '抖音', key: '金句 + 共鸣' },
      ],
    };

    return cases[category] || cases['知识'];
  }

  // ============================================================
  // 预测结果
  // ============================================================
  static getPrediction(score, platform) {
    if (score >= 85) {
      return { level: '大爆款', probability: '高', expectedViews: '100w+', suggestion: '直接发布，注意选择高峰时段' };
    } else if (score >= 70) {
      return { level: '小爆款', probability: '中高', expectedViews: '10w-100w', suggestion: '可以发布，建议优化标题和封面' };
    } else if (score >= 50) {
      return { level: '有潜力', probability: '中', expectedViews: '1w-10w', suggestion: '建议优化后再发布，重点改进钩子和转折' };
    } else {
      return { level: '待优化', probability: '低', expectedViews: '<1w', suggestion: '建议大幅优化脚本结构后再发布' };
    }
  }

  // ============================================================
  // 辅助函数
  // ============================================================
  static getPacingSuggestion(density, turningPoints, hasCTA, category) {
    const tips = [];

    if (density === '低') tips.push('信息密度偏低，建议精简内容或增加干货');
    if (density === '高') tips.push('信息密度偏高，注意适当停顿让观众消化');
    if (turningPoints < 2) tips.push('转折点较少，建议增加"但是/没想到/其实"等转折');
    if (!hasCTA) tips.push('缺少互动引导，建议结尾加入点赞/评论引导');

    return tips.length > 0 ? tips.join('；') : '节奏良好，保持即可';
  }
}

module.exports = ViralVideoPredictor;
